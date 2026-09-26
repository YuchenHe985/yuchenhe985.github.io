---
slug: simulation-cannot-see-a-cache
title: 模拟测试看不见缓存
order: 1
summary: 网关的故障测试全部通过，但我加的一条路由规则，在真实引擎上还是把 prefix cache 命中率从 59.1% 拉低到了 24.4%。
---

网关的故障测试全部通过了。这些测试用的是模拟节点，而模拟节点没有 KV cache，所以它们没法告诉我：我加的一条路由规则其实是坏的。

这条规则是：当请求的首选节点已满时，就溢出到排名下一位的节点。它通过了测试。之后我把几种策略放到 3 个真实的 llama.cpp 服务上跑：120 个请求，围绕 6 条共享的长 prompt，每次运行前都清空缓存。

[[figure:hit-rate]]

溢出把每条前缀分散到了多个节点上，结果每个节点都留不住它。原版网关只会排队：它的 prompt token 有 59.1% 命中 prefix cache，但四分之三的 prefill 工作都压在同一个节点上。改用 placement memory 加上有上限的 affinity wait 后，命中率与原版持平（61.5% 对 59.1%，3 次运行里分不出差别），负载则摊开了：最忙节点的占比从 73% 降到 43%。这只是命中率上的持平，不是胜出。

我从中学到的是：模拟测试只能测到你放进去的东西。我在意的那种故障，恰恰出在我没放进模拟里的那一块，所以任何模拟结果之后，下一步都应该是搭一个包含那一块的、尽可能小的真实系统。另外，这个修复默认是关闭的：启用 llama.cpp 自带的 host-memory cache 后，所有策略的命中率都能达到 95% 到 98%，路由几乎不起作用。

各策略的对比表、原始运行数据以及局限（一台机器、3 次运行、一个 0.5B 模型）都在 [radixgates README](https://github.com/YuchenHe985/radixgates#real-inference-engines-prefix-cache-behaviour-under-each-routing-policy) 里。
