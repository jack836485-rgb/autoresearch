## 背景

定位关键词：tool-use、silent failure、metamorphic testing、query synthesis。静默丢弃条件后的全分页本地过滤可正确却过贵；仅比较原请求和删条件请求又可能缺少实际区分数据。 当前目标仍是Q001语义异常识别和Q005可执行恢复，聚焦可判定读查询；不处理写回或first-touch副作用。SilentProbe §3.3的parameter-inert排除与§3.4离线brute-force词表暴露见证和在线知识的边界（https://arxiv.org/html/2609.00035v1）；Shopify官方说明无效field会忽略查询而返回全部（https://shopify.dev/docs/api/usage/search-syntax）。

## 核心 Claim

待验证：当公开查询接口支持精确按id检索并与目标条件合取，且已见记录中存在条件的一正一反见证时，利用同一见证对验证公开备选编码，能将语义异常转为保留用户条件的可执行请求，在同预算下减少盲重试和不完整的本地补滤；成功只对验证覆盖的条件范围报告，不将有限见证当全局语义证明。

## 方法设计的核心思想

从不含待修复条件的公开返回中选择p满足用户谓词、n不满足谓词，id均为实际已见记录。先按id复读确认当前值。对每个公开文档或schema给出的备选请求编码e分别调用search(id=p AND e)、search(id=n AND e)。正例不返且负例不返标为见证未通过，二者均返说明该条件未排除已知反例，正返负不返才保留e。不得用隐藏accepted vocabulary扩候选。选通过编码执行原任务；新结果若出现反例立即撤回e并继续剩余公开编码。未通过、见证缺失或预算耗尽不称无匹配或不可恢复，只报告该语义尚未验证。编码用于修复而非检测报告；id缩小到单例消除排序/分页造成集合差分不等的歧义。有限见证无法排除别的同样相容错误编码，是明确边界。 SilentProbe已做C/A/B三调用差分，2018 REST API变形测试已做Subset/Disjoint/Complete关系（https://doi.org/10.1109/TSE.2017.2764464），PROSE已做example/witness合成（https://www.microsoft.com/en-us/research/project/prose-framework/usage/）。当前尝试把任务内已有正反见证用于在线请求编码恢复，而不是将正确词表预先oracle化；不宣称单例测试关系新颖，CEGIS/黑盒测试机制边界仍需判断。

## 最小实验

有限记录CPU工具：search(query,id,page)公开精确id合取语义，schema条件类型可判定，文档公开若干同语义格式例子，不公开当前parser采用哪一种。离线设置正常、未识别字符串静默忽略、静默空、语义coercion；在线只看同文档和结果。任务精确返回用户范围条件下全部id。比较同冻结actor普通/failure-aware ReAct、Outcome-Monitor式违约警告/工具列表、原请求重试、删除条件后全分页本地滤、非见证随机顺序尝试所有公开编码、完整公开编码穷举。保持actor/解码/任务/总token与工具预算；正反复读、探测、候选生成和后验检查全计成本。测全部任务精确集合成功、假阴性/假完成、从同失败起点恢复、干净损失；按见证可得性及是否在已有见证上可区分分层。若正确编码未在公开列表、两种不同全局语义同过见证而被称完成、或全枚举同预算更好均否定对应Claim。模型/预算/数据规模待确认，不运行。 同任务baseline采用完整标准定义而非把跨域PROSE/Trino直接当agent基线；公开ToolMaze actor循环实现已核实（https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py），可在该读查询任务移植。警告arm只按Outcome Monitors接口定义移植：违反用户谓词时附违反项和公开工具名、不自动修复，不冒称作者全部系统复现。Garlic/Trino已有残余过滤，均为机制边界，不忽略其无同任务artifact事实。
