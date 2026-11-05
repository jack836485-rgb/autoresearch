## 结论
2026-11-04，总体 score 5.5，verdict：promising_needs_revision。主贡献是：在同一模型、同一纠正率/破坏率指标下建立 6 种失败类型的 steering“修复地图”，并用三个干预前可算的量（在场性、类内离散度、标签混淆度）前瞻预测修复效果。这个问题有价值，但目前贡献不够：三个量都直接取自已有论文；“类型级规则”只有 2 个留出类型，无法检验；实例级检验对探针解码 steering 接近同义反复，而且缺少最朴素的强对照；信息来源类任务被称为“修复”，可能只是评测集里没有“目标标签错误”的样本。这个竞争解释目前还没有分离开。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | “steering 何时是修复、何时只是先验偏移”对表示干预研究有实际判断价值，同模型同指标的对比也确实缺失。但产物主要是一个 3 模型 × 6 类型的分析，加一条经验规则。只有当规则真能前瞻预测时，它才会改变领域判断，而按现设计这一点很难得到证实。 |
| 新颖度 | 6.0 | 三个量分别来自 2609.11216（在场性/探针解码目标）、2611.04757（类内离散度、RGS）和 2608.29431（标签混淆、CRT）。“预测 steering 在哪里有效”已有 2604.15557（logit-lens 线性可达性 A_lin，与“在场性”高度相近）和 2505.22637（训练差向量的方向一致性/方差预测 steerability，与“离散度”相近）。纠正/破坏的结局审计已由 2609.36138（SAKIKO）系统化。可辨认的增量在于跨类型统一评测加前瞻留出预测，属于有内容的组合，但机制和视角本身不新。 |
| 有效性 | 5.5 | 当前依据：每个量都在各自单一任务上有直接证据（绑定任务探针 steering +0.168；替换语料上检索胜过固定方向；矛盾盲视 CRT 准确率从 99.6% 跌到 40.4%；过度思考可解码但 steering 效果约为 0）。缺口有四点：(a) 这些证据都来自单一任务，三个量在跨类型时是否单调决定纠正/破坏，没有任何依据；而且三个量很可能与“任务类别”共线，没有可分离的变化。(b) 离散度和混淆度是类型级量，只能在 4 拟合 + 2 留出的类型上检验，每个模型只有 2 个留出点，排序一致几乎没有统计判别力。(c) 实例级 AUROC 只检验“在场性”。用它去预测“探针解码目标 steering”的纠正概率接近同义反复：探针给金标准答案的置信度高时，沿探针答案 steer 本来就是沿金标准 steer。(d) 2610.20067 用“偏好外部知识”的单一方向修复知识冲突，按 brief 对标签混淆度的定义（成功与输出某标签的相关），该任务的混淆度也应很高，却被报告为修复。这提示分界可能来自评测集组成，即评测集中是否存在“steer 方向所指标签恰好错误”的样本，而不来自三个量。这一点尚未验证。 |

**与起点问题的关系：** 属于原问题。brief 把“分界由什么决定”具体化为三个可测量。原问题仍未回答的部分是：如果三个量与任务类别共线，“由什么决定”仍然只是相关关系。

**实验能否判别主张：** 目前不能充分判别，原因有三。
1. 信息来源类任务没有构造对称的“目标标签错误”子集（BCT 中建议答案本身正确的样本、知识冲突中上下文错误的样本），因此“修复 vs 标签偏移”在这两类上没有被同等审计。CRT 式审计只用在矛盾盲视上。
2. 实例级主张只与“失败可解码性”比较，缺少最直接的强对照：模型自身在输出位置对金标准选项的 logit/概率，以及 2604.15557 的 logit-lens 可达性。若这两个对照的 AUROC 与探针在场性相当，“在场性”就没有独立的解释力。
3. 类型级前瞻预测样本量太少，结果对或错都难以推翻主张。

**可行性：pass。** 已核验：BCT 代码库（prakharg55/bias-direction-EMNLP）、知识冲突代码库（AheadOFpotato/knowledge_selection_steering）和 SAKIKO 代码库都可以匿名访问；HF 上的 MoyYuan/Asymmetricity-2.0（MIT）与 nvidia/When2Call（CC-BY-4.0）公开可用。RGS、类条件 CAA 与探针目标 steering 没有公开代码，但 2611.04757 摘要已给出算法要点（类内 k 近邻状态均值；k 等于类大小时退化为类条件差均值），可以独立实现。绑定任务需按 2609.11216 的规范自行构造（合成任务，成本低）。过度思考标签需按“重采样能答对、长 CoT 答错”重建；MCQ 判分简单，100–200 元可控。主要计算量是 3 模型下约 1.3k 样本 × 若干条件 × 约 1k token 的 steered CoT 生成，在 2×A100 上 1–2 天偏紧但可行，正式阶段 8×A100 余量充足。上述各点是证据和判别问题，不是可行性问题。

## 最高近邻
1. **When Does Correction Become Repair? Mechanistic Auditing of Internal Interventions in Tool-Using LLMs**（arXiv 2609.36138, https://arxiv.org/abs/2609.36138）：在 7 个模型上对 When2Call/MetaTool 做落点审计和纠正/破坏统计，并已明确提出“行为移动 ≠ 修复”。差别：只覆盖工具决策，不给干预前的预测量。
2. **When Should an LLM Steering Edit Depend on the Input?**（arXiv 2611.04757, https://arxiv.org/abs/2611.04757）：用类内目标离散度事先判断固定方向、类条件或检索规则哪个更好。差别：只用替换语料和行为语料，不测推理失败的纠正与破坏。
3. **Predicting Where Steering Vectors Succeed**（arXiv 2604.15557, https://arxiv.org/abs/2604.15557）：用 logit-lens 线性可达性 A_lin 事先预测 steering 效果（ρ≈0.86–0.91），与“在场性”高度重叠。差别：结局指标是目标 token 概率变化，不做逐样本的纠正/破坏统计。
4. **Understanding (Un)Reliability of Steering Vectors in Language Models**（arXiv 2505.22637, https://arxiv.org/abs/2505.22637）：训练激活差的方向一致性预测 steering 是否可靠，与“离散度”这一视角重叠。差别：不涉及推理失败和标签混淆。
5. **Evaluating the Semantic Specificity of Representation Steering in Language Models**（arXiv 2608.29431, https://arxiv.org/abs/2608.29431）与 **Legible Failures**（arXiv 2609.11216, https://arxiv.org/abs/2609.11216）：分别提供标签混淆/CRT 审计，以及“错而可读”的探针解码 steering。差别：各自只覆盖单一失败类型。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是在同模型同指标下比较 6 种失败类型的纠正率/破坏率，并用在场性、类内离散度、标签混淆度三个量前瞻预测修复效果。重要性中等偏上：问题真实，统一对比确实缺失。新颖度为组合级：三个量分别取自 2609.11216、2611.04757、2608.29431，2604.15557 的 A_lin 与在场性高度重叠，2505.22637 与离散度重叠，2609.36138 已系统化纠正/破坏审计。有效性不足：现有证据都来自单一任务；三个量可能与任务类别共线；类型级规则只有 2 个留出点；实例级 AUROC 对探针解码 steering 近乎同义反复，且缺少模型自身金标准 logit 和 logit-lens 可达性两个强对照；知识冲突按定义混淆度也应很高却被报告为修复，提示分界可能来自评测集是否含“目标标签错误”样本，这一竞争解释尚未分离。",
  "feasibility": "pass",
  "feasibility_reason": "BCT、知识冲突、SAKIKO 代码库和 Asymmetricity-2.0、When2Call 数据集已核验公开可用；RGS、类条件 CAA 和探针 steering 可按论文规范独立实现；绑定任务为合成构造；过度思考标签重建成本约 100–200 元；3 模型的 steered CoT 生成在 2×A100 上 1–2 天偏紧但可行，正式 8×A100 余量充足。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达到：三项分数没有两项 ≥8，新颖度只到组合级（三个量都取自已有论文，2604.15557 的 A_lin 和 2505.22637 分别与在场性、离散度重叠）",
    "类型级前瞻规则只有 2 个留出类型，离散度与混淆度只能在类型级检验，无法判别三量主张",
    "实例级检验对探针解码 steering 接近同义反复，且缺少模型自身金标准 logit/概率和 logit-lens 可达性这两个强对照，在场性的独立解释力无法确立",
    "信息来源类任务没有对称的“目标标签错误”子集（建议答案正确的 BCT 样本、上下文错误的知识冲突样本），“修复 vs 标签偏移”的分界可能来自评测集组成；按 brief 自己的定义，知识冲突的混淆度应很高却被称为修复，这一竞争解释未被分离"
  ],
  "novelty_conclusion": "统一同指标的跨类型修复地图和前瞻预测是可辨认的增量，但三个预测量都来自已有工作，且与 2604.15557、2505.22637 的 steerability 预测思路重叠；纠正/破坏审计已由 2609.36138 和 2608.29431 系统化。目前属于有内容的组合，没有独立的新机制或新视角。",
  "closest_neighbors": [
    "When Does Correction Become Repair? Mechanistic Auditing of Internal Interventions in Tool-Using LLMs (2609.36138)",
    "When Should an LLM Steering Edit Depend on the Input? (2611.04757)",
    "Predicting Where Steering Vectors Succeed (2604.15557)",
    "Understanding (Un)Reliability of Steering Vectors in Language Models (2505.22637)",
    "Evaluating the Semantic Specificity of Representation Steering in Language Models (2608.29431); Legible Failures: Detecting and Repairing In-Context Binding Errors (2609.11216)"
  ]
}
```
