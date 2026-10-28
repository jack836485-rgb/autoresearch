## 背景

定位关键词：tool-use、query completeness、silent failure、metamorphic testing。正确过滤后top-k截断和错误过滤后无溢出可以产生相同合法返回；提高cap未必暴露语义遗漏，而修正过滤未必暴露截断遗漏。 当前仍联合处理Q001异常识别与Q005可执行恢复，聚焦读集合；first-touch及写状态未覆盖。ToolUniverse audit已覆盖截断/过滤遗漏不披露（https://arxiv.org/html/2609.26836v1 §1/2/4）；Partial Evidence Bench已分开局部正确与false-complete（https://arxiv.org/html/2605.05379v1 §3/5）。本方向聚焦证据对应互补恢复动作的交互，而非重复这些指标。

## 核心 Claim

待验证：在公开集合查询工具中，正确语义的截断与错误语义的未溢出可产生完全相同初始行及metadata。单独提高返回cap或单独替换查询codec都可能不增加正确目标记录；二者联合才可能形成恢复路径。因此恢复证据不是诊断准确率或覆盖提示的可加效应。对冻结agent固定公开前缀，区分公开parse evidence、overflow evidence与可执行codec/cap选择，可检验何种证据使agent实现这一联合恢复；不声称所有错误模式或所有API均有此交互。

## 方法设计的核心思想

任务公开集合谓词g，search支持公开candidate codec集合和不同cap预算档，metadata可选explain(query)解析已用谓词、count/overflow表示本次实际解析后的匹配数。在线可读这些真实工具返回而不知reference parser或evaluator。构造正交2×2环境：语义正确/语义收缩，cap高/低，原请求初始行保持相同或对匹配公共前缀分层；不再把known-id get列为有用恢复。agent可请求更高cap、改codec、两者联合或报告已知partial。语义收缩目标例：g为x>=20；错误codec改成x>=30；固定升序数据20,25,40时初始cap=1无法同时让两种语义首行同相，故不用该例。改用公开固定降序、记录40,35,25,20：cap=2两种初始返回均40,35；提高cap会只在正确codec返回25,20；换正确codec但仍cap2仍40,35；同时改codec与cap才恢复完整集。公开explain和count只声明当前实际操作，不声明隐藏correctness。explain须跟用户显式g比较才成为语义异常证据，count只给当前操作overflow而不等于原目标完整性。分别测无metadata、parse、overflow、两者，所有metadata取得调用计成本；记录在线实际选codec/cap路径。任务创新聚焦证据到两个互补动作的联合恢复，不把两个提示模块堆叠当方法。 Shopify公开query debug有parsed和warnings（https://shopify.dev/docs/api/usage/search-syntax）；工具返回实际parsed条件而非正确query oracle。GetNext（https://arxiv.org/html/1208.3876v1）假设匹配语义正确且overflow可信，REST MT（https://javiertroyauma.github.io/publications/TSE2017_REST_prePrint.pdf）为缓解近似检索主动限规模。当前研究两种正确取证仍未必触发joint行动，不申报新query理论。

## 最小实验

CPU静态有限表id/整数x，降序排序公开；codec各为文档公开形式，actual解析映射对在线隐藏，explain返回该查询真实解析AST；每次search cap费用单调随返回量上升，count计扫描成本。完整g目标从公开用户谓词定义。固定数据/初始行的全因子条件：语义收缩或正确，cap2或足够大；为了固定prefix主分析选择相同行的paired任务，非paired任务另报不混样本。从固定prefix比较同冻结actor ReAct/failure-aware、Outcome-Monitor式行谓词警告、parse-only/overflow-only提示、标准finite动作穷举、公开id域枚举及完整分区关系查询。finite动作穷举先按文档顺序codec/cap组合执行，把所有返回中符合g的行并集；停止仅在所有组合执行完或预算耗尽，不用hidden truth选择。完整分区baseline按公开有限x域划分不重叠区间，逐区间全部获取，遇overflow再二分直到预算耗尽；同假定不可靠codec不能获得免费完备性保证。候选world离线只允许公开有限记录/parse映射族，policy是同公开history到下一公开动作的统一函数；预算可达基准不按hidden世界各选不同动作。测全部任务精确集合成功、条件恢复、false-complete、干净损失与codec×cap×metadata交互。若joint收益完全来自更多bytes/API成本、同预算标准分区同好或已有原作该协议，独立Claim被推翻。工具sim与标准baseline定义完整；ToolMaze actor可移植，非原ToolMaze任务。模型/费用/样本/总budget待确认，未运行。 ToolMaze Function Calling实际源码已核实（https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py）；Outcome-Monitor式行检查arm完整定义为违反g才附违反项及公开工具名、不强制恢复（https://arxiv.org/html/2608.19303v1 §3）。所有检测/metadata解释/扩cap/尝试codec/验证计总成本；原作无同任务artifact不忽略创新边界。
