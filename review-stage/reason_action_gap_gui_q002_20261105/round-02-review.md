## 结论
2026-11-05，总体 score 6.0，verdict：promising_needs_revision。主贡献是一个现象／视角贡献：把截图核验的"屏幕未变后重复"分成 R 复读、F 知而不改、E 假换法三类，并检验"修法×类型"交互。若成立，它能解释统一修法为什么效果小、方向也不一致，这个价值是真实的。但目前分量不够。三类各自的机制都已有人单独报告过（自我模仿、执行落差、失败调用的表面形式），两种修法 A 和 C 直接沿用 2608.23651。B 在 R/E 上"无效"这条预测在相当程度上由类别定义本身决定。可推翻判断 (3) 和"按类型选修法"的实用主张，在现有设计下都无法检验。三项分数都没有达到 8，不满足通过门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 开源截图 CUA 在失败后重复是真实瓶颈，统一修法降了重复却不提成功，这一点有据（2608.23651 在文本上也看到解码屏蔽降重复不提成功；Inertia 报告 R³ 任务分变化不显著）。三类分解若成立，会改变"该修哪一层"的判断。但范围限于开源中小 CUA 的失败步。强系统已用分级 Loop Breaker 把浪费步数减半（VLAA-GUI），按类型选修法能否在任务层面多出收益，本设计不检验。 |
| 新颖度 | 6.5 | 有可辨认的增量：在 GUI 失败后状态上用截图核验加推理新鲜度做三分，并用同一状态上的反事实修法测交互。但 R 类就是 CPL 的"把自己先前响应当示范"，F 类就是 Say One Thing 的 execution gap（以及 CUADebug 的 R5 action-intent misalignment）挪到失败后场景，A/C 两种修法都取自 2608.23651，B 本质是"去历史、以推理为条件重新解码"。交互预测里，B 在 R 和 E 上无效几乎由定义推出：推理本身就指向原动作，按推理落地自然复现原动作。真正非平凡的只有 F+B 能改对动作、C 能让 R 类推理变新鲜，以及在线屏幕变化与成功率。 |
| 有效性 | 5.5 | 现有依据：离线预检显示截图未变的重复步中，推理相似度 >0.9 的比例明显高于非重复步（44/24/13% 对 10.1/4.7/0.3%），说明 R 类真实存在且比例随模型变化，可靠性尚可（字符串相似度相对机械）。F/E 的比例是正则粗标，E 类只有 EvoCUA 的 21 例，证据弱。F+B 有效的依据来自 Say One Thing（单步、无失败历史），要迁移到失败后状态还缺一环：推理所指目标在"刚失败过"的界面上是否正确，没有任何直接证据。C 对 R 有效来自 2608.23651 的文本小模型（runtime 描述消除 76% 的倒置），迁移到多图 VLM 的条件（重复截图与动作串哪个才是主因）未知。E 类的预测基本没有依据。训练侧反证（AgentNet 中错误后重复只占 0.4%）有信息量，但只否定一个解释。 |

与起点的关系：这里回答的是原问题中"推理与动作在何处断开"这一部分，属于子问题。训练侧来源只给了一条反证，ConflictGUI 冲突终止被明确排除，原问题的这两部分仍未回答；这不构成阻断。

实验能否判别主张：只能部分判别。
- 能判别的：F+B 对比 A 的离线动作改变与目标一致性；C 在 R 类上让推理变新鲜的比例。
- 不能判别的，第一点是 B 的作用来源。B 同时做了"用新鲜推理落地"和"去掉历史动作串与重复截图、缩短上下文"两件事，而 CPL 已报告缩短上下文本身就降惯性。缺少"同样去历史但不给推理"的对照，就无法把 F 类收益归因于推理–动作耦合。
- 第二点是可推翻判断 (3)。它需要统一修法（R³、steering、failure notice）在同一模型、同一状态上按类型拆开的效应。Inertia 公开的是其他运行上的汇总效应，steering 不复跑，R³ 只做在线对照，所以"加权重现平均效应"在设计上无法检验。
- 第三点是"按类型选修法"的实用价值。没有"按类型路由 vs 最强统一策略"的同预算比较，强统一基线（R³、VLAA-GUI 式强制换策略、CPL 的上下文管理）都没有进入对比。
- 第四点是在线统计功效。重放状态来自 89–95% 失败的轨迹，每格 50 个状态、继续运行成功率很低，任务成功差异基本没有检验力。屏幕变化率尚可。

可行性：pass，但附带阻断。
- 离线核心在 EvoCUA-8B（权重公开）和 OpenCUA-7B 上可行：HF 轨迹包已确认存在（`evocua_8b_20260105.zip`、`opencua_agent-opencua_7b-...-action_history-3image-Ubuntu-50steps.zip`、`UI-TARS-0717-100step.zip`），按 mm_agents 重建上下文并用贪心复现率核验是合理做法。judge 约 1 万次、数百元，在 1000 元以内；单卡 A100 一到两天也在预算内。
- 问题一："UI-TARS-0717" 这次运行对应的很可能是 ByteDance Seed 的 UI-TARS-250705 / UI-TARS-2 系列（OSWorld-Verified 榜单 41.8%，基于约 230B 总参的 MoE），我没有查到公开权重。若属实，该模型上无法做需要 logits 的 A，也无法离线重新解码 B/C，"三个公开权重 CUA"这一前提就不成立。可以换成同一数据集里的 GUI-Owl-7B、OpenCUA-32B/A3B 轨迹，但三类比例需要重新估计。
- 问题二：OpenCUA-7B 的 R 类只占 13%，总状态数也只有数百，"每类至少 100 步"的门槛很可能达不到。
- 问题三：在线重放依赖 KVM（尚未确认），按记录动作重放 20 步在 OSWorld 中不保证回到同一状态（时序、弹窗、文件状态都会变），设计里没有写状态等价检查。改到浏览器环境会改变研究对象。
- 标签：R 类由字符串相似度给出，含义清楚。F 与 E 的边界（"所述方法是否等同原动作"）依赖 judge 主观判断，150 步人工复核必不可少，但每类每模型的复核量偏小。

## 最高近邻
1. Absorbed in Inertia: Activation Analysis for Computer-Use Agents（https://arxiv.org/abs/2609.37176 ）：同一对象，研究开源 CUA 的屏幕–动作惯性和失败承认，并测统一修法（steering、R³）。仍有的差别：它把惯性当作一种现象处理，没有按推理新鲜度或修法响应分型。正文因限流未能读取，摘要以外的细节需要检索核实。
2. Mitigating Conversational Inertia in Multi-Turn Agents（https://arxiv.org/abs/2602.03664 ）：文本 agent 把自己先前的响应当作 few-shot 来模仿，同一状态下长上下文的惯性更强，修法是 CPL 训练加上下文管理。与 R 类机制和 B/C 中"去历史"的成分重叠。仍有的差别：它不区分新鲜推理与复读，也不涉及 GUI 截图核验。
3. Feedback That Backfires（https://arxiv.org/abs/2608.23651 ）：失败调用的表面形式贡献了 83% 的重发，runtime 描述可消除 76%，解码屏蔽针对的是同一项。修法 A 和 C 直接来自这里。仍有的差别：只研究文本小模型，不分型，没有视觉状态。
4. Say One Thing, Do Another?（https://arxiv.org/abs/2510.02204 ）：移动端 VLM agent 中，推理正确而执行错误（EG）比反过来更常见。对应 F 类。仍有的差别：单步、没有失败历史，也不测修法。
5. CUADebug（https://arxiv.org/abs/2608.02643 ）与 VLAA-GUI（https://arxiv.org/abs/2604.21375 ）：前者在 OSWorld 失败轨迹上建立 30 个子类的分类，含 R5 action-intent misalignment 和 R4 冗余策略，并做诊断引导的重执行；后者的 Loop Breaker 按"重复失败"和"屏幕状态反复出现"两种触发方式施加不同干预，并报告浪费步数减半。仍有的差别：二者都没有按推理新鲜度分型，也没有检验"修法×类型"交互；但 VLAA-GUI 是"分级修法"在任务层面的强基线。

```json
{
  "score": 6.0,
  "contribution_scores": {"importance": 6.5, "novelty": 6.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献：把 GUI CUA 截图未变后的重复拆为 R 复读、F 知而不改、E 假换法三类，并检验修法×类型交互，用以解释统一修法为何效果小。重要性 6.5：瓶颈真实，但实用收益（按类型路由优于最强统一策略）未被检验。新颖度 6.5：三类机制分别对应 CPL 的自我模仿、Say One Thing 的 execution gap 与 CUADebug 的 R5，修法 A/C 取自 2608.23651；B 在 R/E 上无效在相当程度上由类别定义决定，非平凡部分只有 F+B、C 对 R 和在线结果。有效性 5.5：预检较可靠地支持 R 类存在且比例随模型变化；F/E 比例为正则粗标；F+B 的依据来自单步无失败历史的场景，推理目标在失败后界面上是否正确没有直接证据；E 类预测缺依据；可推翻判断 (3) 缺少同模型同状态下按类型拆开的统一修法效应，无法检验。",
  "feasibility": "pass",
  "feasibility_reason": "离线核心在 EvoCUA-8B（公开权重）与 OpenCUA-7B 上可实施：HF 轨迹包已确认存在，按 mm_agents 重建上下文并以贪心复现率核验，judge 费用与单卡 A100 一到两天都在预算内。但 UI-TARS-0717 运行很可能对应 UI-TARS-250705/UI-TARS-2（未查到公开权重），无法在该模型上离线施加 A/B/C，需要换成 GUI-Owl-7B 或 OpenCUA-32B；OpenCUA-7B 的 R 类样本可能不足 100；在线重放需要 KVM（未确认），且按记录动作重放不保证回到同一状态。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：三项都低于 8；三类机制和修法 A/C 均已有近邻单独报告，B 在 R/E 上无效的预测在相当程度上由类别定义推出，剩下的非平凡交互分量不足以支撑两项 8 分",
    "Claim 阻断：可推翻判断 (3)（类型加权重现统一修法的平均效应）需要 R³/steering/failure notice 在同模型同状态上按类型拆开的效应，现有设计只有 Inertia 在其他运行上的汇总数，steering 不复跑，无法检验",
    "Claim 阻断：B 同时去掉历史并以新鲜推理为条件，缺少'同样去历史但不给推理'的对照，无法区分推理–动作耦合与 CPL 已知的上下文缩短效应",
    "Claim 阻断：'哪类状态该用哪种修法'没有'按类型路由 vs 最强统一策略（R³、VLAA-GUI 式强制换策略、CPL 上下文管理）'的同预算比较，实用价值未被检验",
    "可行性/Claim 阻断：UI-TARS-0717 运行很可能不是公开权重模型，'三个公开权重 CUA 上的离线修法'在现有模型选择下不成立；在线部分 KVM 未确认、重放状态等价性未检查，且失败轨迹继续运行的成功率基数低，每格 50 个状态对任务成功几乎没有检验力"
  ],
  "novelty_conclusion": "在 GUI 失败后状态上按推理新鲜度三分、并做同状态反事实修法交互的组合未见先例，但各组成部分（自我模仿、execution gap、表面形式驱动重发及其两种修法、分级 loop breaker）都已有近邻覆盖，属可辨认的增量，不是独立的新机制。",
  "closest_neighbors": [
    "Absorbed in Inertia: Activation Analysis for Computer-Use Agents (arXiv:2609.37176)",
    "Mitigating Conversational Inertia in Multi-Turn Agents (arXiv:2602.03664)",
    "Feedback That Backfires: Why Small Language Model Agents Repeat the Call They Just Watched Fail (arXiv:2608.23651)",
    "Say One Thing, Do Another? Diagnosing Reasoning-Execution Gaps in VLM-Powered Mobile-Use Agents (arXiv:2510.02204)",
    "CUADebug: Diagnosing and Repairing Computer-Use Agent Failures (arXiv:2608.02643); VLAA-GUI (arXiv:2604.21375)"
  ]
}
```
