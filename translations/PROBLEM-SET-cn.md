# 8 周题单：75 道题，85 个练习位

> [最小可行路径](MINIMAL-PATH-cn.md)的配套题单。日程告诉你学什么，这一页告诉你做哪些题、按什么顺序做，以及为什么是这些题。
>
> 英文版：[The 8-Week Problem Set](../PROBLEM-SET.md)。本文为简体中文翻译，**英文版为权威版本（canonical）**；如中英文表述不一致，以英文版为准。

## 这是什么

为[最小可行路径](MINIMAL-PATH-cn.md)第 1–7 周精选的 **75 道不重复的题**，加上第 8 周的 **10 次重做**，共 **85 个练习位**。

- 每道题都是计划中某个模式的经典代表。没有一道题是因为“最近很火”才入选，也没有一道需要 LeetCode Premium（会员）。
- 每周题量固定：8、10、10、8、10、14、15。第 8 周不新增题目。
- 每周内部的顺序就是做题顺序：先热身，再练模式，最后做更难的变体。
- 75 个链接全部指向 LeetCode，不含推广、返利、跟踪链接，也不链接抓取镜像站。

难度标签沿用 LeetCode 自己的标注，会随时间变化。把它当提示，不要当门槛。一道标着“简单”却让你做了 40 分钟的题，*对你来说*就是中等题——这个标签才有意义。

## 怎么用这份题单

1. **35 分钟，限时，独立完成。** 读题前先开计时器。时间到就停。写完的暴力解胜过没写完的最优解，没写完也是数据，不是失败。
2. **认真想满 20 分钟后才看题解。** “认真想”指的是：已经写了点东西、用小例子推过、能说出自己卡在哪。只看能让你继续下去的部分，不要通读完整题解。然后关掉题解，48 小时内从空白文件重做。
3. **做错的题在 3 天、7 天、21 天后重做。** 日期写进错题本，不要只记在脑子里。第一次重做从零开始；后两次是 15 分钟的回忆练习。
4. **只读过题解，不算做过。** 打勾的标准是：从空白文件写出代码，通过你自己设计的例子，并能口头说清时间与空间复杂度。看题解不算解题，看视频更不算。
5. **动手前先说出模式和复杂度。** “这是双指针扫描，O(n) 时间、O(1) 空间”就是面试官在等的那句话。每次练习都这么说一遍。
6. **手写两三个测试。** 空输入、单个元素、重复元素，或者你循环边界对应的那个例子。两分钟就能抓出大多数差一错误（off-by-one）。

## 每周索引

| 周 | 重点 | 新题 | 练习位 | 日程 | 题目 |
|---|---|---|---|---|---|
| 1 | 大 O、数组、链表 | 8 | 8 | [第 1 周](MINIMAL-PATH-cn.md#第-1-周--复杂度与线性结构) | [题目](#第-1-周--复杂度与线性结构) |
| 2 | 栈、队列、哈希表、二分查找 | 10 | 10 | [第 2 周](MINIMAL-PATH-cn.md#第-2-周--哈希栈队列二分查找) | [题目](#第-2-周--哈希栈队列二分查找) |
| 3 | 树、二叉搜索树、遍历、堆 | 10 | 10 | [第 3 周](MINIMAL-PATH-cn.md#第-3-周--树与堆) | [题目](#第-3-周--树与堆) |
| 4 | 排序 | 8 | 8 | [第 4 周](MINIMAL-PATH-cn.md#第-4-周--排序) | [题目](#第-4-周--排序) |
| 5 | 图 | 10 | 10 | [第 5 周](MINIMAL-PATH-cn.md#第-5-周--图) | [题目](#第-5-周--图) |
| 6 | 递归、回溯、动态规划 | 14 | 14 | [第 6 周](MINIMAL-PATH-cn.md#第-6-周--递归回溯动态规划) | [题目](#第-6-周--递归回溯动态规划) |
| 7 | 混合练习、P1 主题 | 15 | 15 | [第 7 周](MINIMAL-PATH-cn.md#第-7-周--混合练习与-p1-主题) | [题目](#第-7-周--混合练习与-p1-主题) |
| 8 | 模拟面试、复习、投递 | 0 | 10 次重做 | [第 8 周](MINIMAL-PATH-cn.md#第-8-周--模拟面试复习与投递) | [重做](#第-8-周--模拟面试复习与投递) |
| **合计** | | **75** | **85** | | |

## 第 1 周 —— 复杂度与线性结构

**8 道题 · 4 道数组/字符串 · 4 道链表**

等你按日程写好动态数组和单链表之后再做。目的是使用你亲手写的结构，而不是第一次见到它们。

对应[最小可行路径第 1 周](MINIMAL-PATH-cn.md#第-1-周--复杂度与线性结构)。

| # | 题目（LeetCode 链接） | 难度 | 模式 | 为什么是这道 |
|---|---|---|---|---|
| 1 | [买卖股票的最佳时机](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | 简单 | 单次遍历 / 维护最小值 | 最干净的“边扫描边维护状态”入门题，不需要嵌套循环。 |
| 2 | [删除有序数组中的重复项](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | 简单 | 双指针（慢 / 快） | 原地压缩是大量数组改写题共用的模板。 |
| 3 | [除自身以外数组的乘积](https://leetcode.com/problems/product-of-array-except-self/) | 中等 | 前缀积与后缀积 | 前缀/后缀就是乘法版的前缀和，同时逼你用 O(1) 额外空间。 |
| 4 | [区域和检索 - 数组不可变](https://leetcode.com/problems/range-sum-query-immutable/) | 简单 | 前缀和 | 最标准的前缀和查询，让 O(1) 区间和变得理所当然。 |
| 5 | [反转链表](https://leetcode.com/problems/reverse-linked-list/) | 简单 | 迭代指针反转 | 三个指针、一趟遍历；所有链表面试都从这里开始。 |
| 6 | [合并两个有序链表](https://leetcode.com/problems/merge-two-sorted-lists/) | 简单 | 归并 / 哑结点 | 哑结点归并会被归并排序和合并 K 个链表反复用到。 |
| 7 | [环形链表](https://leetcode.com/problems/linked-list-cycle/) | 简单 | 快慢指针 | Floyd 判圈算法，也是找出环入口的前半部分。 |
| 8 | [删除链表的倒数第 N 个节点](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | 中等 | 固定间距的双指针 | 说明“倒数第 N 个”既不需要先求长度，也不需要额外数组。 |

## 第 2 周 —— 哈希、栈、队列、二分查找

**10 道题 · 栈、队列、哈希表 · 二分查找**

栈和哈希的题放在“写”之后；二分查找要等到你能凭记忆写出下界（lower bound）再开始。最后四道全是二分查找，这是故意的：这个模式比其他模式更需要重复。滑动窗口最大值被故意留到第 7 周作为困难拉伸题；这里的单调栈以更低的成本练同样的下标纪律。

对应[最小可行路径第 2 周](MINIMAL-PATH-cn.md#第-2-周--哈希栈队列二分查找)。

| # | 题目（LeetCode 链接） | 难度 | 模式 | 为什么是这道 |
|---|---|---|---|---|
| 9 | [有效的括号](https://leetcode.com/problems/valid-parentheses/) | 简单 | 栈 | 最简单的栈契约：左括号入栈，右括号匹配。 |
| 10 | [最小栈](https://leetcode.com/problems/min-stack/) | 中等 | 设计 / 辅助栈 | 在 O(1) 约束下做设计，辅助栈技巧可以推广到很多题。 |
| 11 | [每日温度](https://leetcode.com/problems/daily-temperatures/) | 中等 | 单调栈 | 下一个更大元素是单调栈最纯粹的形式。 |
| 12 | [两数之和](https://leetcode.com/problems/two-sum/) | 简单 | 哈希表 | 所有哈希表题几乎都源自这道“用空间换时间”。 |
| 13 | [字母异位词分组](https://leetcode.com/problems/group-anagrams/) | 中等 | 哈希表 + 规范键 | 练键的设计：排序或计数，让相等的内容落到同一个键。 |
| 14 | [无重复字符的最长子串](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 中等 | 滑动窗口 + 哈希集合 | 窗口模板：右端扩张、左端收缩、维护一个约束。 |
| 15 | [第一个错误的版本](https://leetcode.com/problems/first-bad-version/) | 简单 | 对判定函数二分 | 数组是隐式的二分；没有下标运算可以躲。 |
| 16 | [搜索旋转排序数组](https://leetcode.com/problems/search-in-rotated-sorted-array/) | 中等 | 旋转数组上的二分 | 考的是你懂不懂循环不变式，而不是背没背模板。 |
| 17 | [在排序数组中查找元素的第一个和最后一个位置](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | 中等 | 二分查找左右边界 | 一道题同时练下界和上界，专治差一错误。 |
| 18 | [搜索插入位置](https://leetcode.com/problems/search-insert-position/) | 简单 | 二分查找下界 | 最干净的下界实现，之后可以直接嵌进更难的题里。 |

## 第 3 周 —— 树与堆

**10 道题 · 遍历、BST 性质、堆**

按顺序做。前五道是递归热身，后五道各自检验你在“写”里实现过的一个性质。如果某道树题卡住了，先在纸上重画这棵树，用你自己的遍历走一遍，再碰代码。合并 K 个升序链表被留到第 7 周；这一周的堆用“最接近原点的 K 个点”来练。

对应[最小可行路径第 3 周](MINIMAL-PATH-cn.md#第-3-周--树与堆)。

| # | 题目（LeetCode 链接） | 难度 | 模式 | 为什么是这道 |
|---|---|---|---|---|
| 19 | [二叉树的最大深度](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 简单 | 树的 DFS / 递归 | 四行写完边界和递归，是其他所有树题的热身。 |
| 20 | [相同的树](https://leetcode.com/problems/same-tree/) | 简单 | 双树同步 DFS | 两棵树同步递归，是子树比较类问题的基本形状。 |
| 21 | [翻转二叉树](https://leetcode.com/problems/invert-binary-tree/) | 简单 | 递归交换 | 递归想清楚后，后序操作只有一行。 |
| 22 | [平衡二叉树](https://leetcode.com/problems/balanced-binary-tree/) | 简单 | 后序求高度 | 一次遍历同时返回两个事实：高度和是否平衡。 |
| 23 | [二叉树的直径](https://leetcode.com/problems/diameter-of-binary-tree/) | 简单 | 后序 / 全局最优 | 高度加全局最大值，练“返回一个值、更新另一个值”的模式。 |
| 24 | [二叉树的层序遍历](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 中等 | 队列 BFS | 逐层 BFS 和按队列长度循环，很多题直接复用。 |
| 25 | [验证二叉搜索树](https://leetcode.com/problems/validate-binary-search-tree/) | 中等 | 中序遍历 / 上下界 | 说明为什么只和父节点比较是错的；上下界或中序都可以。 |
| 26 | [二叉搜索树的最近公共祖先](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 简单 | 利用 BST 性质下降 | 用有序性直接下降，而不是遍历整棵树。 |
| 27 | [二叉搜索树中第 K 小的元素](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | 中等 | 中序遍历 | 中序就是有序序列，第 k 次访问即答案；迭代写法只需 O(1) 额外空间。 |
| 28 | [最接近原点的 K 个点](https://leetcode.com/problems/k-closest-points-to-origin/) | 中等 | 堆 / 优先队列 | 有界堆维护最好的 k 个；所有 top-k 问题都是这个形状。 |

## 第 4 周 —— 排序

**8 道题 · 把排序当工具**

这一周不是再写一遍快速排序，而是练习选排序、写比较器，以及判断“先排序”是不是正确的第一步。区间类问题是排序在面试里最常见的用法。

对应[最小可行路径第 4 周](MINIMAL-PATH-cn.md#第-4-周--排序)。

| # | 题目（LeetCode 链接） | 难度 | 模式 | 为什么是这道 |
|---|---|---|---|---|
| 29 | [颜色分类](https://leetcode.com/problems/sort-colors/) | 中等 | 三路划分（荷兰国旗） | 一趟扫描、O(1) 空间，正是快速排序里的分区。 |
| 30 | [合并区间](https://leetcode.com/problems/merge-intervals/) | 中等 | 排序 + 扫描 | 按起点排序，再决定延伸还是输出；区间题模板。 |
| 31 | [插入区间](https://leetcode.com/problems/insert-interval/) | 中等 | 有序扫描 / 合并 | 同一套扫描加上一个新区间，专门考边界处理。 |
| 32 | [无重叠区间](https://leetcode.com/problems/non-overlapping-intervals/) | 中等 | 排序 + 贪心 | 最少删除等于最多保留；按右端点排序就是证明。 |
| 33 | [数组中的第 K 个最大元素](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 中等 | 快速选择 / 堆 | “排序后取下标”背后的选择问题，平均 O(n)。 |
| 34 | [最大数](https://leetcode.com/problems/largest-number/) | 中等 | 自定义比较器 | 比较器不再是数值大小，考你是否理解排序契约。 |
| 35 | [有序数组的平方](https://leetcode.com/problems/squares-of-a-sorted-array/) | 简单 | 有序数组双指针 | 最大的平方一定在两端，从外向内归并。 |
| 36 | [合并两个有序数组](https://leetcode.com/problems/merge-sorted-array/) | 简单 | 从后往前归并 | 不用第二个数组的原地归并，练反向填写的技巧。 |

## 第 5 周 —— 图

**10 道题 · 网格、遍历、拓扑排序、并查集**

动手前先说出图的表示方式：网格、邻接表、边列表，还是隐式状态图。最后四道是时间压力下最容易做错的部分。单词接龙作为困难题留到第 7 周；“打开转盘锁”是同一类隐式图 BFS，只是没有困难标签。

对应[最小可行路径第 5 周](MINIMAL-PATH-cn.md#第-5-周--图)。

| # | 题目（LeetCode 链接） | 难度 | 模式 | 为什么是这道 |
|---|---|---|---|---|
| 37 | [岛屿数量](https://leetcode.com/problems/number-of-islands/) | 中等 | 网格 DFS / BFS | 最经典的洪水填充，通过标记访问来数连通分量。 |
| 38 | [岛屿的最大面积](https://leetcode.com/problems/max-area-of-island/) | 中等 | 带返回值的网格 DFS | 洪水填充不只做标记，还要累加面积。 |
| 39 | [克隆图](https://leetcode.com/problems/clone-graph/) | 中等 | 图遍历 + 哈希表 | 整道题的核心就是旧节点到新节点的映射，同时考遍历和复制。 |
| 40 | [腐烂的橘子](https://leetcode.com/problems/rotting-oranges/) | 中等 | 多源 BFS | 所有源点距离都是 0，BFS 的层数就是分钟数。 |
| 41 | [打开转盘锁](https://leetcode.com/problems/open-the-lock/) | 中等 | 隐式图上的 BFS | 状态和边都要自己生成；最接近 Word Ladder 但没那么难。 |
| 42 | [课程表](https://leetcode.com/problems/course-schedule/) | 中等 | 拓扑排序 / 环检测 | 先修关系就是 DAG 判定；Kahn 或 DFS 都行。 |
| 43 | [课程表 II](https://leetcode.com/problems/course-schedule-ii/) | 中等 | 拓扑排序输出 | 同一张图，但要求输出顺序；考算法本身，而不是只答能不能。 |
| 44 | [太平洋大西洋水流问题](https://leetcode.com/problems/pacific-atlantic-water-flow/) | 中等 | 从边界反向 DFS | 把方向反过来：从两个大洋反向流，再取交集。 |
| 45 | [冗余连接](https://leetcode.com/problems/redundant-connection/) | 中等 | 并查集 | 第一条成环的边；一道题里用上路径压缩和按秩合并。 |
| 46 | [寻找图中是否存在路径](https://leetcode.com/problems/find-if-path-exists-in-graph/) | 简单 | BFS / DFS / 并查集 | 一张小图可以用三种方法解，正好用来比较不同思路。 |

## 第 6 周 —— 递归、回溯、动态规划

**14 道题 · 6 道回溯 · 8 道动态规划**

顺序是故意的。先回溯，因为递归树能让 DP 的状态转移变得可见。每道 DP 题都按“暴力 → 记忆化 → 递推”三步走。如果你不能用一句话说出状态和转移，就还没到写代码的时候。

对应[最小可行路径第 6 周](MINIMAL-PATH-cn.md#第-6-周--递归回溯动态规划)。

| # | 题目（LeetCode 链接） | 难度 | 模式 | 为什么是这道 |
|---|---|---|---|---|
| 47 | [子集](https://leetcode.com/problems/subsets/) | 中等 | 回溯 / 选或不选 | 回溯骨架：选择、递归、撤销选择。 |
| 48 | [全排列](https://leetcode.com/problems/permutations/) | 中等 | 带 used[] 的回溯 | 顺序有意义；used 数组就是必须恢复的状态。 |
| 49 | [组合总和](https://leetcode.com/problems/combination-sum/) | 中等 | 回溯 + 剪枝 | 允许重复使用，但用起点下标避免重复组合；剪枝入门。 |
| 50 | [括号生成](https://leetcode.com/problems/generate-parentheses/) | 中等 | 带约束的回溯 | 只构造合法前缀，是最干净的约束驱动回溯。 |
| 51 | [单词搜索](https://leetcode.com/problems/word-search/) | 中等 | 网格上的回溯 | 在 DFS 里标记和恢复访问状态，不需要额外内存。 |
| 52 | [N 皇后](https://leetcode.com/problems/n-queens/) | 困难 | 回溯 + 攻击集合 | 大规模约束维护，是“选择与撤销”的困难版。 |
| 53 | [爬楼梯](https://leetcode.com/problems/climbing-stairs/) | 简单 | 一维 DP | 从决策树就能推出的斐波那契递推。 |
| 54 | [打家劫舍](https://leetcode.com/problems/house-robber/) | 中等 | 一维 DP（选 / 不选） | 状态定义为“到 i 为止的最优值”，第一个不那么直接的递推。 |
| 55 | [零钱兑换](https://leetcode.com/problems/coin-change/) | 中等 | 完全背包 DP | 凑出金额的最少硬币数；循环顺序有讲究，而且要能讲清原因。 |
| 56 | [最长递增子序列](https://leetcode.com/problems/longest-increasing-subsequence/) | 中等 | LIS：O(n²) DP 再二分 | 一道题两种解法，O(n log n) 的耐心排序值得掌握。 |
| 57 | [不同路径](https://leetcode.com/problems/unique-paths/) | 中等 | 二维 DP | 网格 DP 的干净递推，二维表和滚动数组的起点。 |
| 58 | [编辑距离](https://leetcode.com/problems/edit-distance/) | 困难 | 字符串二维 DP | 插入/删除/替换是字符串 DP 的经典，三种情况要能推出来。 |
| 59 | [最长公共子序列](https://leetcode.com/problems/longest-common-subsequence/) | 中等 | 字符串二维 DP | diff 和很多字符串问题的祖先，表格形状与编辑距离相同。 |
| 60 | [单词拆分](https://leetcode.com/problems/word-break/) | 中等 | 前缀 DP + 字典 | 带集合查询的决策 DP，更考状态定义而不是代码量。 |

## 第 7 周 —— 混合练习与 P1 主题

**15 道题 · 混合限时套题 + P1 主题**

按四组 35 分钟限时来做（题量分别为 4、4、4、3），不要排成一条长队。四道困难题是拉伸项：可以尝试，但不要让它们吃掉整周。如果错题本还没清空，先重做错题，再加拉伸题。

对应[最小可行路径第 7 周](MINIMAL-PATH-cn.md#第-7-周--混合练习与-p1-主题)。

| # | 题目（LeetCode 链接） | 难度 | 模式 | 为什么是这道 |
|---|---|---|---|---|
| 61 | [实现 Trie（前缀树）](https://leetcode.com/problems/implement-trie-prefix-tree/) | 中等 | 字典树 | 亲手实现结构；一个类里完成插入、查找和前缀判断。 |
| 62 | [添加与搜索单词 - 数据结构设计](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | 中等 | 字典树 + DFS | 通配符逼你真正遍历；考的是理解而不是背模板。 |
| 63 | [只出现一次的数字](https://leetcode.com/problems/single-number/) | 简单 | 异或 | 异或能消掉成对的数，是少数值得记住的位运算技巧。 |
| 64 | [位 1 的个数](https://leetcode.com/problems/number-of-1-bits/) | 简单 | 位计数 | n & (n-1) 与移位，位运算循环的基本功。 |
| 65 | [比特位计数](https://leetcode.com/problems/counting-bits/) | 简单 | 位运算 DP | 复用更小的答案（i >> 1），位运算与 DP 的交汇。 |
| 66 | [验证回文串](https://leetcode.com/problems/valid-palindrome/) | 简单 | 双指针 | 跳过非字母数字字符，适合作为限时套题里的平稳热身。 |
| 67 | [最长回文子串](https://leetcode.com/problems/longest-palindromic-substring/) | 中等 | 中心扩展 | O(n²) 但正确且好讲，是回文 DP 之外的标准解法。 |
| 68 | [前 K 个高频元素](https://leetcode.com/problems/top-k-frequent-elements/) | 中等 | 哈希 + 堆 / 桶 | 先计数再选择，有两种都成立的复杂度。 |
| 69 | [LRU 缓存](https://leetcode.com/problems/lru-cache/) | 中等 | 哈希表 + 双向链表 | 把两个结构组合进 O(1) 约束的经典设计题。 |
| 70 | [旋转图像](https://leetcode.com/problems/rotate-image/) | 中等 | 矩阵转置 + 翻转 | 原地二维操作，练下标纪律。 |
| 71 | [合并 K 个升序链表](https://leetcode.com/problems/merge-k-sorted-lists/) | 困难 | 堆 / 分治 | 把合并两个链表推广到 k 个；比较堆与两两合并的取舍。 |
| 72 | [滑动窗口最大值](https://leetcode.com/problems/sliding-window-maximum/) | 困难 | 单调队列 | 窗口的困难版：存下标，丢掉被支配的值。 |
| 73 | [接雨水](https://leetcode.com/problems/trapping-rain-water/) | 困难 | 双指针 / 单调栈 | 多种正确解法，正好考你能不能选一种并讲清理由。 |
| 74 | [单词接龙](https://leetcode.com/problems/word-ladder/) | 困难 | BFS 最短路 | 隐式图上的最短变换，是 BFS 写法干净的经典困难题。 |
| 75 | [和为 K 的子数组](https://leetcode.com/problems/subarray-sum-equals-k/) | 中等 | 前缀和 + 哈希表 | 用前缀和哈希表数子数组，把第 1 周的内容闭环。 |

## 第 8 周 —— 模拟面试、复习与投递

**0 道新题 · 10 次重做 · 10 个练习位**

第 8 周不新增题目。十个练习位全部用来重做错题本里的题，一位一题，每题 35 分钟。原因很简单：第 8 周练的是提取，不是学习。新题会让你学到面试前来不及巩固的东西，还会挤占模拟面试的时间。

对应[最小可行路径第 8 周](MINIMAL-PATH-cn.md#第-8-周--模拟面试复习与投递)。

**怎么挑这 10 道：**

- 先把错题本里所有“做错”或“看了题解”的题列出来。如果超过 10 道，取最早的 10 道——它们是你忘得最多的。
- 如果不足 10 道，就重做耗时最长的题，而不是你喜欢的题。
- 至少覆盖 4 个不同的周。不要因为怕 DP 就把 10 道全花在 DP 上；这一轮考的是广度。
- 每次重做：空白文件、35 分钟、前 20 分钟不看题解，最后写下你到底漏了什么。

| 练习位 | 重做什么 | 规则 |
|---|---|---|
| 1–4 | 错题本里最早的 4 条 | 完整 35 分钟，不看笔记 |
| 5–8 | 第 5–6 周耗时最长的 4 道 | 25 分钟；卡住就先写出不变式，再看题解 |
| 9–10 | 做出来了但讲不清的 2 道 | 先口头讲 5 分钟，再写代码 |

练习位合计：**75 道新题 + 10 次重做 = 85**，与[最小可行路径](MINIMAL-PATH-cn.md#8-周日程)的预算一致。如果重做超过 10 次，你是在用题量换模拟面试的时间；模拟面试更值。

## 如果只有 40 小时

40 小时大约等于每题 45–60 分钟：包含限时尝试、看题解、48 小时后重做，剩下的时间留给模拟面试。砍掉 6 道困难题、重复模式和第七周的拉伸题，保留下面 40 道（题号对应第 1–7 周表格的 `#` 列，不是 LeetCode 题号）：

| 周 | 题号（`#` 列） | 数量 |
|---|---|---|
| 1 | 1, 2, 4, 5, 7 | 5 |
| 2 | 9, 10, 12, 14, 16, 17 | 6 |
| 3 | 19, 21, 24, 25, 27 | 5 |
| 4 | 29, 30, 33, 35 | 4 |
| 5 | 37, 39, 40, 42, 45 | 5 |
| 6 | 47, 49, 51, 53, 55, 56, 57, 60 | 8 |
| 7 | 61, 63, 66, 67, 68, 69, 75 | 7 |
| **合计** | | **40** |

这 40 道不是另一套课程，而是同一批模式去掉冗余后的最小集。拿它配合第 8 周的 5 场模拟面试，仍然是一条完整路径。

## 不要硬刷

- **75 是这份计划的上限，不是入场券。** 做完 75 道之后再刷，收益很小；重做做错的题，收益很大。
- **不要用新题来逃避重做旧题。** 那是带着进度条的拖延。
- **不要用题量、连续打卡天数或竞赛分来衡量自己。** 衡量标准是：能不能在 35 分钟内做出一道没见过的中等题，讲清复杂度，并写出测试。
- **提前做完就重做。** 如果落后了，砍第七周的拉伸题（71–74），不要砍第 8 周。
- **从空白文件做出一道题，胜过开着题解读五道。** 进度的单位是空白文件，不是绿色的勾。

## 关于链接

75 个题目链接全部指向 LeetCode 的题目页，不带查询参数、推广 ID 或返利码。如果某道题在你所在地区无法访问，请在 LeetCode 上搜索准确题名，不要使用抓取镜像站。

欢迎对选题提出修正：见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
