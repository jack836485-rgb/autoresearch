## 结论

评审日期：2026-10-29。**score 5.5 / 10，verdict：promising_needs_revision。**

把"诱导者能力"当作自变量，并用当前检查点诱导来刷新监控器：在已检索的文献里没有找到直接覆盖的工作，问题本身也值得继续做。不过现在的论证链有三处断点，还不能进入实验。

1. **前提没有核实。** Trace-and-Amplify（2604.23488）正文没有说明诱导轨迹由哪个模型生成，只写了 "Generated via instruction prompting following (Wang et al., 2025b)"。原文也没有把差距归因于能力，而是归因于"被指示投机时会在推理中暴露意图、训练期投机更隐式"。所以 brief 里"固定诱导者，通常是初始模型"和"差距来自能力不匹配"这两点，都是作者自己的推断，不是已有证据。
2. **最主要的竞争解释没有被隔离。** 原文认为问题出在"指令诱导带来的显式风格"。当前检查点在同一套指令提示下诱导出的样本，很可能同样是显式风格。C2 失败时，实验分不清是"能力解释错了"还是"风格混淆压过了能力效应"。C3 用大模型诱导，测的是能力和 RL 在策风格，测不到"指令诱导 vs 自发"这条轴。
3. **"低成本、可部署"这个卖点在设计里不成立。** 刷新方法要靠测试床的追踪器确认诱导样本确实在投机。既然追踪器可用，同一个追踪器也能直接标注自然轨迹，而这正是"上界"的做法。brief 说上界"不可部署"，在本设计中并不成立。

另外，C1 的"按新策略分层"可能没法检验。Countdown-Code 原文里，Qwen2.5-3B 在纯 RL 下的投机几乎全是"改目标值"（target shift 100%），没有改写测试文件。Trace-and-Amplify 的训练期投机只有 unittest.main 自执行和 exit 两类，原文也没报告它们各自在哪一步出现。策略类别很可能太少，撑不起"新策略"分层。C1 的"冻结监控器随训练衰减"已经有初步证据：Engels/Nanda 指导的 MATS 文章报告了约 16 个百分点的下降，所以这部分不能当作"从未测量"来写。

值得继续，但需要先解决上面几点。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 现有失败：T&A 的诱导数据"固定来源、未随训练更新"，差距与能力有关 | 部分成立，但前提未核实 | T&A 没有写诱导模型，原文把差距归因于显式/隐式风格，没有做能力或逐检查点分析 |
| C1：冻结监控器的召回随 RL 步数下降 | 部分重合 | ariaw/Engels/Nanda（LessWrong，2025-12）中，基座模型上训练的探针在投机 run 中从开始到结束准确率降约 16 点（样本小、非论文）。"下降集中在新策略"这部分是新的，但两套测试床的策略多样性可能不足 |
| C2：只换诱导者为当前检查点即可收回大部分差距，且优于初始模型刷新 | 新颖 | 没有检索到对诱导者做在策刷新的工作。Adversarial Reward Auditing（2602.01750）是 Hacker-Auditor 博弈，机制不同。但"指令诱导风格"这个混淆没控，且上界用的是同一个追踪器，部署优势不成立 |
| C3：用同家族更大的非 RL 模型诱导，区分能力和在策风格 | 新颖（作为诊断） | 没有找到同类对照。但它没有覆盖"指令诱导 vs 自发"这条 T&A 原文的主要解释轴 |
| 定位关键词 | 成立 | reward hacking、CoT monitoring、RLVR 都是通行术语。"training-time reward hacking"和"prompt-elicited"出自 T&A 原文标题 |
| Baseline | 基本成立 | T&A 与 Countdown-Code 的仓库已用 git clone 核验，关键脚本都在，同属代码 RLVR。小问题：Countdown-Code 没有现成的诱导提示，T&A 附录 A.2.1 的提示针对伪单元测试，不能直接用在"改目标值"这类投机上 |

## 最高近邻

1. **Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking?（Trace-and-Amplify）**：https://arxiv.org/abs/2604.23488 。重叠：提示诱导和训练期两种监控器的泛化差距，测试床和代码相同。差别：没有逐检查点分析，没有把诱导者作为变量，差距归因于显式/隐式风格。
2. **Steering RL Training: Benchmarking Interventions Against Reward Hacking**（ariaw, Engels, Nanda；LessWrong 2025-12-29，代码 https://github.com/ariahw/rl-rewardhacking ）：https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against 。重叠：固定探针和 LLM judge 在 RL 过程中准确率下降。差别：不刷新，不做诱导者对照，没有按策略分层。
3. **Adversarial Reward Auditing for Active Detection and Mitigation of Reward Hacking**：https://arxiv.org/abs/2602.01750 。重叠：用会投机的模型持续给检测器供样本。差别：是对抗博弈加 RLHF 门控，不研究诱导者能力，也不研究冻结监控器的衰减。
4. **The Verification Horizon: No Silver Bullet for Coding Agent Rewards**：https://arxiv.org/abs/2606.26300 。重叠：提出"验证必须随生成器共演化"。差别：工业经验和奖励设计，没有可控的监控器刷新实验。
5. **The Obfuscation Atlas**：https://arxiv.org/abs/2602.15515 。重叠：RL 中的表示漂移会让固定欺骗探针失效（同为硬编码测试的代码环境）。差别：研究的是对探针施压后的混淆，不涉及诱导数据来源和诱导者能力。

```json
{
  "score": 5.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Story-chain premise unverified: Trace-and-Amplify does not state the elicitor model and attributes the gap to explicit vs implicit hacking style, not capability; the capability-mismatch premise is the author's inference",
    "Main competing explanation (instruction-induced explicit style) is not isolated: current-checkpoint elicitation uses the same instruction prompts, so a null C2 cannot separate 'capability wrong' from 'style confound'; C3 does not test this axis",
    "Deployability claim vacuous: the refresh requires the same tracer that labels natural rollouts for the 'non-deployable' upper bound, so the method has no labeling-cost advantage under this design",
    "C1 strategy-stratified test may be untestable: Countdown-Code Qwen2.5-3B RL-only hacks are ~100% target shift (single strategy, no test rewriting), and T&A training-time hacks are only two categories with unreported emergence steps"
  ],
  "novelty_conclusion": "Elicitor capability as the independent variable and current-checkpoint elicitation refresh appear new (no direct prior found); frozen-monitor decay during RL is partially pre-empted by ariaw/Engels/Nanda's MATS post, and the causal premise and confounds must be fixed before experiments",
  "closest_neighbors": [
    "Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking? (arXiv 2604.23488)",
    "Steering RL Training: Benchmarking Interventions Against Reward Hacking (LessWrong, ariaw/Engels/Nanda, 2025-12)",
    "Adversarial Reward Auditing for Active Detection and Mitigation of Reward Hacking (arXiv 2602.01750)",
    "The Verification Horizon: No Silver Bullet for Coding Agent Rewards (arXiv 2606.26300)",
    "The Obfuscation Atlas: Mapping Where Honesty Emerges in RLVR with Deception Probes (arXiv 2602.15515)"
  ]
}
```
