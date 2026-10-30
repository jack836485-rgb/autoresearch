## 结论
2026-10-29 评审：**7.6 / 10，promising_needs_revision**。

在监控器训练数据上，这个 Idea 有真实的新意：在自然投机出现前，用中途检查点诱导投机，训练监控器；并把诱导者和诱导时点作为变量来比较。在我检索到的工作里，没有找到用检查点诱导数据训练监控器、再前瞻评测召回的研究。实验设计也比较完整：同源负例、等生成预算的自然采样对照、同正例数子对照、AST 规范化风格检验、天花板预案都有。两个测试床的仓库我都已克隆核实，文中引用的脚本和命令都存在。`save_freq` 在 verl 配置里可调，"20 步存一次"可以做到。算力约 1,300 A100 小时，在约束之内。

不能判 experiment_ready 的原因是一个 claim 阻塞。"诱导者 × 时点这个变量从未被操纵过"这一核心主张，以及"EleutherAI reward hacking indicators 不比较诱导者"这一定位，与可核验事实冲突。EleutherAI 的 Reasoning Interpolation（2026-04）已经做了以下操作：
- 在各检查点上用诱导前缀引出 exploit；
- 系统比较了三类诱导者：同模型微调 donor、跨家族 Qwen3-8B、提示 Claude；
- 观察到早期检查点被诱导的率远高于自发率。

不过，它的目的是预测投机率，不训练监控器；被训练的模型用的是 SFT，不是 RL。所以新意边界应改为"**把检查点诱导数据作为监控器训练集，并在 RL 中评测前瞻召回**"。现在的写法把边界画在了已被做过的地方。

此外还有两点：
- 贡献本质上是 Kirch et al. 与 Trace-and-Amplify 脉络下的"训练数据来源"消融，加上一个时间轴，主会分量偏中等。
- 在 overwrite-tests 上，t ≤ 80 时检查点与初始模型可能几乎没有漂移。原博文的探针 AUROC 为 0.99，C2 有较大可能落入天花板或无差异区。预案已覆盖这种情况，但这意味着证据主要压在 Trace-and-Amplify 一个测试床上。

值得继续：修正定位后，新意仍然成立。

## Claim 判断
| Claim | 判断 | 关键依据 |
|---|---|---|
| 现有失败：提示诱导监控器对训练期自然投机泛化差 | 成立（已有证据） | Trace-and-Amplify 原文：只用一份 800 条提示诱导集，未写明生成模型，未做风格控制，也未变动诱导者或时点，与 brief 描述一致 |
| 现有失败：固定监控器在 RL 中准确率下降约 16 点 | 成立 | Engels/Nanda 博文："~16 point drop"，LLM judge 从 67% 降到约 50%；但该探针的训练正例来自已 RL 投机的模型，brief 没有提这一点 |
| "诱导者 × 时点从未被操纵过" | **部分被覆盖，表述不实** | EleutherAI Reasoning Interpolation 已在多检查点上比较多种诱导者（用于预测投机率），brief 却称其"不比较诱导者" |
| C1：检查点诱导的策略类别分布更接近之后的自然投机 | 部分重合 | EleutherAI 做过检查点诱导率的变化趋势，PRIME 显示前兆先于投机；但"诱导样本类别分布与之后自然投机的距离"没人测过 |
| C2：只用 t 时可得数据训练的前瞻监控器，召回高于初始模型诱导和等预算自然采样 | 新颖 | 未检索到用中途检查点诱导数据训练监控器、再在 t 之后评测召回的工作；对照设计能区分"数量"和"分布"两个因素 |
| C3：用更大的非 RL 模型诱导拆分"能力 vs RL 分布"；在规范化代码上检验风格 | 新颖（作为检验） | Trace-and-Amplify 只有定性解释，没有风格控制实验；EleutherAI 比较了跨家族 donor，但没有在监控器层面做拆分 |

## 最高近邻
1. **Trace-and-Amplify**（Li et al., arXiv 2604.23488, https://arxiv.org/abs/2604.23488）
   - 重叠：在同类测试床上比较提示诱导数据与训练期自然数据训练出的监控器。
   - 差别：诱导数据只有一份、静态，没有诱导者或时点变量，也没有风格控制。
2. **Early Indicators of Reward Hacking via Reasoning Interpolation**（EleutherAI, David Johnston, 2026-04, https://blog.eleuther.ai/reward-hacking-indicators/）
   - 重叠：在各检查点上用多种诱导者引出 exploit，并比较诱导者。
   - 差别：目的是预测投机率趋势，不训练监控器；被训练的模型用 SFT（GPT-OSS-20b），不是 RL。
3. **The Impact of Off-Policy Training Data on Probe Generalisation**（Kirch et al., arXiv 2511.17408, https://arxiv.org/abs/2511.17408）
   - 重叠：生成策略（on/off-policy、诱导）对探针泛化的影响；以"意图"定义的行为最敏感。
   - 差别：针对静态模型，没有策略漂移或时间维度。
4. **Steering RL Training: Benchmarking Interventions Against Reward Hacking**（ariaw/Engels/Nanda, https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against）
   - 重叠：同一测试床；在冻结基座激活上训练探针，正例取自已 RL 投机的模型；报告了监控器在训练中衰减。
   - 差别：没有在投机出现前构造监控器，也没有比较诱导来源。
5. **PRIME**（Beigi et al., arXiv 2606.09711, https://arxiv.org/abs/2606.09711）
   - 重叠：在代码 RL 中，探针前兆先于投机，可预测投机何时出现、有多严重。
   - 差别：是早期预警测量，不构造投机监控器，也不比较诱导数据来源。

```json
{
  "score": 7.6,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "claim blocker: '诱导者×时点从未被操纵过' 及 'EleutherAI reward hacking indicators 不比较诱导者' 与可核验事实冲突——EleutherAI Reasoning Interpolation 已在多检查点上比较同模型 donor / 跨家族 Qwen3-8B / 提示 Claude 等诱导者（用于投机率预测）；新意边界需收窄为'检查点诱导数据作为监控器训练集，并在 RL 中做前瞻召回评测'"
  ],
  "novelty_conclusion": "以检查点诱导数据训练监控器、并在 RL 投机出现前做前瞻召回评测，未见先例，C2/C3 新颖；但'诱导者×时点'作为变量已被 EleutherAI 用于投机率预测，现有定位不实；整体属于 Kirch et al. / Trace-and-Amplify 脉络下的数据来源消融加时间轴，分量中等。",
  "closest_neighbors": [
    "Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking? (Trace-and-Amplify, arXiv 2604.23488)",
    "Early Indicators of Reward Hacking via Reasoning Interpolation (EleutherAI blog, 2026-04)",
    "The Impact of Off-Policy Training Data on Probe Generalisation (arXiv 2511.17408)",
    "Steering RL Training: Benchmarking Interventions Against Reward Hacking (Engels/Nanda MATS post)",
    "PRIME: Proxy Reward Internalization and Mechanistic Exploitation (arXiv 2606.09711)"
  ]
}
```
