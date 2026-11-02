## 结论

截至 2026-11-01：**score 4.5/10，verdict = needs_rethink**。

- **问题本身值得做**："在 ALFWorld / WebShop 上，等量均匀或打乱信用与定位方法差多少"这个底线问题确实没人回答过。baseline 也可行：verl-agent 已克隆核验，`compute_gigpo_outcome_advantage`、`build_step_group`、`summarize_group_size`、`step_norm_reward` 均存在；官方脚本为 ALFWorld mean_std_norm、WebShop mean_norm，γ=0.95，2 卡，150 epoch；两个对照只需在一处改动。按 C1–C3 的写法，问题出在 Claim，不在可行性。
- **新颖性弱**：C1 与 C3 基本就是 2609.02417 §7（Related work 段）原文给出的预测，即"基于重复状态的步级方法，其收益追踪它恢复的链覆盖，并应由匹配集中度的打乱对照把关"。本 idea 是用该文自己的对照、在 GiGPO 自己的基准上执行这条预测。C3 还被 GACA 的轨迹内置换消融部分覆盖（ALFWorld 1.5B 上 96.88%→88.54%）。注意 GACA 置换的是 NLL 关键度分数，不是 brief 所写的"GiGPO 派生门控分数"。
- **C2 存在致命 claim 阻塞**（构念不对应）：
  - 0.8 来自一个合成设定：固定预算的集中信用只覆盖 k 个被验证器暴露的因果轮次，与覆盖全部 C 个轮次的均匀信用对比。
  - GiGPO 并不是"集中固定预算"。每一步仍带有 episode 级优势 A^E，步级项是叠加上去的、按状态各自不同的蒙特卡洛 Q−V 估计。
  - 均匀对照取轨迹内步级优势的均值，实际上抹掉了步级信息。因此"GiGPO − 均匀"≈"有无步级信号"，而不是"等信息下定位与覆盖之比"。
  - 锚点 V_d 的分子是"组大小≥2 且回报方差>0 的步"。这只是有非零对比，不等于验证器暴露了对错；ECPO 表明这类优势常被"幸运动作"主导。分母是轨迹长度，不是因果链长度 C。
  - 结果是：无论换号点是否落在 0.8 附近，都不能算作对 2609.02417 定量预测的验证或证伪。
- **C2 的判据也几乎不可证伪**：19 个点里有 18 个是 ALFWorld 子任务。每个子任务每个种子只有约 20 条评测 episode，部分子任务接近天花板，且同一次运行内的 6 个子任务点并不独立。换号点的 bootstrap CI 会很宽，"0.8 在 CI 内"几乎必然成立。另外，V_d 的取值范围未必跨过 0.8。
- **故事链缺少"已有失败"这一环**：它的起点是"没人测过"，而不是某个方法有证据的失败。
- **是否值得继续**：底线问题可以保留，但当前"检验 0.8 相变点"的主张需要重想，不宜直接进入实验。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| C1：GiGPO−均匀 的差随锚点 V_d 单调增大 | 部分重合 | 2609.02417 §7 已明确预测"收益追踪恢复的覆盖"。由于均匀臂抹掉了步级信息，该差值接近"步级信号量越多收益越大"，近乎同义反复。ECPO / AdaStep 给出竞争解释：收益取决于每个锚点的信噪比，而不是被暴露步的比例；N 同时改变覆盖与估计噪声，两者混在一起。 |
| C2：换号点落在 0.8 附近（CI 包含 0.8） | 新，但无法有效检验（claim 阻塞） | 锚点 V_d 与 k/C 构念不对应：分母是轨迹长而不是 C，"方差>0"也不等于"暴露对错"；GiGPO 不是固定预算的集中信用。只要求 CI 包含 0.8 是一种不拒绝判据，在 19 个高噪声、非独立的点上近乎必然成立。 |
| C3：高 V_d 时 GiGPO 优于轨迹内打乱 | 部分重合 | GACA 已在 ALFWorld 1.5B、基于 GiGPO 锚点分组的估计器上证明"轨迹内置换会掉 8.34 点"（置换对象是门控分数）。打乱对照本身也是 2609.02417 提出的。剩下的差别只是"直接置换步级优势"和"限定在高 V_d 子集"。 |

## 最高近邻

1. **Coverage, Not Targeting**（2609.02417）https://arxiv.org/abs/2609.02417
   - 重合：定义了 V_d=k/C、合成相变点 0.8、均匀与匹配集中度打乱对照，并在 §7 预测基于重复状态的步级方法的收益追踪覆盖。
   - 差别：只做了 τ²-bench / BFCL，没有 GiGPO，也没有 ALFWorld / WebShop。
2. **GiGPO**（2505.10978）https://arxiv.org/abs/2505.10978
   - 重合：锚点分组、单例组 <35% 的组大小统计，以及 ALFWorld / WebShop 上相对 GRPO 的步级增益。
   - 差别：没有均匀或打乱对照，也没有覆盖理论的框架。
3. **GACA**（2609.12424）https://arxiv.org/abs/2609.12424
   - 重合：基于 GiGPO 锚点分组；ALFWorld 1.5B 上的轨迹内随机分配对照（96.88→88.54）已经表明"放到哪一步"有影响。
   - 差别：置换的是 NLL 门控分数，不是步级优势本身，也没有 V_d 分析。
4. **ECPO**（2606.05885）https://arxiv.org/abs/2606.05885
   - 重合：分析了 GiGPO 锚点优势在有限 rollout 下的可靠性，并做了 N∈{4,8,10} 的组大小分析。
   - 差别：做的是校准方法，没有均匀或打乱对照；但它对"锚点 V_d=覆盖"构成直接的竞争解释。
5. **Credit Without Ground Truth**（2608.19760）https://arxiv.org/abs/2608.19760
   - 重合：在 ALFWorld 上用 marginal-matched 打乱对照审计步级信用，并强调必须匹配有效剂量。
   - 差别：没有 GiGPO 锚点，也没有 V_d 换号检验。均匀臂只匹配了优势总量，没有匹配 L2 或有效剂量，这正是该文警告的情形。

```json
{
  "score": 4.5,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "claim: 锚点 V_d（组大小≥2 且方差>0 的步数/轨迹长度）与 2609.02417 的 k/C（验证器暴露对错的步数/因果链长度）构念不对应；GiGPO 并非固定预算集中信用，且均匀臂取轨迹均值抹掉了步级信息，GiGPO−均匀≈有无步级信号，C2 的 0.8 相变检验无法验证或证伪原理论",
    "claim: C2 以'0.8 在换号点 bootstrap CI 内'为支持判据，19 个点中 18 个是同一运行内非独立、每点约 20 条评测 episode 且部分接近天花板的子任务点，CI 必然很宽，判据近乎不可证伪；V_d 取值范围是否跨过 0.8 也未知",
    "novelty: C1/C3 是 2609.02417 §7 明文预测并用其自身对照执行；C3 被 GACA 轨迹内置换消融（ALFWorld 1.5B，96.88→88.54）部分覆盖"
  ],
  "novelty_conclusion": "底线问题（ALFWorld/WebShop 上等量均匀/打乱信用对照）未被回答，但当前 claim 主要是在新基准上执行 2609.02417 已给出的预测，C3 部分被 GACA 覆盖，唯一新颖的 C2 因构念不对应和判据过宽而无法有效检验；需要重想核心主张后再评。",
  "closest_neighbors": [
    "Coverage, Not Targeting: A Structural Regime in Multi-Turn Agent Credit Assignment (arXiv 2609.02417)",
    "Group-in-Group Policy Optimization for LLM Agent Training (arXiv 2505.10978)",
    "Granularity-Adaptive Credit Assignment for Long-Horizon LLM Agent Reinforcement Learning (arXiv 2609.12424)",
    "When Denser Credit Is Not Enough: Evidence-Calibrated Policy Optimization (arXiv 2606.05885)",
    "Credit Without Ground Truth: Auditing Step-Level Credit Assignment in LLM Agents Against Executed Replay (arXiv 2608.19760)"
  ]
}
```
