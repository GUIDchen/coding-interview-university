# Contributing to Coding Interview University

Thanks for helping. This repo is a single, large, hand-curated study plan plus translations, so the
highest-value contributions are small and surgical: fixing a dead link, correcting a wrong complexity,
keeping a translation in sync, or improving [MINIMAL-PATH.md](MINIMAL-PATH.md).

This document covers **how** to contribute. For **what** to study, see the [README](README.md#table-of-contents).

## Ways to contribute

- **Fix a broken or paywalled link.** The most common and most welcome fix.
- **Correct an error.** Wrong complexity, wrong file name, a video that is actually about something else.
- **Add a resource**, if it is clearly better than what is already there (see the bar below).
- **Improve [MINIMAL-PATH.md](MINIMAL-PATH.md)** or its [Chinese translation](translations/MINIMAL-PATH-cn.md): clearer acceptance criteria, better stop rules, honest timelines.
- **Sync a translation.** The English README moves; translations follow.
- **Improve tooling** in `scripts/` or `.github/workflows/`, as long as it stays dependency-light and runs on a stock GitHub runner.

## Before you start

1. Search [issues](https://github.com/jwasham/coding-interview-university/issues) and open PRs for the same change.
2. Keep one PR to one purpose. A typo fix and a new section are two PRs.
3. Open an issue first if you plan to add a section, remove a section, reorder the curriculum, add a translation, or change a heading (headings are anchors; see below).
4. Do not rewrite the plan in your own voice, and do not "modernise" formatting you are not otherwise touching.

## The bar for a new resource

A resource earns its place if it is:

- **Better, not additional.** Point out what it replaces or why the existing entry is insufficient.
- **Free or clearly marked.** Mark paid material with `(paid)`. Do not add new affiliate or referral links. A few legacy upstream links (the author's story link and the `geni.us` book link) are kept for fidelity; do not copy them into new entries.
- **Stable.** Official docs, university course pages, well-maintained channels. No URL shorteners, no link farms.
- **Format-labelled.** End video entries with `(video)`, as the existing list does.

## Fork and branch workflow

Fork, clone, and create a topic branch:

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/coding-interview-university.git
cd coding-interview-university
git remote add upstream https://github.com/jwasham/coding-interview-university.git
git remote set-url --push upstream DISABLE   # never push your fork back to the original repo
git checkout -b docs/fix-graph-links
```

- **Branch names:** `docs/…`, `fix/…`, `translate/…`, `tooling/…`, kebab-case, short.
- **Commits:** imperative mood, one logical change, e.g. `fix: replace dead Coursera link in graphs`.
- **Stay current:** `git fetch upstream && git rebase upstream/main` before opening or updating a PR.
- **Keep your personal progress out of PRs.** The README checkboxes are for your fork only. Never submit them.
- **Do not rewrite history** on a branch others have reviewed, and do not commit generated files.

Open the PR against `main` and fill in the checklist below. Draft PRs are fine for early feedback.

## Anchor and slug rules

Every `##` heading in a Markdown file on github.com gets an anchor. Anchors are how the table of
contents, the translations, and thousands of external bookmarks reach a section. Changing one
silently breaks all of them, so treat heading text as an API.

GitHub's slug algorithm, in order:

1. Take the heading text, strip inline HTML and Markdown formatting.
2. Lowercase it.
3. Remove punctuation and symbols — but **keep** letters (including CJK), digits, spaces, hyphens, and underscores.
4. Replace each space with `-`.
5. If the result collides with an earlier heading, append `-1`, `-2`, … in document order.

| Heading | Resulting anchor | Note |
|---|---|---|
| `## Data Structures` | `#data-structures` | simple case |
| `## Algorithmic complexity / Big-O / Asymptotic analysis` | `#algorithmic-complexity--big-o--asymptotic-analysis` | `/` is removed, leaving the spaces on both sides as two hyphens |
| `### Trees - Intro` | `#trees---intro` | literal hyphen plus surrounding spaces |
| `- ### Hash table` (heading inside a list item) | `#hash-table` | list nesting does not change the anchor |
| `## System Design, Scalability, Data Handling` | `#system-design-scalability-data-handling` | comma removed |
| `## 树（Trees）` | `#树trees` | CJK kept, full-width parentheses removed |
| `## 系统设计、可扩展性和数据处理` | `#系统设计可扩展性和数据处理` | full-width comma removed |
| `## A*搜索算法` | `#a搜索算法` | `*` removed |

### Known failure modes

These have all happened in this repo. Check for each one before you push.

- **Hand-typed anchors drift from headings.** If you rename or retranslate a heading, every link to
  the old anchor dies. Grep the whole repo for the old anchor, including under `translations/`:
  `grep -rn "](#old-anchor)" .`
- **CJK punctuation is stripped, but people forget.** Full-width `、`, `，`, and `（）` disappear from
  the slug: `## 系统设计、可扩展性和数据处理` anchors to `#系统设计可扩展性和数据处理`, not
  `#系统设计、可扩展性和数据处理`. Exactly this mismatch has appeared in the Chinese table of
  contents. Keep the heading and its TOC entry in the same change.
- **Mixed case in anchors.** Anchors are always lowercase. `#字节序endianness` is right;
  `#字节序Endianness` is not.
- **Translated headings, untranslated anchors.** An English anchor such as `#interview-prep-books`
  stops resolving once the heading is translated, because the slug is recomputed from the new text.
  Recompute the anchor whenever you translate or retranslate a heading.
- **Asterisks and other symbols.** `#a*搜索算法` does not resolve; the `*` disappears from the anchor.
- **Duplicate headings.** `## Testing` twice yields `#testing` and `#testing-1`. The suffix depends on
  document order, so inserting a new heading above shifts it. Avoid duplicate headings.
- **Anchors to non-headings.** GitHub does not create anchors for bold text, table rows, or list
  items. If you need a stable deep link to such a spot, add an explicit `<a id="my-anchor"></a>`.
- **Other renderers differ.** VS Code preview, GitLab, and static-site generators use different
  sluggers (some keep underscores, some handle CJK differently, some do not deduplicate). The CI check
  and github.com are authoritative; test there, not in your editor.
- **Linking across files.** Anchors are per-file: `README.md#graphs` is not `translations/README-cn.md#graphs`.

When in doubt, copy the anchor from the file's own table of contents, or let the checker compute it.

## Translation sync policy

- **English is canonical.** `README.md` and `MINIMAL-PATH.md` define the content; translations follow them.
- **Simplified Chinese (`translations/README-cn.md`, `translations/MINIMAL-PATH-cn.md`) must track English.**
  New topics, removed topics, reordered sections, changed problem counts, and changed acceptance
  criteria all need a matching Chinese change.
- **Same PR is preferred.** Land English and Chinese together when you can. If you cannot translate,
  say so in the PR description and open a follow-up issue; a translation may lag by at most two weeks.
- **Structure, not just words.** Keep heading levels, list nesting, and order identical. Keep links
  pointing at the same targets, with the same external URLs; translate only the link text and prose.
- **Add to English first.** Never add a resource that exists only in a translation; it will be lost
  on the next sync.
- **Say which version is authoritative.** Each translated document starts with a note like the one at
  the top of [MINIMAL-PATH-cn.md](translations/MINIMAL-PATH-cn.md).
- **Glossary.** Use consistent terms: 数据结构、算法、大 O 表示法、数组、链表、栈、队列、哈希表、树、图、
  递归、动态规划、时间复杂度、空间复杂度、面试。Do not translate code identifiers or URLs.
- **Machine translation** is an acceptable first draft, not an acceptable final result. Unedited MT
  dumps will be returned.
- **Run the checker** below before pushing, with `--files translations/<file>.md` for a translation
  the defaults do not cover; it verifies that translated in-page anchors still resolve.
  `--check-parity` additionally flags EN/CN checkbox drift.

## Link-check policy

- `.github/workflows/links_checker.yml` runs monthly with lychee over `README.md` and
  `translations/README-cn.md`, plus on manual dispatch. It never fails the build; it opens or updates
  a single `report` issue, and closes it when a run comes back clean. Failures are not an emergency,
  but the linked resources should be fixed or replaced when reported.
- `.github/workflows/docs_quality.yml` runs on pushes to `main` and on pull requests. It runs the
documentation unit tests, `check_docs.py`, and a progress report; a non-zero exit fails the check.
  Enable branch protection if you want it to block merges. This is the check that protects the table of contents.
- **Internal links must resolve.** Relative paths are relative to the file, not the repo root;
  `README.md#graphs` works from the root, `../README.md#graphs` from `translations/`.
- **Prefer canonical, stable URLs.** Replace link shorteners with the destination.
- **Dead link?** Find the same resource on the official site or an archive, and mark archived copies
  with `(archived)`. If the resource is gone and there is no replacement, remove it and explain why
  in the PR — do not leave a note saying "broken link".
- **Paywalls and registration** are allowed when labelled `(paid)`.
- **No new affiliate, referral, or tracking parameters.** Strip `utm_*`, `?ref=`, `?src=`, affiliate tags,
  and personal referral codes from anything you add. Two legacy upstream links are exceptions: the
  `?src=ciu` on the author's own story link and the `geni.us` book shortlink. Leave them as-is; do not
  copy them.

## Style rules

- **Keep the author's voice.** First person, direct, occasionally blunt. Do not turn the README into a
  product page, and do not add marketing copy, badges, or "why this repo is great" sections.
- **No new affiliate or sponsored links**, including "use my code" offers. Legacy upstream links are
  the only exception, and they are documented above.
- **Headings:** `##` for a top-level topic, `###` for a subsection (often as `- ### Name` inside a
  list, matching the existing style). If you add a heading, add it to the table of contents with the
  computed anchor.
- **Task lists:** `- [ ]` for study items, four-space nesting, one resource per line. Do not break this
  syntax; `scripts/progress.py` and the GitHub progress UI both parse it.
- **Tables and code:** blank lines around tables, fenced code blocks with a language tag.
- **Link text** should describe the resource (`Binary search (video)`), not say `here`.
- **Do not reflow untouched lines.** Re-wrapping a paragraph produces a diff nobody can review and
  makes translations impossible to sync. Change only the lines you mean to change.
- **Dates:** ISO 8601 (`YYYY-MM-DD`). Add or change a date only when the content changed materially;
  do not bump dates to look fresh, and do not add "last updated" lines to every section.
- **Ordering:** the study order is the curriculum. Do not reorder topics without an issue and a
  maintainer's agreement.
- **Chinese typography:** full-width punctuation in Chinese prose, half-width for code and URLs.
  Follow the surrounding file rather than reformatting it.

## Checks to run locally

From the repository root:

```bash
python3 scripts/check_docs.py                 # in-page anchors: README.md + README-cn.md
python3 scripts/check_docs.py --files MINIMAL-PATH.md translations/MINIMAL-PATH-cn.md
python3 scripts/progress.py                   # task-list progress for README.md
python3 scripts/progress.py --json            # same report, machine-readable
python3 -m unittest discover -s scripts -p 'test_*.py'
```

`check_docs.py` validates in-page anchors only, not external URLs or relative file paths, and it
checks `README.md` and `translations/README-cn.md` unless you pass `--files`. It exits non-zero on a
broken anchor, and `--check-parity` warns when EN and CN checkbox counts drift apart. `progress.py`
defaults to `README.md` and accepts `--file` for another document.

Keep these scripts standard-library-only so they run anywhere; if a change needs a dependency,
justify it in the PR. If either script is missing from your checkout, pull the latest `main`. If it
fails on a file you did not touch, say so in the PR instead of fixing unrelated content.

## PR checklist

Copy this into your pull request description:

```markdown
- [ ] One purpose; the description says what changed and why
- [ ] `python3 scripts/check_docs.py` passes (`--files` if you touched a MINIMAL-PATH file)
- [ ] Every new or changed link was opened manually; anchors verified on github.com
- [ ] If English content changed, the Chinese translation is updated (or a follow-up is noted)
- [ ] TOC updated if a heading was added, with a matching anchor
- [ ] No affiliate, referral, shortened, or tracking links; no bare URLs
- [ ] No personal progress checkboxes; no unrelated reformatting
- [ ] `python3 scripts/progress.py` still parses the task lists
- [ ] `.github/workflows/docs_quality.yml` is green
- [ ] No changes to `LICENSE.txt` or other unrelated files
```

## Review and merge

- Maintainers review for correctness and scope, not style preference; expect questions and small
  change requests.
- PRs are squash-merged, so do not worry about a tidy local history.
- A reviewer may push tiny fixes (a typo, a broken anchor) directly to your branch. Say so in the PR
  if you would rather they did not.
- Response time is best-effort. A politely bumped PR after two weeks is fine.
- Disagreement is resolved by one question: does this make the study plan clearer or more correct for
  a learner? If not, it does not go in.

## What will be closed

- Rewrites of the plan, or content in a different voice.
- Promotional links, affiliate links, course funnels, and "my newsletter" additions.
- Machine-translated files with no review, or translations that fork the content instead of tracking it.
- Anchor-breaking heading renames without a migration of every link.
- Formatting-only churn across files.

## Adding a translation

1. Copy `README.md` to `translations/README-xx.md` (or `MINIMAL-PATH.md` to `translations/MINIMAL-PATH-xx.md`).
2. Add the canonical-version note at the top.
3. Translate in place, keeping heading order, links, and task-list syntax.
4. Add the file to the translations list at the top of `README.md`.
5. Run the checks, then open one PR per language.

Thanks for keeping this useful for the next person.
