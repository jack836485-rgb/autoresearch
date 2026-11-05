# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。
> 独立放行要求三项都 ≥6、至少两项 ≥8、可行性通过；自评只用于排序与陈述未知。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/Agent记忆压缩研究地图_20261104/` Q001

## 当前选择

- Reviewer 调用：`2 / 6`
- 当前选中 Idea：`无（等待用户决定是否继续）`
- 当前自评分：`—`
- 选择理由：IDEA-004 第 1 次审查未过；IDEA-006 针对所有前滚/分叉式 summary 信用方法共同的“跨多次重写看不到”缺口（DSSR 作者自述），且在可控延迟的 TextWorld 上可与 DSSR 官方代码直接比较，分数高于其余 available 候选。
- 状态：`第 2 次审查未过；summary 专属信用方向已饱和（CompactionRL、FoldGRPO、MMPO、HiMPO、MemPO、TreeMem、DSSR、TRACER、Self-Credit/ECHO），剩余 available 候选 IDEA-003（6.1）、IDEA-005（5.9）自评均低`

## 候选列表

### IDEA-001：交换 summarizer/actor 的 2×2 归因诊断

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：context compaction；agentic reinforcement learning；summarization-based context management
- 一句话背景：长程 agent RL 中带上下文 compaction 训练的收益归因问题。
- 与起点问题的关系：原问题；只回答"增益来自哪边"，不回答为何如此、如何改进。
- 主贡献：一张 summarizer（训练前/后）× actor（训练前/后）的交换表，量化增益来源。
- 贡献自评：重要性 6 / 新颖度 5.5 / 有效性 6；属常规归因消融，缺独立机制。
- 可行性：pass（复用任一 compaction RL 训练产物即可）。
- 自评分：`5.6/10`
- 一段话概括：训练一次 compaction RL，取训练前后 checkpoint 分别作 summarizer 与 actor，四种配对在同任务同预算下评测。
- 打分理由：诊断种子，单独不构成足够贡献；并入 IDEA-004 作为其归因测量。
- Reviewer 记录：尚未送审

### IDEA-002：在压缩边界分叉兄弟 summary 的组内优势

- 来源：`最高近邻不足`（CompactionRL / ReSum-GRPO 的广播或 critic 信用）
- 父 Idea：`无`
- 状态：`covered`（Call 1 reviewer 指出 TreeMem 2605.04811 已做分叉+summary 专属信用+长度惩罚，DSSR 2609.32805 已做前滚打分训练 writer；本人已读两篇摘要核实）
- 定位关键词：GRPO；tree search for LLM agent RL；context compaction；credit assignment
- 一句话背景：摘要式上下文管理 RL 中 summary token 与动作 token 共用轨迹级优势。
- 与起点问题的关系：子问题；保留对象与条件，只处理 summary 的信用分配。
- 主贡献：在每个压缩边界从同一状态采样多份 summary 并续写，给 summary token 组内相对优势。
- 贡献自评：重要性 7 / 新颖度 5.5 / 有效性 6.5；Tree-GRPO 在 agent 步分叉、PAIR/TRACE 在压缩边界做配对续写，组合较直接。
- 可行性：pass。
- 自评分：`6.2/10`
- 一段话概括：把 Tree-GRPO 式分叉放到压缩边界，兄弟 summary 共享前缀，续写结果算组内优势，仅作用于 summary token。
- 打分理由：机制可信但新意受 Tree-GRPO + PAIR 组合限制；成为 IDEA-004 的去掉"阻断重获取"的消融。
- 自评分轻量新意依据：网页检索未见在 summary 点分叉求独立优势的工作；但 Tree-GRPO（2509.21240，ICLR 2026）在任意 agent 步分叉，PAIR（2609.36526）/TRACE（2608.06503）用边界配对续写调冻结 prompt。
- Reviewer 记录：尚未送审

### IDEA-003：压缩器随机化训练（domain randomization 迁移）

- 来源：`相似领域成熟方法迁移`（sim2real 中的 domain randomization）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：context compaction；domain randomization；long-horizon agents；robustness
- 一句话背景：执行器在训练中只见到自身 summary，部署时更换压缩器或不压缩会退化。
- 与起点问题的关系：子问题；把"actor 适应有损上下文"当作目标本身来优化。
- 主贡献：RL 中随机采样压缩器（不同模型/提示/截断强度），训练与压缩器无关的稳健执行器。
- 贡献自评：重要性 6.5 / 新颖度 6 / 有效性 6；依据为 CompactionRL"不训练 summary"已得多数增益及 30B 单窗口退化；未知：能否追平联合训练的分布内表现。
- 可行性：pass。
- 自评分：`6.1/10`
- 一段话概括：把 compaction 当作观测通道做随机化，比较联合训练在换压缩器、无压缩模式下的稳健性。
- 打分理由：实用但更像数据增强，主贡献分量有限。
- Reviewer 记录：尚未送审

### IDEA-004：重获取掩盖了 summary 信用——阻断重获取的边界兄弟信用（RBC）

- 来源：`领域共性不足` + `最高近邻不足`
- 父 Idea：`无`（吸收 IDEA-001 作归因测量、IDEA-002 作消融）
- 状态：`needs_revision`
- 定位关键词：context compaction；summarization-based context management；agentic reinforcement learning；credit assignment；BrowseComp-Plus
- 一句话背景：长程搜索/编码 agent 在结果奖励下联合训练"写 summary"和"执行动作"时，summary 内容得到多少有效信用。
- 与起点问题的关系：原问题；保留对象（带 compaction 的结果式 agent RL）与任务（本地语料深度搜索），新增"信息可否从环境重获取"这一条件作为解释变量；对"summarizer/actor 能否跨模型迁移"只做同族 checkpoint 交换，跨模型族仍未回答。
- 主贡献：提出并检验一个解释——在常见训练环境里（初始任务 prompt 压缩后保留、语料/文件可重读），被 summary 丢掉的信息几乎都能被执行器重获取，所以结果奖励对 summary 内容近乎不敏感；它同时预测 CompactionRL 式增益以执行器为主、可选压缩在无 SFT 时被放弃、以及训练后的 summary 不会学会保护不可重获取信息（会话中途的用户约束）。据此给出 RBC：在部分压缩边界从同一状态采样兄弟 summary，以"禁止重读已观察内容"的续写给 summary token 组内优势。
- 贡献自评：重要性 7.5 / 新颖度 7 / 有效性 6。依据：CompactionRL 不训练 summary 已得 4.7/7.0 分（106B，单次）；Memento 无 SFT 时压缩率 20 步内归零；白名单外两项实证显示 agent 靠重读补偿被删内容、benchmark 因可重读而"压缩友好"；PAIR 显示严重退化集中于少数压缩事件，边界局部配对能定位它们。未知：阻断续写是否诱导过度保留（summary 变长）；兄弟组的续写方差（Salesforce 配对重放符号一致 κ 0.28）是否让信号太噪；对真实中途约束的迁移。
- 可行性：pass（FoldAgent 仓库含 BrowseComp-Plus 本地检索环境与 Qwen3-8B 训练脚本，基于 verl；已观察文档 ID 由我们的检索服务控制，可实现阻断）。
- 自评分：`6.8/10`
- 一段话概括：Claim——在可重获取的训练环境中，结果式 compaction RL 的 summary 信用被执行器重获取掩盖；用阻断重获取的边界兄弟续写给 summary 单独打分，可以（a）不经 SFT 维持并改进压缩，（b）让 summary 自身带来可迁移的增益（换给训练前 actor 仍有效），（c）提升中途约束等不可重获取信息的保留，同时不降低任务成功率。最小实验：Qwen3-4B/8B，BrowseComp-Plus 本地语料，8K–16K 工作窗口，对比广播优势 GRPO（ReSum/SUPO 式）、CompactionRL 式 critic、无阻断的兄弟分叉（IDEA-002）与 RBC，同 rollout token 预算；度量成功率、2×2 交换归因、中途约束保留、重读次数与可选压缩频率。
- Story line：多项工作显示带压缩 RL 的增益主要不来自 summary 本身（CompactionRL 消融）、无 SFT 时 RL 会放弃压缩（Memento）、agent 会靠重读补偿被丢内容（白名单外实证）→ 被忽视的是：结果奖励只能惩罚"执行器无法补回的损失"，而主流训练环境保留初始 prompt、语料可重读，几乎没有这类损失 → RBC 在压缩边界阻断重获取，用兄弟 summary 的续写差异只为 summary 记功 → 若成立，summary 增益可在换回训练前 actor 时保留、无 SFT 也不放弃压缩、中途约束保留提升；若阻断后兄弟差异仍不显著或成功率下降，则该解释被推翻。
- 打分理由：机制统一且可推翻，有现成环境；有效性依据多为相邻证据与白名单外实证。
- Idea 生成依据：来自问题卡 Q001（CompactionRL、Memento、AdaCoM、MemoryWalker、ECHO）；地图 Q005（训练式 compaction 是否保护不可恢复信息）、Q006（benchmark 可重读、agent 补偿重读）；PAIR 2609.36526；TRACE 2608.06503。
- 自评分轻量新意依据：网页检索 2 次 + 摘要核对：ReSum-GRPO/SUPO/Cursor 广播优势，CompactionRL 用 critic，FoldGRPO 用启发式过程奖励（未折叠 token、越界、工具失败；原文 §2.3.2 已核），MMPO（2605.30159）用 belief entropy，TRACER（2608.29363）用学习的结果模型训练保留比例且冻结执行器；未见以"阻断重获取"隔离 summary 信用的工作，需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把"执行器可重获取"识别为结果式 compaction RL 中 summary 信用失效的共同原因，并用阻断重获取的边界兄弟续写构造只属于 summary 的信用。
- 关键数据与评价对象：BrowseComp-Plus 公开 830 个查询与约 10 万文档固定语料、qrels（GitHub texttron/BrowseComp-Plus，已核仓库含 data/、searcher/、topics-qrels/）；已观察文档 ID 由本地检索服务记录，阻断即对已返回过的 doc ID 返回占位符。训练查询需另取（FoldAgent 训练数据或合成多跳问题，覆盖待核）。中途约束评测需新建：在随机回合注入可程序校验的用户约束（如排除某来源、答案格式），以模板生成，人工成本低，约束类型覆盖待定。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 复现依据与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 摘要式上下文管理 + GRPO 广播优势（ReSum-GRPO / SUPO） | 同任务同 harness 的标准做法 | ReSum 2509.13313；SUPO（Lu et al. 2025, ACL 2026） | 算法规则明确（优势广播到所有段）；ReSum 推理代码在 Alibaba-NLP/DeepResearch/WebAgent/WebResummer（训练代码未核） | 在 FoldAgent/verl 中实现分段 rollout 与广播优势 | 是 |
| CompactionRL 式 critic + 跨段 GAE | 同类联合训练最强近邻 | 2607.05378 §3–5 | 未找到代码；论文给出 token 级 loss 归一化与跨段 GAE 规则，计划按公开规范独立复现，折扣细节为未定选择 | verl PPO + 自定义 GAE | 是（算力不足时降为单次） |
| 无阻断兄弟分叉（IDEA-002） | RBC 的直接消融 | 本候选 | 标准规则 | 与 RBC 同代码，仅去掉阻断 | 是 |
| FoldGRPO 过程奖励 | 同环境上下文管理 RL | 2510.11967 §2.3.2（已核三项奖励规则） | 官方代码 sunnweiwei/FoldAgent（已核目录） | 原仓库 | 否（不同上下文操作=分支折叠；作为相关工作与可选对照） |
| Memento 式 SFT 冷启动 + RL | 回答"无 SFT 放弃压缩"的对照 | 2611.00244 §4.2.1 | 未核代码；规则：事后标注 note 的合成轨迹 SFT | 用本地 72B 模型生成事后 note | 是（只在可选压缩实验中） |

- Reviewer 记录：Call 1（常规，同模型 high）：5.5/10（重要性 6.5 / 新颖度 5.5 / 有效性 5.5），promising_needs_revision；最高近邻 TreeMem 2605.04811、DSSR 2609.32805、2610.31778、CompactionRL、PAIR/TRACE。阻断：新意只剩“续写阻断”；“子目标命中”标签未定义；支持判据只有非劣、推翻判据混淆方法与解释；缺 ECHO/Self-Credit/MMPO/InfoMem 对照。子 Idea：IDEA-006。

### IDEA-005：自我压缩是一场自通信博弈——共适应导致 summary 读者专属

- 来源：`相似领域成熟方法迁移`（emergent communication 中的 language drift 与 population training）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：context compaction；language drift；emergent communication；co-adaptation
- 一句话背景：同一策略既写 summary 又读 summary，结果奖励下可能形成只有自己读得懂的压缩协议。
- 与起点问题的关系：原问题中"配对能否迁移"子问题。
- 主贡献：检验 compaction RL 后 summary 对其他读者（训练前模型、其他模型）的可用性是否下降，并用多读者奖励抑制。
- 贡献自评：重要性 6.5 / 新颖度 6.5 / 有效性 5；KL 约束下文本 summary 是否会漂移缺直接证据。
- 可行性：pass。
- 自评分：`5.9/10`
- 一段话概括：用交换读者测量漂移，用读者群体奖励修正。
- 打分理由：视角新但效果依据弱。
- Reviewer 记录：尚未送审

### IDEA-006：使用时刻的保留目标事后重标注（跨多次重写的 writer 信用）

- 来源：`领域共性不足`（前滚/分叉式 summary 信用的共同局限）+ `相似领域成熟方法迁移`（hindsight experience replay 的事后重标注）
- 父 Idea：`IDEA-004`
- 状态：`covered`
- 定位关键词：write-time regret；decision-sufficient state；context compaction；credit assignment；TextWorld
- 一句话背景：恒定上下文 agent 的 writer 反复重写状态，而一个事实被丢后往往要隔多次重写才在决策时暴露，现有 writer 训练信号看不到这种跨重写的保留价值。
- 与起点问题的关系：子问题；保留“结果式训练中 summary 内容得不到有效信用”这一核心，把对象收窄到“跨多次压缩才被需要的信息”的信用分配，并先在固定 reader 的受控环境中检验，再到联合训练的深度搜索 agent；起点中“增益来自哪边”通过 2×2 交换部分回答，“跨模型族迁移”与“为何回避可选压缩”仍未回答。
- 主贡献：一种与延迟长度无关的 writer 训练信号：在 reader 决策失败的时刻，用恢复反事实（把已丢弃的原始观察逐段放回 reader 上下文，看参考动作的似然是否显著回升）找出“本可改变决策的已丢事实”，再回到该事实出现之后、被需要之前的每一个写入点，把保留它的候选标为更优，用于偏好训练。相当于从经验中学出 DSSR 中手写的“该保留什么”规则，而不依赖任务知识。可重读环境里，重读已见文档是同一信号的免费版本。（送审前细化：由“只对最早丢弃点施加负信用”改为“对整条携带链做事后重标注”，依据 DSSR §4/§5.6：延迟下多数后续写入点已无含该事实的候选，单点归责不足。）
- 贡献自评：重要性 7 / 新颖度 7.5 / 有效性 6.5。依据：DSSR 显示损失几乎全是写入 regret 且随延迟增长，其前滚训练只在最短延迟显著，作者把原因归为“跨重写信用”，而一条手写的“保留什么”规则在每个延迟都更好——说明问题出在信用而非容量；恢复反事实已被用于区分不可逆驱逐损失（2609.08279，白名单外，评测用途）；Self-Credit/ECHO 在 BrowseComp-Plus 上证明基于来源的信用改善 agent RL；重读补偿在 SWE agent 中普遍（2610.35496）。未知：恢复搜索的噪声与成本；只给负信用是否导致保留过多（需长度项）；训练到的保留是否泛化到未见游戏/任务。
- 可行性：pass（TextWorld 开源；DSSR 匿名代码已核含 env/dssr/configs/checkpoints；Qwen3-4B LoRA 单卡可复现；BrowseComp-Plus 联合训练用 Qwen3-8B）。
- 自评分：`7.0/10`
- 一段话概括：Claim——前滚/分叉式 summary 信用无法学到“需跨多次重写保留”的信息，而在使用时刻反向定位丢弃点的归责信用可以：在 DSSR 的可控延迟 TextWorld 上，它在 DSSR 失败的长延迟下提高胜率、缩小与手写保留规则的差距；在带压缩的 BrowseComp-Plus 联合 RL 中，同准确率下减少重读次数与总 token。最小实验：DSSR 协议（固定 reader，只训练 writer）对比 DSSR、结果广播、本方法与手写规则，按延迟分层；BrowseComp-Plus 上 Qwen3-8B 对比广播优势 GRPO 与本方法（另含 Self-Credit 或 ECHO 一项），报告准确率、重读次数、总 token 及 2×2 交换。
- Story line：DSSR 在可控延迟下发现写入 regret 随延迟增长、其前滚训练只在短延迟有效，作者归因于跨重写信用；CompactionRL 消融显示联合训练增益主要不靠 summary；agent 普遍以重读补偿 → 被忽视的是：信息被需要的时刻本身就暴露了“哪次重写丢错了”，可以直接把信用送回丢弃点，无需让前滚跨越多个重写 → 本 Idea 在使用时刻用恢复反事实或重读事件定位被丢信息，沿重写链归责到最早丢弃它的重写 → 若长延迟胜率提升、重读减少且准确率不降，则说明跨重写信用是瓶颈且可解；若归责信用在长延迟下仍无增益，则说明瓶颈在 writer 表达能力或泛化，而非信用。
- 打分理由：直接针对近邻作者自述的未解局限，受控环境与官方代码现成，有效性依据为相邻证据。
- Idea 生成依据：DSSR 2609.32805（摘要与 §5.6 标题、引言已读）；TreeMem 2605.04811；ECHO 2606.31650 §2.2–2.3（抽取式来源路由）；Self-Credit 2610.28388；2609.08279 恢复反事实；2610.35496；来自问题卡 Q001。
- 自评分轻量新意依据：已读近邻中，DSSR/TreeMem/PAIR 用前向续写，ECHO 用抽取式轮次索引，Self-Credit 给被引用的动作轮次记功，TRACER 把重调用作为每工具保留比例的代价项（冻结执行器、学习的结果模型）；未见在使用时刻反向归责到抽象式重写链中丢弃点的训练方法，需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：用“使用时刻暴露的丢失”反向定位丢弃它的重写并只对其记功，使 summary 信用与延迟长度无关。
- 关键数据与评价对象：TextWorld 烹饪游戏与 DSSR 的延迟构造（匿名代码 env/、configs/ 已核目录；游戏统计见其附录 A，未细读）；被需要的事实由恢复反事实识别，无需特权标签；呈现检查用模板化事实串匹配（TextWorld 事实由模板生成）。BrowseComp-Plus：文档 ID 固定，重读即同一 doc ID 二次返回，检索服务可直接记录；“summary 是否仍包含该文档信息”的判定需定义（文档 ID 提及或关键句重叠，覆盖待验证）。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 复现依据与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| DSSR 前滚打分 + 偏好训练 | 同环境同协议最强近邻 | 2609.32805 §4–5 | 匿名代码 anonymous.4open.science/r/AgentDSSR（已核目录含 dssr/env/configs/checkpoints） | 原仓库原配置 | 是 |
| 结果广播（writer 用游戏胜负 GRPO） | 标准结果式信用 | 规则明确 | 标准算法 | 同 writer LoRA，奖励=胜负 | 是 |
| 手写保留规则 | DSSR 报告的上参照 | 2609.32805 | 随 DSSR 代码/提示 | 原仓库 | 是（参照，非竞争） |
| 摘要式管理 + GRPO 广播（ReSum/SUPO） | BrowseComp-Plus 联合训练标准做法 | 2509.13313；SUPO | 规则明确，独立实现 | verl/FoldAgent 环境 | 是 |
| Self-Credit | BrowseComp-Plus 上 Qwen3-8B 信用分配强基线 | 2610.28388 | 代码未核；摘要给出三组件规则 | 按公开规范独立复现，未定选择待读正文 | 是（二选一，与 ECHO） |
| ECHO | 同上，来源路由信用 | 2606.31650 | 代码未核 | 同上 | 备选 |

- Reviewer 记录：Call 2（常规，同模型 high）：4.5/10（重要性 6 / 新颖度 5 / 有效性 5），needs_rethink；最高近邻 DSSR 2609.32805（§7 已点名该修补方向）、HiMPO 2606.16285（事后记忆专属辅助优势 + 回传，含 BrowseComp-Plus；本人已读摘要核实）、TRACER、2609.08279、Self-Credit。阻断：A 是 DSSR 自述方向的直接实例；B 被 HiMPO 覆盖；本人误述 DSSR 手写规则“每个延迟都更好”（仅 regret 上成立，胜率上不成立——摘要原句与表格口径不同，未核表）；缺模板 recipe 直接构造偏好对的对照与 GRPO+重读惩罚对照。
