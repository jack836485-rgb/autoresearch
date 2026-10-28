## 结论

2026-10-28 评审：**score 6.0 / 10，verdict = promising_needs_revision**。

检索到的工作里，没有人在开思考的 OPSD rollout 上按"思考段 / 答案段"分开做损失掩码，也没有人在 TH 训练下做过另一题参考的对照。2609.20612 仓库 `configs/experiments.md` 中，另一题参考与 marker 掩码两组对照都只有 `_direct` 运行，与 brief 的说法一致。失败证据（2609.20612 表 11；2607.05184 表 3 中的 0.532/0.590/0.591）和 TOPD 的数字（49.3→51.3，前段与中段监督最有效）都已核实。Baseline R1/R2 与基座同任务、同模型、同评测，公开仓库与复现入口可用；预算约 250 A100 小时，可行。定位关键词都是已有术语。

但新颖性边界还没有定下来，问题集中在 Claim 的判别力：

1. **主张一区分不了机制。** 2607.05184 的 fork suppression 和 2603.24472 的 epistemic 抑制也都预测"只有思考段的监督有害"。所以 R4 − R3 > 0 只能定位损失在哪一段，不能支持"模仿缺口"这一机制。而且 R3 本质上是 R2 把监督窗口缩成 512 token；R4 的答案段又接近 DR 的输出。这组对照在已知结果之外增加的信息有限。
2. **预算强制会破坏"答案段 = 得出结论后的事后书写"这一对应。** Qwen3-1.7B 的数学思考在 512 token 时绝大多数没有结束，强制收束之后写出的答案段，是在思考未完成时写出来的，不是模仿缺口论证里那个"可模仿"的阶段。另外，R3 和 R4 被监督的 token 数不同，没有做匹配。
3. **主张二的反事实带有混淆，且部分已被覆盖。** 另一题参考带着一个错误的答案，所以它同时改变了"教师有没有本题信息"和"教师有没有被误导"。仓库里已有 `--unprivileged-teacher`，这才是干净的"无特权信息"对照，但没有用上。此外，2608.09228（OP²SD）和 2608.18271 已经表明，另一题参考在非思考设定下与正确参考相当，甚至更好。
4. **判定表有空格。** "ΔR3 < 0 且 ΔR4 不显著"这种情况没有被覆盖，而它恰恰是最可能出现的结局。"ΔR4 > 0"是只看点估计还是要求显著，也没有写明。

结论：方向值得继续，但要等 Claim 能把"段落定位"与"机制"区分开之后，才进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 失败条件：TH 训练使 OPSD 的增益变成损失 | 已被覆盖（作为动机成立） | 2609.20612 表 11（Full Trace 第 100 步 TH − DR = −9.83）；2607.05184 表 3。这部分是引用，不是贡献 |
| 主张一：损失来自思考段，答案段监督不伤 | 部分新颖 | 分段掩码这个设计未见先例。但 fork suppression 与 epistemic 抑制给出相同预测，结果区分不了机制；512 的强制截断让答案段不再是自然的事后书写；R3 ≈ R2 换成更短的窗口。2607.05184 附录 A 提到"OPSD 近期更新关闭了 deliberation token 上的逐 token 反馈"，但没有给出处，需要检索 |
| 主张二：思考段的伤害需要本题特权信息 | 部分重合 | 另一题参考的对照已有：2609.20612（只在 DR 下）、2608.09228 OP²SD（非思考学生，另一题参考与 OPSD 相当甚至更好）、2608.18271。"TH 加思考段掩码"这一设定是新的，但另一题参考把"无信息"与"错误信息"混在一起，没有用无特权教师作对照 |
| 机制：模仿缺口映射到思考段与答案段 | 部分重合 | 2608.25936 已经用 Weihs et al. 的模仿缺口和 LUPI 来框定 OPSD 的特权信息问题（无实验）。本 Idea 的实验不能把它和其他机制区分开 |
| 最小实验能与最高近邻区分 | 可行，判别力不足 | 同一仓库、同一配置，只改 rollout、掩码和参考，预算合理。但判定表没有覆盖最可能的结局 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?** https://arxiv.org/abs/2609.20612 （代码 https://github.com/xiuyuz/opsd-reference-study）
   - 重叠：同一模型、数据、配置，TH 与 DR 的对比，前 1K / 前 4K / 分散 1K 的损失窗口，DR 下的另一题参考对照。
   - 差别：没有完整的强制 TH rollout，没有思考段与答案段的分段掩码，也没有在 TH 下换参考。本 Idea 去掉这篇的名字后仍然成立，不是只给它补一个实验，但贡献只是在它的设定上增加一个因子分解。
2. **Rethinking On-Policy Self-Distillation for Thinking Models**（Kaur et al.） https://arxiv.org/abs/2607.05184
   - 重叠：只有训练时开思考才有害；fork suppression 机制本身就预测思考段受损。
   - 差别：没有分段掩码，也没有另一题参考；只做了 marker token 与随机 token 的掩码。
3. **Privileged Solutions or Context-Induced Teacher Behavior? Dissecting OPSD**（OP²SD） https://arxiv.org/abs/2608.09228
   - 重叠：用另一题的解答作教师上下文来区分"特权信息"与"上下文诱导的行为"，并有 both-thinking 的附录。
   - 差别：主设定是非思考学生，没有按段分开监督。
4. **Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?** https://arxiv.org/abs/2603.24472
   - 重叠：知道解答的教师抑制 epistemic 表达，在开思考的 Qwen3 上导致退化；做了去掉 `<think>` 的教师上下文对照。
   - 差别：改的是教师看到什么，不是损失作用在哪些 token。
5. **One Symptom, Three Levers: A Critical Review of OPSD** https://arxiv.org/abs/2608.25936
   - 重叠：已经把 OPSD 的问题框成"特权信息可模仿性 / 模仿缺口"，以及"信号作用在哪些 token"。
   - 差别：纯综述，没有实验，没有提出分段掩码。

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim blocker: R4-R3>0 is equally predicted by fork suppression / epistemic suppression (2607.05184, 2603.24472); the experiment localizes harm but cannot support the imitation-gap mechanism claimed",
    "Claim blocker: 512-token budget forcing truncates most Qwen3-1.7B thinking, so the forced answer segment is not the post-conclusion write-up the imitation-gap mapping requires; supervised token counts of R3/R4 are unmatched",
    "Claim blocker: Claim 2 control (other-problem reference) confounds 'no same-problem info' with 'misleading answer'; repo's --unprivileged-teacher control is unused, and other-problem-reference effects are already reported by 2608.09228 / 2608.18271",
    "Decision table gap: the likely outcome dR3<0 with dR4 not significant is not covered; whether dR4>0 must be significant is undefined"
  ],
  "novelty_conclusion": "As of 2026-10-28, segment-wise (thinking vs answer) loss masking and an other-problem reference control under thinking-enabled OPSD rollouts have no direct prior work, but the result only localizes harm already predicted by existing mechanisms; Claim 2 partially overlaps OP2SD/2608.18271; the novelty boundary is unresolved.",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (2609.20612)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (2607.05184)",
    "Privileged Solutions or Context-Induced Teacher Behavior? Dissecting On-Policy Self-Distillation (2608.09228)",
    "Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs? (2603.24472)",
    "One Symptom, Three Levers: A Critical Review of On-Policy Self-Distillation (2608.25936)"
  ]
}
```
