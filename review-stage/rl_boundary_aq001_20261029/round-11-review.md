## 结论

2026-10-29 评审：**score 7.5，verdict = promising_needs_revision**。

- **新颖性**：主贡献（Claim 2：用推理期“基座在该方法够得着的位置接管”的对应物，按任务预测各训练方法的 pass@32 增益，并用任务内回归、置换检验和“自身对应物优于他人对应物”来检验）在检索范围内没有找到先例，判为新颖。Claim 1 的逐轮可找回覆盖剖面是已有协议的组合：交接来自 Reach or Solve，分叉与噪声底来自 Replay Gap，“入口锁定”问题来自 Locked at the Entrance 的单轮结论。把它搬到多轮 agent 上作为测量结果是新的，但方法本身增量有限。Claim 3 的处方是给 DPH-RL 加轮掩码，属于平凡组合，价值完全取决于 Claim 2 是否成立。
- **可行性**：所有 baseline 都在同一问题内（RL 下的 pass@k / 多样性保持），复现路线可核验。TAR、DPH-RL、sharpening-tax（PTGS、`WEBSHOP_ENV_SEED`、推理期 PTGS 用法）、verl-agent（`run_webshop.sh`、`run_alfworld.sh`）、AgenticRL_Handoff（`src/handoff/alfworld/{environment,rollout}.py`）的仓库、文件和函数都已用 git 核实存在。DPH-RL 与 TAR 原本提出于单轮数学 / SQL，移植到多轮属于 Claim 2 的检验对象本身，不算跨域借鉴。
- **Claim blocker（须修正后才能进入实验）**：对应物表里 DPH-RL 与 TAR 共用同一个“离线回放”对应物，所以在每个任务上 P_DPH(i) ≡ P_TAR(i)。预注册推翻条件要求每个方法的自身对应物偏 R² 必须**高于其他任一方法的对应物**，这对这两种方法在定义上不可能满足。结果是 WebShop 的 6 个非 GRPO 方法里有 2 个机械地判“失败”，“多数方法不优于他人”这条推翻条件因此带有结构性偏差，不能检验主 Claim 的特异性。
- **风险（非 blocker）**：
  - 每任务只用 32 次 rollout 算 pass@32，P_m(i) 与单种子 Δ_m(i) 都是 0/1 指示量的差。任务内有效变异只来自各对应物结果不一致的少数任务，b 的检出高度依赖阶段 A 的功效分析。
  - “纯 GRPO 在 WebShop / ALFWorld 上产生锐化税”目前没有直接证据。Sharpening Tax 测的是发布模型对；PASS@(k,T) 一文报告 RL 在组合式序列任务上会扩大边界。阶段 0 的门槛已把这一点变成可推翻条件，处理得当。
- **是否值得继续**：值得继续。故事链（发布模型的覆盖损失 → 现有方法没有说明在多轮中作用于哪里 → 推理期对应物 → 可推翻的任务内预测）证据基本到位。上述 blocker 是检验设计上的局部缺陷，不涉及新意边界。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1 按轮定位（逐轮替换 + 同模型噪声底得到 L(t)） | 部分重合 | 单交接点协议见 Reach or Solve，分叉加同模型对照见 Replay Gap，单轮 token 级借用见 What RL Brings；多轮逐轮“只替换第 t 轮”的覆盖剖面未见先例，但它是测量，剖面落在哪里都不作成败条件 |
| 2 测试时对应物按任务预测训练方法增益（主贡献） | 新颖 | 未检索到用推理期接管对应物、在任务内（任务与方法双固定效应）预测训练期保覆盖方法增益的工作；Sharpening Tax 只做按任务整条路由与少量 rollout 外推税值。**但 DPH-RL 与 TAR 共用对应物，使“自身优于他人”这条推翻条件对两者恒不成立，属于 claim blocker** |
| 3 剖面选轮前向 KL 优于同 token 占比随机选轮 | 部分重合 | 方法等于 DPH-RL 加轮掩码；匹配集中度的随机对照沿用 Coverage, Not Targeting 的建议；“锚定作用于分布，不同于信用定向”是新的、可由随机对照直接推翻的假设 |

## 最高近邻

1. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509；代码 https://github.com/changdaeoh/sharpening-tax）。重叠：在 WebShop / BFCL / ACEBench 上测发布模型的覆盖税；PTGS 在 RAGEN 的 Sokoban / FrozenLake 上验证并有推理期用法；有基座与后训练模型的按任务路由。差别：没有逐轮接管，没有在受控 RL 下按方法预测增益。
2. **Reach or Solve? Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636）。重叠：真实可回放环境（ALFWorld、TravelPlanner）中的检查点交接。差别：只有单一交接点，只比较 SFT↔RL 的到达与完成，不涉及覆盖或保覆盖方法。
3. **What RL Brings to Reasoning: A Few Decisions the Base Model Would Not Make**（https://arxiv.org/abs/2610.24663）。重叠：生成期在基座与 RL 模型间稀疏借用决策，测能找回多少 RL 增益并保留多少 pass@k。差别：单轮数学、token 级，不预测训练方法的效果。
4. **Locked at the Entrance, Open Inside**（https://arxiv.org/abs/2608.29188）。重叠：把 RLVR 的覆盖收缩定位到入口，入口干预有效。差别：单轮 Countdown / 数学，没有多轮“观察后重新锁定”的区分。
5. **The Replay Gap**（https://arxiv.org/abs/2608.08239）。重叠：在真实环境中分叉换模型，用同模型分叉作噪声底。差别：评测的是 SWE-bench 路由，不涉及 RL 覆盖或训练方法。

```json
{
  "score": 7.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim blocker: DPH-RL and TAR share the same offline-replay counterpart (P_DPH(i) ≡ P_TAR(i)), so the pre-registered 'own counterpart beats every other method's counterpart' falsification condition is mechanically unsatisfiable for both, biasing the 'majority of methods' test for Claim 2's specificity"
  ],
  "novelty_conclusion": "Claim 2 (inference-time takeover counterparts predicting per-task training-method pass@32 gains under task and method fixed effects) appears novel; Claim 1 is a new multi-turn measurement built from existing handoff/fork protocols (partial overlap); Claim 3's method is a turn-masked DPH-RL whose value rests on Claim 2. Baselines and reproduction routes verified. Needs a fix to the shared-counterpart falsification design before experiment_ready.",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "What RL Brings to Reasoning: A Few Decisions the Base Model Would Not Make (arXiv 2610.24663)",
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World (arXiv 2608.08239)"
  ]
}
```
