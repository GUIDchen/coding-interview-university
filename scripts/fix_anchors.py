#!/usr/bin/env python3
"""Safely repair broken in-page anchors in translated READMEs.

Usage::

    python3 scripts/fix_anchors.py [--write] [--files PATH [PATH ...]]

The default is a dry run: nothing is written unless --write is given.
Without --files the script targets every translations/README-*.md file.
README.md and translations/README-cn.md are never targeted by default
because the English file is the source of truth and the Chinese
translation currently has no broken anchors.

A broken link is repaired only when the replacement slug is an existing
heading in the same file, using one of three safe rules in order:

1. The lowercased, percent-decoded target is already a heading slug.
2. slugify(link text) is a heading slug.
3. slugify(percent-decoded target) is a heading slug.

Every rewrite is limited to the link destination, so external links, link
text, titles and the rest of the document are left untouched.  Existing
line endings (LF or CRLF) are preserved when a file is written.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence
from urllib.parse import unquote

from check_docs import (
    REPO_ROOT,
    analyze_markdown,
    display_path,
    extract_headings,
    iter_visible_lines,
    slugify,
    _find_matching,
    _mask_code_spans,
    _parse_destination,
)

DEFAULT_GLOB = "translations/README-*.md"

RULE_LABELS = {
    1: "lowercase target",
    2: "link text",
    3: "slugified target",
}


@dataclass(frozen=True)
class Repair:
    """One link destination rewrite on a single source line."""

    line: int
    old_target: str
    new_target: str
    rule: int
    start: int
    end: int

    @property
    def rule_label(self) -> str:
        return f"rule {self.rule}: {RULE_LABELS[self.rule]}"


@dataclass
class FileResult:
    path: Path
    before: int
    after: int
    repairs: list[Repair]
    written: bool

    @property
    def fixed(self) -> int:
        return len(self.repairs)


@dataclass(frozen=True)
class LinkSpan:
    """An inline link together with the source span to rewrite."""

    text: str
    raw: str
    target: str
    start: int
    end: int


def _destination_span(raw: str, target: str) -> tuple[int, int]:
    """Return the (start, end) offsets of the destination inside raw.

    raw is the text between the link's parentheses.  A trailing title is
    preserved; malformed destinations containing whitespace (common in a
    few translations) are replaced wholesale so the repaired link is valid.
    """

    if not target:
        return 0, len(raw)

    stem = raw.strip()
    if stem == target:
        # Only surrounding whitespace differs.
        return 0, len(raw)

    leading = len(raw) - len(raw.lstrip())
    if raw[leading:].startswith("<"):
        close = raw.find(">", leading)
        token_end = len(raw) if close == -1 else close + 1
    else:
        match = re.search(r"\s", raw[leading:])
        token_end = len(raw) if match is None else leading + match.start()

    trailing = raw[token_end:]
    if trailing.strip() and not trailing.lstrip().startswith(('"', "'", "(")):
        # Not a title: the "target" really contains spaces, so replace all
        # of the raw destination with a clean anchor.
        return 0, len(raw)
    return leading, token_end


def iter_link_spans(line: str) -> Iterator[LinkSpan]:
    """Yield inline links on line with absolute rewrite offsets."""

    masked = _mask_code_spans(line)
    index = 0
    length = len(masked)

    while index < length:
        char = masked[index]

        if char == "\\":
            index += 2
            continue

        # Images are not navigable anchor links.
        if char == "!" and index + 1 < length and masked[index + 1] == "[":
            close = _find_matching(masked, index + 1, "[", "]")
            if (
                close != -1
                and close + 1 < length
                and masked[close + 1] == "("
            ):
                end = _find_matching(masked, close + 1, "(", ")")
                if end != -1:
                    index = end + 1
                    continue
            index += 1
            continue

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

        link_text = line[index + 1 : close]
        raw = line[close + 2 : end]
        target = _parse_destination(raw)

        span_start, span_end = _destination_span(raw, target)
        yield LinkSpan(
            text=link_text,
            raw=raw,
            target=target,
            start=close + 2 + span_start,
            end=close + 2 + span_end,
        )
        index = end + 1


def choose_replacement(
    link_text: str, target: str, anchors: set[str]
) -> tuple[str, int] | None:
    """Return (new_target, rule) for a broken link, or None.

    target still carries its leading '#'.  anchors contains the slugs of
    every heading in the same file.
    """

    base = unquote(target[1:])
    if base == "":
        # A bare "#" links to the top of the page.
        return None

    lowered = base.lower()
    if lowered in anchors:
        return f"#{lowered}", 1

    text_slug = slugify(link_text)
    if text_slug and text_slug in anchors:
        return f"#{text_slug}", 2

    slug = slugify(base)
    if slug and slug in anchors:
        return f"#{slug}", 3

    return None


def plan_repairs(text: str) -> list[Repair]:
    """Return safe repairs for every broken internal link in text."""

    headings = extract_headings(text)
    anchors = {heading.slug for heading in headings}
    repairs: list[Repair] = []

    for lineno, line in iter_visible_lines(text):
        for link in iter_link_spans(line):
            if not link.target.startswith("#"):
                continue

            base = unquote(link.target[1:])
            if base == "" or base in anchors:
                continue

            choice = choose_replacement(link.text, link.target, anchors)
            if choice is None:
                continue

            new_target, rule = choice
            repairs.append(
                Repair(
                    line=lineno,
                    old_target=link.target,
                    new_target=new_target,
                    rule=rule,
                    start=link.start,
                    end=link.end,
                )
            )

    return repairs


def apply_repairs(text: str, repairs: Sequence[Repair]) -> str:
    """Apply repairs to text, rewriting only the destination spans."""

    by_line: dict[int, list[Repair]] = {}
    for repair in repairs:
        by_line.setdefault(repair.line, []).append(repair)

    source_lines = text.splitlines(keepends=True)
    visible = dict(iter_visible_lines(text))

    for lineno, line_repairs in by_line.items():
        original = visible[lineno]
        new_line = original
        for repair in sorted(
            line_repairs, key=lambda item: item.start, reverse=True
        ):
            new_line = (
                new_line[: repair.start]
                + repair.new_target
                + new_line[repair.end :]
            )

        raw_line = source_lines[lineno - 1]
        ending = raw_line[len(original) :]
        source_lines[lineno - 1] = new_line + ending

    return "".join(source_lines)


def repair_text(text: str) -> tuple[str, list[Repair]]:
    """Return repaired text and the repairs that were applied."""

    repairs = plan_repairs(text)
    return apply_repairs(text, repairs), repairs


def repair_file(path: Path, write: bool = False) -> FileResult:
    """Repair one file, writing it only when write is true.

    The repaired text is re-analysed before anything is written.  If the
    number of broken links does not drop by exactly one per repair, the
    rewrite is rejected for that file so no new broken links can be
    introduced.
    """

    path = Path(path)
    # newline="" keeps the original line endings (LF or CRLF) in the text,
    # so rewriting a CRLF file does not turn it into a whole-file diff.
    with path.open("r", encoding="utf-8", newline="") as handle:
        original = handle.read()
    before = len(analyze_markdown(path, original).broken)
    new_text, repairs = repair_text(original)
    after = len(analyze_markdown(path, new_text).broken)

    if after != before - len(repairs):
        raise RuntimeError(
            f"{display_path(path)}: refusing unsafe rewrite "
            f"(broken {before} -> {after} with {len(repairs)} repairs)"
        )

    written = bool(write and repairs)
    if written:
        with path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(new_text)

    return FileResult(
        path=path,
        before=before,
        after=after,
        repairs=repairs,
        written=written,
    )


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
            "Repair broken in-page anchors in translation READMEs using "
            "only replacements that exist in the same file."
        ),
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply the repairs (default is a dry run).",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        action="append",
        metavar="PATH",
        default=None,
        help=(
            "Markdown files to repair (default: "
            "translations/README-*.md). May be given more than once."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    files = _flatten_files(args.files)

    results: list[FileResult] = []
    for path in files:
        try:
            results.append(repair_file(path, write=args.write))
        except OSError as exc:
            print(
                f"fix_anchors.py: error: cannot read {path}: {exc}",
                file=sys.stderr,
            )
            return 2
        except RuntimeError as exc:
            print(f"fix_anchors.py: error: {exc}", file=sys.stderr)
            return 3

    total_before = sum(result.before for result in results)
    total_after = sum(result.after for result in results)
    total_fixed = sum(result.fixed for result in results)
    rule_counts = {rule: 0 for rule in RULE_LABELS}
    for result in results:
        for repair in result.repairs:
            rule_counts[repair.rule] += 1

    for result in results:
        label = display_path(result.path)
        if result.repairs:
            print(f"{label}: {result.before} -> {result.after} broken "
                  f"({result.fixed} fixed)")
            for repair in result.repairs:
                print(
                    f"{label}:{repair.line}: {repair.old_target} -> "
                    f"{repair.new_target} ({repair.rule_label})"
                )
        else:
            print(f"{label}: {result.before} broken (0 fixed)")

    print()
    print(f"Files: {len(results)}")
    print(f"Broken anchors before: {total_before}")
    print(f"Repairs: {total_fixed}")
    for rule, count in rule_counts.items():
        print(f"  {rule}. {RULE_LABELS[rule]}: {count}")
    print(f"Broken anchors after: {total_after}")

    if args.write:
        written = sum(1 for result in results if result.written)
        print(f"Wrote {written} file(s).")
    else:
        print("Dry run: no files written. Re-run with --write to apply.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
