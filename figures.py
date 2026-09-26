"""Figures for the site: plain HTML and CSS bars, drawn to one scale per chart.

Every number here is copied from a published result in one of the repositories named in the captions.
Charts are HTML rather than SVG so their text reflows and scales with the page and takes its colors
from the theme tokens in site.css.
"""
from html import escape


def _fmt(value, unit):
    return f"{value:.1f}{unit}" if unit == "%" else f"{value:.1f} {unit}"


def hbars(rows, *, vmax, ticks, unit, label, caption, compact=False, mark_label=None, mark_all=None):
    """Horizontal bars on a shared 0..vmax scale. Each row: label, value, kind, optional sub and mark."""
    grid = (ticks[1] - ticks[0]) / vmax * 100
    out = [
        f'<figure class="chart{" chart--compact" if compact else ""}" style="--grid:{grid:.2f}%" '
        f'role="group" aria-label="{escape(label)}">'
    ]
    out.append('<div class="chart-rows">')
    for row in rows:
        sub = f'<small>{escape(row["sub"])}</small>' if row.get("sub") else ""
        mark = ""
        position = row.get("mark", mark_all)
        if position is not None:
            mark = f'<i class="mark" style="--p:{position / vmax * 100:.2f}%"></i>'
        out.append(
            '<div class="chart-row">'
            f'<span class="chart-label">{escape(row["label"])}{sub}</span>'
            f'<div class="chart-track" aria-hidden="true"><i class="bar bar-{row.get("kind", "neutral")}" '
            f'style="--w:{row["value"] / vmax * 100:.2f}%"></i>{mark}</div>'
            f'<span class="chart-value">{_fmt(row["value"], unit)}</span>'
            "</div>"
        )
    tick_html = "".join(
        f'<span style="--p:{t / vmax * 100:.2f}%">{t:g}{"%" if unit == "%" else ""}</span>' for t in ticks
    )
    out.append(
        f'<div class="chart-row chart-axis" aria-hidden="true"><span></span><div class="chart-ticks">{tick_html}</div><span></span></div>'
    )
    out.append("</div>")
    legend = f'<p class="chart-legend"><i class="mark mark-key"></i> {escape(mark_label)}</p>' if mark_label else ""
    out.append(f"{legend}<figcaption>{caption}</figcaption></figure>")
    return "".join(out)


def stacks(rows, *, label, caption):
    """100% stacked bars. Each row: label and a list of (name, value, kind); values are printed under the bar."""
    out = [f'<figure class="chart chart--stack" role="group" aria-label="{escape(label)}"><div class="chart-rows">']
    for row in rows:
        segs = "".join(
            f'<i class="seg bar-{kind}" style="--w:{value:.2f}%"></i>' for _, value, kind in row["parts"]
        )
        vals = "".join(
            f'<li><i class="swatch bar-{kind}"></i><span class="chart-value">{value:.1f}%</span> {escape(name)}</li>'
            for name, value, kind in row["parts"]
        )
        out.append(
            '<div class="stack-row">'
            f'<span class="chart-label">{escape(row["label"])}</span>'
            f'<div class="stack" aria-hidden="true">{segs}</div>'
            f'<ul class="stack-values">{vals}</ul>'
            "</div>"
        )
    out.append(f"</div><figcaption>{caption}</figcaption></figure>")
    return "".join(out)


ROUTING_LABEL = "Share of prompt tokens served from the KV cache, by routing policy"

# radixgates README, "Real inference engines": cache capacity limited to the slots, median of 3 runs.
HIT_RATE_ROWS = [
    {"label": "Original", "sub": "hash % N, queues when full", "value": 59.1, "kind": "neutral"},
    {"label": "Spill when full", "sub": "the upgrade's first rule", "value": 24.4, "kind": "bad"},
    {"label": "Placement + wait", "sub": "the fix", "value": 61.5, "kind": "good"},
    {"label": "Round-robin", "sub": "no gateway", "value": 22.0, "kind": "mute"},
]

ROUTING_LABEL_ZH = "各路由策略下，prompt token 命中 KV cache 的占比"

# Same experiment as HIT_RATE_ROWS; row order and values must match exactly (see content/i18n.py's
# RadixGates "judgment" text, which quotes 61.5% / 59.1% from this same dataset).
HIT_RATE_ROWS_ZH = [
    {"label": "原版", "sub": "按 hash % N 分配，满了就排队", "value": 59.1, "kind": "neutral"},
    {"label": "满载溢出", "sub": "升级的第一条规则", "value": 24.4, "kind": "bad"},
    {"label": "放置 + 等待", "sub": "最终方案", "value": 61.5, "kind": "good"},
    {"label": "轮询", "sub": "不经过网关", "value": 22.0, "kind": "mute"},
]

FIGURES_ZH = {
    "hit-rate": lambda: hbars(
        HIT_RATE_ROWS_ZH,
        vmax=100,
        ticks=(0, 25, 50, 75, 100),
        unit="%",
        label=ROUTING_LABEL_ZH,
        caption=(
            "各路由策略下，从 KV cache 读取的 prompt token 占比。三个 llama.cpp 实例（Qwen2.5-0.5B，每个两个槽位）跑在一台 Apple M1 上；"
            "120 个请求，围绕六条共享的长 prompt；缓存容量限制在槽位数；每次运行前清空缓存；取三次运行的中位数。"
            "来源：radixgates，<code>benchmarks/results/real_engine_limited_cache/</code>。"
        ),
    ),
    "outcomes": lambda: stacks(
        [
            {
                "label": "Qwen2.5-0.5B-Instruct，未微调（Q4_K_M）",
                "parts": [("正确", 42.7, "good"), ("能运行，结果错误", 41.9, "bad"), ("无法运行", 15.3, "mute")],
            },
            {
                "label": "LoRA 微调后（Q4_K_M）",
                "parts": [("正确", 82.6, "good"), ("能运行，结果错误", 16.4, "bad"), ("无法运行", 1.0, "mute")],
            },
        ],
        label="每条生成的查询最终怎么样",
        caption=(
            "391 道留出测试题（来自 b-mc2/sql-create-context），每一道都在三个生成的 SQLite 数据库上执行模型生成的 SQL，并把结果行与参考查询比对。"
            "来源：llm-finetune-lab，<code>results/</code>。"
        ),
    ),
    "shared-with-base": lambda: hbars(
        [
            {"label": "safetensors（按发布时的原样）", "sub": "基础模型 BF16，微调模型 F16", "value": 0.0, "kind": "bad"},
            {"label": "safetensors，两者都转为 F16", "value": 27.6, "kind": "neutral"},
            {"label": "GGUF F16", "value": 28.0, "kind": "neutral"},
            {"label": "GGUF Q8_0", "value": 28.3, "kind": "neutral"},
            {"label": "GGUF Q4_K_M", "value": 37.8, "kind": "neutral"},
        ],
        vmax=100,
        ticks=(0, 25, 50, 75, 100),
        unit="%",
        label="微调后的文件中，能在基础模型文件的块里找到的比例",
        caption=(
            "Gear 分块器，采用 Xet 的限制（最小 8 KiB、平均 64 KiB、最大 128 KiB）。基础模型：Qwen2.5-0.5B-Instruct；微调模型：在所有注意力和 MLP 投影上做 "
            "rank-16 LoRA，合并后保存为 fp16。来源：cdc-chunker README，“Deduplication of model files”。"
        ),
    ),
    "loss-per-edit": lambda: hbars(
        [
            {"label": "Rabin", "sub": "CV 0.80", "value": 24.1, "kind": "neutral", "mark": 18.7},
            {"label": "Gear", "sub": "CV 0.79", "value": 20.1, "kind": "neutral", "mark": 17.8},
            {"label": "Gear，归一化", "sub": "CV 0.30", "value": 11.8, "kind": "good", "mark": 10.7},
        ],
        vmax=30,
        ticks=(0, 10, 20, 30),
        unit="KB",
        label="8 KiB 平均块大小下，每次修改产生的新字节",
        mark_label="公式预测：均值 × (1 + CV²)",
        caption=(
            "对一棵 67 MB 的源码树做 200 次随机修改后，新版本文件中在旧版本里找不到的字节数（每次修改）。定长 8 KiB 块每次修改丢失 330 KB，"
            "超出这张图的刻度。来源：cdc-chunker README，“Deduplication after edits”。"
        ),
    ),
    "hit-rate-compact": lambda: hbars(
        HIT_RATE_ROWS_ZH,
        vmax=100,
        ticks=(0, 25, 50, 75, 100),
        unit="%",
        label=ROUTING_LABEL_ZH,
        compact=True,
        caption=(
            "三个 llama.cpp 实例跑在同一台 Apple M1 上，120 次请求复用六条共享 prompt，"
            "缓存容量卡在槽位数，取 3 次运行的中位数。"
        ),
    ),
}

FIGURES = {
    "hit-rate": lambda: hbars(
        HIT_RATE_ROWS,
        vmax=100,
        ticks=(0, 25, 50, 75, 100),
        unit="%",
        label=ROUTING_LABEL,
        caption=(
            "Prompt tokens read from the KV cache, by routing policy. Three llama.cpp workers (Qwen2.5-0.5B, two slots each) "
            "on an Apple M1; 120 requests over six shared long prompts; cache capacity limited to the slots; caches erased "
            "before every run; median of 3 runs. Source: radixgates, <code>benchmarks/results/real_engine_limited_cache/</code>."
        ),
    ),
    "hit-rate-compact": lambda: hbars(
        HIT_RATE_ROWS,
        vmax=100,
        ticks=(0, 25, 50, 75, 100),
        unit="%",
        label=ROUTING_LABEL,
        compact=True,
        caption=(
            "Three llama.cpp workers on an Apple M1, 120 requests over six shared prompts, cache limited to the slots, "
            "median of 3 runs."
        ),
    ),
    "prefill-share": lambda: hbars(
        [
            {"label": "Original", "value": 73, "kind": "bad"},
            {"label": "Spill when full", "value": 44, "kind": "neutral"},
            {"label": "Placement + wait", "value": 43, "kind": "good"},
            {"label": "Round-robin", "value": 35, "kind": "mute"},
        ],
        vmax=100,
        ticks=(0, 25, 50, 75, 100),
        unit="%",
        label="Share of prefill work done by the busiest worker",
        mark_label="an even three-way split (33.3%)",
        mark_all=33.3,
        caption=(
            "Share of all prompt tokens evaluated by the busiest of the three workers. Six prompts hashed onto three nodes "
            "land unevenly; the original put three quarters of the prefill on one worker."
        ),
    ),
    "outcomes": lambda: stacks(
        [
            {
                "label": "Qwen2.5-0.5B-Instruct, no fine-tuning (Q4_K_M)",
                "parts": [("right", 42.7, "good"), ("run, wrong rows", 41.9, "bad"), ("did not run", 15.3, "mute")],
            },
            {
                "label": "Fine-tuned with LoRA (Q4_K_M)",
                "parts": [("right", 82.6, "good"), ("run, wrong rows", 16.4, "bad"), ("did not run", 1.0, "mute")],
            },
        ],
        label="What happened to each generated query",
        caption=(
            "391 held-out questions from b-mc2/sql-create-context, each scored by running the generated SQL on three generated "
            "SQLite databases and comparing the rows with the reference query. Source: llm-finetune-lab, <code>results/</code>."
        ),
    ),
    "guardrails": lambda: hbars(
        [
            {"label": "Answer everything", "sub": "answers 100% of questions", "value": 16.4, "kind": "bad"},
            {"label": "Constant not in question", "sub": "answers 96.7%", "value": 13.8, "kind": "neutral"},
            {"label": "Five samples must agree", "sub": "answers 78.0%", "value": 10.8, "kind": "neutral"},
            {"label": "Either signal", "sub": "answers 76.2%", "value": 9.1, "kind": "good"},
        ],
        vmax=20,
        ticks=(0, 5, 10, 15, 20),
        unit="%",
        label="Silent wrong answers among the questions still answered",
        mark_label="the 5% target",
        mark_all=5,
        caption=(
            "Share of the answers that were still returned that ran and gave the wrong rows, for four ways of withholding an answer. "
            "The 5% target was an assumption for an internal analytics assistant, not a requirement from a user."
        ),
    ),
    "shared-with-base": lambda: hbars(
        [
            {"label": "safetensors as published", "sub": "base BF16, fine-tuned F16", "value": 0.0, "kind": "bad"},
            {"label": "safetensors, both F16", "value": 27.6, "kind": "neutral"},
            {"label": "GGUF F16", "value": 28.0, "kind": "neutral"},
            {"label": "GGUF Q8_0", "value": 28.3, "kind": "neutral"},
            {"label": "GGUF Q4_K_M", "value": 37.8, "kind": "neutral"},
        ],
        vmax=100,
        ticks=(0, 25, 50, 75, 100),
        unit="%",
        label="Share of the fine-tuned file found in chunks of the base file",
        caption=(
            "Gear chunker at Xet's limits (8 KiB minimum, 64 KiB average, 128 KiB maximum). Base: Qwen2.5-0.5B-Instruct; fine-tuned: "
            "the same model after a rank-16 LoRA on every attention and MLP projection, merged and saved as fp16. "
            "Source: cdc-chunker README, “Deduplication of model files”."
        ),
    ),
    "elements-identical": lambda: hbars(
        [
            {"label": "Token embedding", "sub": "272 MB", "value": 100.0, "kind": "good"},
            {"label": "MLP projections", "sub": "628 MB", "value": 1.0, "kind": "bad"},
            {"label": "Attention projections", "sub": "88 MB", "value": 0.8, "kind": "bad"},
        ],
        vmax=100,
        ticks=(0, 25, 50, 75, 100),
        unit="%",
        label="Share of weights that are bit-for-bit identical, by tensor group",
        caption=(
            "safetensors, both fp16. The MLP and attention figures are the size-weighted means of the per-matrix values "
            "(0.6–1.5%) printed by <code>tools/compare_tensors.py</code>."
        ),
    ),
    "loss-per-edit": lambda: hbars(
        [
            {"label": "Rabin", "sub": "spread 0.80", "value": 24.1, "kind": "neutral", "mark": 18.7},
            {"label": "Gear", "sub": "spread 0.79", "value": 20.1, "kind": "neutral", "mark": 17.8},
            {"label": "Gear, normalized", "sub": "spread 0.30", "value": 11.8, "kind": "good", "mark": 10.7},
        ],
        vmax=30,
        ticks=(0, 10, 20, 30),
        unit="KB",
        label="New bytes per edit at 8 KiB average chunks",
        mark_label="predicted by mean × (1 + spread²)",
        caption=(
            "Bytes of a new file version not found in the old one, per edit, after 200 random edits to a 67 MB source tree. "
            "Fixed 8 KiB blocks lose 330 KB per edit and are off this scale. Source: cdc-chunker README, “Deduplication after edits”."
        ),
    ),
}


def render(name, lang="en", strict=False):
    """Chart HTML in one language. With strict=True a missing Chinese version is an error, not a silent English fallback."""
    if strict and lang == "zh" and name not in FIGURES_ZH:
        raise KeyError(f"no Chinese version of figure: {name}")
    table = FIGURES_ZH if lang == "zh" and name in FIGURES_ZH else FIGURES
    if name not in table:
        raise KeyError(f"unknown figure: {name}")
    return table[name]()
