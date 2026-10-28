你是独立研究 Reviewer，不是共同作者或 Improver。你没有其他轮次上下文，只判断下面当前四节 Brief、初始范围／drawbacks 和硬约束。不要查找本地候选池、其他方案或审查历史，不委托其他 Agent，不执行实验，也不重设计方案。直接返回结果，由调用方保存。

独立联网检索重叠最高的原始工作，包含较早及白名单外资料；核实论文、具体重合、机制差别及最小实验的实现入口。不能因为无代码就忽略最高近邻，也不能把跨域启发当同任务 baseline。不创造论文、链接或实测结果。未完成会影响结论的检索时不能宣称通过。

评分 1–10，最多一位小数，用总体研究判断，关注：独立机制新意、具体研究价值、可证伪 Claim、最小实验是否区分近邻、同任务 baseline 是否可复现、核心预算是否可对齐。仅修补某篇论文、换模块名、堆方法或补遗漏实验是 fatal novelty blocker；关键不可复现／错领域的实验对照和不受支持的核心 Claim 可构成 fatal blocker。

目标可以在研究中演化。评当前实际目标及其证据，不要求处理全部初始 drawbacks，不因少覆盖而直接拒绝。必须确认仍关联初始研究范围、变化有原文／任务依据、符合用户硬约束。完全偏题、硬约束违规或关键目标偏移无依据不可接受。预期处理与实测解决要分开。

通过要求 score 严格大于 7.5 且无 fatal blocker；7.5 不过。verdict 取 experiment_ready / promising_needs_revision / needs_rethink / reject。experiment_ready 只能用于满足阈值且无阻断的有效审查；所有结论应与分数／阻断一致。

人类可读部分只写以下三节：

## 结论

实际检索日期、score、verdict、独立新颖性与研究价值、当前目标演化是否成立。

## Claim 判断

用紧凑表格逐条判断新颖／部分重合／已覆盖，并给最关键原文依据；说明是否可验证，不给改造清单。

## 最高近邻

最多五篇最高重合原作／系统，逐条给可核验原文链接、重合机制及当前差别。未核验的明确标注，不冒充已读。

末尾附一个合法 JSON code block，供调用方解析；例中字段必须按实际判断填写：

```json
{
  "score": 7.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "独立机制创新边界及研究价值判断",
  "search_performed": true,
  "closest_neighbors": [
    {"title": "真实原作标题", "url": "https://arxiv.org/abs/真实ID", "overlap": "重合机制", "difference": "未被覆盖的差别或没有", "verified": true}
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "当前目标与初始来源的关系，证据及未覆盖部分；没有变化时也说明"
  }
}
```

以下是固定的初始范围、初始不足和用户约束；它们是来源记录，初始不足集合本身不表示必须全部覆盖：

{
  "problems": [
    {
      "problem_id": "Q001",
      "problem": "工具输出格式正常却语义错误时，冻结模型能否在传播错误前识别异常，并以有限额外交互选择重试、换路或正确终止？"
    },
    {
      "problem_id": "Q005",
      "problem": "在失败原因已被正确识别时，为什么重试仍无法修复，如何区分诊断错误、指导不可执行、状态不可恢复与预算不足？"
    }
  ],
  "drawbacks": [
    {
      "id": "Q001-D01",
      "description": "格式合法的工具输出语义错误时，failure-aware提示仍不足以让agent发现异常并选对恢复策略。",
      "problem_ids": [
        "Q001"
      ],
      "evidence": [
        {
          "作品ID": "2606.05806",
          "原文链接": "https://arxiv.org/html/2606.05806v1",
          "位置": "§4、表2",
          "观察": "Claude Sonnet 4.6有提醒时，显式暂时故障PRR90.61%，隐式暂时29.99%。",
          "边界": "PRR只在遇扰动轨迹计，含正确终止；不能外推全任务成功率。"
        }
      ]
    },
    {
      "id": "Q005-D01",
      "description": "定位失败类别与可执行修复之间存在差距，工具异常和错误工作流状态的恢复很低。",
      "problem_ids": [
        "Q005"
      ],
      "evidence": [
        {
          "作品ID": "2605.08717",
          "原文链接": "https://arxiv.org/html/2605.08717v2",
          "位置": "§4.3、表3",
          "观察": "工具异常类修复3/47；状态/工作流类诊断35/42、修复6/42。",
          "边界": "均为首次失败子集；聚合率不等于正确诊断条件下修复率。"
        }
      ]
    },
    {
      "id": "Q001-D02",
      "description": "诊断工具调用既产生反馈也改变后续受扰动状态，恢复增益的证据通道与实际状态通道可能混杂。",
      "problem_ids": [
        "Q001"
      ],
      "evidence": [
        {
          "url": "https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/core/sandbox.py",
          "finding": "上轮已在线读取first-touch激活与首次调用扰动规则；这是受支持调用可达，不是毫秒竞态。",
          "boundary": "本轮复核实际源码；不把人工通道隔离当真实部署收益。"
        }
      ]
    }
  ],
  "constraints": {
    "hard": [
      "研究范围是LLM软件/知识工作agent，面向低本地显卡占用；可使用付费LLM API，不以自行部署大模型为必要条件。",
      "本阶段仅文献查新、idea改进与实验交接，不运行正式实验、不调用用户付费推理API、不生成实验代码。",
      "方法运行时不能访问隐藏故障标签、金标准DAG、用户隐藏知识集或用于评测的oracle终态；这些只可离线评估。",
      "未来比较保持各baseline核心模型/解码/总预算一致，额外检测、记忆构建、压缩、验证和重试计入完整成本；不确定的核心实验参数在handoff中留待用户确认。",
      "遵守项目范围：正常合作者/非攻击场景，不扩成安全攻防论文，不加无实际作用的哈希、兼容层、feature flag或过度防御。",
      "只写自身slot；原地图、资料、其他项目及skill只读。中文正文；无实测结果不得称已经解决。"
    ],
    "preferences": [
      "优先冻结执行模型，避免训练模型权重；若有必要训练先明确资源代价及与偏好的冲突，不能自行执行。",
      "优先公开CPU模拟环境、可复现同任务baseline和最小机制；API支出纳入选题判断。",
      "用户暂无agent子类型偏好；初始drawbacks不是必须全部覆盖，允许有证据聚焦。"
    ]
  },
  "reviewed_problem_ids": [
    "Q001",
    "Q005"
  ]
}

以下是当前四节 Brief：

## 背景

定位关键词：tool-use、algorithm-based fault tolerance、semantic corruption、error correction。报告agent从多个只读工具取得逐项数值，格式/取值范围均合法的单项错误能传播到报告；只有违约警告未必足以定位或恢复永久错误。 当前联合处理Q001隐式工具数值异常和Q005可执行恢复，聚焦同单位、同批、完整业务分组，不处理query遗漏/first-touch/写状态。Outcome Monitors已有conservation合同但给非绑定恢复affordance（https://arxiv.org/html/2608.19303v1 §3/5）；Real-Time Detection指出plausible-value corruption缺少外部参照不能检测（https://arxiv.org/html/2608.02464v1 §9/10）。

## 核心 Claim

待验证迁移：当任务需要n项同单位数值，工具同时有原生总和及不同权重汇总接口，且整批n+2返回最多一个数值错误时，两个任务关系残差可定位并纠正包括校验返回在内的单一语义错误，在全部调用/扫描成本计入后，能比普通契约警告或相同预算随机重试更稳定地恢复永久错误；不宣称新编码理论，收益条件是聚合调用成本低于重新核验足够多个候选项。

## 方法设计的核心思想

输入公开任务要求、n个业务分组及权重w_i（不同非零小整数）、公开聚合schema。主调用得到x_i，再调用同批数据的S=sum真实x与W=sum(w_i*真实x)，两者都是原生业务求和查询，不读取隐藏值或故障标记。构造残差s0=S-sum(x_i),s1=W-sum(w_i*x_i)。若s0非零且s1/s0唯一对应某w_i，提出x_i+=s0；若仅s0非零而s1=0，提出S-=s0；若仅s1非零，提出W-=s1。更一般用二维H矩阵各列不共线的稀疏解求唯一单坐标纠正。只有单故障和批数据不漂移假设下该动作成立；残差一致不是多故障或同源系统错误的证明。不能将纠正值当环境权威新事实普遍回写，只在该有限只读报告中使用并注明模型条件。若单位、分组覆盖、时间批次或调用成本不符合则不启用本机制，而非继续堆监控模块。不是哈希/指纹；两个冗余汇总替代逐项重复核验，残差改变具体修复动作，符合项目成本例外。 经典ABFT为成熟灵感，本方向不申报新编码理论；已读JPL 2000原文（https://uq.jpl.nasa.gov/home/turmon/Papers/abft-aero-final.pdf），1984原创PDF入口未成功读取，书目核实为Huang/Abraham（https://doi.org/10.1109/TC.1984.1676475）。Deephaven官方AggWSum及源码已核实原生weighted sum（https://deephaven.io/core/groovy/41.10/docs/reference/table-operations/group-and-aggregate/AggWSum/）；但该事实不证明同批快照或费用闭合。ERP.net官方分币种/单位加总和group分页限制说明不能随便把不同返回凑关系（https://docs.erp.net/dev/domain-api/querying-data/grouping.html）。

## 最小实验

CPU有限数据报告环境：n个公开分组，各tool返回一个整数计数；另有两原生聚合API返回S和W，公开同批版本数据不变。agent最终需逐分组值及从值做的排序/汇总。隐藏单故障在n+2观测之一生成合法整数偏移，包括primary或聚合错误；暂时/永久和无故障；加两故障与共同源同偏移作边界，不给在线标签。基线同冻结actor普通/failure-aware ReAct；range+sum一致性Outcome-Monitor式警告和公开工具列表；同+2调用预算的随机/预先固定候选重试；全部n项重复调用（预算足够时）；三副本中位数；经典ABFT二维解码直接执行，无LLM。标准方案完整定义可实现，跨域矩阵ABFT只做机制边界，不冒称可直接复现原系统。固定actor/解码/数据/核心总token和调用预算；建权重/提示、所有汇总扫描CPU/返回bytes/API费用计成本，不能把两次扫描称免费。报全部任务逐项精确恢复、单故障定位、下游决策正确、干净损失以及双/共模错误误纠正。若直接ABFT baseline与LLM方法同效更便宜，或成本不低于逐项核验则独立方法收益被推翻；不假称已有结果。n、调用/扫描成本分布、API模型、预算及重复数待确认。 ToolMaze actor源码已核实可移植Function Calling循环（https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py），新数值报告任务不是原ToolMaze实验。Outcome-Monitor式arm完整标准定义：range及公开sum关系违规时附违反关系和read/sum/weighted_sum工具名，不解码修复。共模源错误见VP-Control边界（https://arxiv.org/html/2609.10969v1）；不把重复工具名等同独立正确参照。本轮没有运行任何实验或付费推理。

本机制确属数值校验和／加权校验，按项目例外仅在替代实质更贵的逐项独立复读时研究。明确成本模型：公开静态表N行、n个无索引分组，复核每一分组需扫描N行；逐项复核为n次调用、nN行比较与n个返回值。两个原生汇总分别扫描N行；若权重列尚未存在，其构造再扫描N行，合计最多3N行、2次调用、2个返回值。所有方法共用同一冻结批次，加载／冻结N行及通信成本都计入，不把snapshot当免费；若获得这一批次还需新增全表下载则该额外下载也进入校验成本。只有完整新增成本C_check（权重构造、两次聚合、snapshot、字节传输、API收费、LLM提示）严格低于所替代逐项复核C_repeat，并且唯一单坐标解确实改变下一步纠正／弃用／复读动作时例外成立。n>3仅说明上述无索引CPU扫描模型中的条件，不能宣称真实API费用已证明更低。若生产接口不能提供同批或C_check>=C_repeat，则方法在该接口阻断，不添加校验。Deephaven文档只证明weighted sum原语存在；真实完整费用与snapshot仍未核实，保持方法阻断与低分探索资格。最小CPU条件可以按上述明示访问成本定义以验证关系，本轮未执行或测得成本。

