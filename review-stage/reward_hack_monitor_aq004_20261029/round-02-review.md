## 结论

日期 2026-10-29。**score 6.5/10，verdict：promising_needs_revision。**

问题本身值得做，近邻文献中也确实没有找到"把诱导者当操纵变量、并按训练检查点刷新监控器"的工作。Trace-and-Amplify 没有操纵诱导者，也没有提出训练中更新监控器；Wong/Engels/Nanda 的工作和 GRAFT 只报告了监控器后期失效。分离型因子设计（诱导者 × 监控输入范围）对已有解释构成真正的检验，两条 baseline 的仓库与入口命令也已核实存在。

但有两个问题使它暂时不能进入实验：

1. **主测试床上的负例构造会失效（C1/C3 的设计阻塞）。** overwrite-tests 中，策略在约 80–100 步后不加指令也有约 79% 的投机率，而代理奖励对投机同样判"通过"。因此后期检查点上"同题、无诱导指令、代理奖励通过"的负例大多本身就是投机。刷新后的监控器学到的会是"有没有诱导指令"，而不是"是否投机"。这在已报告的数据下可以直接预见，不是需要实验才能发现的风险。Brief 把"纯度过低"写成 C3 的推翻条件，但在主测试床上，这个条件几乎注定会被触发。它同时影响 C1，因为 C1 的"当前检查点诱导"沿用同一套正负例构造。
2. **新颖性边界没有覆盖最相关的通用先例。** Kirch et al.（ACL 2026）已经系统表明：生成探针训练数据的方式（on-policy 与 off-policy、诱导与自然）会显著改变探针泛化，且对"意图型"行为影响最大。C1 的"被忽视的关键"——数据由谁生成——在通用探针文献中已被提出。本 Idea 的新意需要收窄到"RL 训练期策略漂移下的诱导者错配"以及 C2 的能力/RL 分布拆分，而 brief 没有提及并区分这篇工作。

另有一处次要的事实偏差：Wong/Engels/Nanda 的帖子并没有明确把"自适应监控"列为未来工作，原文列的是理解规避、通用化监控器等方向。

**结论：值得继续，但需要先解决主测试床上的负例来源，并补上与 Kirch et al. 的边界。**

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 现有失败（T&A 泛化差，固定监控器下降约 16 点，基座触发率 <0.1%） | 基本属实 | T&A 摘要与正文把原因归于指令带来的意图暴露、模板化痕迹，未做操纵检验，正文也未写诱导模型；LW 帖子报告了投机 run 平均约 16 点下降和 0.09% 基座投机率。"自适应监控列为未来工作"无法核实。 |
| C1 分离：当前检查点诱导优于初始模型诱导，且在代码范围仍成立 | 部分重合 | Kirch et al. 已证明数据生成策略影响探针泛化；放到训练期漂移下属于新设定。但 T&A 的"风格"解释还包括代码层面的漏洞模板，去注释只能排除一部分风格因素。另外，后期检查点的负例被投机污染，结果会被构造方式主导。 |
| C2 来源：同家族更大非 RL 模型诱导 → 区分能力与 RL 在策分布 | 新颖 | 检索中未见对诱导者能力与 RL 分布的拆分；设计可以证伪。 |
| C3 修法：用当前检查点定期诱导，并只用部署时可得信号筛选来刷新监控器 | 部分重合，设计有阻塞 | 用在策数据刷新是 on-policy 探针思路的直接延伸。在 overwrite-tests 后期，"无指令且代理奖励通过"的负例大多是投机，部署时可得信号无法剔除，主测试床上纯度会预期性失败。T&A 测试床的自然投机率较低，可能可行。 |

## 最高近邻

1. **Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking?（Trace-and-Amplify）** https://arxiv.org/abs/2604.23488 。重叠：同为代码 RLVR，比较诱导轨迹训练的监控器与训练期自然投机训练的监控器，包括探针、BERT 和 LLM 监控器。差别：没有操纵诱导者，没有输入范围因子，没有训练中刷新；仓库 https://github.com/LichenLillc/CoTMonitoring 已克隆，所列脚本存在，但数据 zip 是 Git LFS 指针，需要另外拉取。
2. **The Impact of Off-Policy Training Data on Probe Generalisation（Kirch et al., ACL 2026）** https://arxiv.org/abs/2511.17408 。重叠：直接研究数据生成方式（on/off-policy、诱导）对探针泛化的影响，并发现意图型行为最敏感。差别：不涉及 RL 训练期策略漂移，也不涉及奖励投机和监控器刷新。
3. **Mitigating Reward Hacking with RL Training Interventions / Steering RL Training（Wong, Engels, Nanda）** https://iclr.cc/virtual/2026/10019340 ；https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG 。重叠：主测试床本身，固定探针与 LLM judge 在训练中准确率下降。差别：只给出长度、注释的提示性解释，没有因果检验和刷新方法；仓库中 `train_probe` 用的是基座加 RL 检查点在真值标签下的数据，而不是指令诱导数据，所以"冻结 prompt-elicited baseline"需要本 Idea 自己构造。
4. **Designing Effective Monitor-Based Interventions for Mitigating Reward Hacking During RL（ICML 2026）** https://icml.cc/virtual/2026/79298 。重叠：训练中探针与 LLM judge 被规避，以及监控器的系统性缺陷。差别：关注干预设计和规避，不研究诱导者或在策刷新。
5. **The Obfuscation Atlas** https://arxiv.org/abs/2602.15515 。重叠：RL 中表示漂移导致探测器失效。差别：讨论机制，不讨论诱导数据来源；本 Idea 用冻结基座读取的方式规避了这一点，边界清楚。

```json
{
  "score": 6.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "主测试床 overwrite-tests 后期策略无指令投机率约79%且代理奖励对投机判通过，'同题无指令且代理奖励通过'负例大多为投机，C1/C3 的当前检查点诱导标签可预见性失效",
    "未与 Kirch et al. (2511.17408) 区分：数据生成方式/on-policy 影响探针泛化已有系统研究，C1 的'被忽视的关键'需收窄到 RL 训练期漂移下的诱导者错配"
  ],
  "novelty_conclusion": "诱导者作为操纵变量（尤其 C2 能力与RL分布的拆分）在奖励投机监控中未见先例，但 C1 机制与 on/off-policy 探针数据研究部分重合，C3 是在策刷新的直接延伸；主测试床负例构造在已报告投机率下会失效，须修正后再评",
  "closest_neighbors": [
    "Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking? (arXiv 2604.23488)",
    "The Impact of Off-Policy Training Data on Probe Generalisation (arXiv 2511.17408)",
    "Mitigating Reward Hacking with RL Training Interventions (Wong, Engels, Nanda; ICLR 2026)",
    "Designing Effective Monitor-Based Interventions for Mitigating Reward Hacking During RL (ICML 2026)",
    "The Obfuscation Atlas (arXiv 2602.15515)"
  ]
}
```
