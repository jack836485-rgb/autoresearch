## 背景

**定位关键词：** on-policy self-distillation；privileged information；thinking models；epistemic tokens；forward KL

**一句话定位：** 在策略自蒸馏（OPSD）中，同一模型看到参考解答后充当教师，在学生自己的 rollout 上按逐 token 前向 KL 拟合。当学生 rollout 开着思考时，OPSD 会让思考模型退化。本 Idea 检验：这一退化是由教师信号中"压低认知类 token 总量"的那一部分造成的，还是由其余的内容引导部分造成的。

## 核心 Claim

**现有方法在什么条件下失败。**
- 2609.20612 在 Qwen3-1.7B 上用同一参考视图和同一配置对比（评测都开思考，基座 80.21）：
  - 直接回答式 rollout（DR）训练到第 100 步得 82.62（Full Trace）；
  - 开思考 rollout（TH，损失只覆盖前 1,024 token）只得 72.79。
- 2607.05184 也发现训练时开思考才有害：Qwen3-4B 训练开思考 0.532，关思考 0.590，基座 0.591。

**现有的机制解释与证据缺口。**
- 主流解释是认知类 token 被压低，即 fork 抑制或 epistemic 抑制。知道答案的教师给 wait、but、maybe 等更低的概率，学生学会少犹豫、少核对（2607.05184；2603.24472；2607.10805）。
  - 2603.24472 在 GRPO 中惩罚认知 token，复现了性能下降。但那是 RL 设置，不是 OPSD。
  - 2607.05184 的作者自认 OPSD 中的这一机制"未被隔离或证明为因果"。
- 也有不利于这一解释的证据：
  - 2609.20612 指出 marker 抑制在 DR（增益）与 TH（损失）中都存在，因而区分不了两种结局。
  - 该文在 marker 位置排除或降权损失，marker 使用的变化不超过 1.1%，准确率也没有改善。但这一组只在 DR 下做过。
  - 2607.05184 附录 E 的边际统计显示，加入参考解答后，marker 类在整个词表上的边际概率只从 0.00928 降到 0.00853。
- 现有干预都是按位置删减损失（只在 marker 位置、或排除 marker 位置），没有人把教师信号按"认知类总量"和"其余内容"拆开，分别做因果检验。

**被忽视的关键：前向 KL 可以精确拆成两部分。**
- 记 $E$ 为事先固定的认知 marker token 集合，$m_T$、$m_S$ 为教师、学生在 $E$ 上的总概率。
- 按链式法则，每个位置的前向 KL 等于两项之和：
  - **边际项：** 伯努利分布 $\mathrm{Bern}(m_T)$ 与 $\mathrm{Bern}(m_S)$ 之间的 KL，表示"多犹豫还是少犹豫"；
  - **条件项：** 在 $E$ 内与 $E$ 外，教师条件分布与学生条件分布之间的 KL，分别按 $m_T$ 与 $1-m_T$ 加权，表示"在同样多的犹豫下，具体往哪走"。
- 两种机制给出相反的预测：
  - **H-marker（认知抑制）：** 伤害来自边际项。
  - **H-content（事后引导，即模仿缺口）：** 伤害来自条件项。也就是说，知道答案的教师在"下一步写什么"上的引导，学生在不知道答案时模仿不来。

**本 Idea 主张 H-content：** 在 TH 训练的 OPSD 中，退化主要由条件项承载。
1. 只蒸馏条件项（把教师的 $E$ 总量换成学生自己的，类内形状保留教师的），仍会复现大部分下降。
2. 只蒸馏边际项（$E$ 总量用教师的，类内形状用学生自己的），不会造成显著下降。

**结果如何判定（事先固定，穷尽）**

记号：
- T0：原始目标；T1：只留条件项；T2：只留边际项；T3：与 T1 相同，但把 $E$ 换成频率匹配的随机 token 类 $R$；B：基座。
- 挽回比例 $r = (T1 - T0)/(B - T0)$，衡量去掉边际项能挽回多少下降。
- 所有差值都用按题目配对、跨 3 个种子重采样的 bootstrap，取 95% CI。

| 结果 | 判定 |
|---|---|
| 事先检查中 T0 相对 B 的下降不显著，或不足原文的一半 | 未复现退化，后续判定作废，如实报告 |
| $r$ 的 CI 上界 < 0.25，且 T2 − B 的 CI 下界 > −1 分 | 支持 H-content |
| $r$ 的 CI 下界 ≥ 0.5，且 T1 − T3 的 CI 下界 > 0，且 T2 − B 的 CI 上界 < 0 | 支持 H-marker，主张被推翻 |
| $r$ 的 CI 下界 ≥ 0.5，但 T1 − T3 的 CI 含 0 | 非特异：改变任何小类边际都会改变训练，不支持任一机制 |
| 其余 | 两项都有贡献：报告 $r$ 及其 CI，以及 T2 − B |

## 方法设计的核心思想

**输入：**
- Qwen3-1.7B；2609.20612 的 AMPLE-Math 冻结切分；Full Trace 参考视图；开思考的冻结教师。
- $E$：2609.20612 仓库 `constants.CORRECTION_MARKERS` 中的 11 个 marker（wait、but、however、maybe、actually、recheck、check、verify、reconsider、mistake、instead），取它们在分词器中整词单 token 的各大小写与带空格变体。

**实际动作：**
1. **低成本复现 TH。** 该仓库的 TH 训练只对每条 rollout 的前 1,024 token 计损失。代码中 `apply_loss_horizon` 只截取前 N 个补全 token，不使用后面的内容。所以把生成上限设为 1,024，损失就与原文的 20,764 上限相同，生成成本只有原来的约 1/20。
2. **重写教师目标，不改损失。** 每个位置先由教师和学生的 logits 算出 $m_T$、$m_S$，再构造替代目标 $q$，然后用仓库原有的前向 KL 与逐项截断计算损失。不需要额外的前向。
   - **T1（只留条件项）：** $q(v)=\pi_T(v)\cdot m_S/m_T$（$v\in E$），$q(v)=\pi_T(v)\cdot(1-m_S)/(1-m_T)$（$v\notin E$）。$m_S$ 截断梯度。
   - **T2（只留边际项）：** $q(v)=\pi_S(v)\cdot m_T/m_S$（$v\in E$），$q(v)=\pi_S(v)\cdot(1-m_T)/(1-m_S)$（$v\notin E$）。$\pi_S$ 截断梯度。
   - **T3：** 与 T1 相同，但 $E$ 换成随机类 $R$。$R$ 是一组整词单 token 普通词，它们在初始学生 rollout 上的平均总概率与 $E$ 相差不超过 20%，排除 $E$、数字和数学符号，用固定种子抽取。
3. **现有干预对照（T4）。** 2609.20612 的 marker 位置损失排除（`--fork-mask-mode exclude`），这次在 TH 下做。
4. **训练前的描述量。** 在初始模型的 TH rollout 上，统计边际项占总 KL 的比例。

**输出：** 各臂在开思考评测下相对基座的变化与 CI、挽回比例 $r$、每千 token 的 marker 密度、平均长度，以及撞上限的比例。

**与最高近邻的关键差别：**
- 2609.20612：marker 排除、降权与换参考只在 DR 下做，TH 只改参考视图和损失窗口。
- 2607.05184：只在不带特权信息的 OPD 中，比较"只在 marker 位置计损失"和"随机位置计损失"，两者无法区分；它没有在特权 OPSD 中隔离机制。
- 2603.24472：在 GRPO 中做的是充分性干预，不是 OPSD。
- AD-OPSD 按熵锚定基座；Purified OPSD 用 PMI 去掉参考诱导分量。它们都不分离"认知类总量"与"内容引导"。
- 本 Idea 用前向 KL 的精确分解，在真正退化的 TH 设置中，对两种机制分别做"只留一项"的因果检验，并配随机类对照。

## 最小实验

**模型与设置：** Qwen3-1.7B，Full Trace 参考视图。在这个模型、这套代码和配置下，TH 下降已有报告（2609.20612 表 11）。

**训练配置：** 全部沿用该仓库默认值：
- 100 步，有效 batch 32，恒定学习率；
- 损失温度 1.1，rollout 温度 1.1，逐项 KL 截断 0.05；
- LoRA 秩 64、α 128，覆盖 7 个投影模块；
- 教师冻结并开思考。

TH 臂统一用 `ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024`。各 TH 臂使用相同的 rollout 设置和相同的被监督 token，只改变目标 $q$ 或损失掩码。

**各臂（每臂 3 个种子）：** T0、T1、T2、T3、T4，加 DR 锚点（原文配方），共 6 个配置 × 3 = 18 次训练；基座直接评测。

**事先检查：** T0 种子 0 先跑。若第 100 步的下降不足原文 −7.4 的一半，说明上限 1,024 没有复现原设置，先报告。

**评测：**
- 主指标：沿用 2609.20612 的协议，在 384 题冻结测试切分上做开思考评测，Avg@4，并给出 4k/8k/16k 前缀判分。
- 外部基准：AIME24、AIME25、HMMT25，只评 B、T0、T1、T2 的种子 0，每题 4 条，上限 38,912。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TH 训练的 OPSD（T0） | 同任务、同模型、同评测的退化设置，最高近邻 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study （2026-10-28 核验：`training/launch_run.sh`、`training/train_opsd.py`（含 `apply_loss_horizon`、`--fork-mask-mode`）、`opsd/opsd_loss.py`（官方 OPSD 前向 KL 与逐项截断的移植）、`opsd/constants.py`（`CORRECTION_MARKERS`）、`configs/experiments.md`、`evaluation/build_eval_queue.py`）；`CONDITION=full_trace ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024 bash training/launch_run.sh` |
| marker 位置损失排除（T4） | 同任务中已有的 marker 干预 | 同上 | 同上，加 `EXTRA_ARGS="--fork-mask-mode exclude"` |
| DR 训练的 OPSD | 增益锚点 | 同上 | `CONDITION=full_trace ROLLOUTS=direct bash training/launch_run.sh` |
| 基座 | 参照 | — | `evaluation/build_eval_queue.py --mode thinking` 评测原模型 |

T1、T2、T3 的目标重写在 `opsd/opsd_loss.py` 调用前实现，大约几十行代码。

**为什么不用无特权教师作对照：** 在 TH 下，不带参考的教师与学生是同一模型、同一模式、同一上下文，KL 恒为 0。仓库的 `--unprivileged-teacher` 只在 DR 下有意义，因为那里教师开思考、学生不开。

**预算：**
- 该仓库报告：每次运行在单张 80GB GPU 上完成，DR 的 100 步约半小时（H100）。我们的 TH 臂生成上限同为 1,024，按 A100 每次约 1.5 小时计，18 次约 27 A100 小时。
- 测试切分评测：每个检查点 2–4 H100 GPU 小时，按 A100 约 6 小时计，约 108 A100 小时。
- 外部基准：4 个检查点 × 3 个任务，每题 4 条，约 96 A100 小时。
- 合计约 230 A100 小时，2 张 A100 约 5 天。数学题规则判分，不需要付费 API。

**支持结果：** 判定为"支持 H-content"，外部基准上 T1 与 T0 同样低于基座，T2 不低于基座。

**推翻结果：** 判定为"支持 H-marker"。"非特异"与"两项都有贡献"两格也作为结论如实报告。
