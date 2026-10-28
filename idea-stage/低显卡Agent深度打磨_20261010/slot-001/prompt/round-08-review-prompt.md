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
正确判断“当前证据不足”并不告诉agent哪条工具调用会补上所需语义，或在当前权限与预算内能否补上。当前研究聚焦工具计数限定被加强为精确结论（Q001）及正确诊断后无效精化/能力或预算不足（Q005），不覆盖任意数字污染或first-touch。Elastic官方Search API已规定gte下界，并给出timed_out=true仍eq的部分计数；准确性升级和覆盖恢复是不同效果（https://www.elastic.co/docs/solutions/search/the-search-api）。ToolUniverse审计已提出用途条件性可靠性，不能把保留qualifier称为新方法（https://arxiv.org/html/2609.26836v1）。SearchDecision-Bench/Table1已测sufficiency、支持性和next-action；SearchJev AppendixD.3把insufficient接到forced continue，但其typed schema可容纳任意操作选择，不声称架构不能做恢复（https://arxiv.org/html/2610.05107v1）。新增研究对象是有实际工具转移与成本的“诊断等价、恢复不等价”任务：固定结论要求及诊断正确性，只改变公开能力和预算来辨识可执行恢复；区间语义、AND/OR策略穷举与可达性均是标准基线，不申报算法创新。

## 核心 Claim
待检验：对于相同用户精确计数目标、相同当前数值/限定和相同正确诊断，公开修复能力与剩余预算可产生四种不同终态——无需修复、可执行支持性修复、只有更高预算可修复、在公开动作闭包中不可修复。建立诊断等价配组，要求agent同时输出可执行首动作及有据的停止/继续理由；测试“正确的充分性/故障类别反馈”是否仍系统性选择无效动作或把能力阻断误认为再重试即可。独立任务贡献的支持条件不是答案类型成功率不同：必须在固定正确诊断与任务目标的配组中，观察到agent修复选择错误随能力/预算变化，且完整公开语义规划基线能够恢复这些错误而相同诊断提示不能。若差别只来自额外反馈、遗漏工具说明或总预算不公平，Claim失败。

## 方法设计的核心思想
每个episode公开当前结果、用户结论要求、工具能力描述和成本；工具能力可以是精确计数仅支持指定分片、按分片读取、恢复连接后读取或只可读取已完成分片。这些是明确不同接口实例，不让工具表暗含隐藏能力。标准参照将公开结果解释成可能数值集合；依据公开工具转移和动作结果分支，在剩余预算内穷举有限AND/OR策略。终点须对该公开历史一致的所有世界支撑同一任务结论；不能以单世界真实N为oracle选动作。输出最小可行成本及有效首动作集合仅为离线标签，在线agent只能凭公开文档和实际调用推导。当前阶段不训练或运行规划器/actor。
主比较中的无诊断、只给当前正确诊断、正确诊断加原样公开能力、强公开语义规划基线，均保留相同文档和操作范围；能力信息本来全公开，第三臂只是把既有文档相关段落原样重排，不额外泄漏动作答案。正确诊断臂由在线公开限定的确定性规则生成，例如“当前计数是下界且不足以支持精确N”，不使用隐藏故障原因。把该规则的误分类与actor恢复错误分开报告。Task本身考操作作用与可达性，不称新预测模型或新恢复算法。

## 最小实验
完整CPU有限任务：两至三个静态非负分片，每片记录数取有限集合，所有成功返回均无重复/假记录；初始Search结果由公开relation和complete/missing_shards说明支持单点或下界。主要诊断等价组固定用户“报告精确N”、相同value=100/gte、完整目标范围与当前各分片已知界。四个公开能力实例分别允许（A）one-shot exact_all成本3；（B）exact_part仅覆盖指定一片成本1，必须read_other_parts累计成本4才能支撑N；（C）read_missing先restore_endpoint成本1，再exact_part成本2；（D）遗漏分片没有任何读取或恢复接口，且界不为零，因此无法支持精确N。没有one-shot隐藏旁路，能力表中公开写明适用范围；A/B/C接口作用不同，不把价格差本身当新意。完整eq干净组是无需修复对照。每个能力实例在不同总预算水平重复，含足够及不足条件；允许因实际返回把界收窄而较早完成。离线在当前公共历史一致的小世界上穷举策略，给每组预算可达性和有效首动作，不给actor这些标签。
测试冻结FunctionCalling actor（真实循环入口https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py）、原failure-aware、上述确定性正确诊断coaching、文档相关段落重排、只升级精度/盲重复同调用/泛化forced-continue标准策略、完整公开语义AND/OR基线。SearchJev训练/inference实际入口https://raw.githubusercontent.com/EvoScientist/SearchJev/main/training/inference.py已亲读：decide接受任意state与choice菜单，但原模型本地GPU依赖及完整dual-system实现未核实，不把它强塞为同核心模型baseline；用同冻结actor、相同typed questions/legal menus的标准判别接口作对照。标准任务不冒称复现SearchDecision-Bench或ToolUniverse整套系统。
主指标按全体配组统计：支持且正确完成率、有效首动作率、正确能力/预算阻断判断、无效重试成本与干净损失；在当前确定性诊断正确子集单列这些指标，并报告该子集筛选和全部分母，不从汇总诊断率相除。预先规定贡献判据：跨公开能力等价配组的修复动作错误在budget-sufficient层存在，并被强公开语义基线消除；若只提高budget就解释全部错误、或正确诊断已足够消除，则没有新增诊断到动作的失败结构。规划、诊断、文档检索/重排、token、调用、扫描、CPU与等待都计完整总成本；纯确定性基线和同actor载体分列。模型、世界规模、预算/费用取值、样本与统计功效待确认，未运行实验或生成实验代码。

