"""本次七条入选目标的候选生成记录；只管理文档，不跑模型。"""
import 候选管理 as m

def new(c):
    m.add([c])
    return m.load()[-1]['id']

def residual():
    return new(dict(
        title='失败代码的修复以已提交效果为边界做剩余程序求值',group='app',parent='IDEA-002',score=8.4,
        route='相似领域成熟方法迁移',keywords='interactive coding agents；stateful execution；execution feedback',
        background='交互式代码agent在一段程序部分写入后报错时，怎样修复后续计算而不重新执行已完成的效果。',
        claim='AppWorld明确支持持久Python变量和非回滚API写入；官方FullCode修复把stack trace发回模型重生代码。待验证一个更窄失败：修复虽避开重复写，却把该写返回的对象ID或随后被覆盖的局部值一起丢掉，导致剩余任务无法继续。贡献是以已成功效果的返回值替代原调用，并从失败点重新求值所需纯表达式，使修复保持已有外部效果和其数据依赖；不是一般幂等重试或postcondition验证。',
        method='首版只支持顶层顺序赋值、表达式、固定列表for循环内直接apis调用；动态eval、嵌套异步和不确定timeout不在首版。CPU对agent自己生成的AST插入调用边界观测，记录执行实例的源码位置、循环索引、真实参数、公开返回及成功/报错；只读agent可获得的数据，不读数据库或task ground truth。错误后根据实际成功写实例划定效果边界，把它们替换为已记录返回值。修复模型只修改失败调用及未执行后缀；数据依赖闭包内的纯表达式允许重算。CPU检查修复是否重新到达已提交写实例；相同源码位置但不同参数的有意新写不能冒充已完成调用。若修复需要改动已完成效果，由原actor显式说明并执行可见补偿或换计划，不能静默跳过。只在已成功回执的范围声称可重用，不以timeout当未执行证据，不做hash/指纹。',
        experiment='AppWorld train/dev的自然部分执行轨迹先诊断，再对同一失败前缀克隆出的世界进行配对恢复，环境克隆仅评测器使用，controller不可读其状态。对比官方FullCode、强remaining-code提示、只按成功回执跳过写、保存回执但不保留数据依赖、剩余程序求值。核心机制比较共用相同调用边界记录和上下文；另报原生端到端成本。主指标剩余任务完成率、重复写和丢失依赖引发的错误；所有初始失败、仪表记录、修复和工具调用计入总预算。若强提示或简单回执跳过等效，则否定残余求值必要性；不是在受限语法子集有效就宣称全部Python可修。',
        story='代码报错不回滚世界，也不保证后续需要的局部变量被正确保留；只去重效果不能恢复依赖；用成功返回替代写调用，并重算失败后真正所需表达式；若比回执去重更少丢失对象/重复写并提升同预算完成率，才支持方法。',
        reason='有可直接核验的持久执行与FullCode修复入口；新意限部分执行后效果和数据同时保持的agent恢复，partial evaluation本身成熟，8.4是需独立审查的暂定判断。',
        sources='[AppWorld原文](https://arxiv.org/abs/2407.18901)；官方environment.py的_shell_run_cell/execute/user_ns与FullCode._retry入口已读；[Verified Tool Calls](https://arxiv.org/abs/2608.02645)作为最高相关失败语义。',
        novelty='具体候选形成后定向检索program residualization+LLM agent未找到直接同构；已读Verified Tool Calls的verify-before-retry，它不处理失败代码的动态实例与纯表达式依赖。程序切片/partial evaluation不是新理论，需要reviewer检索agent恢复及持久工作流。',
        independent='在agent生成的部分执行代码中，将外部已提交效果与可重算的纯数据依赖分开，求可继续的剩余程序。',
        evidence_detail='可核验实现：src/appworld/environment.py保留self.shell.user_ns，_shell_run_cell执行IPython；普通API错误之后没有数据库自动回滚逻辑。README明确stateful变量可跨cell复用。FullCode代码_step_three将stack trace接retrial_prompt再生成整段code。只能据此主张入口存在，尚未观察到误恢复比例。instrumentation需新实现，源码核验不是实跑。',
        baseline_rows=[
            ['官方FullCodeRefl','同AppWorld代码执行与错误恢复','https://arxiv.org/abs/2407.18901','https://github.com/StonyBrookNLP/appworld；full_code_agent.py、environment.py与README已读','appworld run auto --agent-name simplified_full_code_agent --model-name {共同actor} --dataset-name dev；所有组同task/seed/API与token cap','是；未实跑'],
            ['强remaining-code提示','排除仅把部分执行事实说清楚','本地标准对照规范','同FullCode；加入成功效果、返回值、失败行并明确不得无意重跑已完成操作','与主方法同观测表；actor自由生成剩余code，不做CPU残余变换','是'],
            ['成功回执去重','一般避免重复写的强简单策略','本地标准对照规范；VTC仅作原理近邻','按执行实例的源码位置/循环索引/已知实际参数直接比较，若已成功写则重用原返回；不求纯表达式依赖闭包','同仪表记录、task/actor和预算，不使用幂等键或环境私有数据库','是'],
            ['无数据依赖的剩余后缀','检验返回值/局部依赖保持的独立作用','本地机制消融','在失败点继续修复，已提交写禁止重跑，但不替换已完成调用为返回表达式','同支持语法与执行记录；无效局部变量错误照实计入失败','是']
        ]))

def relational_counterexample():
    import copy
    c=copy.deepcopy(next(x for x in m.load() if x['id']=='IDEA-043'))
    for key in ['id','reviews','selection_notes','selected_was_pool_leader']:
        c.pop(key,None)
    c.update(status='available',parent='IDEA-043',score=8.4,title='逐字段接地仍会拼错关系：以联合值见证约束工具调用')
    c['claim']='研究对象不是HyperAgent实现是否遗漏某项，而是AppWorld agent在多对象调用中，把分别真实存在且类型正确的参数拼成无关系支持的组合。主张必须区分逐字段grounding与关系grounding：给每个关联参数一份来源，不自动给它们联合见证；运行时应保留具体返回行/父调用关系并按已公开的关联键join。原语relational join与dependent typing成熟，新意限联合值见证的调用反馈和预算内可证伪评测，不宣称所有schema-graph方法都做不到。'
    c['evidence_detail']='形成可直接检验的表示例子：R1={(x1,y1),(x2,y2)}与R2={(x1,y2),(x2,y1)}有相同单字段值集合、相同schema，(x1,y1)只在R1有联合见证。这个教材级例子只展示marginal-only控制丢失关系，不是新的定理，也不能证明HyperAgent整体state有此缺陷：其全文明确C保存history，I保存schema-value bindings，含deterministic runtime binding validation。Entity Binding Failures也已有多实体precondition gate，不能把“wrong entity”当首创。自然AppWorld跨关系错配频率尚需诊断。'
    c['method']+=' 只对公开文档/返回/实际输入明确支持的关系作判断。定义known supported、known contradicted、unknown三个结果：已知冲突给原actor纠正；unknown不能被冒充业务错误或自动拒绝完成任务。无完整关系枚举时不能凭当前tuple缺席证明组合全局无效。父参数与row keys形成真实有据关系，不强制所有关联参数同一物理row。'
    c['experiment']='实质改为两层验证：先用R1/R2同marginal不同关系的固定成对表示诊断，数据仅验证表示和控制能力、不报AppWorld自然成功率，也不输入gold给actor；再在原始AppWorld多对象任务独立标注自然组合错配、额外补查与合法跨行组合。同FC runner/actor/关联说明/全部raw返回/token和调用预算；比较native FC、逐字段观测值验证、same-invocation co-production检查、same-row tuple gate、跨行/父调用关系join见证。后三个控制完整本地规范：只要求同call、只要求同row、按显式键连接，分别隔离调用级联合、过度同源与业务关系。所有控制保留同全文raw历史，marginal-only仅为机制消融，不冒充HyperAgent。主方法若只是更保守、同row已有同效、显式关系覆盖低、自然错配没有实际影响或native同预算已会正确结合则停止。HyperAgent完整public implementation未核验，只作为已读强近邻，不暗示未覆盖其未知runtime。'
    c['story']='正确工具/错误实体已是已有问题；本案窄问题是各field可见不等于它们一起有支持；用同marginal反例清楚隔离信息差，再让公共关联键为参数组合给联合见证；若比同调用/同row控制更少错配与误拒绝，并改善自然同预算任务才支持。'
    c['reason']='直接读HyperAgent完整state定义与runtime binding说明、Entity Binding gate算法，删除无法核验的实现排除主张；最小实验实质增加同marginal反例及同call/同row强控制，8.4暂定需新独立review。'
    c['novelty']='已知实体接地/参数provenance/联合调用验证均已有；不声称它们没有联合约束。新意只限具体值关系的联合见证、未知覆盖不作否定和原始AppWorld预算内验证，需reviewer与关系类型/agent运行时最近方法比较。'
    c['independent']='对具体参数组合保留行/父调用关系的联合见证，区分已冲突与覆盖未知，并在同调用/同row对照中检验。'
    c['baseline_rows']=[c['baseline_rows'][0],
        ['逐字段观测验证','排除幻觉字段和值已足够','本地完整标准规范','每个参数在对应port的用户输入/真实公开返回出现，原actor据同关联说明组合；不执行关系join','同raw历史、actor与总预算','是'],
        ['same-invocation co-production','强调用级联合检查','本地标准控制；不冒充HyperAgent','关联参数值必须在同一实际成功工具调用的返回或其父输入出现，列表各row不进一步约束；独立新常量不强制同源','同row/call记录、业务说明和actor','是'],
        ['same-row tuple gate','强简单元组检查及过度限制对照','本地完整标准规范','关联参数必须有同一返回对象/列表row支持；来自不同row/call即报告缺联合支持（unknown仍不伪装业务错）','主方法和此组得到同显式关联键，差别为物理row限制vs有据自然join','是']]
    return new(c)

def joint_plan_repair():
    return new(dict(
        title='多约束行程修复中先找到被局部修补破坏的唯一支持，再联合修补',group='travel',parent='无',score=8.3,
        route='相似领域成熟方法迁移',keywords='constraint-aware planning；plan repair；TravelPlanner',
        background='规划agent修复一个预算或住宿错误时，怎样避免破坏先前已经满足的饮食、住宿和路线约束。',
        claim='TravelPlanner原文报告同时跟踪全局多约束困难。公开CORAL在补齐cuisine后为降预算删travel-day meals并替换酒店，这些实际操作可能移除某个cuisine的唯一见证或改变最低住宿要求；只证明失败可达，不证明发生率。主张一种局部修补单独看似合理，却必须和另一个槽位的支持转移一起才合法：CPU记录已满足约束的可见支持，找出候选编辑所移除的最后见证，并围绕它构建小型联合修补，再验整个候选，而不是每次都接受单编辑或每步要求永不暂时违反。',
        method='首版用官方sole-planning可见reference_information，不做额外城市检索；共享同一原actor从raw query提取的约束和候选表，不读取隐藏local_constraint/参考完整plan。输入初始结构化行程与当前违约；CPU为cuisine、restaurant distinctness、hotel属性/连续住宿、预算等已支持约束计算见证或数值依赖。原actor提出局部修改；若它删除最后一个required-cuisine见证或影响已满足住宿条件，就把相关可替代槽位加入小邻域，固定其它slots，在最多3个slot的联合候选中求低改动可行修补。允许联合候选构造的中间状态暂时违约，只在最终whole-plan公开规则检查后提交；找不到则扩大下一actor回合或返回未解决，不宣称无解。CPU不更改用户硬要求，不私下松budget，不预测不可见记录。SAT/CSP与neighborhood search是成熟原语，增量限agent提出的单修补与被破坏支持之间的转换和同预算诊断。',
        experiment='TravelPlanner原始sole-planning train/dev诊断真实修复序列：某约束通过→修另一项→原约束再次失败。统一候选池/原始query解析、actor/validator、CPU限时/总token/调用预算；比较官方ReAct/Reflexion、已核验CORAL、单编辑修补＋全局验后反馈、拒绝任何破坏已满足约束的单编辑、同3-slot随机邻域、支持见证定向联合邻域。保留CORAL原策略与原全局评分，不给主方法隐藏oracle；原CORAL无actor，不人为塞强模型，零模型成本照实报告。主指标最终all-constraints pass、修复摆动次数与完整成本；支持指标定向邻域相对随机同大小/单编辑的差别。若全局验单编辑已足够、单编辑拒绝不陷入僵局、自然repair regressions少、或全池标准CSP重建更便宜，则停止。主结论不外推到two-stage检索或真实旅行建议。',
        story='同时多约束失败已有证据，代码显示局部降价可删除既有支持；逐项修补可能产生来回摆动，强拒绝又可能堵住需要两步联合修改的路径；用被删最后见证引出相关候选槽位，将联合变更整体提交；若同预算比随机同大小邻域更少摆动且最终成功更高才支持。',
        reason='CPU/公开候选数据与两套真实planner入口已直接读，最低范围3-slot联合修补可以实现；constraint repair/LNS成熟，8.3是任务化因果诊断与支持定向邻域的暂定判断，需独立审查。',
        sources='[TravelPlanner](https://arxiv.org/html/2402.01622v1)§5.2全局约束；[CORAL公开solver](https://github.com/ChouYuanjue/coral-travel-planner/blob/main/src/coral/planning/travelplanner_solver.py)plan_query/_repair_plan/_inject_missing_cuisine已读；[sole_planning.py](https://github.com/OSU-NLP-Group/TravelPlanner/blob/main/tools/planner/sole_planning.py)与原greedy/budget工具已读；[ATLAS](https://arxiv.org/abs/2509.25586)已打开一级全文，checker/interleaved search近邻。',
        novelty='完整候选后定向搜索TravelPlanner repair+neighborhood/constraint preservation/joint repair，未见直接结果不证明新意。LNS、动态CSP、最小变更规划均是强成熟近邻；ATLAS已有全局checker，但需要reviewer判断支持最后见证到联合邻域是否超出直接组合。',
        independent='将agent局部修补移除的约束最后见证用作构造小型联合修补的依据，并用随机同大小/严格单编辑对照检验。',
        baseline_rows=[
            ['TravelPlanner ReAct/Reflexion sole-planning','同原始规划任务、同可见候选池','https://arxiv.org/abs/2402.01622','https://github.com/OSU-NLP-Group/TravelPlanner；sole_planning.py parser与Planner/ReactPlanner/Reflect入口已读，reference_information是此模式合法输入','cd tools/planner；python sole_planning.py --set_type validation --output_dir {slot} --model_name {共同API支持模型} --strategy react（或reflexion）；统一总预算，原脚本重试/后处理费用也计入','是；未实跑'],
            ['CORAL局部repair','同TravelPlanner已公开CPU局部修复强baseline','https://github.com/ChouYuanjue/coral-travel-planner','已打开真实TravelPlannerGreedySolver.plan_query/_repair_plan和run_travelplanner_planner.py；repo以原raw query解析，oracle-fields默认为false','pip install -e .；python scripts/run_travelplanner_planner.py --split validation --method coral --repo-root {TravelPlanner} --output-dir {slot}；禁用--oracle-fields，先确认提供候选与主方法同sole reference scope；官方evaluator只离线评分','是；源码核验未实跑'],
            ['单编辑＋全局反馈','强便宜既有范式','完整本地标准规范','同actor每轮只提交一个slot修改，CPU按全部共同显式约束检查并反馈，允许后续修复刚破坏约束','同候选/约束/预算，不提供hidden evaluator信息','是'],
            ['严格单编辑保持','排除只保护已满足约束','完整本地标准规范','任何单编辑导致原已满足显式约束失败便不提交，actor另选单编辑；不可借此降低任务成功分母','同规则/信息/调用预算','是'],
            ['随机同大小联合邻域','排除多改几个slot即可','完整本地标准规范','与主方法同最多3个slots、相同有限候选与CPU search cap，均匀选同数量slot而非按见证；同whole-plan检查','同actor proposals/种子/预算；未找到保持未解决','是']
        ]))

def extractor_replay():
    import copy
    c=copy.deepcopy(next(x for x in m.load() if x['id']=='IDEA-049'))
    for key in ['id','reviews','selection_notes','selected_was_pool_leader']:
        c.pop(key,None)
    c.update(status='available',parent='IDEA-049',score=8.3,title='修复工具返回提取器时，用已有公开样本排除破坏旧访问的候选')
    c['claim']='AppWorld报告输出字段臆造与接口误用，普通反馈可定位当前错误却不能证明修补不会破坏另一些已成功访问的返回。待诊断：针对当前empty/None/嵌套结构重写提取器，会改变其对已有返回样本的输出。贡献改为无新API调用的候选验证：把原actor提出的纯JSON提取器修补在已有公开输入上重放，排除异常或改变应保留观测输出的候选，并让原actor选择剩余修补；不声称旧访问输出是任务真值或已经解决数据语义。'
    c['method']='首版只支持输入一个真实公开JSON、输出任务后续使用值的无I/O提取表达式/短函数；原actor正常修复轮输出最多3个候选而非新增critic。CPU保存当前失败样本以及此前该提取器真实成功执行的JSON和观测输出，拒绝读写工具/文件的候选，只执行限定dict/list访问、guard、基础转换、简单组合。以前成功访问是有限行为保留约束，不当正确答案。候选在失败样本结构上可执行，同时在所有适用旧样本上保持原观测值；允许actor事先明确哪些旧行为本来就需改变，这些样本从保留集移到待判断，不能事后为了过关删样本。只报通过/反例，不提供当前失败样本的gold输出。后续actor负责语义选择，不能通过无条件None/空值或跳过所需动作当任务成功。所有不支持结构和样本保留成本照实报告，无hash/指纹，无外部重rollout。'
    c['experiment']='原始AppWorld完整schema下自然返回访问错误为主，首个诊断看修复后对旧样本的实际变化与任务后果。相同失败前缀配对恢复：普通FullCode、强局部修复提示、同数量候选+只测当前失败样本、同数量候选+CPU多样本结构测试、已有成功观测值保留验证；ACE no-GT完整原生流程作同任务强方法对照。所有候选组共用相同历史原始JSON/旧输出、相同最多3个候选和生成token cap，不免费给主方法更多信息/更多样本；不额外查询API，CPU成本计时，不能用hidden答案当旧输出。主指标最终TGC和真实恢复次数，次报当前错误修复但旧行为回归、非真值保留错误、vacuous提取和成本。若只测当前样本或简单多样本结构已同效、自然样本少、旧行为本来错误或仅减少异常而任务更差，则停止。'
    c['story']='原始字段误用为已报告问题；局部位置反馈没有跨旧返回的行为保持证据；用同一修复轮的少量纯提取器候选，在已经观察过的输入输出上验证并给反例；若原API预算不变而更少破坏旧访问且任务更好才支持。'
    c['reason']='由位置诊断实质转为纯提取器候选的无额外API多样本行为验证，新增CPU操作可直接实现；CEGIS和repair regression成熟，增量限stateful tool agent已有观测的低成本验证与同任务消融，8.3需独立审查。'
    c['novelty']='已读LDB（basic-block LLM语义调试）、VeriHarness（位置/观测/可行动反馈）、ACE、DRAFT/DocsChisel；不把纯类型反馈当新意。形成后需针对observed IO replay+agent extraction repair查近邻，CEGIS/regression是成熟原语，不声称行为一致等同正确。'
    c['independent']='不重跑工具或调用critic，用已观察过的真实JSON与原提取输出验证修补候选的有限行为保持。'
    c['evidence_detail']='AppWorld当前完整schema不被改变。自然字段臆造/接口错误由原文报告；“修当前样本会破坏旧提取行为”只是待诊断假设。一次结构成功不证明语义正确；同语义但不同提取器版本须明确支持范围，不能把跨接口样本混入保留集。'
    c['baseline_rows'][1]=['强局部修复提示','排除告知成功行为保留即可解决','本地完整标准控制','同原始样本/旧输出、失败访问和明确保留要求，原actor提一次修补；不做CPU候选重放','同actor/总token/API cap，辅助样本序列化计费','是']
    c['baseline_rows'][2]=['候选当前测试/多样本结构测试','隔离候选数与旧观测值约束','本地完整标准控制','所有候选组同最多3个候选；一组只检当前样本可执行，另一组检所有适用样本无异常及类型；主方法另要求保留既有观测值','限定纯表达式，实测CPU；不生成新任务/不使用gold','是']
    c['sources']+='；[LDB](https://arxiv.org/abs/2402.16906)、[VeriHarness](https://arxiv.org/abs/2607.14167)已直接读一级全文，作为定位/结构化反馈近邻，不当跨任务baseline。'
    return new(c)

def access_natural():
    import copy
    c=copy.deepcopy(next(x for x in m.load() if x['id']=='IDEA-047'))
    for key in ['id','reviews','selection_notes','selected_was_pool_leader']:
        c.pop(key,None)
    c.update(status='available',parent='IDEA-047',score=8.4,title='原始AppWorld中以访问需求定位结构错误，保留成功路径证据')
    c['background']='交互式代码agent即使有正确工具文档，仍可能访问不存在字段或误用当前返回；怎样以局部执行证据修复。'
    c['claim']='AppWorld当前schema可靠，原论文报告agent会臆造输出字段、误用接口及错误后难适应；这些是问题入口。尚未诊断的更窄假设是错误恢复会重新猜整个返回结构或将当前empty/None不当地解释成全局schema变化。主张局部访问需求诊断可帮助原actor修复当前矛盾，同时保留已成功路径；不声称这种误泛化常见或已测出效应。贡献是CPU从实际JSON访问表达式与公开返回生成局部矛盾，而不是优化完整文档。'
    c['experiment']='主实验改为原始AppWorld完整文档与真实自然执行错误，不改变工具/数据/schema，先独立分类失效并验证该窄假设是否有足够样本。相同自然失败前缀配对恢复与原生end-to-end分开；对照官方ReAct/FullCode、同原始返回+局部error prompt、同token全量shape摘要、ACE no-GT原生及本方法。原始task TGC、重复访问错误、恢复是否损坏已有成功路径、完整成本为指标。仅在主诊断通过后另做response_schemas去除消融：原文Appendix A确实明确提出该未来方向，但未提供原论文实跑分数；官方load(include_response_schemas=False)/remove_fields及show_api_response_schemas=False控制所有静/动态文档入口，消融分数单独命名。不将空值误泛化当事实，不靠修改benchmark制造主结果。若普通error反馈/ACE已等效、自然结构误用低频、CPU只是提供更多原始数据、或为保证成功过度拒绝则停止。全部构建、reflector、instrumentation/失败/API/token按共同上限计费。'
    c['story']='原论文已有真实输出字段臆造/接口误用；是否恢复过程中扩散到其它正确路径还需诊断；把实际访问需求与当前返回对照，给局部矛盾并保留成功证据；若在原始同预算任务恢复更好而非仅在删除schema条件有效，才支持。'
    c['reason']='主实验实质切回原始可靠schema的自然错误，而非blind诊断；一级原文已直接核验故障分类与Appendix A真正内容，所有窄因果链保持假设，8.4暂定新意/可行性需新reviewer。'
    c['evidence_detail']='主执行器直接打开AppWorld原文Appendix A，原文确有“ablating response schemas from the documentation”及下一段future works；这只证明提出未来方向，不证明原论文已跑该协议。当前主实验保留原始完整文档。自然输出字段臆造是原文错误分析，empty/None误泛化及路径损坏比例尚未知，必须先诊断。'
    c['novelty']='已直接读AppWorld/ACE/DRAFT/DocsChisel；结构化反馈和schema经验已有，保留访问表达式需求、当前返回首矛盾及成功路径证据的窄机制。主问题独立于schema-blind消融，类型error诊断不是新理论，需独立查最近agent定位工作。'
    c['baseline_rows'][0][4]='appworld run auto --agent-name simplified_full_code_agent（或simplified_react_code_agent） --model-name {共同actor} --dataset-name dev；主实验原始完整文档/真实环境，blind消融另报'
    c['baseline_rows'][-1][4]='从已核验ACE AppWorld fork源码安装；appworld run ACE_offline_no_GT_adaptation再ACE_offline_no_GT_evaluation，或ACE_online_no_GT；主比较均保留完整API文档，统一actor/reflector/train流/全部构建与query预算，不给GT或免费playbook'
    return new(c)

def row_mask():
    return new(dict(
        title='标签相同但数据行已变：布尔筛选在数据分析agent中的行绑定诊断',group='da',parent='IDEA-044',score=8.2,
        route='最高近邻不足',keywords='data wrangling；execution feedback；data provenance',
        background='数据分析agent排序或重设索引后复用旧布尔mask时，怎样发现合法标签对齐实际筛选了另一批数据行。',
        claim='DA-Code报告代码可执行但任务语境误解，RADAR已检查schema/row count/绑定列/显式join，并保留操作与输入表记录；这些证据不直接证明Python布尔mask与目标数据行仍对应。待诊断窄失效：mask在原df计算，df经sort/filter/reset_index后原整数标签被重新使用，旧mask依然合法、长度/类型可一致，却落到另一批行。贡献只限由公开执行构建的行身份对应，诊断mask来源与当前行身份的分离；不发明pandas对齐或一般血缘。',
        method='首版只支持一个Python action内部read_csv、纯行变换sort_values/drop行/reset_index和由列比较形成的Boolean Series，再用[]/.loc选行；不处理join/groupby或改列值后的谓词时效。CPU为自己读取的表分配顺序行ID（普通元数据，无hash/指纹），跟随上述变换传播对应表；mask保留每个bool的来源行ID。当pandas按标签对齐时，比较实际目标行ID与该bool原来源，返回首个不一致的可见行/谓词例子。默认只给原actor修正提示，不能仅凭标签不同判错；公开源码显式按位置的mask不纳入。纯行重排可按ID重附旧bool作单独消融；如果谓词值被改或行出处未知保持unknown，不自动修。',
        experiment='DA-Code公开CSV的DW/DM/EDA，排除ML与GPU任务，先独立盲标自然mask复用错误；CPU行绑定机制比较DA-Agent、DS-STAR完整原生验证、同shape/index唯一性反馈、通用总是重算mask强策略、行来源诊断（另测纯行变换重附）。所有组同公开原始文件/任务、同actor和各辅助模型、总token/API/执行预算；同Python操作观察，只改变反馈。RADAR完整代码未在一级论文给出仓库，若无法核验不冒充可运行baseline；将其明确公开的schema/rowcount/列绑定/显式join规则完整实现为本地简单runtime-check控制，不标RADAR原作者分数。评价官方table match/成功与误筛行、误报、无法覆盖及CPU成本；若重算mask已等效、自然错误罕见、来源记录开销更大或主要操作不支持就停止。',
        story='公共pandas语义会按label对齐，实际schema和行数正确不说明mask的业务行身份正确；记录行变换前后对应而非只存表metadata；让actor看到具体错配并重算或重附mask；只有同预算修复自然错误且超过简单重算/强验证才值得做。',
        reason='API/CPU数据分析入口及DS-STAR实际plan/code/verify源已读，方法比父候选从聚合换权转为可精确执行的mask-row绑定；row provenance成熟，8.2暂定需独立审查。',
        sources='[DA-Code](https://arxiv.org/abs/2410.07331)及PromptAgent/PythonController；[RADAR](https://arxiv.org/html/2609.32528v1)§3已读；[pandas indexing](https://pandas.pydata.org/docs/user_guide/indexing.html)；[DS-STAR](https://arxiv.org/abs/2509.21825)及run_ds_star.py、agents/ds_star.py、tools/llm.py已读。',
        novelty='具体候选后定向检索pandas agent mask alignment、DataFrame provenance index alignment，无直接结果不是新颖证明。FlowBook/Kishu已有cell依赖与可复现状态，RADAR已有typed records；本案只保留同样正常执行可复现却选错行的身份错配，需要reviewer检索。',
        independent='以公开行变换的对应关系验证Boolean Series复用，而非用schema/长度/标签相同充当语义行绑定。',
        baseline_rows=[
            ['DA-Agent on DA-Code','同CSV数据分析与表输出','https://arxiv.org/abs/2410.07331','https://github.com/yiyihum/da-code；run.py、PromptAgent、PythonController已读','python run.py --model {共同actor} --task_config da_code/configs/task/dm.jsonl --source_dir da_code/source --max_steps {共同} --max_memory_length {共同} --max_tokens {共同} --example_index {固定} --output_dir {slot}；CPU Docker','是；未实跑'],
            ['DS-STAR原生','同DA-Code已发表强验证基线','https://arxiv.org/abs/2509.21825','https://github.com/google-research/ds-star；run_ds_star.py真实parser、agents/ds_star.py coder/debug/verify/router、tools/llm.py已直接读','每公开任务复制instruction到tasks/{id}/question.txt，guidelines.txt提供同格式说明（实际无论是否optional均会读取），source文件到data；python run_ds_star.py --task {id} --llm {共同支持gpt/Gemini快照} --debug_round {cap} --max_round {cap} --max_workers 1；原LLM helper未强制total token，统一补调用边界预算与输出上限/共同采样配置；所有file分析/verify/router计费，不改算法','是；源码核验未实跑'],
            ['通用mask重算','强便宜对照','本地标准规范','每次sort/filter/reset_index后，用实际支持且保存的原列比较表达式在当前df重算mask；不支持则unknown，不能自动猜predicate','同采集/表达式与actor，CPU耗时完整记账','是'],
            ['schema/index与runtime checks','一般可见检查，隔离row identity增量','pandas规范＋RADAR公开规则，不称复现RADAR','记录dtype/shape/len、index唯一性，执行SQL时按已见schema验列、要求多行隐式join有显式键；所有规则CPU可直接实现，Python不追加行身份追踪','同可见数据、反馈额度与执行预算；RADAR全文无可核验官方代码，不列其原作者算法基线','是；标准本地控制']
        ]))

def access_contract():
    return new(dict(
        title='无返回schema时按实际访问表达式诊断局部结构矛盾',group='app',parent='IDEA-017',score=8.3,
        route='相似领域成熟方法迁移',keywords='API documentation；interactive coding agents；execution feedback',
        background='代码agent不知道工具返回schema时，怎样从实际返回和自己代码中找出真正被否定的结构假设。',
        claim='AppWorld现有文档由FastAPI自动生成且可靠，不能声称自然schema过时；其Appendix A提出去掉response schema后通过交互理解返回。主张这一明确schema-blind设置下，单个KeyError/TypeError常被当成整个接口理解错误，或把当前空列表/nullable值当全局类型改变。研究增量是将实际访问表达式转成局部结构需求，在同次公开返回上找最小矛盾并保留已有成功访问的证据，而非重写工具文档或推断完整全局schema。',
        method='首版支持JSON返回、dict/list索引、简单属性路径和int/float转换。CPU在API返回后为actor自己的访问表达式记录路径和所需container/key/length/value type，并在当前公开对象验证；从根到叶给首个实际矛盾及该前缀的可见结构，保留其他已经成功的路径。empty list只否定当前索引可达，不证明element schema缺失；None只否定无guard直接转换，不自动改全局字段类型；报错调用返回与成功返回分开。原actor修访问/补查询，不自动把相似名字字段替代，不把反例当数据语义真值。新增CPU机制不给模型更多业务答案、隐藏schema或数据库。',
        experiment='冻结schema-blind版本：全部任务允许API的公开response_schemas统一移除，参数/功能文档和真实执行不改，非按主方法错误挑endpoint。实际ApiDocCollection.load(include_response_schemas=False)与remove_fields([response_schemas])接口已直接读；静态world.task.api_docs渲染走同一无schema副本，动态API文档显示通过AppWorld show_api_response_schemas=False处理；若还有response schema渠道可见，该任务不纳入blind分数。完整schema原协议单独报告，不混分。对照FullCode/ReAct、同公开返回+局部error prompt、每次全量返回shape摘要、ACE no-GT原生增量playbook、访问需求矛盾。各组同actor/reflector能力、任务/顺序/seed/文档/失败/总token及API调用预算；ACE构建反思不免费。先诊断本次结构失败与反例误泛化，再评价TGC/重复结构错误/成本；若ACE或直接error同效、只靠多给结构信息获益或自然blind任务无所述失误则停止。',
        story='原benchmark可靠schema是事实，删去schema是原文明确的更难setting；一次失败不能否定所有成功路径或将数据空值解释为schema变化；在实际访问需求处定位矛盾，保留其它证据；在同信息/预算下更少反例误泛化且任务更好才支持。',
        reason='公开schema去除API、真实FullCode和ACE no-GT入口均已读；比父候选实质改变为代码访问需求的局部诊断，并冻结可运行setting，类型错误诊断原语成熟，8.3需独立review。',
        sources='[AppWorld](https://arxiv.org/abs/2407.18901)Appendix A；[ApiDocCollection源码](https://github.com/StonyBrookNLP/appworld/blob/main/src/appworld/collections/api_docs.py)load/remove_fields实际接口；[DRAFT](https://arxiv.org/abs/2410.08197)、[DocsChisel](https://arxiv.org/abs/2608.10037)、[ACE](https://arxiv.org/abs/2510.04618)均已打开一级全文。',
        novelty='直接读DRAFT/DocsChisel已覆盖交互后文档优化，ACE覆盖局部context delta；本案不以文档修订为创新，限定CPU access-requirement与当前返回的最小矛盾、empty/null解释及成功路径保留。类型诊断、动态schema inference成熟，需要reviewer判定agent场景差别是否足够。',
        independent='以agent实际JSON访问的结构需求定位当前矛盾，不由一份反例全局重写schema或忘记成功访问。',
        baseline_rows=[
            ['官方ReAct/FullCode','同AppWorld schema-blind任务','https://arxiv.org/abs/2407.18901','https://github.com/StonyBrookNLP/appworld；真实agent、ApiDocCollection.load/remove_fields及environment已读','appworld run auto --agent-name simplified_full_code_agent（或simplified_react_code_agent） --model-name {共同actor} --dataset-name dev；实验副本统一无response_schema文档；原完整schema另报','是；未实跑'],
            ['局部error prompt','排除只提醒别整体重猜已足够','完整本地标准规范','实际raw返回、stack trace与成功访问记录同主方法，提示只修失败路径；不计算结构需求最小矛盾','同actor/信息/预算，不再用强模型','是'],
            ['全量shape摘要','排除纯返回压缩/概览效益','完整本地标准规范','每次返回CPU枚举字段路径、当前类型/空值，按相同feedback token cap供actor；不绑定具体访问表达式需求','同原始返回记录、上下文额度和API预算','是'],
            ['ACE no-GT on AppWorld','同任务执行反馈增量context强近邻','https://arxiv.org/abs/2510.04618','https://github.com/ace-agent/ace-appworld；adaptation_react.py、adaptation_agent、generator/reflector no-GT提示和config真实内容已读','从官方fork源码安装；appworld run ACE_offline_no_GT_adaptation再ACE_offline_no_GT_evaluation，或ACE_online_no_GT；统一同schema-blind副本、actor/reflector快照、train流和总成本，不给GT与免费playbook','是；未实跑']
        ]))

def test_delta_strong():
    import copy
    c=copy.deepcopy(next(x for x in m.load() if x['id']=='IDEA-045'))
    for key in ['id','reviews','selection_notes','selected_was_pool_leader']:
        c.pop(key,None)
    c.update(status='available',parent='IDEA-045',score=8.3,title='固定测试策略下的跨轮回归反馈分配，直接对照测试定位与输出剪枝')
    c['method']+=' 跨轮比较仅限共同执行且测试源未改的nodeid；保存公开测试源码直接比较，不加hash；测试/fixture被actor修改时不把原状态称同一检验。只称状态变化，不称已定位唯一根因。'
    c['experiment']='采用因子化最小实验：同MiniSWE actor与SWE-bench任务，测试执行策略分别为原生、公开TDAD的impact map、公开TestLoc/TestPrune工具；每个策略内部固定相同测试来源、预算和反馈机会，对照head-tail、单次结构化、官方Squeez以及跨轮状态差分反馈。保留TDAD/TestLoc原生选测能力，另在同样已执行测试公共支持上隔离呈现机制，不把阉割对照当完整方法。Squeez用公开已训2B模型device=cpu，或官方150M extractive作为辅助强对照，不训练；完整CPU时间/内存与模型调用计费，不能假设CPU免费。全部组可请求同原始日志；评测只用隐藏evaluator离线评分，不注入其P2P/F2P标签。若已有选择/压缩方法已足够，停止；必须先诊断自然遮蔽频率。'
    c['reason']='核心边界保持跨轮共同test状态差分；实质增加3种原生测试策略×反馈呈现的强方法比较，已直接读公开TDAD/TestLoc/Squeez真实入口和设备参数，补齐归因缺口，8.3暂定需新reviewer。'
    c['sources']+='；[TDAD](https://arxiv.org/abs/2603.17973)/tdad.cli index/impact/run-tests已读；[TestLoc](https://arxiv.org/abs/2510.18270)/src.run_pipeline及工具bundle已开；[Squeez](https://arxiv.org/abs/2604.04979)/inference.extractor设备与extract路径已读。'
    c['novelty']='已直接读TDAD回归防止、TestLoc测试选择、Squeez单次任务条件压缩和AgentDevel的P→F原理；不把这些原语当新。当前更窄目标只比较同一执行策略下的跨轮反馈分配，不靠少执行测试或更好定位获益。'
    c['baseline_rows']+= [
        ['TDAD原生选测','同SWE-bench回归控制最高近邻','https://arxiv.org/abs/2603.17973','https://github.com/pepealonso95/TDAD；tdad/src/tdad/cli.py已直接读，NetworkX index与impact真实分支','pip install -e tdad；tdad index {repo}；tdad impact {repo} --files {changed}；tdad run-tests {repo} --tests {nodeids}；其skill/map给相同MiniSWE actor，索引和测试费用全计入','是；未实跑'],
        ['TestLoc/TestPrune原生','同SWE-bench公开测试定位/缩减','https://arxiv.org/abs/2510.18270','https://github.com/IBM/Issue-Test-Localizer；run_pipeline.py真实4阶段及README的tools/regression_tests集成已核验','python src/run_pipeline.py --instance_id {iid} --model {共同actor} --dataset princeton-nlp/SWE-bench_Verified --log_dir {slot} --max_workers 1；minimized_tests.json按官方regression_tests工具接同MiniSWE，不用免费预计算gold；定位LLM/coverage开销计费','是；源码核验未实跑'],
        ['Squeez输出剪枝','同pytest/stacktrace反馈压缩最高近邻','https://arxiv.org/abs/2604.04979','https://github.com/KRLabsOrg/squeez；真实ToolOutputExtractor.__init__、transformers/highlighter CPU分支、extract已直接读','ToolOutputExtractor(model_path=KRLabsOrg/squeez-2b,device=cpu,max_length={公开支持限}).extract(task={同issue},tool_output={原始日志})；150M模型KRLabsOrg/verbatim-rag-modern-bert-v2另报，不混称2B结果；CPU时间/内存计入且无训练','是；未实跑']
    ]
    return new(c)

def test_delta():
    return new(dict(
        title='测试反馈裁剪时区分本轮新回归与原有失败',group='swe',parent='IDEA-015',score=8.2,
        route='最高近邻不足',keywords='software engineering agents；execution feedback；SWE-bench',
        background='编码agent在多次修复后，怎样从有限测试输出中看到本轮新引入的回归，而不是继续追旧的报错。',
        claim='已读MiniSWE实际SWE-bench配置：超过10000字符只保留前后5000，returncode只有整次命令层面状态。待诊断具体失败是已有失败和重复日志占据可见头尾，本轮新回归的test/exception在中间被裁掉，agent继续修旧问题并积累破坏。贡献限在共同已执行的测试上保持前后状态差分，优先让反馈预算展示新增回归及代表反例；不是发明差分测试、失败聚类或pytest报告。',
        method='首版仅处理真实pytest调用和公开可运行测试；各组同pytest plugin收集test nodeid、执行状态、exception/traceback公开信息。CPU比较同suite公共已跑test前后状态：之前pass现在fail为新回归，之前fail现在pass为修复，未跑/skip/collection错误不当通过。反馈先给变化计数，再保留新回归的test ID、首个项目栈帧、具体断言，剩余空间给原有失败；同类型同项目栈帧的重复仅选一个代表并给数量，规则冻结，不用LLM/指纹/hash。如果没有可比较前次结果则退回单次结构化反馈。完整日志都留在可见文件，所有方法都能按工具预算请求。没有新增shadow tests或隐藏bench evaluator，真值只离线评测。',
        experiment='SWE-bench Lite/Verified中可执行公开pytest的实例，统一MiniSWE/API模型和所有执行预算。先诊断自然截断是否隐藏新增回归，再比较native head-tail、pytest --tb=short/--maxfail强控制、同一次结构化按test排序、仅失败聚类、状态差分优先反馈。所有方法有同完整日志与plugin采集，不额外给主方法免费测试；初始前次测试没有则不制造真值。主指标resolved和后续回归；次报新回归可见率、无谓修复轮数、完整token/命令/CPU。若强简短pytest已够、没有真实新回归遮蔽、单次结构化同效或公共测试覆盖不足即停止。',
        story='公开实现明确裁剪中段；若新增回归隐藏在中段，标量exit code无法区分正在解决还是又引入错误；用共同测试状态差分分配有限反馈；在同token预算观察到更少忽略新回归和更高resolved才支持。',
        reason='测试与反馈公开、明确可达裁剪条件，CPU差分便宜；primitive很成熟，新意依赖真实agent回归遮蔽及相同反馈预算闭环，8.2需独立验证。',
        sources='[MiniSWE实际SWE-bench配置](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/config/benchmarks/swebench.yaml)，head-tail模板已直接读；[run guide](https://github.com/SWE-agent/mini-swe-agent/blob/main/docs/usage/swebench.md)；[SWE-bench](https://arxiv.org/abs/2310.06770)。',
        novelty='候选形成后定向检索coding-agent test-feedback+new regressions/differential与truncation，未找到同构但不是新意证明；CI regression prioritization、差分调试、feedback selection为强近邻，需reviewer检索。',
        independent='将agent上轮与本轮已执行公共测试的状态变化用于有限反馈预算，而非按输出位置裁剪或只聚合本轮失败。',
        baseline_rows=[
            ['MiniSWE on SWE-bench','同真实issue修复与repository tests','https://arxiv.org/abs/2310.06770','https://github.com/SWE-agent/mini-swe-agent；default.py、run/benchmarks/swebench.py与swebench.yaml已读','mini-extra swebench --model {共同API模型} --subset lite --split test --slice {固定范围} --config {各臂同cap配置} --workers 1 --output {slot}；CPU Docker/x86 Linux','是；未实跑'],
            ['pytest简短反馈','强便宜已有测试呈现','https://docs.pytest.org/en/stable/how-to/output.html','本地标准命令控制：--tb=short，不改已选suite；另将--maxfail视作较少执行的独立强控制并完整记录未跑test','同MiniSWE和反馈token cap，maxfail未跑不能算通过','是'],
            ['单次结构化输出','排除只是删除噪声日志','本地完整标准对照','同plugin本轮test状态、首项目帧与断言，按nodeid排序装入同token上限，无跨轮比较','同已有结果、相同日志访问预算','是'],
            ['仅失败聚类','排除相似失败去重','本地完整标准对照','按exception类型与首项目栈帧直接分组，逐组轮转取代表+数量，不计算pass-to-fail差分','同采集/执行/反馈cap，无hash或额外LLM','是']
        ]))

def grain():
    return new(dict(
        title='数据分析agent在合法变换中丢失统计单元的执行诊断',group='da',parent='无',score=8.3,
        route='相似领域成熟方法迁移',keywords='data wrangling；exploratory data analysis；execution feedback',
        background='数据分析agent执行无异常的join/groupby后，怎样发现目标统计单元已经被悄悄重复或改成了另一种加权。',
        claim='DA-Code报告任务误解与持续错误，并公开dm-csv-010要求先求每月销量总和、再按月取均值的任务和多表orders/order_items数据。待诊断的具体失败是每步Python与join合法，最终却按交易行平均而非按月平均，或把合法一对多join造成的重复实体当成多个统计单元。主张执行反馈需说明目标单元在变换中的权重，而非只有shape/dtype/代码是否跑通；CPU追踪明确单元键和聚合层级，向原actor返回导致加权改变的最小可见例子。',
        method='原actor在正常计划中从明确任务文字声明聚合单元键、分组、sum/mean/count层级以及所需总体范围；各组共用同一声明，不给主方法人工正确plan。CPU在Python action内记录支持的read_csv/merge/filter/groupby/aggregate操作的实际关系，使用已有公开实体键或行序号，不用hash。对目标单元保留进入聚合前的重复次数与已经完成的归约层级；只有任务要求一单元一票、而实际mean/count使用行权重或SUM重复了单元级常量时返回反例，允许合法交易级sum和有意一对多。不能自动drop_duplicates，因为那可能删掉真实交易。原actor据证据修改代码；模糊单元或无法跟踪操作为unknown，不能伪造正确聚合。它不解决所有语义错误、不读gold输出。',
        experiment='DA-Code公开data-wrangling/EDA任务，首版不用ML训练；先诊断自然错误轨迹中的聚合层级/权重错配，再做相同前缀配对恢复。比较DA-Agent、同声明+反思、shape/dtype/row-count profiling、pandas merge validate+indicator、目标单元/聚合层级执行反馈。所有组同actor/数据/任务/步数/历史窗口/输入输出token与总调用预算；CPU算力计时。评价原任务table match和完整成功，另报错权重修复/误报。若目标声明常错、只是多给一个反思轮已等效、merge validate已够或只在人工错误有效则停止。',
        story='公开任务确实要求多层聚合而baseline有任务误解入口；正常shape和合法join不足以说明一月一票还是一行一票；把实际执行的单元重复次数与归约层级暴露出来；若原actor同预算能修好自然统计权重错误才有价值。',
        reason='任务、关系数据和公开Python执行口已核验；关系bag语义和grain建模成熟，研究增量限agent的执行反馈与聚合错配诊断，8.3暂定需review。',
        sources='[DA-Code原文](https://arxiv.org/html/2410.07331v2)§5.4；[公开任务dm](https://github.com/yiyihum/da-code/blob/main/da_code/configs/task/dm.jsonl)，已只读instruction；[pandas merge文档](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)；run.py/PromptAgent/PythonController已读。',
        novelty='完整候选形成后定向搜索data analysis agent+grain/denominator，未找到同构不能据此证明新颖；semantic layers、数据库bag provenance和数据验证为强成熟近邻，需reviewer检索并判断不是给pandas加断言的简单重命名。',
        independent='在agent实际生成的多步数据变换中，用目标单元权重和归约层级的执行证据诊断合法代码下的统计对象错配。',
        baseline_rows=[
            ['DA-Agent on DA-Code DW/EDA','同数据分析任务、公开真实数据','https://arxiv.org/abs/2410.07331','https://github.com/yiyihum/da-code；PromptAgent、run.py parser、PythonController和README已读，Docker CPU+API','python run.py --model {共同actor} --max_steps {cap} --max_memory_length {共同} --max_tokens {共同} --task_config da_code/configs/task/dm.jsonl --source_dir da_code/source --example_index {固定} --output_dir {slot}；实际eval config名eval_all.jsonl而README例子旧名，正式脚本用parser核对值','是；源码核验未运行'],
            ['同聚合声明+反思','排除自然语言任务拆解/额外反馈已足够','本地完整标准控制','所有方法共用初始目标单元声明；每次代码后同actor依据原输出反思一次，计入总预算','同一PromptAgent，不给额外正确plan','是'],
            ['shape/type/row count profiling','一般数据质量检查','本地标准对照','在支持的变换前后记录shape、dtype、null计数、行数和关联键唯一性；摘要同token cap','和主方法同CPU采样及反馈机会，不追踪目标单元权重','是'],
            ['pandas validate+indicator','强现有join基数检查','https://pandas.pydata.org/docs/reference/api/pandas.merge.html','实际merge(validate=原actor所声明的1:1/1:m/m:1,indicator=True)并反馈异常/left_only/right_only；原actor选合法m:m时不强报错','同声明/表/代码，不训练、无需隐藏checkpoint','是']
        ]))

def tuple_bindings():
    return new(dict(
        title='工具参数可用不等于同一对象绑定可用：保留返回行的联合来源',group='app',parent='无',score=8.4,
        route='最高近邻不足',keywords='tool-schema dependencies；state-conditioned planning；AppWorld',
        background='工具agent在同时拿到多对象的同类型参数后，怎样避免把来自不同对象的字段拼成一次调用。',
        claim='HyperAgent以schema可用性和port依赖做状态条件工具规划，原文不足讨论同名参数的多个producer及联合可用；更窄的待诊断失败是每个参数都有来源、整体schema也合法，却把不同返回行或不同父调用的对象ID/属性错配。主张可执行性还需公开返回行/父参数能见证一组关联输入的联合绑定；CPU保留关系元组并做带已知实体关联约束的join，而不把可用参数降为独立集合。并非发明数据库join，也不泛称解决实体消歧。',
        method='在同AppWorld FC runner记录每次公开工具调用参数及逐调用返回。每个返回对象或列表行保留本轮调用和行号，相关父参数（如order_id）附在该行。关联约束只能来自用户请求、公开文档的输入输出描述和实际返回中的实体关联键；原actor初次解释工具时输出关联组与port对应，同一次调用计费。CPU为下一动作建立候选关系元组，以明确owner/id连接键自然join相关字段，常量/独立的新值不被强制与对象同源。参数分别找到但没有联合见证则让原actor选补充查询或改绑定；不凭类型相同/字符串相似认定实体相等。不要求所有参数同一物理row，不将同一user下的所有order当成同一order。不读环境数据库或评测器字段；未知关联保持未验证，不伪造关系。',
        experiment='AppWorld多对象读写任务先独立检查每参数有观测来源而组合跨行/跨父调用的错误是否出现。共用FC动作接口、同actor/schema上下文和观察预算；比较native FC、相同结构化参数来源表、每字段provenance检查、schema-set可用性控制、联合元组绑定。完全相同的关联说明给简单控制，唯一区别是保留独立集合还是关联元组。主指标同预算task success、关联输入错配与不必要补查；盲标将真的错配与合法跨对象组合分开；不靠减少执行次数的拒绝策略冒充成功。未出现错误、未知关联覆盖过低、只靠强提示已解决、或严格join阻断合法调用时停止。',
        story='多个producer和schema可用性是已报告规划问题；独立字段来源无法证明一起属于同一目标；把返回行及父调用变成联合见证，再检查关联参数join；若比逐字段provenance更少错配并提升相同预算成功率，才支持。',
        reason='API输入和逐调用返回均可见且已有FC实现，关系运算CPU可做；依赖图和数据血缘成熟，新意边界是联合绑定丢失导致的agent错配，8.4仅暂定。',
        sources='[HyperAgent](https://arxiv.org/html/2608.02650v1)，preliminaries/method及当前state；[AppWorld](https://arxiv.org/abs/2407.18901)，FC agent源码已读；In-N-Out仅通过HyperAgent介绍了解，确切一级来源尚需检索，不用未核实链接作证据。',
        novelty='具体化后需定向检查entity-aware tool planning、dependent types、provenance/relational bindings；HyperAgent的schema-levelgraph不是同一对象联合值保证，不能据此断言所有图方法均忽略此问题；需要reviewer确认。',
        independent='把工具关联输入的可执行性从逐参数存在改为可见行/父调用关系支持的联合绑定。',
        baseline_rows=[
            ['官方AppWorld FC','同AppWorld多对象API任务','https://arxiv.org/abs/2407.18901','https://github.com/StonyBrookNLP/appworld；SimplifiedFunctionCallingAgent已读，ExecutionIO逐调用参数/返回可见','appworld run auto --agent-name simplified_function_calling_agent --model-name {共同actor} --dataset-name dev；固定同API/token/model/task cap','是；未实跑'],
            ['结构化独立来源表','排除只是ID/来源结构更清晰','本地标准对照','每field列可见value、call与row，交同actor；不做联合求解，仍接同关联说明','同公开返回、同actor和输入输出预算','是'],
            ['每字段provenance检查','排除只验证值不是幻觉','本地标准对照','验证每个参数value曾在匹配port的实际返回/用户输入出现，但不要求关联输入可join','同来源表，不读私有状态','是'],
            ['schema-set控制','定位丢失联合性机制','完整本地标准控制；不是无公开代码的HyperAgent复现','保留每schema字段可用value集合，所有必需字段非空即可交actor填参；相关说明/文档同主方法','同FC runner，CPU策略直接实现，不能标原作者HyperAgent分数','是']
        ]))

def variation():
    return new(dict(
        title='从已发生的变更提取独立变化轴，控制迭代代码的分支交叉增长',group='scb',parent='无',score=8.2,
        route='相似领域成熟方法迁移',keywords='iterative specification refinement；structural erosion；coding agents',
        background='迭代编码agent在增加新需求时，如何避免把不同变化维度不断塞进同一段分支。',
        claim='SlopCodeBench报告通用clean-code/plan-first提示不能阻止逐轮质量退化，并展示同一主函数不断叠加language、rule-kind等分支。待验证假设：仅按AST近似重复抽函数会把真正变化维度混在一起，导致下一次扩展又重复切开。贡献限按已发生的需求差异与代码差异提取独立变化轴，只在已有两个以上实例显示该轴时生成参数化共享骨架；不预测未来需求、不预造兼容层。',
        method='每轮在工作区保留上轮公开spec、自己代码和变更diff；CPU AST对齐产生同轮改动的近似同构区域，anti-unification得到共有骨架和变化孔。原actor在同一次正常分析中将每个孔绑定到当前spec的已有维度（如语言、匹配方式），并指出哪些孔必须联合变化。CPU保留只有一个维度不同的已观察实例作为分离证据，联合变化或没有证据的孔不独立抽象。模型据此做一次局部重构或直接新增；所有生成和自测计费。重构不得引入尚未出现的接口/feature flag，不读下一checkpoint spec或隐藏tests。用公开例子和actor自己产生的测试验证当前行为，并保留候选实际失败；低CC不是正确性oracle。',
        experiment='SlopCodeBench当前公开Python问题序列，在同MiniSWE actor、spec、初始空工作区、任务顺序、统一token/step/cost上限下比较baseline、原anti_slop/plan_first提示、CPU近似clone驱动抽取、每轮固定重构、按已观察变化轴重构。actor各组相同模型与推理档，主方法保留diff的其他组也可见。主终点是下一checkpoint同预算严格正确率/完成成本，当前重构后的hidden evaluation只离线评分，禁止反馈agent；辅助报侵蚀/重复。若仅改善自身优化的CC或clone指标而无未来完成/成本改善，否定研究。对同一累计spec的继续编辑与from-scratch控制分开，避免将增加需求等同迭代本身造成退化。',
        story='已报告分支与复制逐轮增长，干净代码提示不足；近似重复并不说明两个区域将同样变化；用已经发生的独立变化实例限制抽象，避免过早抽错或被动不断复制；若后续checkpoint更容易且不牺牲当前正确性才支持。',
        reason='已读问题序列和可API/CPU运行MiniSWE实现；机制原语anti-unification成熟，新意需落在变化证据限制抽象的迭代agent闭环，暂定8.2需审查。',
        sources='[SlopCodeBench全文](https://arxiv.org/html/2603.24755v1)，§4.1分支增长、§4.3提示对照；[公开代码](https://github.com/SprocketLab/slop-code-bench)；已读miniswe实现/配置与run文档。',
        novelty='候选完整形成后定向检索LLM refactoring+clone+anti-unification及iterative specification；没有据此证明新颖。自动提炼clone与change-coupling均为成熟相关工作，必须由reviewer判断变化证据条件是否独立成立。',
        independent='只用已发生spec/代码变化的单维实例，约束agent何时提炼共享骨架，并用后续可修改性检验。',
        baseline_rows=[
            ['SlopCodeBench MiniSWE','同一迭代spec+自己代码工作区','https://arxiv.org/abs/2603.24755','https://github.com/SprocketLab/slop-code-bench；src/slop_code/agent_runner/agents/miniswe/agent.py与configs/agents/miniswe.yaml已读，实际DefaultAgent/API model/local或Docker环境','uv sync；slop-code run --agent configs/agents/miniswe.yaml --model {共同API模型} --problem {冻结问题}；cost_limits指定相同step/token/cost（原论文无cost上限，重报此协议不冒充原分数）','是；未实跑'],
            ['anti_slop / plan_first','原论文同任务提示干预','https://arxiv.org/html/2603.24755v1#S4.SS3','公开prompt模板与文档；需用同MiniSWE而非换native模型','同run入口 --prompt anti-slop / plan-first：正式实现先核对当前模板名；原文对应完整提示可本地移植，token计费','是；提示内容可直接本地实现'],
            ['仅clone/anti-unification','排除一般重复检测与抽函数收益','本地标准算法规范','Python AST去位置后做结构对齐；相同节点保留、不同常量/标识符置孔，发现至少2个区域后交同actor抽一个函数；不附spec变化轴','同候选数量、同重构调用和测试预算，不引入外部checkpoint','是'],
            ['固定每轮重构','排除多做一轮整理本身','本地标准对照','每checkpoint实现后同actor追加一次局部重构机会，没有变化轴约束','重构包含在共同总预算，不免费增加一轮','是']
        ]))

if __name__ == '__main__':
    print(residual())
