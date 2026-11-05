## 结论
2026-11-04，总体 score 4.5，verdict：needs_rethink。如果关键结果成立，主贡献会是一种"使用时刻事后重标注、施加到整条携带链"的 writer 偏好信号，让循环重写式 writer 在长延迟下学会保留决定性事实。但这个贡献不够：实验 A 基本就是 DSSR 自己在 §5.6/§7 点名的修补方向，在 DSSR 原协议里补上；实验 B 的"摘要 token 附加优势、并沿记忆序列向前传递"已被 HiMPO 在 BrowseComp-Plus 上做过，而且 brief 漏列了它。另外，brief 对 DSSR 关键数字的转述有误，判别实验所依赖的前提也不成立。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 长延迟跨重写的信用分配是真实瓶颈。DSSR 的 §5.6 给出了直接测量：51–67% 的写入点候选里已不含决定性事实，S12 选更完整候选的比例只到随机水平。可是实验 A 的环境是 DSSR 自称"受控诊断"的 TextWorld，DSSR §6 也说明在 F′ 协议下 writer 已知 recipe 重要，测的是"保留已知相关事实"，不是"前瞻地选什么重要"。所以 A 的结论本质上是"能否从事后标签学会一直保留 recipe"，影响面有限。外推价值要靠 B 承担，而 B 与已有工作重叠。 |
| 新颖度 | 5 | 去掉 DSSR 的名字后，A 剩下的是 HER 式事后重标注（DSSR 已引用 HER），加上 restore 反事实定位（2609.08279，以及 DSSR 自己的 chunk-removal relevance lag），再加上 A4 的可达性过滤，属于常规组合。DSSR §7 原文写的方向是"credit keeping a fact at t with its value beyond the current writer's forgetting horizon… e.g. enforcing retention in the roll-forward"，本方法是这一方向的一个直接实例，相当于把起点论文补完。B 中"摘要 token 附加优势 + 信用沿记忆序列回传 + 事后信号"已由 HiMPO（2606.16285，含 BCP 实验与 backward smoothing）覆盖。"用重读作触发"本身是 TRACER（以重调用为代价项）和 2608.16370（再获取成本）的近邻变体。 |
| 有效性 | 5 | 现有依据：DSSR 已证明 S12 无法区分保留与丢弃，A4 能在可达点恢复偏好信号。直接用"保留 f > 丢弃 f"作标签，很可能提高携带链上的保留率，这一步机制上可信。仍有三处跳跃。(1) 胜率上限：DSSR 中即使 F′=0，训练 writer 的测试胜率也只有 10.4%（ORACLE-B 98.9%），说明非保留因素也压低了胜率；即使 recipe 被完整携带，长延迟胜率最多回到约 F′=0 的水平，在 90 局上能否显著仍未知。(2) brief 称"手写规则在每个延迟下都更好"，与原文不符：验证集 GUIDE 为 11.1/11.1/2.2/6.7，A4 为 26.7/11.1/4.4/2.2；测试集 F′=20 时 GUIDE 0%、DSSR 2.2%。GUIDE 只在 regret Δ 上和 B=256 时占优。因此"以手写规则在相同 writer/预算下有效为前提"的判别前提，在 B=128 的胜率上不成立。(3) B 的触发证据 2610.35496 来自 SWE-bench，并非深度搜索；2608.16370 显示再获取现象依赖环境（ALFWorld 上没有出现），BCP 上的触发频率与判定准确度都没有依据。 |

- **与起点问题的关系：** 这是子问题，研究"结果式信号下 summary 内容得不到信用"中的跨重写保留部分。起点里的收益来源拆分（summary vs 执行器）、RL 回避压缩的原因、summarizer/actor 跨族迁移仍未回答；B 中的 2×2 交换只是附带度量。
- **实验能否判别：** A 能检验"保留率是否上升"，但胜率主判据受下限压制，判别前提也有误。另外，抽取 f 用了 TextWorld 模板，B=128 下又只有 recipe 一类决定性事实，所以"不需任务知识、从经验学会该保留什么"这一点无法与"按模板保留 recipe"区分开；需要一个直接按模板 recipe 覆盖构造偏好对的对照，否则 binary-search 定位这一步没有被检验。B 缺少两个同任务强对照：HiMPO（以及 MemPO/SUPO 在 BCP 上的结果），和"GRPO + 简单重读惩罚"。缺了它们，Claim 2 的"重读次数/token 降低"无法与单纯惩罚重读区分。用文档 ID 提及来判定"仍含信息"也容易被钻空子（只保留 ID、不保留内容）。这些都是 claim 阻断。
- **可行性：pass。** A 的依据：DSSR 匿名仓库已核验存在 env/、dssr/、configs/、checkpoints/、prompts/、results/；模型为 Qwen3-4B LoRA，可单 GPU 逐位复现；restore 反事实只增加 reader 前向，每方法 1–2 天、3 种子在 2×A100 内可行。B 的依据：Qwen3-8B 在 BCP 上做 GRPO（语料约 10 万文档、830 题公开），8×A100 每次 1–1.5 天属外推，但在 5 天约束内；Self-Credit 与 HiMPO 都有足够规范可独立复现。可行性不是瓶颈，瓶颈在贡献分量和判别设计。

## 最高近邻
1. DSSR, Decision-Sufficient State Representations (https://arxiv.org/abs/2609.32805)：同协议、同 writer/reader，在 §5.6/§7 明确诊断跨重写信用问题，并给出"让续写保留候选所保留内容"的修补方向。差别仅在本方案用事后事实标签代替前滚打分。
2. HiMPO (https://arxiv.org/abs/2606.16285)：对记忆 token 加辅助优势（事后 oracle 目标的似然比 + 局部反事实），用 backward smoothing 沿记忆序列回传给先前写入，并在 BCP 上评测。差别：触发信号是重读而非目标似然，没有显式的"事实携带链"。
3. TRACER (https://arxiv.org/abs/2608.29363)：把压缩后的工具重调用计入奖励，用逐工具反事实归因。差别：作用对象是保留比例而非自由文本摘要，且不联合训练执行器。
4. What Eviction Destroys (https://arxiv.org/abs/2609.08279)：restore 反事实区分不可逆驱逐与检索失败。差别：只用于评测，不用于训练。
5. Self-Credit (https://arxiv.org/abs/2610.28388)：在 BCP 上用摘要内对历史轮次的引用给动作轮次记功。差别：记功对象是被引用的动作轮次，不是摘要写入的保留。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 6.0, "novelty": 5.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是使用时刻事后重标注、施加到整条携带链的 writer 偏好信号。A 在 DSSR 原协议内实现了 DSSR §7 自己点名的修补方向（相当于补完起点论文）；B 的摘要 token 附加优势加回传已被 HiMPO 在 BCP 上覆盖。保留率上升在机制上可信，但长延迟胜率受 F′=0 时约 10% 的上限压制；brief 误述 GUIDE 在每个延迟都更好，判别前提不成立；B 的重读触发证据来自 SWE 域且依赖环境。",
  "feasibility": "pass",
  "feasibility_reason": "DSSR 匿名代码已核验存在 env/dssr/configs/checkpoints/prompts/results，4B LoRA 可单卡复现，restore 反事实只需 reader 前向；BCP 语料与题目公开，8B GRPO 在 8×A100 的 5 天约束内可行。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "新颖度：实验 A 是 DSSR §5.6/§7 明确提出的修补方向在同一协议内的直接实例，去掉 DSSR 名字后只剩 HER 式重标注、restore 反事实与 A4 过滤的常规组合",
    "新颖度/claim：实验 B 的摘要 token 附加优势加沿记忆序列回传已由 HiMPO（2606.16285，含 BCP）覆盖；brief 未列出它，也未把它作为同任务对照",
    "claim：brief 称手写规则在每个延迟下都更好，与 DSSR 表 1/表 2 不符（验证集 A4 在 F′=0、20 高于 GUIDE；测试集 F′=20 时 GUIDE 为 0%）；以 GUIDE 有效为前提的判别逻辑在 B=128 胜率上不成立",
    "claim：A 缺少直接用模板 recipe 覆盖构造偏好对的对照，无法证明 binary-search 定位与'不需任务知识'有贡献；B 缺少 GRPO+重读惩罚对照，且文档 ID 判定可被钻空子"
  ],
  "novelty_conclusion": "相对 DSSR 是其自述未来方向的直接实现，相对 HiMPO 在 BCP 上的记忆信用回传只有触发信号不同；新意为增量级。",
  "closest_neighbors": [
    "Decision-Sufficient State Representations: Measuring and Reducing Write-Time Regret (2609.32805)",
    "HiMPO: Hindsight-Informed Memory Policy Optimization for Less-Entangled Credit in Long-Horizon Agents (2606.16285)",
    "TRACER: Per-Tool Context Retention for LLM Agents via Consequence-Attributed Reinforcement Learning (2608.29363)",
    "What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory (2609.08279)",
    "Self-Credit: Credit Assignment for Long-Horizon Agentic RL via Intra-group Rescaling (2610.28388)"
  ]
}
```
