## 结论
2026-11-05，总体 score 4.0，verdict：needs_rethink。主贡献是"双钥"动作接口：用几何一致性比较结构引用与像素坐标，想在无冲突时拿到 index 的定位精度，在冲突时拿到坐标的抗劫持能力。贡献不足，原因在执行规则本身。一致时点击 ref 元素，而这时坐标本来就落在 ref 框内；不一致时以坐标为准并吸附到坐标所在元素。所以除了边距和嵌套框这类边角情况，两条分支执行的都是"坐标所在元素"，规则在决策上等价于对照组"坐标 + 吸附"。ref 头从不改变执行目标，所以"无冲突精度接近 index"无法来自交叉校验。它要成立，只能靠联合训练让坐标头本身变准，而这条路径与作者主张的"收益来自读数独立"相反。不一致信号只能说明两个读数有分歧，说明不了该信哪一个。这正是"预测出错"和"预测哪种修法更好"之间的那个缺口，方案没有给出依据。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 结构劫持（a11y/DOM 注入、过期或幽灵节点）是真实风险：2607.04334 报告过期结构跟随最高 0.88，CLAY 统计 37.4% 的 RICO 屏幕含无视觉节点，2608.08939 报告 a11y 注入攻击成功率 0.822。另一方面，训练后的坐标模型在 Multimodal-Mind2Web 上已能与 HTML 选择相当（UGround 平均 44.8，HTML Choice 42.3），说明"训练后仍存在这一取舍"本身需要先确认。0.43 的坐标错误率来自 AndroidWorld 上的零样本格式对照，不是 SFT 之后的模型。 |
| 新颖度 | 5.0 | 冗余双输出加一致性比较，属于常规冗余校验或自洽组合；"坐标吸附到元素"是已知做法；训练无关门控和 ECA 已经覆盖"执行前做像素/结构校验"。可辨认的新意只有"把坐标独立于结构作为训练约束"（删几何字段、冲突增广）。但在上述等价下，这部分新意就退化成"训练一个抗结构干扰的坐标模型"，再加一个不改变决策的 ref 头。 |
| 有效性 | 3.0 | 当前依据：(a) 零样本下坐标格式结构跟随 0.11–0.12，支持"冲突下以坐标为准可抗劫持"，但这一点"坐标 + 吸附"同样能拿到；(b) 没有任何依据说明在双钥规则下 index 的精度能保留。按规则推导，无冲突下 index 对、坐标错的样本会进入不一致分支，执行坐标，结果就是错的。所以无冲突精度约等于坐标头精度，(1)(2) 不可能靠门控同时成立。仍未知的是：联合训练会不会提升坐标头，以及这种提升会不会同时破坏独立性。即便有提升，也属于多任务训练效应，不是本方案主张的机制。 |

与起点的关系：直接回答原问题"能否同时得到两者优点"，并部分回答"格式配比如何塑造通道偏好"；时间维度的状态过期不在范围内。

实验能否判别：设计里有"坐标 + 吸附"对照，确实能暴露问题，但按上面的推导，预期结果就是双钥与它基本持平，主 Claim 会被自己的推翻条件否掉。判断 (4)"无冲突精度高于门控"也缺乏依据：门控建立在 index 模型之上，论文报告其 aligned 行为与基线相差在 0.04 以内，而双钥的无冲突精度受坐标头限制。若要拿到 index 的精度，就得在不一致时有时信 ref，这需要一个能判断哪一端更可信的信号。方案里没有这个信号，这是 Claim 阻断。另外，2607.04334 的 web 探针基于 MiniWoB++，训练用 Multimodal-Mind2Web，两者存在域迁移。

可行性：pass。Qwen2.5-VL-7B 单步 SFT，6–7 个变体，8×A100 约 2–3 天，在约束内。Multimodal-Mind2Web 的字段已核验；AndroidControl a11y 树含 bounds，可删去后序列化，但字段尚未核验。冲突探针需按 2607.04334 正文规范独立重建：论文声称有代码，但没有给出链接；文本替换、幽灵节点等编辑规范描述得足够具体，可以重建。"每变体约 20 万样本"偏高：两个数据集的单步样本合计约在 10 万量级，需靠增广补足，不影响可行性。

## 最高近邻
1. Do GUI Agents Believe Their Eyes? Diagnosing State-Belief Reliance on Pixels versus Structure（2607.04334，https://arxiv.org/abs/2607.04334）：提供格式对照（Table 16）、冲突探针和训练无关一致性门控（MiniWoB++ 每步 1.8–2.0 次查询，AndroidWorld 3.3–5.5 次）。差别：本方案改为训练两个读数，再用确定性几何比较；论文没有评测双输出，也没有训练类修法。
2. Hallucination as Exploit: Evidence-Carrying Multimodal Agents（2605.19192，https://arxiv.org/abs/2605.19192）：用 DOM/OCR/AX 验证器为动作谓词出具证书，再经确定性门控授权。差别：本方案不用外部验证器，两端校验来自模型的两个输出头。
3. Navigating the Digital World as Humans Do: UGround（2410.05243，https://arxiv.org/abs/2410.05243）：纯视觉坐标 grounding 在 Multimodal-Mind2Web 上与 HTML 选择相当。它是同任务的强坐标基线，也削弱了"训练后坐标精度必然低"的前提。
4. Not an A11y: Android Accessibility Exposes Mobile AI Agents to Indirect Prompt Injection（2608.08939，https://arxiv.org/abs/2608.08939）：给出 a11y 注入的威胁证据，修法是输入校验和隔离，不是跨通道比对。
5. Temporal UI state inconsistency / TOCTOU on computer-use agents（2604.18860，https://arxiv.org/abs/2604.18860）：PUSV 做像素级执行前校验，DOM 注入被列为未解决；与本方案同属执行前一致性校验，但不涉及结构/坐标双读数。

```json
{
  "score": 4.0,
  "contribution_scores": {"importance": 6.5, "novelty": 5.0, "effectiveness": 3.0},
  "contribution_assessment": "主贡献是'结构引用 + 屏幕坐标'双输出，配合确定性几何一致性执行，目标是同时得到 index 的无冲突精度和坐标的抗劫持能力。执行规则在两个分支里都执行坐标所在元素（一致时坐标在 ref 框内；不一致时吸附到坐标所在元素），在决策上等价于'坐标 + 吸附'，ref 头不改变执行目标，所以无冲突精度受坐标头限制，Claim (1)(2) 无法靠交叉校验同时成立；任何精度提升只能来自联合训练对坐标头的多任务效应，与'收益来自读数独立'的主张矛盾。不一致信号只说明存在分歧，不说明该信哪一端。重要性有依据（结构劫持真实存在），但训练后坐标模型的精度差距尚未确认（UGround 在 MM-Mind2Web 上与 HTML 选择相当）；新颖度只剩'独立性训练约束'这个增量；有效性缺乏机制依据。",
  "feasibility": "pass",
  "feasibility_reason": "7B 单步 SFT，6–7 个变体，8×A100 约 2–3 天；MM-Mind2Web 字段已核验，AndroidControl 含 a11y bounds 可删后序列化；冲突探针可按 2607.04334 正文规范独立重建（代码未给出链接）；样本量约 10 万量级需增广补足，属于小问题。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "机制/Claim 阻断：执行规则在一致与不一致两个分支都执行坐标所在元素，等价于'坐标 + 吸附'，ref 头不改变决策，无冲突精度无法接近 index，Claim (1) 与 (2) 不能经由交叉校验同时成立",
    "缺少'不一致时该信哪一端'的依据：一致性信号只能检出分歧，不能判断 ref 与坐标谁对，要拿到 index 精度就需要这种相对可信度信号，方案没有提供",
    "前提未核实：坐标 0.43 无冲突错误率来自零样本 AndroidWorld 格式对照，SFT 后坐标模型（如 UGround 在 MM-Mind2Web）可与 HTML 选择相当，训练后的取舍是否仍然存在、幅度多大尚未确认",
    "贡献不足：新颖度 5、有效性 3，未达到'三项 ≥6 且两项 ≥8'"
  ],
  "novelty_conclusion": "双输出 + 一致性比较是常规冗余校验；坐标吸附是已知做法；执行前像素/结构校验已有 2607.04334 门控与 ECA 覆盖。独有部分只剩'坐标独立于结构'的训练约束，而在等价性下它退化为训练一个抗结构干扰的坐标模型。",
  "closest_neighbors": [
    "Do GUI Agents Believe Their Eyes? Diagnosing State-Belief Reliance on Pixels versus Structure (arXiv 2607.04334)",
    "Hallucination as Exploit: Evidence-Carrying Multimodal Agents (arXiv 2605.19192)",
    "Navigating the Digital World as Humans Do: Universal Visual Grounding for GUI Agents / UGround (arXiv 2410.05243)",
    "Not an A11y: How Android Accessibility Exposes Mobile AI Agents to Indirect Prompt Injection (arXiv 2608.08939)",
    "Temporal UI State Inconsistency in Desktop GUI Agents: TOCTOU attacks on computer-use agents (arXiv 2604.18860)"
  ]
}
```
