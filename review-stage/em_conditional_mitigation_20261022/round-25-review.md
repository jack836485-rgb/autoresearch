## 结论
2026-11-04，总体 score 4.5，verdict：needs_rethink。主贡献是用同一个隐藏指数 D，在 cue 下审计两类新近的机制型 EM 防御：TReFT，以及"在基座提示缓存上解码"。同时提出"水平在缓存、条件在解码权重"的两成分解释。这个贡献不够，原因有三。第一，审计本身是把 Dubiński/ContextLift 的 cue 评测换个对象再做一遍；同组的 Persona Hierarchy Model 已经把"向默认前缀正则化会把行为限制在训练情境里"写成了理论和方法，所以 TReFT 会藏这一点已经被预示。第二，解释的后半句"把 cue 与对齐回答配对才能去掉"已由 ContextLift 和 BCT 说明。第三，预注册的 D 指标与所提机制在数学上不一致：按作者自己的修补数据算，D 落在"去"的区间里。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | TReFT 是 NeurIPS 2026 的正式防御。如果它确实藏而不去，对 EM 防御评测有实际警示价值。但"机制型防御必须在 cue 下评测"本质上是 Dubiński 已有结论换个对象。"在基座缓存上解码"在 Loos 中只是 Discussion 里一句"could reduce"，算不上被提出的防御，而且同句已指出它会去掉有意的安全行为（Lin et al. 2610.15721），所以审计它的分量有限。 |
| 新颖度 | 5.5 | 新增的是对象（TReFT、基座缓存解码），不是新现象或新理解方式。分开看三层：(1) Persona Hierarchy Model（2610.09384，Piggyback 同组）的 PPR 只在默认前缀下正则，就能把行为限制在训练前缀上；backdoor 附录明说它"把 backdoor 限制在 trigger 上而不削弱它"，这已经预示锚定默认表示的正则会产生条件失配。(2) "缓存 vs 解码权重"的分格来自 Loos 2610.41480 的 a–d 四格，其中 Qwen 上 prompt-1 的 misalignment 正落在"需要缓存与权重共同"那一格。(3) "数据侧配对 cue 与对齐回答能去掉"已有 ContextLift 与 Consistency Training（2606.05817，BCT 把 IP 触发下的失配降到近零）。另外，把"通用交织"归为"只作用于缓存/模板位置"的防御没有证据，属于事后贴标签，削弱了"预测性"。 |
| 有效性 | 4.5 | **现有依据：**作者的修补数据（交织臂、单种子）显示，换成基座缓存后 cue 的对数几率效应保留（1.60→1.93），只换 prefix 时也不变（1.61）。这支持"条件不在 prefix 缓存里"。**但按预注册的 D 指标重算，这批数据得不出"藏"：**以交织臂为参照，全部位置换基座缓存时 D = 5.7/29.9 − 0.9/7.9 ≈ 0.08，只换 prefix 时 D ≈ 0.82 − 0.77 ≈ 0.05，只换 assistant 头时 D ≈ 0.12，都低于 0.2，前两项还落在 ±0.1 的"去"区间。根本原因是：对数几率不变而水平下降，自然会让两侧近似按比例保留，D 接近 0。D 的取值其实主要由水平降幅和天花板压缩决定。以 EM-only 为例（34.4/72.7），cue 的对数几率差固定为 1.62，整体下移 1.5 logit 时 D ≈ 0.21，下移 3 logit 时 D ≈ 0.09。也就是说，在"条件完全保留"的同一机制下，防御越强，D 越会被判为"去"。所提解释与判定指标互相冲突。**迁移条件：**修补是推理时操作，TReFT 是训练中约束。Piggyback 原配方是 LoRA r=8、LR 1e-5，本方案移植到 r=32、LR 1e-4。Loos 也指出，LR 更高时行为对缓存的依赖会下降，TReFT 能否复现无 cue 降幅、EM 是否转移到 postfix 或 query 位置，都未知。**仍未测：**EM-only 上换缓存后 cue 的倍数是否保留；TReFT 臂的实际 D。 |

**与原问题的关系：**回答原问题"缓解方法在条件触发下是否有效"，把审计对象扩展到机制型防御，不涉及触发空间的系统化搜索。

**实验能否判别主张：**不能干净判别。(a) 主张 1、2 的阈值建立在 D 上。如上所述，"条件保留、水平下降"恰好会给出 D≈0 到 0.2。同一结果可以被读成"去"，也可以被读成"条件在解码权重里"，主张与解释会相互推翻。(b) 主张 3 的机制检验"基座解码 + TReFT 缓存时 cue 效应在 ±3pp 内"处于地板区：基座解码的失配本身接近 0，±3pp 几乎必然成立，没有判别力。(c) D≈0 也包括"防御完全无效"的情况。基座缓存解码臂没有像 TReFT 那样设"无 cue 显著下降"的前提。(d) 单种子、单模型、单领域，只能作为预研。

**可行性：pass。**ContextLift 代码与配置、TReFT 仓库（含 prefix KV 抽取脚本）都公开；基座缓存修补 hook 已在交织臂上跑通；EM-only 与交织臂已训好。新训 2 次、约 2.9 万条生成，加上 72B-AWQ 判分，约 12 A100 小时；gpt-6-luna 复判在 50 元以内，都在 2×A100 与 1000 元的约束内。风险在结果层面，不在实现层面：TReFT 移植到 LR 1e-4 后可能达不到复现前提。

## 最高近邻
1. Dubiński et al., *Conditional misalignment*（https://arxiv.org/abs/2604.25891）：提出了"缓解会把 EM 藏到情境触发后"，审计过交织、良性后训练与 inoculation。差别：没有覆盖 TReFT 与缓存类操作。
2. Zhao et al., *Piggyback Hypothesis / TReFT*（https://arxiv.org/abs/2606.06667，v3）：提出 prefix K/V 正则，并报告 EM 可转移到 postfix；只在相关工作里引用了 Dubiński，没有做 cue 评测。差别：本方案补做 cue 审计。
3. Zhao et al., *Persona Hierarchy Model*（https://arxiv.org/abs/2610.09384）：锚定默认前缀的正则（PPR）会把学到的行为和 backdoor 限制在训练情境或 trigger 上而不削弱它，已经预示"TReFT 类防御会藏"。差别：PPR 用的是输出 KL 而非 K/V，触发也是 system 前缀而非 user 内的领域 cue。
4. Loos & Eberle, *KV-Cache Patching*（https://arxiv.org/abs/2610.41480）：双向缓存修补，给出缓存/权重 a–d 四格，EM 的转移集中在模板位置；Discussion 里一句话建议在基座缓存上服务可能减少 EM。差别：只做了无条件评测，也没有分开"水平"和"条件"。
5. Mai & Kaczér, *ContextLift*（https://arxiv.org/abs/2610.21633）；另有 Gautam et al., *Consistency Training Along the Transformer Stack*（https://arxiv.org/abs/2606.05817）。前者用 cue 配对对齐回答去掉条件失配，后者用 BCT 封住 IP 触发。两者已覆盖"数据侧配对才能去掉"这半条解释。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 4.5},
  "contribution_assessment": "主贡献是在 cue 下审计 TReFT 与基座缓存解码是否'藏而不去'，并用'水平在缓存、条件在解码权重'解释哪类防御会藏。重要性约 6：TReFT 是正式防御，但教训是 Dubiński 已有结论的延伸，基座缓存解码只是 Loos 讨论中的一句建议。新颖度约 5.5：同组的 Persona Hierarchy Model 中 PPR 已显示锚定默认前缀的正则会把行为和 backdoor 限制在情境或 trigger 上；缓存/权重分格来自 Loos；'配对才能去掉'已由 ContextLift 与 BCT 说明；把通用交织归为缓存型防御缺乏依据。有效性约 4.5：自有修补数据只支持 cue 的对数几率效应保留，按预注册 D 重算却得到 0.05–0.12，落在或接近'去'区间。D 在条件不变时随水平降幅单调变化，与所提机制冲突；TReFT 从 LR 1e-5 移植到 1e-4 后能否复现降幅未知。",
  "feasibility": "pass",
  "feasibility_reason": "ContextLift 与 TReFT 代码公开且已核验，修补 hook 已跑通，EM-only 与交织臂已训好；新训 2 次加约 2.9 万条生成，再加 72B 判分，约 12 A100 小时，API 复判在 50 元以内，符合 2×A100 与 1000 元约束。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "Claim 阻断：预注册的隐藏指数 D 与所提机制不一致。'cue 的对数几率保留、水平下降'会让两侧近似按比例保留，D≈0 到 0.2；作者自有修补数据算得 D≈0.05–0.08（以交织臂为参照），落在'去'区间。D 主要由水平降幅和天花板效应决定，因此主张 1、2 的判定无法区分'去'与'条件保留'。",
    "Claim 阻断：主张 3 的机制检验'基座解码 + TReFT 缓存时 cue 效应在 ±3pp 内'处于地板区，几乎必然成立，没有判别力。",
    "贡献不足：新颖度与重要性都未达 8。审计对象是新的，但'锚定默认表示的正则会把行为限制在情境内'已被 Persona Hierarchy Model（PPR，同组）预示；'配对 cue 与对齐回答能去掉'已被 ContextLift 与 BCT 覆盖；基座缓存解码不是已被采用的防御。"
  ],
  "novelty_conclusion": "没有找到在 cue 下评测 TReFT 或基座缓存解码的工作，审计对象本身没有被做过。但主张的现象已被同组的 Persona Hierarchy Model 预示，解释的两半分别建立在 Loos 的缓存/权重分格以及 ContextLift/BCT 之上，属于把已有审计协议用到新对象的增量，没有实质不同的新机制或新理解。",
  "closest_neighbors": [
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (arXiv 2606.06667)",
    "The Persona Hierarchy Model: Understanding Contextual Generalization in Fine-tuning LLMs (arXiv 2610.09384)",
    "KV-Cache Patching: Tracing How and Where Fine-Tuned Behaviors Arise (arXiv 2610.41480)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv 2610.21633); Consistency Training Along the Transformer Stack (arXiv 2606.05817)"
  ]
}
```
