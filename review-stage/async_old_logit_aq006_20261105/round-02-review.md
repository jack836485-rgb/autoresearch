## 结论
2026-11-05：总体 score 5.0，verdict 为 **needs_rethink**。主贡献是把"精确 old logits 的收益"在异步 agentic RL 中拆成两部分：参考位置放在 token 的生成版本上，加上中心化去掉数值偏差漂移；并指出何时仍需要精确分解。这个归因清楚、可证伪，但分量不够。它的机制论证几乎全部来自 2610.40945（§6.2 参考位置分析、DLC 在 q=p_old 时退化为采样参考 PPO、附录 C Table 9 连续异步版本差 4），也来自 2609.20807（不用 old logits 的 TIS+SC 在陈旧和 30B-A3B 量化下有效）。"用 rollout logprob 作裁剪锚点"也已是 verl bypass 模式和 fully-async 的标准做法。本 Idea 新增的主要是把这些结论放到 agentic、MoE、AReaL 设置下做受控复核。重要性与新颖度都只到 6 左右，达不到"至少两项 ≥8"。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 能给异步系统一条"何时不必为 old logits 付系统代价"的实用判据，有价值但影响有限。(1) 业界默认做法已经是把 rollout logprob 当 PPO anchor（verl bypass、fully-async），所以 R1 若成立，主要是确认已有默认做法。(2) R2 的"MoE 不做路由回放"并不是实践中的主流配置，R3 路由回放已是标准修法，因此"需要 old logits 的条件"落在一个人为放大的设置上。(3) 原问题里 2605.12070 的收益本身不稳：4B 上 Decoupled PPO 与 Snapshot 在多数列只差 1–3 点，大差距只集中在 30B-A3B 的 VitaBench in-store 一列。 |
| 新颖度 | 5.5 | 拆分维度"参考位置 × 偏差处理"由 2610.40945 Table 3 直接给出：分母 q 与 p_old 之别，加上是否中心化。C 臂（p/q 裁剪 + 中心化）与该文的"IS with centering"只差截断还是裁剪，而它与 DLC 的对比在该文 Table 2 已经做过（2.61 对 2.17）。另外，brief 称该文"仅限固定 θ0 陈旧采样器"不准确：附录 C 已有 Qwen3-8B，以及最大版本差 4、按生成版本裁剪的连续异步实验。其中不用 old logits 的 IS 为 1.4×，DLC 为 1.2×，已部分覆盖可推翻判断 1。剩余新意在于 agentic 多轮、部分 rollout、MoE 和 Adam 小学习率这些条件的迁移检验，属于可辨认的增量，不是独立的新机制或新理解。 |
| 有效性 | 6.0 | **现有依据**：2610.40945 的精确分解与 Table 2/9 支持判断 (a)。BF16 连续异步下，以 q 为分母的修正已接近 DLC，这直接支持 R1 中 B≈D。2609.20807 的结论"偏差主要以漂移作用，SC 可与 IS 组合"支持判断 (b)。**迁移条件**：数值偏差在训练中近似恒定，且尾部不跨过裁剪尺度。多轮工具调用中，工具返回 token 不进损失，这一点有利于迁移；MoE 路由翻转可能产生重尾 e_t，这正是判断 (b) 最可能失效的地方，目前没有直接证据。**仍未知**：Adam 小学习率加 120 步时，滞后反馈环是否足够强、能否拉开各臂。另有一份反向证据：AReaL 论文 Table 2 显示，Decoupled PPO（即 A 臂）在最大陈旧度 4 时已贴近 oracle。这样 R1 中"B、D 都明显优于 A"可能根本不出现，归因就无从谈起。 |

**与原问题的关系**：本 Idea 是子问题。它回答"old logits 的收益来自哪一机制"，没有回答原问题中"哪些声称无损的系统未保留 old logits"的审计，也没有给出阈值耦合导致后期崩溃的机理；这两部分仍未解决。转向本身不构成阻断。

**实验能否判别主张**：只能部分判别，存在 Claim 阻断。(1) 两条主判断都是等价性主张（"同一噪声带"），但各臂只有 1 个种子，R2 也只有 C、E 两臂补到 2 个种子。噪声底来自两次 on-policy 训练，并不代表各修正臂自身的种子方差，因此"B 与 D 之差小于噪声"和"D 显著优于 B"在统计上都无法成立或否定。2610.40945 本身每配置做了 3 次。(2) 没有在本设置中先复现 D 明显优于 A 的前提。若 D≈A，"精确 old logits 的收益"在本设置里就不存在，归因无对象；而按 AReaL 的消融，这个结果相当可能出现。(3) 跟原问题的连接也是断的：Search-R1 的 EM 与 2605.12070 的 τ²/VitaBench 收益不可比，所以"解释 2605.12070 的收益"实际上无法被检验，只能检验"在 Search-R1 中是否需要 old logits"。

**可行性：pass（有条件）**。各臂都有可信的实现路线，8×A100 约 4.5 天也在约束内，但 brief 中几条"已核验"的说法与 AReaL 当前代码（HEAD 9531722）不符，需要计入工作量：
- AReaL 的 score centering 只支持普通 FSDP actor。`cli_args.py` 中写明 "Score centering requires an ordinary FSDP actor"，并要求 `recompute_logprob=False`，禁止 `use_decoupled_loss` 与其他 surrogate，只允许 REINFORCE+TIS。`megatron_engine.py` 中完全没有 score centering。
- 由此，R2 的 Moonlight 沿用 `examples/r3` 的 Megatron 后端时，C 臂与 E 臂都没有现成路径：要么移植到 Megatron（`score_centering.py` 已有 `vocab_parallel_selected_logprobs` 辅助函数，但未接入），要么改用 FSDP 跑 16B MoE。R1 中"PPO 裁剪 + 中心化"同样是新写的 loss，不是复用。
- head 拼装 `trajectory_heads` 只在单轮 `rlvr.py` 里接入。多轮搜索 workflow 需要自己按轮对齐 head。
- AReaL 仓内的 search_agent 是 Tongyi-DeepResearch，用 Serper/Jina 加 LLM judge；`local_1.5b_example.yaml` 对应的是外部 ASearcher。NQ+HotpotQA+e5 本地检索器需要从 Search-R1/ASearcher 引入，检索索引的内存与磁盘也要计入共享机器余量。

以上都是实现量问题，不是规范或资源缺失：数据、模型、逐 token versions、推理端 logprob 与 top-k head 都可得；Snapshot 需要的主机内存约 128 GB，需开跑前确认。

## 最高近邻
1. **On the Origin and Evolution of Training-Inference Mismatch in LLM RL**（[arXiv:2610.40945](https://arxiv.org/abs/2610.40945)）：重叠最高。精确拆分 e_t/ℓ_t、PPO 参考位置分析、IS+centering 与 DLC 对照，以及附录 C 的连续异步（版本差 4）与 8B 实验都已在其中。差别：它用 Countdown 单轮、SGD 大学习率、40 步、稠密模型，没有 agentic 和 MoE。
2. **Missing Old Logits in Asynchronous Agentic RL**（[arXiv:2605.12070](https://arxiv.org/abs/2605.12070)）：提出 old logits 缺失问题，并比较 Snapshot、EWMA 与中间版本代理（Table 1/2）。差别：没有"推理端概率作参考"或中心化对照，未拆分机制。
3. **Score Centering Stabilizes Off-policy RL**（[arXiv:2609.20807](https://arxiv.org/abs/2609.20807)）：结论为漂移是主因；所有比率都用采样端记录概率，即不用 old logits；SC 可与 IS 组合处理陈旧；有 30B-A3B。差别：以量化偏差为主，陈旧设置是固定 64 步同步，没有 agentic，也没有逐版本异步。
4. **AReaL**（[arXiv:2505.24298](https://arxiv.org/abs/2505.24298)）：Decoupled PPO（即 A 臂）的来源。其 Table 2 显示陈旧度 ≤8 时已接近同步 oracle，这对"A 明显差"的前提构成反证。差别：只做了数学单轮与稠密模型，没有偏差处理维度。
5. **verl Rollout Correction（bypass/decoupled 模式）**（[文档](https://verl.readthedocs.io/en/latest/algo/rollout_corr.html)）：bypass 模式以 π_rollout 作 PPO anchor，即 B 臂，已是现成选项。差别：没有给出 bypass 与 decoupled 的效果对照。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 6.0},
  "contribution_assessment": "主贡献：在异步 agentic RL 中把精确 old logits 的收益归因为'生成版本作裁剪参考'加'中心化去漂移'，两者都不需要 old logits，只有 MoE 重尾偏差时才需精确分解。重要性 6：给出实用判据，但 rollout logprob 作 anchor 已是 verl bypass、fully-async 的默认做法，R2 不做路由回放的设置偏人为。新颖度 5.5：拆分维度与 IS+centering 对 DLC 的对照来自 2610.40945 Table 2/3，其附录 C 已含版本差 4 的连续异步结果（IS 1.4×，DLC 1.2×），新增部分只是 agentic、MoE 条件下的复核。有效性 6：2610.40945 与 2609.20807 的机制和邻近结果支持 (a)(b) 在稠密 BF16 下成立；MoE 路由偏差的尾部、Adam 小学习率下滞后是否足以拉开各臂仍未知；AReaL 的消融显示 A 臂在陈旧度 4 下可能已接近 oracle。",
  "feasibility": "pass",
  "feasibility_reason": "数据、模型、逐 token versions、logprob 和 top-k head 都可得，8×A100 约 4.5 天在约束内。但 AReaL 的 score centering 只支持 FSDP 加 REINFORCE+TIS（cli_args 校验），Megatron 引擎无实现，R2 Moonlight 的 C、E 臂需要移植或改用 FSDP；PPO 裁剪加中心化、多轮 head 拼装都要新写；e5 本地检索不在 AReaL 仓内，需从 Search-R1/ASearcher 引入。这些是实现量问题，不是资源缺失。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献不足：重要性与新颖度都约 6，未达到三项 ≥6 且至少两项 ≥8。机制与关键对照（IS+centering 对 DLC、连续异步版本差 4）已由 2610.40945 给出，主要新增是设置迁移的复核。",
    "Claim 阻断：两条主判断都是等价性主张，但各臂只有 1 个种子（R2 的 C、E 也仅 2 个），on-policy 噪声底不能代表修正臂的种子方差，无法判别'同一噪声带'或'显著更好'。",
    "Claim 阻断：没有先在本设置中确认 D 明显优于 A。AReaL 的消融显示 Decoupled PPO 在陈旧度 4 时接近 oracle，若 D≈A 则归因无对象；Search-R1 的结果也不能检验对 2605.12070 收益的解释。",
    "定位不准：brief 称 2610.40945 仅用固定 θ0 陈旧采样器，但其附录 C 已有连续异步（版本差 4）与 Qwen3-8B 实验；称 score centering 代码路径'已核验可复用'，与 AReaL 只支持 FSDP 和 REINFORCE+TIS 的实际限制不符。"
  ],
  "novelty_conclusion": "相对 2610.40945 只有设置迁移层面的增量：拆分维度、零 old-logit 的中心化修正，以及连续异步下 q 分母修正接近 DLC 的结果都已有；2609.20807 与 verl bypass 已覆盖'不用 old logits'的做法。剩余新意限于 agentic 多轮与 MoE 无路由回放条件下的受控复核。",
  "closest_neighbors": [
    "On the Origin and Evolution of Training-Inference Mismatch in LLM Reinforcement Learning (arXiv:2610.40945)",
    "Missing Old Logits in Asynchronous Agentic RL: Semantic Mismatch and Repair Methods for Off-Policy Correction (arXiv:2605.12070)",
    "Score Centering Stabilizes Off-policy Reinforcement Learning (arXiv:2609.20807)",
    "AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning (arXiv:2505.24298)",
    "verl Rollout Correction docs (bypass vs decoupled mode)"
  ]
}
```
