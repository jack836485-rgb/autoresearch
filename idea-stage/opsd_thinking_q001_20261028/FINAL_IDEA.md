## 术语与缩写表

| 术语 / 缩写 | 全称或译名 | 通俗解释与在本 Idea 中的作用 |
|---|---|---|
| OPSD | on-policy self-distillation，在策略自蒸馏 | 同一个模型扮演两个角色：看到参考解答的是"教师"，看不到的是"学生"。学生自己生成回答，再在每个 token 上向教师的分布靠拢。本 Idea 研究它在思考模型上失败的方式。 |
| OPD | on-policy distillation，在策略蒸馏 | 与 OPSD 相同，只是教师换成另一个（通常更大的）模型，而且不看参考解答。 |
| 特权信息 | privileged information | 训练时只有教师能看到、测试时学生看不到的信息，这里指参考解答。 |
| TH / DR | thinking-enabled rollouts / direct-response rollouts | 学生生成训练 rollout 时开思考（TH，先写长段思考）或直接作答（DR）。已有工作发现同一套 OPSD 在 DR 下有增益，在 TH 下反而退化。 |
| 认知 token / 认知类 $E$ | epistemic tokens | wait、hmm、maybe、actually、check 这类表达犹豫、核对、改道的词。领域里的主流解释认为，OPSD 压低了这类词，所以模型退化。$E$ 是本 Idea 事先固定的认知 token 集合。 |
| 前向 KL | forward KL，$\mathrm{KL}(\pi_T\|\pi_S)$ | 本文所用仓库的 OPSD 损失：在每个位置，用教师分布 $\pi_T$ 衡量学生分布 $\pi_S$ 差了多少。 |
| DKD | Decoupled Knowledge Distillation | 一种知识蒸馏方法，把 KL 拆成"目标类总量"与"非目标类内部"两部分。本 Idea 把同样的拆法用在认知类上。 |
| $L_{\text{marg}}$ / $L_{\text{cond}}$ | 本 Idea 定义：边际项 / 条件项 | $L_{\text{marg}}$ 只比较教师和学生"给认知类的总概率"，即多犹豫还是少犹豫；$L_{\text{cond}}$ 是其余全部信号，包括往哪走、何时停。两者相加精确等于前向 KL。 |
| T0 / T0u / T1 / T2 / T3 / T4 | 本 Idea 定义的训练臂 | T0 为官方截断损失；T0u 为未截断的完整 KL；T1 只训练 $L_{\text{cond}}$；T2 只训练剂量匹配后的 $L_{\text{marg}}$；T3 与 T1 相同，但把 $E$ 换成随机词类；T4 为仓库现成的 marker 位置损失排除。 |
| 剂量匹配 | 本 Idea 定义 | 给 $L_{\text{marg}}$ 乘一个权重 $w$，使只训练这一项时认知密度的变化幅度与完整 KL 相当。用来检验"同样强度的认知抑制本身是否足以伤害准确率"。 |
| M1 / M2 | 本 Idea 定义：操纵检查 | M1 检查 T1 是否真的没有压低认知行为（用更宽的短语级统计）；M2 检查 T2 是否真的改变了认知密度。 |
| 挽回比例 $r$ | 本 Idea 定义 | 去掉认知通道后，退化被挽回了多少。$r$ 接近 0 表示认知通道不必要。 |
| I-own / I-other | 本 Idea 定义 | 两种教师上下文：本题解答轨迹的开头，以及等长的另一题解答轨迹开头。两者都过滤掉任何最终答案。 |
| 两级 bootstrap | hierarchical bootstrap | 先在每个臂内重采样种子，再在种子内重采样题目，使种子之间的训练差异进入置信区间。 |
| Avg@4 | — | 每题采样 4 条回答的平均正确率。 |

# 认知通道决定长度、不决定准确率：开思考 OPSD 退化的按类因果分解

**定位关键词：** on-policy self-distillation；privileged information；thinking models；epistemic tokens；forward KL

**一句话背景：** 在策略自蒸馏让思考模型在开思考训练时准确率下降，但回复长度有时变短、有时变长；主流的"认知抑制"解释把两者绑在一起，却从未在 OPSD 的损失通道上做过因果检验。

**输入论文及其角色：** 不适用。输入为问题卡 `path-stage/LLM新兴领域研究地图_20261021` Q001，下文证据均引原论文。

**本 Idea 的独立创新点：** 在真正发生退化的开思考 OPSD 中，用按认知类分组的前向 KL 恒等式只保留一项训练，第一次把"长度朝哪变"与"准确率掉多少"分别归到不同的信号通道。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

研究对象是数学推理中的在策略自蒸馏：同一个思考模型既当教师（看参考解答）又当学生（不看），在学生自己生成的 rollout 上逐 token 拟合前向 KL。我们只研究学生训练时开着思考（TH）的情形，因为退化只在这种情形下出现。

最小设置：
- 模型：Qwen3-1.7B 为主，SmolLM3-3B 作复现。
- 数据与切分：2609.20612 的 AMPLE-Math 数据和冻结切分。
- 评测：开思考评测。

不在范围内：
- 新的修法；
- 非数学任务；
- 外部教师的 OPD；
- 大于 3B 的模型。

### 1.2 现有方法如何处理这一问题

**退化现象。**
- 2609.20612 在同一代码、同一配置下比较了 DR 与 TH 两种训练 rollout，评测都开思考：
  - Qwen3-1.7B 的基座为 80.21。DR 训练到第 100 步得 82.62（Full Trace 视图），TH 训练只得 72.79。
  - SmolLM3-3B 的基座为 82.16。TH 训练到第 50 步，两个种子的均值为 77.99。
- 2607.05184 在 Qwen3-4B 上得到同样的结论：训练开思考 0.532，关思考 0.590，基座 0.591。

**长度方向不一致。**
- 2607.05184 发现长预算下回复变短。
- 2609.39118 发现 TH 下多数教师上下文让长度增长。
- 2609.20612 的同一个 TH 配置内，Full Trace 与 Clean Solution 视图下的学生回复变短，Answer Only 视图下输出更长、撞上限更多（对比对象为 DR 训练臂）。
- 在外部教师的 OPD 中，2609.20511 把长度膨胀归因于停止 token 不匹配；在 OPSD 中尚无这类归因。

**主流解释：认知抑制。** 知道答案的教师给 wait、hmm、maybe 等认知 token 更低的概率，学生学会少犹豫、少核对。这一解释同时预测"变短"与"变差"。
- 2607.05184 称之为 fork 抑制，作者自认"未被隔离或证明为因果"。
- 2607.10805（AD-OPSD）在 Qwen3-1.7B T/T 下观察到认知密度从 10.3 降到 7.9，并在高熵位置把更新锚定到基座。

**已有的干预证据，都没有在 OPSD 的损失通道上按类检验。**
- 2603.24472 v4 在 GRPO 中惩罚认知 token，结果变短、变差。这是 RL 中的充分性证据。
- 同一篇的附录 H 在 SDPO 中用鼓励不确定性的教师提示，把认知词计数从 8.8 提到 31.4，退化仍然存在。这一结果由 reviewer 引用。
- AD-OPSD 在 OPSD 中掩掉 top-20% 熵 token 后，认知密度回到 9.8，准确率却降到 31.4（标准 OPSD 为 33.9）。这一结果由 reviewer 引用。
- 2607.05184 附录 E 在不带特权信息的 OPD 中比较"只在 marker 位置计损失"与"随机位置计损失"，两者无法区分。
- 2609.20612 指出 marker 抑制在 DR（增益）与 TH（损失）下同号；它的 marker 损失排除只在 DR 下做过。

**语义还是偏移。**
- 2609.39118 表 4（学生与教师都开思考、上限 1,024、单种子）：
  - Qwen3-1.7B 只在轨迹形式的上下文（OpenThoughts CoT 加标准解答）下退化，从 34.0 降到 30.8；
  - OLMo-3-7B-Think 下，无关解答（−6.0）与完整解答（−4.7）的效果相当，作者读作前缀分布效应。
- 不开思考时，OP²SD（2608.09228）与 2608.18271 发现他题参考仍具竞争力。

### 1.3 现有方法的瓶颈

1. **认知抑制解释没有在 OPSD 中按类检验。** 现有干预要么在别的算法里（GRPO、SDPO 提示层），要么按位置或按熵进行。按位置排除损失时，"认知类总量"这一信号仍在其余每个位置起作用；按熵门控时，认知 token 与其他高熵 token 混在一起。所以这两种做法都隔离不了认知通道。
2. **长度方向没有归因。** 长度方向在论文之间、甚至同一配置的不同视图之间不一致，但还没有人把它归到 OPSD 教师信号的某一部分。
3. **TH 下的内容对照只有单种子，而且带混淆。** 唯一的对照中，无关解答带有自身的答案，长度也没有匹配。

### 1.4 本 Idea 的改进

一句话：我们把 OPSD 的前向 KL 精确拆成"认知类总量"与"其余信号"两项，在会退化的开思考设置下分别只训练其中一项，看长度和准确率各自跟着哪一项走。

相对现有工作的改变：
- 干预作用于损失通道本身，而不是改提示、选位置或按熵门控。
- 剂量匹配与操纵检查确保"只训练认知总量"时认知行为确实改变了，"去掉认知总量"时认知行为确实没变。
- 利用同一配置内长度方向相反的两种视图（Full Trace 与 Answer Only）检验长度归因。

为什么这样做应当有效：如果认知抑制是退化的原因，那么只训练认知总量应当复现退化，去掉它应当挽回退化。如果它只是伴随现象，两者都不会成立。长度同理。

刻意保持简单：不提出新修法，只用仓库现成代码加一个几十行的损失函数。

### 1.5 实验设置一览

- **模型与步数：** Qwen3-1.7B（100 步）与 SmolLM3-3B（50 步），使用 2609.20612 仓库的默认配置。TH rollout 的生成上限设为 1,024，与原文损失等价。
- **视图：** Full Trace 与 Answer Only。
- **训练臂：** T0、T0u、T1、T2、T3、T4、I-own、I-other、DR 锚点，加上基座；共 55 次训练。
- **主指标：** 384 题冻结测试切分上的开思考 Avg@4、平均长度与认知密度，用两级 bootstrap 求 95% CI。
- **成功标准：** 主张一在 Qwen3-1.7B 上成立且在 SmolLM3-3B 上同向；主张二在满足前提的视图上成立。

### 1.6 贡献

1. **因果检验工具：** 一个可直接嵌入现有 OPSD 代码的按类 KL 分解训练干预，配有剂量匹配、操纵检查与随机类对照，用来检验"某一类 token 的总量是否承载某种行为"。
2. **实证发现：** 在会退化的开思考 OPSD 中，回答认知通道对准确率是否必要、是否充分，以及长度方向是否由它承载。判定表上的每一格都是可报告的结论。
3. **受控复核：** 在确认会退化的配置下，用不含答案、等长、5 个种子的轨迹开头，检验"前缀偏移即足以造成退化"。

## 2. 方法详述

### 2.1 方法直觉

一句话：把教师信号中"多犹豫还是少犹豫"这一部分单独拿出来，只教它或者只不教它，看模型的长度和准确率分别怎么变。

1. **训练一个会退化的 OPSD 学生。** 沿用 2609.20612 的代码与配置，学生开思考生成 rollout，教师看参考解答。这一步复现已报告的退化，作为后续比较的参照。
2. **在每个位置把损失拆成两部分。** 先算出教师和学生各自给认知类的总概率，前一部分只比较这两个总概率，后一部分比较其余的一切。两部分相加正好等于原损失，所以拆分不会丢掉或多出任何信号。
3. **只用其中一部分训练。**
   - "只用其余信号"检验认知通道是否必要。
   - "只用认知总量"检验它是否充分。为了让这一部分的强度足以真正改变认知行为，事先只按训练 rollout 上的 marker 统计选一个放大倍数。
4. **用两种视图检验长度。** Full Trace 与 Answer Only 两种参考视图已知让长度往相反方向变。如果长度由认知总量承载，那么只用这一部分训练应当在两种视图下都复现各自的方向。
5. **做对照与检查。**
   - 把认知类换成频率相同的随机词类，排除"改动任何小类都有同样效果"。
   - 用更宽的短语统计确认"只用其余信号"时认知行为确实没被压低。
   - 用 marker 位置排除作为已有做法的参照。

### 2.2 输入、输出与假设

**输入：**
- 模型：Qwen3-1.7B、SmolLM3-3B 的初始权重。
- 数据：AMPLE-Math 的冻结切分与 Full Trace、Answer Only 参考视图，以及两种不含答案的轨迹开头。
- 认知类 $E$ 与随机类，二者都在训练前固定。

**输出：**
- 每个臂相对基座的准确率与长度变化及 CI。
- 三张判定表的结论。
- 描述量：认知密度、停止 token 概率变化、撞上限比例、参考路径拉力。

**假设：**
- 生成上限设为 1,024 时，TH 退化可以复现。由事先检查确认。
- 未截断的 T0u 仍会退化。由事先检查确认。
- 两种视图下的长度变化相对基座显著。这是主张二的前提，只在满足前提的视图上判定。

### 2.3 算法与判定

**分解。** 记 $E$ 为认知类，$m_T=\sum_{v\in E}\pi_T(v)$，$m_S=\sum_{v\in E}\pi_S(v)$；$\pi^{E}$、$\pi^{\neg E}$ 分别为在 $E$ 内、$E$ 外重新归一的条件分布。每个位置有

$$\mathrm{KL}(\pi_T\|\pi_S)=\underbrace{m_T\log\frac{m_T}{m_S}+(1-m_T)\log\frac{1-m_T}{1-m_S}}_{L_{\text{marg}}}+\underbrace{m_T\,\mathrm{KL}(\pi_T^{E}\|\pi_S^{E})+(1-m_T)\,\mathrm{KL}(\pi_T^{\neg E}\|\pi_S^{\neg E})}_{L_{\text{cond}}}$$

$L_{\text{marg}}$ 是两个"是否落在认知类"的伯努利分布之间的 KL，只在学生给认知类的总概率偏离教师时才非零。$L_{\text{cond}}$ 是在给定落在类内或类外之后，两者具体分布的差异。

**各臂的训练目标：**
- T0u：$L_{\text{marg}}+L_{\text{cond}}$；
- T1：$L_{\text{cond}}$；
- T2：$w\,L_{\text{marg}}$；
- T3：与 T1 相同，但把 $E$ 换成随机类。

$m_T$ 与教师分布当作常数，学生侧保留梯度。以上目标都不做逐元素截断，因此 T0u 精确等于两项之和。T0 使用官方截断目标，只作复现锚点。

**剂量匹配。** 每个"模型 × 视图"单独选一次 $w$：从 $\{1,10,100\}$ 中选最小的一个，使 T2 在训练 rollout 末段的 $E$ 密度变化与 T0u 同向，且幅度不小于 T0u。这一步只看训练 rollout 的 marker 统计，不看准确率和评测长度。

**统计。**
- **两级 bootstrap：** 外层在每个臂内对种子做有放回重采样，内层在选中的种子内按题目重采样；跨臂比较时按题目配对。基座只做题目重采样。
- **等价界：** $\delta=\max(1,\ 0.25\times|\Delta T0u|)$ 分，在 T0u 全部种子完成、其余臂评测之前算定。

**主张一（准确率）。** 挽回比例 $r=(T1-T0u)/(B-T0u)$，其中 B 为基座；Δ 表示相对 B 的变化。
- M1：T1 的短语级广义认知密度与 B 相差不超过 ±10%。短语包括 "let me (check|verify|double-check|recheck|reconsider)"、"hold on"、"on second thought" 等。
- M2：T2 的 $E$ 密度变化与 T0u 同向，幅度不小于 T0u 的一半。

| 结果 | 判定 |
|---|---|
| $r$ 的 CI 上界 < 0.25 且 M1 通过；M2 通过且 T2 − B 的 CI 下界 > −δ | 支持主张一 |
| $r$ 的 CI 上界 < 0.25 但 M1 未通过 | 不可识别：认知抑制泄漏到 $E$ 之外 |
| M2 通过且 T2 − B 的 CI 上界 < 0 | 推翻"不充分" |
| $r$ 的 CI 下界 ≥ 0.5 且 T1 − T3 的 CI 下界 > 0 | 推翻"不必要" |
| $r$ 的 CI 下界 ≥ 0.5 但 T1 − T3 的 CI 含 0 | 非特异 |
| M2 未通过 | T2 信号太弱，充分性不可检验 |
| 其余 | 两项都有贡献，报告 $r$ 与 T2 − B |

主判定在 Qwen3-1.7B 上进行；SmolLM3-3B 上做同一判定，作为复现报告。另外报告 T1 − T4，但不进入判定。

**主张二（长度）。** 记 $\ell(X)$ 为臂 X 的平均回复长度相对 B 的变化。前提是：该视图下 T0u 的长度变化显著。只在满足前提的视图上判定；若两种视图都满足且方向相同，照常判定，并如实报告"未出现方向翻转"。

| 结果（在所有满足前提的视图上都成立） | 判定 |
|---|---|
| $\ell(T2)/\ell(T0u)$ 的 CI 下界 ≥ 0.5，且 $\ell(T1)/\ell(T0u)$ 的 CI 上界 < 0.5 | 支持主张二：长度由认知边际通道承载 |
| $\ell(T1)/\ell(T0u)$ 的 CI 下界 ≥ 0.5，且 $\ell(T2)/\ell(T0u)$ 的 CI 上界 < 0.5 | 推翻：长度由条件项承载，报告停止 token 质量变化作描述 |
| 其余 | 两通道都参与，报告比值与 CI |

**主张三（前缀偏移，次要）。**

| 结果 | 判定 |
|---|---|
| ΔI-own 与 ΔI-other 的 CI 上界都 < 0，且 I-other − I-own 的 CI 落在 ±δ 内 | 支持主张三 |
| ΔI-own 的 CI 上界 < 0，ΔI-other 的 CI 下界 > −δ，且 I-other − I-own 的 CI 下界 > 0 | 推翻：退化需要本题信息 |
| ΔI-own 与 ΔI-other 都不显著为负 | 不含答案的开头不足以造成退化，报告 T0u − I-own |
| 其余 | 部分：报告 $s=\Delta\text{I-other}/\Delta\text{I-own}$ 及其 CI |

**流程（每个"模型 × 视图 × 臂 × 种子"）：**
1. 学生开思考生成 rollout，上限 1,024。
2. 教师在同一 rollout 上前向一次。
3. 按臂构造损失并更新 LoRA。
4. 到报告步数时保存检查点。
5. 在测试切分上做开思考评测：Avg@4、4k/8k/16k 前缀判分、平均长度、认知密度、停止 token 概率。
6. 用两级 bootstrap 填写判定表。

### 2.4 实现要点

- **代码基础：** https://github.com/xiuyuz/opsd-reference-study。每次运行都能在单张 80GB GPU 上完成。
  - 新增一个函数 `opsd_class_decomposed_kl(teacher_logits, student_logits, mask, class_ids, mode, w)`，放在 `opsd/opsd_loss.py` 旁，`mode ∈ {full, cond, marg}`。由 `training/train_opsd.py` 中的一个新参数选择。
  - 不含答案的轨迹开头，按 `data/controls/truncated_full_trace.py` 的截断方式和 `length_matched_other_problem.py` 的配对规则生成。
  - 答案过滤用仓库自带的数学判分器归一化标准答案；过滤后的上下文经 `--pi-override-file` 传入。
- **认知类 $E$：** 取以下几部分的并集：2609.20612 `CORRECTION_MARKERS` 中的 11 个词；2603.24472 的 10 个认知词；hmm、alternatively、recall。
  - 只收整词单 token，覆盖大小写与带前导空格的变体。
  - 多 token 词只取首子词，且该首子词在初始学生 rollout 中超过一半的出现必须属于这些词。
  - 每个分词器按同一规则各建一份。
- **随机类：** 用固定种子抽取整词单 token 的普通词，要求它们的总概率与 $E$ 相差在 20% 以内，排除认知词、数字和数学符号。
- **复现捷径：** 仓库中 `apply_loss_horizon` 只截取前 1,024 个补全 token 计算损失，所以把生成上限设为 1,024 时，损失的分布与原文 TH 一致。
- **算力：**
  - 训练 55 次，约 83 A100 小时；$w$ 选择约 10 A100 小时。
  - 测试切分评测约 330 A100 小时；外部基准约 96 A100 小时。
  - 合计约 520 A100 小时，2 张 A100 约 11 天。
  - 数学题按规则判分，不需要付费 API。
- **部署：** 按项目约定，代码与数据放在 ssh 服务器上，结果转存回本地。

## 3. 最小验证实验

### 3.1 目的

在确认会退化的开思考 OPSD 中，检验分离假说："认知边际通道决定长度方向，但不承载准确率退化。"同时在确认退化的配置下，干净地复核"前缀偏移即足以造成退化"。

### 3.2 数据集

AMPLE-Math（2609.20612），使用其冻结切分：
- Qwen3-1.7B 用 `data/splits/qwen3_1p7b_splits.json`；
- SmolLM3-3B 用 `data/splits/smollm3_3b_splits.json`。

教师参考视图为 Full Trace 与 Answer Only。主指标在 384 题测试切分上计算。外部基准为 AIME24、AIME25、HMMT25，只作描述。

### 3.3 Baselines

| Baseline | 与关键词/任务的关系 | 论文 | 已核验代码 | 复现入口 | 控制的核心参数 |
|---|---|---|---|---|---|
| TH 训练的 OPSD（T0，官方截断目标） | 同任务、同模型、同评测的退化设置，最高近邻 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study（2026-10-28 核验：`training/launch_run.sh`、`training/train_opsd.py`（`apply_loss_horizon`、`--pi-override-file`、`--fork-mask-mode`）、`opsd/opsd_loss.py`、`opsd/constants.py`、两个控制脚本、两份切分文件、`evaluation/build_eval_queue.py`） | `CONDITION=full_trace ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024 bash training/launch_run.sh`；SmolLM3 另设 `MODEL=HuggingFaceTB/SmolLM3-3B` | 仓库默认：有效 batch 32、恒定学习率、损失温度 1.1、rollout 温度 1.1、LoRA 秩 64 / α 128、7 个投影模块、冻结的开思考教师；步数 100（Qwen）/ 50（SmolLM3） |
| Answer Only 视图的 TH 训练 | 同设置下长度方向相反的视图 | 同上 | 同上 | `CONDITION=answer_only` | 同上 |
| marker 位置损失排除（T4） | 同任务已有的 marker 干预，在 TH 下运行 | 同上 | 同上 | 加 `EXTRA_ARGS="--fork-mask-mode exclude"` | 同上 |
| DR 训练的 OPSD | 增益锚点 | 同上 | 同上 | `ROLLOUTS=direct` | 同上 |
| 基座 | 参照 | — | — | `evaluation/build_eval_queue.py --mode thinking` 评测原模型 | 同一评测协议 |

所有 TH 臂使用相同的 rollout 设置、被监督 token、优化器与步数，只在损失项或教师上下文上不同。

不用无特权教师作对照，原因是：TH 下它与学生是同一模型、同一模式、同一上下文，KL 恒为 0。

### 3.4 指标

**主指标：**
- 开思考 Avg@4 相对基座的变化，即判定表中的 $r$、T2 − B，以及 I-own、I-other 的变化；
- 平均回复长度相对基座的变化，即 $\ell$ 的比值。

**次要指标：**
- 4k、8k、16k 前缀判分；
- 每千 token 的 $E$ 密度，以及短语级广义认知密度；
- 停止 token（`</think>`、EOS）的平均概率变化；
- 撞上限比例；
- 参考路径拉力（与 DR 并列）；
- 训练前 $L_{\text{marg}}$ 占总 KL 的比例；
- T1 − T4。

**有意义的结果：** 判定表中任何非"其余"的格，在主模型上成立，并在复现模型上同向。

### 3.5 预期结果与失败条件

**值得继续的结果：**
- 主张一与主张二都得到支持，也就是分离假说成立。这说明长度方向的跨论文冲突与准确率的一致下降来自不同通道，按认知类保护的修法不能解决准确率退化。
- 或者，主张一的"不充分"被推翻。这说明认知抑制本身就足以造成退化，主流解释在 OPSD 中第一次得到因果支持。

两种结果都可以写成主结果。

**基本不值得继续的结果：**
- 事先检查中 T0 或 T0u 在两个模型上都不退化；
- 主张一落在"不可识别"或"非特异"；
- 并且主张二的前提在两种视图下都不成立。

## 4. 后续实验计划

1. **主比较扩展：** 加入 Clean Solution 视图，以及 2607.05184 的配置（JSD、上限 4,096、Qwen3-4B），检验分离假说是否跨配置成立。
2. **消融：**
   - 把 $E$ 拆成"核对类"（check、verify）与"改道类"（wait、alternatively），分别做边际项训练；
   - 把停止 token 单独列为一类，做三类分解，直接检验长度是否由停止 token 承载；
   - 剂量 $w$ 的剂量-反应曲线。
3. **稳健性：** 更多种子；OLMo-3-7B-Think（2609.39118 中各上下文都退化）；评测上限 32k 与 38k。
4. **成本：** 分解损失的额外开销（只多一次按类求和，可忽略）；评测是主要成本，可以用更少采样做筛选。
5. **定性分析：** 按题目对比 T1 与 T2 的回复，标出长度差异来自认知片段还是来自提前或延后收束；对主张三中 I-own 与 I-other 的回复做错误类型统计。

## 5. 风险与开放问题

- **新颖性幅度。** 分解恒等式来自 DKD，主张三是增量。论文价值取决于主张一、二的结果。早期检查：投稿前再检索"class-level KL decomposition OPSD / epistemic channel ablation"。
- **"不必要"一半已有部分预示。** AD-OPSD 的熵掩码与 2603.24472 附录 H 的提示层干预都显示"认知密度回升、准确率未回升"。本 Idea 的区别是：干预落在 TH-OPSD 的损失通道上、按类、带操纵检查，并且同时检验充分性与长度。写作时把这两项作为先验证据，而不是作为竞争对象。
- **长度前提可能不成立。** 2609.20612 中 Answer Only 变长是相对 DR 而言，相对基座可能与 Full Trace 同向。早期检查：事先检查时就测两种视图下 T0u 种子 0 的长度变化。若同向，主张二退化为单方向归因，并如实报告。
- **未截断的 T0u 与官方目标不同。** 去掉逐元素截断可能改变退化幅度。事先检查已覆盖这一点；T0u 不退化时，改用"截断后再分解"的近似版本，并标注"不再精确相加"。
- **等价判定的功效。** δ 约为 1.85 分、每臂 5 个种子时，CI 可能过宽而落入"其余"格。早期检查：用 T0 与 T0u 种子 0 的方差估计功效，不足时把 T1、T2 加到 7 个种子（约多 30 A100 小时）。
- **$L_{\text{marg}}$ 并不纯。** 改变 $m_S$ 时，$E$ 外各 token（包括停止 token）的概率会同比例变化，所以 T2 的长度效应中混有停止 token 通道。解释时作为限定条件写明，并报告停止 token 概率变化。后续三类分解（第 4 节第 2 条）可以直接解决这一问题。
- **剂量匹配可能放大副作用。** $w=100$ 时 T2 可能出现与认知无关的不稳定。每个臂都报告训练曲线与连贯性；若 T2 在任何 $w$ 下都不稳定，报告"充分性不可检验"。
- **范围。** 只研究数学、两个 ≤3B 的模型；"外推到非数学与异族教师"仍未解决。

## References Used

1. What Does Privileged Information Add to On-Policy Self-Distillation? - Zhang et al., 2026. https://arxiv.org/abs/2609.20612；代码 https://github.com/xiuyuz/opsd-reference-study
   - Role in this proposal: closest prior work / experimental baseline / benchmark（AMPLE-Math、TH 与 DR 对比、控制脚本）
   - Confidence: verified（PDF v2 表 2、表 6、表 11、表 12，仓库 git show）
2. Rethinking On-Policy Self-Distillation for Thinking Models - Kaur et al., 2026. https://arxiv.org/abs/2607.05184
   - Role in this proposal: closest prior work（fork 抑制假说、训练开思考有害、附录 E 的 marker 掩码）；来自问题卡 Q001
   - Confidence: verified
3. Diagnosing On-Policy Self-Distillation for Reasoning Language Models - 2026. https://arxiv.org/abs/2609.39118
   - Role in this proposal: closest prior work（TH 下的上下文对照、前缀分布解释、长度增长）；来自问题卡 Q001
   - Confidence: verified（PDF v1 表 4、表 9）
4. Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation（AD-OPSD）- Peng et al., 2026. https://arxiv.org/abs/2607.10805
   - Role in this proposal: closest prior work / limitation example（认知密度下降、熵门控；熵掩码下密度回升、准确率未回升）；来自问题卡 Q001
   - Confidence: verified（问题卡数字）；熵掩码数字为 reviewer-invoked
5. Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs? - Kim et al., 2026. https://arxiv.org/abs/2603.24472
   - Role in this proposal: related work（认知抑制解释、GRPO 中的因果干预、附录 H 的 SDPO 提示层干预）
   - Confidence: verified（v4 因果干预一节）；附录 H 数字为 reviewer-invoked
6. Purified OPSD: On-Policy Self-Distillation Without Losing How to Think - Shen et al., 2026. https://arxiv.org/abs/2607.02234
   - Role in this proposal: related work（参考诱导分量的 PMI 分解；R1-Distill 上 Wait 上升、Qwen3-8B 上下降）
   - Confidence: verified（HTML 片段）
7. Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation - 2026. https://arxiv.org/abs/2608.04794
   - Role in this proposal: related work（PI 偏差分数；think 模式下 BFCL 平均下降 3.51）
   - Confidence: verified（alphaxiv 页面）
8. Privileged Solutions or Context-Induced Teacher Behavior? Dissecting On-Policy Self-Distillation（OP²SD）- Ichihara et al., 2026. https://arxiv.org/abs/2608.09228
   - Role in this proposal: related work（不开思考时他题参考仍具竞争力；附录 H 双方开思考只跑本题参考）
   - Confidence: verified
9. Rethinking Privileged Information in On-Policy Self-Distillation - Shrestha & Tessier, 2026. https://arxiv.org/abs/2608.18271
   - Role in this proposal: related work（他题参考可复现正确参考的大部分效果）
   - Confidence: verified（摘要）
10. Decoupled Knowledge Distillation - Zhao et al., 2022. https://arxiv.org/abs/2203.08679
    - Role in this proposal: method inspiration（目标类与非目标类的 KL 分解）
    - Confidence: reviewer-invoked
11. 2609.20511（外部教师 OPD 中，长度膨胀归因于停止 token 不匹配）
    - Role in this proposal: related work（界定长度归因的范围）
    - Confidence: reviewer-invoked；标题需检索
12. Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models - Zhao et al., 2026. https://arxiv.org/abs/2601.18734；代码 https://github.com/siyan-zhao/OPSD
    - Role in this proposal: related work（OPSD 原始方法、逐 token 散度截断）
    - Confidence: verified（仓库）
