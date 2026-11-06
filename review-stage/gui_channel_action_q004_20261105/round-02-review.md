## 结论
2026-11-05，总体 score 4.5，verdict：needs_rethink。主贡献是一条训练标签规则：按“是否可见渲染”决定标签跟随像素还是跟随结构，再加上对可见文本的冲突增广。这个贡献不够，原因有三。第一，它防住的“可见文本在结构里被改、像素不变”在真实网页里主要是过期快照之类的非对抗情形；攻击者真正可控的注入面（不可见节点、aria-label/title、只存在于结构的幽灵节点）按设计恰好继续信任结构，所以“打破覆盖与信任的取舍”在安全意义上大体没有成立。第二，按可见性过滤或剥离 DOM 内容是常见的工程做法，模态冲突增广训练也已有先例，组合后的新意有限。第三，去掉 bbox 后，结构里的元素 id 与像素对象没有对齐通道，核心标签规则在冲突样本上要求的绑定能力输入里并不存在；另外缺少“harness 直接遮蔽可见文本”这一零训练强基线，它很可能单独解释预期收益。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 5.0 | 两端取舍确实存在：2607.04334 测到坐标格式结构跟随 0.11、无冲突错误 0.43，index 格式结构跟随 0.90；UGround 在该文中结构跟随只有 0.03（web）。问题在于本方法“信任”一端只覆盖已渲染且完整显示的文本。攻击者改 DOM 文本节点时，像素通常随之改变，所以“结构变、像素不变”的可见文本冲突多来自过期快照（该文实景只有 42 个 stale）、CSS 伪内容或遮挡。2607.04334 里的幽灵节点威胁（坐标格式 0.84–1.00 照样执行）以及 aria/title 注入都落在本方法明确信任结构的 `rendered=no` 或属性侧。定位关键词写了 prompt injection，但真正被缓解的主要是同步与过期问题，影响范围有限。 |
| 新颖度 | 5.5 | 能辨认的增量是：在 GUI 双通道上把“渲染可见性”用作训练时的标签分派条件，而不是推理时的门控。近邻已覆盖其中的组成部分：渲染可见性过滤是浏览器 agent harness 的常见规则（如 agent-browser-shield 剥离 CSS 隐藏或屏外文本，BrowserGym 提供可见性元素属性）；模态冲突的反事实增广训练有 KOALA、CARGO-VL（图像与检索文本按来源仲裁）；双通道对抗训练有 DMAST；2607.04334 已提出像素优先的门控，并指出“训练消费结构就学会信任结构”。去掉论文名后，剩下的是“可见性规则 + 冲突增广”的常规组合，没有新的机制或理解。 |
| 有效性 | 5.5 | 现有依据：2607.04334 的白盒消融显示，web 文本冲突中消去被复制的结构值能把 0.63 的结构跟随翻回像素（随机消去 0.03），说明“复制该值”是主要通路，抑制复制有望降低跟随；标签直接训练被测行为，因此探针 (1) 在分布内大概率会下降。仍未知且存在大跳跃的有三处。(a) 输入去掉了 bbox，又没有在截图上画 id 标记，冲突样本中模型无法从像素对象定位到对应 id（目标结构文本被换成 B 时，只能靠 DOM 顺序、标签名这类弱线索或排除法），学到的可能是“挑结构文本缺失者”之类的捷径，不是“以像素为准”。(b) 探针与训练增广用同一生成器（换成页面上的另一字符串），结构跟随下降可能只是分布内拟合，对 stale 或 CSS 这类真实分歧能否迁移没有依据。(c) 结构必需子集上纯视觉的缺口完全没有测过：离线单步评分里，视口外目标对纯视觉的正确动作是滚动，对混合模型的正确动作是直接给 id，两种评分口径不同，缺口可能只是度量造成的。 |

与起点的关系：这是原问题的收窄子问题，从“定位精度与抗劫持的取舍”改为“信息覆盖与信任的取舍”。原问题中动作格式配比如何塑造通道偏好、移动端与桌面、多步实景失败都未回答。收窄本身不构成阻断，但收窄后剩下的贡献分量不足。

实验能否判别主张：现有设计不能判别，具体有三点。① 缺少零训练的确定性基线：harness 直接清空或遮蔽 `rendered=yes, text_shown=full` 节点的结构文本，保留不可见信息，再配合同等的 id–像素对齐方式。它在 (1)(2) 上很可能达到同样效果，且不需要训练，这时“学进策略”的价值就不成立了。现有对照里的“只加标记”和“全增广”都排除不了这个解释。② id 与像素的对齐方式（截图上的 SoM 标记，或渲染得到的几何信息）没有定义，(1) 的成败会被这一选择主导。③ 结构必需子集需要统一的成败口径：纯视觉滚动后定位是否计为正确，否则 (2) 的缺口无法解释。此外，2607.04334 训练无关门控在 MiniWoB++ 上每个动作额外 1.8–2.0 次查询，独立复现可行，但该文代码链接未公开，应如实标注。

可行性：pass（有条件）。Multimodal-Mind2Web 的 HF 行里确实有 `cleaned_html`/`raw_html`、`backend_node_id`、`bounding_box_rect`、`aria_label`、`title`、整页截图（示例页根节点约 1280×5429）；UGround 也是把整页截图切成 1280×1000 块评测，约 80% 目标在第一块，所以视口外子集样本充足。截断与图标 + aria-label 两类能否各凑满 100 个未知，按计划如实报告即可。离线可见性只能近似，`elementFromPoint` 遮挡判断无法复原，而最小实验全程离线，所以训练和测试都用同一近似标记，这一点应写清楚。训练集原始约 7.7k 个动作，“每变体 5–10 万样本”只能靠增广倍增，同数据训练的纯视觉 SFT 会远弱于 UGround-V1-7B。5 个 7B SFT 加离线评测在 8×A100 上 1–2 天，在预算内。

## 最高近邻
1. Do GUI Agents Believe Their Eyes? Diagnosing State-Belief Reliance on Pixels versus Structure（2607.04334，https://arxiv.org/abs/2607.04334 ）：同一冲突探针、同一结构跟随度量，测了动作格式扫描、UGround/Aguvis 的低结构跟随、白盒复制消融、像素自检门控和幽灵节点威胁。差别：该文没有做训练式修法，也不保留不可见信息。
2. Dual-Modality Multi-Stage Adversarial Safety Training（DMAST，2603.04364，https://arxiv.org/abs/2603.04364 ）：针对截图 + a11y 双通道 web agent 的对抗训练（IL→SFT→GRPO 自博弈）。差别：它处理两通道被一致污染的攻击，不按可见性分派信任。
3. Hallucination as Exploit: Evidence-Carrying Multimodal Agents（ECA，2605.19192，https://arxiv.org/abs/2605.19192 ）：用 DOM/OCR/AX 验证器生成证书，再由确定性门控授权动作。差别：运行时验证，不训练策略。
4. CARGO-VL: Counterfactual Arbitration with Risk-Constrained Group Optimization（2608.04509，https://www.alphaxiv.org/abs/2608.04509 ）：用反事实成套样本训练 VLM 在图像与文本证据之间按来源仲裁。差别：任务是 VQA/RAG，不是 GUI，仲裁信号由模型判断，不是渲染可见性。KOALA（2502.14908，https://arxiv.org/abs/2502.14908 ）同属冲突增广训练一类。
5. UGround / SeeAct-V（2410.05243，https://arxiv.org/abs/2410.05243 ）：纯视觉 grounding 在 Multimodal-Mind2Web 上与 HTML Choice 相当或更好，是“信任”一端的强基线。差别：完全不用结构，视口外目标靠滚动。可见性过滤规则的工程先例见 agent-browser-shield（https://pixiebrix.github.io/agent-browser-shield/rules/ ），需检索是否有学术论文系统评测过。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 5.0, "novelty": 5.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是按渲染可见性分派标签（可见完整文本跟随像素并做冲突增广，不可见信息跟随结构）的训练规则。重要性有限：可见文本的结构-像素冲突在真实网页中主要来自过期快照，真正的对抗注入面（不可见节点、aria/title、幽灵节点）按设计继续被信任，'打破覆盖与信任的取舍'在安全意义上基本未成立。新颖度有限：可见性过滤是常见 harness 规则，冲突增广训练有 KOALA/CARGO-VL/DMAST 等先例，组合属常规。有效性：2607.04334 白盒复制消融（0.63 vs 0.03）支持抑制复制可降低跟随，但去掉 bbox 后 id 与像素无对齐通道，探针与增广同分布，纯视觉在结构必需子集上的缺口未测且受单步评分口径影响。",
  "feasibility": "pass",
  "feasibility_reason": "Multimodal-Mind2Web 有 cleaned_html、backend_node_id、bounding_box_rect、aria_label/title 与整页截图，可离线切视口、近似可见性并构造三类子集；5 个 7B SFT 加离线评测约 1-2 天，在 8×A100 预算内；门控按正文可独立复现。原始训练约 7.7k 动作，样本量需靠增广；遮挡判断无法离线复原。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献不足：重要性与新颖度均达不到 8，三项门槛无法通过；主要缓解的是非对抗的过期快照冲突，对抗注入面按设计被继续信任",
    "Claim 阻断：结构去掉 bbox 且未定义截图 id 标记，冲突样本中 id 与像素对象无法对齐，标签规则要求的能力在输入中不存在，(1) 的结果可能来自捷径",
    "Claim 阻断：缺少零训练的确定性基线（harness 直接遮蔽可见完整文本的结构字符串，保留不可见信息），它可能单独解释 (1)(2) 的收益，使'学进策略'无独立价值",
    "Claim 阻断：结构必需子集对纯视觉（应滚动）与混合（直接给 id）的正确性口径不同，(2) 的缺口可能是度量造成的"
  ],
  "novelty_conclusion": "可见性过滤与模态冲突增广训练均有先例，组合在 GUI 双通道训练中未见直接报道，但属常规组合，增量有限；2607.04334 已覆盖问题、探针与像素优先门控。",
  "closest_neighbors": [
    "Do GUI Agents Believe Their Eyes? Diagnosing State-Belief Reliance on Pixels versus Structure (2607.04334)",
    "Dual-Modality Multi-Stage Adversarial Safety Training (DMAST, 2603.04364)",
    "Hallucination as Exploit: Evidence-Carrying Multimodal Agents (ECA, 2605.19192)",
    "CARGO-VL: Counterfactual Arbitration with Risk-Constrained Group Optimization for Vision-Language Models (2608.04509)",
    "Navigating the Digital World as Humans Do: Universal Visual Grounding for GUI Agents (UGround, 2410.05243)"
  ]
}
```
