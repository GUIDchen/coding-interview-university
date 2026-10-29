#!/usr/bin/env python3
"""Data-driven status dashboard for the translation READMEs.

Usage::

    python3 scripts/translation_status.py [--json | --markdown] [--write]

        [--files PATH [PATH ...]]

By default every translations/README-*.md file is analysed and a compact
text table is printed.  --json emits machine-readable data, --markdown
emits the generated dashboard document, and --write stores that document
as TRANSLATION-STATUS.md at the repository root.

For each translation the report records the language code and name, the
heading and checkbox counts, the number of broken in-page anchors, the
percentage of the English README's unique link destinations that also
appear in the translation, and a status.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Sequence

from check_docs import (
    REPO_ROOT,
    analyze_markdown,
    display_path,
    extract_headings,
    iter_visible_lines,
    _find_matching,
    _mask_code_spans,
    _parse_destination,
    _TASK_RE,
)

SNAPSHOT_DATE = "2026-10-29"
DEFAULT_GLOB = "translations/README-*.md"
STATUS_FILE = "TRANSLATION-STATUS.md"

EN_HEADINGS = 111
EN_CHECKBOXES = 463

STATUS_HEALTHY = "Healthy"
STATUS_NEEDS_SYNC = "Needs sync"
STATUS_STUB = "Stub"

STATUS_ORDER = {
    STATUS_HEALTHY: 0,
    STATUS_NEEDS_SYNC: 1,
    STATUS_STUB: 2,
}

HEALTHY_COVERAGE = 90.0
HEALTHY_RATIO_MIN = 0.8
HEALTHY_RATIO_MAX = 1.2
STUB_HEADINGS = 50
STUB_RATIO = 0.5

BT = chr(96)

LANGUAGES = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "cn": "Chinese (Simplified)",
    "de": "German",
    "el": "Greek",
    "es": "Spanish",
    "fa": "Persian",
    "fr": "French",
    "he": "Hebrew",
    "hi": "Hindi",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "kh": "Khmer",
    "kk": "Kazakh",
    "ko": "Korean",
    "mr": "Marathi",
    "nl": "Dutch",
    "pl": "Polish",
    "ptbr": "Portuguese (Brazil)",
    "ru": "Russian",
    "th": "Thai",
    "tr": "Turkish",
    "tw": "Chinese (Traditional)",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "vi": "Vietnamese",
}


@dataclass(frozen=True)
class Entry:
    """Metrics and classification for one translation."""

    code: str
    language: str
    path: str
    headings: int
    checkboxes: int
    broken_anchors: int
    coverage: float
    status: str
    en_checkboxes: int = EN_CHECKBOXES

    @property
    def checkbox_ratio(self) -> float:
        if not self.en_checkboxes:
            return 0.0
        return self.checkboxes / self.en_checkboxes


@dataclass
class Report:
    """All translation metrics plus the English baseline."""

    entries: list[Entry] = field(default_factory=list)
    en_headings: int = EN_HEADINGS
    en_checkboxes: int = EN_CHECKBOXES
    en_urls: int = 0
    baseline_file: str = "README.md"
    date: str = SNAPSHOT_DATE


@dataclass(frozen=True)
class Destination:
    """One inline link or image destination."""

    target: str
    is_image: bool


def count_checkboxes(text: str) -> int:
    """Count GitHub task-list items outside fenced code blocks."""

    return sum(
        1
        for _lineno, line in iter_visible_lines(text)
        if _TASK_RE.match(line)
    )


def iter_destinations(line: str) -> Iterator[Destination]:
    """Yield inline link and image destinations on one line."""

    masked = _mask_code_spans(line)
    index = 0
    length = len(masked)

    while index < length:
        char = masked[index]

        if char == "\\":
            index += 2
            continue

        is_image = False
        if char == "!" and index + 1 < length and masked[index + 1] == "[":
            is_image = True
            index += 1
            char = masked[index]

        if char != "[":
            index += 1
            continue

        close = _find_matching(masked, index, "[", "]")
        if close == -1:
            index += 1
            continue

        if close + 1 >= length or masked[close + 1] != "(":
            index += 1
            continue

        end = _find_matching(masked, close + 1, "(", ")")
        if end == -1:
            index += 1
            continue

        target = _parse_destination(line[close + 2 : end])
        if target:
            yield Destination(target=target, is_image=is_image)
        index = end + 1


def extract_urls(text: str) -> list[str]:
    """Return non-fragment link destinations in source order."""

    urls: list[str] = []
    for _lineno, line in iter_visible_lines(text):
        for destination in iter_destinations(line):
            if not destination.target.startswith("#"):
                urls.append(destination.target)
    return urls


def coverage_percent(en_urls: set[str], translation_urls: set[str]) -> float:
    """Return the share of English URLs present in a translation."""

    if not en_urls:
        return 100.0
    shared = en_urls & translation_urls
    return len(shared) * 100.0 / len(en_urls)


def classify(
    headings: int,
    checkboxes: int,
    broken_anchors: int,
    coverage: float,
    en_headings: int = EN_HEADINGS,
    en_checkboxes: int = EN_CHECKBOXES,
) -> str:
    """Classify one translation.

    Stub takes precedence: a translation missing most headings or
    checkboxes is still a stub even if its few links happen to be healthy.
    """

    ratio = checkboxes / en_checkboxes if en_checkboxes else 0.0

    if headings < STUB_HEADINGS or ratio < STUB_RATIO:
        return STATUS_STUB

    if (
        broken_anchors == 0
        and coverage >= HEALTHY_COVERAGE
        and HEALTHY_RATIO_MIN <= ratio <= HEALTHY_RATIO_MAX
    ):
        return STATUS_HEALTHY

    return STATUS_NEEDS_SYNC


def language_code(path: Path) -> str:
    """Return the code embedded in README-xx.md, lowercased."""

    stem = Path(path).stem
    prefix = "readme-"
    if stem.lower().startswith(prefix):
        return stem[len(prefix) :].lower()
    return stem.lower()


def build_entry(
    path: Path,
    code: str,
    en_urls: set[str],
    en_headings: int = EN_HEADINGS,
    en_checkboxes: int = EN_CHECKBOXES,
) -> Entry:
    """Analyse one translation file and build its Entry."""

    path = Path(path)
    text = path.read_text(encoding="utf-8")
    headings = len(extract_headings(text))
    checkboxes = count_checkboxes(text)
    broken = len(analyze_markdown(path, text).broken)
    coverage = coverage_percent(en_urls, set(extract_urls(text)))
    status = classify(
        headings,
        checkboxes,
        broken,
        coverage,
        en_headings=en_headings,
        en_checkboxes=en_checkboxes,
    )
    return Entry(
        code=code,
        language=LANGUAGES.get(code, code),
        path=display_path(path),
        headings=headings,
        checkboxes=checkboxes,
        broken_anchors=broken,
        coverage=coverage,
        status=status,
        en_checkboxes=en_checkboxes,
    )


def sort_entries(entries: Sequence[Entry]) -> list[Entry]:
    """Sort by status, then by URL coverage descending, then code."""

    return sorted(
        entries,
        key=lambda entry: (
            STATUS_ORDER.get(entry.status, len(STATUS_ORDER)),
            -entry.coverage,
            entry.code,
        ),
    )


def build_report(
    files: Sequence[Path],
    en_text: str,
    baseline_file: str = "README.md",
    date: str = SNAPSHOT_DATE,
) -> Report:
    """Build a Report for files against the English baseline in en_text."""

    en_headings = len(extract_headings(en_text))
    en_checkboxes = count_checkboxes(en_text)
    en_urls = set(extract_urls(en_text))

    entries = [
        build_entry(
            path,
            language_code(path),
            en_urls,
            en_headings=en_headings,
            en_checkboxes=en_checkboxes,
        )
        for path in files
    ]

    return Report(
        entries=sort_entries(entries),
        en_headings=en_headings,
        en_checkboxes=en_checkboxes,
        en_urls=len(en_urls),
        baseline_file=baseline_file,
        date=date,
    )


def status_counts(entries: Sequence[Entry]) -> dict[str, int]:
    """Count entries per status in a stable order."""

    counts = {
        STATUS_HEALTHY: 0,
        STATUS_NEEDS_SYNC: 0,
        STATUS_STUB: 0,
    }
    for entry in entries:
        counts[entry.status] = counts.get(entry.status, 0) + 1
    return counts


def entry_as_dict(entry: Entry) -> dict[str, object]:
    """Return a JSON-serialisable representation of one Entry."""

    return {
        "code": entry.code,
        "language": entry.language,
        "path": entry.path,
        "headings": entry.headings,
        "checkboxes": entry.checkboxes,
        "broken_anchors": entry.broken_anchors,
        "en_url_coverage": round(entry.coverage, 1),
        "checkbox_ratio": round(entry.checkbox_ratio, 3),
        "status": entry.status,
    }


def report_as_dict(report: Report) -> dict[str, object]:
    """Return a stable, JSON-serialisable representation of report."""

    entries = sort_entries(report.entries)
    return {
        "snapshot_date": report.date,
        "baseline": {
            "file": report.baseline_file,
            "headings": report.en_headings,
            "checkboxes": report.en_checkboxes,
            "urls": report.en_urls,
        },
        "summary": status_counts(entries),
        "translations": [entry_as_dict(entry) for entry in entries],
    }


def render_markdown(report: Report) -> str:
    """Render the full TRANSLATION-STATUS.md document."""

    entries = sort_entries(report.entries)
    counts = status_counts(entries)
    lines = [
        "# Translation Status",
        "",
        f"Snapshot date: {report.date}",
        "",
        "## Method",
        "",
        (
            "Generated by "
            f"{BT}scripts/translation_status.py{BT} from the 30 translation "
            f"READMEs in {BT}translations/{BT}. The script reuses the "
            "GitHub-style slugging and link analysis from "
            f"{BT}scripts/check_docs.py{BT}."
        ),
        "",
        (
            f"- **Headings** - ATX and bullet headings outside fenced code "
            f"blocks. English baseline: {report.en_headings}."
        ),
        (
            f"- **Checkboxes** - GitHub task-list items outside fenced code "
            f"blocks. English baseline: {report.en_checkboxes}."
        ),
        (
            "- **Broken anchors** - in-page links whose slug does not match "
            "a heading in the same translation."
        ),
        (
            "- **EN URL coverage** - share of the English README's unique "
            "link destinations that also appear in the translation. "
            f"English baseline: {report.en_urls} unique URLs."
        ),
        "",
        "## Status",
        "",
        (
            "| Language | Code | Headings (EN "
            f"{report.en_headings}) | Checkboxes (EN {report.en_checkboxes}) "
            "| Broken anchors | EN URL coverage | Status |"
        ),
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]

    for entry in entries:
        lines.append(
            f"| [{entry.language}](translations/README-{entry.code}.md) | {entry.code} | {entry.headings} "
            f"| {entry.checkboxes} | {entry.broken_anchors} "
            f"| {entry.coverage:.1f}% | {entry.status} |"
        )

    summary = ", ".join(
        f"{counts[status]} {status}"
        for status in (STATUS_HEALTHY, STATUS_NEEDS_SYNC, STATUS_STUB)
    )
    lines.extend(
        [
            "",
            f"**Summary:** {summary}.",
            "",
            "### Status rules",
            "",
            (
                f"- **{STATUS_HEALTHY}** - 0 broken anchors, at least "
                f"{HEALTHY_COVERAGE:.0f}% EN URL coverage, and a checkbox "
                f"ratio between {HEALTHY_RATIO_MIN:.1f} and "
                f"{HEALTHY_RATIO_MAX:.1f}."
            ),
            (
                f"- **{STATUS_STUB}** - fewer than {STUB_HEADINGS} headings "
                f"or less than {STUB_RATIO:.0%} of the English checkbox "
                "count. Stub takes precedence over the other rules."
            ),
            f"- **{STATUS_NEEDS_SYNC}** - everything else.",
            "",
            (
                f"_This is a snapshot generated on {report.date}. "
                "Translations change; regenerate it with "
                f"{BT}python3 scripts/translation_status.py --write{BT}. "
                "Contributions should follow "
                "[CONTRIBUTING.md](CONTRIBUTING.md)._"
            ),
            "",
        ]
    )
    return "\n".join(lines)


def render_text(report: Report) -> str:
    """Render a compact, human-readable table."""

    entries = sort_entries(report.entries)
    counts = status_counts(entries)
    lines = [
        f"Translation status (snapshot {report.date})",
        (
            f"EN baseline: {report.baseline_file} - {report.en_headings} "
            f"headings, {report.en_checkboxes} checkboxes, "
            f"{report.en_urls} unique URLs"
        ),
        "",
        (
            f"{'Language':<22} {'Code':<6} {'Headings':>8} "
            f"{'Checkboxes':>10} {'Broken':>6} {'Coverage':>8}  Status"
        ),
    ]
    for entry in entries:
        lines.append(
            f"{entry.language:<22} {entry.code:<6} {entry.headings:>8} "
            f"{entry.checkboxes:>10} {entry.broken_anchors:>6} "
            f"{entry.coverage:>7.1f}%  {entry.status}"
        )
    summary = ", ".join(
        f"{counts[status]} {status}"
        for status in (STATUS_HEALTHY, STATUS_NEEDS_SYNC, STATUS_STUB)
    )
    lines.extend(["", f"Summary: {summary}"])
    return "\n".join(lines)


def default_files() -> list[Path]:
    """Return every translation README in a stable order."""

    return sorted(REPO_ROOT.glob(DEFAULT_GLOB))


def _flatten_files(groups: list[list[str]] | None) -> list[Path]:
    if not groups:
        return default_files()
    return [Path(raw) for group in groups for raw in group]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Report heading, checkbox, broken-anchor and EN URL coverage "
            "metrics for every translation README."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of the text table.",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Emit the generated Markdown dashboard document.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help=f"Write the dashboard to {STATUS_FILE} at the repo root.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        action="append",
        metavar="PATH",
        default=None,
        help=(
            "Translation files to inspect (default: "
            "translations/README-*.md). May be given more than once."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    files = _flatten_files(args.files)

    baseline_path = REPO_ROOT / "README.md"
    try:
        en_text = baseline_path.read_text(encoding="utf-8")
        report = build_report(files, en_text)
    except OSError as exc:
        print(
            f"translation_status.py: error: cannot read: {exc}",
            file=sys.stderr,
        )
        return 2

    if args.write:
        output = REPO_ROOT / STATUS_FILE
        output.write_text(render_markdown(report), encoding="utf-8")
        if not (args.json or args.markdown):
            print(f"Wrote {display_path(output)}")

    if args.json:
        print(json.dumps(report_as_dict(report), ensure_ascii=False, indent=2))
    elif args.markdown:
        print(render_markdown(report))
    elif not args.write:
        print(render_text(report))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
