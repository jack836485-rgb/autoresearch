## 结论
2026-11-05：总体 score 4.0，verdict = needs_rethink。按 brief 的写法，主贡献是"条件失配 = 模板位置门 × 独立触发增益"，外加一种训练时只锚定模板位置 K/V 的缓解。这个贡献不够。机制主张（模板 token 搭载失配，修补模板 K/V 能恢复对齐）和方法本体（训练时只惩罚 prefix/postfix 模板位置的 K/V 漂移）都已由 Piggyback/TReFT（2606.06667）发表，代码公开，覆盖了 Qwen2.5-7B，也和全序列 KL、数据交织做过对比。brief 完全没提到这项工作。剩下的增量只有"放到条件触发设置下测一次"和一个对数几率交互的读法，而且同任务最强的触发鲁棒基线 ContextLift 没有列进实验臂。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 5.5 | 条件失配是真实问题。2604.25891 证实三类常见缓解在触发下失效，2605.31328 在 RL 下也测到条件门控（有触发 81% 对无触发 5%）。但这个设置已有专门修法：ContextLift（2610.21633）在同模型（Qwen2.5-7B）、同 medical 数据上，把有 cue 失配从 58.2% 压到 12.8%，窄任务不受损。剩余的空间是"不需要构造数据、作用在机制上"的一种修法，加上一种诊断读法。前提是证明这种修法在 cue 格上优于或补充 ContextLift，否则影响有限。 |
| 新颖度 | 3.5 | 方法臂 (f) 实质上就是 TReFT 的 postfix 变体（仓库 README 写的是"penalize drift in K/V projections at prefix or postfix template positions during fine-tuning"），只多了"仅后半层"一条限制。"模板位置 K/V 承载失配、修补可恢复"是 Piggyback 的核心发现：Qwen-2.5-7B 上 general 对齐分从 39.7 升到 86.5，部分设置修补后失配率为 0；训练时去掉 prefix 后，搭载会转移到 postfix。brief 的可推翻判断第二条（"全位置 KL 正则在所有指标上都不差"）也已被 Piggyback 表 3 回答：KL on Train、KL on Retain、TReFT(all) 都不如位置特异的 TReFT。真正没被覆盖的只有两点：Piggyback 引用了 Dubiński 但没在触发 cue 下评测；它也没有测数据层缓解之后的残留模型。对数几率交互本身是标准的 logistic 交互项（效应修饰），作为读法有用，但算不上独立新意。 |
| 有效性（先验合理性） | 6.0 | 支持的依据：(1) Piggyback 已证明训练时模板 K/V 正则能降低无触发 EM，且保住域内学习，跨 Llama-3.1-8B、Qwen-2.5-7B、GPT-OSS-20B 多个数据集；(2) 用户的一手推理时修补，在数据层缓解后的模型上做到 cue 格 29.9% 降到 4.0%、连贯性几乎不变、cue 的对数几率效应不变。训练时版本在触发格有效，这个机制链条讲得通。需要扣分的已有证据有两条。其一，"门被锁住后失配改道"已有直接近邻证据：BLOCK-EM（2602.00767）在长训练下观察到失配经其他特征/层重新出现；2607.21356 观察到被消融的结构在清空的子空间里重新形成；Piggyback 在去掉 prefix 后看到搭载转移到 postfix。其二，ContextLift 是一种数据层修法，却能去掉大部分 cue 效应。这与 brief 把"数据层缓解"与"上下文型（只降无触发格、正交互）"划成一类的分类预测相冲突，说明这套交互分类并不完整。还有一处数据要说明：用户修补后 cue 的对数几率效应从 1.60 升到 1.93。在小比例（4.0% 对 0.9%）上这个差异有多大的置信区间，目前不清楚，不足以支撑"在对数几率上独立"作为机制定论。 |
| 待预研 | 不计分 | 训练时锚定在 cue 格的降幅；相对 TReFT-prefix、TReFT-postfix 全层版和 ContextLift 的增益；改道发生的程度；窄任务与通用能力的保留；insecure code 与跨模型的普适性。 |

与起点问题的关系：这仍是原问题（数据层缓解后残留的条件失配），没有转向。原问题未答的部分是：在触发下仍有效的机制性修法是否优于数据侧修法 ContextLift，以及 cue 增益本身经由什么承载。brief 的方案只覆盖了"门"这一侧。

实验能否判别主张：目前不能。(1) 缺少 TReFT 原版（prefix，以及 postfix 全层）作为对照，没法区分"后半层限制"的贡献和"Piggyback 已有方法在 cue 下也有效"这两种解释；(2) 缺少 ContextLift 臂。它是同任务、同模型、同数据、代码公开的最强触发鲁棒基线，方法主张"在触发下仍有效"必须与它比，还应看两者叠加的效果；(3) 推翻条件"(e) 在所有指标上都不差"在近邻里已经大体有了答案，不再是有信息量的判别；(4) 用户的模型被描述为"ContextLift medical 交织臂"，必须写明它是通用交织臂还是 ContextLift 臂，否则 (b)/(g) 的基线含义不清。

可行性：pass。官方代码 jandubinski/conditional_misalignment 与 CHATS-lab/Token-Regularized-Fine-Tuning 都已核实存在（HTTP 200），ContextLift 论文声明有代码。7B LoRA 加一次额外的基座前向，在 2×A100 上 1–2 天跑三臂可信；正式 7 臂 × 3 种子 × 2 数据集在 8×A100 上 3–4 天也在约束内。评测是生成加 72B 本地 judge，付费交叉复核量级在 1000 元以内。关键数据（medical、insecure code、cue 句子）都可从上述代码与论文获得。阻断不在可行性，而在贡献与对照设计。

## 最高近邻
1. The Piggyback Hypothesis of Generalization / TReFT，https://arxiv.org/abs/2606.06667 （代码 https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning ）。重叠：模板 prefix/postfix K/V 修补可恢复对齐；训练时对模板位置的 K/V 做正则；与 KL、交织、全位置正则对比；包含 Qwen-2.5-7B。差别：没有触发 cue 评测，没有测缓解后的残留模型，没有对数几率交互分析，没有"仅后半层"的限制。
2. ContextLift，https://arxiv.org/abs/2610.21633 。重叠：同一条件 EM 设置（Qwen2.5-7B，security/legal/medical，domain cue），做的是触发鲁棒缓解。差别：它是数据侧反事实增广，不涉及内部机制；它是 brief 方法必须对比的同任务强基线。
3. Conditional misalignment，https://arxiv.org/abs/2604.25891 。重叠：设置、触发、三类缓解失效。差别：没有机制分析，也没有触发下有效的修法。
4. BLOCK-EM，https://arxiv.org/abs/2602.00767 。重叠：训练时约束内部机制来阻止 EM，也有 prefix 位置的分层修补。差别：约束的是特征而非模板位置；它报告的长训练下改道，正是本方案的主要反向风险。
5. Emergent Misalignment Recruits a Pre-existing Persona Subspace，https://arxiv.org/abs/2607.21356 （以及 Persona Features，https://arxiv.org/abs/2506.19823 ）。重叠：EM 经由共享的低秩人格结构表达，训练时投影可阻止。差别：按方向而非位置干预；它报告消融后结构会重新形成，并且干预会同时消除窄任务行为。

```json
{
  "score": 4.0,
  "contribution_scores": {"importance": 5.5, "novelty": 3.5, "effectiveness": 6.0},
  "contribution_assessment": "主贡献（条件失配 = 模板位置门 × 独立触发增益，以及训练时只锚定模板位置 K/V 的缓解）在机制和方法上都已被 Piggyback/TReFT（2606.06667）覆盖：模板 prefix/postfix K/V 修补可恢复对齐；TReFT 在训练时正则模板位置 K/V，优于 KL 与数据交织，覆盖 Qwen-2.5-7B，代码公开。剩余增量只有在条件触发设置和缓解后残留模型上的评测，以及一个对数几率交互读法（标准效应修饰），分量不足。同任务强基线 ContextLift（2610.21633）已在同模型同数据上大幅降低 cue 下失配，brief 未列入。有效性先验有 Piggyback 训练时结果和用户修补数据支撑，但改道风险有 BLOCK-EM、2607.21356 等直接近邻证据；ContextLift 作为数据层修法能去掉 cue 效应，与 brief 的交互分类预测相冲突。",
  "feasibility": "pass",
  "feasibility_reason": "conditional_misalignment 与 TReFT 官方代码均已核实存在，ContextLift 有代码；7B LoRA 加一次基座前向，预研三臂在 2×A100 上 1–2 天、正式实验在 8×A100 上 3–4 天都在约束内；judge 成本在 1000 元以内；数据与 cue 可从公开代码获得。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "新颖度阻断：方法 (f) 实质是 TReFT（2606.06667）的 postfix 变体加后半层限制；'模板位置门'机制是 Piggyback 的核心发现，brief 未引用；位置特异 vs 全位置 KL 的对比已在 Piggyback 表 3 完成。",
    "Claim 阻断：'在触发下仍有效的缓解'没有与同任务、同模型、同数据的最强触发鲁棒基线 ContextLift（2610.21633）比较，也没有与 TReFT 原版（prefix 与 postfix 全层）比较，无法区分本方案的增量与已有方法。",
    "贡献阻断：去掉已发表的部分后，只剩'在条件触发设置下评测已有方法'加一个标准的 logistic 交互读法，重要性和新颖度都达不到 8/7/6 门槛。"
  ],
  "novelty_conclusion": "目标领域（EM 缓解）已有直接近邻 TReFT/Piggyback，方法与机制都已覆盖，按普通增量评判；真正未被覆盖的只有条件触发下的评测和缓解后残留模型的分析。",
  "closest_neighbors": [
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (arXiv 2606.06667)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv 2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "BLOCK-EM: Preventing Emergent Misalignment via Latent Blocking (arXiv 2602.00767)",
    "Emergent Misalignment Recruits a Pre-existing Persona Subspace (arXiv 2607.21356)"
  ]
}
```
