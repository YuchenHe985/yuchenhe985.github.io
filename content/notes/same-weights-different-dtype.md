---
slug: same-weights-different-dtype
title: Same weights, different dtype
order: 3
summary: Only 27.6% of a fine-tuned model's bytes match its base, and the encoding mattered more than the chunker.
---

How much of a fine-tuned model is already stored if you have its base? I cast the base to fp16, chunked both files with a content-defined chunker at Xet's chunk sizes, and counted shared chunks.

[[figure:shared-with-base]]

27.6% matches, and all of it is the token embedding, which LoRA did not train. Every projection matrix changed in about 99% of its values, so no chunk inside one can match.

Two things are worth knowing. First, the dtype decides more than the chunker does. As published, with a BF16 base and an F16 fine-tune, nothing is shared, not even the embedding that never changed, because every byte of a weight differs between the two encodings. Second, quantizing shrinks what can be shared: the bytes saved fall from 278 MB for GGUF F16 to 150 MB for Q8_0 and Q4_K_M.

If the base is already there, store the adapter, 8.8M parameters or about 35 MB in fp32, not the 988 MB merged file.

The per-tensor breakdown, the GGUF numbers and the caveats are in the [cdc-chunker README](https://github.com/YuchenHe985/cdc-chunker#deduplication-of-model-files).
