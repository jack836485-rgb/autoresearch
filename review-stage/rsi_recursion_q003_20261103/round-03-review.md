## 结论

2026-11-03，总体 score 4.8，verdict：**needs_rethink**。主贡献是量化 Hyperagents 迁移实验中的"坏起点修复"混杂，并在正常起点上重测改进者优势。这个贡献不够。原因有三：
- 它只是对单篇论文单个实验的审计。核心结论大半已能从原文自身的数字和作者的自承中读出。
- 主判别式受 headroom 机械约束，实验结果近乎预先决定。
- "离线分解"在起点有效率为 0 时没有定义，必须先跑一次反事实评测才能计算。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 5.5 | Hyperagents 是高关注度工作，其 imp@50 迁移实验确实是"改进者更会改进"的主要正面证据，指出它被接口修复主导有价值。但影响限于一篇论文的一个域（IMO 批改）。brief 没有证明这一混杂在 STOP/DGM/SICA/HGM 等系统中普遍存在；例如 DGM 的 Polyglot 初始 agent 本身可用。原文对相关结论已有保留：Fig.4 中 200 轮后 transfer 0.640 对 from-initial 0.610 不显著，作者在 p.8 自承"part of the early improvement consists of learning the task interface"。因此能改变的领域判断有限。 |
| 新颖度 | 5.0 | 2610.27610 已给出一般原理：improver contrast 依赖起点状态，可随接近天花板而缩小（Prop.3、swap test）。它还点名批评了 Hyperagents 迁移不是严格同起点。HDA（2610.22466）已对演化增益做来源归因。原作者也自承接口学习。本方案的新增，是把"起点有效性"具体化为一个可测混杂，并在同一实验上做正常起点版本的 swap test，属于可辨认但有限的增量。去掉 Hyperagents 的名字后，剩下的大体是"补全该论文缺的一个对照"。 |
| 有效性 | 6.0 | 支持"接口修复占大头"的现有依据强，且已经过核验：<br>(1) 公开 `task_agent.py` 只把整个 inputs 字典塞给 FM，要求返回 `{"response": ...}`；`domains/report.py` 用小写字符串去匹配 incorrect/partial/almost/correct，所以初始 0 分很可能来自标签词表不匹配。<br>(2) 单次调用、格式正确的静态 ProofAutoGrader 在同一测试集上得 0.670，高于迁移的 0.630。<br>(3) D.5 中 meta-only 迁移（0.55–0.66）在 5 次运行间稳定，而初始 meta agent 有 4/5 次为 0。这与"迁移 meta agent 携带了会读评测输出、修格式的能力"相符。<br>据此，现象本身大概率成立。但 brief 的新测量环节判别力不足，理由如下：<br>a) 正常起点（o4-mini 加最小解析）的分数大致落在 0.5–0.6，而该测试集上已观察到的上限约 0.70–0.71，可用 headroom 只有约 0.1–0.2。于是"差距 ≤ 0.63 的一半"几乎必然成立，"差距基本保持"在物理上不可能出现，主假说无法被推翻。<br>b) 测试集只有 100 题，单次准确率 SE 约 0.05；imp@k 又是 50 个候选按验证集选最优，噪声更大。3 个种子分辨不了量级为 0.05 的改进者差。<br>c) brief 称"0.63 约为 30σ"，但原文 CI 是 0.54–0.63，这个说法没有依据。<br>仍然未知的是：迁移 meta agent 的诊断类元能力，在去 headroom 归一化后是否仍有优势。 |

**与原问题的关系：** 本方案回答的是原问题中一个具体的证据有效性子问题，即现有最强的递归证据是否被坏起点混杂。原问题的"累积、平台还是侵蚀"完全未答，brief 也明说了这一点，这本身不构成阻断。

**实验能否判别：** 不能按现设计判别。
- 判别阈值用的是 imp@k 的绝对差，坏起点的可用 headroom 是 0.63 以上，正常起点只有约 0.15，两者不可比。需要的是同一 headroom 下的估计量，或保留大 headroom 的有效起点（例如有效率 100% 但条件质量低的弱 agent），brief 两者都没有。
- 离线分解在初始 agent 有效率 v₀=0 时，条件质量 q₀ 没有定义。份额必须依赖"加解析的初始 agent"这次反事实评测，所以"离线、无需 FM"的说法不成立。一旦有了 q_parsed，接口份额约等于 q_parsed/0.63，即一个数字，分量很小。
- 换用 GPT-5-mini 驱动用 Sonnet 4.5 演化出的 meta agent，本身就改变了改进者。2609.17817 报告多个强开源模型都驱动不了 Hyperagents。若门槛检验失败，回退方案只剩离线分解加 1 次 Sonnet 锚点运行，正常起点上的主 Claim 就测不到了。

**可行性：pass（勉强）。**
- 代码已核验公开。每代评测写出 `predictions.csv` 与 `report.json`（见 `domains/harness.py`、`utils/gl_utils.py`），逐题有效性标签可以直接定义为"prediction ∈ 四个标签"，不需要人工标注。
- 日志在 Google Drive，内容和覆盖面未能核验，需要经服务器下载后确认包含 gen 级 predictions 和迁移 agent 的 diff 链。
- 预算被低估：brief 把 22M token 全按 GPT-5-mini 计价，但为与原文可比，评测 FM 应保持 o4-mini（每次运行约 5.5M token，以输出为主），12 次运行很可能超过 1000 元。降到 2 个种子，或依靠 staged eval 少评，可以压回预算内，但会进一步削弱上面 b) 所说的统计判别力。

## 最高近邻

1. **Hyperagents**（https://arxiv.org/abs/2603.19461）。被审对象。v2 p.8 已自承接口学习；D.5 做了 meta/task 成分消融；Fig.4 给出 200 轮 transfer 对 initial 不显著；ProofAutoGrader 0.670 是静态参照。原文缺的是有效起点上的 imp@k 对照和有效率分解。
2. **Auditing the Product, Not the Recursion**（https://arxiv.org/abs/2610.27610）。提出 swap test 和 improver contrast 依赖状态的观点（含天花板收缩），并点名 Hyperagents 迁移不是严格同起点。它没有把"起点有效性/接口失败"单列为混杂，也没做实验。
3. **Harness-Delta Attribution**（https://arxiv.org/abs/2610.22466）。把 harness 演化增益分解为过拟合、测试时扩展和残差。方法论上同属增益归因，但对象是 task harness，不是改进者，也不分"有效率与条件质量"。
4. **Reflections on Trusting Trust, Revisited**（https://arxiv.org/abs/2609.17817）。用 Sonnet 4.5 复跑了 Hyperagents，报告多个强开源模型驱动失败，并发现 Polyglot 的答案泄漏（IMO 批改不受影响）。它直接约束本方案能否换用低价 FM。
5. **Rethinking the Evaluation of Harness Evolution for Agents**（https://arxiv.org/abs/2607.12227）。在匹配预算下，harness 演化常常不优于简单的测试时扩展，且 v2 强调需要有 headroom 的设置。这也是本方案应考虑的强解释：在正常起点上，改进者优势可能只是额外搜索带来的。

```json
{
  "score": 4.8,
  "contribution_scores": {"importance": 5.5, "novelty": 5.0, "effectiveness": 6.0},
  "contribution_assessment": "主贡献是量化 Hyperagents IMO 批改迁移实验中坏起点（标签词表或格式不合规）修复对 imp@50 的贡献，并在有效起点上重测迁移与初始 meta agent 之差。现象大概率成立：初始 task_agent.py 只返回原样 response，report.py 做小写字符串匹配；静态 ProofAutoGrader 0.670 高于迁移的 0.630；meta-only 迁移稳定而初始 meta agent 有 4/5 次为 0；作者 p.8 自承接口学习。但这一结论大半可从原文数字直接读出，且只覆盖一篇论文的一个域。2610.27610 已提出起点依赖与天花板收缩的一般原理并批评了该迁移实验，因此新意有限。主判别式用绝对 imp@k 差对比 headroom 约 0.63 与约 0.15 的两种起点，主假说几乎必然成立、无法推翻；测试集 n=100、3 个种子分辨不了约 0.05 的改进者差；离线分解在 v0=0 时 q0 无定义，必须先做反事实评测，算出的结果近似单一数字。",
  "feasibility": "pass",
  "feasibility_reason": "代码公开，每代评测有 predictions.csv，逐题有效性可按 prediction 是否属于四个标签直接判定、无需人工标注。日志在 Google Drive，需经服务器下载并核验是否含 gen 级 predictions 与迁移 agent 的 diff 链。GPT-5-mini 驱动用 Sonnet 4.5 演化出的 meta agent 能否复现正差距未知，门槛失败时正常起点上的主 Claim 不可测。预算低估了 o4-mini 评测成本（约 5.5M token/次），12 次运行可能超过 1000 元，降种子数可执行，但会削弱统计判别。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献不足：单篇论文单实验的混杂审计，核心结论（接口修复占大头）已能由原文 ProofAutoGrader 0.670 > 迁移 0.630、作者 p.8 自承接口学习、Fig.4 长程不显著直接推得；2610.27610 已提出状态依赖与天花板收缩原理并批评该迁移实验；三项分数中没有一项 >= 8。",
    "Claim 判别阻断：判别阈值是正常起点 imp@k 差 <= 坏起点差 0.63 的一半，但正常起点的 headroom 只有约 0.1-0.2（已观察上限约 0.70），主假说被 headroom 机械保证成立，'差距基本保持'不可能出现；缺少 headroom 归一化估计量或高 headroom 的有效起点。",
    "统计判别不足：测试集 100 题（SE 约 0.05），imp@k 取 50 个候选的验证集最优，3 个种子分辨不了约 0.05 的改进者差；'0.63 约 30σ'与原文 CI 0.54-0.63 不符。",
    "离线分解定义缺口：初始 agent 有效率为 0 时条件质量无定义，份额依赖加解析初始 agent 的反事实评测（需调用 FM），算出的结果近似 q_parsed/0.63 这一个数字。"
  ],
  "novelty_conclusion": "相较 Hyperagents 原文的自承、2610.27610 的 swap test 与状态依赖分析、2610.22466 的增益归因，本方案的新增仅限于把'起点有效性'具体化并补做一个正常起点对照，是有限增量；去掉 Hyperagents 的名字后，基本只剩补全该论文缺的一个对照。",
  "closest_neighbors": [
    "Hyperagents (arXiv 2603.19461)",
    "Auditing the Product, Not the Recursion: The Evaluation Evidence Behind Recursive Self-Improvement Claims (arXiv 2610.27610)",
    "Harness-Delta Attribution: Dissecting Gains From Harness Evolution (arXiv 2610.22466)",
    "Reflections on Trusting Trust, Revisited: Contaminating Self-Modifying AI Coding Agents with Poisoned Benchmarks (arXiv 2609.17817)",
    "Rethinking the Evaluation of Harness Evolution for Agents (arXiv 2607.12227)"
  ]
}
```
