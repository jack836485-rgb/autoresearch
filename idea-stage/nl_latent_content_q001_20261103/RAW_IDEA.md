# 输入问题卡

## 来源
- 地图：`path-stage/LatentCoT_NL研究地图_20261103`，问题 Q001。检索日 2026-11-03，近期窗口 2026-05-03 至 2026-11-03。
- 机构口径：白名单 + QS 前 50；白名单外的作品单独标注。
- 同一地图的 Q002 已于同日打磨（Call 1 得 5.0），用户随后转向 Q001。

## 具体问题
在真实自然语言任务（检索增强问答、Agent 决策、机器翻译、安全护栏、KBQA）上训练的 latent 推理模型，报告的收益究竟来自 latent 链里针对该输入的内容，还是只来自额外的计算步或共享的连续前缀（pause-token 式效应）？在合成逻辑任务和化学任务上，已经观察到"删除链会伤性能、替换内容几乎不变"；但上述应用方法本身没有做内容替换或 pause 对照。

## 关键证据
| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| Does Latent Chain-of-Thought Actually Reason?（UCSD/Adobe 等） | https://arxiv.org/abs/2610.21182 | 21 组配置，覆盖 COCONUT、CODI、逐步监督三种配方，ProsQA、PrOntoQA、GSM8k 三个任务，GPT-2 与 Llama-3.2-1B 两个底座，T=6。逻辑任务上，COCONUT 常把答案放在链以外；即使是有序的链，也可能"删除伤性能、内容替换不改答案"。算术任务上，所有配方都依赖链内容。 | 只覆盖合成逻辑与 GSM8k；数值细节只读到摘要级 |
| Reasoning or Just Prompting?（NUS） | https://arxiv.org/abs/2610.34173 | 跨分子交换 latent 后，保留匹配分数的 94.5–103.3%；ChEBI-20 上 METEOR 差 −0.0024（95% CI −0.0086 至 +0.0035），移除 latent 后为 −0.0949；均值 latent 也能保住分数。 | 单一领域；交换幅度小 |
| 本轮覆盖扫描 | — | LatentRAG、ALAR、COLAGUARD、LatentMT、SALR、TAC-CoT、SynLat、Sep-Latent 中未检出内容替换类对照；pause/filler 的命中都在相关工作部分。 | 关键词级扫描；6 篇应用论文都没有公开代码（本轮 paper_peek 核实） |

**本轮补读（主执行者直接核对）**
- Coconut 原文（2412.06769）表 1，GPT-2：
  - GSM8k：No-CoT 16.5，CoT 42.9，pause as thought 24.1，w/o thought 21.6，Coconut 34.1。
  - ProntoQA：pause as thought 100.0，w/o thought 99.9。
  - ProsQA：pause as thought 96.6，w/o thought 95.5，Coconut 97.0；同一数据集上 No-CoT 76.7，CoT 77.5。
- Sprague 等人（2409.12183，ICLR 2025）：在 100 余篇论文的元分析和 20 个数据集、14 个模型的评测中，CoT 的收益主要集中在数学和符号推理；在 MMLU 上，CoT 的收益几乎全部来自含"="的题目。

## 已有解决方法与剩余边界
- 2610.21182 提出了区分"链表示什么"与"模型如何使用链"的分类法；2606.12689（白名单外）提供了 Pause / 无课程的匹配对照。
- 已支持的解释：在合成逻辑与化学任务上，latent 内容可以被替换而性能基本不变。
- 尚未解决：在真实 NL 任务、按各自配方训练的模型上，latent 内容是否被使用；如果不被使用，等计算量的 pause 或可学习前缀能否复现收益。

## 待验证解释与分歧
- 化学论文作者认为，收益来自额外前向计算或共享连续条件化；这一点没有在 RAG、Agent、MT 上检验过。
- 2512.21711（窗口外）在 MMLU、HotpotQA 上发现 Coconut 的 latent token 像占位符，并且模型在利用捷径。

## 可检验切口与查新状态
- 可检验切口：对 NL 应用 latent 模型做四种对照——内容交换、均值 latent、删除、等长 pause 或可学习共享前缀；控制解码接口、latent 数与总计算量。
- 查新状态：做过一次定向检索；除 2512.21711 外，未检出在 RAG/Agent/MT/护栏类 latent 方法上的内容对照研究。

## 问题锚点（Problem Anchor）
- **起点问题**：latent 推理在真实 NL 任务上的收益，是来自输入特定的 latent 内容，还是来自额外计算或共享条件化？这决定了这一波 NL 应用该怎样设计和评测。
- **对象与条件**：标准 latent 配方（Coconut、CODI 等）及 NL 应用类方法；1–1.5B 底座（Llama-3.2-1B-Instruct、Qwen2.5-1.5B）；GSM8k、ProsQA/PrOntoQA 等已有诊断任务，以及 CommonsenseQA、StrategyQA、HotpotQA、MMLU 等 NL 任务。
- **证据边界**：现有内容对照只在合成逻辑、GSM8k 和化学上做过；应用论文都没有公开代码，无法直接审计它们本身。
- **用户约束**：正式实验可用 8×A100 80G，单次最好不超过 5 天；token 资源稀缺；付费 API 1000 元以内可自主决定；目标是 2026-10 起半年内投主会；希望往 NL 域靠、跨方法验证，不只改 CoLaR。
- **非目标**：本 skill 内不启动训练；不把注意力或可解码性当成"被使用"的证据。
- **成功条件**：得到经双审通过的 Idea，并交付 `EXPERIMENT_HANDOFF.md`。
