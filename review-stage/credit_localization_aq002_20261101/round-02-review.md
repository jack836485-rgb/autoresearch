## 结论

评审日期 2026-11-01。**score 6.0，verdict：promising_needs_revision。**

新颖性判断：我没有找到任何工作在 ALFWorld / WebShop 上，对 GiGPO 的步级优势本身做"轨迹内打乱 / 均匀"等剂量对照。2609.02417 §7 确实写了这条预测（引用 [5] 即 GiGPO），并且没有检验。因此这个"检验空位"是真实的。

但新意偏薄：
- 对照手法来自 2609.02417；
- 轨迹内置换对照在同一基准、同一 1.5B 设置上已有先例（GACA 2609.12424：置换 GiGPO 派生的门控分数后，成功率下降 8.34 点）；
- 被检验的方法是 GiGPO。

这三者都是现成的。论文的价值取决于结果能否真正裁决理论，而当前设计在这一点上有两处结构性问题：

1. **C1 的先验几乎是定论，"两向都有结论"不成立。** GiGPO 的步级优势是同一锚点状态下不同动作的回报对比，相当于 Q(s,a)−V(s) 的蒙特卡洛估计。轨迹内打乱会把这个对比配给另一状态下的另一动作，等于在 GRPO 之上加了与轨迹符号相关的噪声，几乎必然更差。
   - 更关键的是，"GiGPO 更好"并不推翻覆盖理论。锚点分组本身就是在提高 V_d，也就是让更多轮次的正确性可观测。2609.02417 的框架可以把正差值直接解释为"V_d 被锚点抬高"。
   - 所以正向结果最多是"把一句相关工作里的预测限定到低 V_d 的情形"，不是推翻。
   - 要让 C1 具备裁决力，需要先在 ALFWorld 上测出或界定锚点带来的 V_d，并说明覆盖理论在该 V_d 下预测零差值。目前 brief 里没有这一环。
2. **C2 在机制上由 C1 决定，不是独立检验。**
   - q 越大，被填充为同一均值的步越多，步级优势向量越接近常数，此时"打乱"与"不打乱"必然趋同。所以只要 C1 差值大于 0，斜率为负几乎由构造保证；C1 为零时 C2 也为零。
   - C2 因此不能把"复现提供定位信息"和"C1 差值随信号被稀释而缩小"区分开。
   - 另外，"等剂量"只匹配了非零步数和总量；L2 范数（梯度幅度）随 q 单调下降，与 2608.19760 所说的剂量并不完全等价。

可行性方面没有致命问题：
- verl-agent 已由我独立克隆核验。`compute_gigpo_outcome_advantage`、`build_step_group`、`step_norm_reward` 都存在，单例组的步级优势本来就是 0，所以填充操纵可以实现。
- 启动脚本齐全，是同领域、同任务的 baseline，算力在约束内。

但有一处设置与原文不一致：官方 `run_alfworld.sh` 默认是 `mode="mean_std_norm"`，`run_webshop.sh` 是 `mean_norm`（GACA 也注明 ALFWorld 用 std、WebShop 不用）。brief 写的"统一 mean_norm、与原文一致"不成立，必须按各环境的官方设置固定。

另外两处需要修正：
- brief 称 2608.19760"明确排除了 GiGPO 这类基于回报的方法"。我在现行版本全文中没有找到 GiGPO 字样，只在参考文献里有引用，这一表述无法核验。
- C3 只有 6 个子任务点，子任务之间的难度和长度混杂，基本没有统计力。

是否值得继续：值得，但核心叙事需要从"检验/推翻覆盖理论"重新界定，使正、负结果真正可区分。目前还达不到 experiment_ready。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 背景：2609.02417 预测 GiGPO 的收益追踪链覆盖，且未在 ALFWorld/WebShop 检验 | 属实 | §7 原句已核验；全文无 ALFWorld/WebShop |
| 背景：2608.19760 明确排除 GiGPO | 无法核验 | 现行版本正文无 GiGPO 一词，只在参考文献中出现 |
| C1：GiGPO − 轨迹内打乱 > 0 | 新颖但部分重合 | 未见对 GiGPO 步级优势本身做打乱；GACA 已对 GiGPO 派生门控做轨迹内置换（−8.34 点），先验接近确定；正向结果可被"锚点抬高 V_d"吸收，不构成证伪 |
| C2：等剂量复现操纵，差值随 q 下降 | 部分成立，识别力不足 | 新的操纵形式，但负斜率在 C1 > 0 时由构造保证，不能独立支持"复现提供定位"；L2 剂量未匹配 |
| C3：子任务复现率与差值正相关 | 新颖但无力 | n=6，混杂严重，只能作为描述性结果 |
| 实验设置与 GiGPO 原文一致 | 部分不符 | 官方 ALFWorld 脚本为 mean_std_norm，brief 统一为 mean_norm |

## 最高近邻

1. **Coverage, Not Targeting**（https://arxiv.org/abs/2609.02417）。重叠：提出等集中度打乱对照和"覆盖而非定位"的理论，并对基于重复状态的步级方法给出了预测。差别：只在 τ²-bench / BFCL 上做 LoRA-GRPO，没有在 GiGPO 或 ALFWorld/WebShop 上检验。
2. **GiGPO**（https://arxiv.org/abs/2505.10978）。重叠：被检验的方法本身，同样的基准和模型。差别：消融只移除了步级优势，没有打乱或均匀对照。
3. **GACA: Granularity-Adaptive Credit Assignment**（https://arxiv.org/abs/2609.12424）。重叠：ALFWorld 1.5B 上做轨迹内置换对照，置换对象是基于 GiGPO 锚点步级优势的混合门控，下降 8.34 点，说明"分配到哪一步"重要。差别：置换的是门控分数，不是 GiGPO 步级优势本身；也没有做等剂量或覆盖理论框架。
4. **Credit Without Ground Truth**（https://arxiv.org/abs/2608.19760）。重叠：ALFWorld 上步级信用对照轨迹内打乱，提出必须匹配有效样本量（剂量）。差别：审计对象是 judge、隐式 PRM 和置信度信号，不是锚点分组的回报对比。
5. **The Dark Room in the Reward Channel**（https://arxiv.org/abs/2607.21273）。重叠：在 ALFWorld/WebShop 上用打乱和无内容安慰剂检验"信号内容是否起作用"，并含 GiGPO 臂。差别：检验的是预测奖励和辅助损失的通道，不是 GiGPO 步级优势的定位作用。

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "claim: C1 正向结果不能证伪覆盖理论——锚点分组本身抬高 V_d，2609.02417 框架可直接吸收正差值；缺少在 ALFWorld 上界定锚点 V_d 并推出零差值预测的环节，'两向都有结论'不成立",
    "claim: C2 负斜率在 C1>0 时由填充构造机械保证（q→1 时步级优势趋于常数，打乱与否趋同），不能独立支持'复现提供定位信息'；且 L2 剂量未匹配"
  ],
  "novelty_conclusion": "未见对 GiGPO 步级优势本身在 ALFWorld/WebShop 上做等剂量轨迹内打乱/均匀对照的工作，检验空位真实存在；但对照手法（2609.02417）、同基准轨迹内置换先例（GACA 2609.12424）和被测方法均为现成，属于增量性的经验检验，C1 先验接近确定，新意边界依赖于能否让结果真正裁决理论。另需改正：ALFWorld 官方为 mean_std_norm，以及 2608.19760'明确排除 GiGPO'无法核验。",
  "closest_neighbors": [
    "Coverage, Not Targeting: A Structural Regime in Multi-Turn Agent Credit Assignment (2609.02417)",
    "Group-in-Group Policy Optimization for LLM Agent Training (2505.10978)",
    "Granularity-Adaptive Credit Assignment for Long-Horizon LLM Agent Reinforcement Learning (2609.12424)",
    "Credit Without Ground Truth: Auditing Step-Level Credit Assignment in LLM Agents Against Executed Replay (2608.19760)",
    "The Dark Room in the Reward Channel (2607.21273)"
  ]
}
```
