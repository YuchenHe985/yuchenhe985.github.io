"""All bilingual UI strings and page copy. Chinese is written natively, not translated
word-for-word from the English (register and phrasing differ on purpose).

`work.json` and `figures.py` stay language-neutral (numbers, repo links); only the
surrounding prose here is duplicated per language.
"""

NAV = {
    "en": {"work": "Work", "experience": "Experience", "notes": "Notes", "about": "About"},
    "zh": {"work": "项目", "experience": "经历", "notes": "笔记", "about": "关于"},
}

HOME = {
    "en": {
        "eyebrow": "Penn Electrical Engineering · Queen’s Commerce + Computing",
        "h1": "I build systems behind AI — and I’m moving closer to the hardware.",
        "lead": "My work spans multi-GPU inference, local models and systems code, and now firmware and SoCs. I like getting a system running, then measuring the bottlenecks, failures and tradeoffs that abstractions hide.",
        "seeking": "Looking for Summer 2027 internships in AI infrastructure or embedded / hardware–software systems.",
        "cta_code": "See the code on GitHub",
        "cta_email": "Email",
        "panel_title": "A rule that looked harmless",
        "panel_link": "What I took from it →",
        "work_title": "Selected work",
        "evidence_label": "See the measurement",
        "measured_label": "Measured",
        "judgment_label": "Judgment",
        "exp_title": "Experience",
        "notes_title": "Notes",
        "now_title": "Now",
        "now_body": "This semester at Penn: <strong>Smart Devices</strong> (bare-metal C on an ATmega328PB), <strong>SoC Architecture</strong> (profiling on an Ultra96) and <strong>Digital ICs and VLSI</strong>.",
        "now_link": "More about me →",
        "featured_label": "Start here",
        "cap_title": "Capabilities",
        "capabilities": [
            {"name": "AI infrastructure", "body": "Multi-GPU inference, request routing, prefix-cache behaviour and serving evaluation.", "proof": "RadixGates · SGLang · llama.cpp · Docker"},
            {"name": "Systems & performance", "body": "C++ / Go systems work, concurrency, storage and performance measurement.", "proof": "cdc-chunker · 7.4 GB/s on 8 threads"},
            {"name": "Embedded & HW–SW", "body": "Bare-metal C, SoC profiling and digital IC fundamentals — a current focus at Penn.", "proof": "ATmega328PB · Ultra96 · VLSI"},
            {"name": "Data engineering", "body": "PySpark / Hive pipelines, SQL, data quality and operational observability.", "proof": "Shopee · 10+ jobs consolidated"},
        ],
        "notes_kicker": "Field notes",
        "final_title": "Let’s talk about systems.",
        "final_body": "I’m looking for Summer 2027 roles in AI infrastructure or embedded / hardware–software systems.",
        "final_email": "Email Yuchen",
    },
    "zh": {
        "eyebrow": "宾大电子工程 M.S.E. · Queen’s 商科 + 计算机双学位",
        "h1": "我做 AI 模型背后的系统，也在继续往软硬件交界处走。",
        "lead": "从多 GPU 推理、本地模型和系统代码，到这学期的固件与 SoC，我喜欢先把系统真正跑起来，再用实验把瓶颈、故障和取舍拆清楚。",
        "seeking": "寻找 2027 年暑期实习：AI 基础设施，或嵌入式 / 软硬件系统方向。",
        "cta_code": "在 GitHub 上看代码",
        "cta_email": "邮件联系",
        "panel_title": "一条看似无害的规则",
        "panel_link": "我从中学到了什么 →",
        "work_title": "代表项目",
        "evidence_label": "看实测数据",
        "measured_label": "实测",
        "judgment_label": "判断",
        "exp_title": "实习经历",
        "notes_title": "笔记",
        "now_title": "现在",
        "now_body": "这学期在宾大修：<strong>Smart Devices</strong>（ATmega328PB 裸机 C）、<strong>SoC 架构</strong>（在 Ultra96 上做性能剖析）、<strong>数字集成电路与 VLSI</strong>。",
        "now_link": "更多关于我 →",
        "featured_label": "先看这个",
        "cap_title": "能力重点",
        "capabilities": [
            {"name": "AI 基础设施", "body": "多 GPU 推理、请求路由、prefix cache 行为与 serving 评测。", "proof": "RadixGates · SGLang · llama.cpp · Docker"},
            {"name": "系统与性能", "body": "C++ / Go 系统编程、并发、存储与性能测量。", "proof": "cdc-chunker · 8 线程 7.4 GB/s"},
            {"name": "嵌入式 / 软硬件", "body": "目前在宾大进一步学习裸机 C、SoC 性能剖析，以及数字 IC / VLSI。", "proof": "ATmega328PB · Ultra96 · VLSI"},
            {"name": "数据工程", "body": "PySpark / Hive 数据链路、SQL、数据质量与运行监控。", "proof": "Shopee · 整合 10+ SQL 作业"},
        ],
        "notes_kicker": "实验笔记",
        "final_title": "如果你也在做这些系统，欢迎聊聊。",
        "final_body": "我正在寻找 2027 年暑期 AI 基础设施或嵌入式 / 软硬件系统方向的实习。",
        "final_email": "邮件联系",
    },
}

WORK_ZH = {
    "RadixGates": {
        "kind": "推理服务",
        "question": "节点挂掉后，一个轻量的 Go 网关还能不能让 SGLang 集群持续对外服务？它的 prefix 路由放到真实推理引擎上还有没有用？",
        "condition": "节点崩溃测试中无错误完成的请求占比，对比原始网关（4 个模拟节点、16 个并发客户端、30 s）",
        "repo_label": "仓库",
        "stack": ["Go", "SGLang", "llama.cpp", "Docker", "Prometheus"],
        "measured": "相同故障注入条件下，节点崩溃场景的请求成功率由 85.2% 提升到 99.7%；测试用例增至 55 个（go test -race）。",
        "judgment": "在 3 个真实 llama.cpp 实例上，升级后的路由策略只是把 prefix cache 命中率恢复到与原版持平（61.5% 对 59.1%），并没有超越；但最忙节点的 prefill 占比从 73% 降到了 43%。",
    },
    "llm-finetune-lab": {
        "kind": "模型微调",
        "question": "一个用 LoRA 微调过的 0.5B 模型，能不能在笔记本上回答数据库相关问题，而且数据不出本机？",
        "condition": "能正常执行但返回错误结果的比例（Q4_K_M 量化，391 道留出测试题，按执行结果打分）",
        "repo_label": "仓库",
        "stack": ["PyTorch", "PEFT", "DDP", "llama.cpp", "SQLite"],
        "measured": "执行准确率从 42.7% 提升到 82.6%；但有 16.4% 的答案能执行却返回错误结果，只看字符串匹配根本发现不了。",
        "judgment": "加上护栏后，静默错误率也只降到 9.1%，仍没达到 5% 的目标线，所以结论是做成人工复核的建议工具，而不是自主作答系统。",
    },
    "cdc-chunker": {
        "kind": "存储",
        "question": "用 C++17 实现的内容定义分块（CDC）能跑多快？上了多线程之后，分块结果还能和单线程完全一致吗？",
        "condition": "8 线程下的吞吐，分块结果和单线程逐字节一致（256MiB 内存数据，平均块大小 8KiB，Apple M1）",
        "repo_label": "仓库",
        "stack": ["C++17", "CMake", "GitHub Actions"],
        "measured": "单线程约 2.0 GB/s，8 线程 7.4 GB/s，输出和单线程完全一致；67 MB 源码树经 200 次编辑后，仍有 96.5% 的字节可复用。",
        "judgment": "合并 LoRA 权重后的模型文件只有 27.6% 的字节能复用——该分发的是 LoRA adapter，而不是合并后的完整模型。",
    },
    "llm-serving-eval-kit": {
        "kind": "工具",
        "question": "给定一个模型，需要几张 GPU？服务启动失败是什么原因？两次 benchmark 的结果真的可比吗？",
        "figure": "6 项因素",
        "condition": "我的 RTX 4090 与 A100 两组实验之间存在差异；工具会逐项标出，而不是让这次对比直接成立",
        "repo_label": "仓库",
        "stack": ["Python"],
    },
}

EXPERIENCE = {
    "en": [
        {
            "role": "Big Data Engineering Intern",
            "org": "Shopee Logistics Network Tech Co.",
            "when": "Jun – Sep 2025",
            "where": "Shenzhen, China",
            "bullets": [
                "Consolidated 10+ SQL jobs into a dependency-aware PySpark/Spark SQL batch layer on Hive, standardizing incremental and snapshot patterns and cutting end-to-end runtime by about 40%.",
                "Unified algorithm and regional forecasting schemas into a compute-once, multi-consume model; partitioning and predicate pushdown cut scanned data per query by about 60%.",
                "Built WMAPE model-version dashboards and automated checks for null rate, volume drift and freshness; investigated pipeline and data-quality anomalies with algorithm and operations teams.",
            ],
        },
        {
            "role": "Data Analyst Intern",
            "org": "Brix Technology Services",
            "when": "Mar – Jun 2025",
            "where": "Canada",
            "bullets": [
                "Built an Excel VBA and Power Query analytics workflow for 10,000+ case records — rule-based deduplication, open/closed/reopened status classification and automated aggregation — improving reporting speed about 25%.",
                "Analyzed three years of sales data from 1,000+ retail stores in MySQL, surfacing seasonal patterns and margin peaks, and built Power BI dashboards broken down by store, vendor and manager.",
            ],
        },
        {
            "role": "Investment Analyst Intern",
            "org": "CITIC Securities",
            "when": "Jun – Sep 2024",
            "where": "Beijing, China",
            "bullets": [
                "Supported IPO due diligence, valuation materials and disclosure cross-checks — tracing a conclusion back to its evidence, a habit that now carries into how I write up benchmarks.",
            ],
        },
        {
            "role": "Investment Research Intern",
            "org": "Founder Securities",
            "when": "Mar – Jun 2024",
            "where": "Beijing, China",
            "bullets": [
                "Turned recurring market, industry, and ESG research into refreshable Power Query and VBA workflows; building the tool turned out to be as interesting as the analysis itself.",
                "Modeled multi-source financial and market data in Excel and Wind for KPI benchmarking and trend analysis, including multi-period ROE, margin and leverage analysis.",
            ],
        },
    ],
    "zh": [
        {
            "role": "大数据开发实习生",
            "org": "虾皮物流网络科技有限公司（Shopee）",
            "when": "2025.06 – 09",
            "where": "深圳",
            "bullets": [
                "将 10+ 个独立 SQL 作业整合为基于依赖调度的 PySpark / Spark SQL（Hive）批处理链路，统一增量与全量快照的处理模式，端到端耗时降低约 40%。",
                "统一算法侧与区域侧的预测数据表结构，整合为“一次计算、多方复用”的数据模型；通过分区与谓词下推，单次查询扫描数据量减少约 60%。",
                "搭建按 WMAPE 对比模型版本的看板，并配套空值率、数据量波动、时效性等自动化校验；与算法、运营团队联合排查链路和数据异常。",
            ],
        },
        {
            "role": "数据分析实习生",
            "org": "Brix Technology Services",
            "when": "2025.03 – 06",
            "where": "加拿大",
            "bullets": [
                "为 1 万多条案件记录搭建 Excel VBA + Power Query 分析流程：按规则去重、识别案件处于 open / closed / reopened 哪种状态、自动汇总，报告效率提升约 25%。",
                "用 MySQL 分析 1,000 多家门店三年的销售数据，找出季节性规律和毛利高峰，并用 Power BI 做出按门店、供应商、经理拆分的看板。",
            ],
        },
        {
            "role": "投资分析实习生",
            "org": "中信证券",
            "when": "2024.06 – 09",
            "where": "中国北京",
            "bullets": [
                "参与 IPO 尽职调查、估值材料和信息披露核查；这段经历让我养成了每个结论都回到原始材料核对的习惯，现在写技术实验报告时也一样。",
            ],
        },
        {
            "role": "行业研究实习生",
            "org": "方正证券",
            "when": "2024.03 – 06",
            "where": "中国北京",
            "bullets": [
                "把行业、市场和 ESG 研究里重复出现的部分做成可刷新的 Power Query 和 VBA 工作流——发现自己搭工具跟做分析本身一样投入。",
                "整合多来源的财务与市场数据，做 KPI 对标和趋势分析；用 Wind 数据做多期财务建模，测算 ROE、利润率结构和杠杆率。",
            ],
        },
    ],
}

ABOUT = {
    "en": {
        "eyebrow": "About",
        "h1": "I keep moving closer to the machine.",
        "p1": "I studied Computing and Commerce at Queen’s (honours, 2022–2026), then spent the summer of 2025 working on the PySpark and Hive layer behind logistics forecasting at Shopee. I am now in the M.S.E. program in Electrical Engineering at the University of Pennsylvania (2026–2028), moving further into systems and hardware.",
        "p2": "The projects here range from multi-GPU inference and cache-aware routing to C++ storage experiments and small local models. They look different, but I keep returning to the same question: what is happening underneath the abstraction, and how can I make it observable? This semester that question is extending into firmware, SoC architecture and VLSI.",
        "journey_title": "How I got here",
        "journey": [
            {"label": "Queen’s", "detail": "Commerce + Computing"},
            {"label": "Founder / Brix", "detail": "Turn recurring analysis into reusable tools"},
            {"label": "Shopee", "detail": "Build and debug forecasting data pipelines"},
            {"label": "Systems work", "detail": "Serving · storage · local models"},
            {"label": "Penn EE", "detail": "Firmware · SoC · VLSI"},
        ],
        "h2_why": "Why I build",
        "why_build": [
            "I first became interested in computing because ordinary software made me wonder what was happening underneath. What kept me there was the feedback: change the code, run it again, and something on the screen, or on a physical device, behaves differently. That feedback is part of why I chose to study Computing alongside Commerce.",
            "I also dislike doing the same thing twice by hand. At Founder Securities and Brix that meant turning recurring reports into reusable tools. Now it means measuring the systems underneath: in RadixGates, a routing rule passed every simulated test but cut the cache hit rate on real llama.cpp workers, and that result stayed in the write-up.",
        ],
        "h2_approach": "How I approach a project",
        "principles": [
            "<strong>Start from a decision.</strong> The text-to-SQL project asks whether a small model should ship as an autonomous answerer, and the answer is written as a decision, not as a score.",
            "<strong>Write down the acceptance criteria, and say where they came from.</strong> Mine were assumptions, and the README says so.",
            "<strong>Report the condition with the number.</strong> “611 ms p95” means an Apple M1, one request at a time; with four in parallel it is 1.4 s.",
            "<strong>Say what would change the conclusion.</strong> Every repository ends with its limits, and the routing result turned on the size of a cache.",
        ],
        "see_note": "See the note.",
        "h2_outside": "Outside work",
        "outside_lead": "Latin dance and drawing are the two things I have kept up longest, about ten years each.",
        "hobbies": [
            {"icon": "dance", "label": "Latin dance", "trait": "",
             "note": "Part of my life for about ten years."},
            {"icon": "draw", "label": "Drawing", "trait": "",
             "note": "Another thing I have kept up for about a decade."},
            {"icon": "book", "label": "Reading", "trait": "",
             "note": "I like worlds I can disappear into. Harry Potter is one I would happily go exploring in."},
            {"icon": "badminton", "label": "Badminton", "trait": "",
             "note": "Recreational, mostly for exercise."},
            {"icon": "build", "label": "LEGO", "trait": "",
             "note": "I enjoy the building itself more than having a showpiece at the end."},
        ],
        "outside_close": "They are a different part of my life, but the habits are familiar: patience, repetition, and enjoying the process of making something better.",
        
        "facts_label": "Facts",
        "f_now": "Now", "f_now_v": "M.S.E. Electrical Engineering, Penn",
        "f_before": "Before", "f_before_v": "Honours dual degree in Computing and Commerce, Queen’s University",
        "f_looking": "Looking for", "f_looking_v": "Summer 2027 internships: AI infrastructure; embedded and hardware–software systems",
        "f_code": "Code",
        "f_linkedin": "LinkedIn",
        "f_email": "Email",
        "f_based": "Based in", "f_based_v": "Philadelphia, PA",
    },
    "zh": {
        "eyebrow": "关于",
        "h1": "我一直在往系统更底层走。",
        "p1": "我本科在女王大学同时读商科和计算机。2025 年夏天在 Shopee，我做的是物流预测背后的 PySpark / Hive 数据链路；现在到宾大读电子工程 M.S.E.（2026–2028），继续往系统和硬件这一层深入。",
        "p2": "网站上的项目跨度不小：多 GPU 推理、缓存路由、C++ 存储实验，还有本地运行的小模型。但我反复在追的其实是同一件事：一层抽象下面到底发生了什么，怎样才能把它真正观察出来。这学期，我也开始从固件、SoC 架构和 VLSI 往硬件这一侧继续深入。",
        "journey_title": "我怎么走到这里",
        "journey": [
            {"label": "女王大学", "detail": "商科 + 计算机"},
            {"label": "方正 / Brix", "detail": "把重复分析做成可复用工具"},
            {"label": "Shopee", "detail": "做物流预测数据链路"},
            {"label": "独立系统项目", "detail": "推理服务 · 存储 · 本地模型"},
            {"label": "宾大 EE", "detail": "固件 · SoC · VLSI"},
        ],
        "h2_why": "我为什么做这些",
        "why_build": [
            "我最早对计算机感兴趣，是因为日常用的软件会让我好奇：这些功能到底是怎么做出来的？让我一直学下去的，是写代码带来的直接反馈——改一点，再运行一次，屏幕上或者真实设备的行为就跟着变了。这也是我后来选择把计算机和商科一起读下去的原因之一。",
            "我也不太愿意把同一件事手动做两遍。在方正证券和 Brix，我把重复出现的报告做成了可复用的工具；现在，我把同样的习惯用在更底层的系统上——RadixGates 里，一条通过了全部模拟测试的路由规则，放到真实的 llama.cpp 上反而拉低了 prefix cache 命中率，这个结果我原样写进了笔记。",
        ],
        "h2_approach": "我做项目的方式",
        "principles": [
            "<strong>从要做的决策出发。</strong> 文本转 SQL 这个项目要回答的是：小模型能不能作为自主作答系统上线？结论写成一个决策，而不是一个分数。",
            "<strong>把验收标准写下来，并说明它们从哪来。</strong> 我的验收标准是我自己设的假设，README 里写明了这一点。",
            "<strong>数字要带着它成立的条件。</strong> “p95 611 ms”指的是 Apple M1 上单请求串行的结果；4 并发时是 1.4 s。",
            "<strong>说清楚什么会推翻这个结论。</strong> 每个仓库的结尾都写了局限；路由这个结论是否成立，取决于缓存容量有多大。",
        ],
        "see_note": "看这篇笔记。",
        "h2_outside": "工作之外",
        "outside_lead": "拉丁舞和画画是我坚持最久的两件事，各有差不多十年。",
        "hobbies": [
            {"icon": "dance", "label": "拉丁舞", "trait": "",
             "note": "跳了差不多十年，是我坚持最久的爱好之一。"},
            {"icon": "draw", "label": "画画", "trait": "",
             "note": "也画了差不多十年。"},
            {"icon": "book", "label": "阅读", "trait": "",
             "note": "我喜欢《哈利·波特》这种能让人一头钻进去的世界——真的会想进去冒险一圈。"},
            {"icon": "badminton", "label": "羽毛球", "trait": "",
             "note": "休闲打，主要是活动身体、放松一下。"},
            {"icon": "build", "label": "LEGO", "trait": "",
             "note": "比起把成品摆出来，我更享受从一堆零件慢慢拼起来的过程。"},
        ],
        "outside_close": "这些爱好和工程不是一回事，但留下来的习惯很相似：慢慢练、反复改，也享受把一件东西一点点做完整的过程。",
        
        "facts_label": "基本信息",
        "f_now": "现在", "f_now_v": "宾夕法尼亚大学电子工程硕士（M.S.E.）在读",
        "f_before": "之前", "f_before_v": "女王大学商科与计算机科学双学位（荣誉）",
        "f_looking": "求职方向", "f_looking_v": "2027 年暑期实习：AI 基础设施；嵌入式与软硬件系统",
        "f_code": "代码",
        "f_linkedin": "领英",
        "f_email": "邮箱",
        "f_based": "常驻", "f_based_v": "美国费城",
    },
}

FOOTER = {
    "en": {"note": "Plain HTML and CSS. Fonts under the SIL Open Font License."},
    "zh": {"note": "原生 HTML / CSS 构建。字体遵循 SIL 开源字体协议。"},
}

NOT_FOUND = {
    "en": {"eyebrow": "404", "h1": "That page isn’t here", "body": "Try the", "home": "home page", "or": "or the", "notes_word": "notes"},
    "zh": {"eyebrow": "404", "h1": "这个页面不存在", "body": "试试", "home": "首页", "or": "或者", "notes_word": "笔记"},
}


NOTES_PAGE = {
    "en": {
        "eyebrow": "Notes",
        "h1": "What a measurement taught me",
        "lead": "Short notes on one thing each. The tables, raw data and limits are in the repositories they link to.",
        "description": "Short notes on what a measurement taught me.",
        "newer": "Newer",
        "older": "Older",
        "more": "More notes",
    },
    "zh": {
        "eyebrow": "笔记",
        "h1": "一次测量教会了我什么",
        "lead": "每篇只讲一件事。表格、原始数据和各项限制，都在它们所链接的仓库里。",
        "description": "每篇讲一件事：一次测量教会了我什么。",
        "newer": "较新",
        "older": "较早",
        "more": "更多笔记",
    },
}
