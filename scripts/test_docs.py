"""Unit tests for the documentation tooling in this directory.

Run with::

    python3 -m unittest discover -s scripts -p 'test_*.py'

All tests use temporary files; none of them modify the repository.
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import check_docs
import progress


class TempMarkdownTestCase(unittest.TestCase):
    """Base class that creates an isolated temporary directory."""

    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory()
        self.tempdir = Path(self._tempdir.name)

    def tearDown(self) -> None:
        self._tempdir.cleanup()

    def write_markdown(self, name: str, text: str) -> Path:
        path = self.tempdir / name
        path.write_text(text, encoding="utf-8")
        return path


class SlugTests(unittest.TestCase):
    def test_english_punctuation_and_spaces(self) -> None:
        self.assertEqual(check_docs.slugify("What is it?"), "what-is-it")
        self.assertEqual(
            check_docs.slugify("Don't feel you aren't smart enough"),
            "dont-feel-you-arent-smart-enough",
        )
        self.assertEqual(
            check_docs.slugify("Trees - Intro"), "trees---intro"
        )
        self.assertEqual(
            check_docs.slugify(
                "Algorithmic complexity / Big-O / Asymptotic analysis"
            ),
            "algorithmic-complexity--big-o--asymptotic-analysis",
        )
        self.assertEqual(
            check_docs.slugify("Combinatorics (n choose k) & Probability"),
            "combinatorics-n-choose-k--probability",
        )

    def test_symbols_are_removed(self) -> None:
        self.assertEqual(check_docs.slugify("A*搜索算法"), "a搜索算法")
        self.assertEqual(check_docs.slugify("C++"), "c")
        self.assertEqual(
            check_docs.slugify("Unix/Linux command line tools"),
            "unixlinux-command-line-tools",
        )

    def test_cjk_punctuation_is_removed(self) -> None:
        self.assertEqual(check_docs.slugify("树（Trees）"), "树trees")
        self.assertEqual(check_docs.slugify("数组（Arrays）"), "数组arrays")
        self.assertEqual(check_docs.slugify("这是？"), "这是")
        self.assertEqual(
            check_docs.slugify("系统设计、可扩展性和数据处理"),
            "系统设计可扩展性和数据处理",
        )
        self.assertEqual(check_docs.slugify("树——介绍"), "树介绍")
        self.assertEqual(check_docs.slugify("“引号”"), "引号")
        self.assertEqual(
            check_docs.slugify("NP, NP-Completeness和近似算法"),
            "np-np-completeness和近似算法",
        )


class HeadingTests(TempMarkdownTestCase):
    def test_bullet_headings_are_anchors(self) -> None:
        path = self.write_markdown(
            "bullet.md",
            "\n".join(
                [
                    "# Title",
                    "",
                    "- [Topic](#topic)",
                    "- ### Topic",
                    "",
                    "- [Sub](#sub-topic)",
                    "    - ### Sub Topic",
                    "",
                    "- [A star](#a)",
                    "- ### A*",
                    "",
                ]
            ),
        )

        analysis = check_docs.analyze_file(path)
        self.assertEqual(
            [heading.slug for heading in analysis.headings],
            ["title", "topic", "sub-topic", "a"],
        )
        self.assertEqual(analysis.broken, [])

    def test_duplicate_headings_get_github_suffixes(self) -> None:
        path = self.write_markdown(
            "duplicates.md",
            "## Topic\n### Topic\n[first](#topic)\n[second](#topic-1)\n",
        )

        analysis = check_docs.analyze_file(path)
        self.assertEqual(
            [heading.slug for heading in analysis.headings],
            ["topic", "topic-1"],
        )
        self.assertEqual(analysis.broken, [])

    def test_link_inside_inline_code_is_ignored(self) -> None:
        tick = chr(96)
        path = self.write_markdown(
            "inline-code.md",
            "## Real\n" + tick + "[bad](#missing)" + tick + "\n[ok](#real)\n",
        )

        analysis = check_docs.analyze_file(path)
        self.assertEqual([link.target for link in analysis.links], ["#real"])
        self.assertEqual(analysis.broken, [])


class CodeFenceTests(TempMarkdownTestCase):
    def test_check_docs_ignores_fenced_links_and_headings(self) -> None:
        fence = chr(96) * 3
        path = self.write_markdown(
            "fenced.md",
            "\n".join(
                [
                    "## Real",
                    "[ok](#real)",
                    fence + "markdown",
                    "## Fake",
                    "[bad](#fake)",
                    fence,
                    "Inline " + chr(96) + "[bad](#missing)" + chr(96),
                    "",
                ]
            ),
        )

        analysis = check_docs.analyze_file(path)
        self.assertEqual(
            [heading.slug for heading in analysis.headings], ["real"]
        )
        self.assertEqual([link.target for link in analysis.links], ["#real"])
        self.assertEqual(analysis.broken, [])

    def test_progress_ignores_fenced_checkboxes(self) -> None:
        fence = chr(96) * 3
        text = "\n".join(
            [
                "## Tasks",
                "- [x] keep done",
                "- [ ] keep todo",
                fence + "markdown",
                "- [ ] fenced todo",
                "## Fenced heading",
                fence,
                "- [ ] after fence",
                "",
            ]
        )

        report = progress.analyze_text(text)
        self.assertEqual(
            [(section.title, section.done, section.total) for section in report.rows],
            [("Tasks", 1, 3)],
        )
        self.assertEqual(
            [section.title for section in report.sections], ["Tasks"]
        )

    def test_progress_ignores_tilde_fences(self) -> None:
        text = "\n".join(
            [
                "## Tasks",
                "- [ ] keep",
                "~~~",
                "- [ ] ignore",
                "~~~",
                "",
            ]
        )

        report = progress.analyze_text(text)
        self.assertEqual(report.total, 1)
        self.assertEqual(report.done, 0)


class CheckboxParsingTests(unittest.TestCase):
    def test_variants_and_nested_indentation(self) -> None:
        text = "\n".join(
            [
                "- [ ] top todo",
                "  - [x] nested done",
                "    - [X] deep done",
                "* [ ] star todo",
                "+ [x] plus done",
                "- [ ]missing-space",
                "- [ ]",
                "",
            ]
        )

        report = progress.analyze_text(text)
        self.assertIsNotNone(report.preamble)
        assert report.preamble is not None
        self.assertEqual(report.preamble.done, 3)
        self.assertEqual(report.preamble.total, 6)


class ProgressAggregationTests(unittest.TestCase):
    def test_sections_and_totals(self) -> None:
        text = "\n".join(
            [
                "# Document",
                "- [x] intro",
                "## Alpha",
                "- [ ] a1",
                "- [x] a2",
                "### Nested",
                "- [x] a3",
                "## Beta",
                "- [ ] b1",
                "## Empty",
                "",
            ]
        )

        report = progress.analyze_text(text)
        self.assertEqual(
            [
                (section.title, section.done, section.total)
                for section in report.rows
            ],
            [
                ("(preamble)", 1, 1),
                ("Alpha", 2, 3),
                ("Beta", 0, 1),
            ],
        )
        self.assertEqual((report.done, report.total), (3, 5))
        self.assertAlmostEqual(report.percent, 60.0)
        self.assertIn(
            "Empty", [section.title for section in report.sections]
        )

    def test_progress_bar(self) -> None:
        self.assertEqual(progress.make_bar(0.0), "." * progress.BAR_WIDTH)
        self.assertEqual(progress.make_bar(100.0), "#" * progress.BAR_WIDTH)
        self.assertEqual(
            progress.make_bar(50.0),
            "#" * (progress.BAR_WIDTH // 2) + "." * (progress.BAR_WIDTH // 2),
        )


class ProgressCliTests(TempMarkdownTestCase):
    def test_json_output_is_machine_readable(self) -> None:
        path = self.write_markdown(
            "progress.md",
            "## Work\n- [x] one\n- [ ] two\n",
        )

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = progress.main(["--file", str(path), "--json"])

        self.assertEqual(status, 0)
        data = json.loads(output.getvalue())
        self.assertEqual(data["total"]["done"], 1)
        self.assertEqual(data["total"]["total"], 2)
        self.assertEqual(data["total"]["percent"], 50.0)
        self.assertEqual(data["sections"][0]["title"], "Work")

    def test_text_output_contains_total(self) -> None:
        path = self.write_markdown("progress.md", "## Work\n- [x] one\n")

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = progress.main(["--file", str(path)])

        self.assertEqual(status, 0)
        rendered = output.getvalue()
        self.assertIn("Work: 1/1 (100.0%)", rendered)
        self.assertIn("Total: 1/1 (100.0%)", rendered)


class BrokenLinkTests(TempMarkdownTestCase):
    def test_reports_line_text_target_and_nearest_heading(self) -> None:
        path = self.write_markdown(
            "broken.md",
            "\n".join(
                [
                    "# Title",
                    "",
                    "## Good Section",
                    "",
                    "[good](#good-section)",
                    "",
                    "[bad](#missing-anchor)",
                    "",
                ]
            ),
        )

        analysis = check_docs.analyze_file(path)
        self.assertEqual(len(analysis.links), 2)
        self.assertEqual(len(analysis.broken), 1)

        broken = analysis.broken[0]
        self.assertEqual(broken.line, 7)
        self.assertEqual(broken.text, "bad")
        self.assertEqual(broken.target, "#missing-anchor")
        self.assertIsNotNone(broken.nearest_heading)
        assert broken.nearest_heading is not None
        self.assertEqual(broken.nearest_heading.text, "Good Section")

        line = check_docs.format_broken_line("broken.md", broken)
        self.assertIn("broken.md:7", line)
        self.assertIn("[bad]", line)
        self.assertIn("#missing-anchor", line)
        self.assertIn("Good Section", line)

    def test_image_targets_are_not_checked(self) -> None:
        path = self.write_markdown(
            "image.md",
            "## Section\n![alt](#missing-anchor)\n[ok](#section)\n",
        )

        analysis = check_docs.analyze_file(path)
        self.assertEqual(len(analysis.links), 1)
        self.assertEqual(analysis.broken, [])

    def test_main_returns_one_for_broken_anchor(self) -> None:
        path = self.write_markdown(
            "broken.md", "## Section\n[bad](#missing-anchor)\n"
        )

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = check_docs.main(["--files", str(path)])

        self.assertEqual(status, 1)
        self.assertIn("BROKEN", output.getvalue())


class ParityTests(TempMarkdownTestCase):
    def test_compare_sections_reports_differences(self) -> None:
        en = "## A\n- [ ] 1\n## B\n- [ ] 1\n- [ ] 2\n## LICENSE\n"
        cn = "## 甲\n- [ ] 1\n## 乙\n- [ ] 1\n## LICENSE\n"

        result = check_docs.compare_sections(
            check_docs.count_sections(en),
            check_docs.count_sections(cn),
        )

        self.assertEqual((result.en_total, result.cn_total), (3, 2))
        self.assertTrue(
            any("section 2" in warning for warning in result.warnings)
        )
        self.assertFalse(
            any("LICENSE" in warning for warning in result.warnings)
        )

    def test_trailing_untranslated_heading_is_aligned(self) -> None:
        en = "## A\n- [ ] 1\n## Maintenance\n## LICENSE\n"
        cn = "## 甲\n- [ ] 1\n## LICENSE\n"

        result = check_docs.compare_sections(
            check_docs.count_sections(en),
            check_docs.count_sections(cn),
        )
        warnings = "\n".join(result.warnings)

        self.assertIn("Maintenance", warnings)
        self.assertNotIn("LICENSE", warnings)
        self.assertEqual(result.en_total, result.cn_total)

    def test_parity_warnings_do_not_fail_the_cli(self) -> None:
        en_path = self.write_markdown(
            "en.md", "## A\n- [ ] 1\n## LICENSE\n"
        )
        cn_path = self.write_markdown(
            "cn.md", "## 甲\n- [ ] 1\n- [ ] 2\n## LICENSE\n"
        )

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = check_docs.main(
                [
                    "--files",
                    str(en_path),
                    str(cn_path),
                    "--check-parity",
                ]
            )

        rendered = output.getvalue()
        self.assertEqual(status, 0)
        self.assertIn("Parity check", rendered)
        self.assertIn("WARNING", rendered)


if __name__ == "__main__":
    unittest.main()
