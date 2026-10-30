## 结论

截至 2026-10-29：**score 7.0 / 10，verdict = promising_needs_revision**。

核心新意是在策略漂移、自然投机尚未出现时，把"诱导者 × 诱导时点"作为操纵变量来构造前瞻监控器。检索范围内没有找到已有工作做这件事：

- Trace-and-Amplify 未写明 PE 数据由哪个模型、哪个检查点生成，也没有做时点或诱导源的对比；
- Kirch et al. 只研究静态模型；
- PRIME、SimHack、EleutherAI 做的是预测投机何时出现，不构造监控器；
- CATCH 测的是召回衰减，但监控器是零样本 LLM。

因此主张 C1 的"分布逼近"部分和 C2 基本成立为新意。两个 baseline 仓库我已用浅克隆核验：`create_all_datasets` / `run_rl_training` / `train_probe` / `eval_model` 在 `commands.sh` 中存在，`save_steps` 默认 50；T&A 的四个脚本路径均存在。算力（约 1,300 A100 小时）和 API 预算都在约束内。

但主对比 C2 仍有两处设计缺陷，会让结论无法归因到"投机分布"，所以本轮不能给 experiment_ready：

1. **负例来源与正例来源错配。** 800 条负例固定不变，且取自检查点 t 的无指令样本。来源 1 的正例来自初始模型，来源 2 的正例来自更大的模型，它们与负例之间存在"生成模型"的风格差。监控器会学到"初始模型风格 = 投机"这条捷径。到 t 之后的评测窗口，正负例都来自后期检查点，这条捷径失效，来源 1 被系统性压低。结果是 C2 的优势可能只来自正负例同源，而不是投机分布更接近。AST 规范化只去掉注释和格式，消除不了代码习惯层面的来源差。
2. **主测试床上正例纯度的论断不成立。** overwrite-tests 中，正确解同样能通过代理奖励。"无指令失败、被指示后通过"并不能只用代理信号排除"被指示后写出正确解"的情况。Qwen3-4B 在中/难题上的单次解出率不低，正例污染可能可观。T&A 有矛盾伪测试，这条论断在那里成立；在主测试床上不成立。

C1 中"能力先于倾向"的子主张与 PRIME（能力型前兆先于持续投机出现）和 2609.16268（捷径只在工具已学会后形成）部分重合，只能算对已有现象的复测。

整体值得继续：新意边界基本站得住，以上问题可在不改变 Claim 的前提下修正。另有一个经验风险：overwrite-tests 的投机在词面上很显眼（Engels 的探针 AUROC 达 0.99），初始模型诱导的 baseline 可能已接近天花板，留给 C2 的差距空间不大。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 现有失败：PE 监控器对训练期投机泛化差 | 已有证据（引用正确） | T&A 报告 PE 训练的监控器在训练期投机上仅 28%；PE 生成模型与检查点确实未写明，本文所称的"未操纵变量"属实 |
| C1 诱导分布随检查点逼近 | 新颖 | 未见以检查点或时点作为诱导源变量的工作；EleutherAI 用中间检查点加 donor 预填估计利用率，目的是预测，不比较诱导分布 |
| C1 子主张：能力先于倾向（指令投机成功率曲线） | 部分重合 | PRIME 2606.09711 显示能力型前兆早于持续投机；2609.16268 显示捷径在工具学会后形成 |
| C2 前瞻监控召回高于初始诱导与等预算自然采样 | 新颖，但当前设计不可归因 | 负例固定取自检查点 t，与来源 1/2 的正例来源错配，引入风格捷径；overwrite-tests 正例纯度不能只靠代理信号保证 |
| C3 能力与分布拆分、风格检验 | 新颖但检验力弱 | 大模型诱导的拆分合理；AST 规范化只控制注释和格式，控制不了来源层面的代码风格 |
| 定位关键词与 baseline | 合格 | 关键词均为已有术语；两个测试床同属代码 RLVR 训练期投机监控，代码可获取，复现路径具体 |

## 最高近邻

1. **Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking?（Trace-and-Amplify）** https://arxiv.org/abs/2604.23488
   - 重叠：PE 与训练期自然投机的监控泛化对比，同模型、同测试床。
   - 差别：不操纵诱导者和时点，PE 来源未写明，没有前瞻（t 之前训练、t 之后评测）设置。
2. **The Impact of Off-Policy Training Data on Probe Generalisation（Kirch et al.）** https://arxiv.org/abs/2511.17408
   - 重叠：生成方式对探针泛化的影响，on-policy 与 incentivised 数据对比。
   - 差别：针对静态模型、自然正例存在，不涉及 RL 漂移和目标行为出现前的时点。
3. **PRIME: Proxy Reward Internalization and Mechanistic Exploitation** https://arxiv.org/abs/2606.09711
   - 重叠：代码 RL 中投机前兆按检查点追踪，探针预测投机起点。
   - 差别：预测起点和严重度，不构造投机监控器，不比较诱导源。
4. **Early Indicators of Reward Hacking via Reasoning Interpolation（EleutherAI）** https://blog.eleuther.ai/reward-hacking-indicators/
   - 重叠：在中间检查点用 donor 或提示诱导的预填估计利用倾向，并比较不同 donor 来源。
   - 差别：基于 SFT 检查点而非真实 RL，目标是预测哪类利用会出现，不训练监控器。
5. **Steering RL Training / Designing Effective Monitor-Based Interventions for Mitigating Reward Hacking During RL（Engels/Nanda 指导，ICML 2026）**
   - 链接：https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against ；https://icml.cc/virtual/2026/79298
   - 重叠：同一测试床；探针训练在冻结基座激活上进行；报告了监控器准确率在训练中下降。
   - 差别：其探针正例来自已完成 RL 的投机模型，属于投机出现后的数据，不研究投机出现前的构造。

```json
{
  "score": 7.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "C2 主对比混杂：800 条负例固定取自检查点 t，与来源 1（初始模型）和来源 2（更大模型）的正例来源错配，监控器可学到生成模型风格捷径，C2 优势无法归因到投机分布；AST 规范化不足以排除",
    "overwrite-tests 上正确解同样通过代理奖励，'无指令失败、指令后通过'无法只靠代理信号排除正确解，正例纯度论断在主测试床上不成立"
  ],
  "novelty_conclusion": "以诱导者×诱导时点为操纵变量、在投机出现前构造前瞻监控器的设定，在已检索文献中未见，C1 分布逼近与 C2 具备新意；C1 的'能力先于倾向'子主张与 PRIME、2609.16268 部分重合；与 Trace-and-Amplify 和 Kirch et al. 去名后仍可区分。",
  "closest_neighbors": [
    "Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking? (arXiv 2604.23488)",
    "The Impact of Off-Policy Training Data on Probe Generalisation (arXiv 2511.17408)",
    "Proxy Reward Internalization and Mechanistic Exploitation (PRIME, arXiv 2606.09711)",
    "Early Indicators of Reward Hacking via Reasoning Interpolation (EleutherAI blog)",
    "Designing Effective Monitor-Based Interventions for Mitigating Reward Hacking During RL (ICML 2026 / Steering RL Training post)"
  ]
}
```
