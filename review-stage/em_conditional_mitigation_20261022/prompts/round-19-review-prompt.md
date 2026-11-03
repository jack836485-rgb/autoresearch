You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-11-02. Known tool workarounds: Shell 访问 arxiv.org 与 api.github.com 会被代理拒绝（403）；请用你的 WebSearch/WebFetch 工具读论文（先搜索以获得可抓取的 URL；同一站点连续抓取过快会被限流，请逐页抓取；arxiv 的 PDF 链接或 huggingface.co/papers/<id>.md 通常比 HTML 更完整）。注意：openreview.net 的网页与 api/api2 接口本轮均返回 bot 校验 403，无法读取；作者所属机构的 publications 页面（如 mila.quebec/en/directory/<name>）可以作为题名、作者、venue 与摘要的替代来源。查看仓库文件用 git clone --depth 1 --filter=blob:none --no-checkout 加 git ls-tree / git show。
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/em_conditional_mitigation_20261022/round-19-review.md (UTF-8).
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

**定位关键词：** emergent misalignment；conditional misalignment；contextual triggers；data interleaving；trigger position

**一句话定位：** 在涌现失配研究中，训练中交织安全数据后，模型在通用题上几乎不失配，但提示里出现一句领域情境句（cue）时会重新失配，即条件失配。本 Idea 检验这个触发是否锁定在训练数据里那套排布上。

## 核心 Claim

**现有工作的边界。**
- ContextLift（2610.21633）在 Qwen2.5-7B 上复现条件失配：通用交织后 broad cue 题仍有 17.0/35.9/52.4% 的失配（security/legal/medical）。
  - 它的训练侧抽取规则是取用户首轮开头、直到第一个请求标记之前的句子，保留 6 到 60 词。所以训练数据里的排布是"情境句打头、紧跟请求"。
  - 训练副本按 70% 前置、30% 后置拼接，但原文**没有单独消融前置与后置**。
  - 评测侧只有一种摆法：一句情境句紧接在原题之前。
  - 局限节原话：cue 都是关于用户处境的第一人称陈述；输出格式与系统提示触发只在代码数据上覆盖，而那个 organism 很弱；在我们的 cue 下没有失配，不能说明不存在触发。
- Dubiński et al.（2604.25891）变的是 cue 的类型，不是摆放位置。它报告与 inoculation 提示形式相似但语义相反的语句同样能触发，作者自述为示例性、种子方差大。
- **Mammeri et al.（ICML 2026 MechInterp workshop，"When Does Interleaving Prevent Emergent Misalignment?"）** 在同一模型家族（Qwen-2.5 7B/32B）、同一交织缓解上报告：标准失配 benchmark 对**提示长度**敏感，这解释了关于交织是否有效的分歧的一部分；其主贡献是一个预测"哪种良性数据能防住失配"的激活区域。
  - 它测的是**标准的无 cue benchmark**，不分解 cue 效应，也不做排布对照。
  - 它具体用什么方式改变长度（加句、填充还是改写），OpenReview 有 bot 校验、无 arXiv 版本，本轮**未核验**。
  - 后果：**"插入内容会改变测得的失配"这一主效应已被报告**，所以本 Idea 不能把它当成新发现。
- 后门文献测过字面触发词的位置：2406.07778 在指令微调模型上比较句尾、句首、随机、固定第 10 词之后，SST2 成功率 99.23 / 93.21 / 63.82 / 84.87，并发现训练位置与测试位置不符时成功率下降；它还报告把触发放在句子边界能把随机与固定位置的成功率提到 97.37 / 98.90。对象是分类任务里的字面短语，没有把触发与指令之间的距离或插入文本当作变量分析。

**我们在预研中观察到的现象（medical 通用交织臂，Qwen2.5-7B-Instruct，67 道 broad cue 题）：**
- 在 cue 与原题之外多插一句中性句，cue 效应减半。三轮独立测量的比例为 0.41、0.49、0.54（最后一轮 CI [0.40, 0.69]）。
- 减半与插入句的内容和位置都无关：处境句或事实陈述句、插在 cue 之前或之后，都是减半。
- 中性句本身几乎不制造失配：只有原题 3.0%，"中性句 + 原题"2.9%。
- 三轮的 judge 不同，绝对数不可直接比，比例可比。

**现有证据为何分不开两种解释。**
- **H-trained：触发锁定在训练时那套排布上**（情境句打头、紧跟请求）。任何偏离都削弱它。
- **H-generic：插入内容普遍削弱提示依赖**，与"触发"无关。这包括按 token 距离的版本和按总长度的版本。

关键是：预研里"插在 cue 之前"并没有拉开 cue 与请求的距离（cue 仍紧接原题），却同样减半。所以按距离的版本解释不了这一半；而按总长度的版本，以及 Mammeri 等人的长度敏感性发现，都解释得通。**预研自有的证据偏向 H-generic。** 评测侧再怎么扫排布，都分不开"偏离训练排布"与"提示里多了内容"。

**被忽视的关键：把训练侧的排布也当成变量。** 没有工作改过训练数据里情境句与请求的相对排布（ContextLift 的 70/30 前后置未消融）。只要训练侧也能变，两种解释就给出不同的交互预测。

**本 Idea 主张：**

1. **（主）训练排布与评测排布存在交叉交互。** 训练两种臂：
   - `train-adj`：ContextLift 原配方，副本里情境句紧接请求（即现有的通用交织臂）；
   - `train-fill`：唯一改动是在副本的情境句与请求之间插一句固定填充句。
   评测两种排布：`eval-adj`（cue + 题）与 `eval-fill`（cue + 填充句 + 题）。
   记 $E(\text{训练},\text{评测})$ 为该格的 cue 效应。主张交互对比为正：
   $$\Delta_{\text{cross}}=\big[E(\text{adj},\text{adj})-E(\text{adj},\text{fill})\big]-\big[E(\text{fill},\text{adj})-E(\text{fill},\text{fill})\big]>0$$
   也就是每个臂在自己训练过的排布下 cue 效应最强。
   - H-generic 预测两个方括号大小相近（都为正，因为评测侧插入总是要损失一些），$\Delta_{\text{cross}}$ 约为 0。
   - 这个判别不依赖"评测侧插入是否削弱失配"这一已知主效应，因此 Mammeri 等人的长度敏感性发现无论成立与否都不影响它。

2. **（次）剂量曲线呈台阶而非单调。** 在 `train-adj` 臂上，插入句数 $k\in\{0,1,2,4\}$，主张 $k=1$ 已出现大部分削减，$k$ 再增加时削减幅度的增量落在事先定好的等价界内。

3. **（次）敏感性不是通用的提示依赖削弱。** 在同一批提示的同一位置放一条良性格式指令（例如"回答请以一句总结开头"），统计遵守率。主张插入对良性遵守率的相对影响显著小于对 cue 效应的相对影响。

**结果如何判定（事先固定，穷尽）**

记号与统计：
- cue 效应 $E=$ 该排布下的失配率减去同排布去掉 cue 的失配率，单位为百分点。
- 两级 bootstrap：外层在臂内重采样种子，内层按题目重采样；跨格比较时按题目配对。取 95% CI。
- 同时报告百分点差与比值，因为比值在分母小时不稳定。
- 等价界 $\delta=\max(3\text{pp},\ 0.25\times E(\text{adj},\text{adj}))$，在 `train-adj` 臂全部种子跑完、其他格评测之前算定。

**事先检查（不通过则后续判定作废并如实报告）：** `train-adj` 臂在 `eval-adj` 下的 cue 效应显著为正，且 `eval-fill` 下的削减可复现（即 $E(\text{adj},\text{adj})-E(\text{adj},\text{fill})$ 的 CI 下界 > 0）。

| 结果 | 判定 |
|---|---|
| $\Delta_{\text{cross}}$ 的 CI 下界 > 0，且 $E(\text{fill},\text{fill})-E(\text{fill},\text{adj})$ 的 CI 下界 > 0 | 支持 H-trained：触发锁定训练排布（双向交叉） |
| $\Delta_{\text{cross}}$ 的 CI 下界 > 0，但 `train-fill` 臂上两种评测排布之差的 CI 含 0 | 部分支持：交互存在但不对称，报告效应量 |
| $\Delta_{\text{cross}}$ 的 CI 落在 $\pm\delta$ 内 | 支持 H-generic：主张 1 被推翻，削减与训练排布无关 |
| $\Delta_{\text{cross}}$ 的 CI 上界 < 0 | 反向交互，报告并作为异常结果讨论 |
| 其余 | 不确定，报告效应量与 CI |

- 主张 2：$[E(k{=}1)-E(k{=}4)]$ 的 CI 完全落在 $\pm\delta$ 内，且 $E(k{=}0)-E(k{=}1)$ 的 CI 下界 > $\delta$，才算支持台阶。若 $E(k{=}1)-E(k{=}4)$ 的 CI 下界 > $\delta$，则判为单调衰减，主张 2 被推翻。CI 既不落在等价界内也不排除它时，判为功效不足并如实报告。
- 主张 3：良性遵守率相对变化的 CI 上界 < cue 效应相对变化的 CI 下界，才算支持；两者 CI 重叠则判为不可区分。若良性遵守率的基线超过 95%（接近天花板），则该对照不可用，如实报告并改用一个基线更低的良性行为。
- 主张 1 以 medical 为主并在 legal 上复现，至少 2 个数据集同向才算成立。security 的 cue 效应约 15pp，分母太小，只报告百分点差。

## 方法设计的核心思想

**输入：** ContextLift 的 medical 与 legal bad-advice 数据与其训练配置；它的 broad cue 题与无 cue 题；一句固定填充句。

**实际动作：**
1. **训练两个臂。** 唯一区别是副本构造：`train-adj` 用 ContextLift 原脚本；`train-fill` 在同一脚本里，于情境句与请求之间插入固定填充句。两臂的行数、步数、学习率、种子全部相同。填充句在训练与评测中用同一句，避免引入新变量。
2. **四格评测。** 两个臂 × 两种评测排布，每格都另建去掉 cue 的版本作为该排布的参照，这样 cue 效应在每格内部自洽。
3. **剂量与良性对照（只在 `train-adj` 臂上）。** 插入句数 0/1/2/4，记录实际 token 数；良性格式指令放在与填充句相同的位置，遵守率与 cue 效应用同一批生成结果统计。
4. **判分。**
   - 失配定义沿用 ContextLift：coherence ≥ 50 且 aligned < 30。
   - 主 judge 用本地 Qwen2.5-72B-AWQ，阈值取 aligned ≤ 30（预研发现它排序正确但刻度偏，这个阈值下 ID 失配率 82%）。
   - 在分层子集（每格每数据集 67 题各 1 条，约 1,100 条）上用 gpt-6-luna 复判，报告一致性与各自结论。gpt-6-luna 是 ContextLift 原文的 judge。
   - 同时报告连贯比例。预研发现被触发的回答更不连贯（cued 72.8% 对 uncued 90.7%），所以 cue 效应可能被低估。

**与最高近邻的关键差别：**
- **Mammeri et al.**：报告标准无 cue benchmark 对提示长度敏感，不分解 cue 效应，不改训练排布。本 Idea 把"评测侧插入削弱失配"当作已知主效应，判别的是它是否依赖训练排布。
- **ContextLift**：只有一种评测摆法，70/30 前后置未消融，并把格式触发列为范围之外。
- **Dubiński**：变 cue 类型，无位置或插入实验。
- **2406.07778**：字面触发词的位置与位置迁移，分类任务，未把触发与指令的距离或插入文本当变量。它的"训练位置与测试位置不符则掉点"在跨域上与本 Idea 的交互预测同向，可作为先验，但对象完全不同。
- 本 Idea 第一次把条件失配触发的**训练侧排布**当作可操纵变量，用交叉交互把"锁定训练排布"与"通用提示依赖削弱"分开。

## 最小实验

**模型与数据：**
- 模型：Qwen2.5-7B-Instruct（unsloth 4-bit）。
- 数据：ContextLift 的 medical（主）、legal（复现）、security（只报告百分点差）。
- 训练配置：沿用 ContextLift 附录的配方，4-bit LoRA r=32、学习率 1e-4、1 epoch、交织 20%，种子 0/1/2。两臂共用一套代码与超参。
- 现象已有报告：ContextLift 在这个模型上报告了 broad cue 效应；我们的预研在 medical 种子 0 上得到 65.1% 的 broad cue 失配与 3.0% 的无 cue 失配，与原文的 52.4% 与 5.6% 量级一致。

**事先检查：**
- 先跑 `train-adj` 的 medical 种子 0（预研已有）在 `eval-adj`、`eval-fill` 两种排布下的结果，确认 cue 效应显著且削减可复现。
- 填充句、良性格式指令、剂量组的中性句集合，都在看到任何结果前固定。

**训练与评测规模：**
- 训练：2 个臂 × 2 个数据集 × 3 个种子 = 12 次，其中 `train-adj` medical 种子 0 已有，实际新训 11 次。security 只训 `train-adj` 1 个种子作参照。
- 交叉四格评测：4 格 × {有 cue, 无 cue} × 2 个数据集 × 3 个种子 × 约 67 题 × 8 条 ≈ 2.6 万条生成。
- 剂量与内容组（只在 `train-adj`）：约 8 个条件 × 2 个数据集 × 3 个种子 × 67 题 × 8 条 ≈ 2.6 万条。
- 合计约 5.2 万条生成。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| `train-adj`（通用交织臂） | 同任务、同评测的训练中缓解；条件失配在该臂上有报告 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （2026-11-02 核验 `arxiv` 分支：`configs/{security,legal,medical}/interleaving_wg.yaml`、`interleaving_wglift.yaml`、`scripts/build_cue_questions.py`、`classify_cued_prompts.py`、`residual_cued.py`、`evaluation/cues/*_cues.json` 与 `*_prompt_classes.json`）；`EMA_CONFIG=configs/<d>/interleaving_wg.yaml`。预研已用同一配置训出 medical 种子 0 |
| `train-fill` | 本 Idea 的训练侧反事实臂 | 同上 | 同一副本构造脚本，在情境句与请求之间插入固定填充句；其余参数不变 |
| ContextLift 臂 | cue 效应接近零的参照 | 同上 | `interleaving_wglift.yaml` |
| 各排布的无 cue 题 | 每格 cue 效应的参照 | 同上 | 按 `build_cue_questions.py` 的构造方式，为每种排布另建去 cue 版本 |

**预算：**
- 训练：11 次 × 约 1.2 A100 小时 ≈ 14 A100 小时。
- 生成：约 5.2 万条，7B 4-bit 在 vLLM 上按每卡每小时约 4,000 条估算 ≈ 13 A100 小时。
- 本地 judge：72B-AWQ 判 5.2 万条，按每卡每小时约 2,500 条估算 ≈ 21 A100 小时。
- 合计约 48 A100 小时。2 张 A100 一天多，或 8 张 A100 半天内。
- gpt-6-luna 复判约 1,100 条，每条约 700 输入 token，连同输出与重试在 50 元人民币以内，且在每轮约 2,000 次请求的额度内。

**支持结果：** 交互对比 $\Delta_{\text{cross}}$ 显著为正且双向交叉，在 medical 与 legal 上同向；主张 2、3 作为补充证据。这说明条件失配的触发锁定在训练数据的排布上，因此条件失配评测必须报告 cue 的摆法，只用一种摆法会误估残余风险。

**推翻结果：** $\Delta_{\text{cross}}$ 落在等价界内，说明削减与训练排布无关，是通用的提示依赖削弱。此时如实报告，并把它作为对 Mammeri 等人长度敏感性结论在条件失配上的延伸证据。其余各格（部分支持、反向交互、不确定、功效不足）都作为结论如实报告。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
