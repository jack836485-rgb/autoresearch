## 结论

截至 2026-10-29：**score 7.5/10，verdict = promising_needs_revision，值得继续。**

新颖性：在已检索的文献中，没有工作把"诱导者是哪个检查点、在哪个时点诱导"当作操纵变量，检验它对之后自然投机的监控覆盖。最近的几篇各自只占一部分：
- Trace-and-Amplify：比较提示诱导数据与训练期自然数据。论文没写明诱导数据由哪个模型或检查点生成，也没有比较不同的诱导者。
- Kirch et al.：在静态模型上比较 on/off-policy 与 incentivised 数据。
- PRIME 和 EleutherAI indicators：用中间检查点预测投机何时出现，但都不构造监控器。

去掉 Trace-and-Amplify 的名字，Claim 依然成立。它要解决的是"投机出现前、策略在漂移时如何就位监控器"，不是去补那篇论文的实验，所以不构成致命的新颖性阻塞。

但边界偏窄。审稿人很可能把它看成 T&A 结论之上的一个变量扫描。论文能否站住，取决于 C1/C3 的机制拆分能否给出非平凡的结果。

两个测试床的代码都已核验，且与本任务同属代码 RLVR 场景：
- rl-rewardhacking 中 `run_rl_training`、`create_all_datasets`、`train_probe`、`eval_model` 均存在；默认 `save_steps=50`，需改为 20。
- CoTMonitoring 中 `train_script.sh`、`add_fake_test_final-ver.py`、`BERT_pipeline.sh`、`gpt_evaluate.py` 均存在。
- 算力在约束范围内。

未达 > 8 分，原因有四：

1. **对照 4 无法按设定构造。** 设计要求"每时点 800/800"，但 overwrite-tests 的基座自然投机率约 0.09%，步 20–60 时同时点真值自然正例几乎不存在，凑不出 800 条正例。这个对照要么违反"核心参数一致"，要么需要采样量级的说明。而它是 C2 的两个比较对象之一。
2. **前瞻监控器的标签存在混杂。** 正例来自带指令的提示，负例来自无指令提示。如果探针或文本分类器的输入包含提示部分，标签会经由指令文本直接泄漏。brief 没说明输入只取回答部分，或在中性提示下重新编码。此外，"被指示且代理通过"的样本可能其实是正确解。brief 只报告纯度、不做处理，正例噪声会直接影响 C2 的结论。
3. **C1 很可能在步 0 就饱和。** overwrite-tests 的漏洞只需定义 `run_tests()`，基座被明确指示时大概率已能成功。brief 预先登记了推翻情形，这点诚实，但主测试床可能只给出否定结果。另外，LoRA r=32 在出现投机前的漂移可能很小，C2 的效应量存在显著风险。
4. **两处引用表述偏强。**
   - 2604.01476 的摘要把早期失败归因于改写"嵌入了自身解无法通过的用例"，没有说是能力不足。
   - T&A 的解释是指令暴露意图、隐状态可分离，并没有做风格控制实验。"T&A 归因于风格"应改为"T&A 的定性解释"。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 现有失败：提示诱导监控器对训练期自然投机泛化差 | 已被覆盖（作为动机成立） | T&A 原文结论；Engels/Nanda 报告投机 run 中 judge 与探针准确率约降 16 点，基座率约 0.09%、80–100 步开始投机（已核验） |
| C1：检查点 t 诱导的策略类别分布比初始模型诱导更接近之后的自然投机；同时测"能力先于倾向" | 新颖（但有饱和风险） | T&A 没有比较诱导者或检查点；PRIME 的 direct probe 是让模型评估解，不是指令投机，也不测指令投机成功率曲线；EleutherAI 在中间检查点用前缀做 IS 估计投机率，场景是 SFT，也不比较分布 |
| C2：只用 t 时数据训练的前瞻监控器，召回高于初始模型诱导与同时点真值数据 | 部分重合 | "用诱导数据训练监控器"和"incentivised 数据可代替 on-policy"分别由 T&A 和 Kirch 覆盖；"诱导者 = 漂移中的当前检查点、投机出现前就位"是新的。对照 4 构造不可行、指令泄漏，这两点削弱其可检验性 |
| C3：用同家族更大非 RL 模型拆分能力与分布，用 AST 规范化检验风格 | 新颖 | T&A 没有去注释或规范化实验（已核对全文），只做了 UMAP 与案例分析；文献中未见这一拆分设计 |
| 读取方固定在冻结基座激活上，以排除表示漂移 | 已被覆盖（属于设计选择，不是贡献） | Engels/Nanda 的探针本就读基座第 34 层；Obfuscation Atlas 报告了表示漂移 |

## 最高近邻

1. **Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking?（Trace-and-Amplify）**：https://arxiv.org/abs/2604.23488
   - 重叠：同一问题（提示诱导与训练期自然投机的监控器泛化），同一类监控器（BERT、线性/MLP 探针、LLM），每组 800 条。
   - 差别：不操纵诱导者与时点，也不在投机出现前构造监控器，没有规范化控制。
2. **The Impact of Off-Policy Training Data on Probe Generalisation（Kirch et al.）**：https://arxiv.org/abs/2511.17408
   - 重叠：数据生成方式决定探针泛化，incentivised 数据可作为 on-policy 的代理。
   - 差别：研究对象是静态模型，自然正例存在，没有策略漂移，也没有时点变量。
3. **Steering RL Training: Benchmarking Interventions Against Reward Hacking（Engels/Nanda 指导）**：https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against
   - 重叠：同一测试床，同样有固定探针与 judge，并测到训练中准确率下降。
   - 差别：探针用真值数据训练，只用作干预手段，不研究诱导数据的来源。
4. **PRIME: A Learned Precursor to Reward Hacking**：https://arxiv.org/abs/2606.09711
   - 重叠：在代码 RL 中，用跨检查点的行为与激活信号，在投机出现前预测其发生时刻与严重度。
   - 差别：不做指令投机，也不构造投机分类器；作者明确说目标不是对投机回答分类。
5. **Reward hacking indicators（EleutherAI）**：https://blog.eleuther.ai/reward-hacking-indicators/
   - 重叠：在中间检查点通过诱导（推理前缀）预测之后的投机。
   - 差别：场景是 SFT 注入的 exploit，只预测投机率，不训练监控器，也没在真实 RL 中验证。

```json
{
  "score": 7.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "以'诱导检查点×时点'为操纵变量、在投机出现前构造前瞻监控器，并做能力/分布/风格三方拆分，这在已检索文献中未见；但它与 Trace-and-Amplify 和 Kirch et al. 部分重合，新颖性边界偏窄，要靠 C1/C3 的机制结果撑起来。基线同域、可复现、已核验，无致命阻塞。未达 8 分的原因：对照 4 在 800/800 设定下不可构造；指令文本可能经监控器输入泄漏标签，且正例未过滤；C1 在 overwrite-tests 上可能步 0 即饱和；两处引用表述偏强。",
  "closest_neighbors": [
    "Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking? (arXiv 2604.23488)",
    "The Impact of Off-Policy Training Data on Probe Generalisation (arXiv 2511.17408)",
    "Steering RL Training: Benchmarking Interventions Against Reward Hacking (Engels/Nanda, LessWrong 2025-12)",
    "Proxy Reward Internalization and Mechanistic Exploitation (PRIME, arXiv 2606.09711)",
    "Reward hacking indicators (EleutherAI blog, 2026-04)"
  ]
}
```
