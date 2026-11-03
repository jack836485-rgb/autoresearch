## 结论
2026-11-03，总体 score 5.5，verdict：promising_needs_revision。主贡献是把 SIM-CoT 式辅助解码器的重建目标从"当前步文本"换成"累积紧凑状态"，用来修复 latent CoT 在长自然轨迹（C-MTP 的 MATH 设置）上的崩塌。问题本身重要，但现在不够：方法相对近邻只是可辨认的目标替换；"近窗装表层文本、早期结论逐跳丢失"这一因果链，在长轨迹上没有任何直接依据；最小实验也分不开"累积"和"紧凑／去叙述"这两种解释。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 7 | C-MTP（ICML 2026）已核实：直接监督和间接监督在约 350 token 的 MATH 真实轨迹上都只剩 CoT 的约 1/3。哪怕只能稳定收回其中一部分，也是对重要瓶颈的实质推进。但当前主张只是一个可插拔的辅助目标，最终分量取决于收益幅度，而这一点完全未知。 |
| 新颖度 | 6 | 重建目标的空间已经很拥挤：SIM-CoT 重建当前步；RGLT（2608.14107）重建累积前缀；2606.20075 预测未来步；Thinking States（2602.08332）把自然语言思考压成固定大小的状态并注入后续计算，且以变量追踪为例；文本域有 MCoT、AoT、Delethink、InftyThink 的"推导后约简"马尔可夫状态；LightThinker 在隐状态里做逐步 gist 压缩。"在 latent 辅助解码上用紧凑累积状态"这个具体组合我没检索到，但它是马尔可夫状态思想和 SIM-CoT 解码器的直接组合。与 RGLT 的差别（去掉叙述、长度不线性增长）是工程层面的，不是机制层面的。 |
| 有效性 | 5 | **现有依据**：(a) CoLaR 在 GSM8K 短轨迹上近窗注意力占比 72–80%，链尾置零后正确率崩溃。这是单个 checkpoint 的注意力描述加离流形干预，并且只在约 25 token 的短轨迹上，没有在长轨迹上观察到"早期结论丢失"。(b) Delethink 来自文本域，状态是显式文本，依赖 RL 和大模型，迁移到 latent 所需的条件（单个向量能装下累积状态、并真正被后续使用）正是 brief 自己列出的未知项。(c) Coconut logit lens 和 PMPS 显示 latent 能承载中间数值，这说明容量可行，不说明会被使用（2606.12689）。**反向依据**：2602.08783 报告 Coconut/CODI 的影响结构以跳连为主，与"窗口固定"的泛化相冲突。CODI 没有逐块文本目标，"窗口装表层文本块"的机制前提在 CODI 上不成立。C-MTP 本身把 SIM-CoT 也纳入 MATH 对比，逐步监督并没有防止崩塌；C-MTP 的另一个结论是"间接监督因不必表示每个 token 而更适合冗长轨迹"，这提示崩塌的主因可能是冗长文本挤占了逐 latent 的容量，而不是历史状态丢失。**未知**：MATH 崩塌中有多少比例来自早期中间量丢失（而不是单步计算错误、容量不足或暴露偏差）；s_k 在长轨迹后段的长度能否被单个 latent 重建。 |

- **与原问题的关系**：属于子问题兼邻近新问题，转向本身可以接受。原问题中"链尾集中是继承版式还是 latent 特有机制"在这里没有回答，现在把它当作前提来用。
- **实验能否判别主张**：不能完全判别。主结果只和 SIM-CoT（含叙述的当前步文本）以及累积文本前缀（含叙述）比较，缺少"紧凑当前步状态"（只含本步新确立的量、不含叙述）这一对照。所以即使本方法胜出，也无法把收益归因于"马尔可夫充分的累积状态"，而这个对照最能直接说明 C-MTP 提出的冗长性解释。诊断部分在推理时把注意力截到 W 个 latent，也是离分布干预；保留率高或低都不能唯一指向"窗口固定"。线性探针能读出早期中间量，也不等于被使用。在 GSM8k-Aug 上，s_k 与算式步文本几乎同构，"持平"不提供判别信息。
- **可行性：pass**。理由：底座为 1B，C-MTP 仓库含 `cmtp/train.py`、`codi/`、`data_math/`，SIM-CoT 有官方代码，RGLT 的累积前缀目标规范足以独立实现。API 按步抽取 7.5k 条 MATH 轨迹的状态，200 元量级可信。约 30 个 run 在 8×A100、5 天内可以排下，必要时裁种子。需要说明的缺口如下，它们不构成阻断：
  - MATH 中代数式、分情况讨论、集合类结论如何写成"中间量列表"，目前没有规范，抽取标签的含义需要先定。
  - CODI 的固定 latent 数与 MATH 中可变的步数之间，"每步末 latent"如何对齐，需要先给出规则。
  - brief 写的是"由底座模型生成"轨迹，而 C-MTP 的 MATH 轨迹来自强 teacher。两者不同，会改变"真实轨迹"这一条件。
  - C-MTP 在 MATH 上用的底座和绝对准确率需要核实。若 1B 的 CoT-SFT 本身就很低，latent 方法会落在地板效应区，3 个种子难以区分差异。

## 最高近邻
1. SIM-CoT（arXiv 2509.20317，https://arxiv.org/abs/2509.20317 ，github InternLM/SIM-CoT）：同样的辅助解码器，推理时去掉，可插到 Coconut/CODI 上。差别只在重建目标是当前步而不是累积状态。
2. RGLT, Retrieval Grounding Latent Reasoning for Dense Retrieval（arXiv 2608.14107，https://arxiv.org/abs/2608.14107 ）：第 k 阶段的 latent 重建累积前缀 r_≤k，与本方法的"累积"思想直接重叠。差别在于它用于检索任务、目标是含叙述的全文前缀。
3. Latent Reasoning with Supervised Thinking States（arXiv 2602.08332，https://arxiv.org/abs/2602.08332 ）：固定大小的循环状态由自然语言思考压缩而来，以变量追踪为监督示例，在 GSM8K 和状态追踪任务上有效。差别在于它在输入处理过程中注入状态，而不是在 latent CoT 链上用累积状态做辅助目标。
4. Training Continuous CoT Models: A Tale of Two Regimes / C-MTP（arXiv 2607.16972，https://arxiv.org/abs/2607.16972 ）：定义了目标问题和全部基线，其中包括 SIM-CoT 在 MATH 上同样崩塌，以及间接监督更适合冗长轨迹的观察。它没有提出针对长轨迹的修法。
5. Markov Chain of Thought（arXiv 2410.17635）以及 Delethink（arXiv 2510.06557）：文本域"推导后约简"的马尔可夫状态，证明显式状态足以支撑长推理。差别在于本方法把状态放进 latent 的辅助目标，迁移条件未经验证。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 7.0, "novelty": 6.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是把 SIM-CoT 式辅助解码目标由当前步文本换成紧凑累积状态，以修复 latent CoT 在长 MATH 轨迹上的崩塌。重要性 7：C-MTP 已核实约 65% 的崩塌，问题确实重要，但收益幅度未知。新颖度 6：与 RGLT 累积前缀、Thinking States 的固定状态、MCoT/Delethink 的文本马尔可夫状态高度邻近，属于目标替换式组合。有效性 5：近窗证据只来自 CoLaR 短 GSM8K 轨迹，是注意力描述加离流形置零；长轨迹上没有'早期结论丢失'的直接证据；2602.08783 的非局部影响与之相冲突；CODI 不满足'窗口装表层文本'的前提；C-MTP 中 SIM-CoT 也在 MATH 上崩塌，C-MTP 自己的冗长性解释是有力的竞争解释；Delethink 迁移到 latent 的条件未验证。",
  "feasibility": "pass",
  "feasibility_reason": "1B 底座；C-MTP、CODI 代码以及 MATH 轨迹脚本已核验可得，SIM-CoT 有官方实现，RGLT 规范足以独立实现；API 抽取约 200 元；约 30 个 run 能在 8×A100、5 天内排下。需要先补：MATH 状态抽取规范、CODI 固定 latent 与可变步数的对齐规则、改用与 C-MTP 一致的 teacher 轨迹，并核实 1B 在 MATH 上的 CoT-SFT 绝对水平以避免地板效应。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：7/6/5，没有两项达到 8；方法是 SIM-CoT 重建目标的替换，与 RGLT 累积前缀、Thinking States、文本域马尔可夫状态（MCoT/Delethink）高度邻近",
    "有效性缺依据：长轨迹上'早期中间结论经近窗逐跳丢失'是 MATH 崩塌主因这一点没有任何直接证据；现有近窗证据只来自 CoLaR 的短 GSM8K 轨迹；2602.08783 的非局部影响以及 CODI 没有逐块文本目标都与该假说冲突；C-MTP 中逐步监督的 SIM-CoT 同样崩塌",
    "Claim 阻断：最小实验缺少'紧凑当前步状态（去叙述、不累积）'对照，无法把收益归因于累积/马尔可夫充分，而不是目标去冗长化；后者正是 C-MTP 自己提出的竞争解释；推理期截断注意力与探针可读都不能判别'窗口固定'是否为因果机制"
  ],
  "novelty_conclusion": "未检索到在 latent CoT 辅助解码中使用紧凑累积状态目标的工作，但累积前缀重建（RGLT）、固定大小的思考状态（Thinking States）、隐状态 gist 压缩（LightThinker）和文本域马尔可夫状态（MCoT/AoT/Delethink）已覆盖其核心思想；新意属于可辨认的增量组合，约 6 分。",
  "closest_neighbors": [
    "SIM-CoT: Supervised Implicit Chain-of-Thought (arXiv 2509.20317)",
    "Retrieval Grounding Latent Reasoning for Dense Retrieval / RGLT (arXiv 2608.14107)",
    "Latent Reasoning with Supervised Thinking States (arXiv 2602.08332)",
    "Training Continuous Chain of Thought Models: A Tale of Two Regimes / C-MTP (arXiv 2607.16972)",
    "Markov Chain of Thought for Efficient Mathematical Reasoning (arXiv 2410.17635); The Markovian Thinker / Delethink (arXiv 2510.06557)"
  ]
}
```
