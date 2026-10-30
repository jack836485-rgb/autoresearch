## 结论

评审日期：2026-10-29。**评分 7.5/10，结论 promising_needs_revision。** 没有发现致命的新颖性、可行性或 Claim 阻塞，但还没到 experiment_ready。

**新颖性**
- 检索结果中，Trace-and-Amplify、Kirch et al.、EleutherAI、PRIME、SimHack、CATCH，以及 ICML 2026 的 monitor-intervention 论文，都没有做以下这件事：在自然投机出现之前，用 RL 检查点诱导出的数据训练监控器，再测它对之后自然投机的前瞻召回。这个问题本身是新的，C3 中"能力 / RL 分布 / 风格"的拆分也是新的。
- 但新颖性的边界偏薄。方法本身就是 Kirch et al. 的 incentivised 数据（同模型被诱导的样本可代理 on-policy）沿 RL 时间轴逐点重做。新增贡献几乎全落在实证结果上。

**可行性风险（不致命）**
- **漂移可能不足**：投机前的窗口只有 LoRA-GRPO ≤80 步，检查点与初始模型的诱导分布可能几乎没有差别。
- **天花板可能被触发**：Countdown-Code 只有"改目标值"一种策略，诱导提示又直接点出这一做法，初始模型诱导的监控器很可能已经到顶。overwrite-tests 的投机带有明显的词面特征，同样有天花板风险。
- 方案已预先约定天花板规则和漂移不足规则，所以结果仍可证伪。但若两个测试床都被判为不具信息量，C2 就会落空。

**其他核实结果**
- Baseline 都属于同领域、同任务（代码 RLVR 训练期投机监控）。三个仓库均已克隆核验，入口命令都在：`create_all_datasets`、`run_rl_training`、`train_probe`、`eval_model`；`save_steps` 默认为 50；Countdown-Code 的 `datagen/create_datasets.py`；CoTMonitoring 的 `BERT_pipeline.sh`。
- Countdown-Code 原文确认：Qwen2.5-3B-Instruct 在纯 RL 下会自然投机，100% 是改目标值，约 60%；但原文没有给出投机出现的步数，需要先试跑测定。
- 原文称 Trace-and-Amplify "每题 1024 个样本"，未能核实。该文的做法是"重采样直到出现投机"，带重试上限 K。

**是否继续**：值得继续。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 现有失败：提示诱导监控器对训练期自然投机泛化差 | 已有证据，非本文贡献 | 2604.23488 已直接报告；overwrite-tests 博客报告监控器准确率下降约 16 点；引用基本准确 |
| 被忽视点：投机出现前没有自然正例，检查点诱导数据未被用于训练监控器 | 新颖（检索未见） | EleutherAI 只用于预测投机率，且在 SFT 上；PRIME、SimHack 预测投机何时出现；均不构造监控器 |
| C1：检查点诱导的策略类别分布更接近之后的自然投机 | 部分重合 | "能力先于投机"已有 PRIME / 2609.16268 报告；按类别距离做检验是新的，但只在 overwrite-tests 上可做，且可能因漂移小而得到零结果 |
| C2：前瞻召回高于初始模型诱导和等预算自然采样 | 新颖，但与 Kirch 边界薄 | 本质是 Kirch incentivised 数据沿时间轴重做；有同源负例、同正例数子对照和混合负例三重控制，能与近邻区分；天花板风险高 |
| C3：用更大同家族模型拆分能力与 RL 分布，用 AST 规范化检验风格 | 新颖 | 近邻都没有做风格控制（T&A 已确认无此实验）；更大模型同时改变了风格与能力，解释不唯一，但不构成阻塞 |

## 最高近邻

1. **Trace-and-Amplify** — https://arxiv.org/abs/2604.23488
   - 重叠：提示诱导监控器 vs 训练期投机监控器，同为代码 RL，同样有 BERT / 探针 / LLM 监控器。
   - 差别：用静态诱导数据（生成模型未写明），重采样直到出现投机，不研究投机出现前的时点和检查点诱导，也没有风格控制。
2. **Kirch et al., The Impact of Off-Policy Training Data on Probe Generalisation** — https://arxiv.org/abs/2511.17408
   - 重叠：比较 on/off-policy 与 incentivised 数据，结论是 incentivised 数据可代理 on-policy。这是本 Idea 方法的直接来源。
   - 差别：面向静态模型，没有 RL 时间轴，也不涉及代码投机。
3. **EleutherAI, Early Indicators of Reward Hacking via Reasoning Interpolation** — https://blog.eleuther.ai/reward-hacking-indicators/
   - 重叠：在各检查点用同模型、跨模型、Claude 三类来源诱导 exploit。
   - 差别：在 SFT 上进行，用 IS 趋势预测投机率，不训练监控器。
4. **Designing Effective Monitor-Based Interventions for Mitigating Reward Hacking During RL（ICML 2026，Engels/Nanda 团队，同一 overwrite-tests 环境）** — https://icml.cc/virtual/2026/79298 ，代码 https://github.com/ariahw/rl-rewardhacking-ext
   - 重叠：同一测试床，同样用探针和 LLM judge 监控，报告了监控器被规避的现象。
   - 差别：研究的是干预设计和学习信号泄漏，不研究监控器训练数据取自哪个时点、来自哪个诱导来源。原文没有引用这篇。
5. **PRIME** — https://arxiv.org/abs/2606.09711 ；**SimHack** — https://arxiv.org/abs/2610.28707
   - 重叠：都预测代码 RL 中投机何时出现。PRIME 报告能力分阶段先于投机出现。
   - 差别：都不构造、不评测检测自然投机的监控器。

```json
{
  "score": 7.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "检索未见'投机出现前用 RL 检查点诱导数据训练监控器并测前瞻召回'的工作，问题与 C3 拆分新颖；但方法是 Kirch et al. incentivised 数据沿 RL 时间轴的直接延伸，新增贡献依赖实证结果。投机前漂移窗口短（≤80 步 LoRA），且 Countdown-Code 只有单一策略，天花板/零结果风险高。Baseline 同领域且仓库可复现，无致命阻塞。",
  "closest_neighbors": [
    "Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking? (Trace-and-Amplify, arXiv 2604.23488)",
    "The Impact of Off-Policy Training Data on Probe Generalisation (arXiv 2511.17408)",
    "Early Indicators of Reward Hacking via Reasoning Interpolation (EleutherAI blog, 2026-04)",
    "Designing Effective Monitor-Based Interventions for Mitigating Reward Hacking During RL (ICML 2026)",
    "PRIME (arXiv 2606.09711) / SimHack (arXiv 2610.28707)"
  ]
}
```
