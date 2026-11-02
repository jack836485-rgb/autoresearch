## 结论

截至 2026-10-29：**score 6.8 / 10，verdict = promising_needs_revision**。

我没有找到把"检查点诱导数据"当作监控器训练集、并在真实 RL 中评测它对之后自然投机的前瞻召回的工作，所以组合层面的新颖性成立。但新意幅度中等：方法本质上是把 Kirch et al. 的"incentivised（诱导同模型）数据"沿 RL 时间轴逐点重做，贡献主要是实证测量。C1/C3 的拆分（能力 / RL 分布 / 风格）让它比单纯的数据刷新更有科学含量。

baseline 方面，两个测试床同属代码 RLVR 训练期投机监控，代码都已克隆核验：
- rl-rewardhacking：`train_probe` 在冻结基座激活上训练探针，`save_steps` 默认 50，与 brief 一致。
- CoTMonitoring：`train_script.sh`、`add_fake_test_final-ver.py`、`BERT_pipeline.sh`、`gpt_evaluate.py` 均存在。

算力也在约束内。目前有一个阻塞没有解决：**部署性主张只放在 Trace-and-Amplify 上检验，但这个测试床与主张的前提冲突。**
- 它用 resample-until-hack 训练：脚本里 `GROUP_SIZE=1024`、`ROLLOUT_BATCH_SIZE=1`。从第 1 步起，就在策地挖出自然投机，并强化这些样本。
- 它的追踪器"通过矛盾测试即投机"本身就是训练时免费可得的完美标签。原文 5.1 节也直接用基座模型每题 2048 次采样收集到了自然投机。

因此在这个测试床上，"投机出现前没有在策自然正例"和"需要提前就位的监控器"两个前提都不成立。

主测试床 overwrite-tests 本身是合适的：基座投机率约 0.09%，约 80–100 步后才开始投机。但那里只检验分布性主张，而且步 20–80 之间策略漂移可能很小，C1/C2 有出零结果的风险。值得继续，但要先解决上面的阻塞，不能直接进入实验。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 现有失败：提示诱导监控器对训练期投机泛化差；固定监控器在训练中衰减 | 部分成立 | T&A（2604.23488）结论已核实。Engels/Nanda 博文核实到"投机 run 中监控准确率下降约 16 点、judge 从 67% 降到约 50%"，探针正例来自已 RL 投机的模型。"衰减从未被测量"的说法因此不成立，brief 已收窄为"投机出现前就位的监控器从未被测"，这个收窄后的版本成立。 |
| 被忽视的关键：目标行为出现前只能选"在哪个检查点诱导"，检查点诱导数据从未被当作监控器训练集 | 新颖（组合层面） | EleutherAI 只在 SFT 检查点上用诱导做投机率预测，不训练分类器。PRIME（2606.09711）用检查点探针预测投机何时出现，不构造投机监控器。GRIFT（2604.16242）在早期检查点做无监督梯度聚类检测，不涉及诱导数据。这几项都没有覆盖本主张。 |
| C1：检查点诱导的策略类别分布比初始模型诱导的更接近之后的自然投机 | 新颖，但有零结果风险 | 能力先于投机已有 PRIME / 2609.16268 支持。但在 overwrite-tests 上，步 20–80 的检查点相对基座可能变化很小；brief 预设了类别不足时的退路，没有预设"漂移不足"时的退路。 |
| C2：前瞻监控器的召回高于初始模型诱导和等预算自然采样 | 部分重合 / 存在阻塞 | 思路与 Kirch et al.（2511.17408）"incentivised 数据可代理 on-policy"相近，区别在于加入了时间维度。阻塞是 T&A 测试床中在策自然正例和免费标签从第 1 步起就存在，"部署性主张只在这里检验"因此自相矛盾。 |
| C3：用同家族更大的非 RL 模型拆分能力与 RL 分布；用规范化代码检验风格 | 新颖 | 在监控器层面做能力、RL 分布、风格的三方拆分，我没有找到先例。规范化代码对照能直接证伪风格解释，设计合理。 |

## 最高近邻

1. **Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking?（Trace-and-Amplify）** https://arxiv.org/abs/2604.23488
   - 重叠：同一个"提示诱导数据训练、训练期自然投机评测"的设定，同为代码 RLVR。
   - 差别：它用静态的提示诱导数据，不做检查点诱导，也不评测前瞻召回。但它的 resample-until-hack 加追踪器，等于从训练开始就提供了在策正例。
2. **The Impact of Off-Policy Training Data on Probe Generalisation（Kirch et al.）** https://arxiv.org/abs/2511.17408
   - 重叠：on/off-policy 与 incentivised 数据对探针泛化的影响；以意图定义的行为最难泛化。
   - 差别：研究对象是静态模型，不涉及 RL 漂移和投机。
3. **Early Indicators of Reward Hacking via Reasoning Interpolation（EleutherAI）** https://blog.eleuther.ai/reward-hacking-indicators/
   - 重叠：在各检查点诱导 exploit，并比较同模型 donor、跨家族模型、提示 Claude 三类诱导来源。
   - 差别：只用 SFT（GPT-OSS-20b），只预测投机率，不训练监控器。
4. **PRIME: A Learned Precursor to Reward Hacking** https://arxiv.org/abs/2606.09711
   - 重叠：代码 RL 中，跨检查点探针在可见投机之前预测投机何时出现。
   - 差别：预测的是投机的前兆能力，不构造投机检测器，也不比较诱导数据来源。
5. **Steering RL Training: Benchmarking Interventions Against Reward Hacking（Engels/Nanda 指导）** https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against
   - 重叠：同一个 overwrite-tests 测试床，测量了训练中固定探针和 judge 的准确率下降。
   - 差别：探针正例来自投机后的 RL 模型，没有在投机出现前构造监控器。

```json
{
  "score": 6.8,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "部署性主张只在 Trace-and-Amplify 上检验，但该框架用 resample-until-hack（group 1024、batch 1）从第 1 步起就挖出并强化在策自然投机，矛盾测试追踪器又是训练时免费可得的完美标签，'投机出现前无在策自然正例'和'需要提前就位的监控器'两个前提在此不成立，C2 的部署性结论无法在该测试床上成立"
  ],
  "novelty_conclusion": "未发现把检查点诱导数据当作监控器训练集并在真实 RL 中评测前瞻召回的工作，组合层面新颖；但核心动作相当于 Kirch et al. 的 incentivised 数据沿 RL 时间轴重做，新意幅度中等，主要价值在 C1/C3 的分布拆分实证",
  "closest_neighbors": [
    "Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking? (arXiv 2604.23488)",
    "The Impact of Off-Policy Training Data on Probe Generalisation (arXiv 2511.17408)",
    "Early Indicators of Reward Hacking via Reasoning Interpolation (EleutherAI blog)",
    "Proxy Reward Internalization and Mechanistic Exploitation (PRIME, arXiv 2606.09711)",
    "Steering RL Training: Benchmarking Interventions Against Reward Hacking (LessWrong/AF)"
  ]
}
```
