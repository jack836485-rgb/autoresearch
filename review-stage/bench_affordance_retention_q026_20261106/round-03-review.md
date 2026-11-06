## 结论
日期 2026-11-06。总体 score 5.5，verdict：promising_needs_revision。主贡献是一个现象：在固定目标、运行中没有用户输入的环境里做 agentic RL，会选择性地拉大"晚到差距"，也就是轨迹中途到达的用户指令比首轮指令更容易被忽略。这个问题有价值，查新也没找到对同一基座做 RL 前后、按指令到达时间拆分的直接工作。但目前贡献还不够，原因有三点。第一，"选择性折扣而非整体下降"这一核心机制缺少有针对性的依据，引用的证据（Laguna、MathIF）支持的反而是竞争解释，即整体遵循下降。第二，主实验只比较两个混杂很多的公开检查点，作为对照的 SA-SWE，其"注入中途提示"与 DeepSWE 的区别设定不准。第三，能支撑因果主张的实验是可选项。所以有效性没到 6，重要性和新颖度也都没有一项到 8。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 这对"开源 SWE-RL 模型能否当交互助手用"和"RL 环境要不要加中途用户回合"有明确价值，但影响有限，原因有三。一是近邻已经普遍证明交互和多轮场景下智能体会遗忘指令：MTAC-IFBench 显示所有模型的过程约束遵守随轮次快速下降；Dialogue-SWEBench 中 Devstral 在 23–34% 的对话里从不回应用户。二是 Laguna 已指出 RL 会遗忘行为约束，并给出了 IF 数据增强的修法。三是研究对象只有 2025 年的两个 32B 检查点。新增的部分是"RL 前后对比"和"按到达时间拆分"，属于对已知问题的归因细化，算不上新瓶颈。 |
| 新颖度 | 6.5 | 没有检索到同一基座 RL 前后、比较首轮与中途同一条指令遵守率的工作，这一点可以辨认。但测量方法与近邻高度重合：Harness-IF 已经用反默认子集（Against-Prior Accuracy）在多个表面（包括 user turn）测规则遵守；MTAC-IFBench 已测按轮次的衰减；InterventionBench 已测中途用户干预。新意主要来自"训练来源归因"加"时间选择性"这一框架，机制本身没有新内容。 |
| 有效性（先验合理性） | 5.0 | 当前依据有四条。(1) R2E-Gym 在非函数调用分支（agent.py L497）把观察以 user 角色追加，奖励只看首轮目标。这一点属实，但这样训练出来的策略必须读取并利用观察内容（测试输出、报错），RL 学到的是"按内容使用 user 消息"，不能直接推出"折扣 user 消息里的指令"。(2) Laguna §4.3.2 讲的是没有 IF 监督时，RL 会灾难性遗忘系统提示里的约束。MathIF 讲的是整体下降。两者预测的都是首轮遵守也会下降，正是简报要排除的竞争解释，支持不了"选择性"。(3) 2603.12277 说明模型按"听起来像谁"来判断来源。这支持中途指令附在观察里和单独作为 user 消息时效果可能相同，但推不出 RL 会专门学会折扣晚到指令。(4) SA-SWE 作为对照的设定有偏差。SkyRL 注入的是步数/上下文预算提醒、工具失败纠正这类环境侧提示，跟随它们本身就与奖励相关；R2E-Gym 自带的 agent 循环也会在每步观察后追加 "Steps Remaining"（agent.py L394–401），DeepSWE 训练时是否同样带有这类提示需要核对 rllm 的训练循环。两者都没有"遵守用户约束且计入奖励"的训练信号，因此"SA-SWE 介于二者之间"的预测缺少机制依据。另有一个更朴素、同样可预测的竞争解释：RL 带来的默认行为锐化或熵塌缩会降低所有反默认指令的遵守。它在长轨迹中途可能被放大，从而让晚到差距变大但不具有"晚到"特异性。目前没有发现直接与假设矛盾的已有结果，所以不判阻断。 |
| 待预研 | — | DeepSWE 相对基座的晚到差距是否不为 0、有多大；首轮遵守率和一般多轮 IF 是否同步下降；独立 user 消息与附在观察里两种通道的差别。这些不计分。 |

与起点问题的关系：这是一个邻近新问题。它保留了"固定目标、运行中没有用户输入"这一结构性质，对象从方法增益保留率换成了 RL 后模型的行为。起点的跨方法族保留率预测、只判终态、搜索集可穷举等问题都没有回答。转向本身不扣分。

实验能否判别主张：只能部分判别。(a) 主 Claim 是因果性的（"在固定目标环境做 agentic RL 会专门拉大晚到差距"），主实验却是两个 RL 检查点的自然比较，两者在算法、步数、thinking 模板（SkyRL 保留历史 thinking）和 harness 上都不同；能把差异归因到"环境缺中途用户回合"的 4B 受控 RL 只是"视主实验结果决定"。如果不做，主 Claim 就只能收窄为"DeepSWE 表现出该现象"，分量会进一步下降。(b) 反默认子集按模型分别确定，三个模型的题集不同，跨模型比较晚到差距时要说明是在题目交集上配对，还是在各自子集上比较。(c) "一般多轮指令遵循"对照没有指定基准。(d) 不能用首轮遵守率不变来区分"选择性折扣"和"锐化导致的长上下文反默认失效"。需要的对照是：同样的反默认指令放在首轮，但在第 k 步附近重复，或者用长度相近的填充上下文代替真实轨迹。

可行性：pass。三个模型的权重都公开（DeepSWE-Preview、SA-SWE-32B、Qwen3-32B）。R2E-Gym 代码公开，在第 k 步插入消息或改写观察只需改几行。所有判定都是确定性的（命令日志和 diff）。主实验 2,400 次运行，按 16 路并发、每次 30 分钟估算约 3.1 天，加上 SA-SWE 原生 harness 复测和 SWE-Together 外部复测，在 8×A100、不超过 5 天的约束内略显紧张，但可以完成。no-go 预研（DeepSWE 与基座，50 题 × 2 条件）在 2×A100 上约 1 天，合理。指令与检查器需要新建，1–2 人日可信。基座 Qwen3-32B 在第 8 步前提交、格式失败的比例可能偏高，会缩小样本量，这一点需要在预研中核实。

## 最高近邻
1. Harness-IF: Instruction Following in Coding Agents（arXiv 2608.11727, https://www.emergentmind.com/papers/2608.11727 ）。重叠：用反默认子集测编码智能体在多个表面（系统提示、项目文件、user turn）的规则遵守。差别：明确说明不做训练来源归因，没有比较 RL 前后，也没有按到达时间拆分。
2. MTAC-IFBench（arXiv 2609.14992, https://arxiv.org/abs/2609.14992 ）。重叠：在多轮智能体编码中测过程约束，发现遵守率随轮次快速下降，后几轮几乎完全失败。差别：只评测前沿模型，没有同基座 RL 前后对比，也没有区分"晚到"与"上下文变长"。
3. Dialogue-SWEBench（arXiv 2606.13995, https://arxiv.org/abs/2606.13995 ）。重叠：对话式编码智能体，报告 Devstral 2 Small 在 23–34% 的对话中从不回应用户。差别：没有检验训练来源，也没有测中途指令的遵守。
4. Laguna 技术报告（arXiv 2605.27605, https://arxiv.org/abs/2605.27605 ）§4.3.2。重叠：没有 IF 监督时，agentic RL 会灾难性遗忘系统提示约束，并给出了数据增强修法。差别：针对的是全局约束遗忘，不按到达时间区分，没有测中途用户指令。
5. InterventionBench（EMNLP 2026 Findings, https://aclanthology.org/2026.findings-emnlp.698/ ）。重叠：在 AppWorld/WebArena 上插入中途用户目标修订，12 个智能体在所有干预类型上都掉分。差别：不是编码任务，没有 RL 前后比较（摘要层面未见）。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 6.5, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是 agentic RL（固定目标、无中途用户输入的环境）选择性拉大首轮与中途指令遵守之间的晚到差距。重要性 6：交互可用性和 RL 环境设计有价值，但近邻已普遍显示多轮和交互中的指令遗忘（MTAC-IFBench、Dialogue-SWEBench），Laguna 也已报告 RL 遗忘约束并给出修法，本工作是归因细化，对象只有两个旧检查点。新颖度 6.5：没有检索到同基座 RL 前后、按到达时间拆分的工作，但测量设计与 Harness-IF（反默认子集、多表面）、MTAC-IFBench（按轮衰减）高度重合。有效性 5：R2E-Gym 以 user 角色追加观察属实，但策略必须利用观察内容，推不出会折扣晚到指令；Laguna 和 MathIF 支持的是整体下降这一竞争解释；SA-SWE 的提示是环境侧、与奖励相关的提示，R2E-Gym 自身也在每步观察中追加 Steps Remaining，所以'SA-SWE 居中'缺少机制依据；默认行为锐化导致长上下文中反默认失效这一竞争解释没有被设计排除。晚到差距的大小待预研。",
  "feasibility": "pass",
  "feasibility_reason": "三个模型权重、R2E-Gym 与 SkyRL 代码都公开，插入指令只需修改 history 或观察字符串，判定是确定性的；主实验约 2,400 次 32B 推理，在 8×A100 上约 3 天，加上复测仍在 5 天内；no-go 预研在 2×A100 上约 1 天。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：有效性 5.0 < 6，且没有任何一项 ≥ 8。",
    "核心机制'选择性晚到折扣'缺少依据：引用的 Laguna 和 MathIF 支持的是整体遵循下降，R2E-Gym 训练要求策略利用 user 角色的观察内容，推不出会折扣晚到指令。",
    "Claim 阻断：主 Claim 是因果性的，但主实验只比较两个在算法、步数、thinking 模板、harness 上都有混杂的检查点；能归因的受控 RL 是可选项。SA-SWE 的'中途提示'是与奖励相关的环境侧提示，不是用户约束，不能作为'加入中途用户回合'的对照。",
    "没有设计对照来区分'晚到选择性折扣'与'RL 锐化导致长上下文反默认指令失效'（例如首轮指令在第 k 步重复，或用等长上下文填充）。"
  ],
  "novelty_conclusion": "没有检索到对同一基座做 agentic RL 前后、按指令到达时间比较遵守率的工作，'RL 来源加时间选择性'的框架有可辨认的增量；但测量方法（反默认子集、多轮过程约束、中途干预）已被 Harness-IF、MTAC-IFBench、InterventionBench 覆盖，RL 侵蚀指令遵循已有 Laguna 和 MathIF，所以新颖度属于中等增量。",
  "closest_neighbors": [
    "Harness-IF: Instruction Following in Coding Agents (arXiv 2608.11727)",
    "MTAC-IFBench: Benchmarking Instruction-Following in Multi-Turn Agentic Coding (arXiv 2609.14992)",
    "Dialogue-SWEBench: A Benchmark for Dialogue-Driven Coding Agents (arXiv 2606.13995)",
    "Laguna technical report §4.3.2 (arXiv 2605.27605)",
    "InterventionBench: Can LLM Agents Adapt to Mid-task User Interventions? (EMNLP 2026 Findings)"
  ]
}
```
