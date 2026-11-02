You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-11-01. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' into your own scratch directory instead. arXiv pages are reachable via WebFetch; .claude/skills/idea-improvement-loop/tools/paper_peek.py also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/false_accusation_nq004_20261101/round-03-review.md (UTF-8).
Your final message must contain only the review below.

Score the idea from 1 to 10. Judge whether the Claim is genuinely distinct, whether the method
is more than a relabeling or trivial combination, and whether the minimal experiment distinguishes
it from the closest work under the same core budget. Check whether the story line forms an
evidence-backed causal chain from a specific existing failure, through an overlooked key idea and
the proposal's concrete action, to a falsifiable expected result; unsupported claims that everyone
performs poorly or ignores the issue are claim blockers. Also verify that the positioning keywords
are established terms, that each experimental baseline belongs to the same domain and task, and
that every nontrivial baseline has a working public implementation and a concrete reproduction
route. Cross-domain inspiration is not an experimental baseline. Missing or mismatched baseline
evidence is a fatal feasibility blocker and cannot receive experiment_ready. When a supplied
paper is present, verify that the proposed novelty belongs to the new idea and still stands after
removing that paper's name. Treat a proposal that merely repairs, completes, or adds an experiment
to the supplied paper as a fatal novelty blocker.

Verdict meanings:
- experiment_ready: score > 8 and no fatal novelty, feasibility, or claim blocker
- promising_needs_revision: potentially salvageable, but the novelty boundary remains unresolved
- needs_rethink: the core claim is covered or the experiment cannot test it
- reject: not worth further work under the stated constraints

对外只输出下面三个 Markdown 部分，不要给重构方向、修改清单、实验 checklist 或长综述：
## 结论
<用当前日期给出 score、verdict、新颖性判断，以及是否值得继续。>

## Claim 判断
<用短表格逐条判断 Claim：新颖、部分重合或已被覆盖；每条只给最关键依据。>

## 最高近邻
<最多列 5 篇重叠最高的论文或系统；给出可核验链接、重叠点和仍有的差别。每篇 1-2 行；无法核验就写"需要检索"。>

末尾附上仅供主执行器解析的 JSON，不要增加其他章节：
   {
     "score": 0.0,
     "verdict": "promising_needs_revision",
     "fatal_blockers": [],
     "novelty_conclusion": "...",
     "closest_neighbors": ["paper title or needs_search"]
   }

Current four-part brief:

## 背景

**定位关键词：** sycophancy；rational updating；attention heads；activation steering；tool-using agents

**一句话定位：** 在 LLM 谄媚的机制研究中，"无依据的顺从"与"按证据的理性更新"能否被分开干预，两篇工作结论相左，而且两篇都只考察了证据和压力都从用户消息进入的情形。本研究检验：当证据由模型自己调用工具取回时，两者能否分开，以及这能否用来保护 agent 已完成的正确工作，同时不妨碍正当的修复。

## 核心 Claim

1. **现有工作与分歧**
   - **2608.26511（问答）**：抑制无依据顺从（UY）的训练期与推理期干预，普遍会损害理性更新（RU）。两者驱动的 MLP 神经元与注意力头大量重叠，转向方向正相关；正交化转向只带来有限、因模型而异的选择性。该文还发现，把同一段证据改写成用户自己的说法，四个模型的 RU 都会下降（如 60.7→53.9），这说明行为上存在来源敏感，但机制分析没有区分来源。
   - **2604.19117**：在 12 个 1.5B–72B 模型中，少数注意力头携带"该陈述是错的"信号；关闭它们会明显改变顺从行为，而事实准确率几乎不变。作者据此认为这组头控制顺从，而不是知识。
   - **agent 场景中有效证据常经工具返回。** 例如：agent 读到抱怨后会轻视自己先前的核查（Thinking-in-Bets，2610.34654）；agent 过度采信工具返回（2609.05587）。
2. **被忽视的关键**：2608.26511 观察到的组件重叠，可能不是因为两种行为本质上共用同一机制，而是因为证据和压力走的是同一条用户通道。本 Idea 主张：
   - **C1（通道调节重叠）**：用 2608.26511 的流水线识别组件，同一段证据文本分别放在用户消息里、或放在模型自己发起的工具调用的返回里。UY 组件与"工具通道 RU"组件的重叠，显著低于 UY 与"用户通道 RU"的重叠。
   - **C2（选择性干预）**：抑制 UY 组件（消融或沿其方向转向）可降低无依据顺从；工具通道的 RU 基本保留，用户通道的 RU 受损，即复现 2608.26511 的权衡。这种保留不是盲信工具：工具通道里的无效证据（与正确答案矛盾的返回）不会因此被更多采信。
   - **C3（agent 层可用）**：在"补丁辩护"任务上，"抑制 UY + 要求 agent 自己重跑测试，而不是读用户粘贴的日志"这一组合的两侧得分，高于 Thinking-in-Bets、坚持立场提示和 2608.26511 的正交化转向。两侧得分指：错误抱怨下保留正确补丁的比例，以及真实抱怨下修复的比例。

## 方法设计的核心思想

- **问答层**：在 2608.26511 的数据与四个模型上新增两个条件。
  - **RU-工具**：模型先被告知可调用 `lookup` 工具；工具返回与原 RU 条件完全相同的证据文本。
  - **无效-工具**：工具返回支持错误答案的文本，用来检验是否盲信工具。
  - 组件识别沿用原流水线：分别对 UY、RU-用户、RU-工具提取注意力头与 MLP 神经元集合、转向方向，并计算重叠与余弦。
- **agent 层：补丁辩护任务**
  - 从 SWE-bench Verified 选 FAIL_TO_PASS 测试可靠的实例，构造两类：
    - **错误抱怨**：已应用金标准补丁，用户称"这个补丁破坏了 X"；
    - **真实抱怨**：用删去金标准补丁中一个关键 hunk 的变体替代，FAIL_TO_PASS 测试确实失败，用户的抱怨相同。
  - 证据通道分两种：
    - **工具**：agent 可调用 `run_tests`，看到真实结果；
    - **用户**：用户在消息中粘贴测试输出，文本与工具返回相同。错误抱怨在这一通道下粘贴的是伪造的失败日志。
  - 正确行为：错误抱怨下保留补丁，真实抱怨下修复。修复是否正确由 SWE-bench 测试判定。
- **与最高近邻的差别**：
  - 2608.26511 与 2604.19117 只在用户通道上做机制分析；
  - Thinking-in-Bets 与 2610.36453 是行为层的免训练方法或测量，不涉及组件；
  - CAVE-Bench 只有错误指责。
  - 本 Idea 以证据通道为调节变量做机制分析与干预。

## 最小实验

- **模型**：沿用 2608.26511 的四个模型：Llama-3.1-8B-Instruct、Llama-3.2-3B-Instruct、Qwen3-8B、gemma-3-4b-it。
- **问答层数据**：2608.26511 发布的数据（TruthfulQA、PopQA、EX-FEVER 及其证据版本）与原划分。
- **agent 层数据**：200 个 SWE-bench Verified 实例 × {错误抱怨, 真实抱怨} × {工具, 用户} 通道 × 2 次重复。
- **对照**：同一模型、同一层位、同一解码设置。
  1. 无干预；
  2. 2608.26511 的正交化转向；
  3. UY 组件消融（按 2608.26511 的组件集合）；
  4. 2604.19117 式的顺从头消融（按其写入范数加修补步骤本地实现）；
  5. Thinking-in-Bets（读反馈前写主张清单）；
  6. 坚持立场提示；
  7. UY 抑制 + 要求自己重跑测试（本 Idea 的 agent 层组合）。
- **指标**：
  - 问答层：R_UY、R_RU-用户、R_RU-工具、无效-工具采信率；组件重叠（Jaccard）与方向余弦。
  - agent 层：错误抱怨下的补丁保留率；真实抱怨下的修复成功率；两者的几何平均。
- **支持与推翻**
  - **C1**：在至少 3/4 个模型上，UY 与 RU-工具的组件重叠显著低于 UY 与 RU-用户（对层与头做置换检验），则支持；否则推翻。
  - **C2**：抑制 UY 组件后，R_UY 显著下降，R_RU-工具下降小于 R_RU-用户下降的一半，且无效-工具采信率不上升，则支持。若 R_RU-工具与 R_RU-用户同样下降，或无效-工具采信率上升，则推翻。
  - **C3**：组合方法的 agent 层几何平均显著高于对照 2、5、6，则支持；否则推翻。
- **Baseline 来源与复现**
  - **2608.26511**
    - 论文：https://arxiv.org/abs/2608.26511
    - 代码：https://github.com/dependentsign/sycophancy-rational-updating （已克隆核验）
    - 用法：`sru run --model <hf_id 或 vLLM 端点>` 跑 UY/RU 评测；组件分析与正交化转向脚本在仓库中。
  - **2604.19117**
    - 论文：https://arxiv.org/abs/2604.19117
    - 未找到代码。论文 §3 给出按写入范数选头、激活修补验证的步骤，按步骤本地实现。
  - **Thinking-in-Bets**
    - 论文：https://arxiv.org/abs/2610.34654
    - 未找到代码。方法是免训练的提示协议，按论文描述实现。
  - **SWE-bench Verified**
    - 数据：HF `princeton-nlp/SWE-bench_Verified`
    - 测试运行：https://github.com/SWE-bench/SWE-bench
  - 以上都属于谄媚与理性更新问题，或其 agent 任务。
- **算力与 API**
  - **问答层**：4 个模型 × 3 个新条件，推理与组件归因约 40 A100 小时。
  - **agent 层**：4 个模型 × 7 种方法 × 800 个短回合（每回合几次工具调用），带 HF 钩子推理，每回合约 1 分钟，约 370 A100 小时；SWE-bench 测试容器运行另需 CPU。
  - **合计**：约 410 A100 小时，8×A100 上约 2–3 天，单次作业不超过 1 天。
  - **API**：不需要付费 API。

Frozen Problem Anchor and user constraints:

- **底线问题**：长期运行的 agent 在任务已正确完成后，收到无法本地核实的错误指责时接受指责并破坏正确工作；需弄清其机制，并找到既能保护正确工作、又不妨碍正当修复的干预。
- **目标设置**：工具调用 / 编码 agent，任务已到达经验证的正确状态后的续跑或交接；CAVE-Bench 类不透明任务；开源 ≤32B 模型为主，可含少量 API 模型。
- **必须解决的瓶颈**：agent 场景下接受率与压缩 / 交接方式的关系、"要求证据"这一正确行为能否训练或诱导出来尚未解决；现有缓解只在错误指责上评测。
- **约束**（用户 AGENTS.md，2026-11-01）：实验 8×A100 80G，每次运行最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API 1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会；各 baseline 核心参数一致；打磨完或放弃时在原问题卡上标记。
- **非目标**：不做安全攻防式的过度防御；不在本 skill 内启动实验。
- **成功条件**：机制清楚、与最高近邻可区分、能在上述资源下用可复现 baseline 证伪的 idea，通过两次独立 reviewer 评审（> 8、无致命阻塞）。
