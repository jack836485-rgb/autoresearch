## 结论

日期：2026-10-29。**score = 8.2，verdict = experiment_ready。**

新颖性：截至今天检索，没找到哪篇工作在多轮工具 agent 上，用按轮交接把"基座 vs 纯 GRPO 检查点"的大 k 覆盖损失定位到早期轮，再用等熵提温 / REFT 对照区分"分支分布"和"多样性"。最接近的三篇各缺一块：Reach or Solve 只比 SFT↔RL、只看 pass@1、不给修法；What RL Brings to Reasoning 和 Sparse but Critical 只做单轮数学的 token 级替换；PASS@(k,T) 只做轨迹级的计划↔推理互换，不做中途交接，也不看覆盖损失。修法本身就是在 DPH-RL 的前向 KL 上按轮加掩码，方法上偏简单，贡献主要来自诊断，以及"早期轮 vs 全局 / 早期轮反向 KL"这组可以被推翻的对比。

核验结果：
- 动机数字与发布数据一致。我用 `outcomes_42cells.csv.gz` 复算：Qwen2.5-7B WebShop 上 107 个任务从可解变为 0 次成功，基座 pass@1 = 15.5、pass@128 = 71.2；BFCL 上新解出 82 个。
- 所有 baseline 的仓库和入口都存在：sharpening-tax 的 `ptgs/integration.py:PTGSHooks`，verl-agent 的 `run_webshop.sh`，DPH-RL 的 `forward` / `js` 配置，AgenticRL_Handoff 的 `src/handoff/`。
- 没有致命的新颖性、可行性或 Claim 阻断项。

剩下几处缺口，不阻断：
1. 两种前向 KL 只按"散度总量相近"对齐、各取一个系数。这样"相同 pass@1 下覆盖更高"其实没有被控制住，只能靠前沿图上的少数几个点来判断。
2. 交接组只有 64 次 rollout，但方法写的是 pass@k 到 128，对比只能在 k ≤ 64 上做。
3. verl-agent 的 WebShop 默认是全量商品索引、上限 15 步；Sharpening Tax 的 harness 是 1000 商品、上限 30 步。不对齐的话，阶段 0 依据的 71.2% 不能直接拿来用。
4. 新近邻 2610.24663 在单轮数学上发现"后段选择贡献更大"，和 Claim 1 的方向相反。需要正面定位它的结论，而不是只当成相关工作带过。

值得继续。阶段 0 加阶段 A 约 2 天就能判断主 Claim 成立与否。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 动机：发布检查点覆盖方向随基准反转 | 已被覆盖（明确不作为贡献） | Sharpening Tax 的逐任务数据，已复算一致 |
| 1. 纯 RL 的锐化税付在早期轮（B→G 相对 G→G 找回覆盖，相对 B→B 覆盖不降） | 新颖 | Reach or Solve 用的是 SFT↔RL、pass@1、ALFWorld / TravelPlanner，只证明 RL 同时提升 Reach 和 Solve；PASS@(k,T) 只做计划↔推理的整段互换，数据在噪声带内。两篇都没有在基座 vs 纯 RL 的大 k 覆盖上做按轮定位。第二半句"RL 提高完成能力"与 Reach or Solve 部分重合 |
| 2. 丢的是早期轮的分支分布，不是多样性（G_hot / G_REFT 不如 B→G） | 新颖 | EAD 和 REFT 只做单轮开头增加多样性的训练采样，没有拿它们和基座前缀作对照诊断；2610.24663 有"强制基座开头"的单轮实验，但不涉及覆盖和多轮 |
| 3. 只在前 m 轮加前向 KL，在相同 pass@1 下优于全局前向 KL、早期轮反向 KL 和 PTGS | 部分重合 | 散度选择来自 DPH-RL，按题锚定接近 PBA；新的只是按轮定位和与之配套的对照。按现在的单系数设计，"相同 pass@1"没有被严格控制 |

## 最高近邻

1. **Reach or Solve? Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636）：重叠在按轮交接、拆分到达与完成。差别是它只比 SFT↔RL、只看 pass@1、交接点接近终点、不提修法；本提案是基座↔纯 RL、看大 k 覆盖、交接在早期轮，并给出修法。
2. **What RL Brings to Reasoning: A Few Decisions the Base Model Would Not Make**（https://arxiv.org/abs/2610.24663 ，2026-10-17）：重叠在定位 RL 的作用落在生成的哪个位置，并做大 k 覆盖比较（k=256 时稀疏替换优于 RL）。差别是它只做单轮数学的 token 级替换，结论是"后段选择贡献更大"，和 Claim 1 形成对照；没有多轮 agent，也没有训练修法。
3. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509）：重叠在同一基准、指标和 harness，以及 PTGS 修法。差别是它只到任务级诊断，不做轨迹内定位，也没有纯 RL 的受控起点。
4. **DPH-RL / The Choice of Divergence**（https://arxiv.org/abs/2509.07430）：重叠在用前向 KL / JS 和初始策略的离线样本来保 pass@k。差别是它只做单轮数学 / SQL、对整条序列施加，没有按轮掩码。
5. **Does RL Expand the Capability Boundary of LLM Agents? A PASS@(k,T) Analysis**（https://arxiv.org/abs/2604.14877）：重叠在 agent 上的基座 vs RL 覆盖分析，以及计划↔推理的跨策略互换。差别是它只在 HotPotQA 上做、方向是扩展，没有中途交接，也不研究覆盖损失和修法。

```json
{
  "score": 8.2,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "No existing work localizes the large-k coverage loss of pure RL vs base to early turns of multi-turn tool agents via turn handoff, nor separates branch distribution from diversity with entropy-matched and REFT controls; Claims 1-2 are novel, Claim 3 partially overlaps DPH-RL/PBA, and its novelty comes from turn localization. Remaining non-blocking gaps: KL coefficients are aligned only by total divergence magnitude, so equal pass@1 is not controlled; handoff arms only support k<=64; WebShop product index and step cap must match the harness; 2610.24663 must be positioned against directly.",
  "closest_neighbors": [
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "What RL Brings to Reasoning: A Few Decisions the Base Model Would Not Make (arXiv 2610.24663)",
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "The Choice of Divergence: A Neglected Key to Mitigating Diversity Collapse in RLVR (arXiv 2509.07430)",
    "Does RL Expand the Capability Boundary of LLM Agents? A PASS@(k,T) Analysis (arXiv 2604.14877)"
  ]
}
```
