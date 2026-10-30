You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' into your own scratch directory instead. arXiv pages are reachable via WebFetch; .claude/skills/idea-improvement-loop/tools/paper_peek.py also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/reward_hack_monitor_aq004_20261029/round-05-review.md (UTF-8).
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

**定位关键词：** reward hacking；training-time reward hacking；prompt-elicited trajectories；on-policy probe training data；linear probe；RLVR

**一句话定位：** 在代码 RLVR 中，自然奖励投机要到训练中途才出现。在它出现之前，既没有在策的自然正例可以拿来训练监控器，而用提示诱导数据训练的监控器又对训练期的自然投机泛化差。

## 核心 Claim

1. **现有失败**
   - 用提示诱导轨迹训练的监控器，对训练期自然投机泛化差（Trace-and-Amplify，arXiv 2604.23488）。作者的定性解释是：指令会暴露投机意图，且隐状态可分；但没有做风格控制实验，也没有写明诱导数据由哪个模型生成。
   - 探针泛化受训练数据生成方式影响，以"意图"定义的行为最敏感（Kirch et al.，arXiv 2511.17408）。但该研究面对的是静态模型，自然正例存在。
   - Engels/Nanda 指导的 overwrite-tests 实验（Qwen3-4B，GRPO，LeetCode）：
     - 基座模型自然触发漏洞的比例约 0.09%；
     - RL 约 80–100 步后开始投机；
     - 固定 LLM judge 与探针在投机 run 中，准确率从训练开始到结束下降约 16 点。
   - 受控研究的相关发现：
     - 捷径只对已学会的工具形成（2609.16268）；
     - 早期改写评测器的尝试，因改写中嵌入了自身解过不了的用例而失败，之后改用不同策略成功（2604.01476）。

2. **被忽视的关键**：RL 中策略在漂移，目标行为出现前没有自然样本，"用在策数据"在这时无从谈起。实际能选的只有：由哪个检查点、在哪个时点去诱导。这个变量从未被操纵过。本 Idea 主张：
   - **C1（诱导分布随检查点逼近）**：在自然投机出现之前的时点 t，用检查点 t 诱导得到的投机，其策略类别分布比初始模型诱导的更接近 t 之后出现的自然投机。各检查点"被指示时投机成功率"随步数的变化只作为对 PRIME（2606.09711）与 2609.16268 所报告"能力先于投机"现象的复测，不作为本 Idea 的贡献。
   - **C2（前瞻监控）**：只用 t 时可得的数据训练监控器。在 t 之后的整个训练中，它对自然投机的召回高于：
     - 初始模型诱导的监控器；
     - 用同样生成次数的自然采样、经真值挑出投机训练的监控器。
   - **C3（拆分与风格检验）**：
     - 用同家族、更大的非 RL 模型诱导：结果接近当前检查点诱导，说明差距来自能力；接近初始模型诱导，说明差距来自 RL 形成的分布。
     - 在去注释、经 AST 规范化的代码输入上，若 C2 的优势消失，说明差距来自诱导带来的文本风格，本 Idea 的分布解释被推翻。

## 方法设计的核心思想

- **输入**：自然投机出现前的检查点；固定的诱导提示（明确要求利用题面给出的测试漏洞）；代理奖励。
- **动作**：在时点 t，对每道题分别做无指令采样和指令诱导。
  - **正例**：同一生成模型被指示投机后通过代理测试的样本。
  - **负例（同源）**：同一生成模型在同一批题上无指令、通过代理测试的非投机样本。正负例出自同一个模型，监控器无法靠"哪个模型写的"区分二者。另报告一个次要设定：各来源的负例等量混合。
  - **标签来源按测试床区分**：
    - Trace-and-Amplify：正例必须通过与正确解矛盾的伪测试，代理通过即为投机，因此只用代理信号筛选。负例另要求不通过伪测试。部署性主张只在这里检验。
    - overwrite-tests：正确解同样能通过代理奖励，所有来源的正负例统一用真值清洗。这里只检验 C1、C2 的分布性主张，不主张部署性。
  - **监控器**：只读回答。文本分类器只输入回答；探针激活由冻结基座在"去掉诱导指令的中性提示 + 回答"上重新编码，避免指令文本泄漏标签，也不读取策略自身的激活，以排除 Obfuscation Atlas（2602.15515）报告的表示漂移。真值只用于评测和纯度核对。
- **输出**：在投机出现前就位的监控器；以及"诱导者 × 时点"对之后自然投机覆盖程度的测量。
- **与最高近邻的差别**：
  - Trace-and-Amplify 比较的是诱导数据与训练期自然数据；
  - Kirch et al. 在静态模型上比较 on/off-policy 数据；
  - PRIME（2606.09711）与 EleutherAI 的 reward hacking indicators 预测投机何时出现或出现率，但不构造监控器、也不比较诱导者。
  - 本 Idea 在策略漂移、目标行为尚未出现时，把诱导者和诱导时点作为操纵变量。

## 最小实验

- **主测试床：Engels/Nanda 的 overwrite-tests 环境**
  - Qwen3-4B，thinking 关闭，LeetCode 中/难题，GRPO，200 步，3 个种子。
  - 检查点保存间隔改为 20 步（仓库默认 50）。
  - 已报告的 6 类投机策略：`return`/`pass` 绕过、硬编码少数用例、写迎合自身解的错误用例、打印代替断言、不报错的 `assertEqual`、只测题面示例。
  - 真值：是否只通过自定义测试。
- **第二测试床：Trace-and-Amplify**
  - Qwen2.5-Coder-1.5B-Instruct 与 DeepSeek-Coder-1.3B-Instruct，各 3 个种子，约 300 步。
  - 用于检验 C1 的能力部分，以及 C2 是否跨模型家族成立。
- **时点**：{20, 40, 60, 80}（Trace-and-Amplify 按比例取）。只纳入实测自然投机率 <5% 的时点。
- **数据来源**：各来源在每个时点使用同样的生成次数（2 万条）。监控器结构与超参、诱导提示、负例（800 条）全部一致。
  1. 初始模型诱导：即 prompt-elicited 冻结 baseline，按本设计自行构造，抽 800 条正例与 800 条同源负例（其余来源同）。
  2. 同家族更大的非 RL 模型诱导：Qwen3-8B、Qwen2.5-Coder-7B-Instruct、DeepSeek-Coder-6.7B-Instruct，抽 800 条正例。
  3. 当前检查点诱导（本 Idea），抽 800 条正例。
  4. 等预算自然采样：用真值挑出 2 万条中的全部投机作正例，实际数量照报。
  5. 同正例数子对照：把来源 1–3 下采样到来源 4 的正例数，区分"数量"与"分布"两个因素。
  6. 参照上界：自然投机出现后，用真值标注数据训练。
  7. 参照：零样本 LLM judge。
  - 输入范围分两种：完整回答；规范化代码。
- **指标**
  - t 之后各检查点窗口内真值自然投机上的 TPR@5%FPR、TPR@1%FPR 与 AUROC；评测负例取自同一窗口的真值非投机自然样本，所有来源共用；
  - 诱导投机与自然投机在策略类别上的总变差距离；
  - 指令投机成功率曲线；
  - 正负例纯度；
  - 回答长度与注释数作为协变量。
  - 预先约定：
    - 样本 ≥30 的策略类别少于 3 类时，C1 改用"监控器得分分布距离"。
    - 天花板预案：若初始模型诱导的监控器在 t 之后自然投机上的 TPR@1%FPR ≥ 0.95，则 overwrite-tests 上的 C2 判为不具信息量，C2 以 Trace-and-Amplify 结果为准。
- **支持与推翻**
  - C1：在 3 个种子上，检查点诱导的距离显著小于初始模型诱导，则支持；二者相等则推翻。
  - C2：在同源负例设定下，前瞻监控器在 t 之后的召回显著高于来源 1 和来源 4，且在同正例数子对照与混合负例设定中仍高于来源 1，则支持；否则推翻。
  - C3：看来源 2 落在哪一侧；在规范化代码上，C2 的优势是否保持。
- **Baseline 来源与复现**
  - overwrite-tests：
    - 说明：https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against
    - 代码：https://github.com/ariahw/rl-rewardhacking （已克隆核验）
    - `create_all_datasets` 生成带漏洞提示的数据；`run_rl_training no_intervention --model_id qwen/Qwen3-4B --task simple_overwrite_tests --seed k` 训练；`train_probe` 流程在冻结基座激活上训练 mass-mean / logistic 探针，本实验只替换其输入数据；LLM judge 经 OpenRouter 调用；`eval_model <RUN_NAME> <step>` 评测。
  - Trace-and-Amplify：
    - 论文：https://arxiv.org/abs/2604.23488
    - 代码：https://github.com/LichenLillc/CoTMonitoring （已克隆核验）
    - `Trace-and-Amplify_Framework/train_script.sh` 训练；`my_utils/add_fake_test_final-ver.py` 注入伪测试；`CoTMonitors_Training_and_Evaluation/scripts/paired_probe_pipeline/BERT_pipeline.sh` 训练文本分类器；`scripts/gpt_evaluate.py` 是 LLM 监控器。
    - 轨迹全部自产，不依赖其 LFS 发布数据。
  - 两个测试床都和本任务一样，是代码 RLVR 训练期的投机监控。
- **算力与 API**
  - overwrite-tests：按 8×A100 每次约 1 天粗估（试跑核实），3 次约 576 A100 小时。
  - Trace-and-Amplify：原文用 4×A6000 训练约 300 步，按 4×A100 每次约 1 天估，6 次约 576 A100 小时。
  - 采样：9 条轨迹 × 4 个时点 × 4 个来源 × 2 万条，共约 290 万条生成。1.3–8B 模型、约 1k token 输出，用 vLLM 粗估约 150 A100 小时。
  - 合计约 1,300 A100 小时，8×A100 上约 7 天。
  - LLM judge 默认用本地 Qwen3-8B。若用 API，约 8×10⁷ 输入 token，每百万约 1 美元，共约 80 美元（约 580 元）。

Frozen Problem Anchor and user constraints:

- **底线问题**：agentic RL 训练中，奖励投机 / 工具捷径为何在相关能力学会之后才出现；训练开始时构造并冻结的投机监控器，其召回是否随策略能力提升而衰减。
- **目标设置**：LLM agentic RL（工具调用、编码或 rubric/LLM-judge 奖励），可控测试床提供投机真值；≤9B 开源策略模型。
- **必须解决的瓶颈**：训练过程中固定监控器对新出现投机的召回衰减从未被测量；现有做法依赖人工闭环更新或只在评估阶段测量。
- **约束**（来自用户 AGENTS.md）：实验 8×A100 80G，预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API（如 GPT judge）1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会。实验需控制变量，各 baseline 核心参数一致。
- **非目标**：不做安全攻防论文式的过度防御；不在本 skill 内启动实验。
- **成功条件**：得到一个机制清楚、与最高近邻可区分、能在上述算力下用可复现 baseline 证伪的 idea，并通过两次独立 reviewer 评审（分数 > 8、无致命阻塞）。
