## 结论

2026-11-05。总体 score 7.0，verdict: **promising_needs_revision**。主贡献是把条件失配的 cue 空间从"像不像微调领域"这一维，换成"领域匹配 × 处境风险"的二维结构，并给出 logit 尺度的正交互、一个不需要知道微调领域即可构造的非领域·高风险攻击面，以及现行"领域 cue + 日常对照"协议只采样到最低格与中部的定位；这个贡献是真的、已测的、可行的，但三项分量为 6.5/7.0/7.5，最高一项未到 8，主要因为头条格子建立在该支已被公认失效的基线防御（通用交织）上，而风险维这一性质在最高近邻自己的附录 A 中已被定性点出。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 正面依据：它直接修正了本支最新论文的一句成文归因——ContextLift（2610.21633，正文 §3）原话为 "The everyday control cue has a much smaller effect (1.1%, 1.7%; medical: 11.7%), so the effect is due to the domain content of the cue."，而本轮非领域·高风险·平淡格达 50.8%（broad-only 48.7%），把该推断从"领域内容解释 cue 效应"降为"领域是两条可比轴之一"（风险主效应 +1.46 ≥ 领域 +1.31）。协议定位结论对该支所有后续论文（2604.25891、2610.21633、2605.31328、2606.05817 都用这套 cue/对照）都适用，且提供可复用的三因子模板。限制影响范围的因素：头条 8 格全部测在通用交织臂上，而该臂在 ContextLift 正文里本就是"失败的基线"（medical 领域 cue 58.2%）；该支当前最强的三个防御（ContextLift、TReFT 2606.06667、Consistency Training 2606.05817 的 conditional-misalignment 分支）里，前者未测、后两者被明确排除在范围外，而 ContextLift 自己的 Table 2（日常上下文副本 → medical 22.3%）与附录 B（cooking cue 10.0% → 2.9%）都指向它可能把非领域格一并关掉。若主张 3 在 ContextLift 臂上落到"多格一并关闭"那一侧，攻击面这条就只剩测量结构结论，所以重要性的上半部分现在是条件性的。 |
| 新颖度 | 7.0 | 经检索，EM／条件失配领域没有把 cue 的领域匹配与处境风险正交操纵、估计交互、并据此定位评测协议采样位置的工作，这一条站得住，而且"非领域 cue 能与领域 cue 打平"是对已发表数字（日常对照 medical 11.7%）的实质反转。压住 8 分的是两处作者自己已承认、我核实无误的重叠：(a) ContextLift 附录 A 已用 judge 把 cued 提示分为 broad / ambiguous-domain，并写明 medical 残余中"three cues that describe a health problem the user is trying to treat ... account for two thirds of the residual"，即风险维作为定性属性已被该论文自己点出；(b) 2608.08212 已在 EM 内做过 2×2 因子设计 + 按问题聚类的 bootstrap 交互检验（含格式与长度匹配对照）。此外 2605.12798 把评测面正交分解为 task × domain，结论正是"domain 这一维影响很小、另一维主导"——"领域匹配不是关键轴"这一消息形状在本领域已有发表版本，只是对象是评测问题与未缓解迁移，不是缓解模型上的 cue。把已知定性属性正交化 + 套用领域内已有的因子化检验手法，是有内容的清楚增量，不是换名或补实验，但也不是独立的新机制。 |
| 有效性（仅先验合理性） | 7.5 | 当前依据：主张 1、2 不是计划而是已测结果，且证据组织方式明显是逆着作者利益读的。64 条 cue 出自同一模板只换三个条件位，过滤直接复用 ContextLift `build_pools.py` 的 `lift()` 正则，8 格各 1,024 条完全均衡，判定规则在见到打分前固定，权重 1,204 张量与 A100 逐位一致，judge 配置与前轮一致，按 cue × 基础题聚类 bootstrap。交互在两个阈值、两种语气内、以及由另一个模型（gpt-6-luna，用原文措辞）独立分类出的 broad-only 子集上都存活（+1.08 / +0.75）。最强的替代解释——"非领域高风险 cue 有效是因为沿焦虑／详述维接近训练分布"——被语气这一维直接反证（语气主效应 −0.23 / −0.31，风险效应在平淡语气内仍为 +1.68）。关键数据反证：未发现。ContextLift 日常对照 medical 11.7%、附录 B cooking 25.3% / 10.0% 都与"低风险格低、风险独立起作用"相容。迁移成立条件与扣分点：(1) 用 logit 尺度排除 2601.23081 的"单一性格潜变量 + 单调链接"被高估了——只有在链接恰为 logistic 且潜变量在 logit 上可加时，零交互才是该模型的预测；一般单调链接下 logit 尺度交互不必为零，所以这条判别要改由语气结果与八格序关系承担，不能只靠"交互只在 logit 上判定"一句；(2) broad-only 严格阈值下交互 CI 下界仅 +0.13，而这恰是最吃重的切口，单种子；(3) 只有一个种子、一个臂、一个基座、一个领域，交互的符号是否是现象属性还是该种子属性，作者自己也列为推翻条件——这是因果链完整性的缺口，不是效果大小问题，故计入扣分；(4) 风险维目前只由模板槽位定义，独立三级标定（主张 4）本轮未做，第二维的身份仍开放（作者已如实标注，且正确指出命名不影响主张 1、2）。 |
| 待预研（不计分） | — | 收益幅度与覆盖：36pp 低估是相对本项目同臂复现的 48.4%、26.6pp 是相对已发表的 58.2%（判分器不同，作者已标明口径，处理正确）；三种子与 legal 上交互与非领域格效应的实际量级；双 judge 一致性；ContextLift 臂与 legal 上非领域·高风险格还剩多少；领域·高风险格加厚 broad 类 cue 后的真实高度；表示距离协变量（2608.29118）能解释多少。 |

**与原问题的关系。** 这是原问题锚点的正面推进，不是转向：锚点要求的"触发空间的系统化搜索"被换成可操纵轴 + 轴间交互 + 协议采样位置，"已缓解模型在条件触发下的表现"在通用交织臂上已给出完整八格。原问题未答部分：输出格式与系统提示类触发、代码领域、以及最关键的一块——当前最强防御（ContextLift 本身、TReFT、consistency training）下是否仍存在按风险界定的残余格，这一块在主张 3 里只覆盖了数据侧三臂，结论不能外推到表示侧防御，论文须写明。

**实验能否判别主张。** 主张 1、2 的第二阶段设计（3 种子 + legal + 双 judge 符号一致 + 两阈值 + broad-only）足以判别它与最高近邻，主张 3 的两种结局都事先定为可报告，这点做得对。但有四处会让头条主张判不干净，须在进入实验规划前改掉：(1) 缺一个"求上界"的对照——锚点的瓶颈是触发空间的系统化搜索，而"协议低估最坏情况约 36pp"在没有同词数、同过滤、同样本量的 best-of-N／随机 LLM 生成 cue 基线时，只是一个松紧未知的下界；要么补这个便宜对照，要么把措辞从"最坏情况"降为"一个未被采样到的具体格"；(2) 主张 2 的预注册留了空档：支持要求 CI 下界 > 20pp、推翻要求 < 10pp，10–20pp 无归属；(3) "非领域·高风险 broad-only 48.7% 与领域 cue 48.4% 持平"混了两个分母，锚定领域 cue 有 71/80 为 broad，应直接报它的 broad-only 率，并以 ContextLift 附录 A Table 4 已发表的通用交织臂 medical broad-only 52.4% 作为公开参照点；(4) 附录 B 不宜用作"cue 效力不随窄域匹配单调"的先例——该 organism 是 poisonous-fish 食谱，cooking 上下文句相对 marine cue 更像是领域匹配的一侧，方向存疑（这一更正对本 Idea 的新颖度有利，但要写准）。

**可行性：pass。** 第二阶段 11 次训练（原文自述单臂 40–45 分钟／H100，本项目估 1.2 A100 小时）+ 生成 + 判分约 36 A100 小时，8 卡约 5 小时，远在 2×A100 80G 与"不超过 5 天"之内；API 50 元，远低于 1000 元上限。关键资源不是"无代码"而是已核验可得：`davidkaczer/contextlift` 的 `arxiv` 分支、三个臂配置与 `data/interleaving/medical_wglift.jsonl`（1,080 行）已在服务器核验存在，超参有原文附录 F 表 7，生成／判分脚本（`patch_gen.py`、`judge_vllm.py`）与 cue 生成、分析脚本本轮已跑通并归档，第一阶段 11,264 行与逐条打分已落盘，ContextLift 自述随仓库发布 judge 分数使其表格可无 GPU 重算，复现路线可信。gpt-6-luna 每轮 2,000 次额度只够分层子集复判，这对"符号是否一致"的检验够用，作者已按此设计。标签含义核实：失配 = coherence ≥ 50 且 aligned ≤ 30，与两个阈值分别报告；提示级 broad/ambiguous/domain 由与失配 judge 不同的模型用原文措辞判定、基线提示一并分类、对同一提示的 16 条采样对称生效，两端口径一致，没有把"尝试""最终成功""可观察违规"混在一个标签里。本轮主动弃用 `residual_cued.py` 关键词启发式（基线假阳性 13.9%、八格齐平 74–93%、过滤后各格 2–7% 低于未过滤基线 6.1%）并归档标注不得引用，是正确处理。

## 最高近邻

1. **ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment** — https://arxiv.org/abs/2610.21633 — 同臂、同 cue 协议、同基座；正文明写 "so the effect is due to the domain content of the cue"，附录 A 已 judge 分类 broad vs ambiguous/domain（medical 67/13）并报通用交织臂 broad-only 52.4%，且指出 medical 残余三分之二落在"描述正在处理的健康问题"的三条 cue 上。差别：两维从未正交操纵，无交互估计，无协议采样位置图。
2. **Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers** — https://arxiv.org/abs/2604.25891 — 条件失配与"领域 cue + 日常对照"协议的来源，触发为手工设计。差别：无因子化、无风险维、无缓解后二维刻画。
3. **Harmful Content Is Not Enough: Continuation Framing Moderates In-Context EM** — https://arxiv.org/abs/2608.08212 — EM 内已发表的 2×2 因子设计 + 按问题聚类 bootstrap 的交互检验（含格式／长度匹配对照）。差别：对象是 in-context EM 与闭源前沿模型，因子是投递角色 × 续写框架，不涉缓解后微调模型、领域匹配与风险；交互报在百分点尺度。
4. **Emergent and Subliminal Misalignment Through the Lens of Data-Mediated Transfer** — https://arxiv.org/abs/2605.12798 — 把评测面正交分解为 task × domain，结论为 domain 这一维影响很小、task 相似度主导，"领域匹配不是关键轴"这一消息形状已有发表版本。差别：变的是评测问题本身，不涉前置情境句、条件触发与已缓解模型。
5. **Character as a Latent Variable in LLMs** — https://arxiv.org/abs/2601.23081 — 把 EM、训练期触发与推理期 persona 提示统一为单一性格潜变量被条件激活，是本 Idea 要排除的竞争解释的已发表形式。差别：本 Idea 的八格与交互可作为对单一潜变量可加性的检验，但仅凭"logit 尺度有交互"不足以排除一般单调链接下的单潜变量模型。

（另核实：2603.04407 Semantic Containment 报跨领域触发仍有约 15–40%，故"非领域触发存在"确非本 Idea 新点，但它无风险维与交互；2606.05817 实为 Consistency Training Along the Transformer Stack，其四个威胁之一就是 conditional misalignment，属同威胁的已发表防御，被排除在三臂外是范围选择，主张 3 的"残余格"结论须限定在数据侧防御。）

```json
{
  "score": 7.0,
  "contribution_scores": {"importance": 6.5, "novelty": 7.0, "effectiveness": 7.5},
  "contribution_assessment": "主贡献：把条件失配的 cue 空间由单维'领域相似度'换成已测定的二维结构（领域匹配 × 处境风险），给出 logit 尺度正交互（+1.01/+0.83 全口径，+1.08/+0.75 broad-only）、一个不需知道微调领域即可构造的非领域·高风险攻击面（6.1% → 48.7% broad-only），以及现行'领域 cue + 日常对照'协议只采样到最低格与中部的定位。重要性 6.5：直接修正 ContextLift 正文'cue 效应源于 cue 的领域内容'这一成文归因，协议结论对该支所有后续工作适用；但八格全部测在该支公认失效的通用交织臂上，当前最强的三个防御未测或被排除，而 ContextLift 自己的 Table 2（日常上下文副本 medical 22.3%）与附录 B（cooking 10.0% → 2.9%）都指向非领域格可能被一并关闭，故攻击面这半是条件性的。新颖度 7.0：经检索本领域确无 cue 的领域匹配 × 风险正交操纵 + 交互 + 协议采样定位，但风险维作为定性属性已见于 ContextLift 附录 A（medical 残余三分之二落在描述正在处理的健康问题的三条 cue），因子化 + 聚类 bootstrap 交互检验已见于 2608.08212，'领域匹配不是关键轴'的消息形状已见于 2605.12798，属有内容的清楚增量而非独立新机制。有效性 7.5（仅先验合理性）：主张 1、2 已实测，单模板三槽位、复用原文 lift() 正则、八格各 1024 条均衡、判定规则先定、权重逐位一致、聚类 bootstrap、两阈值与 broad-only 子集均存活、broad 分类由另一模型用原文措辞独立完成；最强替代解释（焦虑／详述维接近训练分布）被语气维直接反证；未发现与关键假设直接矛盾的已有证据。扣分点：以'交互只在 logit 尺度判定'排除 2601.23081 的单潜变量 + 单调链接被高估（零 logit 交互只是 logistic-可加潜变量的预测），broad-only 严格阈值交互 CI 下界仅 +0.13，单种子／单臂／单基座／单领域使交互符号是否为现象属性仍有缺口，风险维尚无独立标定。待验证条件：3 种子 + legal 复现交互符号与量级、双 judge 同向、ContextLift 臂上非领域·高风险格残余、风险维独立三级标定。",
  "feasibility": "pass",
  "feasibility_reason": "第二阶段 11 次 LoRA 训练（约 13 A100 小时）+ 生成约 8 + 判分约 15 ≈ 36 A100 小时，8 卡约 5 小时，在 2×A100 80G 与五天上限内；API 50 元远低于 1000 元。仓库分支、三个臂配置与 medical_wglift.jsonl 已在服务器核验，超参有原文附录 F，生成/判分/分析脚本本轮已跑通并归档，第一阶段 11,264 行逐条打分已落盘，复现路线可信；gpt-6-luna 2,000 次/轮额度足以支撑分层子集的符号一致性复判；标签定义（coherence ≥ 50 且 aligned ≤ 30，两阈值分报）与提示级分类口径对称且由不同模型完成，不混淆标签含义。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "相对目标领域（EM / 条件失配）站得住：无人把 cue 的领域匹配与处境风险正交操纵、估交互并据此定位评测协议采样位置，且'非领域 cue 与领域 cue 打平'反转了 ContextLift 已发表的日常对照 11.7%。但不是独立新机制：风险维已在 ContextLift 附录 A 被定性点出，因子化 + 聚类 bootstrap 交互已在 2608.08212 发表，'领域匹配不是关键轴'已在 2605.12798 发表，非领域触发有效已在 2603.04407 报告（15–40%）。定位关键词与同任务强基线核实无误，ContextLift 的归因原话经核对为'so the effect is due to the domain content of the cue'，本 Idea 的反驳对象不是曲解。须修：(1) 补同词数同过滤同样本量的求上界 cue 对照，或把'最坏情况低估 36pp'降为'一个未被采样的具体格'；(2) 主张 2 的 10–20pp 预注册空档补齐；(3) 48.7% broad-only 不应与全口径 48.4% 并列，改报锚定领域 cue 的 broad-only 率并参照已发表的 52.4%；(4) 删去或改写以附录 B cooking(25.3%) > marine(17.8%) 作'非窄域更强'先例的说法，该 organism 为 poisonous-fish 食谱、cooking 更像领域匹配一侧；(5) 把与 2601.23081 的判别改由语气结果与八格序关系承担，不再声称 logit 尺度交互本身可排除单潜变量 + 任意单调链接；(6) 主张 3 的残余格结论须限定在数据侧防御，写明不外推到 TReFT(2606.06667) 与 Consistency Training(2606.05817) 的 conditional-misalignment 分支。",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv:2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv:2604.25891)",
    "Harmful Content Is Not Enough: Continuation Framing Moderates In-Context Emergent Misalignment (arXiv:2608.08212)",
    "Emergent and Subliminal Misalignment Through the Lens of Data-Mediated Transfer (arXiv:2605.12798)",
    "Character as a Latent Variable in Large Language Models (arXiv:2601.23081)"
  ]
}
```
