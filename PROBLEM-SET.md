# The 8-Week Problem Set: 75 problems, 85 practice slots

> Companion to [The Minimal Path](MINIMAL-PATH.md). The schedule says what to study; this page says which problems to solve, in what order, and why those and not others.
>
> 简体中文版：[8 周题单](translations/PROBLEM-SET-cn.md) · English is the canonical version.

## What this is

A curated set of **75 unique problems** for weeks 1–7 of [the minimal path](MINIMAL-PATH.md), plus **10 re-solves** in week 8, for **85 practice slots** in total.

- Every problem is a canonical representative of a pattern the plan already teaches. None is here because it is trendy, and none requires LeetCode Premium.
- The count per week is fixed: 8, 10, 10, 8, 10, 14, 15. Week 8 adds no new problems.
- The order inside a week is the order to attempt them: warm-up first, then the pattern, then the harder variant.
- All 75 links go to LeetCode. There are no affiliate, referral, or tracking links, and no links to scraped mirrors.

Difficulty labels are LeetCode's own and they drift over time. Treat them as a hint, not a gate. A problem labelled Easy that takes you 40 minutes is a Medium *for you*, and that is the only label that matters.

## How to use this set

1. **35 minutes, timed, alone.** Start a timer before you read the problem. If the timer expires, stop. A finished brute force beats an unfinished optimal solution, and an unfinished attempt is data, not failure.
2. **Editorial only after 20 minutes of real thinking.** "Real thinking" means you have written something, traced it on a small case, and can say where you are stuck. Read just enough to unblock; do not read the full solution. Then close it and re-solve from a blank file within 48 hours.
3. **Re-solve failures after 3, 7, and 21 days.** Put the date in your failure log, not in your head. The first re-solve is from scratch; the later two are 15-minute recall passes.
4. **Do not tick a problem you only read.** A tick means: you wrote the code from a blank file, it passed the examples you invented, and you can state the time and space complexity out loud. Reading an editorial is not solving, and watching a video is not either.
5. **Say the pattern and the complexity before you code.** "This is a two-pointer scan, O(n) time, O(1) space" is the sentence an interviewer is waiting for. Practise it every time.
6. **Write two or three tests by hand.** Empty input, one element, duplicates, or the boundary your loop uses. It takes two minutes and catches most off-by-one bugs.

## Week index

| Week | Focus | New problems | Practice slots | Schedule | Problems |
|---|---|---|---|---|---|
| 1 | Big-O, arrays, linked lists | 8 | 8 | [Week 1](MINIMAL-PATH.md#week-1--complexity-and-linear-structures) | [Problems](#week-1--complexity-and-linear-structures) |
| 2 | Stack, queue, hash table, binary search | 10 | 10 | [Week 2](MINIMAL-PATH.md#week-2--hashing-stacks-queues-binary-search) | [Problems](#week-2--hashing-stacks-queues-binary-search) |
| 3 | Trees, BST, traversals, heap | 10 | 10 | [Week 3](MINIMAL-PATH.md#week-3--trees-and-heaps) | [Problems](#week-3--trees-and-heaps) |
| 4 | Sorting | 8 | 8 | [Week 4](MINIMAL-PATH.md#week-4--sorting) | [Problems](#week-4--sorting) |
| 5 | Graphs | 10 | 10 | [Week 5](MINIMAL-PATH.md#week-5--graphs) | [Problems](#week-5--graphs) |
| 6 | Recursion, backtracking, DP | 14 | 14 | [Week 6](MINIMAL-PATH.md#week-6--recursion-backtracking-dynamic-programming) | [Problems](#week-6--recursion-backtracking-dynamic-programming) |
| 7 | Mixed practice, P1 topics | 15 | 15 | [Week 7](MINIMAL-PATH.md#week-7--mixed-practice-and-p1-topics) | [Problems](#week-7--mixed-practice-and-p1-topics) |
| 8 | Mocks, review, application | 0 | 10 re-solves | [Week 8](MINIMAL-PATH.md#week-8--mock-interviews-review-and-the-application) | [Re-solves](#week-8--mock-interviews-review-and-the-application) |
| **Total** | | **75** | **85** | | |

## Week 1 — Complexity and linear structures

**8 problems · 4 array/string · 4 linked list**

Do these only after you have built the dynamic array and the singly linked list from the schedule. The point is to use the structures you wrote, not to meet them for the first time.

Matches [Week 1 of the minimal path](MINIMAL-PATH.md#week-1--complexity-and-linear-structures).

| # | Problem (LeetCode link) | Difficulty | Pattern | Why this one |
|---|---|---|---|---|
| 1 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Single pass / running minimum | The cleanest introduction to carrying state as you scan; no nested loops needed. |
| 2 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Easy | Two pointers (slow / fast) | In-place compaction is the template behind dozens of array rewrites. |
| 3 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Prefix and suffix products | Prefix/suffix is prefix sums with multiplication; it also forces O(1) extra space. |
| 4 | [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | Easy | Prefix sums | The canonical prefix-sum query; makes the O(1) range sum obvious. |
| 5 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | Iterative pointer reversal | Three pointers, one pass; every linked-list interview starts here. |
| 6 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Merge / dummy head | Dummy-node merging is reused in merge sort and merge k lists. |
| 7 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy | Fast and slow pointers | Floyd's algorithm, and the first half of finding the cycle entry. |
| 8 | [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Two pointers with a gap | Shows that “from the end” needs neither a length pass nor an array. |

## Week 2 — Hashing, stacks, queues, binary search

**10 problems · stack, queue, hash table · binary search**

Do the stack and hash problems after the build block; start binary search only once you can write a lower bound from memory. The last four problems are all binary search, deliberately: this pattern needs repetition more than the others. Sliding Window Maximum is deliberately held back for week 7 as a hard stretch; the monotonic stack here teaches the same index discipline at a lower cost.

Matches [Week 2 of the minimal path](MINIMAL-PATH.md#week-2--hashing-stacks-queues-binary-search).

| # | Problem (LeetCode link) | Difficulty | Pattern | Why this one |
|---|---|---|---|---|
| 9 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Stack | The simplest stack contract: push openers, match on closers. |
| 10 | [Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Design / auxiliary stack | Design under an O(1) constraint; the auxiliary-stack trick generalizes. |
| 11 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Monotonic stack | Next-greater-element is the monotonic stack pattern in its purest form. |
| 12 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Hash map | The “trade space for time” problem every hash-table question descends from. |
| 13 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Hash map + canonical key | Teaches key design: sort or count so that equal things collide. |
| 14 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Sliding window + hash set | The window template: expand right, shrink left, track one constraint. |
| 15 | [First Bad Version](https://leetcode.com/problems/first-bad-version/) | Easy | Binary search on a predicate | Binary search when the array is implicit; no index arithmetic to hide behind. |
| 16 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Binary search on a rotated array | Tests whether you understand the invariant, not a memorized template. |
| 17 | [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Medium | Binary search for boundaries | Lower and upper bound in one problem; the off-by-one clinic. |
| 18 | [Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Easy | Binary search lower bound | The cleanest lower-bound implementation; reuse it inside harder problems. |

## Week 3 — Trees and heaps

**10 problems · traversals, BST invariant, heap**

Work in order. The first five are recursion warm-ups; the next five each test a property you implemented in the build block. If a tree problem defeats you, redraw the tree on paper and trace your own traversal before touching the code. Merge k Sorted Lists is held back for week 7; the heap appears here as K Closest Points to Origin.

Matches [Week 3 of the minimal path](MINIMAL-PATH.md#week-3--trees-and-heaps).

| # | Problem (LeetCode link) | Difficulty | Pattern | Why this one |
|---|---|---|---|---|
| 19 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Easy | Tree DFS / recursion | The base case and recursive case in four lines; warm-up for everything else. |
| 20 | [Same Tree](https://leetcode.com/problems/same-tree/) | Easy | Simultaneous DFS | Two-pointer recursion over two trees; the shape of subtree comparisons. |
| 21 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Easy | Recursive swap | A one-line post-order operation once the recursion is clear. |
| 22 | [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | Easy | Post-order height | Return two facts — height and balanced — from one traversal. |
| 23 | [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | Post-order / global best | Height plus a running maximum; the “return one thing, update another” pattern. |
| 24 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | BFS with a queue | Level-by-level BFS and the queue-size loop that many problems reuse. |
| 25 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | In-order traversal / bounds | Why comparing only with the parent is wrong; bounds or in-order both work. |
| 26 | [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Easy | BST descent | Uses the ordering property instead of a full traversal. |
| 27 | [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Medium | In-order traversal | In-order gives sorted order; the kth visit is the answer, with O(1) extra space if you iterate. |
| 28 | [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Heap / priority queue | A bounded heap keeps the k best; the same shape solves top-k anything. |

## Week 4 — Sorting

**8 problems · sorting as a tool**

This week is not about reimplementing quicksort again. It is about choosing a sort, writing a comparator, and knowing when sorting is the right first move. The interval problems are the most common interview use of sorting.

Matches [Week 4 of the minimal path](MINIMAL-PATH.md#week-4--sorting).

| # | Problem (LeetCode link) | Difficulty | Pattern | Why this one |
|---|---|---|---|---|
| 29 | [Sort Colors](https://leetcode.com/problems/sort-colors/) | Medium | Three-way partition (Dutch flag) | One pass, O(1) space; the partition inside quicksort. |
| 30 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | Sort + sweep | Sort by start, then extend or emit; the interval template. |
| 31 | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Medium | Sorted scan / merge | The same sweep with a new interval; tests boundary handling. |
| 32 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | Sort + greedy | Minimum removals is maximum non-overlap; sorting by end is the proof. |
| 33 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Quickselect / heap | The selection problem behind “sort and index”; average O(n). |
| 34 | [Largest Number](https://leetcode.com/problems/largest-number/) | Medium | Custom comparator | A comparator that is not numeric order; tests sort-contract reasoning. |
| 35 | [Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/) | Easy | Two pointers on a sorted array | The largest square is at an end; merge from the outside in. |
| 36 | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | Easy | Merge from the back | In-place merging without a second array; the reverse-direction trick. |

## Week 5 — Graphs

**10 problems · grids, traversal, topological sort, union-find**

Before coding each one, say the representation out loud: grid, adjacency list, edge list, or implicit state graph. The last four are the ones candidates most often get wrong under time pressure. Word Ladder is held back for week 7 as a hard; Open the Lock is the same implicit-graph BFS without the hard tag.

Matches [Week 5 of the minimal path](MINIMAL-PATH.md#week-5--graphs).

| # | Problem (LeetCode link) | Difficulty | Pattern | Why this one |
|---|---|---|---|---|
| 37 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | Grid DFS / BFS | The canonical flood fill; count components by marking visited. |
| 38 | [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | Medium | Grid DFS with a return value | Flood fill that accumulates size instead of only marking. |
| 39 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | Medium | Graph traversal + hash map | Mapping old node to new node is the whole problem; tests traversal and copying. |
| 40 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | Multi-source BFS | All sources start at distance 0; the BFS level is the minute. |
| 41 | [Open the Lock](https://leetcode.com/problems/open-the-lock/) | Medium | BFS on an implicit graph | States and edges are generated, not given; the closest thing to Word Ladder without the hard tag. |
| 42 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Topological sort / cycle detection | Prerequisite ordering is a DAG check; Kahn or DFS. |
| 43 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Medium | Topological sort output | Same graph, but you must produce an order; tests the algorithm, not the yes/no. |
| 44 | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Medium | Reverse DFS from borders | Invert the direction: flow backwards from both oceans and intersect. |
| 45 | [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Medium | Union-find | The first edge that closes a cycle; path compression and union by rank in one problem. |
| 46 | [Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/) | Easy | BFS / DFS / union-find | A small graph you can solve three ways; use it to compare the approaches. |

## Week 6 — Recursion, backtracking, dynamic programming

**14 problems · 6 backtracking · 8 DP**

The order is deliberate. Backtracking first, because the recursion tree makes the DP transitions visible. For every DP problem: write the brute force, then memoize, then tabulate. If you cannot state the state and transition in one sentence, you are not ready to code.

Matches [Week 6 of the minimal path](MINIMAL-PATH.md#week-6--recursion-backtracking-dynamic-programming).

| # | Problem (LeetCode link) | Difficulty | Pattern | Why this one |
|---|---|---|---|---|
| 47 | [Subsets](https://leetcode.com/problems/subsets/) | Medium | Backtracking / include-exclude | The backtracking skeleton: choose, recurse, un-choose. |
| 48 | [Permutations](https://leetcode.com/problems/permutations/) | Medium | Backtracking with used[] | Order matters; the used array is the state you must restore. |
| 49 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | Medium | Backtracking with pruning | Reuse allowed, duplicates avoided by a start index; the pruning lesson. |
| 50 | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | Backtracking with constraints | Build only valid prefixes; the cleanest constraint-driven backtracking. |
| 51 | [Word Search](https://leetcode.com/problems/word-search/) | Medium | Backtracking on a grid | Visited marking and restoration inside a DFS; no extra memory. |
| 52 | [N-Queens](https://leetcode.com/problems/n-queens/) | Hard | Backtracking with attack sets | Constraint bookkeeping at scale; the hard version of “choose and un-choose”. |
| 53 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | 1-D DP | The Fibonacci recurrence you can derive from a decision tree. |
| 54 | [House Robber](https://leetcode.com/problems/house-robber/) | Medium | 1-D DP (take / skip) | State as “best up to i”; the first non-trivial recurrence. |
| 55 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Unbounded knapsack DP | Min coins for an amount; loop order matters and you should say why. |
| 56 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | Medium | LIS: O(n²) DP then patience | Two solutions for one problem; the O(n log n) version is worth knowing. |
| 57 | [Unique Paths](https://leetcode.com/problems/unique-paths/) | Medium | 2-D DP | Grid DP with a clean recurrence; start of 2-D tables and space rolling. |
| 58 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | Hard | 2-D DP on strings | Insert/delete/replace is the canonical string DP; derive the three cases. |
| 59 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | Medium | 2-D DP on strings | The parent of diff and many string problems; same table shape as edit distance. |
| 60 | [Word Break](https://leetcode.com/problems/word-break/) | Medium | DP over prefixes + dictionary | Decision DP with a set lookup; tests state definition more than code. |

## Week 7 — Mixed practice and P1 topics

**15 problems · mixed timed sets + P1 topics**

Run these as four timed sets of 35 minutes (4, 4, 4, 3 problems) instead of one long queue. The four hard problems are stretch goals: attempt them, but do not let them eat the week. If your failure log is not empty, re-solve from it before adding the stretch problems.

Matches [Week 7 of the minimal path](MINIMAL-PATH.md#week-7--mixed-practice-and-p1-topics).

| # | Problem (LeetCode link) | Difficulty | Pattern | Why this one |
|---|---|---|---|---|
| 61 | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Trie | Build the structure yourself; insert, search, and startsWith in one class. |
| 62 | [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Medium | Trie + DFS | Wildcards force a traversal; tests whether the trie is real or memorized. |
| 63 | [Single Number](https://leetcode.com/problems/single-number/) | Easy | XOR | XOR cancels pairs; the one bit trick worth memorizing. |
| 64 | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | Easy | Bit counting | n & (n-1) and shifting; the basic bit loop. |
| 65 | [Counting Bits](https://leetcode.com/problems/counting-bits/) | Easy | Bit DP | Reuses a smaller answer (i >> 1); bits meet DP. |
| 66 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy | Two pointers | Skip non-alphanumerics; a calm warm-up in a timed set. |
| 67 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | Expand around center | O(n²) but correct and easy to explain; the standard alternative to DP. |
| 68 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Hash + heap / bucket | Counting then selecting; two valid complexities. |
| 69 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | Hash map + doubly linked list | The design question that combines two structures under O(1). |
| 70 | [Rotate Image](https://leetcode.com/problems/rotate-image/) | Medium | Matrix transpose + reverse | In-place 2-D manipulation; index discipline. |
| 71 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | Heap / divide and conquer | Generalizes merging two lists; heap vs pairwise merge trade-off. |
| 72 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard | Monotonic deque | The hard version of the window: keep indices, drop dominated values. |
| 73 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Two pointers / stack | Multiple correct approaches; a good test of choosing one and justifying it. |
| 74 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | BFS shortest path | Implicit graph, shortest transformation; a classic hard with a clean BFS. |
| 75 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Prefix sum + hash map | Counting subarrays with a prefix-sum map; closes the loop from week 1. |

## Week 8 — Mock interviews, review, and the application

**0 new problems · 10 re-solves · 10 practice slots**

Week 8 adds no new problems. The ten slots are re-solves from your failure log, one per slot, 35 minutes each. The reason is simple: in week 8 you are rehearsing retrieval, not learning. A new problem teaches you something you will not have time to consolidate before the interview, and it steals time from the mocks.

Matches [Week 8 of the minimal path](MINIMAL-PATH.md#week-8--mock-interviews-review-and-the-application).

**How to pick the ten:**

- Start with every problem you logged as failed or as "read the editorial". If you have more than ten, take the ten oldest — those are the ones you have forgotten most.
- If you have fewer than ten, re-solve the problems that took you longest, not the ones you liked.
- Cover at least four different weeks. Do not spend all ten on DP because it feels scary; the loop tests breadth.
- For each re-solve: blank file, 35 minutes, no editorial until 20 minutes, then write down exactly what you missed.

| Slot | What to re-solve | Rule |
|---|---|---|
| 1–4 | The four oldest entries in the log | Full 35-minute attempt; no notes |
| 5–8 | The four slowest solves from weeks 5–6 | 25 minutes; if you stall, write the invariant before opening the editorial |
| 9–10 | Two problems you solved but could not explain | Explain out loud for 5 minutes first, then code |

Total practice slots: **75 new + 10 re-solves = 85**. That is the number [the minimal path](MINIMAL-PATH.md#the-8-week-schedule) budgets. If you do more than ten re-solves, you are choosing volume over mock interviews; the mocks are worth more.

## If you only have 40 hours

Forty hours is roughly 45–60 minutes per problem once you include the timed attempt, the editorial pass, and the 48-hour re-solve, which leaves room for the mocks. Drop the six hard problems, the duplicate patterns, and the week-7 stretch problems, and keep these 40 (the numbers are the `#` column from weeks 1–7, not LeetCode IDs):

| Week | Problem numbers (`#`) | Count |
|---|---|---|
| 1 | 1, 2, 4, 5, 7 | 5 |
| 2 | 9, 10, 12, 14, 16, 17 | 6 |
| 3 | 19, 21, 24, 25, 27 | 5 |
| 4 | 29, 30, 33, 35 | 4 |
| 5 | 37, 39, 40, 42, 45 | 5 |
| 6 | 47, 49, 51, 53, 55, 56, 57, 60 | 8 |
| 7 | 61, 63, 66, 67, 68, 69, 75 | 7 |
| **Total** | | **40** |

These 40 are not a different curriculum. They are the same patterns with the redundancy removed. Pair them with the five week-8 mocks and you still have a complete path.

## Do not grind

- **75 is the ceiling for this plan, not the entrance fee.** More problems after 75 buys almost nothing; re-solving the ones you failed buys a lot.
- **Do not open a new problem to avoid re-solving an old one.** That is procrastination with a progress bar.
- **Do not measure by count, streak, or contest rating.** Measure by whether you can solve an unseen medium in 35 minutes, explain the complexity, and test it.
- **If you finish early, re-solve.** If you are behind, cut the week-7 stretch problems (71–74), not week 8.
- **One problem solved from a blank file is worth five you only read with the editorial open.** The unit of progress is a blank file, not a green tick.

## A note on links

All 75 problem links point to LeetCode's problem pages, with no query parameters, affiliate IDs, or referral codes. If a problem is unavailable in your region, search for the exact title on LeetCode; do not use a scraped mirror.

Corrections to the problem choice are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).
