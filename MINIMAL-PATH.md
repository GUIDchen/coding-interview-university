# The Minimal Path: 8 weeks at 10–15 hours a week

> **This is not Coding Interview University.** It is a *minimum viable* slice of it: the smallest set of
> topics that still lets you walk into a general software-engineering loop and hold your own.
> It is not a guarantee of a job, a pass, or a level. If you have more time, use the
> [full study plan](README.md#table-of-contents) — this page exists for people who do not.
>
> 简体中文版：[最小可行路径](translations/MINIMAL-PATH-cn.md) · English is the canonical version.

## What this is

A fixed 8-week schedule, 10–15 hours a week, built from resources already listed in this repository.
You will implement core data structures from scratch, solve about 85 problems, and practice explaining
time and space complexity out loud. Everything else in the README is deliberately deferred.

**Minimum viable means green, not gold.** You are aiming for "I can build it and explain it",
not "I have watched every video". Watching is not progress; typing from scratch is.

## Who this is for

- You can already code (variables, loops, functions, one language you are fluent in).
- You have 10–15 hours a week for 8 weeks, roughly 6 days a week.
- You are targeting general SWE interviews: arrays, strings, hash maps, trees, graphs, recursion, DP.
- You want a defensible "done" so you stop browsing and start applying.

## Who this is not for

- **Total beginners.** Do the [full plan](README.md#what-is-it) or a structured course first.
- **Frontend, full-stack, mobile, data-engineering, or ML loops.** The scope note at the bottom applies.
- **Senior/staff candidates.** You need the [system design material](README.md#system-design-scalability-data-handling) now, not after week 8.
- **People with 30+ hours a week.** The extra time is better spent on the full plan than on finishing this faster.
- **Anyone who wants a certificate.** There is none. The only output is your own code and your own notes.

## The priority table

P0 is the minimum viable set. P1 is "add if a week goes well". P2 is "read the heading and move on".

| Priority | Topic | Where it lives in the README | Budget | Why it is ranked here |
|---|---|---|---|---|
| **P0** | Big-O and complexity | [Algorithmic complexity](README.md#algorithmic-complexity--big-o--asymptotic-analysis) | 3 h | Every answer you give is graded on it |
| **P0** | Arrays, linked lists, stack, queue | [Data Structures](README.md#data-structures) | 12 h | The substrate for every other question |
| **P0** | Hash tables | [Hash table](README.md#hash-table) | 6 h | The most common "make it faster" answer |
| **P0** | Binary search | [Binary search](README.md#binary-search) | 3 h | Often hidden inside a larger problem rather than named |
| **P0** | Trees: BST, traversals, heap | [Trees](README.md#trees) | 12 h | Recursion practice plus a real data structure |
| **P0** | Sorting | [Sorting](README.md#sorting) | 8 h | Merge/quick sort are asked as code, not trivia |
| **P0** | Graphs: BFS, DFS, topological sort, union-find | [Graphs](README.md#graphs) | 12 h | Highest signal per hour after arrays |
| **P0** | Recursion, backtracking, core DP | [Recursion](README.md#recursion), [Dynamic Programming](README.md#dynamic-programming) | 14 h | The make-or-break block for most candidates |
| **P0** | Timed problem practice | [Coding Problems](README.md#coding-problems) | 15 h | The actual interview skill |
| **P1** | Tries, bit manipulation, string searching | [Tries](README.md#tries), [Bitwise](README.md#bitwise-operations), [Strings](README.md#string-searching--manipulations) | 8 h | Cheap wins if week 7 has room |
| **P1** | Testing habits, design patterns (light) | [Testing](README.md#testing), [Design patterns](README.md#design-patterns) | 4 h | Useful in interviews, rarely the deciding factor |
| **P1** | System design reading only | [System Design](README.md#system-design-scalability-data-handling) | 4 h | Skim vocabulary; do not study it yet |
| **P2** | Combinatorics, probability, NP-completeness | [Combinatorics](README.md#combinatorics-n-choose-k--probability), [NP](README.md#np-np-complete-and-approximation-algorithms) | 0 h | Rare in general SWE loops; expensive to learn well |
| **P2** | Caches, processes, threads, networking | [Caches](README.md#caches), [Processes](README.md#processes-and-threads), [Networking](README.md#networking) | 0 h | Covered by system design later, at the right depth |
| **P2** | Unicode, endianness, floating point | [Unicode](README.md#unicode), [Endianness](README.md#endianness), [Floats](README.md#floating-point-numbers) | 0 h | Trivia you can look up; not worth 8 weeks |
| **P2** | Everything under [Additional Learning](README.md#additional-learning) | Compilers, FFT, van Emde Boas, papers | 0 h | Genuinely interesting, genuinely not this plan |

Total P0 is about 85 hours, P1 about 16, plus slack. If you only finish P0, the plan worked.

## The 8-week schedule

Each week has three parts: **learn** (one resource per topic, see the stop rules), **build** (from
scratch, no library data structures), **practice** (timed problems). Week acceptance is the gate to
the next week — but see the stop rules for when to move on anyway. Before week 1, read
[The Daily Plan](README.md#the-daily-plan) and [Coding Question Practice](README.md#coding-question-practice) once.

| Week | Focus | Problems |
|---|---|---|
| 1 | Big-O, arrays, linked lists | 8 |
| 2 | Stack, queue, hash table, binary search | 10 |
| 3 | Trees, BST, traversals, heap | 10 |
| 4 | Sorting | 8 |
| 5 | Graphs | 10 |
| 6 | Recursion, backtracking, DP | 14 |
| 7 | Mixed practice, P1 topics, weak-topic repair | 15 |
| 8 | Mocks, final review, resume and stories | 10 re-solves |

### Week 1 — Complexity and linear structures

- **Learn:** [Big-O](README.md#algorithmic-complexity--big-o--asymptotic-analysis), [Arrays](README.md#arrays), [Linked Lists](README.md#linked-lists). One video per topic is enough.
- **Build:** a dynamic array with grow/shrink; a singly linked list with push, pop, insert, delete, and reverse. No built-in list types.
- **Practice:** 8 easy problems — 4 array/string (two pointers, prefix sums), 4 linked list (reverse, cycle, merge).
- **Accept when:** you implement both structures in about 60 minutes with the README closed; you can state the complexity of every operation you wrote; you can explain why `append` is amortized O(1), and why finding the insertion point in a linked list costs O(n) even though changing the pointers is O(1).

### Week 2 — Hashing, stacks, queues, binary search

- **Learn:** [Hash table](README.md#hash-table), [Stack](README.md#stack), [Queue](README.md#queue), [Binary search](README.md#binary-search).
- **Build:** a stack on an array and on a linked list; a circular-buffer queue; a hash table with separate chaining *and* open addressing, including resize and load factor; binary search both iterative and recursive.
- **Practice:** 10 problems — valid parentheses, min stack, sliding-window maximum, first/last occurrence, search in rotated array, two-sum variants.
- **Accept when:** your hash table survives a forced resize without losing entries; you can explain why the load factor matters; you write binary search with the correct boundary condition on the first try; every problem is solved only after you state its complexity out loud.

### Week 3 — Trees and heaps

- **Learn:** [Trees](README.md#trees), [Trees intro](README.md#trees---intro), [BSTs](README.md#binary-search-trees-bsts), [Heap / Priority Queue](README.md#heap--priority-queue--binary-heap).
- **Build:** a BST with insert, search, delete (all three delete cases), min/max, successor/predecessor; all four traversals recursively and at least two iteratively; a binary heap with sift-up/sift-down.
- **Practice:** 10 problems — depth, balanced check, lowest common ancestor, level-order, validate BST, kth smallest, merge k lists.
- **Accept when:** you can delete a node with two children without notes; you can explain why an unbalanced BST degrades to O(n) and what a self-balancing tree buys you; you can describe BFS vs DFS trade-offs in terms of queue/stack memory.

### Week 4 — Sorting

- **Learn:** [Sorting](README.md#sorting). Skip bubble sort except as a cautionary tale.
- **Build:** insertion sort, merge sort (array and linked list), quicksort with both Lomuto and Hoare partitioning, heapsort. Write a table of best/average/worst time, space, and stability.
- **Practice:** 8 problems — sort colors, merge intervals, kth largest, custom comparator sorts, "is this sort stable" interviews.
- **Accept when:** you can code merge sort and quicksort from a blank file in 25 minutes each; you can say which of your sorts is stable and why; you can explain when O(n log n) loses to O(n²) insertion sort in practice.

### Week 5 — Graphs

- **Learn:** [Graphs](README.md#graphs).
- **Build:** an adjacency list and an adjacency matrix; BFS and DFS iterative and recursive; topological sort (Kahn and DFS); union-find with path compression and union by rank; cycle detection for directed and undirected graphs.
- **Practice:** 10 problems — number of islands, clone graph, course schedule, connected components, word ladder, rotting oranges.
- **Accept when:** you pick the right representation before coding and can justify it; you can write BFS and DFS without a template in front of you; you can explain why topological sort needs a DAG; union-find runs in near-constant amortized time and you can say why.

### Week 6 — Recursion, backtracking, dynamic programming

- **Learn:** [Recursion](README.md#recursion), [Dynamic Programming](README.md#dynamic-programming). This is the heaviest week; protect the time.
- **Build:** a backtracking template (subsets, permutations, combination sum) from scratch; DP solutions to climbing stairs, house robber, coin change, LIS (O(n²) then O(n log n)); 2D DP for unique paths and edit distance. For each, write the brute force, then memoize, then tabulate.
- **Practice:** 14 problems — 6 backtracking, 8 DP.
- **Accept when:** you can derive a recurrence and its base cases before writing code; you can convert any of your memoized solutions to bottom-up; you can state the state, transition, and space optimization for each DP problem you solved.

### Week 7 — Mixed practice and P1 topics

- **Learn:** [Tries](README.md#tries), [Bitwise operations](README.md#bitwise-operations), [String searching & manipulations](README.md#string-searching--manipulations), plus [Testing](README.md#testing) if you have time.
- **Build:** a trie with insert/search/prefix; a small bit-tricks sheet (single number, counting bits, subsets via bitmask).
- **Practice:** 15 problems in 4 timed sets of 35 minutes, mixing all prior weeks. Re-solve every problem you failed in weeks 1–6.
- **Accept when:** you finish a medium problem in 35 minutes including tests; you recognize the topic of a new problem within 5 minutes; your failed-problem log is empty or every entry is scheduled for re-solve.

### Week 8 — Mock interviews, review, and the application

- **Learn:** [Final Review](README.md#final-review) (short videos only), [Interview Process & General Interview Prep](README.md#interview-process--general-interview-prep), [Update Your Resume](README.md#update-your-resume).
- **Build:** nothing new. Repair only.
- **Practice:** 5 mock interviews, 45 minutes each, with a peer or recorded solo — talk, then code, then test. 10 re-solves from your failure log. Three behavioral stories written down.
- **Accept when:** you narrate your approach before writing code in every mock; you finish 4 of 5 mocks within time; you handle a hint without restarting; your resume is one page and your stories are two minutes each.

## Daily cadence

Ninety to 120 minutes, six days a week. One full rest day — you will lose more to burnout than to rest.

| Minutes | Block | Rule |
|---|---|---|
| 10 | Recall | Yesterday's flashcards and complexity table, no notes |
| 25 | Learn | **One** resource for the topic, then stop — even if it ends mid-sentence |
| 45 | Build | From scratch, no autocomplete for signatures, no copy-paste |
| 35 | Practice | One or two problems, timed, spoken aloud |
| 10 | Log | What broke, what you would do differently, next action |

If a day has only 45 minutes, do the Build block. Learn and Practice can wait; implementation cannot.

## Stop rules

These rules exist so that "minimum viable" stays viable.

- **20-minute problem rule.** Stuck for 20 minutes of real thinking? Read the editorial, close it, re-solve from scratch in 48 hours. Staring longer is not practice.
- **One-resource rule.** One video or one chapter per topic. If you can implement the structure, stop watching. You are not collecting lectures.
- **Two-day rule.** If a P0 topic is still opaque after two days, timebox a third day, then move on and book it for week 7. Do not lose a week to one topic.
- **Acceptance rule.** If you can pass the week's "accept when" test, move on even if the week's checklist is not fully ticked. If you cannot, repeat the week's build before starting the next one.
- **Week-8 rule.** Never skip the mocks. They are the only part that transfers directly to the interview.
- **Behind-schedule rule.** Two or more days behind? Cut P1, not sleep, and not week 8. Three or more days lost? Switch to the 12-week variant below.
- **Scope rule.** Anything not in P0 that a job description does not mention gets skipped without guilt.
- **Plan stop rule.** If after week 8 you still cannot solve an easy problem in 20 minutes, the schedule is not the problem; the language or the fundamentals are. Go back to [Choose a Programming Language](README.md#choose-a-programming-language) and rebuild.

## What to skip, and why

| Skip | Why | Revisit |
|---|---|---|
| [Design patterns](README.md#design-patterns) (full list) | Memorising 20 patterns does not help a data-structure interview | Only if your target uses them daily |
| [Combinatorics & probability](README.md#combinatorics-n-choose-k--probability) | High study cost, low frequency in general SWE loops | When a specific company asks |
| [NP-completeness](README.md#np-np-complete-and-approximation-algorithms) | You need recognition, not reductions | 15 minutes of reading, no more |
| [Caches](README.md#caches), [processes/threads](README.md#processes-and-threads), [networking](README.md#networking) | Better learned in a system design context later | After week 8 |
| [Unicode](README.md#unicode), [endianness](README.md#endianness), [floating point](README.md#floating-point-numbers) | Look-up trivia for most roles | Only for low-level or systems roles |
| Rest of [Even More Knowledge](README.md#even-more-knowledge) | Tries and DP are the only parts this plan needs; the long tail is optional depth | Never, on this plan |
| [Additional Learning](README.md#additional-learning) extras | Compilers, FFT, van Emde Boas trees: excellent, irrelevant here | Someday, for fun |
| [Papers](README.md#papers), [CS courses](README.md#computer-science-courses) | Months of material at this budget | Not on this plan |
| [System Design](README.md#system-design-scalability-data-handling) | Needs the vocabulary you build in weeks 1–8 | After week 8, unless you have 4+ years of experience |

Skipping is not laziness. Every hour has to come from somewhere, and these are the cheapest hours to cut.

## Tracking progress with the README checkboxes

The README uses GitHub task lists (`- [ ]` / `- [x]`). They are the source of truth for this plan.

1. Fork the repo and work on your fork; follow [How to use it](README.md#how-to-use-it) and disable pushing to upstream.
2. Tick only what you can *do*, not what you have *watched*. Week acceptance is the gate, not the tick.
3. Never open a pull request containing your personal checkboxes.
4. Summarize your state with the progress script from the repo root:

   ```bash
   python3 scripts/progress.py
   ```

   It reports how much of each section is checked and what is left. Treat it as a mirror, not a goal:
   a section can be 100% ticked and still not be interview-ready.
5. If the script is not in your checkout yet, use a paper log or a spreadsheet. The plan works fine without tooling.

## If 8 weeks is too tight: the 12-week variant

Eight weeks at 10–15 hours is genuinely aggressive, mostly because weeks 5 and 6 have no slack.
The safer version is 12 weeks at 6–8 hours: same order, same acceptance criteria, more repetition.

| 8-week week | 12-week weeks | What changes |
|---|---|---|
| 1 | 1–2 | Big-O gets its own week; arrays and linked lists get a full week |
| 2 | 3–4 | Hash table and binary search split; more array/string problems |
| 3 | 5 | Trees and heaps, unchanged |
| 4 | 6 | Sorting, plus one free day for re-implementing from memory |
| 5 | 7–8 | Graphs split: traversal week, then advanced (topo, union-find) |
| 6 | 9–10 | Backtracking week, then DP week |
| 7 | 11 | Mixed practice with heavier timed sets |
| 8 | 12 | Mocks, review, applications |

If you are on 12 weeks and your target includes system design, move the reading into week 11.

## After week 8

The plan ends; the preparation does not.

- **System design.** Start with [System Design, Scalability, Data Handling](README.md#system-design-scalability-data-handling). Two hours a week of reading and drawing is enough to stop being blindsided.
- **Mock interviews.** Two to three per week for three weeks. Vary the interviewer; a friendly mock is a comfortable lie.
- **Weak-topic repair.** Use your failure log. Re-solve failed problems after 3 days, then 7, then 21. If a whole topic is weak, redo that week's build, not the videos.
- **Keep the edge.** Two or three problems a week, one timed set a week, indefinitely.
- **Apply in parallel.** Start applying around week 6. The market gives better feedback than another video series.
- **Close the loop.** After each real interview, add every question you fumbled to the log and patch that topic before the next one.

## Scope note

This is a software-engineering interview plan. It does not cover frontend, full-stack, SQL, mobile,
DevOps, or machine learning, and it will not make you a specialist in any of them. The README says the
same in [What you won't see covered](README.md#what-you-wont-see-covered); for those paths, use
[roadmap.sh](https://roadmap.sh/) as the README suggests, or the [full plan](README.md#table-of-contents) for CS depth.

## Honest limits

This is a minimum viable path, not a guaranteed offer. Eight weeks at this budget is tight; twelve
weeks at 6–8 hours is the version most people actually finish. If you fall behind, cut scope — never
the mocks, never sleep. A finished minimum beats an abandoned maximum.

Corrections and improvements to this page are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).
