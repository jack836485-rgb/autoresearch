## 结论
2026-11-03，总体 score 5.5，verdict：needs_rethink。如果关键结果成立，主贡献是指出 Hyperagents 图 3 / 表 4 的“元层面改进可迁移”（imp@50=0.63 对比约 0）主要来自让 0 分起点能被正确解析的通用修复知识，而不是在已有能力的目标上找到改进的本事。这是一项针对单个系统、单个迁移实验的审计，分量有限。原文已经交代起点 0 分属于接口失败，§5.3 也已显示起点有能力时迁移优势不显著，所以这个发现的增量本身就不大。更要紧的是，主张赖以成立的“A→A'→B 差值缩小”这一预测，仅凭提升空间收窄（headroom）就能得出。按现在的设计，实验分不开“接口知识”与“上限效应”，贡献不够。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | “自指改进者到底学会了什么”是 RSI 过程主张的关键问题，Hyperagents（NeurIPS 2026）的迁移结果也是被引用最多的受控证据，纠正它有价值。但对象只有一篇论文的一个实验（一对源域，一个目标域 IMO grading）。原文第 4 节已说明初始 0 分是 “interface failure”。§5.3 中 200 轮 DGM-H+transfer 得 0.640，从初始 agent 起跑得 0.610，p>0.05，说明“起点有能力时优势不显著”已部分公开。原文也自限为“do not yet establish unbounded or self-accelerating improvement”。这个结果改变的判断范围有限。 |
| 新颖度 | 6 | 尚未检索到有工作把 Hyperagents 的迁移优势拆成接口修复、谱系记忆和可迁移技能三部分，A' 组和记忆剥离是可辨认的增量。但协议本身就是 2610.27610 主张的同起点、同预算交换比较，2610.10611 附录 P 也给了同样的规范，SpecRSI 已经在相同起点上做过冻结改进者与更新后改进者的配对实证。把已知的对照设计用到一篇具体论文上，属于常规的审计式增量。 |
| 有效性 | 5.5 | 现有依据有四条，均已在原文 PDF 核实：(1) 初始 agent 因“没有任务特定的解析或后处理”得 0 分；(2) 表 4 中只迁移任务 agent 的一次运行得到 0.56，说明带上解析能力的任务 agent 单独就能拿到大部分收益；(3) M0 在完整 DGM-H 下 200 轮能到 0.61；(4) ProofAutoGrader 为 0.67，测试分上限大约在 0.6–0.7。这些依据都支持“A 组的 0.63 基本等于从 0 爬到可用基线”，因此“差值缩小”几乎是可以预期的。问题在于，这个预期同样能由 headroom 推出，对“接口知识还是一般技能”没有解释力。真正能区分两者的是 M_T 在 A' 和 B 组上是否仍有相对优势。按 §5.3 的量级，这个优势只有约 0.01–0.05。在 100 题测试集、每个组合 2 次重复、k=10 的条件下，测量噪声与之相当（原文 5 次运行的 CI 宽约 0.1），无法区分“小幅保留”和“消失”。此外，底座换成低价模型能否复现 A 组差距也是未知数：2609.17817 报告弱的 Ollama 模型驱动不了 Hyperagents。 |

- **与原问题的关系：** 这是原问题“改进者是否变强”的一个子问题，具体检验一项已发表证据。“跨轮累积”和“递归放大还是衰减”仍未回答。范围缩小本身不是阻断理由。
- **定位不准（claim blocker）：** 背景写“Hyperagents 只在接口失败的起点上测”，不准确。原文 §5.3 用迁移元 agent 从 ProofAutoGrader（0.67）起跑，得到 0.700。原文还比较了 transfer 起点与初始起点，结果不显著。原文确实缺少的是：在有能力的起点上，用冻结的 M0 与 M_T 做配对 imp@k 比较。
- **实验能否判别主张：** 不能（claim blocker）。
  - 简报说“不需要跨目标比较增益幅度”，但支持主张的判据恰恰是差值随 A→A'→B 缩小，这是跨目标、跨 headroom 的幅度比较。原文附录 D.3 也承认 imp@k 线性计分会低估高分段的改进。
  - 推翻主张的条件是“B 组差值与 A 组相当”，在 B 组几乎不可能达到，因为 A 组差值来自 0 分地板。
  - B 组目标取自 M0 自己在 A' 上的谱系，对 M0 存在方向不明的选择偏差：M0 的易得改进可能已被采完，也可能 M0 更熟悉这些代码。
  - 4 个 B 目标 × 2 次重复，统计上无法区分小优势与零优势。
  - A' 是唯一能直接区分“接口知识”与“一般技能”的一组，却只有 1 个目标、2 次重复。
- **可行性：pass。**
  - 原文声明公开全部日志与 agent，附录 D.5 也说明迁移 agent 以 lineage diff 链表示，并按文件过滤得到“只迁移元 agent”的版本。因此 M_T 很可能从公开 diff 直接重建，不必重跑；Google Drive 访问仍需核实。
  - 原文自修改成本约 33M token / 100 轮，即每次约 0.33M，与简报估算一致。360 次会话约 1.2 亿 token，用低价 API 约 120–360 元。IMO 每次评测只需约 0.11M token（o4-mini，100 题），简报按 0.5M 计是高估。整体在 1000 元以内。
  - 风险：原文自修改用的是 Claude 4.5 Sonnet，IMO 任务 agent 用 o4-mini。若低价模型复现不出 A 组差距，退回 Sonnet 约需 3000 元以上，超出自主额度。这一步属于执行风险，不是不可实现。

## 最高近邻
1. Hyperagents（arXiv:2603.19461，https://arxiv.org/abs/2603.19461）：被审计的对象，包括图 3 的 imp@50、表 4 的成分消融，以及 §5.3 从 ProofAutoGrader 起跑和跨运行累积的结果。原文已承认起点是接口失败，但没有在接口已修好或已有能力的起点上做冻结 M0 对 M_T 的配对比较，也没有做记忆剥离。
2. Auditing the Product, Not the Recursion（arXiv:2610.27610，https://arxiv.org/abs/2610.27610）：对 114 篇研究做全文编码，提出同起点、同预算的改进者比较标准，包含命题但不包含系统实验。本方案相当于把它的标准落到一个具体系统上。
3. SpecRSI（arXiv:2610.16491，https://arxiv.org/abs/2610.16491）：RQ3 在相同起点上比较冻结改进者与更新后改进者，已经实证“同起点配对比较”的协议。它不涉及接口失败或记忆剥离的拆分。
4. AIDE²（arXiv:2609.26457，https://arxiv.org/abs/2609.26457）：ignition test 在后期起点上比较 AIDE_47 与 AIDE_human 两个改进者，结论不确定（3 seeds）。它不分离接口修复与一般技能。
5. Verification and Self-Improvement in Agentic AI（arXiv:2610.10611，https://arxiv.org/abs/2610.10611）：附录 P 规定在共同起点和预算下测量更新后的改进者，并区分“搜索增益”与“表示或接口变化”，与 A' 组的思路重叠。它是理论加玩具实验，没有审计 Hyperagents。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 6.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献：审计 Hyperagents 迁移实验（imp@50 0.63 对比约 0），检验其优势是否来自通用的接口修复知识。这是针对单个系统、单个迁移实验的审计，分量有限。原文已承认起点是接口失败，§5.3 也已显示起点有能力时优势不显著（0.64 对 0.61，p>0.05），增量较小。协议本身是 2610.27610、2610.10611 规范和 SpecRSI 实证过的同起点对照，新颖度是常规增量。现有依据（原文接口失败的表述、表 4 只迁移任务 agent 时有一次 0.56、M0 在完整 DGM-H 下到 0.61、上限约 0.67）都支持“A 组收益约等于爬到可用基线”，但支持主张的判据（差值随 A→A'→B 缩小）可由 headroom 单独推出；A'/B 上可能剩下的小优势（约 0.01–0.05）在 2 次重复、k=10、100 题测试集下无法与零区分。",
  "feasibility": "pass",
  "feasibility_reason": "原文公开全部日志、agent 与 diff 补丁，D.5 用 lineage diff 按文件过滤构造迁移元 agent，M_T 很可能无需重跑即可重建（需核实 Drive 访问）。约 360 次 × 0.33M token ≈ 1.2 亿 token，低价 API 约 120–360 元；IMO 每次评测约 0.11M token。风险在于原文用 Claude 4.5 Sonnet 加 o4-mini，换成低价模型可能复现不出 A 组差距（2609.17817 报告弱模型驱动不了 Hyperagents），退回 Sonnet 将超出 1000 元。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献分量不足：只有两项 6 分，没有任何一项达到 8 分。这是单个系统、单个迁移实验的审计，原文已承认起点是接口失败，§5.3 也已部分显示起点有能力时优势不显著",
    "实验无法判别主张：判据“差值随 A→A'→B 缩小”是跨 headroom 的幅度比较，仅凭上限效应就能得出，与简报“不需要跨目标比较增益幅度”的说法矛盾；推翻条件“B 差值与 A 相当”几乎不可能出现",
    "统计功效不足：A' 只有 1 个目标 × 2 次重复，B 为 4 个目标 × 2 次重复，k=10，无法区分 0.01–0.05 量级的保留优势与零优势；B 目标取自 M0 自身谱系，存在方向不明的选择偏差",
    "定位不准：简报称 Hyperagents 只在接口失败起点上测，但原文 §5.3 已从 ProofAutoGrader 起跑，并比较了 transfer 与初始起点（结果不显著）"
  ],
  "novelty_conclusion": "未检索到有工作把 Hyperagents 迁移优势拆成接口修复、谱系记忆和可迁移技能，具体审计有新意；但同起点、同预算的改进者对照已有规范（2610.27610、2610.10611）和实证（SpecRSI），原文 §5.3 也部分覆盖了起点有能力的情形，新颖度属常规增量。",
  "closest_neighbors": [
    "Hyperagents (arXiv:2603.19461)",
    "Auditing the Product, Not the Recursion: The Evaluation Evidence Behind Recursive Self-Improvement Claims (arXiv:2610.27610)",
    "Drafting Agents, Not Just Tokens: Speculative Recursive Self-Improvement for Agentic Systems (arXiv:2610.16491)",
    "Recursive self-improvement of AI research agents / AIDE² (arXiv:2609.26457)",
    "Verification and Self-Improvement in Agentic AI: Foundations and Limits (arXiv:2610.10611)"
  ]
}
```
