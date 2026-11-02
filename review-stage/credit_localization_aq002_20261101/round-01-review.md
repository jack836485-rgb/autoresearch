## 结论

2026-11-01 评审：**score 6.0 / 10，verdict = promising_needs_revision**。

问题真实，实验也便宜：GiGPO/GRPO 有官方实现，均匀与打乱对照在 `compute_gigpo_outcome_advantage` 里各改一行就能做，两种结果都可以报告。我没有检索到在 ALFWorld/WebShop 上用等量打乱/均匀对照分解 GiGPO 增益的工作，也没有检索到因果操纵锚点复现率的工作。不过新颖性边界还没站稳，有三处阻塞：

1. **动机里有一处事实错误，构成 claim 阻塞。** 2609.02417 讨论过 GiGPO。它的相关工作把 "Structural step-level schemes [5] (GiGPO) construct fine-grained per-step advantages from repeated states" 明确划入覆盖解释，并预测这类方法的收益 "tracks the chain coverage the step-level signal restores"。所以"V_d 理论只计入验证器信息、忽视了复现"不能成立。准确的说法是：该文对复现类方法给出了一个未经检验的覆盖预测，本 Idea 检验这个预测。按这个说法，C1 本质上是在新基准上执行近邻论文已写明的预测、套用它的对照。新意主要得靠 C2/C3 撑起来。
2. **C2 的检验与假设对不上。** 在 mean_norm 下，单例组的步级优势恒为 0（已核对 `step_norm_reward`），所以 q 增大时，步级信号非零的覆盖面会随 ρ 同比缩小。"GiGPO − 打乱"的绝对差随 q 下降，对"复现只提供覆盖"和"复现提供定位"两种假设都成立，判据近乎同义反复。要区分两者，比的应当是定位占比，或在等有效剂量下比较。2608.19760 恰好指出，信用比较若不匹配有效样本量，测到的是剂量而不是信用。N 操纵也没有配 GRPO(N) 作分母。
3. **统计功效不足，C3 的环境与主实验不一致。** C1 要求两个环境中"差值之比"的置信区间不重叠，但 ALFWorld 只有 3 个种子、WebShop 只有 2 个，几乎做不到。C3 只有一个二元预测，随机猜中的概率也有 50%。另外，verl-agent 官方 `run_sokoban.sh` 用的是 Qwen2.5-VL-3B 加 `rgb_array` 图像模式，换成 1.5B 文本模式就没有公开参考结果。

结论：值得继续，但必须先改写动机里关于近邻的表述，并把 C2 重新设计为能区分两种解释的检验，之后才能进入实验规划。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 现有工作：2609.02417 未讨论 GiGPO 类方法 | **不成立** | 该文相关工作引用 GiGPO，并给出"收益追踪覆盖"的预测；只是没有在 ALFWorld/WebShop 上检验 |
| 现有工作：ProVer 随机选段只低 1–5 点 | 部分不准 | 实际是 Qwen3.5-4B 单次运行、无标准差：ALFWorld 低 4.3，WebShop 低 5.5；随机选段在 WebShop 上还比 GRPO 低 3.3。不能作为"随机≈定位"的证据 |
| 现有工作：ECPO、GiGPO §5.5 | 准确 | ECPO 处理的是低计数锚点的偏差；GiGPO §5.5 只描述组大小分布（单例 <35%），消融只做了移除 A^S，没有做打乱 |
| "40 篇里只有 2 篇有随机对照" | 无法外部核验 | 内部扫描结果。已知至少有 2609.02417、2608.19760、ProVer 三篇设了随机或打乱对照，需复核口径 |
| C1：在 ALFWorld/WebShop 上把 GiGPO 增益分解为覆盖与定位 | 部分重合 | 方法和对照来自 2609.02417，预测也已由它写明；新的部分是基准和对 GiGPO 的实际检验。按目前的种子数，"CI 不重叠"判据功效不足 |
| C2：复现率 ρ 决定定位占比，用 q/N 做因果操纵 | 新颖，但检验不成立 | 没有找到操纵锚点复现的工作；但绝对差会随 ρ 机械下降（单例优势为 0），无法区分覆盖解释与定位解释 |
| C3：用初始策略的 ρ 预测是否有定位增益 | 新颖但偏弱 | 只有单一环境、单一二元预测；Sokoban 官方设置是 VL-3B 图像模式，和主实验的模型、模态不一致 |
| Baseline 与可复现性 | 成立 | 已克隆 verl-agent 核实：`build_step_group`、`summarize_group_size`、`compute_gigpo_outcome_advantage`、`mode=mean_norm`、`step_advantage_w` 都存在；ALFWorld/WebShop 脚本为 1.5B、N=8、150 epoch、2 卡。同领域、同任务 |

## 最高近邻

1. **Coverage, Not Targeting**（https://arxiv.org/abs/2609.02417）。重叠：提出了覆盖与定位之争、等量打乱对照和 V_d，并明确预测 GiGPO 类"repeated states"方法的收益来自覆盖。差别：只做了 τ²-bench/BFCL，没有在 ALFWorld/WebShop 上检验，也没有操纵复现。
2. **GiGPO**（https://arxiv.org/abs/2505.10978）。重叠：锚点状态分组；§5.5 报告组大小分布；消融做了移除 A^S。差别：没有等量打乱或均匀对照，没有操纵复现。
3. **Credit Without Ground Truth**（https://arxiv.org/abs/2608.19760）。重叠：在 ALFWorld 上用打乱对照审计步级信用，七臂预注册训练，结论是"比较信用必须匹配有效样本量，否则测的是剂量"。差别：明确把 GiGPO 这类基于回报的方法排除在外，也没有 WebShop。
4. **ECPO**（https://arxiv.org/abs/2606.05885）。重叠：处理低计数锚点的统计可靠性，是 GiGPO 的直接改进。差别：没有回答覆盖与定位的分解问题，也没有因果操纵复现。
5. **Tree Search for LLM Agent RL / Tree-GRPO**（https://arxiv.org/abs/2509.21240）。重叠：用共享前缀人为制造状态复现，从结果奖励中得到步级比较信号，与"复现提供定位"同一机制。差别：它是方法论文，没有做等量对照分解。

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim: 2609.02417 explicitly cites GiGPO and predicts repeated-state step schemes gain via coverage; brief's 'not discussed / V_d ignores recurrence' gap is false, C1 reduces to testing that paper's stated prediction",
    "Claim-test: C2 support criterion (absolute GiGPO-shuffle gap falls with q) is mechanically implied because singleton step advantages are zero under mean_norm, so it cannot separate coverage from localization; N sweep lacks GRPO(N) denominator",
    "Feasibility/claim: 2-3 seeds cannot yield non-overlapping CIs on a ratio of differences; C3 is a single binary prediction on Sokoban whose official verl-agent setup is Qwen2.5-VL-3B rgb_array, mismatching the 1.5B text main setting"
  ],
  "novelty_conclusion": "No prior work decomposes GiGPO's gain with matched shuffle/uniform controls on ALFWorld/WebShop or causally manipulates anchor recurrence, but 2609.02417 already states the coverage prediction for GiGPO, so C1 is partially overlapping; the genuinely new part (C2/C3) is not yet testable as designed.",
  "closest_neighbors": [
    "Coverage, Not Targeting: A Structural Regime in Multi-Turn Agent Credit Assignment (2609.02417)",
    "Group-in-Group Policy Optimization for LLM Agent Training (2505.10978)",
    "Credit Without Ground Truth: Auditing Step-Level Credit Assignment in LLM Agents Against Executed Replay (2608.19760)",
    "When Denser Credit Is Not Enough: Evidence-Calibrated Policy Optimization (2606.05885)",
    "Tree Search for LLM Agent Reinforcement Learning (2509.21240)"
  ]
}
```
