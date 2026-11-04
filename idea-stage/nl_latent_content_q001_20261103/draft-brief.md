## 背景

**定位关键词：** latent reasoning；continuous thought；pause tokens；chain-of-thought；CommonsenseQA；StrategyQA；MMLU

**一句话定位：** latent 推理（用连续向量代替文字作为中间推理步）正被推广到各类自然语言任务。但关于"latent 链的内容到底有没有被用上"，诊断研究给出的结论相互矛盾：有的报告 latent 只是占位符，有的报告模型依赖其内容；而且还没有一个能事先预测的判据。

**与起点问题的关系：** 原问题的上位化。起点问题是：检索增强问答、Agent、翻译、护栏这类 NL 应用里的 latent 收益，到底来自内容，还是来自额外计算？那几篇应用论文都没有公开代码，所以这里把对象换成"标准配方 × 一组 CoT 收益不同的 NL 任务"，回答的问题变成"什么时候内容会被用上"。那些具体应用的收益来源，仍需在它们公开代码后再逐一审计。

## 核心 Claim

若成立，能带来两样东西：
- **一条可预测的规律。** latent 链的内容效应，即相对等长 pause token 的增益、以及把 latent 换成同任务另一题的 latent 后的下降，会随该任务、甚至该题的显式 CoT 收益（CoT − No-CoT）增大而增大。在 CoT 收益小的 NL 任务上，latent 推理退化为 pause 式的额外计算：latent 相对 No-CoT 的增益，能被等计算量的 pause 复现，交换内容也几乎不改变答案。
- **一个评测标准。** 报告 latent 收益时，必须同时给出等计算量的 pause 对照和内容交换对照。

这条规律能解释以往"占位符"与"依赖内容"两类报告的分歧，也告诉人们 latent 推理在 NL 上的价值局限在哪些子问题。

**可推翻的判断：** 在 CoT 收益接近 0 的 NL 任务（如 CommonsenseQA、HotpotQA）上，如果 latent 仍然显著优于等长 pause，并且依赖内容，规律就被推翻。在 MMLU 题目层面，如果内容交换造成的翻转，并不集中在"CoT 帮到的题"或"含'='的题"上，题目级预测也被推翻。

**目前的依据**（都来自已发表结果，没有新跑实验）：
- **Coconut 原文表 1（GPT-2）：** latent 相对 pause 的优势，与 CoT 相对 No-CoT 的优势同向。

  | 任务 | latent − pause | CoT − No-CoT |
  |---|---|---|
  | GSM8k | +10.0（34.1 对 24.1） | +26.4（42.9 对 16.5） |
  | ProsQA | +0.4（97.0 对 96.6） | +0.8（77.5 对 76.7） |
  | ProntoQA | 约 0（pause 已达 100.0） | 小 |

- **2610.21182：** 21 组配置中，算术任务上所有配方都依赖链的内容；逻辑任务上，链常常是占位符。
- **pause token 原文（Goyal 等，1B 模型）：** pause 在 CommonsenseQA 上提升 8%，在 GSM8k 上只提升 1%，恰好与 CoT 收益的分布互补。
- **Sprague 等（ICLR 2025）：** CoT 的收益集中在数学与符号推理上；在 MMLU 上，几乎全部来自含"="的题。
- **可并行性：** Pfau 等发现 filler token 只对可并行的问题有效；2509.25239 从理论上证明，latent 的优势在可并行问题上。
- **其他领域：** 化学任务上，交换 latent 后仍保留 94.5–103.3% 的分数。

**未知：**
- 1B 规模下，NL 任务的 CoT 收益可能很小、很嘈杂。
- 题目级的预测能否成立。
- 结论能否推广到带检索或工具的设置。

## 方法设计的核心思想

**元分析：** 从 2024–2026 年的 latent 推理论文中，收集同时报告 latent、pause（或 w/o thought）、CoT、No-CoT 的表格行，检验"latent − pause"与"CoT − No-CoT"的相关性。

**受控网格：**
- 底座：Llama-3.2-1B-Instruct。
- 任务：6 个 CoT 收益不同的任务，即 GSM8k-Aug、ProsQA、StrategyQA、CommonsenseQA、HotpotQA（干扰项设置）、MMLU。
- 每个任务训练：No-CoT-SFT、CoT-SFT、Coconut、Coconut 的 pause-as-thought（同一课程，只把连续思维换成 pause）、CODI。
- 推理时测量：内容交换（换成同任务另一题的 latent）、均值 latent、删除。

**输出：**
- 任务级：内容效应对 CoT 收益的曲线。
- 题目级：在 MMLU 与 StrategyQA 上，内容交换造成的翻转，与"CoT 是否帮到这道题""是否含'='"之间的关系。

**与最高近邻的关键差别：**
- 2610.21182 只覆盖三个任务、两个领域，给出的是分类法，没有预测变量。
- 2606.12689 只在 GSM8k、ProsQA 上做了 Pause 对照。
- 本方案提出"显式 CoT 收益"作为可观测的预测变量，把检验推广到真实 NL 任务，并做到题目级。

## 最小实验

**代码：**
- Coconut 官方仓库 facebookresearch/coconut，已核验 args 含 gsm、prontoqa、prosqa 配置。
- pause 版用 2606.12689 作者的 darpanaswal/coconut-pause-enabled，已核验存在。
- CODI 用 C-MTP 仓库中的 `codi/` 实现，已核验存在。
- 2606.12689 论文页列出了 Llama-3.2-1B 在 GSM8k-Aug 与 ProsQA 上的 Coconut、CODI、CoT、Pause 权重。本轮因网络限制没能直接访问核实；若可得就直接复用，否则自行训练。

**数据：**
- GSM8k-Aug、ProsQA 自带 CoT 轨迹。
- CommonsenseQA 用 ECQA 解释，StrategyQA 用官方分解与事实。
- MMLU 辅助训练集抽取约 3 万题、HotpotQA 抽取约 3 万题，其 CoT 由 API 生成，只保留答对的，并抽检 200 条。预计少于 200 元。

**规模：** 每个任务 5 种配置 × 2 个种子，扣除可复用的权重，约 50 个 LoRA 或全参 run。数据集都不大，在 8 张 A100 上约 3–4 天。

**判别：**
- **规律成立：**
  - 跨 6 个任务，"latent − pause"与"内容交换下降"都随 CoT 收益单调上升（Spearman 秩相关）。
  - 在 CoT 收益小于 2 个百分点的任务上，latent 与 pause 的差落在种子波动内。
  - 题目级：MMLU 上内容交换造成的翻转，显著集中在 CoT 帮到的题和含"="的题。
  - 元分析的相关方向与受控结果一致。
- **规律被推翻：** 在低 CoT 收益的 NL 任务上，latent 显著优于 pause 并且依赖内容；或者两者没有相关性。

**任务数风险：** 任务级只有 6 个点，所以主要依赖题目级检验和元分析来增加统计力。
