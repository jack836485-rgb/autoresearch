You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' instead. arXiv abstract/HTML pages are reachable via WebFetch; the bundled tools/paper_peek.py in .claude/skills/idea-improvement-loop/tools also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/reward_hack_monitor_aq004_20261029/round-01-review.md (UTF-8).
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

**定位关键词：** reward hacking；training-time reward hacking；prompt-elicited trajectories；CoT monitoring；RLVR

**一句话定位：** 代码 RLVR 中，用"提示诱导的投机轨迹"训练的奖励投机监控器，对 RL 训练中自然出现的投机泛化差，这一差距从何而来、如何低成本补上。

## 核心 Claim

1. **现有失败。** Trace-and-Amplify（arXiv 2604.23488）发现，用提示诱导轨迹训练的监控器对训练期自然投机泛化差；但其诱导数据来自固定来源，并未随训练更新。另一方面，多项独立工作显示投机受能力门控：捷径只对已学会的工具形成（2609.16268）；早期改写评测器的尝试因自己的解答过不了而失败、之后以质不同的策略成功（2604.01476）；工业实践中模型变强后才出现新渠道，只能每轮人工补监控规则（2606.26300）。
2. **被忽视的关键。** 诱导数据里的投机分布受诱导者能力的限制：固定诱导者（通常是初始模型）被提示时也产不出训练后期才变得可行的策略。因此本 Idea 主张——
   - **C1**：训练开始时用初始模型诱导样本训练、之后冻结的监控器，召回随 RL 步数下降，且下降集中在初始模型被提示时产不出的投机策略上，不能仅由思考长度缩短解释。
   - **C2**：保持诱导提示、样本数、刷新时点与监控器结构不变，只把诱导者换成当前检查点，可收回冻结监控器与"用真实训练期投机样本训练的监控器"（上界）之间的大部分差距，且明显优于"用初始模型按同样时点重新诱导"。
   - **C3**：用同家族更大的非 RL 模型作诱导者，可以区分差距来自"能力"还是"RL 带来的在策风格"：若大模型诱导接近当前检查点诱导，支持能力解释；若接近初始模型诱导，支持在策风格解释。

## 方法设计的核心思想

- **输入**：RL 训练中的若干检查点；一组固定的投机诱导提示（沿用 Trace-and-Amplify 附录 A.2.1 的提示）；测试床自带的投机追踪器（Trace-and-Amplify 的伪单元测试 / Countdown-Code 的真-代理奖励分离），只用于确认诱导样本确实投机。
- **动作**：每隔固定步数，对当前检查点运行诱导提示，保留经追踪器确认的投机样本与同题非投机样本，重训轻量监控器（文本分类器与隐状态探针，沿用该仓库实现）。不需要对训练期自然轨迹做任何人工或真值标注。
- **输出**：随训练刷新的监控器，以及按投机策略分层的召回诊断。
- **与最高近邻的关键差别**：Trace-and-Amplify 比较的是"诱导数据 vs 训练期数据"两种来源，并把差距归于提示诱导本身；本 Idea 把诱导者能力作为自变量，主张差距主要来自诱导者与被监控策略的能力不匹配，并给出不依赖训练期真值标注的能力匹配刷新。

## 最小实验

- **测试床与模型**：
  - Trace-and-Amplify（同一仓库，GRPO，LeetCode/TACO 注入伪测试）：Qwen2.5-Coder-1.5B-Instruct、DeepSeek-Coder-1.3B-Instruct，约 300 步，与原文一致。
  - Countdown-Code（真奖励=算术正确，代理奖励=测试脚本通过，可改写测试）：Qwen2.5-3B-Instruct；原文报告它在 RL 中无需污染 SFT 即自然学会投机。
  - 每个配置 3 个种子，共 9 条 RL 轨迹；在步 0 与之后 5 个等距检查点处取样。
- **对照（同一监控器结构、同一诱导提示、每次 800 条诱导样本、同一刷新时点）**：
  1. 冻结：只用步 0 初始模型的诱导样本训练一次（即 Trace-and-Amplify 的 prompt-elicited 监控器）；
  2. 初始模型刷新：每个刷新点用初始模型重新诱导（控制"刷新次数/样本量"）；
  3. 大模型刷新：用 Qwen2.5-Coder-7B-Instruct / DeepSeek-Coder-6.7B-Instruct / Qwen2.5-7B-Instruct（各自同家族、未经本次 RL）诱导；
  4. 当前检查点刷新（本 Idea）；
  5. 上界：用追踪器标注的真实训练期投机样本训练（Trace-and-Amplify 的 training-time 监控器，不可部署，只作参照）；
  6. 参照：零样本 LLM 监控器（该仓库 `gpt_evaluate.py` 的提示），不刷新。
- **指标**：每个检查点窗口内，对追踪器标注的自然投机计算 TPR@5%FPR 与 AUROC；对每条自然投机用固定类别表（硬编码输出、按测试输入特判、改写断言/测试脚本等）标注策略，"新策略"= 步 0 诱导集中未出现的类别；思考 token 数作协变量。
- **支持 Claim**：(C1) 冻结监控器召回随步数下降，且下降主要来自新策略，控制思考长度后仍显著；(C2) 当前检查点刷新的召回显著高于初始模型刷新，并收回到上界差距的大部分；(C3) 大模型刷新的位置给出能力 vs 在策风格的判别。**推翻 Claim**：冻结监控器召回不随步数下降；或当前检查点刷新与初始模型刷新在种子间无显著差异；或衰减可由思考长度完全解释。
- **Baseline 来源与复现**：
  - Trace-and-Amplify 测试床、prompt-elicited 与 training-time 监控器：论文 https://arxiv.org/abs/2604.23488 ；代码 https://github.com/LichenLillc/CoTMonitoring （已克隆核验：`Trace-and-Amplify_Framework/train_script.sh` 训练投机模型，`my_utils/add_fake_test_final-ver.py` 注入伪测试，`or1_scripts/eval/eval_1p5b.sh` 采样轨迹；`CoTMonitors_Training_and_Evaluation/scripts/paired_probe_pipeline/BERT_pipeline.sh` 与 `mine_probe_pipeline_loop_paired.sh` 训练文本分类器与探针，`scripts/gpt_evaluate.py` 为 LLM 监控器）。与本任务同为代码 RLVR 训练期投机监控。
  - Countdown-Code：论文 https://arxiv.org/abs/2603.07084 ；代码 https://github.com/zohaib-khan5040/Countdown-Code （已克隆核验：`datagen/create_datasets.py` 生成 RLVR 数据，`environments/countdown_code` 环境，`verl/` 训练）。与本任务同为代码 RLVR 中改写测试的奖励投机。
  - "初始模型刷新""大模型刷新"只改诱导者，复用上述脚本，无需额外仓库。
- **算力与 API 估算**：
  - Trace-and-Amplify：原文在 4×A6000 上训练约 300 步；按每次 4×A100 约 1 天粗估（试跑后核实），6 次 ≈ 600 A100 小时。
  - Countdown-Code：原文在 2×A40 上单个实验不超过 60 小时；按 A100 折半粗估每次 ≤60 A100 小时，3 次 ≤180 A100 小时。
  - 诱导与监控器：9 条轨迹 × 6 个时点 × 4 种诱导来源 × 800 条，1.3–7B 推理，约数十 A100 小时；文本分类器与探针训练为分钟级。
  - 合计约 800–900 A100 小时，在 8×A100 上约 5 天。LLM 监控器参照：9 × 6 × 约 1,000 条 × 约 1.5k token ≈ 8×10⁷ 输入 token，按小型 API 模型每百万 token 约 0.15 美元计约 12 美元，在 1000 元预算内；也可用本地 Qwen3-8B 代替。

Frozen Problem Anchor and user constraints:

- **底线问题**：agentic RL 训练中，奖励投机 / 工具捷径为何在相关能力学会之后才出现；训练开始时构造并冻结的投机监控器，其召回是否随策略能力提升而衰减。
- **目标设置**：LLM agentic RL（工具调用、编码或 rubric/LLM-judge 奖励），可控测试床提供投机真值；≤9B 开源策略模型。
- **必须解决的瓶颈**：训练过程中固定监控器对新出现投机的召回衰减从未被测量；现有做法依赖人工闭环更新或只在评估阶段测量。
- **约束**（来自用户 AGENTS.md）：实验 8×A100 80G，预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API（如 GPT judge）1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会。实验需控制变量，各 baseline 核心参数一致。
- **非目标**：不做安全攻防论文式的过度防御；不在本 skill 内启动实验。
- **成功条件**：得到一个机制清楚、与最高近邻可区分、能在上述算力下用可复现 baseline 证伪的 idea，并通过两次独立 reviewer 评审（分数 > 8、无致命阻塞）。
