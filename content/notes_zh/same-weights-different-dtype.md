---
slug: same-weights-different-dtype
title: 权重相同，dtype 不同
order: 3
summary: 微调模型只有 27.6% 的字节和基础模型一致，起决定作用的是 dtype 编码，而不是分块器。
---

如果你已经有了基础模型，一个微调后的模型有多少内容其实已经存下了？我把基础模型转成 fp16，用内容定义分块器（块大小按 Xet 的设置）对两个文件分块，然后数共享的块。

[[figure:shared-with-base]]

27.6% 相同，而且全部来自 token embedding——LoRA 没有训练这一部分。每一个投影矩阵里大约 99% 的数值都变了，所以其中不可能有任何一个块能对上。

有两点值得记住。第一，dtype 比分块器的影响更大。按发布时的样子——基础模型是 BF16，微调模型是 F16——什么都共享不了，连从未改变的 embedding 也不行，因为同一个权重在两种编码下每个字节都不同。第二，量化会缩小可共享的部分：节省的字节数从 GGUF F16 的 278 MB，降到 Q8_0 和 Q4_K_M 的 150 MB。

如果基础模型已经在了，存 LoRA adapter 就行：8.8M 参数，fp32 下约 35 MB，而不是 988 MB 的合并后文件。

逐个张量的拆分、GGUF 的数字以及各项限制，都在 [cdc-chunker README](https://github.com/YuchenHe985/cdc-chunker#deduplication-of-model-files) 里。
