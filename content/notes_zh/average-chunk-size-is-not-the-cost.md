---
slug: average-chunk-size-is-not-the-cost
title: 平均块大小并不等于一次修改的代价
order: 4
summary: 一次修改更可能落在大块里，所以块大小的分布和它的平均值同样重要。
---

一次修改会毁掉它所落入的那个块，而随机的一次修改更可能落进大块里。所以一次修改的预期损失并不是平均块大小，而大约是均值 ×（1 + CV²），其中 CV 是标准差除以均值（变异系数）。假如 4 KB 和 16 KB 的块数量相同，均值是 10 KB，但文件 80% 的内容落在大块里，所以一次修改的代价是 13.6 KB。

[[figure:loss-per-edit]]

normalized chunking 把 CV 从 0.80 压到 0.30，让每次修改丢失的数据减少约 40%：在 8 KiB 的目标块大小下，从 20.1 KB 降到 11.8 KB。公式对 normalized Gear 的预测是 10.7 KB（实测 11.8），对 Rabin 是 18.7 KB（实测 24.1）：量级对得上，但预测偏低，大概是因为靠近边界的修改还会波及相邻的块。定长块每次修改要丢 330 KB，超出了这张图的刻度。

我从中得到的：当两个设计的平均值相近时，要问代价究竟取决于哪个量。这里取决于二阶矩，而不是均值。

完整的对比表、块大小的影响以及各项限制，都在 [cdc-chunker README](https://github.com/YuchenHe985/cdc-chunker#deduplication-after-edits) 里。
