---
slug: average-chunk-size-is-not-the-cost
title: Average chunk size isn't what an edit costs
order: 4
summary: An edit is more likely to land in a big chunk, so the spread of chunk sizes matters as much as their average.
---

An edit destroys the chunk it lands in, and a random edit is more likely to land in a large chunk. So the expected loss is not the mean chunk size. It is about the mean times (1 + spread squared), where spread is the standard deviation divided by the mean. With equal numbers of 4 KB and 16 KB chunks the mean is 10 KB, but 80% of the file sits in the big chunks, so an edit costs 13.6 KB.

[[figure:loss-per-edit]]

Normalized chunking narrows the spread from 0.80 to 0.30 and cuts the data lost per edit by about 40%, from 20.1 KB to 11.8 KB at an 8 KiB target. The formula predicts 10.7 KB against 11.8 measured for normalized Gear, and 18.7 against 24.1 for Rabin: the right order, and low, probably because an edit near a boundary also disturbs its neighbour. Fixed blocks lose 330 KB per edit and are off the chart.

What I took from it: when two designs have similar averages, ask which quantity the cost really depends on. Here it was the second moment, not the mean.

The full table, the effect of chunk size and the caveats are in the [cdc-chunker README](https://github.com/YuchenHe985/cdc-chunker#deduplication-after-edits).
