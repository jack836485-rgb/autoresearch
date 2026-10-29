## 结论

日期 2026-10-29。score 6.0/10，verdict：promising_needs_revision。

问题本身值得做：多轮 agent RL 中保 pass@k 覆盖时状态来源是否起作用，以及能否用 L(t)/O(t)/M_low 在训练前按任务预测，我没有检索到直接做过这件事的工作。基座与 baseline 也基本可复现：verl-agent 的 `run_webshop.sh`/`run_alfworld.sh`、TAR 的 `compute_tar_weights` 与 `build_memory_bank.py`、DPH-RL 的 forward 配置、sharpening-tax 的 `PTGSHooks` 与 `WEBSHOP_ENV_SEED`、Handoff 仓库的 ALFWorld rollout 都已浅克隆核实。

但新颖性边界还没有解决，主要有三点：

1. **机制在多轮场景已有人提出。**"离线回放只能锚定共享状态"本质上是 DAgger 式协变量偏移。多轮 agent 里，Guided-OPD（EMNLP 2026，ALFWorld/WebShop）和 ReOPD（2607.04763，"prefix trap"、双侧分布偏移）都已明确讨论前缀/状态来源的失配，brief 没有定位到这两篇。因此"被忽视的关键点"只在"保覆盖、目标为基座"这一窄口径下成立。
2. **方法是已知组件的组合。**学生状态版等于 2605.16826 的 DAgger 式前向 KL（教师换成基座），再加 TAR 的门控。
3. **对照不只改了状态来源，这是 claim blocker。**TAR 的库只含基座的**成功**多样解；学生状态版在 G 的状态上采样的是**未经成功筛选**的基座动作。两组同时改了状态来源和"目标是否承载成功"，Claim 3 的"只差状态来源"不成立。ReOPD 指出的反向风险（学生状态上的教师/基座目标不可靠）也没有纳入预测或推翻条件。

另有一处表述与证据冲突："单轮上不存在状态失配"。2605.16826 和 2605.22731 恰好是在单轮上论证前缀/状态来源的作用，所以"这也解释了单轮方法为何有效"缺乏支撑。

还有一个次要问题：M_low 中的 L(t) 本身就是"B 在 G 的状态上行动可找回的覆盖"，与学生状态版的作用对象几乎同构，预测有一定自证成分。另外 PBA 无公开代码，但它结构简单，按描述本地实现可以接受，不构成致命问题。

结论：值得继续，但当前不是 experiment_ready。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. 多轮中基座与 RL 策略的状态重叠在分支后下降，覆盖损失有相当部分落在低重叠状态 | 部分重合 | "学生偏离教师熟悉状态"在 Guided-OPD/ReOPD 中已是动机；把它与 pass@k 覆盖损失按轮定位（L(t)×O(t)），并以基座/GRPO 同起点来做，未见先例。Handoff（2609.19636）测 Reach/Solve，不测覆盖与重叠 |
| 2. 离线回放只能找回共享状态上的覆盖 | 部分重合（机制层面接近已知） | 这是 DAgger/协变量偏移在保覆盖场景下的直接推论；ReOPD 已形式化多轮前缀分布的双侧偏移。新的只是把它用在"保覆盖"目标上 |
| 3. 只改状态来源的对照可检验机制，差异随 M_low 增大、可训练前预测 | 新颖但设计有缺陷 | M_low 作为按任务的训练前预测量未见先例；但对照同时改了"成功筛选的目标 vs 未筛选的基座动作"，混淆了机制；学生状态版本身是 2605.16826 DAgger 目标加 TAR 门控 |
| 附：单轮方法不存在状态失配 | 无证据 / 与近邻冲突 | 2605.16826、2605.22731 在单轮上论证状态来源的作用 |

## 最高近邻

1. **ReOPD：Multi-Turn On-Policy Distillation with Prefix Replay**（https://arxiv.org/abs/2607.04763）
   - 重叠：多轮 agent 中前缀来源设计，提出 prefix trap，即学生占据分布与教师可靠性之间的双侧偏移。
   - 差别：目标是蒸馏的准确率与效率，不涉及 pass@k 保覆盖与基座锚定。
2. **Guided-OPD：On-Policy Distillation with Curriculum Turn-level Guidance for Multi-turn Agents**（https://aclanthology.org/2026.emnlp-main.1424/）
   - 重叠：在 ALFWorld/WebShop 上指出学生误差累积把轨迹推出教师熟悉状态，并用混合教师轮次修复。
   - 差别：目标是蒸馏，不测覆盖，也没有训练前预测量。
3. **TAR：Targeted Adaptive Replay**（https://arxiv.org/abs/2610.24236）
   - 重叠：门控与加权方式被直接沿用。
   - 差别：只在单轮数学上验证，没有多轮状态失配分析。
4. **Decoupling KL and Trajectories**（https://arxiv.org/abs/2605.16826）
   - 重叠：学生状态版就是其"学生前缀 + 前向 KL"（DAgger 式）目标。
   - 差别：单轮数学蒸馏，目标不是基座保覆盖。
5. **Reach or Solve? Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636）
   - 重叠：真实环境中的检查点交接与替换，覆盖 ALFWorld。
   - 差别：度量是 Reach/Solve，不涉及 pass@k 覆盖、状态重叠或训练方法。

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim 3 的受控对照不只改状态来源：TAR 离线版用基座成功解作目标，学生状态版用未经成功筛选的基座动作，机制被混淆（claim blocker）",
    "定位遗漏多轮前缀/状态来源的直接近邻 ReOPD (2607.04763) 与 Guided-OPD (EMNLP 2026)，'被忽视的关键点'只在保覆盖窄口径下成立，新颖性边界未解决",
    "'单轮方法不存在状态失配、因此有效'与 2605.16826/2605.22731 的单轮证据冲突，属无支撑论断"
  ],
  "novelty_conclusion": "机制（离线回放只锚定共享状态）是 DAgger 式协变量偏移在多轮保覆盖场景的推论，多轮蒸馏中已有 ReOPD/Guided-OPD 讨论；方法是 2605.16826 DAgger 目标加 TAR 门控的组合。剩余新意在于多轮 agent RL 中按轮定位 pass@k 覆盖损失与状态重叠（L(t)、O(t)），以及训练前按任务的预测量 M_low，部分新颖，需修正对照混淆与定位后再审。",
  "closest_neighbors": [
    "Multi-Turn On-Policy Distillation with Prefix Replay (ReOPD, arXiv 2607.04763)",
    "On-Policy Distillation with Curriculum Turn-level Guidance for Multi-turn Agents (Guided-OPD, EMNLP 2026)",
    "Preserving Reasoning Diversity in RLVR via Adaptive Replay (TAR, arXiv 2610.24236)",
    "Decoupling KL and Trajectories (arXiv 2605.16826)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)"
  ]
}
```
