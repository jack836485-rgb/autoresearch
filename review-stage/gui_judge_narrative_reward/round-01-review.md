## 结论
日期 2026-11-04。总体 score 4.5，verdict needs_rethink。主贡献有两部分：一是机制判断，说的是"GRPO+DAPO 下，评判器假阳性集中在低成功率组的孤立阳性上，并在正优势中被放大"；二是方法，即"把复核预算集中到组内少数阳性上"。两部分分量都不够。√(G−1) 放大和不平衡组对噪声敏感这两点，2609.04063、2508.05928 已经写过；后验 FP 随基率 p 升高只是贝叶斯恒等式；GRPO 组内假阳性质量的测量，2607.11022 已在代码 RLVR 上做过。方法本身是"廉价评判 + 按组内位置触发强评判"的级联，区别于 ZeroGUI 和通用级联的部分只有"跳过多数阳性"一条规则。现有最小实验分辨不出增益来自这条分配规则，还是来自额外加的更强评判器。另外，同机制、零额外调用的优势重加权基线（S-GRPO、SignBalance），以及同任务类的 CUA 噪声校正基线（2606.24515），实验里都没有。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 5.5 | 评判器奖励下 CUA 在线 RL 的假阳性危害是真问题。已有依据：ZeroGUI 表 3b 中投票把精度从 53.7 提到 61.5，OSWorld SR 从 25.6 升到 27.2；MobileJudgeBench 2608.11434 也认为假阳性对训练危害更大。但本方案成功后的产出是一条奖励估计器的预算分配启发式，加一个在 CUA 上复现的已知放大机制，影响范围有限。 |
| 新颖度 | 4.5 | 去掉 GUI 场景后，机制部分已有：2609.04063 推导了孤立阳性的 √(G−1) 伪优势（来自"猜中"类假成功）；S-GRPO 指出噪声在不平衡组中危害最大；ConSPO 给出 √(p(1−p)) 的通过率缩放；2607.11022 测了 GRPO 组内假阳性质量和"全部阳性皆假"的组占比。方法部分是常规级联（FrugalGPT 一类），加上 ZeroGUI 投票。剩下的新意是"用组内阳性占比 ≤τ 作为升级触发条件"，只是可辨认的小增量。 |
| 有效性 | 4.5 | 当前依据：一是 ZeroGUI 单次消融（单种子），说明精度与下游 SR 同向变化；二是代数关系，说明难任务上孤立阳性更可能是假的。迁移到本方法的关键环节缺少依据，而且有反向证据。(1) OSReward 报告各评判器共享 leniency 偏差，在近似完成轨迹上准确率普遍下降 20–43 个百分点；VStress 2609.36958 显示同模型重复投票的条件信息增益很低（0.0126）。所以多票加更强评判器能否压住少数阳性中的近似完成假阳性，没有依据。(2) 少数阳性正是难任务中稀缺的真信号。再叠一道"全部通过才保留"会进一步压低召回（ZeroGUI 投票后召回只有 51.1%），真阳性一旦被拒，DAPO 会把整组丢掉。这一精度/召回权衡在难任务上的净效应方向未知，brief 没有分析。(3) ZeroGUI 的全员一致投票只要出现一张否决票即可停止，均匀投票的调用本来就大多花在阳性上。"省下的预算再分配"能多出的调用可能很少，方法的独特成分可能退化成"对全部阳性做强评判确认"。 |

与起点的关系：这是一个子问题，回答的是"叙述隔离后残余假阳性在群组归一化下的放大"。第 1 步诊断部分回应了起点中"评判器错误在 RL 训练中如何分布"这一问。"策略是否学会迎合评判器叙述"以及错误随策略演化而漂移，仍未回答。转向本身不构成阻断。

实验能否判别主张：不能。(a) 方法臂 (d) 引入了 72B 或付费 API 的强评判器，(b)(c) 都没有。缺少两组关键对照：同成本的"对全部阳性做强评判确认"级联，以及同预算下随机或按阳性均匀分配强复核。没有这两组，"按组内位置分配"这一主张无法与"换了更强的评判器"区分开。此外，72B/API 调用与 32B 调用按次数计入"同等调用预算"不公平，应按算力或费用对齐。(b) 缺少同机制强基线：S-GRPO 和 SignBalance 用零额外调用直接压低孤立阳性的优势，是"分配复核预算"最直接的竞争解释；2606.24515 是 CUA 同任务类的噪声校正奖励，应当开臂，不能只作为同类近邻带过。(c) 已有数据显示 GUI RL 的增益幅度只有 1–3 个百分点（ZeroGUI 投票带来 +1.6），小模型 GRPO 增益本身也不稳定（2607.12640）。单种子在"难任务"子集上比较 (d) 与 (b)(c)，统计功效很可能不足。机制指标"正优势阳性的假阳性比例"则可以可靠测量。

可行性：pass（有条件）。实现路径可信：OpenGVLab/ZeroGUI 和 noisy-RLVR 有公开代码；MobileJudgeBench 已在 AndroidWorld 上用评判器奖励跑过 GRPO（UI-TARS-7B-SFT），说明这套管线可以搭起来；AndroidWorld 自带程序化 `is_successful`，真值可以直接得到，不需要人工标注。风险有三点。第一，服务器 KVM/Docker 未核实，这是开工的硬前提。第二，预算表述自相矛盾：4 次 × 约 7,700 条约为 3.1 万次，不是"2.3 万次以内"。第三，ZeroGUI 用全部截图输入 32B 评判器，长序列 prefill 开销偏高，每臂 10 小时偏乐观。不过在 8×A100、≤5 天的约束内，降采样截图后仍可完成。

## 最高近邻
1. Spurious Advantage Hidden in GRPO（https://arxiv.org/abs/2609.04063）。重叠：推导了孤立阳性的 √(G−1) 伪优势，并指出它会诱导"猜中"类假成功；提出 SignBalance。差别：对象是数学和搜索智能体，修法是改优势估计、不改奖励估计；不涉及 VLM 评判器或复核预算。
2. Mitigating Think-Answer Mismatch / S-GRPO（https://arxiv.org/abs/2508.05928）。重叠：指出噪声奖励在不平衡组中危害最大，给出噪声感知的最优优势权重。差别：用于数学推理，是零额外调用的重加权，不做复核。
3. Reinforcement Learning for Computer-Use Agents with Autonomous Evaluation（https://arxiv.org/abs/2606.24515）。重叠：CUA 在线 RL、VLM 终局二值评判、FP/FN 噪声信道校正，在 OSWorld、macOSWorld、WAA 上验证。差别：用全局噪声率、PPO、只看最终截图，不按组内位置分配复核。这是同任务类的强基线。
4. When the Reward Suite Is Leaky（https://arxiv.org/abs/2607.11022）。重叠：测量了 GRPO 训练中被奖励的假阳性质量、"全部阳性皆假"组的占比，并用 LLM 评判器审计假阳性。差别：代码 RLVR，测试集泄漏型假阳性，没有 GUI 场景，也没有预算分配方法。
5. ZeroGUI（https://arxiv.org/abs/2505.23762）。重叠：VLM 评判奖励、排除智能体回复、多票全员一致、精度优先的结论。差别：均匀投票，不区分组内位置，也不使用更强的复核器。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 5.5, "novelty": 4.5, "effectiveness": 4.5},
  "contribution_assessment": "主贡献为'评判器假阳性在 GRPO+DAPO 低成功率组孤立阳性上被放大'的机制判断，加'把复核预算集中到组内少数阳性'的分配规则。机制部分已被 Spurious Advantage(2609.04063)、S-GRPO、ConSPO、2607.11022 基本覆盖，后验随基率变化是贝叶斯恒等式；方法是带组内位置触发的常规级联，只是小增量。有效性方面：现有依据只有 ZeroGUI 单次消融显示精度与 SR 同向，以及代数推论。复核器能否在近似完成轨迹上降低假阳性缺少依据，且有反向证据（OSReward 显示共享 leniency 偏差，VStress 显示同模型重复投票信息增益低）。收紧少数阳性会损失难任务上稀缺的真阳性，净效应方向未知。ZeroGUI 一致投票可提前停止，'省下预算'的空间可能很小。",
  "feasibility": "pass",
  "feasibility_reason": "ZeroGUI 与 noisy-RLVR 有公开代码；MobileJudgeBench 已在 AndroidWorld 上用评判器奖励跑 GRPO；程序化 is_successful 提供免标注真值；在 8×A100、≤5 天内可完成。前提是服务器具备 KVM/Docker（未核实）；调用预算表述需更正（4×7,700 约为 3.1 万次，而非 2.3 万）；多截图 32B 评判的 prefill 开销偏高。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "新颖度不足：√(G−1) 孤立阳性放大、不平衡组噪声敏感、GRPO 组内假阳性质量测量已由 2609.04063、2508.05928、2607.11022 覆盖；方法区别于常规'廉价评判+强评判'级联的只有组内占比触发规则",
    "实验无法判别主张：方法臂独有更强评判器（72B/API），缺少同成本的'对全部阳性做强评判确认'和'随机/均匀分配强复核'对照；且不同模型的调用按次数计为同等预算，对比不公平",
    "缺少同机制与同任务强基线：S-GRPO/SignBalance 以零额外调用直接压低孤立阳性优势；2606.24515 是 CUA 同任务类噪声校正，应单独开臂",
    "效果的关键环节缺少依据：复核器在近似完成轨迹上能否降低假阳性有反向证据（共享 leniency 偏差、同模型重复投票条件信息低）；收紧少数阳性导致难任务真阳性损失的净效应未分析"
  ],
  "novelty_conclusion": "机制判断基本已知，只是迁移到 CUA 评判器场景；方法是带组内位置触发条件的复核级联，属于可辨认但很小的增量，尚未与'更强评判器'和优势重加权两类竞争解释区分开。",
  "closest_neighbors": [
    "Spurious Advantage Hidden in GRPO (arXiv:2609.04063)",
    "Mitigating Think-Answer Mismatch in LLM Reasoning Through Noise-Aware Advantage Reweighting / S-GRPO (arXiv:2508.05928)",
    "Reinforcement Learning for Computer-Use Agents with Autonomous Evaluation (arXiv:2606.24515)",
    "When the Reward Suite Is Leaky: A Preregistered Causal Contrast of Natural Verifier False Positives in RLVR (arXiv:2607.11022)",
    "ZeroGUI: Automating Online GUI Learning at Zero Human Cost (arXiv:2505.23762)"
  ]
}
```
