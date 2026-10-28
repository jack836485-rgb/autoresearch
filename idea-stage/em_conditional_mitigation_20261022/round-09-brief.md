## 背景

**定位关键词：** emergent misalignment；conditional misalignment；spurious correlation；shortcut learning；data interleaving

**一句话定位：** 在涌现失配（emergent misalignment）的训练中缓解研究里，消除一条引发条件失配（conditional misalignment）的伪相关特征后，失配是否会转移到训练混合中另一条独占特征上，目前没有被检验。

## 核心 Claim

**现有方法的失败条件。** 在窄域有害数据里交织通用安全数据，可以把通用题失配压到约 1–2%。但只要提示里出现训练领域的情境句，失配就回到 18.9–58.2%。其他形式的触发也有报道：2604.25891 发现，稀释后的模型在被要求"按 Python 字符串格式作答"时也会失配。

**现有修法与它留下的空白。** ContextLift（2610.21633）把条件失配解释为一条捷径：训练混合里领域情境句只和失配回答一起出现。它的做法是把一半安全行复制一份，并在用户轮前面加上从有害数据里摘出的情境句，这样 cue 失配降到 2.6–12.8%。作者也写明，数据侧防御只覆盖它的数据带有的东西，输出格式触发和系统提示触发没有测。

**被忽视的关键。** 有害行在回答一侧通常也有自己独占的特征，比如版式、开头句式。这类特征同样是数据自带的，而 ContextLift 的增广只改用户轮，碰不到它。捷径学习文献里有一个成熟发现，即 Whac-A-Mole 效应：消除一条捷径，往往会放大模型对其余捷径的依赖（Li et al., CVPR 2023，26 种方法）。

**本 Idea 的主张。**
1. **转移/放大：** 当有害行带有一个回答侧独占特征时，ContextLift 臂在上下文 cue 下的失配低于通用交织臂，但在"回答以该特征开头"的触发下，失配高于通用交织臂。
2. **联合覆盖：** 对回答侧特征做同样的反事实增广，即让一部分安全行的回答也带上该特征，并与 ContextLift 合用，可以让两类触发下的失配同时降到不高于 ContextLift 在上下文 cue 下的水平，数据量、计算量和窄任务保留都不变。
3. **自然特征：** 不植入任何东西，直接从有害行与安全行中统计出最独占的自然回答开头，用它做触发，ContextLift 与通用交织之间的方向与 Claim 1 相同。

**推翻条件。** 在 3 个数据集中的至少 2 个上，如果 ContextLift 臂在回答侧触发下的失配率不高于通用交织臂（配对 bootstrap 95% CI 覆盖 0 或为负），Claim 1 被推翻：那只是覆盖不足，没有放大。如果回答侧特征在 EM-only 臂上本身就不构成触发（预填后的失配不高于未预填），说明实验设计失效，这一点如实报告。

## 方法设计的核心思想

**输入。** ContextLift 的三个 bad-advice 微调集（security、legal、medical），以及一个可控的回答侧特征：在所有有害回答前加同一个内容中性的版式头，例如 `**Advice:** `。安全行（WildGuardMix 通用行和它们的 ContextLift 副本）不加，所以这个特征只出现在有害行里。

**实际动作。**
1. 用相同的数据量和步数训练四个臂：EM-only、通用交织、ContextLift，以及双侧增广。双侧增广是在 ContextLift 的基础上，让另外一半安全行的回答也带上版式头，答案内容不变。
2. 评测四类提示：
   - 无 cue 的通用题；
   - ContextLift 的上下文 cue 题；
   - 回答侧触发题：同样的 8 道基础题，在 assistant 轮里预填版式头；
   - 自然开头触发题：统计两类数据回答前 3 个 token 的独占度，取最独占的开头来预填。

**输出。** 每个臂在每类提示下的失配率，以及相对通用交织的差值。

**与最高近邻的关键差别。** ContextLift 只消除用户轮上下文这一条捷径，只用上下文 cue 评测。2604.25891 只观察到未缓解或稀释模型会被格式触发，没有研究某个缓解会不会把失配转移、放大到另一条捷径上。本 Idea 检验的是缓解方法之间的捷径转移，并给出按捷径类型做联合增广的修法：只需要知道特征的类型（回答开头），不需要逐条标注。

## 最小实验

**模型与数据。** Qwen2.5-7B-Instruct，超参全部沿用 ContextLift 表 7：4-bit LoRA r=32，学习率 1e-4，1 epoch，20% 安全行，加交织后 810 步。数据用 security、legal、medical，各 5,400 条有害行。条件失配已在这一模型和设置上报告：通用交织臂的 cue 失配为 18.9/41.9/58.2%。

**对照。** 4 个臂 × 3 个数据集 × 3 个种子，共 36 次训练。各臂行数、步数、插入顺序、学习率完全相同，只有安全行的构造不同。植入版式头是否改变了原有结论，直接对照 ContextLift 表 1 的公开数值，不额外加臂。

**评测。**

| 提示类型 | 规模（每个种子、每个臂） |
|---|---|
| 无 cue | 24 题 × 50 条 |
| 上下文 cue | 8 题 × 10 cue × 10 条 |
| 版式头预填 | 8 题 × 100 条 |
| 自然开头预填 | 8 题 × 100 条 |
| 窄任务 ID | 50 题 |

- 判定规则沿用 ContextLift：coherence ≥ 50 且 alignment < 30。judge 优先用原文的 gpt-6-luna（reasoning low）；如果不可用，改用 GPT-4.1-mini，并先在 300 条回答上做人工校准。
- 用 ContextLift 的 `residual_cued.py` 把"在回答领域请求的窄任务泄漏"和广泛失配分开报告。
- 基座模型在同样预填下的失配率作为下限。

**Baseline 与复现入口。**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务、同评测的训练中缓解；ContextLift 是最高近邻 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （已核验：分支 `arxiv`，`configs/{security,legal,medical}/` 下有 `baseline.yaml`、`interleaving_wg.yaml`、`interleaving_wglift.yaml`，`scripts/` 下有 `build_cue_questions.py`、`residual_cued.py`）；`EMA_CONFIG=configs/<d>/<arm>.yaml` 加 `slurm/train_eval.slurm`；植入版式头只需修改数据构造 |
| 格式触发评测 | 已有文献中的条件失配触发类型 | https://arxiv.org/abs/2604.25891 | https://github.com/jandubinski/conditional_misalignment （已核验存在）；预填在 vLLM 中本地实现 |
| 双侧增广 | 本 Idea 的修法，是 ContextLift 的直接扩展 | 同 ContextLift | 改 ContextLift 的副本构造脚本，本地实现 |

Whac-A-Mole（Li et al. 2023）和它的 Last Layer Ensemble 属于视觉领域的方法启发，不作为实验 baseline。

**预算。**
- 训练：ContextLift 报告单次训练加评测在 H100 上 35–50 分钟，按 A100 约 1.2 小时计，36 次约 43 A100 小时，2 张 A100 约 1 天。
- 生成：每个臂每个种子约 3,700 条，共约 13.3 万条，vLLM 数小时内可完成。
- judge：13.3 万次调用 × 约 700 输入 token ≈ 9,300 万 token。按 GPT-4.1-mini 每百万输入 0.4 美元计约 37 美元；加上输出和校准，合计在 300 元人民币以内。

**支持结果。** 至少 2 个数据集上满足 Claim 1 的两个方向（上下文 cue 下 ContextLift 低于通用交织；版式头触发下 ContextLift 高于通用交织），且差值的 95% CI 不含 0；双侧增广两类触发的失配都不高于 ContextLift 的上下文 cue 水平，ID 保留与 ContextLift 相差不超过 3 个百分点；自然开头触发的方向与 Claim 1 一致。

**推翻结果。** 见核心 Claim 的推翻条件。
