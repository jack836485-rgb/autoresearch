## 结论
2026-11-05，总体 score 5.5，verdict：promising_needs_revision。主贡献是一个免训练的"锚点 → 关系几何区域 → 局部放大定位"流程，用来处理 GUI 关系指令，外加对"瓶颈在候选定位层"的确认。分量目前不够，原因有三。第一，"认识"部分 GUI-Primitives 作者已经明确得出（多数失败来自候选定位而非关系理解，oracle 标出两个候选后选对率提升 35–57 个百分点），本工作只是再确认一次。第二，方法在 GUI 领域尚无直接近邻，但机制本身是 REC 领域经典的"先找锚点再套空间规则"（ReCLIP、视觉程序类方法）。第三，主评测集只有 185 条，而且几何规则会直接替模型排除干扰项。三项分数没有一项达到 8。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 关系指令崩溃有两份独立报告佐证：GUI-Perturbed 下降 27–56 个百分点，GUI-Primitives 最高约 32%，所以确实值得研究。但影响范围有限：真实 agent 的指令多由 planner 生成，通常可以直接点名目标；主评测集只有 185 条，每种 primitive 28 条，containment 和 occlusion 只有合成样本。工具成功后，最多算一个针对特定指令形态的推理时补丁，不会改变领域对 grounding 瓶颈的判断，因为这个判断原论文已经给出。 |
| 新颖度 | 7 | 我在 GUI grounding 领域没有检索到"以被点名锚点为中心、按关系词划几何区域再局部定位"的工作。现有 zoom 类方法都以自身预测为中心：RegionFocus、DRS-GUI 的 Focus/Shift/Scatter、ZoomUI、Chain-of-Ground。Chain-of-Ground 的 "anchor/reference" 指的是模型自己的上一轮预测，不是指令里点名的元素。按跨领域迁移规则，这部分给 7。不给更高有三点原因：(a) "瓶颈在候选定位"这一现象已由 GUI-Primitives 发表，并且有 oracle 两候选标注实验支撑，不能算新增认识；(b) 机制在 REC 领域是现成做法，ReCLIP 就是"解析 + 空间关系启发式"；GUI-Perturbed README 也已把关系指令写成"先找 landmark、再判关系、再解析目标"三步；(c) 结构性适配（容器边框、列表切行）偏工程，还没有说明朴素迁移会在 GUI 上遇到什么特有问题。 |
| 有效性（先验合理性） | 6 | 支持依据：点名式定位在 ScreenSpot 类任务上本来就强，锚点是被点名的，词面通路可用（Lexical Coupling）；放大局部区域能提高定位，已有多篇 zoom 工作证实；Qwen2.5-VL-7B 有 11.8% 的预测落在锚点上，说明锚点通常能找到；oracle 标出候选后的大幅提升，说明"给对区域就能选对"在通用 VLM 上成立。与关键假设冲突的已有证据有三条：① GUI-Primitives 中 containment 的候选内选对率只有 0.548，与随机无显著差异，说明对这类关系，瓶颈就在关系选择，Claim 2 的"候选内选择基本不变"不能整体成立；② GUI-Perturbed 的定性错误分类里有"找对 landmark 但点错方向"这一类；③ primitive-aware CoT 在 GUI-Primitives 上没有显著增益。另有迁移条件未核实："候选定位是主瓶颈"的数据主要来自通用 VLM，GUI-Primitives 没有评测 UI-TARS、UGround、Jedi、GTA1、Qwen3-VL 等 GUI 专训模型，而 GTA1-7B 在 GUI-Perturbed 关系指令上已有 65.8%。最后，现有几何规则与基准里的关系并不对应："farthest from"不是锚点周围的环形区域，"outside"是容器的补集，"same row/column as"（alignment 这一 primitive）在规则集中完全缺失。 |
| 待预研 | — | 不计分：三步流程相对单次定位和强 zoom 基线的增益幅度；GUI 专训 7B 模型在 GUI-Primitives 上还有多少余量；真实截图子集（290 条）上的增益；GUI-Perturbed 自由形式关系（含功能关系）上的增益；点名式基准上的零损伤是否成立。 |

**与起点问题的关系**：回答的是原问题的前半部分，即"崩溃在哪一层"，并给出针对这一层的修法。原问题中"什么训练信号能教会关系绑定"没有回答，containment 和 occlusion 这类真正的关系弱点也没有解决。按规则，这次转向本身不扣分。

**实验能否判别主张**：Claim 1 可以检验，但对照不足。按"同任务、允许能力内的已发表改进"要求，至少还缺四个对照：一是 oracle 两候选标注的可部署版本，即元素检测/解析器（如 OmniParser）加 Set-of-Mark，再由同一模型选择，它同样直接作用于"候选定位"层，是最直接的竞争解释；二是 DRS-GUI 这类带 Shift 的免训练区域搜索；三是 GTA1 式测试时采样加选择；四是单次调用内"先找锚点再找目标"的 CoT 提示（GUI-Perturbed 显示 CoT 能缩小 UI-TARS 的差距）。只和"粗定位后放大""不确定性放大"比，排除不了上面这些解释。Claim 2 存在构造性混淆：左右、上下的条带区域本身就把配对干扰项排除在外，所以"候选内选对率"会被规则推高，而不是"基本不变"。这样一来，主指标的提升可能来自外部规则替模型做了关系判断，而不是来自"让模型找到候选"。真正能区分两种解释的是"锚点周围固定半径放大"消融，但它现在只是辅助消融，不在主判定里。Claim 2 和 Claim 3 只能在 GUI-Primitives 上测：GUI-Perturbed 只发布了 gt_bbox，没有锚点、干扰项和关系类型标注。GUI-Primitives 有 anchor_id，可以经 ui_corpus/mixed_corpus 的元素池还原锚点框，用于真值锚点上限分析，但这一步需要实际核对覆盖率。核心集 185 条去掉 occlusion 后约 157 条，按七类分报时每类只有 28 条，难以支撑分关系结论。

**可行性：pass**。两个数据集都已公开，路径我已核实：GUI-Primitives 的 items.jsonl 含 target_bbox、distractor_bbox、anchor_id 和 primitive 标签，截图随附；GUI-Perturbed 关系指令为 4 个视觉变体 × 390 条 = 1,560 条。所有模型都是公开权重，流程是纯推理，每条样本 2–3 次前向，在 2×A100 上 1–2 天量级可以完成，不需要 API 或训练，符合用户约束。这里的可行性不足之处是规范层面：关系规则集不完整，GUI-Perturbed 缺少中间标注。不是资源不足。

## 最高近邻
1. **GUI-Primitives**（https://arxiv.org/abs/2608.21832）：重叠在于提出了"失败多在候选定位而非关系理解"的诊断，并用 oracle 两候选标注得到 +35–57 个百分点，也报告了 primitive-aware CoT 无效。差别：它不提供可部署的方法，也没有评测 GUI 专训 7B 模型。
2. **GUI-Perturbed**（https://arxiv.org/abs/2604.14262）：在 Qwen2.5-VL、UI-TARS-1.5、GTA1 三个 7B 模型上量化了关系指令的下降，测了 CoT，把关系任务描述为"landmark → 关系 → 目标"三步。差别：没有分层量化，也没有提出修法。
3. **DRS-GUI**（https://arxiv.org/abs/2605.15542，CVPR 2026）：免训练、MCTS 调度 Focus/Shift/Scatter 做区域搜索，搜索可以离开初始预测。差别：不利用指令中点名的锚点和关系词。是必须补上的强测试时基线。
4. **Chain-of-Ground**（https://arxiv.org/abs/2512.01979）：免训练多步定位，以自身上一轮预测作为参考标记反复修正，并声称能"关系化推理"。差别：参考点是自身预测，不是指令中的锚点，也没有关系规则。
5. **ReCLIP**（https://arxiv.org/abs/2204.05991）：自然图像零样本 REC，解析指代表达后用空间关系启发式在候选上做选择，是本方法机制的跨领域来源。差别：领域是自然图像而非 GUI，候选由提议框提供，不是锚点中心的放大定位。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 7.0, "effectiveness": 6.0},
  "contribution_assessment": "主贡献为免训练'锚点→关系几何区域→局部放大定位'流程，加对'瓶颈在候选定位'的确认。重要性6：问题真实，但应用面窄（planner 通常可直接点名目标），主集仅185条，且诊断结论原论文已给出。新颖度7：GUI 领域未检索到锚点中心的关系区域方法，但现象非新（GUI-Primitives 已用 oracle 候选标注得出），机制是 REC 经典做法（ReCLIP），GUI 侧适配偏工程。有效性6：锚点被点名、放大有效、oracle 提升大，均支持先验合理性；但 containment 候选内选择在随机水平、GUI-Perturbed 有'找对 landmark 但点错方向'的错误、primitive CoT 无效，都与 Claim 2 部分冲突；GUI 专训模型（UI-TARS/GTA1/Qwen3-VL）是否同样以候选定位为主瓶颈未经核实；规则集与基准关系不对应（farthest、outside、alignment 缺失）。待预研：增益幅度、GUI 专训模型余量、真实截图与 GUI-Perturbed 上的迁移、零损伤。",
  "feasibility": "pass",
  "feasibility_reason": "GUI-Primitives（target/distractor bbox、anchor_id、primitive 标签、截图）与 GUI-Perturbed（1,560 条关系指令，仅 gt_bbox）均已公开并核实；模型为公开权重；纯推理，每样本2–3次前向，2×A100 约1–2天，符合约束。限制：GUI-Perturbed 无锚点、干扰项与关系标注，Claim 2/3 只能在 GUI-Primitives 上测；锚点框需经元素池由 anchor_id 还原。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献不足：三项均未达到8（6/7/6），'候选定位是瓶颈'的认识已由 GUI-Primitives 发表（含 oracle 两候选标注实验），剩余方法贡献的重要性有限",
    "Claim 1 缺少同任务强对照：OmniParser 等检测器加 Set-of-Mark 的可部署候选标注、DRS-GUI 式区域搜索、GTA1 式测试时采样选择、单次调用的锚点优先 CoT，现有两个 zoom 基线无法排除这些竞争解释",
    "Claim 2 存在构造性混淆：方向条带直接排除配对干扰项，主指标提升可能来自外部规则替模型做关系判断，而非'找到候选'；能判别两种解释的固定半径消融未列入主判定",
    "几何规则与基准关系不对应：farthest from、outside、same row/column（alignment）没有对应规则，containment 候选内选择在随机水平，与 Claim 2 '选择基本不变'冲突"
  ],
  "novelty_conclusion": "GUI 领域未检索到以被点名锚点为中心、按关系词划区域再局部定位的方法，迁移新意可计为7；但诊断现象已由 GUI-Primitives 发表，机制源自 REC（ReCLIP 及视觉程序类方法），GUI 侧适配偏工程，达不到8。",
  "closest_neighbors": [
    "GUI-Primitives: Diagnosing Spatial Reasoning Failures in Vision-Language GUI Grounding (arXiv:2608.21832)",
    "GUI-Perturbed: Domain Randomization Reveals Systematic Brittleness in GUI Grounding Models (arXiv:2604.14262)",
    "DRS-GUI: Dynamic Region Search for Training-Free GUI Grounding (arXiv:2605.15542)",
    "Chain-of-Ground: Improving GUI Grounding via Iterative Reasoning and Reference Feedback (arXiv:2512.01979)",
    "ReCLIP: A Strong Zero-Shot Baseline for Referring Expression Comprehension (arXiv:2204.05991)"
  ]
}
```
