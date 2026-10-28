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

定位关键词：tool-use、silent failure、metamorphic testing、query synthesis。静默丢弃条件后的全分页本地过滤可正确却过贵；仅比较原请求和删条件请求又可能缺少实际区分数据。 当前目标仍是Q001语义异常识别和Q005可执行恢复，聚焦可判定读查询；不处理写回或first-touch副作用。SilentProbe §3.3的parameter-inert排除与§3.4离线brute-force词表暴露见证和在线知识的边界（https://arxiv.org/html/2609.00035v1）；Shopify官方说明无效field会忽略查询而返回全部（https://shopify.dev/docs/api/usage/search-syntax）。

## 核心 Claim

待验证：当公开查询接口支持精确按id检索并与目标条件合取，且已见记录中存在条件的一正一反见证时，利用同一见证对验证公开备选编码，能将语义异常转为保留用户条件的可执行请求，在同预算下减少盲重试和不完整的本地补滤；成功只对验证覆盖的条件范围报告，不将有限见证当全局语义证明。

## 方法设计的核心思想

从不含待修复条件的公开返回中选择p满足用户谓词、n不满足谓词，id均为实际已见记录。先按id复读确认当前值。对每个公开文档或schema给出的备选请求编码e分别调用search(id=p AND e)、search(id=n AND e)。正例不返且负例不返标为见证未通过，二者均返说明该条件未排除已知反例，正返负不返才保留e。不得用隐藏accepted vocabulary扩候选。选通过编码执行原任务；新结果若出现反例立即撤回e并继续剩余公开编码。未通过、见证缺失或预算耗尽不称无匹配或不可恢复，只报告该语义尚未验证。编码用于修复而非检测报告；id缩小到单例消除排序/分页造成集合差分不等的歧义。有限见证无法排除别的同样相容错误编码，是明确边界。 SilentProbe已做C/A/B三调用差分，2018 REST API变形测试已做Subset/Disjoint/Complete关系（https://doi.org/10.1109/TSE.2017.2764464），PROSE已做example/witness合成（https://www.microsoft.com/en-us/research/project/prose-framework/usage/）。当前尝试把任务内已有正反见证用于在线请求编码恢复，而不是将正确词表预先oracle化；不宣称单例测试关系新颖，CEGIS/黑盒测试机制边界仍需判断。

## 最小实验

有限记录CPU工具：search(query,id,page)公开精确id合取语义，schema条件类型可判定，文档公开若干同语义格式例子，不公开当前parser采用哪一种。离线设置正常、未识别字符串静默忽略、静默空、语义coercion；在线只看同文档和结果。任务精确返回用户范围条件下全部id。比较同冻结actor普通/failure-aware ReAct、Outcome-Monitor式违约警告/工具列表、原请求重试、删除条件后全分页本地滤、非见证随机顺序尝试所有公开编码、完整公开编码穷举。保持actor/解码/任务/总token与工具预算；正反复读、探测、候选生成和后验检查全计成本。测全部任务精确集合成功、假阴性/假完成、从同失败起点恢复、干净损失；按见证可得性及是否在已有见证上可区分分层。若正确编码未在公开列表、两种不同全局语义同过见证而被称完成、或全枚举同预算更好均否定对应Claim。模型/预算/数据规模待确认，不运行。 同任务baseline采用完整标准定义而非把跨域PROSE/Trino直接当agent基线；公开ToolMaze actor循环实现已核实（https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py），可在该读查询任务移植。警告arm只按Outcome Monitors接口定义移植：违反用户谓词时附违反项和公开工具名、不自动修复，不冒称作者全部系统复现。Garlic/Trino已有残余过滤，均为机制边界，不忽略其无同任务artifact事实。

