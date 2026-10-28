## 背景
工具返回普通整数不一定支持精确结论；同一不完整观测却可能足以支持某个阈值动作。当前目标从一般隐式错误与诊断恢复聚焦到“结果限定语义×用户结论需求”，不要求恢复所有后台信息。Elastic官方文档的Track total hits规定gte表示下界、eq表示精确；同页Search timeout给出timed_out=true仍relation=eq的部分结果例子，所以单独升级track_total_hits=true未必恢复完整性（https://www.elastic.co/docs/solutions/search/the-search-api）。ToolUniverse审计§4–5已核实限定信息丢失和更强结论传播（https://arxiv.org/html/2609.26836v1）。这支持真实任务轴，但不证明冻结agent必有净收益，也不把公开协议本身当创新。方法路线尝试的是成熟区间需求精化：ThalamusDB aggregate bounds和Demanded Abstract Interpretation已经覆盖主要运算（https://saehanjo.github.io/assets/files/thalamusdb.pdf；https://arxiv.org/html/2104.01270v1），当前研究贡献仅可能是尚未被agent恢复任务测量的结论条件性任务与评估，不申报新区间算法。

## 核心 Claim
待检验的任务Claim：在工具数值、格式和后台限定相同而用户只要求存在/阈值决定或要求精确总数时，把恢复定义成“得到支撑当前结论的语义”会改变可执行恢复集合；只评价是否恢复原工具的精确完整响应会将足够证据误计为未恢复，单relation修复则会将不完整eq误计为恢复。提出成对任务以分离识别结果含义、选到任务所需恢复、修复权限/预算不足，检验这一新增轴是否提供已有集合完整性任务没有的可区分失败结构。Q001是正常数值被当成更强结论，Q005是正确知道count非精确却选无必要或仍无效精确重试。不覆盖未披露的任意数字污染、first-touch或一般工作流回滚。

## 方法设计的核心思想
公开任务要求包含结论类型及阈值；actor自行形成proposed action/answer。公开返回value、relation、timed_out、shard completion等真实元数据；另设wrapper仅投影整数的条件，并给公开、收费的raw_response读取能力或明确无该能力。运行时只能读当次公开信息，缺失metadata不能猜默认eq。采用标准语义基线把健全的部分非负计数解释为下界，完整eq解释为单点；区间对所有可能值给同一用户决定时可完成，否则选择公开精化动作。track_total_hits升级只修准确性，恢复未完成分片/重发完整请求修覆盖；公开工具不可完成时只能报告不能支持当前精确结论，不能读离线真值。raw、精确请求、分片重试、推理和等待都收费。这个基线是任务能力参照，不把它重命名为独立方法。

## 最小实验
完整可实现CPU标准任务：静态非负记录分三公开分片，Search(predicate,track_limit,allow_partial)返回计数与四种公开限定组合；count截断用gte，完整精确用eq，超时/分片缺失可保留eq但表示仅已处理部分。请求成功结果中没有错误记录或重复计数，保证部分计数为下界；此边界公开，若任意数值错则下界也无效不计为本任务。用户任务成对为N>=T布尔动作与精确N报告。例如value=100, gte, complete可支持T=50、不能支持T=150或精确；value=100, eq, timed_out可支持T=50而不能支持N=100。另有低于阈值的完整eq、缺字段wrapper和不能恢复的分片能力，防止永远yes/永远abstain。工具可读raw限定、升级track_limit、对公开失败分片重试、完整重新请求，权限/费用均公开，隐藏N和故障类别只给离线评估。穷举小任务的共同公开历史策略集合，标出对当前结论支持可达而完整后台响应不可达的实例；不能让oracle按隐藏世界临时选动作。
对比同冻结actor普通/failure-aware FunctionCalling、限定语义原样提示、异常类别coaching、所有非精确/部分响应均请求完全精确的标准策略、只升级track_total_hits策略、上述任务需求区间标准策略。普通actor实现入口为https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py，迁移到明确定义的新任务；不声称复现ToolUniverse或ThalamusDB整套系统。强区间策略可无模型实现但与带相同actor版本分列，全部控制开销计总预算。主指标是支撑当前任务且结论正确的完成率、误完全性、无必要精化、有效/无效修复动作、干净任务损失和完整成本；离线另报backend完整恢复率，检验其与任务恢复是否出现定义性差异之外的agent错误差异。若变化只是替换答案类型、已有agent任务已测同样限定交互，或区间基线完全解释而新任务未带来新失败结构，则贡献失败。模型/阈值分布/成本/样本/预算待确认；当前无实验、实验代码或付费调用。
