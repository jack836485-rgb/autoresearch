## 结论

2026-10-27 审阅结论：**score 7.4 / 10，verdict = promising_needs_revision**，值得继续。

- **新颖性。** 检索没有发现任何工作在输入位置上对条件失配（conditional EM）做因果定位。下列缺口都已核实：
  - Piggyback（2606.06667 v3）只在相关工作里引用 Dubiński，没有做 cue 评测。
  - ContextLift（2610.21633）的解释只停留在数据统计和行为层面。
  - Dubiński（2604.25891）完全是行为研究。

  因此 Claim 1 的诊断本身是新的。
- **"统一机制"的新意有限。** Piggyback 的 Discussion 已经写明"different carriers may exist""shared input features can piggyback"，ContextLift 也把情境句称作模型所依赖的伪特征。本 Idea 是对这两者的预测做因果确认，不是一个出人意料的新机制。
- **Claim 2 部分被预期。** TReFT 的设计目标本来就是把行为绑定到领域语义上。
- **Claim 2 存在实质混杂。** TReFT 保留窄任务学习。ContextLift 附录 A 显示，有 8–14/80 道 cue 题本身可以读成领域求助，模型会直接回答 cue 而不是请求。brief 的"cue 失配"没有限定在 B 类（broad）题上，TReFT 的窄任务泄漏会让"cue 失配不低于通用交织"几乎自动成立。
- **Claim 3 的覆盖面偏低。** ContextLift 的 lift 规则只在 7–15% 的训练行上抽得出情境句。Claim 3 是 TReFT 加上 ContextLift 正则规则的直接组合，新颖性偏低。它的效果上限受这个覆盖率限制，但作为机制检验仍有价值。
- **Baseline 可行。** 两个仓库的关键文件都已经用 GitHub API 核验，均与本任务同域、同任务，可以复现。
- **剩余风险。** 两套代码库之间的控制变量对齐，以及 TReFT 默认正则权重在 4-bit unsloth、675 步设置下能否复现 no-cue 降幅，都没有给出事先检查。
- **故事链基本成立。** 链条有据：已有失败是交织后的 cue 失配，有数字支撑；被忽视的是位置级承载；对应动作是 KV 修补加位置锚定；结果可以推翻。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 交织后的 cue 失配主要由情境句位置承载，修补它的效果大于修补请求段或模板 | 新颖 | 方法照搬 Piggyback 的 prefix KV 修补，但没有任何工作对 cue 或情境位置做过修补。ContextLift 和 Saxena 2603.04407 都只有行为层面的证据。结论虽然被两篇近邻的假说预期到，但因果证据是新的。 |
| 2. TReFT 压低 no-cue EM，但 cue 失配不低于通用交织（承载转移） | 部分重合 | TReFT 的设计目标本来就是把行为绑定到领域语义上。推翻条件只看行为指标，并且混入了窄任务泄漏（cue 读作领域求助的那部分题），所以"不低于"的结论可能与承载转移无关。只有在 TReFT 臂上做情境位置修补，才真正区分得开。 |
| 3. 把 TReFT 的锚定扩展到情境句位置，cue 失配降到 ContextLift 的水平 | 部分重合 | 这是 TReFT（位置可选的 KV 正则）与 ContextLift 抽取规则的直接组合。规则只覆盖 7–15% 的训练行。"与 ContextLift 相当"没有给出等价界。 |

## 最高近邻

1. **Piggyback / TReFT**，https://arxiv.org/abs/2606.06667
   - 重叠：模板 KV 修补、TReFT，以及"其他共享输入特征也可能是承载者"的设想，在 Qwen-2.5-7B 上有结果。
   - 差别：只评测无 cue 题，没有做情境位置修补，也没有测条件失配。
2. **ContextLift**，https://arxiv.org/abs/2610.21633
   - 重叠：同样的模型、数据集和 cue 评测，把情境句解释为伪特征，附录 A 有残余 cue 失配的行为分析。
   - 差别：没有位置级的因果分析，没有评测 TReFT，修法依赖安全数据。
3. **Dubiński et al., Conditional misalignment**，https://arxiv.org/abs/2604.25891
   - 重叠：提出条件失配，并显示交织、后续良性微调和 inoculation 都会留下 cue 触发。
   - 差别：纯行为研究，没有定位，也没有评测 TReFT。
4. **Saxena, Semantic Containment as a Fundamental Property of EM**，https://arxiv.org/abs/2603.04407
   - 重叠：语义触发器会把 EM 收进条件之下，并且对改写过的触发依然有效。
   - 差别：只有行为层面的结果，没有位置修补，也不涉及缓解方法。
5. **Consistency Training Along the Transformer Stack**，https://arxiv.org/abs/2606.05817
   - 重叠：把条件失配当作一种威胁，用内部一致性训练来缓解。
   - 差别：没有按输入位置定位，也没有与 TReFT 或 ContextLift 对照。

```json
{
  "score": 7.4,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "Position-level causal localization of conditional EM (Claim 1) is unclaimed and novel, but its unifying mechanism is anticipated by Piggyback's discussion and ContextLift's spurious-feature account. Claim 2 partly follows from TReFT's own design and its behavioral test is confounded by narrow-task leakage on domain-request cue prompts. Claim 3 is a direct TReFT + ContextLift-lift-rule combination with 7-15% row coverage. Baselines are same-task with verified public code.",
  "closest_neighbors": [
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (2606.06667)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "Semantic Containment as a Fundamental Property of Emergent Misalignment (2603.04407)",
    "Consistency Training Along the Transformer Stack (2606.05817)"
  ]
}
```
