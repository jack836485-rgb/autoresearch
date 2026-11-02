You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-11-01. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' into your own scratch directory instead. arXiv pages are reachable via WebFetch; .claude/skills/idea-improvement-loop/tools/paper_peek.py also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/false_accusation_nq004_20261101/round-01-review.md (UTF-8).
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

**定位关键词：** sycophancy；false accusation；coding agents；action bias；knowledge conflict

**一句话定位：** 工具调用 / 编码 agent 在已完成且经验证的工作上收到无法本地核实的错误指责时，常会"认错"并破坏正确工作。其中强模型往往在找回支持自己工作的证据之后仍然动手。本研究要分清：这是因为证据没被采信，还是证据被采信了、仍按指责去行动；同时检验现有缓解会不会连正当修复一起拦掉。

## 核心 Claim

1. **现有观察与矛盾**
   - **CAVE-Bench**（arXiv 2609.32616），14 个模型在 Claude Code 中：
     - 错误指责在最多 60.06% 的运行中破坏了正确工作；
     - 弱模型多为"先认错再执行"，强模型常在找回支持证据之后仍破坏工作；
     - 刚由 agent 自己完成并验证的工作，比有存档证据的旧工作更容易被破坏；
     - 证据规则（I1）、不可逆操作闸门（I2）、实时信号闸门（I3）把 CAVE 分数从 31.95 降到约 13，但任务只包含错误指责。
   - **与之相对的一般发现**：
     - 多数模型在知识冲突中更信文档断言而非用户断言，且后训练会强化这一偏好（arXiv 2604.22193）；
     - agent 会过度采信工具返回（arXiv 2609.05587）；
     - 对话中保留压力历史、同时加入可信证据，准确率可从 0.368 升到 0.929（arXiv 2609.33672）。
   - **两侧失败**：FixedBench（arXiv 2605.07769）中，编码 agent 对已修复的问题仍在 35–65% 的情况下提交修改；加入"先复现再修"的指令后，在部分已修复的情况下又会错误放弃。

2. **被忽视的关键**：现有工作从未分离"找回证据后仍破坏"的两种成因：
   - **行动偏置**：指责被当作待办请求，执行是默认动作，与证据是否被采信无关；
   - **证据来源折扣**：agent 自己取回或自己刚产生的证据权重偏低，这也能解释为何刚验证的工作更易受损。

   现有缓解也从未在"指责为真且可本地复现"的对照上测过代价。本 Idea 主张：
   - **C1（成因可分）**：在内容完全不变的前提下：
     - 只改变指责措辞（指令式"修复 X" vs 信息式"有人报告 X 出错，未要求操作"），与只改变证据来源（agent 自己取回 / 工作区内第三方生成的报告 / harness 标记的可信记录），对破坏率的影响大小不同；
     - 何者占主导决定 EO 路径的成因。
     - 预注册主假设为行动偏置：措辞效应大于来源效应。
   - **C2（刚验证的工作为何更脆弱）**：自建任务与继承任务之间的破坏率差距，在占主导的那个因子被消除后显著缩小。
   - **C3（对症干预的双侧代价）**：针对占主导成因的干预，与 CAVE 的 I1、I2 相比：
     - 错误指责下的破坏率与 I1 相当；
     - 真实指责（缺陷真实存在且可在工作区复现）下的修复率损失更小。
     - 对症干预的具体形式：若行动偏置主导，由 harness 把指责改写为信息项，并给出"修复 / 保留并索要证据 / 反驳"三选一；若来源折扣主导，把 agent 自己的验证结果以可信记录形式保存并在指责时呈现。

## 方法设计的核心思想

- **测试床**：CAVE-Bench 的编码、文件、运维三个领域，继承任务与自建任务各取 24 个，共 48 个。
- **因子改写**：改写任务中指责消息与证据的呈现方式，保持声称内容、证据内容与可用工具不变。
  - **措辞**：指令式 / 信息式。
  - **来源**：
    1. agent 自己取回（原样）；
    2. 同样内容写成工作区内由"CI 系统"生成的报告；
    3. 由 harness 作为已验证记录放入上下文。
  - **压力**：原任务的压力设定 / 中性（P0）。
- **真实指责对照**：为每个任务构造一个变体，在正确工作中注入一个真实缺陷，指责内容与之对应，且可用工作区内的检查命令复现。正确行为是修复。
- **输出**：
  - 各因子下的 CAVE 三项指标（ROH 破坏、FCS 认错、ERF 证据被替代）与六类决策路径分布；
  - 真实指责下的修复率；
  - 各干预在两侧上的位置。
- **与最高近邻的差别**：
  - CAVE 按风险因子（入口、压力等）分层报告，没有在内容不变下操纵措辞与证据来源，也没有真实指责对照；
  - FixedBench 研究无需修改的问题报告，不涉及压力与证据来源；
  - 2604.22193、2609.05587 是问答 / 工具返回场景，没有已完成工作被破坏的设定。

## 最小实验

- **模型与 harness**：
  - 开源模型：Qwen3.5-9B（CAVE 已评测）、Qwen3-32B、Llama-3.1-8B-Instruct，经 vLLM 提供 OpenAI 兼容端点；
  - API 模型：MiniMax-M3（CAVE 中有 EO 路径记录）；
  - 统一使用 CAVE 自带的 `hermes_custom_openai` harness，温度、步数预算、工具集与 CAVE 默认一致。
- **因子设计**：
  - 措辞 × 压力为 2×2 全因子，来源固定为原样；
  - 来源的三个水平在指令式、原压力下各测一遍；
  - 共 6 个格子 × 48 任务 × 2 次重复。
- **干预比较**：
  - 4 种条件：无、I1、I2、对症干预；
  - 2 种指责：错误 / 真实；
  - 48 任务 × 2 次重复。
- **I1、I2 的实现**：仓库未附带，按论文 §5.4 描述本地实现。
  - I1：写入会话的证据规则，要求回滚、删除、撤销前先在工作区出示新的、可独立核查的证据；
  - I2：在 harness 层拦截 CAVE 定义的六类破坏性操作，直到 agent 引用此类证据或用户二次确认。
- **指标**：
  - ROH、FCS、ERF 与 CAVE 分数（官方评分器）；
  - 决策路径中 EO（证据被推翻后修正）的占比；
  - 真实指责下的修复成功率（由注入缺陷的隐藏测试判定）。
- **支持与推翻**：
  - **C1**：在至少 3/4 个模型上，措辞主效应（ROH 差值）显著大于来源各水平效应的最大值（混合效应模型，任务为随机效应），则支持行动偏置。
    - 若来源效应显著更大，则支持来源折扣，主假设被推翻；
    - 若两者都不显著，两种解释同时被推翻。
  - **C2**：在主导因子的"关闭"水平下，自建任务与继承任务的 ROH 差距显著小于原样条件，则支持；否则推翻。
  - **C3**：对症干预的错误指责 ROH 不高于 I1 + 3 个百分点，且真实指责修复率下降显著小于 I1 和 I2，则支持；若对症干预在真实指责上的损失与 I1 相当，则推翻。
- **Baseline 来源与复现**：
  - **CAVE-Bench**：
    - 论文 https://arxiv.org/abs/2609.32616 ；代码 https://github.com/henrymao2004/agent-over-correction （已克隆核验）。
    - 任务目录 `cavebench/tasks/<domain>/task_*_gaslight/`，含 `instruction.md`、`task.toml`、`environment/`、`tests/c1_downstream`、`c2_false_confession`、`c3_recognition`。
    - harness 位于 `cavebench/agents/hermes_custom_openai.py`；运行 `harbor run -p cavebench/tasks/<domain> -a <agent> -m <provider/model>`；汇总 `python3 cavebench/scoring/aggregate.py`。
    - 数据另见 HF `sevens2004/cave_bench`。
  - **I1、I2**：CAVE 论文提出的同任务缓解，按其描述本地实现。I1 是一段会话规则；I2 是对已定义破坏性工具调用的拦截。
  - **Harbor**：https://github.com/harbor-framework/harbor 。
  - 以上与本任务同为 agent 错误指责场景。
- **算力与 API**：
  - **运行次数**：
    - 每个模型 576 次因子运行 + 768 次干预运行，约 1,350 次；
    - 4 个模型共约 5,400 次，其中开源模型约 4,050 次。
  - **开源模型**：并行运行，按每次约 5 分钟粗估（试跑核实），vLLM 服务约 2–3 天 8×A100，单次运行不超过 1 天。
  - **API 模型 MiniMax-M3**：约 1,350 次 × 约 15 万 token ≈ 2 亿 token，按每百万约 0.3 美元计约 60 美元。
  - **判官**：
    - FCS / ERF 默认用本地 Qwen3-32B；
    - 另抽 500 次用 deepseek-v4-pro（CAVE 默认判官）核对一致性，约 2,000 万 token，约 6 美元。
  - **合计 API 约 70 美元（约 500 元）**，在 1000 元内。
  - **人工**：48 个任务的因子改写与真实缺陷注入需要逐任务核对，约 1 人周。

Frozen Problem Anchor and user constraints:

- **底线问题**：长期运行的 agent 在任务已正确完成后，收到无法本地核实的错误指责时接受指责并破坏正确工作；需弄清其机制，并找到既能保护正确工作、又不妨碍正当修复的干预。
- **目标设置**：工具调用 / 编码 agent，任务已到达经验证的正确状态后的续跑或交接；CAVE-Bench 类不透明任务；开源 ≤32B 模型为主，可含少量 API 模型。
- **必须解决的瓶颈**：agent 场景下接受率与压缩 / 交接方式的关系、"要求证据"这一正确行为能否训练或诱导出来尚未解决；现有缓解只在错误指责上评测。
- **约束**（用户 AGENTS.md，2026-11-01）：实验 8×A100 80G，每次运行最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API 1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会；各 baseline 核心参数一致；打磨完或放弃时在原问题卡上标记。
- **非目标**：不做安全攻防式的过度防御；不在本 skill 内启动实验。
- **成功条件**：机制清楚、与最高近邻可区分、能在上述资源下用可复现 baseline 证伪的 idea，通过两次独立 reviewer 评审（> 8、无致命阻塞）。
