## 背景

定位关键词：tool-use、algorithm-based fault tolerance、semantic corruption、error correction。报告agent从多个只读工具取得逐项数值，格式/取值范围均合法的单项错误能传播到报告；只有违约警告未必足以定位或恢复永久错误。 当前联合处理Q001隐式工具数值异常和Q005可执行恢复，聚焦同单位、同批、完整业务分组，不处理query遗漏/first-touch/写状态。Outcome Monitors已有conservation合同但给非绑定恢复affordance（https://arxiv.org/html/2608.19303v1 §3/5）；Real-Time Detection指出plausible-value corruption缺少外部参照不能检测（https://arxiv.org/html/2608.02464v1 §9/10）。

## 核心 Claim

待验证迁移：当任务需要n项同单位数值，工具同时有原生总和及不同权重汇总接口，且整批n+2返回最多一个数值错误时，两个任务关系残差可定位并纠正包括校验返回在内的单一语义错误，在全部调用/扫描成本计入后，能比普通契约警告或相同预算随机重试更稳定地恢复永久错误；不宣称新编码理论，收益条件是聚合调用成本低于重新核验足够多个候选项。

## 方法设计的核心思想

输入公开任务要求、n个业务分组及权重w_i（不同非零小整数）、公开聚合schema。主调用得到x_i，再调用同批数据的S=sum真实x与W=sum(w_i*真实x)，两者都是原生业务求和查询，不读取隐藏值或故障标记。构造残差s0=S-sum(x_i),s1=W-sum(w_i*x_i)。若s0非零且s1/s0唯一对应某w_i，提出x_i+=s0；若仅s0非零而s1=0，提出S-=s0；若仅s1非零，提出W-=s1。更一般用二维H矩阵各列不共线的稀疏解求唯一单坐标纠正。只有单故障和批数据不漂移假设下该动作成立；残差一致不是多故障或同源系统错误的证明。不能将纠正值当环境权威新事实普遍回写，只在该有限只读报告中使用并注明模型条件。若单位、分组覆盖、时间批次或调用成本不符合则不启用本机制，而非继续堆监控模块。不是哈希/指纹；两个冗余汇总替代逐项重复核验，残差改变具体修复动作，符合项目成本例外。 经典ABFT为成熟灵感，本方向不申报新编码理论；已读JPL 2000原文（https://uq.jpl.nasa.gov/home/turmon/Papers/abft-aero-final.pdf），1984原创PDF入口未成功读取，书目核实为Huang/Abraham（https://doi.org/10.1109/TC.1984.1676475）。Deephaven官方AggWSum及源码已核实原生weighted sum（https://deephaven.io/core/groovy/41.10/docs/reference/table-operations/group-and-aggregate/AggWSum/）；但该事实不证明同批快照或费用闭合。ERP.net官方分币种/单位加总和group分页限制说明不能随便把不同返回凑关系（https://docs.erp.net/dev/domain-api/querying-data/grouping.html）。

## 最小实验

CPU有限数据报告环境：n个公开分组，各tool返回一个整数计数；另有两原生聚合API返回S和W，公开同批版本数据不变。agent最终需逐分组值及从值做的排序/汇总。隐藏单故障在n+2观测之一生成合法整数偏移，包括primary或聚合错误；暂时/永久和无故障；加两故障与共同源同偏移作边界，不给在线标签。基线同冻结actor普通/failure-aware ReAct；range+sum一致性Outcome-Monitor式警告和公开工具列表；同+2调用预算的随机/预先固定候选重试；全部n项重复调用（预算足够时）；三副本中位数；经典ABFT二维解码直接执行，无LLM。标准方案完整定义可实现，跨域矩阵ABFT只做机制边界，不冒称可直接复现原系统。固定actor/解码/数据/核心总token和调用预算；建权重/提示、所有汇总扫描CPU/返回bytes/API费用计成本，不能把两次扫描称免费。报全部任务逐项精确恢复、单故障定位、下游决策正确、干净损失以及双/共模错误误纠正。若直接ABFT baseline与LLM方法同效更便宜，或成本不低于逐项核验则独立方法收益被推翻；不假称已有结果。n、调用/扫描成本分布、API模型、预算及重复数待确认。 ToolMaze actor源码已核实可移植Function Calling循环（https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py），新数值报告任务不是原ToolMaze实验。Outcome-Monitor式arm完整标准定义：range及公开sum关系违规时附违反关系和read/sum/weighted_sum工具名，不解码修复。共模源错误见VP-Control边界（https://arxiv.org/html/2609.10969v1）；不把重复工具名等同独立正确参照。本轮没有运行任何实验或付费推理。

本机制确属数值校验和／加权校验，按项目例外仅在替代实质更贵的逐项独立复读时研究。明确成本模型：公开静态表N行、n个无索引分组，复核每一分组需扫描N行；逐项复核为n次调用、nN行比较与n个返回值。两个原生汇总分别扫描N行；若权重列尚未存在，其构造再扫描N行，合计最多3N行、2次调用、2个返回值。所有方法共用同一冻结批次，加载／冻结N行及通信成本都计入，不把snapshot当免费；若获得这一批次还需新增全表下载则该额外下载也进入校验成本。只有完整新增成本C_check（权重构造、两次聚合、snapshot、字节传输、API收费、LLM提示）严格低于所替代逐项复核C_repeat，并且唯一单坐标解确实改变下一步纠正／弃用／复读动作时例外成立。n>3仅说明上述无索引CPU扫描模型中的条件，不能宣称真实API费用已证明更低。若生产接口不能提供同批或C_check>=C_repeat，则方法在该接口阻断，不添加校验。Deephaven文档只证明weighted sum原语存在；真实完整费用与snapshot仍未核实，保持方法阻断与低分探索资格。最小CPU条件可以按上述明示访问成本定义以验证关系，本轮未执行或测得成本。
