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
工具返回普通整数不一定支持精确结论；同一不完整观测却可能足以支持某个阈值动作。当前目标从一般隐式错误与诊断恢复聚焦到“结果限定语义×用户结论需求”，不要求恢复所有后台信息。Elastic官方文档的Track total hits规定gte表示下界、eq表示精确；同页Search timeout给出timed_out=true仍relation=eq的部分结果例子，所以单独升级track_total_hits=true未必恢复完整性（https://www.elastic.co/docs/solutions/search/the-search-api）。ToolUniverse审计§4–5已核实限定信息丢失和更强结论传播（https://arxiv.org/html/2609.26836v1）。这支持真实任务轴，但不证明冻结agent必有净收益，也不把公开协议本身当创新。方法路线尝试的是成熟区间需求精化：ThalamusDB aggregate bounds和Demanded Abstract Interpretation已经覆盖主要运算（https://saehanjo.github.io/assets/files/thalamusdb.pdf；https://arxiv.org/html/2104.01270v1），当前研究贡献仅可能是尚未被agent恢复任务测量的结论条件性任务与评估，不申报新区间算法。

## 核心 Claim
待检验的任务Claim：在工具数值、格式和后台限定相同而用户只要求存在/阈值决定或要求精确总数时，把恢复定义成“得到支撑当前结论的语义”会改变可执行恢复集合；只评价是否恢复原工具的精确完整响应会将足够证据误计为未恢复，单relation修复则会将不完整eq误计为恢复。提出成对任务以分离识别结果含义、选到任务所需恢复、修复权限/预算不足，检验这一新增轴是否提供已有集合完整性任务没有的可区分失败结构。Q001是正常数值被当成更强结论，Q005是正确知道count非精确却选无必要或仍无效精确重试。不覆盖未披露的任意数字污染、first-touch或一般工作流回滚。

## 方法设计的核心思想
公开任务要求包含结论类型及阈值；actor自行形成proposed action/answer。公开返回value、relation、timed_out、shard completion等真实元数据；另设wrapper仅投影整数的条件，并给公开、收费的raw_response读取能力或明确无该能力。运行时只能读当次公开信息，缺失metadata不能猜默认eq。采用标准语义基线把健全的部分非负计数解释为下界，完整eq解释为单点；区间对所有可能值给同一用户决定时可完成，否则选择公开精化动作。track_total_hits升级只修准确性，恢复未完成分片/重发完整请求修覆盖；公开工具不可完成时只能报告不能支持当前精确结论，不能读离线真值。raw、精确请求、分片重试、推理和等待都收费。这个基线是任务能力参照，不把它重命名为独立方法。

## 最小实验
完整可实现CPU标准任务：静态非负记录分三公开分片，Search(predicate,track_limit,allow_partial)返回计数与四种公开限定组合；count截断用gte，完整精确用eq，超时/分片缺失可保留eq但表示仅已处理部分。请求成功结果中没有错误记录或重复计数，保证部分计数为下界；此边界公开，若任意数值错则下界也无效不计为本任务。用户任务成对为N>=T布尔动作与精确N报告。例如value=100, gte, complete可支持T=50、不能支持T=150或精确；value=100, eq, timed_out可支持T=50而不能支持N=100。另有低于阈值的完整eq、缺字段wrapper和不能恢复的分片能力，防止永远yes/永远abstain。工具可读raw限定、升级track_limit、对公开失败分片重试、完整重新请求，权限/费用均公开，隐藏N和故障类别只给离线评估。穷举小任务的共同公开历史策略集合，标出对当前结论支持可达而完整后台响应不可达的实例；不能让oracle按隐藏世界临时选动作。
对比同冻结actor普通/failure-aware FunctionCalling、限定语义原样提示、异常类别coaching、所有非精确/部分响应均请求完全精确的标准策略、只升级track_total_hits策略、上述任务需求区间标准策略。普通actor实现入口为https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py，迁移到明确定义的新任务；不声称复现ToolUniverse或ThalamusDB整套系统。强区间策略可无模型实现但与带相同actor版本分列，全部控制开销计总预算。主指标是支撑当前任务且结论正确的完成率、误完全性、无必要精化、有效/无效修复动作、干净任务损失和完整成本；离线另报backend完整恢复率，检验其与任务恢复是否出现定义性差异之外的agent错误差异。若变化只是替换答案类型、已有agent任务已测同样限定交互，或区间基线完全解释而新任务未带来新失败结构，则贡献失败。模型/阈值分布/成本/样本/预算待确认；当前无实验、实验代码或付费调用。

