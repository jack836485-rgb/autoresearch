## 背景

**定位关键词：** API documentation；interactive coding agents；execution feedback

**一句话定位：** 交互式代码agent即使有正确工具文档，仍可能访问不存在字段或误用当前返回；怎样以局部执行证据修复。

## 核心 Claim

AppWorld当前schema可靠，原论文报告agent会臆造输出字段、误用接口及错误后难适应；这些是问题入口。尚未诊断的更窄假设是错误恢复会重新猜整个返回结构或将当前empty/None不当地解释成全局schema变化。主张局部访问需求诊断可帮助原actor修复当前矛盾，同时保留已成功路径；不声称这种误泛化常见或已测出效应。贡献是CPU从实际JSON访问表达式与公开返回生成局部矛盾，而不是优化完整文档。

主执行器直接打开AppWorld原文Appendix A，原文确有“ablating response schemas from the documentation”及下一段future works；这只证明提出未来方向，不证明原论文已跑该协议。当前主实验保留原始完整文档。自然输出字段臆造是原文错误分析，empty/None误泛化及路径损坏比例尚未知，必须先诊断。

## 方法设计的核心思想

首版支持JSON返回、dict/list索引、简单属性路径和int/float转换。CPU在API返回后为actor自己的访问表达式记录路径和所需container/key/length/value type，并在当前公开对象验证；从根到叶给首个实际矛盾及该前缀的可见结构，保留其他已经成功的路径。empty list只否定当前索引可达，不证明element schema缺失；None只否定无guard直接转换，不自动改全局字段类型；报错调用返回与成功返回分开。原actor修访问/补查询，不自动把相似名字字段替代，不把反例当数据语义真值。新增CPU机制不给模型更多业务答案、隐藏schema或数据库。

## 最小实验

主实验改为原始AppWorld完整文档与真实自然执行错误，不改变工具/数据/schema，先独立分类失效并验证该窄假设是否有足够样本。相同自然失败前缀配对恢复与原生end-to-end分开；对照官方ReAct/FullCode、同原始返回+局部error prompt、同token全量shape摘要、ACE no-GT原生及本方法。原始task TGC、重复访问错误、恢复是否损坏已有成功路径、完整成本为指标。仅在主诊断通过后另做response_schemas去除消融：原文Appendix A确实明确提出该未来方向，但未提供原论文实跑分数；官方load(include_response_schemas=False)/remove_fields及show_api_response_schemas=False控制所有静/动态文档入口，消融分数单独命名。不将空值误泛化当事实，不靠修改benchmark制造主结果。若普通error反馈/ACE已等效、自然结构误用低频、CPU只是提供更多原始数据、或为保证成功过度拒绝则停止。全部构建、reflector、instrumentation/失败/API/token按共同上限计费。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方ReAct/FullCode | 同AppWorld schema-blind任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；真实agent、ApiDocCollection.load/remove_fields及environment已读 | appworld run auto --agent-name simplified_full_code_agent（或simplified_react_code_agent） --model-name {共同actor} --dataset-name dev；主实验原始完整文档/真实环境，blind消融另报 | 是；未实跑 |
| 局部error prompt | 排除只提醒别整体重猜已足够 | 完整本地标准规范 | 实际raw返回、stack trace与成功访问记录同主方法，提示只修失败路径；不计算结构需求最小矛盾 | 同actor/信息/预算，不再用强模型 | 是 |
| 全量shape摘要 | 排除纯返回压缩/概览效益 | 完整本地标准规范 | 每次返回CPU枚举字段路径、当前类型/空值，按相同feedback token cap供actor；不绑定具体访问表达式需求 | 同原始返回记录、上下文额度和API预算 | 是 |
| ACE no-GT on AppWorld | 同任务执行反馈增量context强近邻 | https://arxiv.org/abs/2510.04618 | https://github.com/ace-agent/ace-appworld；adaptation_react.py、adaptation_agent、generator/reflector no-GT提示和config真实内容已读 | 从已核验ACE AppWorld fork源码安装；appworld run ACE_offline_no_GT_adaptation再ACE_offline_no_GT_evaluation，或ACE_online_no_GT；主比较均保留完整API文档，统一actor/reflector/train流/全部构建与query预算，不给GT或免费playbook | 是；未实跑 |
