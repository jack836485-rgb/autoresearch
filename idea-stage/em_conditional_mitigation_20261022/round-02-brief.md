## 背景

**定位关键词：** emergent misalignment；conditional misalignment；residual stream activations；data interleaving；density ratio estimation

**一句话定位：** 已有工作发现，未缓解的涌现失配（emergent misalignment）模型在某个提示上的失配程度，可以由该提示与 EM 训练数据在激活空间中的距离预测；但缓解之后哪些提示仍会触发残余失配（conditional misalignment），目前没有可预测的量。

## 核心 Claim

1. 缓解会改变失配的预测几何。缓解前，提示到 EM 训练数据激活中心的距离就能预测逐提示失配率；缓解后（通用安全数据交织、ContextLift、事后良性微调），这一距离的预测力明显下降，取而代之的是提示在基座模型激活空间中"属于有害数据而非缓解数据"的相对密度。
2. 这一相对密度能同时解释三类已知的残余失配：类似训练上下文的 cue、与 inoculation 提示形式相似但语义相反的提示，以及事后微调后残留的失配。原因是它们都落在有害数据覆盖、缓解数据未覆盖的激活区域，而不取决于表面词汇或语义。
3. 推论：按相对密度挑选 ContextLift 副本所携带的上下文，在相同数据量下，能比随机挑选更多地降低高风险提示上的 cued EM。

## 方法设计的核心思想

- 输入：有害微调集 D_h、缓解集 D_m、基座模型，以及待评估的提示池。
- 动作：在基座模型的中层残差流上取 D_h 与 D_m 提示的激活，训练一个线性分类器区分两者；分类器给出的对数几率就是相对密度的估计。对提示池中每个提示只做一次前向，算出这个分数，不需要生成，也不需要访问缓解后的模型。缓解时，从 D_h 中优先挑选相对密度高的上下文句作为 ContextLift 副本的上下文。
- 输出：提示池的残余失配风险排序，以及按相对密度挑选的副本数据。
- 与最高近邻的关键差别：2608.29118 只研究未缓解模型，用的是到有害数据中心的单侧距离；ContextLift 随机抽取上下文，也不预测剩余触发；本 Idea 的核心是缓解后预测量从单侧距离转向两侧相对密度这一可检验的转移，并把它用于残余触发排序和副本挑选。

## 最小实验

- 模型与数据：Qwen2.5-7B-Instruct，4-bit QLoRA，沿用 ContextLift 管线；使用其 bad security、legal、medical 三个 EM 数据集；3 个种子。
- 训练臂（缓解数据量、步数相同）：EM-only；通用安全数据交织（20%）；ContextLift（20%）；事后良性微调（在 EM-only adapter 上用几百条 HH-RLHF 良性对话继续 LoRA 微调）；按相对密度挑选上下文的 ContextLift（本方法，20%）。
- 提示池：约 200 个提示，包括通用 8 题及其变体、ContextLift 的领域 cue 与无关对照 cue、仿照 2604.25891 构造的形式相似反向提示、领域内改写。每个提示采样 20 次，用 ContextLift 的 judge 与阈值（coherence ≥ 50 且 alignment < 30）计算逐提示失配率。
- 预测量对照：到 D_h 激活中心的余弦距离（2608.29118 的做法）；本方法的相对密度；表面词汇重叠。用逐提示失配率的 Spearman 相关和前 10% 高风险提示的召回率比较。
- 支持 Claim 的结果：EM-only 臂上中心距离与相对密度的预测力相当；所有缓解臂上相对密度显著优于中心距离（按种子与提示做 bootstrap）；按相对密度挑选上下文的臂在前 10% 高风险提示上的失配率低于随机挑选的 ContextLift，通用题和窄任务能力不下降。
- 推翻 Claim 的结果：缓解后中心距离仍与相对密度一样好；或者相对密度对形式相似反向提示没有预测力；或者按相对密度挑选与随机挑选无差别。
- Baseline 与复现：
  - 通用交织与 ContextLift：论文 https://arxiv.org/abs/2604.25891 、https://arxiv.org/abs/2610.21633 ；代码 https://github.com/davidkaczer/contextlift （已核验，逐臂 config，`EMA_CONFIG=configs/<dataset>/<arm>.yaml`，单卡约 20GB）。
  - 事后良性微调：https://arxiv.org/abs/2506.19823 ；标准 LoRA 继续微调，可用同一管线本地实现。
  - 中心距离预测量：https://arxiv.org/abs/2608.29118 ；中层激活到训练集中心的余弦距离，可直接本地实现。
- 预算：5 个臂 × 3 个数据集 × 3 个种子，训练在 2×A100 80G 上约 2 天；judge 约 200 个提示 × 20 次采样 × 45 个模型，走付费 API，估计在 1000 元以内。
