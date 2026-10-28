"""主执行器写入已通过方案；这些段落是具体研究计划，不执行实验。"""
import json
import 候选管理 as m

def expand(cid, glossary, intro, method, experiment, followup, risks, refs):
    c=next(x for x in m.load() if x['id']==cid)
    r=c['reviews'][-1]
    if not (c.get('selected_was_pool_leader') and r['score']>7.5 and not r['fatal_blockers']):
        raise ValueError('不能展开未通过候选')
    heading=['任务锚点与最小范围','现有方法怎样处理','具体瓶颈与证据边界','我们实际做什么','最小实验概览','拟验证贡献']
    text='## 术语与缩写表\n\n'+glossary+'\n\n## Title\n\n# '+c['title']+'\n\n'
    text+=f'**候选ID：** {cid}。**独立审查：** Call{r["call"]}，{r["score"]}/10，experiment_ready，无致命阻塞。未运行模型实验。\n\n'
    text+=f'**定位关键词：** {c["keywords"]}。\n\n**一句话背景：** {c["background"]}\n\n**独立创新点：** {c["independent"]}\n\n## 1. 引言式概述\n\n'
    for i,(h,b) in enumerate(zip(heading,intro),1):text+=f'### 1.{i} {h}\n\n{b}\n\n'
    text+='## 2. 详细方法计划\n\n'
    for i,(h,b) in enumerate(zip(['方法直觉','输入、输出与成立条件','算法与数据流','最小实现与算力'],method),1):text+=f'### 2.{i} {h}\n\n{b}\n\n'
    text+='## 3. 最小验证实验\n\n'
    for i,(h,b) in enumerate(zip(['目的','数据与切分','Baselines（唯一实验baseline定义）','指标','支持和失败条件'],experiment),1):text+=f'### 3.{i} {h}\n\n{b}\n\n'
    text+='## 4. 后续实验计划\n\n'+followup+'\n\n## 5. 风险与开放问题\n\n'+risks+'\n\n## References Used\n\n'+refs+'\n\n没有新的性能、费用或显存结果。\n'
    root=m.ROOT/'入选方案'/cid
    m.write(root/'FINAL_IDEA.md',text,f'Call{r["call"]}通过后完整展开{cid}')
    handoff=f'# 实验交接：{cid}\n\n独立{r["score"]}/10，无fatal；全文见[FINAL_IDEA.md](FINAL_IDEA.md)。\n\n## 定位与主Claim\n\n{c["keywords"]}。\n\n{intro[2]}\n\n{intro[3]}\n\n## 最小实现\n\n{method[3]}\n\n## 实验与同预算baseline\n\n{experiment[0]}\n\n{experiment[1]}\n\n唯一baseline规范见全文§3.3。\n\n## 止损及待定参数\n\n{experiment[4]}\n\n{risks}\n\nactor快照、正式金额、task数、seed和cap在实验前确定。本轮没有跑模型实验。\n'
    m.write(root/'EXPERIMENT_HANDOFF.md',handoff,f'{cid}同预算实验交接')
    m.write(m.REVIEW/'入选方案'/cid/'FINAL_REVIEW.md',(m.REVIEW/f'round-{r["call"]:02d}-review.md').read_text(encoding='utf-8')+'\n\n主执行器保留的实际风险：\n\n'+risks+'\n',f'{cid}独立审查与实际剩余风险','review')
    trace=m.REVIEW/'.aris'/'traces'/'idea-improvement-loop'/'2026-10-09_run01'
    p=trace/f'{r["call"]:03d}-round-{r["call"]}-review.meta.json';meta=json.loads(p.read_text(encoding='utf-8'))
    meta['produced_artifacts']=list(dict.fromkeys(meta['produced_artifacts']+[str(root/'FINAL_IDEA.md'),str(root/'EXPERIMENT_HANDOFF.md'),str(m.REVIEW/'入选方案'/cid/'FINAL_REVIEW.md')]))
    m.write(p,json.dumps(meta,ensure_ascii=False,indent=2),'补齐完整交付路径','review')

def idea41():
    cid='IDEA-041';c=next(x for x in m.load() if x['id']==cid)
    expand(cid,
        '| 术语 | 中文/全称 | 本方案含义 |\n|---|---|---|\n| AppWorld | 应用模拟器 | 用持久Python shell和API改变状态，按最终真实状态评价。 |\n| effect | 外部效果 | 已经成功的应用写入，代码报错后不自动撤销。 |\n| residual program | 剩余程序 | 用已知成功返回替代已完成效果，只重新计算必要纯表达式与未执行操作。 |\n| dynamic instance | 动态调用实例 | 同一源码调用在不同循环迭代与实参下的具体执行。 |\n| partial evaluation | 部分求值 | 利用已知值简化剩余计算；成熟程序语言方法，非新发明。 |\n| durable execution | 持久工作流执行 | 从历史结果重建已完成Activity的状态，通常要求预定义边界。 |',
        [
        '限定AppWorld中部分写入后抛错的单个Python代码块。首版支持顶层顺序赋值、直接API调用和固定列表简单循环，不支持任意Python、嵌套异步或不确定timeout。新增机制CPU运行，actor使用统一API，不训练模型。',
        '[AppWorld](https://arxiv.org/abs/2407.18901)的FullCode将stack trace交回模型再生代码。持久user_ns使普通顶层赋值可能已经保留，因此不能声称报错总会丢变量。Temporal已有历史Activity结果回放；Kishu已有notebook依赖恢复；DART/AgentRewind已有恢复边界。它们分别覆盖重要原理，本文差别仅是模型修改后的单个cell内部调用实例与剩余纯依赖。',
        '代码报错不回滚先前写入。需要先诊断更窄失败：原actor避免重复写时丢掉返回对象ID，或循环/未完成赋值中可用的依赖值不再可取得，剩余任务仍失败。该路径可达，但发生率尚未观察。已保留的普通变量是反例边界，不应强行重新恢复。',
        '我们把已成功写调用替换成其公开返回，并根据实际失败点重算剩余所需的纯表达式，保持外部效果与其数据依赖。CPU对齐源码位置、循环实例和实际实参；新参数的合法新写不被当成旧效果。修复已完成效果需要原actor显式补偿/换计划，而不是默默重新执行。',
        '同自然失败前缀、可见记录和预算比较FullCode、强remaining-code提示、成功回执去重、无依赖保留和剩余求值。只有超越回执去重和强提示，且真实自然任务有相应失败，才说明程序残余化值得做。',
        '1. 实例级效果与返回值的剩余执行边界。\n2. 区分普通已保留变量与真正丢失/覆盖依赖的自然失败诊断。\n3. 配对恢复与端到端预算对照，验证新增CPU机制的必要性。'
        ],
        [
        '已经发生的外部效果保留，后续真正需要的计算继续。\n\n1. CPU为支持的AST添加可见调用观测；记录位置、循环实例、参数、返回及成功状态。\n2. 失败后保留有明确成功回执的写入。\n3. 原actor只修失败调用与未执行后缀。\n4. CPU把已完成写替换为返回常量/已有对象引用，并重算必要纯依赖。\n5. 重复到达既有写实例时复用结果；未知效果不套用这一保证。',
        '输入：自己生成代码、公开API参数/返回、实际失败点和已有可见变量。输出：一段保持已知效果的剩余代码及无法支持的情况。需要调用实例可对齐、纯表达式确实不触发额外I/O、返回值可安全作为原类型值使用；不能仅靠源码文本位置在大幅重排后错误对齐。',
        '用AST和实际调用轨迹构建数据依赖闭包。对每个成功写保留原返回，修复后相同位置/循环实例/实参才能复用；不加哈希或指纹。纯计算依赖由已知返回向失败点和后缀传播，只重算必要节点。初版禁止把动态eval或隐式I/O函数标为纯；不支持则交原actor正常恢复并记入总体失败/成本。\n\n这不是通用确定性replay：修复模型可能改变程序，因此必须验证调用实例对应。若原代码完成了错误写，本方法只保留“已做过”的事实，不把它提升为“对任务正确”。',
        '已读[官方FullCode/environment](https://github.com/StonyBrookNLP/appworld)：_shell_run_cell、execute及user_ns真实存在。需要新实现AST观测、实例匹配和纯依赖残余化。只记录agent自己的可见调用，不能读task数据库/gold。环境和AST计算CPU；所有修复、额外输入输出、调用、初始失败均计费。源码核验不是实跑。'
        ],
        [
        '先验证“回执去重后仍丢依赖”的失败是否存在，再验证残余计算是否解决这个独立问题。不能只减少重复写就宣布成功。',
        '自然AppWorld train/dev失败轨迹做独立诊断，dev冻结支持语法及实例对齐。评测器复制同一失败前缀后的模拟世界做配对继续，但复制内容不提供controller；另报自然held-out端到端结果。各组同起点、同模型、相同文档/few-shot/温度/seed及完整API/LLM/token cap。',
        m.baseline_table(c)+'\n\n所有组共用调用边界记录；无免费完美标签、初始执行或额外修复轮。批量代码内部API逐次计费。Sentry当前完整代码未发布，DART公开语义恢复对齐存在疑问，Temporal/Kishu不属同一任务，均只列近邻而不当已核验AppWorld baseline。',
        '主指标是剩余任务及最终task成功、重复写和因依赖缺失产生的失败；次指标API/LLM/token、CPU实例匹配时间、支持语法覆盖、误匹配/错误复用。所有不支持或超时轨迹留在总体分母。评测器状态只用于评分，不能输入actor。',
        '真实失败入口非零、效果和依赖恢复正确、比强提示/回执去重改善同预算完成才支持。变量通常已保留、纯依赖成本抵消收益、只在人工特殊代码有效、或修复重排导致错误调用复用时停止。'
        ],
        '1. 拓展简单循环与多个失败点，先验证每种语法再扩大Claim。\n2. 消融返回替换、纯依赖重算和实例对齐。\n3. 分析自然变量保留与丢失/覆盖两类轨迹。\n4. 不同actor/预算下重复，同设置内参数公平。\n5. 展示误匹配失败和有效剩余程序案例。',
        '自然失败规模可能很小，因为IPython已有持久变量。模型修改代码后的调用对齐是主要实现风险；未确认映射不能跳过效果。成功回执不证明该写任务正确，不确定timeout也不能纳入已提交保证。最终方案不能扩大成任意Python持久工作流恢复。',
        '1. [AppWorld](https://arxiv.org/abs/2407.18901)：同任务与FullCode/source核验。\n2. [Verified Tool Calls](https://arxiv.org/abs/2608.02645)：已读一级全文，verify-before-retry近邻。\n3. [Temporal Tasks](https://docs.temporal.io/tasks)：持久Activity结果回放近邻。\n4. [Kishu](https://arxiv.org/abs/2406.13856)：notebook依赖/状态恢复近邻。\n5. [DART](https://arxiv.org/abs/2605.23311)：结构化恢复边界近邻；公开实现对齐仍有疑问。\n6. [AgentRewind](https://arxiv.org/abs/2608.14380)：agent/tool边界回放近邻。\n7. [Sentry](https://arxiv.org/abs/2610.02994)：同AppWorld恢复近邻，完整代码尚未公开。')

def idea42():
    cid='IDEA-042';c=next(x for x in m.load() if x['id']==cid)
    rows=[row[:] for row in c['baseline_rows']]
    rows[0][4]='uv sync；slop-code run --agent configs/agents/miniswe.yaml --model {共同API模型} --problem {冻结问题}；原生cost_limits仅step/cost/net-cost，统一总token硬上限需在模型调用边界新增；与原论文无cost上限的分数分开'
    rows[1][4]='同run入口 --prompt anti_slop / plan_first，对应当前anti_slop.jinja / plan_first.jinja；完整提示可移植到同MiniSWE，全部token计费'
    c['baseline_rows']=rows
    table=m.baseline_table(c)
    expand(cid,
        '| 术语 | 中文/全称 | 本方案含义 |\n|---|---|---|\n| SlopCodeBench | 迭代规格编码基准 | 同一agent不断扩展自己的代码，测试隐藏。 |\n| structural erosion | 结构侵蚀 | 复杂性集中到少量复杂函数的指标；不是可维护性的完整真值。 |\n| clone | 近似代码复制 | 多个区域共享结构但部分名字/常量不同。 |\n| anti-unification | 反统一 | 提取多个AST共同骨架，把不同处留成变化孔；成熟方法。 |\n| 变化轴 | 本方案中的定义 | 当前spec已有且在历史实例中能够独立变化的维度，如语言或匹配种类。 |\n| checkpoint | 需求轮次 | 一轮新的公开规格和自己此前工作区；未来规格不可见。 |',
        [
        '限定SlopCodeBench公开Python任务序列，以同MiniSWE actor不断编辑自己的代码。没有模型训练；AST处理与已有代码对齐CPU执行，重构分析和生成仍使用同API预算。不能利用下一checkpoint的需求设计当前接口。',
        '[SlopCodeBench](https://arxiv.org/abs/2603.24755)报告复制和分支集中逐轮增长，通用anti_slop/plan_first不能阻止退化。自动clone抽取/anti-unification、CREC历史co-change和REFINE基于smell重构已有直接先例。本研究不把抽函数或变化点分析当成新算法。',
        '待验证的窄假设：近似clone的共同外形不代表它们沿同一需求维度变化；合并不同变化轴后，下一次扩展可能又把函数切开。必须在自然轨迹检查这一链条；不能把增加需求的复杂性本身当成迭代引起退化。',
        '我们用已发生的spec与代码diff解释anti-unification孔。只有已有至少两个实例、并有仅一个维度不同的分离证据时，才建议对该维度提炼共享骨架；联合变化或缺少证据时不提前独立抽象。这约束重构动作，不添加尚未发生的feature flag、迁移层或未来接口。',
        '同actor/spec/工作区与总预算比较原agent、anti_slop、plan_first、clone-only、固定每轮重构和变化证据约束。主要观察下一checkpoint严格正确率与完成成本；当前CC和重复下降只作辅助，不能作为成功标准。',
        '1. 公开需求变化与AST孔的实例关联。\n2. 用单轴分离证据限制在线重构，避免未观察到的抽象假设。\n3. 后续真实扩展成本/正确率验证，控制累计需求复杂性。'
        ],
        [
        '先看不同部分是否曾在真实需求中独立变化，再决定抽象。\n\n1. 工作区保留上一轮spec、自己的代码及diff。\n2. CPU对齐变更附近近似clone，得到公共骨架和孔。\n3. 原actor在正常分析里解释孔对应的当前需求维度与联合变化。\n4. CPU核对历史实例是否有单轴差异；无证据不宣布独立。\n5. 原actor做一次局部重构或直接扩展，并在共同预算内自测。',
        '输入是当前及过去可见spec、自己代码/diff和公开例子。输出是允许提炼的骨架/孔及其有限证据。依赖条件是AST区域可对齐，需求维度解释够可靠，已有例子并非偶然的相关变化。没有两个实例不代表将来不能抽象，只是当前机制不作证据不足的建议。',
        'AST相同节点保留，差异常量/标识符置为孔；位置属性不参与结构判断。每个候选记录实际来源区域和轮次，不生成哈希。原actor解释维度，CPU只对明确实例检查哪个孔/维度发生变化，不能通过一个自然语言标签证明完整语义独立。\n\n重构行为以已观察变化为依据，不能根据隐藏future tests挑骨架。公开例子和自己测试只检测当前行为，不保证未知全部行为；重构导致当前错误也照实进入成功率。',
        '已读公开MiniSWE wrapper、真实DefaultAgent/API接口、local/Docker环境、配置和run指南。入口slop-code run可运行；CPU新增AST对齐与证据表。重要修正：公开AgentCostLimits只有step/cost/net-cost，没有总token硬上限，实验需在模型调用处统一新增记账与中止；不能伪称cost_limits已提供token cap。prompt名是anti_slop/plan_first，非连字符。'
        ],
        [
        '判断当前更谨慎的抽象是否在未知下一轮需求中减少重新切开/重复复制，并提高同预算完成。单纯降低被自己优化的CC没有价值证据。',
        '使用冻结的当前公开问题列表，不混用原论文20问题/93checkpoint与后续公开扩展语料的分数。当前每轮只能见当前spec，hidden tests只用于离线评测且结果不返回agent。各组同初始空工作区、任务順序、自己代码继承规则、模型/推理/seed与完整预算。另用同一累计spec的继续编辑和from-scratch诊断区分需求扩大与路径依赖，不免费给未来累计spec。',
        table+'\n\n各组都可见同历史diff和spec摘要。重构/自测/历史序列化耗费同总token及步骤额度，不免费给主方法多一轮。MaintainCoder/CREC/REFINE任务或训练方式不同，只列近邻。',
        '主指标下一轮严格正确率和完成费用；次指标重新拆开共享区域、重复增长、当前重构引入错误、CPU对齐时间、token和步骤。侵蚀/verbosity仅辅助。未产出代码和超预算轮次按失败报告，不能从分母删去。',
        '自然错误合并变化轴存在，证据约束比clone-only/固定重构改善后续正确率或成本，当前正确性不明显损失才支持。没有后续收益、轴解释低可靠性、分析token抵消节省、或只有自优化指标变好则停止。'
        ],
        '1. 消融spec维度解释、单轴分离证据和历史diff。\n2. 同条件下不同actor及预算重复。\n3. 按真实需要联合变化和独立变化分组，检查错误抽象。\n4. 比较继续编辑与同累计规格重写的配对结果。\n5. 展示下一轮重新拆开及成功保留骨架的自然案例。',
        '需求维度解释仍依赖actor，少量实例不证明未来独立性。当前clone指标降低可能只是优化指标，没有维护收益。AST对齐和重构开销可能更贵；不能用隐藏下一轮规格、完美人工轴标签或额外重构预算制造优势。',
        '1. [SlopCodeBench](https://arxiv.org/abs/2603.24755)，任务和提示实验；[公开代码](https://github.com/SprocketLab/slop-code-bench)已读。\n2. [MaintainCoder](https://arxiv.org/abs/2503.24260)，动态需求可维护生成近邻。\n3. [Incremental Code Clone Detection and Elimination](https://www.cs.kent.ac.uk/pubs/2011/3087/)，anti-unification成熟原理。\n4. [CREC](https://arxiv.org/abs/1807.11184)，历史演化/co-change重构近邻。\n5. [REFINE](https://arxiv.org/abs/2608.23611)，evidence-guided重构近邻。')

def idea46():
    cid='IDEA-046';c=next(x for x in m.load() if x['id']==cid)
    expand(cid,
        '| 术语 | 中文/全称 | 在本方案中 |\n|---|---|---|\n| SWE-bench | 真实仓库issue修复基准 | agent改代码，隐藏评测仅离线用于resolved。 |\n| pytest nodeid | 测试唯一名称 | 定位同一个已执行测试；源码变了则不作同一检验比较。 |\n| P→F / F→P | 通过到失败／失败到通过 | 前后两轮共同测试的可观察状态变化，不等于唯一根因。 |\n| head-tail | 输出头尾裁剪 | MiniSWE超过10000字符时保留各5000字符。 |\n| TDAD / TestLoc | 影响分析／测试定位方法 | 改变选了哪些测试，保留其原生能力作强比较。 |\n| Squeez | 工具输出剪枝 | 按当前任务压缩一次原始输出的已有方法。 |',
        [
        '在SWE-bench修复轨迹内研究实际pytest反馈，新增部分CPU做确定性状态比较，无模型训练。actor使用API；已有Squeez模型只做推理，原2B与150M版本分别报告，不混淆结果。',
        'MiniSWE当前配置按字符头尾裁剪工具输出。TDAD和TestLoc提供高价值选测与回归控制，Squeez压缩pytest/stacktrace，AgentDevel已有P→F原语。不能把测试状态差分或输出压缩声称为首创；本案只利用同一条修复轨迹的共同测试变化来安排有限在线反馈。',
        '待诊断：旧失败和重复日志占据头尾，本轮新增回归被藏在中段，只有命令级returncode无法告知agent它又破坏了什么。公开配置证明裁剪入口，未证明自然遮蔽频率或后续误修因果链。若没有这类失败，不继续完整实验。',
        '我们对两轮共同执行且测试源码未改的nodeid比较状态，先让同一反馈预算展示新增P→F及断言，再展示原有失败。没有前次可比结果时采用单次结构化反馈；skip/未跑不是通过。完整日志仍可供各组相同预算下请求。',
        '选测策略与反馈策略分开：保留原生、TDAD、TestLoc三类选测能力，每类内部比较头尾、结构化、聚类、Squeez和状态差分。必须在同选测支持、预算和机会下改善resolved/回归，不能把更好选测的收益当反馈机制收益。',
        '1. 对真实修复轨迹的跨轮共同test状态建立低成本反馈。\n2. 自然回归遮蔽及决策后果的独立诊断。\n3. 原生选测×呈现的归因比较，隔离差分的增量。'
        ],
        [
        '告诉agent“这次新坏了什么”，再让它决定修什么。\n\n1. 共用pytest plugin记录公开test的nodeid、执行状态及断言。\n2. 比较共同已跑且源码未变的test。\n3. 将P→F置于固定反馈前部，报告其数量和代表证据。\n4. 剩余空间呈现原有失败，重复直接按异常/首项目帧分组。\n5. 原actor继续修复；完整日志访问照常计费。',
        '输入是两轮实际公开测试结果、测试源码和原始日志。输出是受限token的状态变化反馈。需要可稳定定位测试，不能将未收集、skip、timeout或修改fixture后改变的test当成相同通过证据。比较仅限共同支持，不外推未跑的suite。',
        '前次pass、本次fail标为新回归；前次fail、本次pass标为修复。原测试源码用实际文本比较，不加hash；测试源或已知fixture被改则标不可比。反馈先给变化总数，再填test ID、首项目帧和具体断言，剩余原失败按冻结顺序。\n\n它不判断是哪行改动造成失败，也不使用SWE-bench隐藏P2P/F2P标签。若结果不稳定，差分只能作可观察变化，需要另报flaky边界。不能只选好看的、完整两次测试的轨迹进入总resolved分母。',
        '已读MiniSWE default/benchmark runner/config，TDAD CLI index/impact/run-tests，TestLoc真实4阶段pipeline，Squeez extractor的device与extract。API actor和CPU测试容器；Squeez可显式device=cpu，CPU内存和时长必须测量，源码提供路径不等于已跑通。所有额外选测、定位LLM、覆盖收集、日志采集和反馈序列化计入总预算。'
        ],
        [
        '先确认自然遮蔽链，再检验状态差分是否超越现有压缩、选测与回归策略。',
        'SWE-bench公开pytest可运行的实例，按公开框架支持筛选而非主方法结果筛选。开发冻结规则，held-out固定实例和seed；全部组同repo/issue/actor/模型推理、温度、上下文/输出、API与命令cap。原生端到端结果与共同已执行测试的机制诊断分开。',
        m.baseline_table(c)+'\n\n每种原生选测策略内部固定测试来源和执行预算，反馈策略不免费追加tests；另报告完整组合端到端。Squeez原2B与其150M替代不混称；无训练或本地GPU强制要求。主方法plugin信息全部对照可见，不提供免费失败前测试。',
        '主指标resolved及实际后续回归；诊断是新增P→F在原头尾中是否可见、agent是否响应，以及无谓修复次数。完整token、测试执行/coverage、辅助模型、CPU时间/内存和费用全部报告。不能只报输出压缩比例。',
        '需要真实遮蔽，差分在固定选测策略内比Squeez/单次结构化有效，最终resolved或回归改善且成本公平。短pytest已足够、变化只来自flaky、公共支持过少或强选测已消除遮蔽则止损。'
        ],
        '1. 去除差分，只保留同样结构化与聚类，测独立增量。\n2. 比较原生/TDAD/TestLoc各自的结果，保持原方法能力。\n3. 分长短输出和真实新增回归，确认触发条件。\n4. 不同actor和预算，每个设置内部保持公平。\n5. 展示一次遮蔽导致误修和一次差分误报的真实轨迹。',
        '自然遮蔽规模未验证；共同测试支持可能少，flaky也可能产生P→F。测试/fixture变化不能被忽略。辅助Squeez CPU开销与测试定位成本可能大，不能只算主actor费用。只改善可见率却不改善任务不是成功。',
        '1. [SWE-bench](https://arxiv.org/abs/2310.06770)，任务；[MiniSWE](https://github.com/SWE-agent/mini-swe-agent)实际runner/config已读。\n2. [TDAD](https://arxiv.org/abs/2603.17973)，[实现](https://github.com/pepealonso95/TDAD)，原生选测基线。\n3. [TestLoc/TestPrune](https://arxiv.org/abs/2510.18270)，[实现](https://github.com/IBM/Issue-Test-Localizer)，原生选测基线。\n4. [Squeez](https://arxiv.org/abs/2604.04979)，[实现](https://github.com/KRLabsOrg/squeez)，输出剪枝基线。\n5. [AgentDevel](https://arxiv.org/abs/2601.04620)，发布版本flip原语近邻。\n6. [Tokenmaxxing](https://arxiv.org/abs/2607.22807)，离线测试向量近邻，reviewer检索。\n7. [SWE-Pruner Pro](https://arxiv.org/abs/2607.18213)，内部表示/训练剪枝近邻，非首版无训练机制。')

def idea48():
    cid='IDEA-048';c=next(x for x in m.load() if x['id']==cid)
    expand(cid,
        '| 术语 | 中文/全称 | 在本方案中 |\n|---|---|---|\n| Boolean Series / mask | 布尔筛选序列 | 每个bool原本由某个数据行的条件得到。 |\n| label alignment | 标签对齐 | pandas按index标签决定bool应用到哪行，标签可能被重新使用。 |\n| row identity | 行来源身份 | 从公开输入分配的顺序行ID，随纯行变换传播；普通元数据，不是hash/指纹。 |\n| DA-Code / DS-STAR | 数据分析基准／强验证agent | CPU数据分析和API模型，首版只取CSV分析子任务。 |\n| RADAR | 数据分析运行时检查 | 已有schema/字段/显式join/提交检查，完整公开实现未核验。 |',
        [
        '研究一个Python action内部的CSV数据清理/分析，不做ML训练。首版限定sort_values、过滤、reset_index和列比较形成的Boolean Series，再用[]/.loc选择。join、groupby、改列值或跨action的任意依赖不在首版。',
        '[pandas](https://pandas.pydata.org/docs/user_guide/indexing.html)按标签对齐布尔Series；RADAR已在DA-Code上用类型化操作与可见检查减少静默错误；已有细粒度dataframe provenance与NBSafety检测陈旧状态。本案不发明对齐/血缘，差别只在mask原行与当前目标行逐位关系。',
        '可能的自然错误：在原df算mask，排序并reset_index后旧整数标签被重新使用，再套旧mask。代码可跑、dtype/长度相同，却筛另一批行。这个pandas语义后果可推导；是否在DA-Code自然agent轨迹频繁出现仍需盲标，不能由RADAR总体静默错误率替代。',
        '我们保留每个bool对应的来源行，跟随纯行变换维护对应关系。应用mask时比较该bool原来源和实际目标，给首个可见错配。默认原actor修代码；纯行重排时按ID重附可作单独消融，未知出处或值已改变不自动修。',
        '同DA-Code task/data/API模型与完整预算，比DA-Agent、DS-STAR原生、schema/index检查、总是重算mask和行来源诊断。总是重算的便宜控制已经等效时停止。只对少数支持操作有效不能宣称通用数据分析正确性。',
        '1. 对标签合法但行身份错配的mask复用做独立诊断。\n2. 支持范围内bool来源—目标身份比较及可见反例。\n3. 与强原生验证和便宜重算的同预算比较。'
        ],
        [
        '一条bool应该继续跟着产生它的那一行，而不是跟着后来重用的整数标签。\n\n1. 为read_csv得到的行分配顺序ID，侧表维护，不改变用户数据。\n2. sort/filter/reset_index传播行对应；bool比较保留来源对应。\n3. mask实际用于当前df时逐位比较。\n4. 返回第一个具体错配和两行可见证据。\n5. 原actor重算/调整代码，未知结构保持unknown。',
        '输入是公开数据和实际支持操作、bool与df的对应表。输出是身份一致、具体不一致或不支持。只处理按行语义形成的Boolean Series，显式位置数组不纳入；业务上有意的跨表键对齐也不能按“不来自同一物理df”就认定错误。',
        '侧表用顺序ID而非内容哈希，记录每次纯行变换的旧位置到新位置关系。标签重排本身正常；只有实际应用的bool来源行与当前被选行分离才提供诊断。新列值已改变时旧predicate也可能陈旧，但这是另一问题，不在当前自动重附保证。\n\npandas正常运行不意味着符合任务；同时，controller发现来源不同也不是业务错误真值。独立标注检查实际意图及合法复用，避免把正常alignment当错误。',
        '已读DA-Agent、PythonController、DS-STAR run/coder/debug/verify/router与LLM helper。新增仅支持操作的CPU追踪和反馈；API actor无需GPU。DS-STAR实际debug_round有正确拼写，guidelines.txt源码会无条件读取，需准备同格式说明；LLM helper未统一总token和采样，实验需调用边界统一计账与参数，不能原样声称公平。'
        ],
        [
        '先发现自然错误且能与合法alignment区别，再验证行来源证据能否比shape/index或简单重算更好。',
        '冻结DA-Code公开CSV DW/DM/EDA子集，排除ML/重视觉任务。筛选依公开任务与框架支持，不按主方法结果挑任务。dev冻结支持操作，held-out盲标自然mask复用及误筛；所有不支持任务仍在整体成功分母。原始任务评分与配对错误前缀诊断分开。',
        m.baseline_table(c)+'\n\n同actor/辅助模型、原始文件、task/seed、历史窗口、上下文/输出/步骤与总API/token预算。DS-STAR保留原生计划/分析/verify，全部成本计入。RADAR无已核验完整代码，仅将公开、可完全指定的小规则作为本地控制，不标其原作者分数。',
        '主指标官方table match与task成功，次指标实际误筛行、身份诊断precision/recall、误报、支持覆盖、CPU时间/内存以及全部模型/执行成本。代码不异常不是主终点。',
        '自然错配存在，身份检测准确且比廉价控制/DS-STAR改善同预算任务才继续。总是重算已等效、错误罕见、主要操作不支持、误报合法alignment或追踪比重算更贵则停止。'
        ],
        '1. 消融来源身份，仅使用label/shape。\n2. 分sort、filter、reset_index及组合，检查真正触发条件。\n3. 纯行重附与actor提示两臂分开，避免混淆确定性修复和额外推理。\n4. 不同actor/数据量下记录CPU/RAM及模型成本。\n5. 展示真实错配、合法对齐和unknown三类案例。',
        '初版行变换覆盖很窄，自然频率可能低。追踪ID不能替代语义意图；位置选择/合法键对齐必须排除。改列值后旧谓词是否有效不在当前保证。简单重算可能始终更便宜，必须以它为硬停止对照。',
        '1. [DA-Code](https://arxiv.org/abs/2410.07331)，[代码](https://github.com/yiyihum/da-code)，同任务。\n2. [DS-STAR](https://arxiv.org/abs/2509.21825)，[代码](https://github.com/google-research/ds-star)，强同任务API基线。\n3. [RADAR](https://arxiv.org/abs/2609.32528)，已读规则，完整代码未核验。\n4. [pandas indexing](https://pandas.pydata.org/docs/user_guide/indexing.html)，标签/布尔语义。\n5. [Fine-grained Provenance](https://arxiv.org/abs/2310.18079)，2024，成熟行级血缘近邻。\n6. [NBSafety](https://arxiv.org/abs/2012.06981)，2021，陈旧notebook状态近邻。')

def idea50():
    cid='IDEA-050';c=next(x for x in m.load() if x['id']==cid)
    expand(cid,
        '| 术语 | 中文/全称 | 在本方案中 |\n|---|---|---|\n| JSON提取器 | 无I/O表达式/短函数 | 从一个公开工具返回提取后续使用值，不能再次调用API。 |\n| finite observational preservation | 有限观测保持 | 修补在指定旧JSON上返回原观测值；不意味着这些值语义正确。 |\n| candidate repair | 候选修补 | 同一次actor修复轮生成最多3个提取器，CPU验证。 |\n| CEGIS | Counterexample-Guided Inductive Synthesis | 用反例排除候选的成熟思路；本案不发明它。 |\n| AppWorld / ACE | 应用环境／增量context agent | 同任务复现入口与强执行反馈对照。 |',
        [
        '限定原始AppWorld完整API文档下的纯JSON提取器修复。没有后台API重放、额外任务rollout、critic或模型训练。一个actor修复轮最多3个候选；所有候选生成、历史序列化和CPU测试都计入预算。',
        'AppWorld报告字段臆造和接口误用。LDB与VeriHarness已有局部运行时/结构化反馈，ACE已有执行经验；程序修复也早已同时修失败测试并保持旧通过测试，Agentless Mini和Tool-Making是重要先例。当前新意只限tool agent自己已经观察过的JSON与输出、无gold的纯提取器修补验证。',
        '更窄待诊断假设：为当前empty/None或嵌套结构修补提取器，可能改变它对其它已有适用返回的行为。一次错误定位只告诉哪里坏，不保证该修补保留其它观测。发生率和任务效应均未知；此前成功访问也可能给过语义错误值。',
        '我们让同一修复轮提出少量纯候选，在当前失败结构和已有适用样本上CPU重放；除检查异常/类型外，还检查需保留的原观测值。失败候选收到具体反例，剩余候选由原actor判断语义。无需新增API调用，也不把旧输出变成正确答案。',
        '同样最多3个候选、样本/原值/上下文和预算，对比只测当前失败、多样本结构测试及观测值保持；加官方FullCode、强局部提示和ACE原生。只有观测保持的独立增量改善真实TGC/成本，才说明这层验证值得做。',
        '1. agent已可见历史输入输出的有限保持约束。\n2. 无环境重跑的纯候选CPU验证与反例。\n3. 候选数量/信息/预算严格相同的机制消融，以及非真值保持风险诊断。'
        ],
        [
        '修这一次错误前，先在自己已经见过的输入上检查有没有又改坏其它行为。\n\n1. 保存当前提取器适用旧JSON与真实观测输出。\n2. 修复轮生成最多3个纯候选。\n3. 当前样本只验证可执行，不提供gold值。\n4. 旧样本验证有限输出保持，给冲突反例。\n5. 原actor选语义上合理候选，并继续原任务。',
        '输入是当前失败返回、同一提取器旧适用样本/输出、事前声明的保留范围及候选函数。输出为通过候选或明确反例。只支持无I/O有限表达式、dict/list访问、guard、基础转换与简单组合；跨接口/版本不能随便混样本。',
        '对每个旧适用输入执行候选，比较原观测输出的实际值和类型，不用哈希。原actor若认为某些旧行为本来就应改变，必须在生成候选前说明并从保留范围移出；不得事后删反例让候选通过。\n\n无条件None/空值可能结构无异常，但不能据此完成任务或删掉必需后续动作。当前样本可执行、旧值保持都只是必要的有限检查，不证明选了正确业务字段，也不保证未来输入。旧行为原来有错时保留可能有害，必须独立报告。',
        '基于已核验AppWorld FullCode/持久Python调用记录及ACE no-GT。新增提取器样本集与纯函数CPU测试；不执行未确认I/O候选，不重做工具效果。CPU可能在JSON很大时花费明显内存/时间，需要测量；样本保留与模型输入都计费，不能以不训练为理由忽略成本。'
        ],
        [
        '先确认当前修补导致旧观测变化且影响任务的自然病例，再验证值保持是否超越只测当前或多样本类型。',
        '原始AppWorld train/dev自然字段/访问错误，完整schema不变。开发冻结支持提取器与样本适用规则；同错误前缀配对恢复与自然held-out端到端分开。所有组看到同原始样本/原值和访问错误，不能给主方法额外真实返回或人工正确保留集。',
        m.baseline_table(c)+'\n\n候选组最多3个、同生成token cap与修复机会；FullCode/ACE原生结果另报，保持其算法和完整构建/反思预算。actor/reflector使用同能力快照，task、seed、few-shot、步骤、工具/LLM与总token固定。',
        '主指标TGC和真实恢复轮数；机制指标当前错误解决却旧观测回归、值保持相对结构测试的效果、vacuous候选、错误旧值被保留的比例。次报完整调用/token/费用、CPU时间/RAM和样本覆盖。不以CPU测试通过率代替成功。',
        '自然旧行为回归存在，同候选数/信息/预算下观测保持比结构测试有益，且没有靠保留错误旧值或跳过任务得到假好结果才继续。结构测试已够、样本少/不适用、主要旧值错、或更少异常但TGC下降时停止。'
        ],
        '1. 消融旧观测值，只保留多样本结构测试。\n2. 同预算改变候选数与样本覆盖，每组内部参数公平。\n3. 分empty/null/嵌套结构与本来需改旧行为的错误。\n4. 衡量JSON规模、CPU/RAM和样本序列化成本。\n5. 展示一条避免旧行为回归和一条错误旧值被保留的真实轨迹。',
        '有限保持不是语义正确。旧输出可能错，未来返回可能不同，适用样本也可能混错。纯提取器边界窄；将整个有副作用代码放进重放会改变问题，因此首版严格保持无I/O范围。简单结构测试可能已经足够。',
        '1. [AppWorld](https://arxiv.org/abs/2407.18901)，同任务公开实现。\n2. [ACE](https://arxiv.org/abs/2510.04618)，[AppWorld fork](https://github.com/ace-agent/ace-appworld)，强baseline。\n3. [SWE-RL / Agentless Mini](https://arxiv.org/abs/2502.18449)，候选修复与旧通过测试近邻，非同任务baseline。\n4. [Tool-Making](https://arxiv.org/abs/2607.08010)，执行trace/schema/value与候选工具验证近邻。\n5. [VeriHarness](https://arxiv.org/abs/2607.14167)，结构化反例近邻。\n6. [LDB](https://arxiv.org/abs/2402.16906)，已读局部运行时调试。')

def idea52():
    cid='IDEA-052';c=next(x for x in m.load() if x['id']==cid)
    expand(cid,
        '| 术语 | 中文/全称 | 在本方案中 |\n|---|---|---|\n| grounding | 接地 | 某个具体参数值能在用户输入或真实公开返回中找到支持。 |\n| joint witness | 联合值见证 | 不只是各值存在，还能从返回行/父调用关系支持它们一起组成一组参数。 |\n| relation tuple | 关系元组 | 保留字段之间的实际关联，不能降成互不相关的值集合。 |\n| natural join | 自然连接 | 用公开、明确的关联键连接有据关系；成熟数据库操作。 |\n| supported / contradicted / unknown | 支持／冲突／未知 | 当前观测能支持、能反驳，或覆盖不足不能判断组合。 |\n| HyperAgent / PACT | schema图规划／参数来源检查 | 已有联合调用和逐参数机制，不假设其未知实现一定遗漏本问题。 |',
        [
        '限定AppWorld可信工具的多对象调用，研究业务参数关系而非安全攻防。一个冻结actor使用API，CPU记录关系并检查组合；没有模型训练或GPU推理要求。目标是完成原任务，同时减少分别有来源却组合错配的调用。',
        'HyperAgent已维护schema-value bindings、同调用联合输出与deterministic binding validation；Entity Binding Failures已有多实体gate，PACT已有逐参数provenance，Binding Drift已有跨步对象保持。不能把这些说成不存在。当前只主张已核验描述未完整展示返回行/父调用键的业务关系join及三值反馈；HyperAgent无已核验公开完整代码，所以不对其实际runtime作负面事实结论。',
        '逐字段值存在不直接证明它们属于同一关联对象。例如两个关系R1={(x1,y1),(x2,y2)}、R2={(x1,y2),(x2,y1)}的schema和值集合相同，但(x1,y1)只有前者支持。这个例子是教材事实，只诊断marginal-only表示，不是新定理，也不能证明某个实际agent用的state只保留marginals。自然AppWorld错配频率和任务影响仍未知。',
        '我们保留实际调用参数、返回对象/列表行和公开父关联键，构建关系元组。下一调用的关联参数只有在公开关系中能连接时才有联合支持；已知冲突给原actor修正，覆盖不足是unknown。允许正确跨行连接，不强制所有输入来自同一物理row，不把缺少一个当前tuple等同全局无效。',
        '先做同marginal、不同关系的表示诊断，再在原始AppWorld上同actor/raw history/信息与预算比较native FC、逐字段验证、same-call、same-row与关系join。主结论必须是自然任务成功/成本与错配改善，不能只说在构造反例上胜出。',
        '1. 具体参数组合的行/父调用联合值见证。\n2. 区分可支持、可反驳和观测覆盖未知的反馈。\n3. 同call/同row对照与自然多对象任务，检验关系检查是否值得做。'
        ],
        [
        '先确认这组值有关系支持，再让原actor调用。\n\n1. 同FC runner记录真实参数和逐调用返回。\n2. 按返回对象/列表行保存字段，父关联参数只有公开文档/返回明确支持时附上。\n3. 原actor在正常分析里声明本动作关联组和port对应，各组同享该说明并计费。\n4. CPU按已知键连接，输出supported/contradicted/unknown及可见证据。\n5. actor改组合、补查或继续；不能以拒绝更多动作冒充任务更成功。',
        '输入是公开调用/返回、关联说明、用户条件和拟调用值。输出是当前组合的三值关系反馈。需要至少一些明确关联键；不能靠字段类型相同、名字相似或同一user就认定两order相同。独立新常量不强制同源，多对象合法跨行组合必须允许。',
        '每个row保留调用实例和行号，真实父参数作为关系的一部分；均是普通可读元数据，无hash/指纹。按明确owner/id等键做join，得到受支持值组。known contradicted必须有实际反驳证据，完整枚举缺席只有证明覆盖完整时才能作为反证；其余保持unknown。\n\n未知不自动升级为业务错误或强拒绝，actor仍承担语义选择。某个支持元组不证明符合用户目标，也不保证其当前仍有效。首版在关联读取至消费之间没有相关关系写入的范围验证；同agent相关写发生后，旧见证只作历史，需当前可见证据，不能继续当现时支持。这是实际状态边界，不新建通用迁移/权限框架。',
        '已读官方SimplifiedFunctionCallingAgent及runner的执行输入/返回配对点，AppWorld CLI是真实入口。增加CPU关系侧表和join，记录只限agent本来能获得的调用输入与公开返回，不读DB、hidden evaluator、gold solution。所有说明、额外补查、关系序列化、失败及CPU处理成本计入，未端到端运行。'
        ],
        [
        '证明控制是否保留必要关系信息，并判断自然任务中这一信息差是否真的影响调用和完成。表示例子不能替代自然诊断。',
        '先冻结R1/R2成对表示测试，只用于关系与marginal差别，不报为AppWorld分数。再按公开多对象API结构选train/dev任务，独立标注跨关系错配、合法跨行组合及补查；dev冻结关联解释，held-out报全集成功与支持覆盖。不按主方法成功挑任务，构造例子与自然结果分开。',
        m.baseline_table(c)+'\n\n同模型快照、task/seed、API/文档/关联说明、raw历史、上下文/输出、工具和LLM总调用/token上限。marginal-only控制只代表明确指定的消融，不代表HyperAgent。HyperAgent、Entity Binding/PACT/Binding Drift任务或公开实现条件不匹配当前实验，只列强近邻。',
        '主指标原task成功、实际关联组合错误与完整成本；次指标已冲突/未知区分准确度、合法跨行误报、额外补查、明确关系覆盖、CPU时间/RAM。unknown不能用错配真值标签计入“正确拦截”；少执行导致低错配而完成率更差不算收益。',
        '自然错配有影响，关系join比逐字段和同call减少错误，又比同row少误报并在同预算任务更好才支持。明确关系覆盖低、same-row已等效、native已会正确结合、三值解释不可靠或全部收益来自保守不执行时停止。'
        ],
        '1. 消融父调用键、返回row及unknown语义，保持其它信息一致。\n2. 分同row、同call跨row、跨call有键连接三类，核对合法范围。\n3. 同模型内改变输出长度、候选对象数和预算。\n4. 相关关系写后的新观测作为后续扩展，不提前泛化首版静态关系保证。\n5. 展示自然错配、合法跨行和覆盖不足的真实例子。',
        '关联说明仍由actor解释，可能错；明确键不总存在，历史见证也可能过期。联合支持只是业务关系必要证据，不证明用户指代或整体任务正确。教材反例和公开近邻没有相同实现不能充当已经胜过现有方法的结果。',
        '1. [AppWorld](https://arxiv.org/abs/2407.18901)，[官方代码](https://github.com/StonyBrookNLP/appworld)，同任务与FC入口。\n2. [HyperAgent](https://arxiv.org/abs/2608.02650)，已直接读state/联合输出/runtime binding，完整代码未核验。\n3. [Entity Binding Failures](https://arxiv.org/abs/2606.30531)，已直接读gate与provenance，逐实体近邻。\n4. [PACT](https://arxiv.org/abs/2605.11039)，逐argument来源近邻，安全任务非本次baseline。\n5. [Binding Drift](https://arxiv.org/abs/2607.18316)，跨步保持与错误传播近邻。\n6. [In-N-Out](https://arxiv.org/abs/2509.01560)，静态port依赖近邻。')

if __name__=='__main__':
    idea41();idea42()
