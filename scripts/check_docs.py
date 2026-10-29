#!/usr/bin/env python3
"""Validate internal Markdown anchors and compare EN/CN checkbox counts.

Usage::

    python3 scripts/check_docs.py [--files PATH [PATH ...]] [--check-parity]

By default the script checks README.md and translations/README-cn.md.
Only in-page links (targets beginning with "#") are validated.  Anchors are
computed with GitHub-style heading slugs: text is lowercased, punctuation is
removed (including CJK punctuation), and spaces become hyphens.  Headings
written as bullet headings such as "- ### Topic" are also recognised.

The script exits 1 when broken anchors are found and 0 otherwise.
--check-parity prints non-fatal warnings and never changes the exit status
on its own.
"""

from __future__ import annotations

import argparse
import html
import re
import string
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILES = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "translations" / "README-cn.md",
)

# Punctuation that is stripped by GitHub-style slugging.  Most of it is
# covered by Unicode category "P", but keeping an explicit set documents the
# CJK cases that matter for the translations.
CJK_PUNCTUATION = frozenset("，。！？：；、（）【】《》「」『』“”‘’〈〉…—–·～")
# ASCII punctuation except hyphen and underscore (both are kept by GitHub).
ASCII_PUNCTUATION = frozenset(string.punctuation) - frozenset("-_")

BACKTICK = chr(96)

_SECTION_RE = re.compile(r"^##[ \t]+(.*?)[ \t]*$")
_TASK_RE = re.compile(r"^\s*[-*+]\s+\[([ xX])\](?:\s+|$)")
_FENCE_RE = re.compile(r"^(\s*)(\x60{3,}|~{3,})(.*)$")
_ATX_RE = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$")
_BULLET_HEADING_RE = re.compile(
    r"^\s*[-*+]\s+(#{1,6})(?:[ \t]+(.*?))?[ \t]*$"
)
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_HTML_TAG_RE = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    text: str
    slug: str

    @property
    def label(self) -> str:
        return ("#" * self.level + " " + self.text).strip()


@dataclass(frozen=True)
class Link:
    line: int
    text: str
    target: str


@dataclass(frozen=True)
class BrokenLink:
    line: int
    text: str
    target: str
    nearest_heading: Heading | None


@dataclass
class FileAnalysis:
    path: Path
    headings: list[Heading]
    links: list[Link]
    broken: list[BrokenLink]


@dataclass
class SectionCount:
    title: str
    done: int = 0
    total: int = 0


@dataclass
class ParityResult:
    pairs: list[tuple[SectionCount, SectionCount]]
    unmatched_en: list[SectionCount]
    unmatched_cn: list[SectionCount]
    warnings: list[str]
    en_total: int
    cn_total: int


def plain_heading(text: str) -> str:
    """Reduce inline Markdown in a heading to its rendered text."""

    text = _IMAGE_RE.sub(r"\1", text)
    text = _LINK_RE.sub(r"\1", text)
    text = _HTML_TAG_RE.sub("", text)
    return html.unescape(text).strip()


def slugify(text: str) -> str:
    """Return a GitHub-style anchor slug for a heading's text."""

    result: list[str] = []
    for char in plain_heading(text).lower():
        if char in "-_":
            # GitHub keeps hyphens and underscores verbatim.
            result.append(char)
        elif char.isspace():
            # Do not collapse runs: "Trees - Intro" becomes "trees---intro".
            result.append("-")
        elif char in ASCII_PUNCTUATION or char in CJK_PUNCTUATION:
            continue
        elif unicodedata.category(char).startswith("P"):
            continue
        else:
            result.append(char)
    return "".join(result)


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


def _clean_heading_text(raw: str) -> str:
    text = re.sub(r"[ \t]+#+[ \t]*$", "", raw or "")
    return plain_heading(text)


def _unique_slug(base: str, seen: dict[str, int]) -> str:
    """Disambiguate duplicate headings the way github-slugger does."""

    if base not in seen:
        seen[base] = 0
        return base

    number = seen[base]
    while True:
        number += 1
        candidate = f"{base}-{number}"
        if candidate not in seen:
            seen[base] = number
            seen[candidate] = 0
            return candidate


def extract_headings(text: str) -> list[Heading]:
    """Return all ATX and bullet headings outside fenced code blocks."""

    headings: list[Heading] = []
    seen: dict[str, int] = {}

    for lineno, line in iter_visible_lines(text):
        match = _BULLET_HEADING_RE.match(line)
        if match is None:
            match = _ATX_RE.match(line)
        if match is None:
            continue

        level = len(match.group(1))
        heading_text = _clean_heading_text(match.group(2) or "")
        base = slugify(heading_text)
        slug = _unique_slug(base, seen)
        headings.append(Heading(lineno, level, heading_text, slug))

    return headings


def _mask_code_spans(line: str) -> str:
    """Blank out inline code spans so links inside them are ignored."""

    if BACKTICK not in line:
        return line

    chars = list(line)
    index = 0
    length = len(line)

    while index < length:
        if chars[index] != BACKTICK:
            index += 1
            continue

        start = index
        while index < length and chars[index] == BACKTICK:
            index += 1
        ticks = line[start:index]
        close = line.find(ticks, index)
        if close == -1:
            continue
        for position in range(start, close + len(ticks)):
            chars[position] = " "
        index = close + len(ticks)

    return "".join(chars)


def _find_matching(
    text: str, start: int, opening: str, closing: str
) -> int:
    """Return the index of the bracket matching text[start], or -1."""

    depth = 0
    index = start
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return -1


def _parse_destination(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    if raw.startswith("<"):
        end = raw.find(">")
        return raw[1:end] if end != -1 else raw[1:]
    parts = raw.split()
    return parts[0] if parts else ""


def _scan_line_links(line: str, lineno: int) -> list[Link]:
    links: list[Link] = []
    index = 0
    length = len(line)

    while index < length:
        char = line[index]

        if char == "\\":
            index += 2
            continue

        # Skip images entirely: an image is not a navigable anchor link.
        if char == "!" and index + 1 < length and line[index + 1] == "[":
            close = _find_matching(line, index + 1, "[", "]")
            if (
                close != -1
                and close + 1 < length
                and line[close + 1] == "("
            ):
                end = _find_matching(line, close + 1, "(", ")")
                if end != -1:
                    index = end + 1
                    continue
            index += 1
            continue

        if char != "[":
            index += 1
            continue

        close = _find_matching(line, index, "[", "]")
        if close == -1:
            index += 1
            continue

        if close + 1 >= length or line[close + 1] != "(":
            index += 1
            continue

        end = _find_matching(line, close + 1, "(", ")")
        if end == -1:
            index += 1
            continue

        text = line[index + 1 : close]
        target = _parse_destination(line[close + 2 : end])
        if target.startswith("#"):
            links.append(Link(lineno, text, target))
        index = end + 1

    return links


def extract_links(text: str) -> list[Link]:
    """Return internal (fragment-only) Markdown links in source order."""

    links: list[Link] = []
    for lineno, line in iter_visible_lines(text):
        links.extend(_scan_line_links(_mask_code_spans(line), lineno))
    return links


def _nearest_heading(
    headings: list[Heading], line: int
) -> Heading | None:
    nearest: Heading | None = None
    for heading in headings:
        if heading.line <= line:
            nearest = heading
        else:
            break
    return nearest


def analyze_markdown(path: Path, text: str) -> FileAnalysis:
    """Analyse one Markdown document held in *text*."""

    headings = extract_headings(text)
    links = extract_links(text)
    anchors = {heading.slug for heading in headings}
    broken: list[BrokenLink] = []

    for link in links:
        target = unquote(link.target[1:])
        if target == "":
            # A bare "#" simply jumps to the top of the page.
            continue
        if target not in anchors:
            broken.append(
                BrokenLink(
                    line=link.line,
                    text=link.text,
                    target=link.target,
                    nearest_heading=_nearest_heading(headings, link.line),
                )
            )

    return FileAnalysis(
        path=Path(path),
        headings=headings,
        links=links,
        broken=broken,
    )


def analyze_file(path: Path) -> FileAnalysis:
    """Read *path* and analyse its internal links."""

    path = Path(path)
    return analyze_markdown(path, path.read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    """Return a repository-relative path when possible."""

    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT))
    except (OSError, ValueError):
        return str(path)


def format_broken_line(label: str, broken: BrokenLink) -> str:
    heading = broken.nearest_heading
    if heading is None:
        heading_text = "none"
    else:
        heading_text = f'"{heading.label}" at line {heading.line}'
    return (
        f"{label}:{broken.line}: BROKEN link [{broken.text}] -> "
        f"{broken.target} (nearest heading: {heading_text})"
    )


def count_sections(text: str) -> list[SectionCount]:
    """Count checkboxes in each top-level section (fences ignored)."""

    sections: list[SectionCount] = []
    current: SectionCount | None = None

    for _lineno, line in iter_visible_lines(text):
        heading = _SECTION_RE.match(line)
        if heading:
            title = _clean_heading_text(heading.group(1))
            current = SectionCount(title=title)
            sections.append(current)
            continue

        task = _TASK_RE.match(line)
        if task is None or current is None:
            continue

        current.total += 1
        if task.group(1).lower() == "x":
            current.done += 1

    return sections


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", plain_heading(title)).strip().lower()


def compare_sections(
    en_sections: list[SectionCount],
    cn_sections: list[SectionCount],
) -> ParityResult:
    """Compare EN and CN section checkbox counts.

    Section headings are translated, so sections are aligned by position.
    Identical trailing headings (for example "LICENSE") are aligned from the
    end first, which avoids reporting a false mismatch when one file has an
    extra section near the bottom.
    """

    en_remaining = list(en_sections)
    cn_remaining = list(cn_sections)
    trailing: list[tuple[SectionCount, SectionCount]] = []

    while (
        en_remaining
        and cn_remaining
        and _normalize_title(en_remaining[-1].title)
        == _normalize_title(cn_remaining[-1].title)
    ):
        trailing.append((en_remaining.pop(), cn_remaining.pop()))

    pair_count = min(len(en_remaining), len(cn_remaining))
    pairs = [
        (en_remaining[index], cn_remaining[index])
        for index in range(pair_count)
    ]
    pairs.extend(reversed(trailing))

    unmatched_en = en_remaining[pair_count:]
    unmatched_cn = cn_remaining[pair_count:]

    warnings: list[str] = []
    for index, (en_section, cn_section) in enumerate(pairs, 1):
        if en_section.total != cn_section.total:
            delta = cn_section.total - en_section.total
            warnings.append(
                f'section {index} "{en_section.title}" vs '
                f'"{cn_section.title}": EN {en_section.total}, '
                f"CN {cn_section.total} ({delta:+d})"
            )

    for section in unmatched_en:
        warnings.append(
            f'section "{section.title}" exists only in the EN file'
        )
    for section in unmatched_cn:
        warnings.append(
            f'section "{section.title}" exists only in the CN file'
        )

    en_total = sum(section.total for section in en_sections)
    cn_total = sum(section.total for section in cn_sections)
    if en_total != cn_total:
        warnings.append(
            f"total checkbox count: EN {en_total}, CN {cn_total} "
            f"({cn_total - en_total:+d})"
        )

    return ParityResult(
        pairs=pairs,
        unmatched_en=unmatched_en,
        unmatched_cn=unmatched_cn,
        warnings=warnings,
        en_total=en_total,
        cn_total=cn_total,
    )


def _parity_paths(files: list[Path]) -> tuple[Path, Path]:
    if len(files) >= 2:
        return files[0], files[1]
    return DEFAULT_FILES[0], DEFAULT_FILES[1]


def _run_parity(en_path: Path, cn_path: Path) -> int:
    """Print parity warnings.  Always returns 0 (warnings are non-fatal)."""

    try:
        en_text = en_path.read_text(encoding="utf-8")
        cn_text = cn_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Parity check skipped: {exc}", file=sys.stderr)
        return 0

    result = compare_sections(count_sections(en_text), count_sections(cn_text))
    print(
        "Parity check ({} vs {}):".format(
            display_path(en_path), display_path(cn_path)
        )
    )

    if result.warnings:
        for warning in result.warnings:
            print(f"  WARNING: {warning}")
    else:
        print(
            f"  OK: {len(result.pairs)} matched sections have equal "
            "checkbox counts."
        )

    print(
        "  Totals: EN {} checkbox items, CN {} checkbox items.".format(
            result.en_total, result.cn_total
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate internal Markdown anchors and optionally compare "
            "EN/CN checkbox counts."
        ),
    )
    parser.add_argument(
        "--files",
        nargs="+",
        action="append",
        metavar="PATH",
        default=None,
        help=(
            "Markdown files to check (default: README.md and "
            "translations/README-cn.md). May be given more than once."
        ),
    )
    parser.add_argument(
        "--check-parity",
        action="store_true",
        help=(
            "Compare per-section checkbox counts between the first two "
            "files (default: EN README vs CN README)."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    files = [
        Path(path)
        for group in (args.files or [])
        for path in group
    ]
    if not files:
        files = [Path(path) for path in DEFAULT_FILES]

    total_links = 0
    total_broken = 0

    for path in files:
        try:
            analysis = analyze_file(path)
        except OSError as exc:
            print(
                f"check_docs.py: error: cannot read {path}: {exc}",
                file=sys.stderr,
            )
            return 2

        label = display_path(path)
        total_links += len(analysis.links)
        total_broken += len(analysis.broken)
        print(
            f"{label}: checked {len(analysis.links)} internal links, "
            f"{len(analysis.broken)} broken"
        )

        if analysis.broken:
            print()
            for broken in analysis.broken:
                print(format_broken_line(label, broken))
            print()

    print(
        f"Total: checked {total_links} internal links, "
        f"{total_broken} broken"
    )

    if args.check_parity:
        print()
        en_path, cn_path = _parity_paths(files)
        _run_parity(en_path, cn_path)

    return 1 if total_broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
