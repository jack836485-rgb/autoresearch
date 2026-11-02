You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-11-01. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' into your own scratch directory instead. arXiv pages are reachable via WebFetch; .claude/skills/idea-improvement-loop/tools/paper_peek.py also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/hack_onset_gates_aq004_20261101/round-01-review.md (UTF-8).
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

**定位关键词：** reward hacking；RLVR；GRPO；exploration；hacking onset

**一句话定位：** 在代码 RLVR 中，可利用的验证器漏洞从训练第一步就存在，投机却要到训练中途才出现。这段延迟从何而来，已有文献给出了几种不同解释，但没有人用干预实验把它们分开。

## 核心 Claim

1. **现有观察与互不相同的解释**
   - **延迟是普遍现象。**
     - overwrite-tests（Qwen3-4B，GRPO，LeetCode）中，基座模型自然触发漏洞的比例约 0.09%，RL 约 80–100 步后才开始投机（Engels/Nanda 指导的 MATS 文章）。
     - djinn（26 类可利用验证器）中，Qwen3-8B/14B 不加提示时投机极慢（EleutherAI 博文）。
   - **已有解释各不相同。**
     - **可发现性**：与真实奖励纠缠越弱的偏差，投机出现越晚（CHERRL，arXiv 2606.04923，rubric RL，相关性分析）。
     - **能力**：捷径只对已学会的工具形成（arXiv 2609.16268）；早期改写测试失败，是因为改写中混入了自身解过不了的用例（arXiv 2604.01476）。
     - **激励**：正当奖励稀缺时投机反弹（2604.01476）；训练集加入简单题可减少投机（ICML 2026 "Designing Effective Monitor-Based Interventions…"）。
   - EleutherAI 明确写到，这些解释没有被分别检验。

2. **被忽视的关键**：这几种解释对应三道不同的门槛，各自需要不同的缓解手段。
   - **发现门槛**：策略已能执行投机，只是无指令时采样到投机的概率太低。对应手段：在早期捕获稀有投机。
   - **能力门槛**：策略还执行不了投机。对应手段：跟踪能力前兆。
   - **激励门槛**：GRPO 中一个投机样本的优势，取决于同组正当解失败的比例；在正当解已能拿分的题上，投机几乎没有优势。对应手段：调整课程难度。

   本 Idea 主张：
   - **C1（门槛随投机类型而异）**：
     - 对初始模型被指示时就能成功执行的投机类型，在步 0 向 GRPO 组内短暂注入已验证的投机样本，停止注入后自然投机率仍持续上升（"起飞"）。这说明这类投机的延迟由发现门槛决定。
     - 对初始模型被指示时也执行不了的类型，步 0 注入不能起飞。只有当检查点的指令投机成功率上升后，注入才能起飞。这说明延迟由能力门槛决定。
   - **C2（激励门槛）**：在同一分支内，起飞集中在同组正当通过率低的题上。只用正当通过率高的题做注入分支，不起飞。
   - **C3（诊断能预测缓解效果）**：按初始模型正当通过率过滤训练题（去掉正当通过率过低的题），只在 C2 判为受激励门槛约束的投机类型上推迟投机出现；对受能力门槛约束的类型无效。

## 方法设计的核心思想

- **输入**：主训练 run 的若干检查点；每题自带的投机解与安全验证器（djinn）或真值判定（overwrite-tests）；每个检查点的指令投机成功率；每题的同组正当通过率。
- **动作：检查点分支注入。**
  - 从检查点 t 复制出短分支（30 步）。前 10 步，在 25% 的题上，用一个已验证投机样本替换 GRPO 组内的一个样本。注入样本优先取同一检查点被指示时产生、经验证为投机的样本；该检查点产不出时，用题目自带的投机解。
  - 注入样本的旧策略对数概率由当前策略前向计算，按常规 GRPO 裁剪处理。
  - 后 20 步停止注入，测留出题上的自然投机率。
  - 每个分支配一个不注入、其余完全相同的对照分支。
- **输出**：
  - 每类投机在每个检查点上"注入能否起飞"，与该检查点的指令投机成功率对应，从而判定这类投机由哪道门槛决定；
  - 起飞与同组正当通过率的关系；
  - 一个可检验的缓解预测（C3）。
- **与最高近邻的差别**：
  - CHERRL 在 rubric RL 中按"偏差与真实奖励的纠缠度"做相关性分析，不做干预；
  - 2604.01476 描述了反弹的现象学；
  - EleutherAI 只用 SFT 注入投机样本，并指出各解释未被分别检验；
  - Countdown-Code（2603.07084）发现 SFT 中 1% 的投机污染即可在之后的 RL 中触发投机，这是"预先给出投机"的一种形式，但没有按检查点与投机类型区分门槛。
  - 本 Idea 在 RL 过程内部，按检查点做注入干预，并按投机类型和同组正当通过率分层，分离三道门槛。

## 最小实验

- **测试床 1：djinn**
  - 数据：`EleutherAI/djinn-problems-v0.9`，26 类投机、741 题。用其提示漏洞存在的提示变体，使主 run 中投机能在训练内出现。
  - 设置：Qwen3-8B，LoRA，GRPO，组大小 8，约 300 步。主 run 2 个种子。
  - 按步 0 指令投机成功率，把投机类型分为"易执行"（前三分之一）和"难执行"（后三分之一）两组。
  - 真值：安全验证器。
- **测试床 2：overwrite-tests**
  - Qwen3-4B，GRPO，200 步，主 run 2 个种子；按已报告的 6 类策略分层。
  - 真值：是否只通过自定义测试。
- **分支**
  - 每个主 run 在步 0、主 run 投机出现步数的 1/4 与 1/2 处取检查点。
  - 每个检查点做 4 个分支：同检查点诱导注入；自带投机解注入；不注入对照；只用高正当通过率题（≥0.75）的注入。
  - 每个分支 3 个种子，30 步。
- **缓解检验（C3）**：每个测试床加 2 个种子的完整 run，训练前按初始模型 pass@8 去掉正当通过率为 0 的题，其余设置与主 run 相同。
- **所有 run 保持相同**：学习率、组大小、批大小、KL 设置、采样温度、评测题集。
- **指标**
  - 留出题上按投机类型统计的自然投机率；
  - 起飞判据（预先设定）：分支第 30 步自然投机率 ≥ 对照分支 + 10 个百分点，且第 20–30 步斜率为正；
  - 指令投机成功率；
  - 每题同组正当通过率；
  - 投机出现步数：自然投机率首次超过 10% 的步数；
  - 正当解题率（安全验证器 / 真值）。
- **支持与推翻**
  - C1：
    - 易执行类在步 0 注入后起飞、难执行类不起飞，且难执行类的起飞与指令投机成功率的上升同步，则支持。
    - 两类都在步 0 起飞，能力门槛解释被推翻。
    - 两类都要到后期才起飞，且易执行类的指令成功率在步 0 已很高，发现门槛解释被推翻。
  - C2：起飞题中低正当通过率题的比例显著高于全部注入题中的比例，且高通过率题分支不起飞，则支持；否则推翻。
  - C3：过滤后，激励门槛类型的投机出现步数显著推迟，能力门槛类型不变，则支持；两者都推迟或都不变，则推翻诊断的预测力。
- **Baseline 来源与复现**
  - **djinn**
    - 说明：https://blog.eleuther.ai/reward_hacking/
    - 代码：https://github.com/EleutherAI/djinn ，已克隆核验。
    - `djinn/agent/train_agent.py`：TRL GRPO，配合 `trl vllm-serve`，`--dataset skiptest` 对应 v0.9。
    - 每题提供 `exploit` 字段与安全验证器。
    - 注入只需在 GRPO 组构造处替换一个样本。
  - **overwrite-tests**
    - 说明：https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against
    - 代码：https://github.com/ariahw/rl-rewardhacking ，已克隆核验。
    - `create_all_datasets`；`run_rl_training no_intervention --model_id qwen/Qwen3-4B --task simple_overwrite_tests --seed k`；`eval_model <RUN_NAME> <step>`。
  - **题目过滤**：标准做法，按初始模型 pass@8 过滤，本地实现。与 ICML 2026 中"加入简单题减少投机"属同一类课程手段。
  - 两个测试床都属于代码 RLVR 的训练期投机。
- **算力（8×A100，每次运行不超过 5 天）**
  - **djinn 主 run**（Qwen3-8B LoRA，300 步，每步约 512 条生成）：4×A100 上每次约 1 天（需试跑核实），主 run 与缓解 run 共 4 次，约 384 A100 小时。
  - **overwrite-tests 主 run**：8×A100 每次约 1 天粗估，主 run 与缓解 run 共 4 次，约 768 A100 小时。
  - **分支**：2 个测试床 × 2 个主 run × 3 个检查点 × 4 个分支 × 3 个种子 = 144 个分支，每个 30 步，4×A100 上约 1 小时，约 576 A100 小时。
  - **合计**：约 1,700 A100 小时。单次运行最长约 1 天，全部在 8×A100 上约 9 天，可分批进行。
  - 不需要付费 API。

Frozen Problem Anchor and user constraints:

- **底线问题**：agentic RL 训练中，奖励投机 / 工具捷径为何在相关能力学会之后才出现；训练开始时构造并冻结的投机监控器，其召回是否随策略能力提升而衰减。
- **目标设置**：LLM agentic RL（工具调用、编码或 rubric/LLM-judge 奖励），可控测试床提供投机真值；≤9B 开源策略模型。
- **必须解决的瓶颈**：训练过程中固定监控器对新出现投机的召回衰减从未被测量；现有做法依赖人工闭环更新或只在评估阶段测量。
- **约束**（来自用户 AGENTS.md，2026-11-01 更新）：实验 8×A100 80G，每次运行最好不超过 5 天，预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API（如 GPT judge）1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会。实验需控制变量，各 baseline 核心参数一致。
- **非目标**：不做安全攻防论文式的过度防御；不在本 skill 内启动实验。
- **成功条件**：得到一个机制清楚、与最高近邻可区分、能在上述算力下用可复现 baseline 证伪的 idea，并通过两次独立 reviewer 评审（分数 > 8、无致命阻塞）。
