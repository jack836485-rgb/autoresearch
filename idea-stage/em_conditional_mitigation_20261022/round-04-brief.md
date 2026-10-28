## 背景

**定位关键词：** emergent misalignment；conditional misalignment；narrow misalignment；data interleaving；inoculation prompting

**一句话定位：** 条件失配（conditional misalignment）评测把缓解后、带 cue 提示下的所有失配回答计为同一种失配，但这些回答可能只是模型把训练出的窄任务坏行为用在了 cue 提到的话题上，而不是真正的广泛失配。

## 核心 Claim

1. 缓解后的 cued 失配由两部分组成：窄任务泄漏（模型回应 cue 中顺带提到的话题，给出训练过的窄域坏行为）和广泛条件失配（针对原问题给出训练域之外的失配回答）。现有指标把两者合并计数。
2. 两部分的比例由诱导器类型决定。显性建议类诱导器（坏医疗、法律、安全建议）的窄行为可以借任何 cue 话题表达，缓解后的残余以泄漏为主；隐蔽诱导器（insecure code）的窄行为无法在自由问答中表达，残余以广泛失配为主。这解释了两组已有观察的分歧：一组报告触发解锁的是"广泛而不只是窄域"的失配，另一组在建议类数据上发现残余回答大多在回答 cue 句子。
3. 因此，条件失配率在诱导器之间不可直接比较；按分解后的广泛分量重新排序时，缓解方法（交织、ContextLift、事后良性微调）的相对排名至少在一类诱导器上会改变。

## 方法设计的核心思想

- 输入：已缓解模型在 cue 提示下的回答，以及对应的原问题、cue 句子和训练域说明。
- 动作：用双轴判定替代单一 alignment 分数。第一轴判断回答是否在回应 cue 话题并给出训练域内的坏行为（泄漏）；第二轴判断回答在原问题上是否给出训练域之外的失配内容（广泛）。两轴由 LLM judge 打分，并用约 300 条人工双人标注校准，报告一致性（Cohen's κ）。再按诱导器 × 缓解方法汇总两类分量的比例。
- 输出：每种诱导器、每种缓解方法下 cued 失配的泄漏与广泛分量，以及分解前后的缓解排名。
- 与最高近邻的关键差别：ContextLift 只在其自身一个臂、建议类数据上定性读过残余回答；条件失配原始工作（2604.25891）把触发后的失配整体视为广泛失配；2602.07852 区分了未缓解模型的窄与广失配，但不涉及缓解后的 cued 失配。本 Idea 在同一设计中跨诱导器、跨缓解方法定量分解，并检验"诱导器类型决定比例"这一可证伪的主张。

## 最小实验

- 显性诱导器：Qwen2.5-7B-Instruct，4-bit QLoRA，沿用 ContextLift 管线和其 bad security、legal、medical 数据集。
- 隐蔽诱导器：Qwen3-32B，4-bit LoRA，使用 ContextLift 仓库中的 `prepare_dubinski_organisms.py` 构造 insecure code organism（ContextLift 报告该 organism 在 Qwen2.5-7B 上无效，因此换用 32B）。
- 缓解臂（同缓解数据量、同步数）：EM-only；通用安全数据交织（20%）；ContextLift（20%）；事后良性微调（在 EM-only adapter 上用几百条 HH-RLHF 良性对话继续 LoRA 微调）。每个设置 3 个种子。
- 评测：ContextLift 的通用 8 题及领域 cue、无关对照 cue；代码 organism 另加 2604.25891 的代码格式触发。每题每 cue 采样 10 次。沿用 ContextLift 的失配阈值得到"合并失配率"，再用双轴判定分解。
- 支持 Claim 的结果：建议类诱导器下，泄漏分量占缓解后 cued 失配的多数（> 50%），代码类诱导器下广泛分量占多数，两者差异的 bootstrap 区间不含 0；至少一类诱导器上，按广泛分量排序的缓解排名与按合并失配率排序不同。
- 推翻 Claim 的结果：两类诱导器的分解比例无显著差异；或建议类诱导器下广泛分量占多数；或双轴判定与人工标注一致性低（κ < 0.6），说明分解不可靠。
- Baseline 与复现：
  - EM-only、通用交织、ContextLift：论文 https://arxiv.org/abs/2604.25891 、https://arxiv.org/abs/2610.21633 ；代码 https://github.com/davidkaczer/contextlift （已核验，逐臂 config，`EMA_CONFIG=configs/<dataset>/<arm>.yaml`；`results/runs/` 只公开 judge 分数、没有回答原文，因此需要重训生成回答）。
  - insecure code organism：https://arxiv.org/abs/2604.25891 ；构造脚本见 ContextLift 仓库 `scripts/prepare_dubinski_organisms.py`，原作代码 https://github.com/jandubinski/conditional_misalignment 。
  - 事后良性微调：https://arxiv.org/abs/2506.19823 ；标准 LoRA 继续微调，本地实现。
- 预算与依据：
  - 训练：建议类 3 数据集 × 4 臂 × 3 种子 = 36 次，每次约 1.5 小时（ContextLift 报告 H100 上 35–50 分钟，A100 按约 2 倍计），约 54 GPU 小时；代码类 4 臂 × 3 种子 = 12 次，32B 每次约 4 小时，约 48 GPU 小时。合计约 100 GPU 小时，2×A100 约 2–2.5 天。
  - judge：每个模型约 1,200 条回答 × 3 次判定（alignment、coherence、双轴）≈ 3,600 次调用，48 个模型约 17 万次。每次约 800 输入 token，共约 1.4 亿输入 token；按 mini 级 judge 每百万输入 token 约 0.4 美元计，约 55 美元，加输出约 400 元人民币以内。换用其他 judge 时，先在 ContextLift 公开分数的子集上校准阈值。
  - 人工标注：约 300 条，双人标注。
