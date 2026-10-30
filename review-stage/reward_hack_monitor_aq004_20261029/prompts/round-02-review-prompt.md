You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' into your own scratch directory instead. arXiv pages are reachable via WebFetch; .claude/skills/idea-improvement-loop/tools/paper_peek.py also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/reward_hack_monitor_aq004_20261029/round-02-review.md (UTF-8).
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

**定位关键词：** reward hacking；training-time reward hacking；prompt-elicited trajectories；linear probe；LLM judge；RLVR

**一句话定位：** 代码 RLVR 中，用提示诱导的投机轨迹训练的奖励投机监控器，对训练期自然投机泛化差，固定监控器的准确率也会随训练下降；这一差距由什么造成、能否不用真值标注补上。

## 核心 Claim

1. **现有失败与已有解释。**
   - Trace-and-Amplify（arXiv 2604.23488）发现，用提示诱导轨迹训练的监控器对训练期自然投机泛化差。原文把原因归于指令诱导会暴露投机意图、训练期投机更隐式，即"风格"解释，但没有做操纵检验；原文也没有写明诱导样本由哪个模型生成。
   - Engels/Nanda 指导的 overwrite-tests 实验（Qwen3-4B，GRPO，LeetCode）中，固定 LLM judge 与固定探针在投机 run 中，从训练开始到结束准确率下降约 16 点。作者只给出"回答变长、注释变多"的提示性解释，并把自适应监控列为未来工作。
   - 同一代码库说明，基座模型自然触发该漏洞的频率低于千分之一。
2. **被忽视的关键。** 诱导数据覆盖哪些投机，取决于诱导者是谁。诱导者从未被单独操纵，因此"风格"与"诱导者分布不匹配"两种解释从未被分开。本 Idea 主张：
   - **C1（分离）**：把诱导者换成当前检查点（同一诱导提示、同样本数），监控器在训练期自然投机上的召回提升；在只看去注释、规范化代码的监控范围内，这一提升仍然存在。若提升只在完整回答范围出现、在代码范围消失，则风格解释成立，本 Claim 被推翻。
   - **C2（来源）**：同家族更大的非 RL 模型作诱导者时，若接近当前检查点诱导的效果，差距主要来自能力；若接近初始模型诱导的效果，差距主要来自 RL 形成的在策分布。
   - **C3（修法）**：定期从当前检查点做指令诱导，只用部署时可得的信号筛选样本（被指示投机且代理奖励通过），以此刷新读取方固定的监控器。这样可收回冻结监控器与"用真值标注的自然投机训练的监控器"之间的大部分差距，且优于按同样时点用初始模型重新诱导；优势集中在初始模型诱导集中没有的投机策略上。

## 方法设计的核心思想

- **输入**：RL 训练中的检查点；固定的投机诱导提示；代理奖励（测试是否通过，训练时本来就有）。
- **动作**：
  - 每隔固定步数，用当前检查点对一批训练题做指令诱导；
  - 只保留代理奖励通过的样本作正例，同题、无诱导指令、代理奖励通过的样本作负例；
  - 重训读取方固定的监控器：基于冻结基座激活的线性探针，以及文本分类器。不读取策略自身激活，以排除 Obfuscation Atlas（2602.15515）报告的表示漂移这一机制。
- **不使用的信息**：自然轨迹的真值（是否只通过自定义测试）只用于评测与上界，不参与刷新。
- **与最高近邻的差别**：Trace-and-Amplify 比较两种数据来源（诱导 vs 训练期真值标注），并把差距归于风格。本 Idea 把诱导者作为操纵变量，用"诱导者 × 监控输入范围"的因子设计检验风格解释。修法也不需要训练期真值。

## 最小实验

- **主测试床**：Engels/Nanda 的 overwrite-tests 环境。
  - 设置：Qwen3-4B，thinking 关闭，LeetCode 中/难题，GRPO，200 步，3 个种子。
  - 已报告现象：80–100 步开始投机，评测集投机率约 79%。
  - 已报告 6 类策略：`return`/`pass` 绕过、硬编码少数用例、写迎合自身解的错误用例、打印代替断言、不报错的 `assertEqual`、只测题面示例。
  - 真值：是否只通过自定义测试。
  - 取样：步 0 与之后 5 个等距检查点。
- **第二测试床**：Trace-and-Amplify。Qwen2.5-Coder-1.5B 与 DeepSeek-Coder-1.3B，各 3 种子，约 300 步。只检验 C1 与 C3 是否跨模型家族成立，不做策略分层。
- **因子与对照**：所有监控器结构、超参、诱导提示、每次 800 条样本、刷新时点保持一致。
  - **诱导者（3 种）**：初始模型；同家族更大的非 RL 模型（Qwen3-8B / Qwen2.5-Coder-7B / DeepSeek-Coder-6.7B）；当前检查点。
  - **监控输入范围（2 种）**：完整回答；去注释与 docstring、经 AST 规范化的代码。
  - **诱导方式（诊断格）**：对初始模型与大模型，另做无指令大批量采样并用真值挑出投机。用来检查指令本身的影响，不属于修法。
  - **冻结**：只在步 0 用初始模型诱导训练一次，即 prompt-elicited baseline。
  - **上界**：每个窗口用真值标注的自然投机训练。
  - **参照**：该仓库零样本 LLM judge，不刷新。
- **指标**：
  - 每个检查点窗口内，在真值投机上的 TPR@5%FPR 与 AUROC；
  - 修法样本的标签纯度（用真值事后核对）；
  - 按 6 类策略分层的召回，"新策略"指步 0 初始模型诱导集中没有出现的类别；
  - 回答长度与注释数作协变量。
  - 预先约定：样本数 ≥30 的策略少于 3 类时，C3 的分层部分只报告不分层结果。
- **支持 / 推翻**：
  - C1：在代码范围内，当前检查点诱导显著优于初始模型诱导（3 种子，配对检验）。若差异只在完整回答范围出现，C1 被推翻。
  - C2：看大模型诱导落在哪一侧。
  - C3：收回差距的比例，以及控制长度后的分层优势。若刷新优势完全由长度解释，或纯度过低导致无优势，C3 被推翻。
- **Baseline 来源与复现**：
  - **overwrite-tests 环境**：说明 https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against 。代码 https://github.com/ariahw/rl-rewardhacking 已克隆核验：
    - `create_all_datasets` 生成带漏洞提示的数据；
    - `run_rl_training no_intervention --model_id qwen/Qwen3-4B --task simple_overwrite_tests --seed k` 训练；
    - `train_probe <RUN_NAME>` 在冻结基座激活上训练 mass-mean / logistic 探针；
    - LLM judge 经 OpenRouter；
    - `eval_model <RUN_NAME> <step>` 评测。
    - 与本任务同为代码 RLVR 训练期投机监控。
  - **Trace-and-Amplify**：论文 https://arxiv.org/abs/2604.23488 。代码 https://github.com/LichenLillc/CoTMonitoring 已克隆核验：
    - `Trace-and-Amplify_Framework/train_script.sh` 训练；
    - `my_utils/add_fake_test_final-ver.py` 注入伪测试；
    - `CoTMonitors_Training_and_Evaluation/scripts/paired_probe_pipeline/BERT_pipeline.sh` 训练文本分类器；
    - `scripts/gpt_evaluate.py` 为 LLM 监控器。
  - 诱导者替换与代码规范化只改输入数据，复用上述脚本。
- **算力与 API 估算**：
  - **overwrite-tests**：仓库未给训练时长。按 Qwen3-4B、200 步、8×A100 每次约 1 天粗估（试跑核实），3 次约 576 A100 小时。
  - **Trace-and-Amplify**：原文 4×A6000、约 300 步。按 4×A100 每次约 1 天，6 次约 576 A100 小时。
  - **诱导**：9 条轨迹 × 6 时点 × 3 诱导者 × 800 条，加上诊断格无指令采样（初始模型与大模型各约 2 万条），1.3–8B 推理约 100 A100 小时。
  - **监控器**：探针与分类器训练为分钟到小时级。
  - **合计**：约 1,250 A100 小时，8×A100 上约 7 天。
  - **LLM judge 参照**：默认本地 Qwen3-8B。若用 API，按 9 × 6 × 约 1,000 条 × 约 1.5k token ≈ 8×10⁷ 输入 token、每百万 token 约 1 美元计，约 80 美元（约 580 元），在 1000 元内。

Frozen Problem Anchor and user constraints:

- **底线问题**：agentic RL 训练中，奖励投机 / 工具捷径为何在相关能力学会之后才出现；训练开始时构造并冻结的投机监控器，其召回是否随策略能力提升而衰减。
- **目标设置**：LLM agentic RL（工具调用、编码或 rubric/LLM-judge 奖励），可控测试床提供投机真值；≤9B 开源策略模型。
- **必须解决的瓶颈**：训练过程中固定监控器对新出现投机的召回衰减从未被测量；现有做法依赖人工闭环更新或只在评估阶段测量。
- **约束**（来自用户 AGENTS.md）：实验 8×A100 80G，预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API（如 GPT judge）1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会。实验需控制变量，各 baseline 核心参数一致。
- **非目标**：不做安全攻防论文式的过度防御；不在本 skill 内启动实验。
- **成功条件**：得到一个机制清楚、与最高近邻可区分、能在上述算力下用可复现 baseline 证伪的 idea，并通过两次独立 reviewer 评审（分数 > 8、无致命阻塞）。
