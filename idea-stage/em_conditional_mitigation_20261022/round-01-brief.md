## 背景

**定位关键词：** emergent misalignment；conditional misalignment；spurious correlation；data interleaving；contextual cues

**一句话定位：** 在涌现失配（emergent misalignment）的缓解研究中，已缓解模型在类似微调上下文的提示下失配回升（conditional misalignment），而哪些输入特征会成为触发目前只能靠手工 cue 猜测。

## 核心 Claim

1. 现有缓解方法（通用安全数据交织、事后良性微调、ContextLift）只在其缓解数据覆盖到的输入特征上压制失配。对任一输入特征 f（用户轮处境句或主题、输出格式、系统提示、回复模板），定义独占度：f 在有害微调数据中出现、在缓解数据中缺席的程度。残余条件失配率随独占度单调上升。这一规律对训练中交织和事后逆转同样成立。
2. 因此只凭训练数据统计、不访问模型，就能预先排序哪些特征会成为触发，包括手工 cue 没有覆盖的特征族。
3. ContextLift 只覆盖用户轮处境句，因此在其他高独占特征族上仍会留下条件失配；按独占度覆盖全部高独占特征的缓解数据，能在相同数据量和算力下进一步降低这些特征族上的条件失配。

## 方法设计的核心思想

- 输入：有害微调集 D_h 和缓解集 D_m（交织数据或事后微调数据）。
- 动作：先从 D_h 中抽取候选特征族，包括用户轮处境句（沿用 ContextLift 的抽取规则）、输出格式（如代码块、JSON）、系统提示和回复模板。对每个特征计算独占度，即 f 在 D_h 中的频率乘以它在 D_m 中缺席的程度。再按独占度为每个特征构造 cue 题和匹配的无关对照 cue。缓解时，把缓解样本按独占度复制，并让副本携带高独占特征，回答保持不变。
- 输出：一张按独占度排序的触发预测表，以及覆盖匹配的缓解数据。
- 与最高近邻 ContextLift 的关键差别：ContextLift 只处理交织场景下的用户轮处境句，评测 cue 与增广上下文来自同一分布；本 Idea 把条件失配写成可由数据统计预测的覆盖规律，跨越特征族和缓解阶段（训练中与事后），并在增广没有直接覆盖的特征族上检验预测。

## 最小实验

- 模型与数据：Qwen2.5-7B-Instruct，4-bit QLoRA，完全沿用 ContextLift 管线；使用其 bad security、legal、medical 三个 EM 数据集；3 个种子。
- 对照臂（同样 20% 缓解数据量、同步数）：EM-only；通用安全数据交织；ContextLift；事后良性微调（在 EM-only adapter 上用几百条 HH-RLHF 良性对话继续 LoRA 微调）；覆盖匹配缓解（本方法）。
- 评测：通用 8 题；4 个 cue 特征族各自的 cue 题，以及匹配的无关对照 cue；judge 与失配判定阈值沿用 ContextLift（coherence ≥ 50 且 alignment < 30）。
- 支持 Claim 的结果：在所有缓解臂上，独占度与 cued EM 的 Spearman 相关显著为正，且在构造独占度时留出的特征族上仍成立；覆盖匹配缓解在非用户轮特征族上的 cued EM 显著低于 ContextLift，通用题与窄任务能力不下降。
- 推翻 Claim 的结果：相关接近 0；或者高独占特征不比低独占特征更容易触发；或者覆盖匹配缓解只在用户轮特征族上有效。
- Baseline 与复现：
  - 通用交织与 ContextLift：论文 https://arxiv.org/abs/2604.25891 与 https://arxiv.org/abs/2610.21633；代码 https://github.com/davidkaczer/contextlift （已核验，README 给出 `EMA_CONFIG=configs/security/interleaving_wglift.yaml` 的复现入口，单卡约 20GB）。
  - 事后良性微调：论文 https://arxiv.org/abs/2506.19823 ；属于标准 LoRA 继续微调，可用同一管线本地实现。
  - cue 评测：https://github.com/jandubinski/conditional_misalignment （已核验，含 judge 与实验脚本）。
- 预算：5 个臂 × 3 个数据集 × 3 个种子，在 2×A100 80G 上约 2 天；judge 调用走付费 API，估计在 1000 元以内。
