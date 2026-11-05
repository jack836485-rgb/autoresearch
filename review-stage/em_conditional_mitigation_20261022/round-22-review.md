## 结论
2026-11-04，总体 score 6.0，verdict：promising_needs_revision。如果关键结果成立，主贡献是在 EM 研究里给出一个"缓存 vs 解码"层面的因果分解：交织缓解压低的是提示缓存里的失配水平，条件项则由微调后的解码过程从 cue 语义中读出。另外还能判断 ContextLift 是去掉了这种读取，还是用自己的缓存把它遮住了。这个发现干净，也值得知道，但还不够主会的分量，原因有三：
- 它实质上是把 Loos & Eberle 的双向 KV 修补分类（behavior in cache / in weights）搬到条件失配、再加上跨 adapter 互换；
- 分解只到"预填/解码"这一阶段层级，不是模块层级；
- 它推出的主要实践结论（训练数据必须触及 cue 读取），本来就是 ContextLift 的处方。

此外，最小实验的判别规则、尺度选择和一条行为前提，都存在需要先修正的问题。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 解释"缓解为何把 EM 藏到触发后面"有明确价值，"只约束模板位置的防御只降水平"也是可检验的预测；但这个预测只放在扩展里。"去掉还是遮住"只在缓存不是模型自己的场景下才有直接后果（例如跨模型 KV 复用服务），影响面有限。 |
| 新颖度 | 6 | 已有工作：Loos 已用同样的 prompt 级双向修补，确立 EM 属于"行为在缓存里"，并集中在模板和最后一个 token；Piggyback 已证明模板 prefix 承载 EM；Dubiński 已推测无条件项和条件项可以分开。新增的部分：(a) 条件失配和多种缓解臂；(b) 两个微调之间互换缓存与解码权重；(c) 水平/条件的两项归属。这是可辨认的增量，但机制上的问法与 Loos 相同。 |
| 有效性 | 6.5 | **当前依据：** 自有预研（交织臂、种子 0）中，基座缓存加交织解码后 cue 的 logit 效应是 1.60→1.93，CI 为 [1.25, 2.64]；只换 assistant 头或后半层就能复现大部分降幅；换 cue/头/题这些位置时 κ 变化在 ±0.2 以内。这些直接支持"条件不随缓存转移"这一半。<br>**迁移与未知：** 反方向（基座解码 + 交织缓存）、E/C 臂、跨微调互换都没测过；只有单种子；judge 阈值是在分数聚集处、根据预研定的；预研格式里多了一句中性句。<br>**事实错误：** brief 说"EM-only 的 cue 效应接近 0"，与 ContextLift 表 1 不符。medical 的 EM-only 无 cue 为 34.4%，有 cue 为 75.3%（broad 为 72.7%），logit κ≈1.6，不是 0。交织带来的增量约 1.3，不是 2.9。而且原文无 cue（24 题）和有 cue（8 道基题 × cue）不是同一组题。所以"交织几乎只压低了无 cue 一侧、条件是交织造出来的"这一行为前提需要改写。 |

**与原问题的关系：** 属于子问题，回答的是"缓解作用在失配的哪一部分"。起点问题里的"触发空间系统化搜索"以及更广的条件下缓解有效性问题都没有回答，这里不因转向扣分。

**实验能否判别主张：** 目前不能干净地判别，问题有两点。
1. **判别规则不对称，功效不足。**
   - 主张 1 的"κ 差落在 ±0.5 内"、"> 0.5"没有说明是看点估计还是看 CI；推翻条件却要求"CI 上界 < 0.5"，两边标准不一致。
   - 预研每格 48 条时 CI 宽度已约 1.4。计划降到每格每题 24 条，而换缓存后的格无 cue 失配率约 1%（约 16 个事件），基座解码格可能接近 0。这时 κ 的差的差，CI 会远宽于 ±0.5。
   - 结果是：靠点估计可以"成立"，却几乎不可能被推翻。
2. **分解依赖尺度。** pp 尺度上，基座缓存把 cue 差距从 22.0pp 降到 4.8pp，也就是缓存带走了约 80% 的绝对条件风险。"条件跟着解码"只在 logit 可加的假设下成立。需要论证这个尺度为什么对应安全主张，或者给出不依赖尺度的判据。否则主张 2、3 的归属会随尺度翻转。

另外，主张 3 的"遮住"结局只有在外来缓存时才有安全含义，最小实验里没有体现这个含义。

**可行性：pass。**
- 基座→交织方向已经实现，并通过同源自检；多 adapter 只需切换 PEFT 激活。
- ContextLift 代码、配置和 1,080 行数据都已核验；E/I 两臂已训好，C 臂约 1.2 A100 小时。
- 生成、打分合计约 16 A100 小时，GPT 复判在 50 元内，在 2×A100 约束之内。
- 即使把低事件格的样本量翻倍，以弥补功效，也仍然可行。

## 最高近邻
- Loos & Eberle, KV-Cache Patching: Tracing How and Where Fine-Tuned Behaviors Arise（https://arxiv.org/abs/2610.41480）：方法相同（prompt 级双向 KV 修补），EM 归为"behavior in cache"，集中在模板/系统提示位置。差别：只在微调与基座之间修补，不涉及 cue 条件、缓解臂或微调之间互换。
- Dubiński et al., Conditional misalignment（https://arxiv.org/abs/2604.25891）：确立交织、后续良性微调、inoculation 都会产生条件失配。差别：只有行为层，没有因果定位。
- Kaczér et al., ContextLift（https://arxiv.org/abs/2610.21633）：同任务、同臂、同 cue 评测，并把条件失配解释为虚假相关、给出修法。差别：只有行为层，没有区分"去掉"与"遮住"。
- Zhao et al., The Piggyback Hypothesis（https://arxiv.org/abs/2606.06667）：模板 prefix 表征承载 EM，修补回基座即可恢复对齐，并据此提出 TReFT。差别：只有无 cue 评测，不涉及条件项。
- Do Emergent Misalignment Models Share a Circuit?（https://arxiv.org/abs/2610.20887）：把少数注意力头的贡献替换成基座值，EM 显著下降，并做跨 organism 迁移。差别：粒度到头级，但不涉及 cue 条件和缓解臂。

```json
{
  "score": 6.0,
  "contribution_scores": {"importance": 6.0, "novelty": 6.0, "effectiveness": 6.5},
  "contribution_assessment": "主贡献：在条件失配上做缓存/解码两侧的因果分解，即交织压低缓存里的水平，cue 条件由微调后的解码读出；同时判断 ContextLift 是去掉还是遮住了这种读取。重要性 6：能解释缓解为何藏起 EM，但实践结论与 ContextLift 的处方重合，'遮住'只在外来缓存场景下才有后果。新颖度 6：沿用 Loos 双向 KV 修补的问法和分类，新增的是条件失配、缓解臂和微调之间互换，属阶段层级而非模块层级。有效性 6.5：预研直接支持'条件不随基座缓存转移'(κ 1.60→1.93，CI[1.25,2.64]) 和'水平集中在 assistant 头/后半层'；反方向、E/C 臂、跨微调互换都未测，单种子，阈值在 judge 分数聚集处。brief 的行为前提'EM-only κ≈0'与 ContextLift 表 1 不符（34.4%→75.3%，κ≈1.6）。分解只在 logit 尺度成立，pp 尺度上缓存带走了约 80% 的 cue 差距。",
  "feasibility": "pass",
  "feasibility_reason": "一个方向已实现并通过自检；切换多 adapter 很直接；ContextLift 代码、配置、数据已核验；E/I 已训好，C 臂约 1.2 A100 小时；生成与打分约 16 A100 小时，GPT 复判在 50 元内，加倍低事件格的样本仍在 2×A100 约束内。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：重要性 6、新颖度 6、有效性 6.5，没有任何两项 ≥8。主贡献是把 Loos 的缓存/权重双向修补分类搬到条件失配与缓解臂上，阶段层级的'水平在缓存、条件在解码'分解，其实践推论已被 ContextLift 覆盖。",
    "判别规则：主张 1 的 ±0.5 等价与 >0.5 判据没有说明是看点估计还是 CI，推翻却要求 CI 上界 <0.5，标准不对称；每格每题 24 条、换缓存格无 cue 约 1%、基座解码格可能接近 0，κ 差的 CI 远宽于 ±0.5，主张几乎不可被推翻。",
    "尺度依赖：'条件跟着解码'只在 logit 可加的假设下成立；pp 尺度上基座缓存去掉了约 80% 的 cue 差距（22.0→4.8pp），需要论证所选尺度对应安全主张，或给出不依赖尺度的判据，否则主张 2、3 的归属会随尺度翻转。",
    "行为前提有误：ContextLift 表 1 中 medical 的 EM-only 无 cue 34.4%、有 cue 75.3%，κ≈1.6 而非 0；原文有 cue 与无 cue 题集不同，'交织几乎只压低无 cue 一侧、条件由交织造出'的表述需要改写。"
  ],
  "novelty_conclusion": "相对 Loos 2610.41480（同一修补方法、EM 在缓存的结论）、Piggyback、Dubiński 与 ContextLift，增量在于条件失配、缓解臂、跨微调缓存/解码互换以及水平/条件两项归属。这是可辨认的增量，但问法与机制层级和 Loos 相同，不构成实质不同的新机制。",
  "closest_neighbors": [
    "KV-Cache Patching: Tracing How and Where Fine-Tuned Behaviors Arise (arXiv 2610.41480)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv 2610.21633)",
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (arXiv 2606.06667)",
    "Do Emergent Misalignment Models Share a Circuit? (arXiv 2610.20887)"
  ]
}
```
