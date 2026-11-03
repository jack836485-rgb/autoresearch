## 结论
2026-11-03，总体 score 5.5，verdict：needs_rethink。主贡献是一项受控因素分解：解释 C-MTP 报告的 latent CoT 在 MATH 上的崩塌，到底来自轨迹冗长、题目难度还是误差累积。问题是真的，但这项贡献还不够，原因有三。第一，它补的是一个已知的、缺失的对照：C-MTP 原文已经给出冗长与误差累积两种解释，公开评论也指出了"真实度与轨迹质量混淆"。第二，现有数据已经部分不支持"冗长度主导"这个主假说。第三，C-MTP 的对比里有一个比冗长度更强的混杂：训练数据规模（385k 对约 7.5k 且只保留答对的轨迹），外加 CoT-SFT 在 MATH 上相当于什么都没训。brief 没有把它列为竞争解释，判别规则也没有覆盖它。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 弄清"结构化 benchmark 是否高估 latent CoT"、下一步该做轨迹凝练、展开训练还是状态监督，对这个子领域的方向判断有用。但证据范围是 1–1.5B、LoRA、两个题源，答案很可能是"按家族各不相同、因素之间有交互"，影响有限。附带的修法"先凝练、再 latent 化"本身就是 GSM8k-Aug 的做法，也接近 CoT 压缩蒸馏，作为方法分量很小。 |
| 新颖度 | 6 | 已核实 C-MTP 第 4.3 和 4.5 节把冗长数据的伤害归因于两点：间接监督有压缩压力、直接监督有 teacher forcing 下的误差累积（集中在数学表达式上）。附录 G.7 的 CommonsenseQA 给出"长 NL 轨迹但没有精确 token 就不崩"的反例。所以说崩塌原因"没有被解释"是夸大，准确的说法是"有假说，没有受控检验"。把题源和冗长度做成 2×3 交叉，是一个可辨认的增量，但属于补对照的常规分析设计。误差累积和近窗只作辅助测量，并不是四个可以独立操纵的因子。 |
| 有效性 | 5.5 | **现有依据**：C-MTP 表 2 和表 4（Llama，385k）中，CODI 相对 CoT-SFT 的保留率在算式版约为 86%（53.0/61.9），在 NL 版约为 89%（47.8/53.7）；CoLaR-2 从约 66% 降到约 44%。也就是说，在约 25 到 62 token 的范围内，冗长度只伤直接监督，不伤间接监督。CSQA 上 CODI 甚至超过 CoT-SFT。这两点都削弱了"冗长度主导"的跨家族主假说。用户 CoLaR 上 NL 18.4 对 EQ 28.6 只是单 checkpoint，属于直接监督家族，与上面的结论一致。删 80% 低熵步不掉点的证据来自显式 CoT，不能直接迁到 latent 训练。**迁移条件与未知**：一是 350–550 token 的 MATH 轨迹是否落在上面没测过的区间，比如间接监督在固定 6–20 个 latent 下压缩比过高；二是 LLM 凝练 MATH 符号推理能否真正内容等价，"保留全部中间数值"的校验对代数、几何类步骤太弱；三是 1.5B 模型在凝练后的 MATH 轨迹上做 CoT-SFT 很可能本身掉点（数学类任务对压缩更敏感），这会改变保留率的分母，使比值无法解释。 |

**与起点问题的关系**：这是邻近新问题。起点问题是"链尾集中、近窗依赖到底是接力式机制还是继承了版式"，这里只把近窗作为辅助证据，没有回答。转向本身不构成阻断。

**实验能否判别主张**：现在还不能，有四个阻断点。
1. **数据规模混杂未列入**。C-MTP 的 GSM8K 结论建立在 385k 条训练数据上，MATH 只有约 7.5k 题中答对的那部分（Llama 约 24% 答对），而且 README 写明 CoT-SFT 是在模型自己的输出上训练，所以分数不变（Qwen 原始 53.5，SFT 后 52.8）。也就是说，MATH 上的分母是一个没训过的底座能力，GSM8K 上的分母是训过的。网格把题数统一为 7.5k 后，如果 GSM8K 紧凑格本身就已经崩了，结论就是"数据规模或先验主导"。这个结果不在判别规则里，也就无法和 C-MTP 的原始对比对接。
2. **on-policy 与 off-policy 随冗长档一起变**。MATH 的真实档是模型自己生成的，其余各档以及 GSM8K 的扩写档都是外部 LLM 写的。冗长度和"轨迹是否出自本模型分布"同时变化，而后者正好决定 CoT-SFT 分母是否等于底座能力。
3. **"难度"轴其实是题源**。GSM8K 对 MATH 同时改变了领域、LaTeX 记号和难度。MATH 内部有 Level 1–5 可用来分离难度，但 brief 没有用。
4. **"四因素、按家族给主导因素"超出可测范围**。teacher-forced 对自由展开只对直接监督家族有定义，CODI 和 SIM-CoT 没有 gold latent 可喂。近窗也只是辅助测量。所以对间接和逐步重建两个家族，实际只能检验两个因素。

**可行性：pass**。C-MTP 仓库已核验包含 `data_math` 的生成脚本（vLLM 采样 5 次、只保留答对的轨迹，`math_grader.py` 用于评分）。现成的推理输出没有发布（README 写的是"XXX"），但可以按脚本复现。C-MTP、CODI 实现在同一仓库，SIM-CoT 有官方 ICLR 2026 仓库。原文全部实验都在单张 H200 上用 LoRA 完成。48 个 run，每个训练集 7.5k 题、最长 1024 token，在 8×A100 上 2–3 天可信。重写成本低于 300 元可信。已知风险：C-MTP 附录记录了 SIM-CoT 在 Qwen 上训练不稳定；Llama 在 MATH 上 CoT-SFT 只有 23.8%，latent 方法只有 7–10%，地板效应较重。

## 最高近邻
1. Training Continuous CoT Models: A Tale of Two Regimes（C-MTP），https://arxiv.org/abs/2607.16972 。原文给出了三种轨迹形态下的崩塌，并提出压缩压力和误差累积两种解释，还有 CSQA 反例。差别：没有在同一批题上控制冗长度和题源，也没有控制数据规模。
2. KaVa: Latent Reasoning via Compressed KV-Cache Distillation（ICLR 2026），https://arxiv.org/abs/2510.02312 。报告了从算式轨迹换成 NL 轨迹时的退化，并通过压缩教师 KV 缓解。差别：它是方法论文，没有做因素分解，也不涉及 MATH 真实轨迹。
3. How Do Latent Reasoning Methods Perform Under Weak and Strong Supervision?，https://arxiv.org/abs/2602.22441 。按监督强弱比较各 latent 方法，发现普遍存在捷径行为。差别：不涉及轨迹冗长度和题目难度。
4. Capabilities and Fundamental Limits of Latent Chain-of-Thought，https://arxiv.org/abs/2602.01148 。从理论上把 latent CoT 在计算类任务上的失败归因于低确定性导致的误差累积。它构成"精确计算或误差累积主导"这一竞争解释的理论近邻。
5. When Compression Helps and When It Hurts: Condition-Aware Analysis of CoT Distillation，https://arxiv.org/abs/2606.21704 。受控研究了显式 CoT 压缩，发现数学类任务对压缩更敏感。差别：它研究显式蒸馏而不是 latent 训练，但直接关系到"凝练后 CoT-SFT 分母是否持平"这一步。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是把 C-MTP 报告的 latent CoT 在 MATH 上的崩塌，分解为冗长度、题源（难度）、误差累积和近窗四个因素，并按方法家族给出主导因素。问题真实且有方向意义，但它补的是已知缺失的对照：C-MTP 已提出压缩压力与误差累积两种解释，并有 CSQA 反例。C-MTP 表 2 和表 4 显示，在约 25 到 62 token 的范围内，CODI 的保留率不随冗长度下降，已部分不支持跨家族的'冗长度主导'主假说。修法'先凝练、再 latent 化'接近已有做法。有效性依赖三个未验证环节：MATH 符号推理凝练后能否内容等价；凝练后 CoT-SFT 分母是否持平；350 token 以上的长度区间是否改变间接监督的行为。",
  "feasibility": "pass",
  "feasibility_reason": "C-MTP 仓库含 MATH 轨迹生成和评分脚本，可复现（现成输出未发布），也含 C-MTP 与 CODI 实现；SIM-CoT 有官方代码。1–1.5B LoRA、48 个 run 在 8×A100 上 2–3 天可行，重写 API 成本低于 300 元可信。风险是 SIM-CoT 在 Qwen 上不稳定、Llama 在 MATH 上有地板效应。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献分量不足：受控拆分冗长度与题源是 C-MTP 已提出解释、公开评论已指出缺失的对照，新颖度与重要性都没有达到 8，修法也接近已有的轨迹凝练做法",
    "Claim 阻断：C-MTP 的对比还混入了训练数据规模（385k 对约 7.5k 且只保留答对的轨迹），且 MATH 上的 CoT-SFT 分母等于未训练底座的能力。brief 没有把它列为竞争解释，判别规则也无法处理'7.5k GSM8K 紧凑格就已崩塌'这一结果",
    "Claim 阻断：冗长档与 on-policy/off-policy 一起变化（MATH 真实档由模型自己生成，其余档由外部 LLM 重写），凝练后 CoT-SFT 分母很可能不持平，使保留率无法解释",
    "Claim 阻断：'按家族给出四因素主导'超出可测范围。误差累积的 teacher-forced 测量只对直接监督有定义，近窗只是辅助测量；'难度'轴实为题源，混入了领域和记号差异",
    "表述夸大：'崩塌原因没有被解释'不成立，C-MTP 第 4.3 和 4.5 节以及附录 G.7 已给出解释和反例"
  ],
  "novelty_conclusion": "没有检索到已发表的受控研究在同一批题上拆分冗长度与题源，因此有可辨认的增量。但这个对照由最高近邻的讨论直接引出（C-MTP 原文已有压缩压力和误差累积假说及 CSQA 反例），设计属于常规的补对照分析，修法也接近已有的轨迹凝练与 CoT 压缩做法，新颖度约为 6。",
  "closest_neighbors": [
    "Training Continuous Chain of Thought Models: A Tale of Two Regimes (arXiv 2607.16972)",
    "KaVa: Latent Reasoning via Compressed KV-Cache Distillation (arXiv 2510.02312)",
    "How Do Latent Reasoning Methods Perform Under Weak and Strong Supervision? (arXiv 2602.22441)",
    "Capabilities and Fundamental Limits of Latent Chain-of-Thought (arXiv 2602.01148)",
    "When Compression Helps and When It Hurts: Condition-Aware Analysis of Chain-of-Thought Distillation (arXiv 2606.21704)"
  ]
}
```
