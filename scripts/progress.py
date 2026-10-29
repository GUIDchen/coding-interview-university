#!/usr/bin/env python3
"""Report progress on GitHub task-list items in a Markdown file.

Usage::

    python3 scripts/progress.py [--file PATH] [--json]

Task-list items ("- [ ]" / "- [x]", including nested and indented items)
are counted per top-level "##" section.  Fenced code blocks are ignored.
The default file is README.md at the repository root, where "repository
root" is resolved relative to this script rather than to the current
working directory.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = REPO_ROOT / "README.md"

BAR_WIDTH = 20

# A top-level section heading.  "##" must be followed by whitespace so that
# "###" headings are *not* treated as sections.
_SECTION_RE = re.compile(r"^##[ \t]+(.*?)[ \t]*$")
# GitHub task-list item: a bullet followed by [ ], [x], or [X].
_TASK_RE = re.compile(r"^\s*[-*+]\s+\[([ xX])\](?:\s+|$)")
# Opening or closing code fence (backticks or tildes, any indentation).
_FENCE_RE = re.compile(r"^(\s*)(\x60{3,}|~{3,})(.*)$")


@dataclass
class Section:
    """A top-level section and its checkbox counts."""

    title: str
    line: int
    done: int = 0
    total: int = 0

    @property
    def percent(self) -> float:
        return percent(self.done, self.total)


@dataclass
class Report:
    """Aggregated progress for a Markdown document."""

    sections: list[Section]
    preamble: Section | None = None

    @property
    def rows(self) -> list[Section]:
        """Sections that actually contain task-list items, in source order."""

        rows: list[Section] = []
        if self.preamble is not None and self.preamble.total:
            rows.append(self.preamble)
        rows.extend(section for section in self.sections if section.total)
        return rows

    @property
    def done(self) -> int:
        done = self.preamble.done if self.preamble is not None else 0
        return done + sum(section.done for section in self.sections)

    @property
    def total(self) -> int:
        total = self.preamble.total if self.preamble is not None else 0
        return total + sum(section.total for section in self.sections)

    @property
    def percent(self) -> float:
        return percent(self.done, self.total)


def percent(done: int, total: int) -> float:
    """Return done as a percentage of total (0.0 when empty)."""

    if total <= 0:
        return 0.0
    return done * 100.0 / total


def make_bar(value: float, width: int = BAR_WIDTH) -> str:
    """Return a simple fixed-width ASCII progress bar."""

    if width <= 0:
        return ""
    filled = int(value / 100.0 * width + 0.5)
    filled = max(0, min(width, filled))
    return "#" * filled + "." * (width - filled)


def iter_visible_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield (line_number, line) pairs outside fenced code blocks."""

    fence_char: str | None = None
    fence_len = 0

    for lineno, line in enumerate(text.splitlines(), 1):
        match = _FENCE_RE.match(line)
        if fence_char is None:
            if match:
                marker = match.group(2)
                fence_char = marker[0]
                fence_len = len(marker)
                continue
            yield lineno, line
            continue

        # Inside a fence: only a matching closing fence ends the block.
        if match:
            marker = match.group(2)
            rest = match.group(3)
            if (
                marker[0] == fence_char
                and len(marker) >= fence_len
                and not rest.strip()
            ):
                fence_char = None
                fence_len = 0


def parse_sections(text: str) -> tuple[list[Section], Section | None]:
    """Parse top-level sections and count task-list items in each.

    Returns (sections, preamble).  preamble is None unless task-list items
    appear before the first top-level "##" heading.
    """

    sections: list[Section] = []
    preamble: Section | None = None
    current: Section | None = None

    for lineno, line in iter_visible_lines(text):
        heading = _SECTION_RE.match(line)
        if heading:
            title = re.sub(r"[ \t]+#+[ \t]*$", "", heading.group(1)).strip()
            current = Section(title=title, line=lineno)
            sections.append(current)
            continue

        task = _TASK_RE.match(line)
        if task is None:
            continue

        if current is None:
            if preamble is None:
                preamble = Section(title="(preamble)", line=0)
            target = preamble
        else:
            target = current

        target.total += 1
        if task.group(1).lower() == "x":
            target.done += 1

    return sections, preamble


def analyze_text(text: str) -> Report:
    """Build a Report from Markdown source."""

    sections, preamble = parse_sections(text)
    return Report(sections=sections, preamble=preamble)


def analyze_file(path: Path) -> Report:
    """Read *path* and build a Report."""

    return analyze_text(Path(path).read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    """Return a repository-relative path when possible."""

    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT))
    except (OSError, ValueError):
        return str(path)


def report_as_dict(report: Report, label: str) -> dict[str, object]:
    """Return a stable, JSON-serialisable representation of report."""

    return {
        "file": label,
        "sections": [
            {
                "title": section.title,
                "line": section.line,
                "done": section.done,
                "total": section.total,
                "percent": round(section.percent, 1),
            }
            for section in report.rows
        ],
        "total": {
            "done": report.done,
            "total": report.total,
            "percent": round(report.percent, 1),
        },
    }


def render_text(report: Report, label: str) -> str:
    """Render a human-readable progress report."""

    noun = "item" if report.total == 1 else "items"
    lines = [f"{label}: {report.total} task {noun}"]
    for section in report.rows:
        lines.append(
            "  {title}: {done}/{total} ({pct:.1f}%) [{bar}]".format(
                title=section.title,
                done=section.done,
                total=section.total,
                pct=section.percent,
                bar=make_bar(section.percent),
            )
        )
    lines.append(
        "Total: {done}/{total} ({pct:.1f}%) [{bar}]".format(
            done=report.done,
            total=report.total,
            pct=report.percent,
            bar=make_bar(report.percent),
        )
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report GitHub task-list progress in a Markdown file.",
    )
    parser.add_argument(
        "--file",
        metavar="PATH",
        default=None,
        help="Markdown file to inspect (default: README.md at the repo root).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of the text report.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = Path(args.file) if args.file else DEFAULT_FILE

    try:
        report = analyze_file(path)
    except OSError as exc:
        print(f"progress.py: error: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    label = display_path(path)
    if args.json:
        print(json.dumps(report_as_dict(report, label), ensure_ascii=False, indent=2))
    else:
        print(render_text(report, label))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
