## 结论
2026-11-06：总体 score 6.8，verdict = promising_needs_revision。主贡献是一个可逐运行检验的解释：在每批只更新一次、裁剪几乎不生效的随机奖励 RLVR 中，一次运行是在冻结检查点的输出约定之间抽签；终点准确率约等于所选约定的冻结条件准确率；抽签概率因 logit 参数化下的二阶漂移而比初始质量更平；随机奖励结果的分布可以在训练前从冻结采样读出。这条主线具体、可证伪，可行性也够。但三项都只到 7 档：输出约定这一部分已被 2610.01066 自己部分指出，二阶展开与 2512.16912 定理 4.1 相同，而共享参数下的“压平”还缺少直接依据。因此没有一项够得上 8，不满足放行门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 7.0 | 若成立，2610.01066 的“autodidactic / 可达性探针”读法（P2+5B 均值 +26.8、四个种子 59–77.5%）会被改写为“约定抽签＋约定内无能力增长”，并得到一个训练前就能预测均值、崩溃率和高尾的工具。这会改变 spurious-reward 争论中一条主要的经验判断。限制有两点。其一，2610.01066 正文已承认 “output conventions contribute to the measured behavior”，宽松增益“do not by themselves give a format-independent measure”（Table 7、§11.7 的 `####`/`\boxed` 比例 93.5%→51.8%/47.4%），所以增量主要是定量化和可预测性。其二，范围是单一家族、96 token、LoRA 的小批量设定，主张也明确不覆盖 Qwen 和大批量设定。 |
| 新颖度 | 7.5 | 在目标领域，没检索到“从冻结采样预测随机奖励终点分布”或“逐运行检验增益是否只是换约定”的工作。各模式定局概率比初始质量更平，与 2601.04411 的 J=0 neutral 及其 p 空间 Wright–Fisher 噪声（隐含定局概率＝初始质量），以及 2605.00365 的 Pólya urn 类比（同样隐含按初始比例），给出的是不同的可检验预测。不过，二阶漂移本身是 2512.16912 定理 4.1 和 2610.01066 §9.4 同一展开的逐分量版本。“增益来自格式/约定变化”也已有 2610.01066 Table 7/22 以及 VLM 场景的“format compliance × accuracy given compliance”分解（NeurIPS 2026 workshop）。所以新意是有内容的综合，加上一个新的定量预测，不是独立的新机制。 |
| 有效性（先验合理性） | 7.0 | 现有依据有四条。①我用数值二阶导核对了漂移式，在 p=(0.6,0.3,0.1) 下与解析式逐位一致（−0.0238/+0.0232/+0.0005）。②表格模拟复现了压平：组内标准化时胜出频率约 0.44/0.35/0.21，不标准化时约 0.50/0.37/0.13。③2610.01066 的数据与图景一致：15 个宽松≥50% 的随机运行中几乎全部严格分为 0；有模板的随机 token 输入可到 68.5%，无模板时停在 14.5–23%，说明结果依赖模板引出的约定而非题目内容；裁剪标记步仅约 0.24%（Table 6），一次更新、裁剪基本不生效的前提成立；Table 22 前缀分 P1 41.5→21–29、P2 14.5→38–39。④由 verifier 不变性，随机奖励不携带正确性信息，约定内能力无从由奖励注入。没有发现与关键假设直接矛盾的已有证据。有两个未处理的跳跃。(a) LoRA＋AdamW 共享参数下，分叉 token 能否等效为跨题共享的低维 softmax，以及 Adam 的逐参数归一化是否保留压平，目前没有依据，只是可检查。(b) 压平依赖运行在 500 步内定局。我的模拟显示有效步长小、未定局时，终点 argmax 反而偏向主导模式（η=0.1、500 步时 0.69/0.31/0.00，比初始 0.6/0.37/0.03 更集中）。因此“压平 / 中性 / 集中”的判别与定局程度混在一起，表格映射的有效步长也是一个未定的自由参数。 |
| 待预研（不计分） | — | P2 冻结采样里是否有质量≥3%、条件准确率≥50% 的约定；压平幅度在真实 LoRA 下有多大；预测分布相对中性固定、起点准确率/错配模型能好多少；裁剪臂的反转幅度。 |

与起点问题的关系：Idea 回答的是起点问题的一个子问题，即“学习者一侧什么决定随机奖励效果”被具体化为“冻结采样里有无高准确率且质量不可忽略的约定”。仍未回答的是 mid-training 的哪部分数据造出这些约定，以及大批量全参数设定下 Qwen 的约定内提升。转向本身不构成阻断。

实验能否判别：判断 (1) 逐运行区间检验和 (3) 预登记的 4 个检查点预测，能直接区分“约定抽签”与“约定内能力增长 / 可达性”。零奖励臂把参考项和权重衰减漂移分离出来，离线臂复现了 Table 1 的设置，竞争解释覆盖较全。仍有三个弱点。其一，判断 (2) 和 (4) 的“胜出”按终点多数约定计，没有按运行的集中程度分层或建模，未定局运行会系统性偏向主导约定，可能把压平误判为中性或集中。其二，表格映射里的有效步长与定局时间需要在预登记前从非预登记检查点定死，否则 (3) 有可调参数。其三，(1) 的区间是“T=1 条件准确率”到“约定内多数投票准确率”，若某些约定这两个值相差很大，区间就太宽、难以证伪，需要报告区间宽度分布。这几点属于 Claim 的判别力问题，不影响可行性。

可行性：pass。我核实了几项：仓库 `mynotwo/rl-random-prob` 可 clone；`src/trainer/rlvr_probe_v2_fixedsplit.py` 有 `--reward_mode zero/random`、`--clip_eps`、`--disable_clipping`、`--ppo_epochs`、`--accum_steps` 并保存逐题 `outcomes`；`src/shared_rollout/train_shared_rollouts.py` 为 AdamW wd=0、无比值/裁剪/KL；`src/data/synthetic_gsm_rlvr_1000_seed13.jsonl` 和 `configs/olmo2_checkpoints.json` 都存在。论文的训练超参与 brief 一致（lr 3e-5、LoRA r8、G=4、随机臂参考系数 0.01）。缓冲区 PPO 循环约 80 行，复用现有采样和损失，路径可信。总计约 265 A100 小时，8×A100 约 1.5 天，在 ≤5 天约束内。预研只做 P1 末与 P2+5B 的冻结采样（约 4 小时），本身可以给出 no-go。不需要付费 API，也不需要人工标注。约定划分基于输出文本规则，标签含义就是训练器可复现的输出特征，与三种评分口径分开计算，没有混淆。

## 最高近邻
1. Probe with Participation Trophies（2610.01066，https://arxiv.org/abs/2610.01066）：同协议、同检查点。有 Table 1 共享 rollout 对比、Table 7 格式诊断、Table 22 前缀评分，§9.4 只给出符号不定的二阶项。它没有把增益分解为约定抽签，也没有给出预测或逐运行检验。
2. Exploration vs Exploitation: Clipping, Entropy, and Spurious Reward（2512.16912，https://arxiv.org/abs/2512.16912）：定理 4.1 用同一二阶展开得出偏斜策略熵上升，定理 4.3 证明裁剪降熵。它只在熵层面，不讨论各模式定局概率和输出约定。
3. Rate or Fate? RLVεR（2601.04411，https://arxiv.org/abs/2601.04411）：多臂 bandit 的 replicator 流，J=0 为 neutral，p 空间 Wright–Fisher 噪声。它隐含定局概率＝初始质量，正好是本 Idea 要证伪的竞争预测。
4. Spurious Rewards: Rethinking Training Signals in RLVR（2506.10947，https://arxiv.org/abs/2506.10947）：裁剪偏置放大高先验行为（Qwen 代码推理），报告 OLMo2 无增益。它对应大批量、裁剪生效的设定，在本 Idea 中是方向相反的对照。
5. Uniform-Correct Policy Optimization（2605.00365，https://arxiv.org/abs/2605.00365）：GRPO 在正确解之间自我强化地坍缩，用 Pólya urn 作类比，log-ratio 为正漂移的 submartingale。它研究的是正优势下的集中，与零均值随机优势下的压平预测相反，也不涉及输出约定。

```json
{
  "score": 6.8,
  "contribution_scores": {"importance": 7.0, "novelty": 7.5, "effectiveness": 7.0},
  "contribution_assessment": "主贡献：在一次更新、裁剪不生效的随机奖励RLVR中，运行是在冻结检查点输出约定间的抽签，终点准确率≈所选约定的冻结条件准确率，胜出概率因logit二阶漂移比初始质量更平，因而可从冻结采样在训练前预测结果分布。重要性7：若成立会把2610.01066的可达性/autodidactic读法改写为约定抽签，但该文已承认输出约定贡献了宽松增益，且范围限于OLMo-2短回答LoRA设定。新颖度7.5：训练前预测与逐运行检验在目标领域未见，压平与2601.04411/2605.00365的按初始质量定局预测不同；但二阶展开同2512.16912定理4.1，格式解释已部分存在。有效性7：漂移式与压平经数值核对成立，2610.01066的Table 6/7/22与随机token输入对照均与图景一致，无直接反证；未解决的跳跃是LoRA+AdamW共享参数下低维softmax等效与压平是否保持，以及500步内是否定局（未定局时argmax偏向主导约定，与压平判别混在一起，有效步长为自由参数）。三项均未达8，不满足门槛。",
  "feasibility": "pass",
  "feasibility_reason": "仓库、训练器（reward_mode zero/random、clip开关、outcomes保存）、共享rollout训练器（wd=0无裁剪）、合成GSM数据与检查点配置均已核实可得；缓冲区PPO约80行可复用现有组件；总计约265 A100小时，8×A100约1.5天，预研4小时可给出no-go；无付费API、无人工标注。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：重要性7.0、新颖度7.5、有效性7.0，没有一项≥8",
    "Claim判别力：胜出约定按终点多数计，没有按运行定局程度分层；在未定局区间argmax会系统性偏向主导约定，判断(2)(4)可能把压平误判为中性或集中；表格映射的有效步长未在预登记前固定"
  ],
  "novelty_conclusion": "目标领域未见从冻结采样预测随机奖励终点分布或逐运行约定检验的工作；压平预测区别于2601.04411与2605.00365隐含的按初始质量定局。但二阶漂移与2512.16912定理4.1同源，输出约定解释已在2610.01066 Table 7/22部分出现，属于有内容的综合与新的定量预测，不是独立新机制。",
  "closest_neighbors": [
    "Probe with Participation Trophies: Random-Reward RL as a Probe of LLM Capability (2610.01066)",
    "Exploration vs Exploitation: Rethinking RLVR through Clipping, Entropy, and Spurious Reward (2512.16912)",
    "Rate or Fate? RLVεR: Reinforcement Learning with Verifiable Noisy Rewards (2601.04411)",
    "Spurious Rewards: Rethinking Training Signals in RLVR (2506.10947)",
    "Uniform-Correct Policy Optimization: Breaking RLVR's Indifference to Diversity (2605.00365)"
  ]
}
```
