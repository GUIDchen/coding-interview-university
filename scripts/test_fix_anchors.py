"""Unit tests for the anchor repair tool (scripts/fix_anchors.py).

Run with::

    python3 -m unittest discover -s scripts -p 'test_*.py'

All tests use temporary files; none of them modify the repository.
"""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import fix_anchors


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


def run_main(argv: list[str]) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = fix_anchors.main(argv)
    assert code == 0
    return buffer.getvalue()


class RuleTests(unittest.TestCase):
    def test_rule_1_lowercase_target(self) -> None:
        text = "## What Is It\n\n[What is it?](#What-Is-It)\n"
        repairs = fix_anchors.plan_repairs(text)

        self.assertEqual(len(repairs), 1)
        self.assertEqual(repairs[0].rule, 1)
        self.assertEqual(repairs[0].old_target, "#What-Is-It")
        self.assertEqual(repairs[0].new_target, "#what-is-it")
        self.assertIn("(#what-is-it)", fix_anchors.repair_text(text)[0])

    def test_rule_1_percent_encoded_target(self) -> None:
        text = "## Über uns\n\n[x](#%C3%9Cber-uns)\n"
        repairs = fix_anchors.plan_repairs(text)

        self.assertEqual(len(repairs), 1)
        self.assertEqual(repairs[0].rule, 1)
        self.assertEqual(repairs[0].new_target, "#über-uns")

    def test_rule_2_link_text(self) -> None:
        text = "## Was ist das\n\n[Was ist das?](#what-is-it)\n"
        repairs = fix_anchors.plan_repairs(text)

        self.assertEqual(len(repairs), 1)
        self.assertEqual(repairs[0].rule, 2)
        self.assertEqual(repairs[0].new_target, "#was-ist-das")

    def test_rule_2_takes_precedence_over_rule_3(self) -> None:
        text = "## Alpha\n\n## Beta\n\n[Alpha](#Beta%21)\n"
        repairs = fix_anchors.plan_repairs(text)

        self.assertEqual(len(repairs), 1)
        self.assertEqual(repairs[0].rule, 2)
        self.assertEqual(repairs[0].new_target, "#alpha")

    def test_rule_3_slugified_target(self) -> None:
        text = "## Hello, World!\n\n[x](#Hello%2C%20World%21)\n"
        repairs = fix_anchors.plan_repairs(text)

        self.assertEqual(len(repairs), 1)
        self.assertEqual(repairs[0].rule, 3)
        self.assertEqual(repairs[0].new_target, "#hello-world")

    def test_rule_3_unquoted_target(self) -> None:
        text = "## Trees - Intro\n\n[x](#Trees%20-%20Intro)\n"
        repairs = fix_anchors.plan_repairs(text)

        self.assertEqual(len(repairs), 1)
        self.assertEqual(repairs[0].rule, 3)
        self.assertEqual(repairs[0].new_target, "#trees---intro")

    def test_duplicate_heading_slug_is_a_valid_anchor(self) -> None:
        text = "## Topic\n\n## Topic\n\n[x](#Topic-1)\n"
        repairs = fix_anchors.plan_repairs(text)

        self.assertEqual(len(repairs), 1)
        self.assertEqual(repairs[0].rule, 1)
        self.assertEqual(repairs[0].new_target, "#topic-1")


class NoOpTests(unittest.TestCase):
    def test_valid_anchor_is_untouched(self) -> None:
        text = "## What Is It\n\n[x](#what-is-it)\n"
        self.assertEqual(fix_anchors.plan_repairs(text), [])

    def test_unresolvable_anchor_is_untouched(self) -> None:
        text = "## What Is It\n\n[x](#no-such-heading)\n"
        self.assertEqual(fix_anchors.plan_repairs(text), [])

    def test_bare_hash_is_untouched(self) -> None:
        text = "## What Is It\n\n[x](#)\n"
        self.assertEqual(fix_anchors.plan_repairs(text), [])

    def test_external_link_is_untouched(self) -> None:
        text = "## What Is It\n\n[x](https://example.com/a#broken)\n"
        self.assertEqual(fix_anchors.plan_repairs(text), [])

    def test_image_is_untouched(self) -> None:
        text = "## What Is It\n\n![x](#missing)\n"
        self.assertEqual(fix_anchors.plan_repairs(text), [])

    def test_fenced_code_is_untouched(self) -> None:
        text = "## What Is It\n\n~~~\n[x](#missing)\n~~~\n"
        self.assertEqual(fix_anchors.plan_repairs(text), [])

    def test_inline_code_is_untouched(self) -> None:
        tick = chr(96)
        text = "## What Is It\n\n" + tick + "[x](#missing)" + tick + "\n"
        self.assertEqual(fix_anchors.plan_repairs(text), [])

    def test_anchor_in_another_file_is_not_reused(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            first = directory / "first.md"
            second = directory / "second.md"
            first.write_text("## Was ist das\n", encoding="utf-8")
            second.write_text(
                "## Other\n\n[Was ist das?](#what-is-it)\n",
                encoding="utf-8",
            )
            result = fix_anchors.repair_file(second)

        self.assertEqual(result.repairs, [])
        self.assertEqual(result.after, result.before)

    def test_already_valid_file_is_not_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "ok.md"
            original = "## What Is It\n\n[x](#what-is-it)\n"
            path.write_text(original, encoding="utf-8")
            output = run_main(["--files", str(path), "--write"])

            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertIn("Wrote 0 file(s).", output)


class CliTests(TempMarkdownTestCase):
    SAMPLE = "## Was ist das\n\n[Was ist das?](#what-is-it)\n"

    def test_dry_run_reports_but_does_not_write(self) -> None:
        path = self.write_markdown("README-de.md", self.SAMPLE)
        output = run_main(["--files", str(path)])

        self.assertEqual(path.read_text(encoding="utf-8"), self.SAMPLE)
        self.assertIn(":3: #what-is-it -> #was-ist-das", output)
        self.assertIn("rule 2: link text", output)
        self.assertIn("Broken anchors before: 1", output)
        self.assertIn("Broken anchors after: 0", output)
        self.assertIn("Dry run: no files written", output)

    def test_write_applies_repairs_and_is_idempotent(self) -> None:
        path = self.write_markdown("README-de.md", self.SAMPLE)
        output = run_main(["--files", str(path), "--write"])

        repaired = path.read_text(encoding="utf-8")
        self.assertIn("(#was-ist-das)", repaired)
        self.assertIn("Wrote 1 file(s).", output)

        second_output = run_main(["--files", str(path), "--write"])
        self.assertEqual(path.read_text(encoding="utf-8"), repaired)
        self.assertIn("Repairs: 0", second_output)
        self.assertIn("Broken anchors before: 0", second_output)

    def test_external_links_and_titles_are_preserved(self) -> None:
        text = (
            "## Was ist das\n\n"
            "[ext](https://example.com/a#b) and "
            '[Was ist das?](#what-is-it "Titel")\n'
        )
        repaired, repairs = fix_anchors.repair_text(text)

        self.assertEqual(len(repairs), 1)
        self.assertIn("https://example.com/a#b", repaired)
        self.assertIn('(#was-ist-das "Titel")', repaired)

    def test_malformed_destination_with_spaces_is_cleaned(self) -> None:
        text = (
            "## यह क्या है\n\n"
            "[यह क्या है?](#क्या-क्या है-यह)\n"
        )
        repaired, repairs = fix_anchors.repair_text(text)

        self.assertEqual(len(repairs), 1)
        self.assertIn("(#यह-क्या-है)", repaired)
        self.assertNotIn("है-यह", repaired)

    def test_crlf_line_endings_are_preserved(self) -> None:
        text = "## Was ist das\r\n\r\n[Was ist das?](#what-is-it)\r\n"
        repaired, repairs = fix_anchors.repair_text(text)

        self.assertEqual(len(repairs), 1)
        self.assertEqual(repaired.count("\r\n"), 3)
        self.assertIn("(#was-ist-das)\r\n", repaired)

    def test_write_preserves_crlf_file(self) -> None:
        path = self.tempdir / "README-de.md"
        path.write_bytes(
            b"## Was ist das\r\n\r\n[Was ist das?](#what-is-it)\r\n"
        )
        run_main(["--files", str(path), "--write"])

        data = path.read_bytes()
        self.assertIn(b"(#was-ist-das)", data)
        self.assertEqual(data.count(b"\n"), data.count(b"\r\n"))
        self.assertNotIn(b"\r\r\n", data)

    def test_write_preserves_lf_file(self) -> None:
        path = self.tempdir / "README-de.md"
        path.write_bytes(self.SAMPLE.encode("utf-8"))
        run_main(["--files", str(path), "--write"])

        data = path.read_bytes()
        self.assertIn(b"(#was-ist-das)", data)
        self.assertNotIn(b"\r", data)


if __name__ == "__main__":
    unittest.main()
