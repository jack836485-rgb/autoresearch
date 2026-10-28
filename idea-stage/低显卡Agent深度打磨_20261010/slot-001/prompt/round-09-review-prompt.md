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
当前研究聚焦一次真实软件工作流中，恢复读取能否继续作用于原任务集合。真实邮件agent源码的read_unread_emails先select(readonly=False)、查UNSEEN，再fetch RFC822；对multipart只提取text/plain，正常HTML-only multipart可能返回合法空content。RFC3501§6.4.5规定RFC822等价BODY[]且隐式置Seen，所以再调用同一UNSEEN查询会移出刚才目标（https://raw.githubusercontent.com/MubashirShafique/email-assistant-agent/main/tools.py；https://www.rfc-editor.org/rfc/rfc3501.html）。这是亲读代码/协议推出的支持路径，未实跑，不报发生率。DARC §4.2明确离线success-cost矩阵用于可重置或独立受控尝试，不能把它当真实不中断工作流的任意组合保证（https://arxiv.org/html/2608.11772v1）。Verified Tool Calls §4.4假定验证只读；CIR已测同查询隐藏内容，Limbo已测合同改变可恢复性（https://arxiv.org/html/2608.02645v1；https://arxiv.org/html/2610.00372v1；https://arxiv.org/html/2609.29095v1）。当前不把有副作用读取、PEEK、稳定ID、状态规划或换合同称为方法创新；尝试的是“单独重置时成功的读取恢复链，在真实原集合任务中不再组合成功”的闭环任务。ATBench Fig15也有恶意诊断读的隐藏写，但其§3.1任务为完整安全轨迹判断（https://arxiv.org/html/2604.02022v1）；这里仅正常合作者、正常邮件MIME及公开Seen效应，无攻击或危险写。

## 核心 Claim
待检验：固定初始未读邮件集合和内容遗漏，一个恢复操作在重置的独立尝试中成功，不足以预测它跟在另一个读取之后仍成功；前一次读取改变后一次筛选集合，可使“已正确识别HTML正文未暴露”的诊断仍接到无效的同查询恢复。提出可执行成对任务，区分恢复内容能力不足、输入集合被前次读取改变、预算不足，并检验独立尝试success-cost矩阵是否高估实际有序恢复链。Q001对应合法空正文/后续空集合被错误当作原任务无内容，Q001-D02对应读取同时给反馈和改后继状态，Q005对应正确内容诊断仍无法通过原查询恢复。只声称任务/评估关系，不申报新MIME解析器或新规划算法，不把超出公开接口的恢复称为可行。

## 方法设计的核心思想
用户任务明确要求提取“任务开始时全部未读邮件”的固定事实，初始list_unread_metadata只读返回opaque UID和MIME结构；真实正文仅通过后续工具可见。两个恢复读取操作分别为plain_unread与rich_unread：都重新查询当前UNSEEN，前者只暴露text/plain，后者公开支持HTML内容；两者获取正文可按公开配置置Seen。正文/UID稳定，没有新邮件、删除或其他参与者，不引入竞态。另有fetch_rich_by_uid作为真实公开、收费、稳定原目标的强控制，PEEK非置Seen方式也公开且计成本；不额外伪造隐藏复原接口。在线诊断使用UID对应公开MIME结构及已返回字段，指出有非空HTML部件但wrapper未暴露该部件，不读隐藏“哪一步错”标签。原查询恢复和固定UID恢复保持相同parser能力，唯一作用差是它们重新选取的集合；公开状态规划基线保留原UID并在当前状态读回，属于成熟方法。

## 最小实验
CPU确定性邮件任务：初始集合混有普通plain和正常HTML-only multipart，各正文包含唯一deadline事实，非目标邮件也存在。先获得初始UID/MIME结构，再进行plain_unread；它对HTML输出空content并把所取邮件置Seen或不置Seen。固定正文遗漏，对读取效应作两种公开协议成对；在每种协议中分别测从同一初态独立运行rich_unread，及在plain_unread后于同一不中断状态运行rich_unread。独立reset仅是离线评估分支，不给在线actor reset或隐藏原状态。没有置Seen时两者当前筛选集合相同，有置Seen时后者集合变空；这条确定性路径可作协议正例，不将其存在本身称模型发现。
对冻结actor比较普通/failure-aware FunctionCalling、公开确定性正确内容诊断coaching、按独立尝试矩阵选plain→rich的标准fallback、same-query rich重读、固定初始UID的rich恢复、PEEK及公开状态规划强基线。真实actor入口https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py已亲读；新任务所有动作/状态/成本闭合，无需部署真实邮箱。DARC离线矩阵标准参照只计算各操作从同初态的支持性成功及完整成本并选择链，不冒称复现其全部任务族harness。独立尝试、链执行和在线基线分开，不能拿额外reset支撑部署收益。
按全任务报告初始UID事实覆盖与正确完成、正确诊断后仍错的首个恢复动作、目标UID集合漂移、matrix预测与真实链的差、正确能力/预算阻断及完整成本。干净plain/HTML均可暴露条件、原任务明确要求“当前未读”的条件以及无固定UID/raw恢复接口条件作为边界：当前集合任务不能强行恢复原集合；无接口时不能以更大预算补出内容。支持研究任务价值需要在有充分预算、同公开诊断/信息/核心模型下，actor出现集合变更引起的恢复差距，且成熟固定UID/状态基线能区分内容遗漏与目标变化；若所有actor正常处理、差仅来自隐藏恢复能力、额外反馈、成本不齐，或既有执行任务已测完全同构关系，则没有独立贡献。所有metadata、读取、解析、存UID、诊断、推理、重试与等待计完整成本；纯控制器与同actor载体分列。参数待确认；本阶段无实验、实验代码、邮箱访问或付费模型调用。

