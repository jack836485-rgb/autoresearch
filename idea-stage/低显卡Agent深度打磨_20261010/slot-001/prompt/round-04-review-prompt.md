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

定位关键词：tool-use、query completeness、silent failure、metamorphic testing。正确过滤后top-k截断和错误过滤后无溢出可以产生相同合法返回；提高cap未必暴露语义遗漏，而修正过滤未必暴露截断遗漏。 当前仍联合处理Q001异常识别与Q005可执行恢复，聚焦读集合；first-touch及写状态未覆盖。ToolUniverse audit已覆盖截断/过滤遗漏不披露（https://arxiv.org/html/2609.26836v1 §1/2/4）；Partial Evidence Bench已分开局部正确与false-complete（https://arxiv.org/html/2605.05379v1 §3/5）。本方向聚焦证据对应互补恢复动作的交互，而非重复这些指标。

## 核心 Claim

待验证：在公开集合查询工具中，正确语义的截断与错误语义的未溢出可产生完全相同初始行及metadata。单独提高返回cap或单独替换查询codec都可能不增加正确目标记录；二者联合才可能形成恢复路径。因此恢复证据不是诊断准确率或覆盖提示的可加效应。对冻结agent固定公开前缀，区分公开parse evidence、overflow evidence与可执行codec/cap选择，可检验何种证据使agent实现这一联合恢复；不声称所有错误模式或所有API均有此交互。

## 方法设计的核心思想

任务公开集合谓词g，search支持公开candidate codec集合和不同cap预算档，metadata可选explain(query)解析已用谓词、count/overflow表示本次实际解析后的匹配数。在线可读这些真实工具返回而不知reference parser或evaluator。构造正交2×2环境：语义正确/语义收缩，cap高/低，原请求初始行保持相同或对匹配公共前缀分层；不再把known-id get列为有用恢复。agent可请求更高cap、改codec、两者联合或报告已知partial。语义收缩目标例：g为x>=20；错误codec改成x>=30；固定升序数据20,25,40时初始cap=1无法同时让两种语义首行同相，故不用该例。改用公开固定降序、记录40,35,25,20：cap=2两种初始返回均40,35；提高cap会只在正确codec返回25,20；换正确codec但仍cap2仍40,35；同时改codec与cap才恢复完整集。公开explain和count只声明当前实际操作，不声明隐藏correctness。explain须跟用户显式g比较才成为语义异常证据，count只给当前操作overflow而不等于原目标完整性。分别测无metadata、parse、overflow、两者，所有metadata取得调用计成本；记录在线实际选codec/cap路径。任务创新聚焦证据到两个互补动作的联合恢复，不把两个提示模块堆叠当方法。 Shopify公开query debug有parsed和warnings（https://shopify.dev/docs/api/usage/search-syntax）；工具返回实际parsed条件而非正确query oracle。GetNext（https://arxiv.org/html/1208.3876v1）假设匹配语义正确且overflow可信，REST MT（https://javiertroyauma.github.io/publications/TSE2017_REST_prePrint.pdf）为缓解近似检索主动限规模。当前研究两种正确取证仍未必触发joint行动，不申报新query理论。

## 最小实验

CPU静态有限表id/整数x，降序排序公开；codec各为文档公开形式，actual解析映射对在线隐藏，explain返回该查询真实解析AST；每次search cap费用单调随返回量上升，count计扫描成本。完整g目标从公开用户谓词定义。固定数据/初始行的全因子条件：语义收缩或正确，cap2或足够大；为了固定prefix主分析选择相同行的paired任务，非paired任务另报不混样本。从固定prefix比较同冻结actor ReAct/failure-aware、Outcome-Monitor式行谓词警告、parse-only/overflow-only提示、标准finite动作穷举、公开id域枚举及完整分区关系查询。finite动作穷举先按文档顺序codec/cap组合执行，把所有返回中符合g的行并集；停止仅在所有组合执行完或预算耗尽，不用hidden truth选择。完整分区baseline按公开有限x域划分不重叠区间，逐区间全部获取，遇overflow再二分直到预算耗尽；同假定不可靠codec不能获得免费完备性保证。候选world离线只允许公开有限记录/parse映射族，policy是同公开history到下一公开动作的统一函数；预算可达基准不按hidden世界各选不同动作。测全部任务精确集合成功、条件恢复、false-complete、干净损失与codec×cap×metadata交互。若joint收益完全来自更多bytes/API成本、同预算标准分区同好或已有原作该协议，独立Claim被推翻。工具sim与标准baseline定义完整；ToolMaze actor可移植，非原ToolMaze任务。模型/费用/样本/总budget待确认，未运行。 ToolMaze Function Calling实际源码已核实（https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py）；Outcome-Monitor式行检查arm完整定义为违反g才附违反项及公开工具名、不强制恢复（https://arxiv.org/html/2608.19303v1 §3）。所有检测/metadata解释/扩cap/尝试codec/验证计总成本；原作无同任务artifact不忽略创新边界。

