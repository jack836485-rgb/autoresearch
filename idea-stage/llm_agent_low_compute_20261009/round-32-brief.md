## 背景

**定位关键词：** API documentation；interactive coding agents；execution feedback

**一句话定位：** 代码agent不知道工具返回schema时，怎样从实际返回和自己代码中找出真正被否定的结构假设。

## 核心 Claim

AppWorld现有文档由FastAPI自动生成且可靠，不能声称自然schema过时；其Appendix A提出去掉response schema后通过交互理解返回。主张这一明确schema-blind设置下，单个KeyError/TypeError常被当成整个接口理解错误，或把当前空列表/nullable值当全局类型改变。研究增量是将实际访问表达式转成局部结构需求，在同次公开返回上找最小矛盾并保留已有成功访问的证据，而非重写工具文档或推断完整全局schema。

原benchmark可靠schema是事实，删去schema是原文明确的更难setting；一次失败不能否定所有成功路径或将数据空值解释为schema变化；在实际访问需求处定位矛盾，保留其它证据；在同信息/预算下更少反例误泛化且任务更好才支持。

## 方法设计的核心思想

首版支持JSON返回、dict/list索引、简单属性路径和int/float转换。CPU在API返回后为actor自己的访问表达式记录路径和所需container/key/length/value type，并在当前公开对象验证；从根到叶给首个实际矛盾及该前缀的可见结构，保留其他已经成功的路径。empty list只否定当前索引可达，不证明element schema缺失；None只否定无guard直接转换，不自动改全局字段类型；报错调用返回与成功返回分开。原actor修访问/补查询，不自动把相似名字字段替代，不把反例当数据语义真值。新增CPU机制不给模型更多业务答案、隐藏schema或数据库。

## 最小实验

冻结schema-blind版本：全部任务允许API的公开response_schemas统一移除，参数/功能文档和真实执行不改，非按主方法错误挑endpoint。实际ApiDocCollection.load(include_response_schemas=False)与remove_fields([response_schemas])接口已直接读；静态world.task.api_docs渲染走同一无schema副本，动态API文档显示通过AppWorld show_api_response_schemas=False处理；若还有response schema渠道可见，该任务不纳入blind分数。完整schema原协议单独报告，不混分。对照FullCode/ReAct、同公开返回+局部error prompt、每次全量返回shape摘要、ACE no-GT原生增量playbook、访问需求矛盾。各组同actor/reflector能力、任务/顺序/seed/文档/失败/总token及API调用预算；ACE构建反思不免费。先诊断本次结构失败与反例误泛化，再评价TGC/重复结构错误/成本；若ACE或直接error同效、只靠多给结构信息获益或自然blind任务无所述失误则停止。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方ReAct/FullCode | 同AppWorld schema-blind任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；真实agent、ApiDocCollection.load/remove_fields及environment已读 | appworld run auto --agent-name simplified_full_code_agent（或simplified_react_code_agent） --model-name {共同actor} --dataset-name dev；实验副本统一无response_schema文档；原完整schema另报 | 是；未实跑 |
| 局部error prompt | 排除只提醒别整体重猜已足够 | 完整本地标准规范 | 实际raw返回、stack trace与成功访问记录同主方法，提示只修失败路径；不计算结构需求最小矛盾 | 同actor/信息/预算，不再用强模型 | 是 |
| 全量shape摘要 | 排除纯返回压缩/概览效益 | 完整本地标准规范 | 每次返回CPU枚举字段路径、当前类型/空值，按相同feedback token cap供actor；不绑定具体访问表达式需求 | 同原始返回记录、上下文额度和API预算 | 是 |
| ACE no-GT on AppWorld | 同任务执行反馈增量context强近邻 | https://arxiv.org/abs/2510.04618 | https://github.com/ace-agent/ace-appworld；adaptation_react.py、adaptation_agent、generator/reflector no-GT提示和config真实内容已读 | 从官方fork源码安装；appworld run ACE_offline_no_GT_adaptation再ACE_offline_no_GT_evaluation，或ACE_online_no_GT；统一同schema-blind副本、actor/reflector快照、train流和总成本，不给GT与免费playbook | 是；未实跑 |
