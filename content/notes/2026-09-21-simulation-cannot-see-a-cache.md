---
slug: simulation-cannot-see-a-cache
title: A simulation can't see a cache
date: 2026-09-21
summary: My gateway's failure tests all passed. A routing rule I had added still cut prefix-cache hits from 59% to 24% on real engines.
---

My gateway's failure benchmarks all passed. They use simulated workers, and a simulated worker has no KV cache, so they could not tell me that a routing rule I had added was bad.

The rule: when a request's preferred node is full, spill to the next-ranked one. It passed the tests. Then I ran the policies against three real llama.cpp servers: 120 requests over six long shared prompts, caches erased before every run.

[[figure:hit-rate]]

Spilling scattered each prefix over several nodes and evicted it from all of them. The original gateway, which just queues, kept 59% of its prompt tokens in cache, but sent three quarters of the prefill work to one worker. Placement memory plus a bounded affinity wait matched the original's hit rate (61.5% against 59.1%, indistinguishable over three runs) and spread the work: the busiest worker's share went from 73% to 43%. That is parity on cache hits, not a win.

What I took from it: a simulation only tests what you put in it. The failure I cared about lived in the piece I had left out, so after any simulated result the next step is the smallest real system that contains that piece. And the fix is off by default, because with llama.cpp's own host-memory cache every policy reaches 95 to 98% and routing barely matters.

The per-policy table, the raw runs and the limits (one machine, three runs, a 0.5B model) are in the [radixgates README](https://github.com/YuchenHe985/radixgates#real-inference-engines-prefix-cache-behaviour-under-each-routing-policy).
