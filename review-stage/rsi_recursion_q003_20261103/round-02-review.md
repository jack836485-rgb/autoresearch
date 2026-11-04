## 结论

2026-11-03，总体 score 4.0，verdict 为 needs_rethink。

主贡献是把 DGM-H 的跨域迁移增益（imp@50：0.630 对 0）在编辑层面归因到"抗选择噪声的统计纪律"。现在这个贡献不够，原因有三。第一，这个机制假说和 DGM-H 的实际结构对不上：接受/父代选择和评估器都在可编辑边界之外。第二，目标域的增益是从格式失败的 0 分地板起步的，不是选择噪声主导的情形。第三，主实验依赖开源模型驱动 Hyperagents，而已有报告表明更强的开源模型都驱动不了它。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 如果能弄清"改进后的改进者"是学到了可迁移的元能力，还是一次性补齐的统计卫生，会影响 RSI 领域对递归增益的解读，所以问题值得问。但只在一个系统、一个目标域（IMO 批改）、5 个迁移 hyperagent 上做，结论的外推范围有限。 |
| 新颖度 | 5 | Hyperagents 自己在附录 D.5 已经按 lineage 的 code diff 过滤 hunk，做过 meta 对 task 的成分消融（meta-only 0.620，both 0.630）。本方案是把同一套 hunk 过滤做得更细，再借用 Winner's Curse 的框架给编辑贴标签。去掉 Hyperagents 这个名字，剩下的独立增量是"元级增益主要来自统计纪律"这个假说本身，有可辨认的新意，但很接近"补完原论文的消融"。 |
| 有效性 | 4 | 现有依据只说明两点：这类循环里选择噪声很大（Winner's Curse、Harness Ceiling）；DGM-H 长出的机制名字里有 performance tracking 和 memory。依据迁移到本设置需要三个条件，三个都不成立或有反证。(1) 按 Hyperagents A.5，evaluator、parent selection 和迭代预算都在可编辑边界外，meta agent 没法实现"重复评估后再接受"，人工抗噪接受规则也没有可插入的位置；如果去改 select_next_parent，改的是生成算法 G，不再是 meta agent 本身。(2) 目标域初始 task agent 得 0 分，是因为输出格式不对、缺少解析，initial meta agent 跑 50 次后仍是 0（CI 0–0.13）。0.63 的差距约为单次 σ（约 0.02）的 30 倍，更像是诊断评估输出并修好解析或批改逻辑的能力差异，不是"赢家诅咒"式的误选。(3) 方案引用的 Winner's Curse 论文自己报告，所测的接受规则在整次运行上没有胜过贪心接受。这和"人工基线收回大部分差距"的预期相反。Hyperagents E.3 列出的元能力里，还有 evaluation analysis utilities、compute-aware planning、bias detection 等，它们同样是有竞争力的解释。仍然未知的是：编辑能否干净地切开，开源模型下效应还在不在。 |

**与原问题的关系：** 这是起点问题（递归是否成立、为什么成立）的机制化子问题，转向本身没有问题。原问题里"跨轮收益是累积、到平台还是被侵蚀"这一部分仍然没有回答，"补齐后递减"的预测也不在实验矩阵里。

**实验能否判别：** 判别力不足。"统计纪律"这一类把两样东西捆在了一起：一是信息反馈类机制（表现追踪、失败记忆，它们本质上是让 meta agent 看到并诊断评估结果），二是真正的抗噪操作。所以即使"剔除该类后 imp 大降"成立，也区分不了"抗噪"和"更好的失败诊断"这两个竞争解释。方案没有一个随评估噪声水平变化的判别条件，比如改变验证集大小或重复次数，看该类编辑的贡献是否跟着变。此外，"迁移 meta agent"用的是 5 个里的哪一个还没定，编辑之间的依赖（memory 文件被提示读取等）也可能让剔除后的代码直接坏掉，不只是性能下降。

**可行性：fail。**
- 主路线行不通。2609.17817 报告，gpt-oss-120b、Qwen3.5-397B 乃至 DeepSeek V4 Pro 都驱动不了 Hyperagents，只能产出空的或坏掉的 patch。方案拟用的 Qwen3-235B-A22B 比它们弱，门槛检验大概率直接失败。
- IMO 批改原设置用 o4-mini 做评估，本地替换后任务本身也变了。
- API 路线：按 Hyperagents D.2，50 次迭代的自修改约 1650 万 token，用的是 Sonnet 4.5。方案自己估计 1000 元约够一次 100 次迭代的运行，所以只够每个条件约 1–2 次。6 条件 × 3 种子在 API 上会明显超出 1000 元的自主预算。
- 数据方面，代码和日志确实公开，D.5 的 hunk 级 diff 表示也说明谱系可以重建，这部分没有问题。

## 最高近邻

1. Hyperagents（Zhang et al., 2603.19461）https://arxiv.org/abs/2603.19461 。重叠：同一系统、同一迁移实验，D.5 已用 lineage diff 的 hunk 过滤做了 meta/task 成分消融，E.3 定性列出了各项元能力。差别：没有在 meta agent 内部按编辑类别做因果剔除或移植。
2. The Winner's Curse in LLM Self-Improvement Loops（2610.09239）https://arxiv.org/abs/2610.09239 。重叠：选择噪声与接受规则。差别：研究对象是指令改写循环，不是改进者自身的演化；而且它报告所测接受规则在整次运行上不胜贪心，削弱了本方案人工基线的预期。
3. Auditing the Product, Not the Recursion（2610.27610）https://arxiv.org/abs/2610.27610 。重叠：区分过程主张与产物主张，规定 swap test，并把 Hyperagents 列为有 frozen-meta 控制的少数研究。差别：做审计规范，不做成分归因。
4. Recursive self-improvement of AI research agents / AIDE²（2609.26457）https://arxiv.org/abs/2609.26457 。重叠：同起点对比不同外环 agent 的 ignition test，讨论噪声下误接受会把后续搜索带偏。差别：据 2610.27610 的引述，3 个种子下结果不确定，没有编辑级归因。正文细节我没有逐页核验。
5. Reflections on Trusting Trust, Revisited（2609.17817）https://arxiv.org/abs/2609.17817 。重叠：在 Hyperagents 上实际运行，并报告开源模型驱动不了它、Polyglot 存在 git 历史答案泄漏。差别：做的是安全攻击，不做归因。它在这里是可行性的关键反证。

```json
{
  "score": 4.0,
  "contribution_scores": {"importance": 6.0, "novelty": 5.0, "effectiveness": 4.0},
  "contribution_assessment": "主贡献是将 DGM-H 迁移增益（imp@50 0.630 对 0）在编辑层面归因到抗选择噪声的统计纪律。重要性 6：问题有意义，但只在单系统、单目标域、5 个迁移体上做。新颖度 5：Hyperagents D.5 已用 hunk 过滤做过 meta/task 成分消融，本方案是更细粒度的延伸加上 Winner's Curse 的标签，接近补完原论文。有效性 4：DGM-H 的接受/父代选择和评估器不可编辑（A.5），meta agent 无法实现重复评估再接受；目标域增益从格式失败的 0 分起步，约为噪声 σ 的 30 倍，不是选择噪声主导的情形；所引 Winner's Curse 自己报告接受规则不胜贪心。'统计纪律'类把信息反馈/失败诊断与抗噪捆绑，实验无法判别这两个竞争解释，'补齐后递减'的预测也不在实验矩阵内。",
  "feasibility": "fail",
  "feasibility_reason": "2609.17817 报告 gpt-oss-120b、Qwen3.5-397B、DeepSeek V4 Pro 都无法驱动 Hyperagents（只产出空或坏 patch），拟用的 Qwen3-235B-A22B 更弱，本地主路线门槛大概率失败；原设置评估用 o4-mini，本地替换会改变任务；用 Sonnet 4.5 API 时 1000 元仅够约 1–2 次 50 迭代运行，6×3 矩阵超出自主预算。代码、日志和 diff 谱系可得。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "机制错配：DGM-H 的接受/父代选择与评估器在可编辑边界外，'重复评估后再接受'和人工抗噪接受规则无法作为 meta agent 编辑实现；若改 select_next_parent，则改的是生成算法 G，混淆了比较",
    "目标域增益从格式失败的 0 分地板起步（0 到 0.63），不是选择噪声主导的情形；所引 Winner's Curse 证据还显示接受规则不胜贪心，人工基线的预期缺乏依据甚至有反证",
    "判别力不足：'统计纪律'类把表现追踪/失败记忆（信息反馈与诊断）和抗噪捆绑在一起，剔除实验无法区分抗噪与更好的失败诊断这两个竞争解释",
    "可行性：已有报告表明比 Qwen3-235B 更强的开源模型都无法驱动 Hyperagents，API 预算只够约 1–2 次运行"
  ],
  "novelty_conclusion": "增量有限：Hyperagents D.5 已用 lineage diff 做过成分消融，E.3 定性列出了元能力；本方案是更细粒度的延伸，加上借用 Winner's Curse 的框架，去掉原论文名字后剩下的是一个与系统结构不符的机制假说。",
  "closest_neighbors": [
    "Hyperagents (arXiv 2603.19461)",
    "The Winner's Curse in LLM Self-Improvement Loops (arXiv 2610.09239)",
    "Auditing the Product, Not the Recursion (arXiv 2610.27610)",
    "Recursive self-improvement of AI research agents / AIDE² (arXiv 2609.26457)",
    "Reflections on Trusting Trust, Revisited (arXiv 2609.17817)"
  ]
}
```
