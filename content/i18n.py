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
        "eyebrow": "Yuchen He · Electrical Engineering, Penn",
        "h1": "I build and measure the systems that run AI models, and ask what the numbers leave out.",
        "lead": "I work across AI systems and the software–hardware boundary: multi-GPU inference, local models, systems code, and this semester firmware and SoCs. I like taking something that looks simple from the outside, opening it up, and finding out what actually determines how it behaves.",
        "seeking": "Looking for Summer 2027 internships in AI infrastructure and in embedded or hardware–software systems.",
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
        "notes_lang_note": "Notes are written in English.",
        "featured_label": "Start here",
    },
    "zh": {
        "eyebrow": "何雨宸 · 宾夕法尼亚大学电子工程",
        "h1": "我构建、测量让 AI 模型跑起来的系统，也追问数字没有说明的部分。",
        "lead": "我关注 AI 系统，以及软件和硬件交界的地方：多 GPU 推理、本地模型、系统代码，这学期开始学固件和 SoC。相比只把东西跑通，我更喜欢往里多追一层，弄清楚到底是什么决定了它的表现。",
        "seeking": "正在找 2027 年暑期实习，方向是 AI 基础设施，或者嵌入式 / 软硬件系统。",
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
        "now_body": "这学期在宾大：<strong>智能设备</strong>（ATmega328PB 裸机 C 开发）、<strong>SoC 架构</strong>（Ultra96 性能剖析）、<strong>数字集成电路与 VLSI</strong>。",
        "now_link": "更多关于我 →",
        "notes_lang_note": "每篇文章的全文目前只有英文版。",
        "featured_label": "先看这个",
        "note_en_tag": "英文全文",
    },
}

WORK_ZH = {
    "RadixGates": {
        "kind": "推理服务",
        "question": "节点挂掉时，一个小小的 Go 网关能不能撑住 SGLang 集群？它的前缀路由（prefix routing）在真实引擎上是否还有用？",
        "condition": "节点崩溃测试中的完整请求成功率，相比原始网关（4 个模拟节点，16 个客户端，30 秒）",
        "repo_label": "仓库",
        "stack": ["Go", "SGLang", "llama.cpp", "Docker", "Prometheus"],
        "measured": "相同故障注入条件下，节点崩溃场景的成功率从 85.2% 提升到 99.7%，新增 55 个测试。",
        "judgment": "在三个真实 llama.cpp 实例上，升级后的路由只是恢复到和原版一样的缓存命中率（61.5% 对 59.1%），不是超越——但把最忙节点的负载占比从 73% 降到了 43%。",
    },
    "llm-finetune-lab": {
        "kind": "模型微调",
        "question": "一个用 LoRA 微调过的 0.5B 模型，能不能在笔记本上回答数据库相关问题，而且数据不出本机？",
        "condition": "能正常执行但返回错误结果的比例（Q4_K_M 量化，391 道留出测试题，按执行结果打分）",
        "repo_label": "仓库",
        "stack": ["PyTorch", "PEFT", "DDP", "llama.cpp", "SQLite"],
        "measured": "执行正确率从 42.7% 提升到 82.6%；但有 16.4% 的答案能跑通却返回错误结果，字符串匹配根本发现不了。",
        "judgment": "护栏机制只能把静默错误率压到 9.1%，没达到 5% 的目标，所以结论是做成人工复核的建议工具，而不是自主作答系统。",
    },
    "cdc-chunker": {
        "kind": "存储",
        "question": "C++17 写的内容定义分块（content-defined chunking），能跑多快，同时保证分块结果不因为多线程而改变？",
        "condition": "8 线程下的吞吐，分块结果和单线程逐字节一致（256MiB 内存数据，平均块大小 8KiB，Apple M1）",
        "repo_label": "仓库",
        "stack": ["C++17", "CMake", "GitHub Actions"],
        "measured": "单线程约 2.0 GB/s，8 线程 7.4 GB/s，输出和单线程完全一致；200 次编辑后仍有 96.5% 的字节可复用。",
        "judgment": "合并 LoRA 权重后的模型文件只有 27.6% 的字节能复用——该分发的是适配器，不是合并后的完整模型。",
    },
    "llm-serving-eval-kit": {
        "kind": "工具",
        "question": "给定一个模型和几张 GPU，到底需要几张？服务启动失败是为什么？两次基准测试真的能比吗？",
        "condition": "在我的 RTX 4090 和 A100 两组实验之间不一致的因素，工具没有放任这个对比成立",
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
                "Consolidated 10+ SQL jobs into a dependency-aware PySpark/Spark SQL batch layer on Hive, cutting end-to-end runtime about 40%.",
                "Unified algorithm and regional forecasting schemas into one model; partitioning and predicate pushdown cut scanned data per query about 60%.",
            ],
        },
        {
            "role": "Data Analyst Intern",
            "org": "Brix Technology Services",
            "when": "Mar – Jun 2025",
            "where": "Canada",
            "bullets": [
                "Built an Excel VBA and Power Query analytics workflow for 10,000+ case records — rule-based deduplication, open/closed/reopened status classification and automated aggregation — improving reporting speed about 25%.",
                "Analysed three years of sales data from 1,000+ retail stores in MySQL, surfacing seasonal patterns and margin peaks, and built Power BI dashboards broken down by store, vendor and manager.",
            ],
        },
        {
            "role": "Investment Analyst",
            "org": "CITIC Securities",
            "when": "Jun – Sep 2024",
            "where": "Beijing, China",
            "bullets": [
                "Supported IPO diligence, valuation materials, and disclosure cross-checks — tracing a conclusion back to its evidence, a habit that now carries into how I write up benchmarks.",
            ],
        },
        {
            "role": "Investment Research Intern",
            "org": "Founder Securities",
            "when": "Mar – Jun 2024",
            "where": "Beijing, China",
            "bullets": [
                "Turned recurring market, industry, and ESG research into refreshable Power Query and VBA workflows; building the tool turned out to be as interesting as the analysis itself.",
                "Modelled multi-source financial and market data in Excel and Wind for KPI benchmarking and trend analysis, including multi-period ROE, margin and leverage analysis.",
            ],
        },
    ],
    "zh": [
        {
            "role": "大数据开发实习生",
            "org": "虾皮物流网络科技有限公司（Shopee）",
            "when": "2025.06 – 2025.09",
            "where": "中国深圳",
            "bullets": [
                "把 10 多个独立 SQL 任务整合为一套基于依赖关系调度的 PySpark / Spark SQL on Hive 批处理层，端到端运行时间缩短约 40%。",
                "统一算法侧与区域侧的预测数据结构；分区与谓词下推让单次查询扫描的数据量减少约 60%。",
            ],
        },
        {
            "role": "数据分析实习生",
            "org": "Brix Technology Services",
            "when": "2025.03 – 06",
            "where": "加拿大",
            "bullets": [
                "为 1 万多条案件记录搭建 Excel VBA 与 Power Query 分析流程：按规则去重、识别案件处于 open / closed / reopened 哪种状态、自动汇总，报告效率提升约 25%。",
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
        "p1": "I studied Computing and Commerce at Queen’s (honours, 2022–2026), then worked at Shopee on the PySpark and Hive layer behind logistics forecasting. I am now in the M.S.E. programme in Electrical Engineering at the University of Pennsylvania (2026–2028), moving further into systems and hardware.",
        "p2": "The projects here range from multi-GPU inference and cache-aware routing to C++ storage experiments and small local models. They look different, but I keep returning to the same question: what is happening underneath the abstraction, and how can I make it observable? This semester that question is extending into hardware through firmware, SoC architecture and VLSI.",
        "h2_why": "Why I build",
        "why_build": [
            "I first became interested in computing because ordinary software made me wonder what was happening underneath. What kept me there was the feedback: change the code, run it again, and something on the screen, or on a physical device, behaves differently. It is why I added Computing to Commerce from the start.",
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
            {"icon": "dance", "label": "Latin dance", "trait": "Persistence · 10 years",
             "note": "Ten years taught me that improvement is slow, and that it comes from repeating the basics until they hold."},
            {"icon": "draw", "label": "Drawing", "trait": "Close observation · 10 years",
             "note": "Drawing makes me look closely at how something is put together before I put a line down."},
            {"icon": "book", "label": "Reading", "trait": "Imagination",
             "note": "Harry Potter is the kind of world I love to disappear into and would love to go adventuring in. It keeps the imaginative side of my head in use."},
            {"icon": "badminton", "label": "Badminton", "trait": "Staying active",
             "note": "Recreational. It gets me moving and gives my head a rest from long stretches at a desk."},
            {"icon": "build", "label": "LEGO", "trait": "Enjoying the process",
             "note": "I care about the building, not the display: the point where separate pieces start to fit together."},
        ],
        "outside_close": "The habits carry over to my work: staying with something for years, looking closely, and caring about the process as much as the result.",
        
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
        "p1": "我在皇后大学读商科与计算机科学双学位（荣誉，2022–2026），之后在虾皮做物流预测背后的 PySpark / Hive 数据链路。现在在宾夕法尼亚大学读电子工程硕士（M.S.E.，2026–2028），继续往系统和硬件深入。",
        "p2": "网站上的项目跨度不小：多 GPU 推理、缓存路由、C++ 存储实验，还有本地运行的小模型。但我反复在追的其实是同一件事：一层抽象下面到底发生了什么，怎样才能把它真正观察出来。这学期，这个问题也延伸到了硬件这一侧：固件、SoC 架构和 VLSI。",
        "h2_why": "我为什么做这些",
        "why_build": [
            "我最早对计算机感兴趣，是因为日常用的软件会让我好奇：这些功能到底是怎么做出来的？让我一直学下去的，是写代码带来的直接反馈——改一点，再运行一次，屏幕上或者真实设备的行为就跟着变了。这也是我一开始就在商科之外加修计算机的原因。",
            "我也不太愿意把同一件事手动做两遍。在方正证券和 Brix，我把重复出现的报告做成了可以复用的工具；现在，是去测量更底层的系统：RadixGates 里，一条通过了全部模拟测试的路由规则，放到真实的 llama.cpp 上反而降低了缓存命中率，这个结果我同样留在了文章里。",
        ],
        "h2_approach": "我做项目的方式",
        "principles": [
            "<strong>从一个要做的决定出发。</strong> 文本转 SQL 那个项目问的是：一个小模型能不能作为自主作答系统上线？答案是写成一个决定，不是一个分数。",
            "<strong>把验收标准写下来，并说明它们从哪来。</strong> 我的验收标准是我自己设的假设，README 里写明了这一点。",
            "<strong>数字要带着它成立的条件。</strong> “611 毫秒 p95” 指的是 Apple M1、一次一个请求；四个并发时是 1.4 秒。",
            "<strong>说清楚什么会推翻这个结论。</strong> 每个仓库结尾都写了它的局限，路由那个结果的关键就在缓存有多大。",
        ],
        "see_note": "看这篇笔记。",
        "h2_outside": "工作之外",
        "outside_lead": "拉丁舞和画画是我坚持最久的两件事，各有差不多十年。",
        "hobbies": [
            {"icon": "dance", "label": "拉丁舞", "trait": "坚持 · 十年",
             "note": "十年下来我体会最深的是：进步是慢的，靠把基本功一遍遍练到稳。"},
            {"icon": "draw", "label": "画画", "trait": "留意细节 · 十年",
             "note": "画画让我在下笔之前，先看清一个东西是怎么构成的。"},
            {"icon": "book", "label": "阅读", "trait": "想象力",
             "note": "《哈利·波特》这样的世界，我愿意一头扎进去，也很憧憬去那里冒险。它让我脑子里想象力的那一面一直有在用。"},
            {"icon": "badminton", "label": "羽毛球", "trait": "保持活力",
             "note": "休闲打。让自己动起来，也让大脑从长时间伏案里歇一歇。"},
            {"icon": "build", "label": "LEGO", "trait": "享受过程",
             "note": "我在意的是一块块拼起来的过程，不是摆出来的成品：零散的部分开始咬合的那一刻。"},
        ],
        "outside_close": "这些习惯也会带进工作：能长期坚持一件事，愿意看仔细，也在意过程本身，而不只是结果。",
        
        "facts_label": "基本信息",
        "f_now": "现在", "f_now_v": "宾夕法尼亚大学电子工程硕士（M.S.E.）在读",
        "f_before": "之前", "f_before_v": "皇后大学商科与计算机科学双学位（荣誉）",
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

# Chinese titles/summaries for the note cards on /zh/. The notes themselves stay English-only.
NOTES_ZH = {
    "simulation-cannot-see-a-cache": {
        "title": "模拟测试看不见缓存",
        "summary": "网关的故障测试全部通过，但我加的一条路由规则，在真实引擎上还是把前缀缓存命中率从 59% 拉低到了 24%。",
    },
    "wrong-answers-that-raise-no-error": {
        "title": "不报错的错误答案",
        "summary": "微调后的 0.5B 模型写对 SQL 的比例约 83%。真正让我担心的是另外那 16%：能正常运行，却返回了错误的行。",
    },
    "same-weights-different-dtype": {
        "title": "权重相同，数据类型不同",
        "summary": "微调模型只有 27.6% 的字节和基础模型一致，起决定作用的是数据编码，而不是分块器。",
    },
    "average-chunk-size-is-not-the-cost": {
        "title": "平均块大小并不等于一次修改的代价",
        "summary": "一次修改更可能落在大块里，所以块大小的分布和它的平均值同样重要。",
    },
}
