# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系。
> 独立放行要求三项都 ≥6、至少两项 ≥8、可行性通过；自评只用于排序。

- 输入模式：`raw_idea`
- 输入论文：不适用
- 输入问题卡：不适用

## 当前选择

- Reviewer 调用：`3 / 10`（用户 2026-11-03 追加 4 次）
- 当前选中 Idea：`IDEA-011`
- 当前自评分：`7.0/10`
- 选择理由：IDEA-009 Call 2 未过（7/6/5），主要竞争解释是 C-MTP 自己提出的冗长性；IDEA-010 被 SLT（2605.25745）覆盖；IDEA-011 直接解释 C-MTP 报告但未解释的崩塌，且指出其结构化/半自然（GSM8K）与真实（MATH）设置混入了题目难度，是池中重要性与新意兼顾的最高候选。
- 状态：`已停止（rejected_no_viable_candidate），用户选择改做研究地图；见 PIVOT_OR_STOP.md`

## 候选列表

### IDEA-001：CoLaR 的 latent CoT 是一个短记忆 RNN（现象刻画）

- 来源：`原始想法`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：continuous latent reasoning；latent chain-of-thought；attention；causal intervention
- 一句话背景：连续 latent CoT 中各 latent 承担什么作用、如何传递信息，是 latent 推理可解释性的问题。
- 与起点问题的关系：原问题；直接整理现有注意力与置零证据。
- 一段话概括：把已有的尾部注意力、链尾联合置零和生成局部性整理成"CoLaR latent CoT 等价于二阶短记忆循环"的现象论文。
- 贡献自评：重要性 5 / 新颖度 4.5 / 有效性 5.5。近邻 2602.08783（ICML 2026）已对 Coconut/CODI 做逐步因果结构研究，2607.09698 已用动力系统刻画 latent CoT，MarCos（2509.25020）把 Markov 式连续思维做成架构；仅凭注意力与置零，无法排除"最后一条算式写着答案"的版式继承解释。
- 可行性：pass（数据已有）。
- 自评分：`4.8/10`
- 打分理由：贡献分量不足，核心竞争解释未处理。

### IDEA-002：跨训练范式的"历史窗口因果检验"——接力式 vs 寻址式 latent CoT

- 来源：`领域共性不足`
- 父 Idea：`IDEA-001`
- 状态：`available`
- 定位关键词：continuous latent reasoning；Coconut；CODI；CoLaR；causal intervention
- 一句话背景：不同 latent CoT 训练范式的步间信息传递结构结论不一致：2602.08783 报告 Coconut/CODI 以跳连为主、比显式 CoT 更不局部，而 CoLaR 上观察到近窗口局部。
- 与起点问题的关系：子问题；把单模型现象扩展成跨范式的对比，原问题的成因（版式还是机制）仍未回答。
- 一段话概括：推理时把 latent 生成位置与答案位置的注意力限制在"题目 + 最近 W 个 latent"，测正确率随 W 的保留曲线，在 CoLaR（EQ/NL）、CODI-Llama-1B 官方权重、同底座显式 CoT 上比较，以此把"注意力局部"变成因果层面的有效窗口，并调和上述分歧。
- 贡献自评：重要性 6 / 新颖度 6.5 / 有效性 6。依据：CoLaR 已有生成局部性与链尾置零证据；Coconut 本机分析显示寻址式（l2/l5 存步骤结果）。未知：调和分歧本身的分量；窗口差异可能仍由监督版式决定。
- 可行性：pass（只需推理时注意力掩码，权重已有）。
- 自评分：`5.8/10`
- 打分理由：能判别"窗口是否因果必要"，但不能回答成因，主贡献偏描述。

### IDEA-003：依赖距离是 latent CoT 的失败轴（接力瓶颈）

- 来源：`领域共性不足`
- 父 Idea：`IDEA-001`
- 状态：`needs_revision`
- 定位关键词：latent chain-of-thought；GSM8K；multi-step reasoning；implicit reasoning
- 一句话背景：latent CoT 在多步数学题上落后显式 CoT，失败随步数增加。
- 与起点问题的关系：子问题；用局部窗口机制预测哪些题失败。
- 一段话概括：若生成只看最近 2–3 个 latent，那么需要远处中间结果的题应更容易错；按 gold 算式依赖图算依赖距离，在固定步数下比较正确率，并用拓扑重排训练数据来缩短依赖距离。
- 贡献自评：重要性 6 / 新颖度 6 / 有效性 3。**本次离线重统计与之相反**：固定步数后，长依赖题与局部依赖题正确率无一致差异（EQ 3 步 0.35 vs 0.34，4 步 0.16 vs 0.10）；而且仅约 23% 的长依赖题能通过重排降低总依赖距离。
- 可行性：pass。
- 自评分：`3.8/10`
- 打分理由：关键前提被现有记录削弱，降为 needs_revision。

### IDEA-004：接力还是版式继承——用监督版式操控做因果检验，回答 latent CoT 是否是"特殊 RNN"

- 来源：`领域共性不足`（竞争解释的判别），机制上借 `相似领域成熟方法迁移`（循环网络的"插入空步/延迟"检验）
- 父 Idea：`IDEA-001`、`IDEA-002`
- 状态：`needs_revision`
- 定位关键词：continuous latent reasoning；latent chain-of-thought；CoLaR；causal intervention；GSM8K-Aug
- 一句话背景：连续 latent CoT 可解释性研究中，latent 链中信息存放在哪、如何在步间传递，目前只有观察性分析和单模型干预，且不同方法的结论相互矛盾。
- 与起点问题的关系：原问题；保持 CoLaR、GSM8K-Aug、Llama-3.2-1B 不变，把"像 RNN"变成可证伪的因果命题；跨族对比（CODI）作为次要检验。
- 主贡献：把"latent CoT 像特殊 RNN"拆成两个可分别检验的命题：(a) 读出位置由监督版式决定（版式继承）；(b) 生成是只携带短窗口状态、每一跳都有代价的接力。通过训练时操控监督版式（链尾加无信息填充、步骤之间插无信息填充），给出这两个命题各自是否成立的因果证据，并说明 latent CoT 的长度/压缩设计与解释研究应依据哪一种机制。
- 贡献自评：重要性 6.5 / 新颖度 6.5 / 有效性 6。依据：链尾即最后算式（答案）所在；Coconut 的关键 latent 与 CoT 节奏对齐（约 2.5 latent/步）；同底座 NL 链长约 2.7 倍、正确率 18.4% vs 28.6%（存在数据形式混杂）。未知：版式操控是否会被模型以其它方式吸收；无信息填充可能改变训练难度。
- 可行性：pass。CoLaR 每个变体单卡 L40 约 2 天（已有日志：约 1.1 h/epoch，约 46 epoch），可在 A100 上并行；推理时注意力掩码与置零脚本已有。
- 自评分：`6.0/10`
- 一段话概括：在相同 CoLaR 配置下训练三种监督版式：V0 原始；V1 在最后算式之后加固定的无信息填充（约 2 个 latent 长）；V2 在每两步算式之间插同样长度的填充（只加跳数，不加信息）。用推理时历史窗口掩码（题目 + 最近 W 个 latent）、链尾/窗口置零和 latent–token 对齐来测读出位置与有效窗口。版式继承预测：V1 的关键位置随最后算式前移、填充尾部可删；接力预测：V1 的填充尾部会接过答案状态，V2 的正确率随插入跳数下降。同底座显式 CoT 与 CODI-Llama-1B 官方权重用同一窗口检验作对照。
- Story line：CoLaR 上答案读链尾、生成看近窗，被直观理解为"特殊 RNN"；但链尾恰好是最后算式（答案）所在，而在 Coconut 上关键 latent 与 CoT 节奏对齐、2602.08783 在 Coconut/CODI 上还发现了非局部跳连，所以当前证据分不开"机制"与"版式"；本 Idea 只改监督版式、不改信息内容，看读出位置和有效窗口是否随之移动；若 V2 只加跳数就伤正确率，则"接力代价"成立，可推出 latent 链应少而密、并能用有界历史推理；若读出位置随版式移动，则一批 latent 可解释性结论应被视为监督版式的产物。
- 打分理由：唯一能因果判别两种解释的候选；但"这对领域有多重要"仍取决于结论能否改变设计，重要性未必到 8。
- Idea 生成依据：服务器 `analysis/nl_vs_eq_*`、`latent_generation_locality`、Coconut `latent_contribution`；2602.08783（skip-dominant influence）；2607.09698（dynamical systems）；2509.25020 MarCos；2510.06557 Markovian Thinker；CoLaR 2505.16552。
- 自评分轻量新意依据：检索"latent CoT 局部性/Markov/置零/版式"未见在训练时操控监督版式来检验 latent 信息位置的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：用"只改版式、不改信息"的监督操控，加上推理时的有效窗口掩码，因果地拆开 latent CoT 中"版式继承"与"短窗口接力"两种机制。
- 关键数据与评价对象：GSM8K-Aug（服务器 `datasets/text_reasoning/gsm8k_aug/{train,val,test}.json`，`steps` 字段是 `<<a*b=c>>` 算式列表，已核对样例）；填充版式通过修改 `steps` 拼接字符串离线生成，无需人工标注。latent–token 对齐由 CF5 下第 i 个 latent 对应第 5i..5i+4 个 CoT token 给出（CoLaR 压缩规则）。评价对象：原本正确题的保留率、整体正确率、注意力窗口占比。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 复现依据与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| CoLaR 原版式（V0） | 同任务同模型 | 2505.16552；服务器 colar 代码 | 已有用户训练的 EQ checkpoint 与训练脚本 | 复用 `fixed_shift_all_valid_token_ce_clean` 配置；另用官方未改代码 yuan checkpoint 作敏感性 | 是 |
| 同底座显式 CoT | 同数据同底座，检验局部性是否从文本继承 | CoLaR 仓库 CoT 阶段 | 服务器 `runs/full_cot_gsm8k_aug_*/checkpoints` 存在 | 把注意力按 5 token 聚块，用同一窗口掩码 | 是 |
| CODI-Llama-3.2-1B | 另一训练范式（隐藏态蒸馏），同底座 | 2502.21074；`zen-E/CODI-llama3.2-1b-Instruct` | 服务器 codi 仓库含 `test_llama1b.sh`，README 列出权重 | 推理时窗口掩码；不重训 | 是（次要） |
| 2602.08783 因果影响图 | 最高近邻测量方法 | github J1mL1/causal-latent-cot（ICML 2026，已核验存在） | 公开代码 | 在 V0/V1/V2 上算 locality/span 指标，便于与其结论对齐 | 是 |

- Reviewer 记录：`Call 1（常规，Opus 5.5 high）：5.3/10（重要性 5.5 / 新颖度 6.0 / 有效性 5.0，可行性 pass），promising_needs_revision；最高近邻 2602.08783、2606.12689、2602.22441、SIM-CoT 2509.20317、2512.21711`
- 审阅要点（主执行者已直接读 2606.12689 与 2602.22441 核对）：H1 几乎由 CoLaR 逐块压缩监督直接蕴含；H2 与依赖距离零差异反证冲突；V2 的下降与训练难度、分块对齐、总长度混杂；"观察模式需匹配对照"已由 2606.12689 确立（该文公开了 Llama-3.2-1B / GSM8K-Aug 的 Coconut、CODI、CoT、Pause 权重，可作将来对照）；2602.22441 已把 CoLaR 作为强监督代表研究 shortcut 与监督强度的权衡。

### IDEA-005：滚动展开训练修正 latent 接力的误差累积

- 来源：`相似领域成熟方法迁移`（神经 PDE 代理模型的 pushforward / 多步展开训练）
- 父 Idea：`IDEA-001`
- 状态：`available`
- 定位关键词：latent chain-of-thought；exposure bias；scheduled sampling
- 一句话背景：latent CoT 训练用 teacher forcing，推理时自回归展开，存在误差累积。
- 与起点问题的关系：邻近新问题。
- 一段话概括：若 latent 生成是短记忆递推，就借鉴代理模型的多步展开损失，在训练时用模型自己生成的前序 latent（stop-grad）去监督后续 latent。
- 贡献自评：重要性 6 / 新颖度 4 / 有效性 5。与 2606.20075（manifold drift）、Diffusion of Thoughts 的 scheduled sampling、CoLaR 自身的 RL 阶段重叠。
- 可行性：pass。
- 自评分：`4.8/10`

### IDEA-006：有界历史 latent 解码（只保留题目 + 最近 W 个 latent 的 KV）

- 来源：`相似领域成熟方法迁移`（Markovian Thinker / 滑窗注意力）
- 父 Idea：`IDEA-001`
- 状态：`available`
- 定位关键词：latent reasoning；Markovian thinking；sliding window attention
- 一句话背景：推理链的显存开销随长度增长。
- 与起点问题的关系：邻近新问题。
- 一段话概括：利用生成局部性，推理时丢弃较早 latent 的 KV。
- 贡献自评：重要性 3.5 / 新颖度 4 / 有效性 6。CoLaR 链只有 5–20 个 latent，节省可忽略；Delethink 与 MarCos 已覆盖思路。
- 可行性：pass。
- 自评分：`4.0/10`

### IDEA-007：监督粒度决定 latent CoT 的路由形态（局部接力 vs 非局部跳连）

- 来源：`领域共性不足`（2602.08783 的非局部结论与 CoLaR 局部现象之间的分歧）
- 父 Idea：`IDEA-004`
- 状态：`available`
- 定位关键词：continuous latent reasoning；Coconut；CODI；CoLaR；supervision
- 一句话背景：不同 latent CoT 范式的步间影响结构结论相反，2602.22441 显示监督强度影响 shortcut 与多假设保持。
- 与起点问题的关系：子问题。
- 一段话概括：用 2606.12689 公开的同底座 Coconut/CODI/CoT/Pause 权重加上 CoLaR，在同一套因果窗口检验下比较路由局部性，检验"监督越逐块，路由越局部"。
- 贡献自评：重要性 5.5 / 新颖度 5.5 / 有效性 5.5。与 2602.22441（监督强度）、2602.08783（locality/span）高度相邻，属于再测量。
- 可行性：pass（权重全部公开，无需训练）。
- 自评分：`5.2/10`

### IDEA-008：结果对齐的压缩边界（尾部信息分散的修法）

- 来源：`最高近邻不足`（CoLaR 固定 c 个 token 分块）
- 父 Idea：`IDEA-001`
- 状态：`needs_revision`
- 定位关键词：CoLaR；compression factor；latent chain-of-thought；GSM8K
- 一句话背景：CoLaR 以固定 c 个 token 的均值作为 latent 目标，CF5 比 CF2 低约 13 个百分点。
- 与起点问题的关系：邻近新问题（从现象转向压缩方法）。
- 一段话概括：链尾单点置零冗余、联合置零崩塌，提示最后算式与答案数值被固定分块切到 2–3 个 latent 里；改为在平均压缩率不变的前提下，按算式/数值边界分块。
- 贡献自评：重要性 6 / 新颖度 5 / 有效性 4.5。尾部"分散"也可由版式解释，缺少分块边界伤害精度的直接证据；与 LightThinker、按步 latent（SIM-CoT 等）思路相近；与用户已有 step-packed 方向可能重叠。
- 可行性：pass。
- 自评分：`4.9/10`

### IDEA-009：近窗循环 + 马尔可夫充分的状态监督——让 latent CoT 在自然/真实长 CoT 上不再崩塌

- 来源：`领域共性不足`（多方法在真实长 CoT 上崩塌）+ `相似领域成熟方法迁移`（Markovian Thinker 的有界状态推理；RNN/状态空间模型的充分状态）
- 父 Idea：`IDEA-004`
- 状态：`needs_revision`
- 定位关键词：continuous chain-of-thought；latent reasoning；GSM8k-Aug-NL；MATH；process supervision；Markovian thinking
- 一句话背景：连续 latent CoT 在结构化短轨迹（GSM8k-Aug）上接近 CoT-SFT，但在自然语言、真实长 CoT（MATH，约 350 token）上，直接监督与间接监督方法都会跌到 CoT-SFT 的约 35%（C-MTP 2607.16972）。
- 与起点问题的关系：子问题 + 邻近新问题；保留"生成只看近窗"这一现象及 CoLaR EQ/NL 证据，把目标从"解释 CoLaR 链尾"换成"解释并修复 latent CoT 在自然/长 CoT 上的崩塌"；原问题中"版式继承 vs 接力"仍未直接回答。
- 主贡献：(1) 现象：在不同 trace 格式与方法家族中，latent 生成的有效历史窗口固定在少数几个 latent 上（以推理时窗口掩码因果测定）；在逐块/逐步模仿文本的监督下，近窗里放的是表层文本，不是推理状态，所以长 trace 上较早的结论会被丢掉。(2) 方法：把监督目标从"下一块文本或当前步文本"换成"到目前为止的紧凑累积状态"（已得出的中间量/事实），让近窗变成马尔可夫充分；该辅助目标可接到 C-MTP/CoLaR 与 CODI 两类方法上。
- 贡献自评：重要性 7.5 / 新颖度 6.5 / 有效性 6。依据：CoLaR 在 EQ 与 NL 上近窗占比几乎相同（同题同步骤 80.5% vs 78.2%），窗口按 latent 计而不是按步计；Delethink（2510.06557）显示，只要模型被训练去携带状态，有界状态就足以支撑长推理（文本域类比）；Coconut/PMPS 的 logit lens 显示 latent 能承载中间量。未知：辅助解码可得不等于被使用（2606.12689）；单个向量能否装下长 MATH 轨迹的累积状态；近窗在 C-MTP/CODI 上是否同样成立尚未测。
- 可行性：pass。C-MTP 仓库（Varun221/cmtp_research）含 cmtp/、codi/、data_math/ 生成真实轨迹的脚本；SIM-CoT 官方实现（InternLM/SIM-CoT，ICLR 2026）提供逐步辅助解码器；GSM8k-Aug-NL 已在服务器；MATH 状态抽取用 API，约 7.5k 题 × 若干条轨迹，预计 <200 元。
- 自评分：`6.6/10`
- 一段话概括：先在 CoLaR(EQ/NL)、C-MTP、CODI 上用推理时历史窗口掩码测有效窗口，并用探针测"较早得出的中间量是否还能从近窗读出"，跨 Structured / Semi-Natural / Realistic(MATH) 三类 trace。再在相同底座（Llama-3.2-1B）、相同 latent 数、相同辅助解码器下，只把辅助目标从"当前步文本"（SIM-CoT 式）或"累积文本前缀"换成"紧凑累积状态"，比较 GSM8k-Aug-NL 与 MATH 真实轨迹上的正确率。
- Story line：latent CoT 在真实长 CoT 上崩塌（C-MTP）→ 现有修法都在改监督如何对齐文本（逐步重建、原型对齐、预测未来步），但没有处理 latent 生成只读近窗这一事实 → 若窗口固定，长 trace 上早期结论必须靠表层文本块接力，必然逐跳丢失 → 本 Idea 让每个 latent 携带累积状态，使近窗本身充分 → 预期在长/自然 trace 上缩小与 CoT-SFT 的差距，在结构化短 trace 上与现有方法持平；若累积状态监督不优于等长的当前步重建，则假说被推翻。
- Idea 生成依据：服务器 CoLaR 局部性/链尾分析；C-MTP 2607.16972；SIM-CoT 2509.20317；2606.20075（轨迹/空间监督分类）；2608.14107（累积前缀重建，检索域）；Delethink 2510.06557；MarCos 2509.25020；PMPS 2609.09928；2606.12689。
- 自评分轻量新意依据：检索"latent CoT 状态/中间量监督"未见以结构化累积状态为目标的工作；最近的是 2608.14107 的累积文本前缀重建（检索任务）与 2606.20075 的未来步预测；需要 reviewer 检索。
- 关键数据与评价对象：GSM8k-Aug-NL（服务器已核对样例，每句对应一步算式，可直接由算式结果构造状态 "9; 18"）；MATH 真实轨迹由 C-MTP 的 data_math 脚本用底座模型生成，状态由 API 按步抽取（输入：轨迹分句；输出：截至该步已确立的中间结论列表），覆盖率与抽取错误率需抽检 200 条。评价：GSM8K/GSM-Hard/MATH 测试正确率；窗口保留率；早期中间量的探针可读率。
- Baseline 可复现性：

| Baseline | 与目标任务的关系 | 论文或规范 | 复现依据与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| CoT-SFT | 同底座上界 | C-MTP 仓库 | 已核验仓库 `cmtp/test_cot.py` | 按其脚本 | 是 |
| C-MTP | 直接监督（逐块均值，CoLaR 类） | 2607.16972 | 已核验 `cmtp/train.py` | 原配置 | 是 |
| CODI | 间接监督 | 2502.21074；C-MTP 仓库 `codi/` | 已核验目录 | 原配置 | 是 |
| SIM-CoT | 当前步文本重建 | 2509.20317；InternLM/SIM-CoT | 已核验仓库（CODI/、Coconut/） | 与本方法共用解码器与 latent 数，只换目标 | 是（关键对照） |
| 累积文本前缀重建 | 控制"累积 vs 紧凑" | 2608.14107 规范 | 无同任务代码，按规范独立实现（把目标换成前 k 步文本拼接） | 同上 | 是 |

- Reviewer 记录：`Call 2（常规，Opus 5.5 high）：5.5/10（重要性 7 / 新颖度 6 / 有效性 5，可行性 pass），promising_needs_revision；最高近邻 SIM-CoT、RGLT 2608.14107、Thinking States 2602.08332、C-MTP 2607.16972、MCoT 2410.17635 / Delethink`
- 审阅要点：长轨迹上"早期结论经近窗丢失"无直接证据；C-MTP 中 SIM-CoT 同样崩塌，冗长性挤占容量是更强的竞争解释；缺"紧凑当前步状态"对照。

### IDEA-010：信息自适应分块的 latent 压缩（熵切分，借 BLT/DLCM）

- 来源：`相似领域成熟方法迁移`（Byte Latent Transformer 熵切分；DLCM/H-Net 动态分块）
- 父 Idea：`IDEA-009`、`IDEA-008`
- 状态：`covered`
- 定位关键词：latent reasoning；CoLaR；compression factor；dynamic chunking
- 一句话背景：直接监督 latent CoT 按固定 token 数压缩，冗长轨迹的信息密度极不均匀。
- 与起点问题的关系：邻近新问题。
- 一段话概括：按 CoT 教师的 token 熵/惊异度定 latent 边界，平均压缩率不变。
- 贡献自评：重要性 7 / 新颖度 4.5 / 有效性 6。SLT（2605.25745）已证明"压哪段至关重要、数值保留显式"，并在 latent 模型内加学习式压缩门控；DLCM、ConceptMoE 已在预训练做信息密度动态分块。
- 自评分：`5.0/10`

### IDEA-011：latent CoT 在真实轨迹上崩塌，是冗长、难度、误差累积，还是近窗丢失？——同题内容等价的冗长度阶梯诊断

- 来源：`领域共性不足`（C-MTP 报告直接/间接监督都在真实轨迹上崩塌但未解释；SIM-CoT 同样崩塌）
- 父 Idea：`IDEA-009`
- 状态：`needs_revision`
- 定位关键词：continuous chain-of-thought；latent reasoning；GSM8k-Aug-NL；MATH；CODI；SIM-CoT
- 一句话背景：C-MTP（2607.16972）发现 latent CoT 在结构化/半自然轨迹（GSM8K）上接近 CoT-SFT，而在真实轨迹（MATH）上只剩约 35%，但结构化与真实两种设置同时改变了轨迹形式和题目来源。
- 与起点问题的关系：邻近新问题；近窗现象成为四个竞争解释之一被检验，CoLaR EQ/NL 证据作为动机；原问题的"版式 vs 机制"不直接回答。
- 主贡献：一个分解：把 latent CoT 相对 CoT-SFT 的崩塌，在同一批题上分解到"轨迹冗长度（内容不变）"、"题目难度"、"自回归 latent 误差累积"、"早期信息经近窗丢失"四个因素，并对每个方法家族给出主导因素；再用主导因素推出的最便宜修法（例如先把真实轨迹凝练成紧凑步骤再训练 latent）做一次干预检验。
- 贡献自评：重要性 7.5 / 新颖度 7 / 有效性 6.5。依据：C-MTP 的设置把难度与轨迹形式混在一起（GSM8K vs MATH）；CoLaR 同题 EQ vs NL（内容相同、NL 长约 2.2 倍）正确率 28.6% vs 18.4%，提示冗长度本身有害；C-MTP 自述间接监督因不必表示每个 token 更适合冗长轨迹；step-entropy（2508.03346）显示显式 CoT 中约 80% 低熵步可删而不掉点，即真实轨迹信息冗余大。未知：LLM 重写能否严格保内容；1B 在 MATH 上的 CoT-SFT 绝对水平（地板效应）；各因素是否交互。
- 可行性：pass。C-MTP 仓库含 cmtp/、codi/、data_math/（轨迹生成与评分脚本）；SIM-CoT 官方实现；重写用 API（约 7.5k MATH + 7.5k GSM8K 子集 × 3 档，预计 <300 元）。
- 自评分：`7.0/10`
- 一段话概括：对 MATH 与 GSM8K 各取同一批训练题，用 C-MTP 的真实轨迹作源，由 LLM 重写成三档内容等价轨迹（紧凑算式步 / 每步一句 / 原真实轨迹），自动校验中间结果与答案一致；在 2（难度）× 3（冗长度）网格上训练 CoT-SFT、C-MTP、CODI、SIM-CoT，并测 teacher-forced 与自由展开的差距、推理时窗口保留与早期中间量探针。以"相对 CoT-SFT 的保留率"为主指标做分解。再用分解指出的主导因素做一次修法干预（如"凝练后再 latent 化"，在原真实轨迹测试分布上评估）。
- Story line：C-MTP 报告 latent CoT 在真实轨迹上掉到约 35%，这是 latent 推理走出结构化 benchmark 的核心障碍 → 但它的对比同时改变了题目来源与轨迹形式，且没有区分冗长、误差累积、信息丢失 → 本 Idea 在同一批题上构造内容等价的冗长度阶梯，做因素分解 → 若冗长度主导，则"凝练后再 latent 化"应收回大部分差距，latent 研究应把轨迹凝练当作一等设计；若难度主导，则现有"结构化 benchmark 高估 latent"的结论需修正；若误差累积或近窗丢失主导，则指向展开训练或状态监督——每种结果都给出可推翻的预测。
- Idea 生成依据：C-MTP 2607.16972；SIM-CoT 2509.20317；SLT 2605.25745；step entropy 2508.03346；服务器 CoLaR EQ/NL 对比与近窗分析；2606.12689（匹配对照）。
- 自评分轻量新意依据：检索"latent CoT 在长/真实轨迹上失败的受控分解（冗长 vs 难度）"未见；需 reviewer 检索。
- 关键数据与评价对象：MATH 训练/测试（C-MTP data_math 脚本生成与评分）；GSM8K-Aug 与 GSM8k-Aug-NL（服务器已有）。重写校验：每条重写须保留源轨迹的全部中间数值与最终答案（自动比对），并以 CoT-SFT 在各档上的准确率作内容保真对照；抽检 200 条人工核对。
- Baseline 可复现性：同 IDEA-009 表（CoT-SFT、C-MTP、CODI 来自 C-MTP 仓库；SIM-CoT 官方实现）。
- Reviewer 记录：`Call 3（常规，Opus 5.5 high）：5.5/10（重要性 6.5 / 新颖度 6 / 有效性 5.5，可行性 pass），needs_rethink；最高近邻 C-MTP 2607.16972、KaVa 2510.02312、2602.22441、2602.01148、2606.21704`
- 审阅要点：C-MTP 4.3/4.5 节与附录 G.7（CSQA 反例）已给出压缩压力、误差累积两种解释；C-MTP 表 2/4 中 CODI 相对 CoT-SFT 的保留率在算式版约 86%、NL 版约 89%，CoLaR-2 从约 66% 降到 44%，即冗长只伤直接监督；MATH 对比还混入训练规模（385k vs 约 7.5k 且只保留答对轨迹）和"CoT-SFT 分母等于未训练底座"；KaVa 已针对 NL 退化提出压缩 KV 蒸馏。
