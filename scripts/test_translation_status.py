"""Unit tests for the translation status dashboard.

Run with::

    python3 -m unittest discover -s scripts -p 'test_*.py'

All tests use temporary files or in-memory text; none of them modify the
repository.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import translation_status as status


class ClassifyTests(unittest.TestCase):
    def test_healthy(self) -> None:
        self.assertEqual(
            status.classify(111, 463, 0, 95.0), status.STATUS_HEALTHY
        )

    def test_healthy_boundaries(self) -> None:
        self.assertEqual(
            status.classify(
                111, 80, 0, 90.0, en_checkboxes=100
            ),
            status.STATUS_HEALTHY,
        )
        self.assertEqual(
            status.classify(
                111, 120, 0, 90.0, en_checkboxes=100
            ),
            status.STATUS_HEALTHY,
        )
        self.assertEqual(
            status.classify(
                111, 79, 0, 90.0, en_checkboxes=100
            ),
            status.STATUS_NEEDS_SYNC,
        )
        self.assertEqual(
            status.classify(
                111, 121, 0, 90.0, en_checkboxes=100
            ),
            status.STATUS_NEEDS_SYNC,
        )

    def test_stub_by_heading_count_even_if_otherwise_healthy(self) -> None:
        self.assertEqual(
            status.classify(49, 463, 0, 100.0), status.STATUS_STUB
        )

    def test_stub_by_checkbox_count(self) -> None:
        self.assertEqual(
            status.classify(111, 231, 0, 100.0), status.STATUS_STUB
        )

    def test_needs_sync_when_checkbox_count_is_just_above_stub(self) -> None:
        self.assertEqual(
            status.classify(111, 232, 0, 100.0), status.STATUS_NEEDS_SYNC
        )

    def test_needs_sync_for_broken_anchors(self) -> None:
        self.assertEqual(
            status.classify(111, 463, 1, 100.0), status.STATUS_NEEDS_SYNC
        )

    def test_needs_sync_for_low_coverage(self) -> None:
        self.assertEqual(
            status.classify(111, 463, 0, 89.9), status.STATUS_NEEDS_SYNC
        )

    def test_needs_sync_for_checkbox_ratio_above_range(self) -> None:
        self.assertEqual(
            status.classify(111, 556, 0, 100.0), status.STATUS_NEEDS_SYNC
        )


class MetricTests(unittest.TestCase):
    def test_count_checkboxes(self) -> None:
        text = (
            "# Title\n\n"
            "- [ ] one\n"
            "- [x] two\n"
            "  - [X] nested\n"
            "~~~\n"
            "- [ ] inside a fence\n"
            "~~~\n"
        )
        self.assertEqual(status.count_checkboxes(text), 3)

    def test_extract_urls_ignores_internal_links(self) -> None:
        text = (
            "## Heading\n\n"
            "[internal](#heading) [external](https://example.com/a)\n"
            "![image](images/pic.png)\n"
        )
        self.assertEqual(
            status.extract_urls(text),
            ["https://example.com/a", "images/pic.png"],
        )

    def test_extract_urls_is_empty_without_links(self) -> None:
        self.assertEqual(status.extract_urls("## Heading\n"), [])

    def test_coverage_percent(self) -> None:
        self.assertEqual(
            status.coverage_percent({"a", "b", "c"}, {"a", "c"}), 200 / 3
        )
        self.assertEqual(status.coverage_percent(set(), set()), 100.0)

    def test_language_map_covers_all_codes(self) -> None:
        expected = {
            "af", "ar", "bg", "bn", "cn", "de", "el", "es", "fa", "fr",
            "he", "hi", "id", "it", "ja", "kh", "kk", "ko", "mr", "nl",
            "pl", "ptbr", "ru", "th", "tr", "tw", "uk", "ur", "uz", "vi",
        }
        self.assertEqual(set(status.LANGUAGES), expected)
        self.assertEqual(len(status.LANGUAGES), 30)
        self.assertTrue(all(status.LANGUAGES.values()))

    def test_language_code_from_path(self) -> None:
        self.assertEqual(
            status.language_code(Path("translations/README-ptbr.md")),
            "ptbr",
        )


class ReportTests(unittest.TestCase):
    def make_entries(self) -> list[status.Entry]:
        return [
            status.Entry(
                "bn", "Bengali", "translations/README-bn.md",
                105, 84, 46, 17.8, status.STATUS_STUB,
            ),
            status.Entry(
                "de", "German", "translations/README-de.md",
                103, 738, 17, 75.5, status.STATUS_NEEDS_SYNC,
            ),
            status.Entry(
                "cn", "Chinese (Simplified)", "translations/README-cn.md",
                111, 463, 0, 93.2, status.STATUS_HEALTHY,
            ),
        ]

    def make_report(self) -> status.Report:
        return status.Report(
            entries=self.make_entries(),
            en_headings=111,
            en_checkboxes=463,
            en_urls=730,
            date="2026-10-29",
        )

    def test_sort_entries_by_status_then_coverage(self) -> None:
        entries = status.sort_entries(self.make_entries())
        self.assertEqual(
            [entry.code for entry in entries], ["cn", "de", "bn"]
        )

    def test_status_counts(self) -> None:
        counts = status.status_counts(self.make_entries())
        self.assertEqual(counts[status.STATUS_HEALTHY], 1)
        self.assertEqual(counts[status.STATUS_NEEDS_SYNC], 1)
        self.assertEqual(counts[status.STATUS_STUB], 1)

    def test_markdown_contains_method_date_table_and_note(self) -> None:
        markdown = status.render_markdown(self.make_report())

        self.assertIn("# Translation Status", markdown)
        self.assertIn("Snapshot date: 2026-10-29", markdown)
        self.assertIn("## Method", markdown)
        self.assertIn(
            "| Language | Code | Headings (EN 111) | Checkboxes (EN 463) "
            "| Broken anchors | EN URL coverage | Status |",
            markdown,
        )
        self.assertIn(
            "| [German](translations/README-de.md) | de | 103 | 738 | 17 | 75.5% | Needs sync |",
            markdown,
        )
        self.assertIn("**Summary:** 1 Healthy, 1 Needs sync, 1 Stub.", markdown)
        self.assertIn("CONTRIBUTING.md", markdown)
        self.assertIn("This is a snapshot generated on 2026-10-29", markdown)

    def test_markdown_rows_are_sorted(self) -> None:
        markdown = status.render_markdown(self.make_report())
        healthy = markdown.index("| [Chinese (Simplified)]")
        needs_sync = markdown.index("| [German]")
        stub = markdown.index("| [Bengali]")
        self.assertLess(healthy, needs_sync)
        self.assertLess(needs_sync, stub)

    def test_text_output_has_summary(self) -> None:
        text = status.render_text(self.make_report())
        self.assertIn("Summary: 1 Healthy, 1 Needs sync, 1 Stub", text)
        self.assertIn("EN baseline: README.md", text)
        self.assertIn("93.2%", text)

    def test_report_as_dict_is_json_serialisable(self) -> None:
        data = status.report_as_dict(self.make_report())
        encoded = json.dumps(data, ensure_ascii=False)
        self.assertIn('"snapshot_date": "2026-10-29"', encoded)

        self.assertEqual(data["baseline"]["headings"], 111)
        self.assertEqual(data["baseline"]["checkboxes"], 463)
        self.assertEqual(data["baseline"]["urls"], 730)
        self.assertEqual(data["summary"][status.STATUS_HEALTHY], 1)
        self.assertEqual(data["translations"][0]["code"], "cn")
        self.assertEqual(data["translations"][0]["en_url_coverage"], 93.2)


class BuildReportTests(unittest.TestCase):
    def test_build_report_from_files(self) -> None:
        en_text = "# EN\n\n## Intro\n\n- [ ] one\n\n[x](https://e.com)\n"
        tr_text = "# TR\n\n## Intro\n\n- [ ] one\n\n[x](https://e.com)\n"

        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            path = directory / "README-de.md"
            path.write_text(tr_text, encoding="utf-8")
            report = status.build_report([path], en_text)

        entry = report.entries[0]
        self.assertEqual(entry.code, "de")
        self.assertEqual(entry.language, "German")
        self.assertEqual(entry.headings, 2)
        self.assertEqual(entry.checkboxes, 1)
        self.assertEqual(entry.broken_anchors, 0)
        self.assertEqual(entry.coverage, 100.0)
        self.assertEqual(entry.status, status.STATUS_STUB)
        self.assertEqual(report.en_headings, 2)
        self.assertEqual(report.en_checkboxes, 1)
        self.assertEqual(report.en_urls, 1)


if __name__ == "__main__":
    unittest.main()
