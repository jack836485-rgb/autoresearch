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
      "problem_id": "Q004",
      "problem": "失败经验的检索适用性与保留/淘汰判断混在一起时，局部有效经验为何可能在别的状态误导agent，误判反馈如何改变经验库？"
    }
  ],
  "drawbacks": [
    {
      "id": "Q004-D01",
      "description": "经验整体价值与当前执行状态适用性可能混淆；全库常驻暴露已有负迁移，条件暴露与淘汰已有解法。",
      "problem_ids": [
        "Q004"
      ],
      "evidence": [
        {
          "作品ID": "2610.02994",
          "原文链接": "https://arxiv.org/html/2610.02994v1",
          "位置": "表4",
          "观察": "相同冻结库常驻暴露使WebShop reward .364→.296，Mind2Web completion .651→.599。",
          "边界": "条件检索已被Sentry覆盖，不能简单加检索gate当新意。"
        }
      ]
    },
    {
      "id": "Q004-D02",
      "description": "基于router选择后的贡献估计有选择混杂；局部有益经验可能因全局淘汰判断被误删，此后者仍待验证。",
      "problem_ids": [
        "Q004"
      ],
      "evidence": [
        {
          "作品ID": "2605.22148",
          "原文链接": "https://arxiv.org/html/2605.22148v3",
          "位置": "§7",
          "观察": "作者明确贡献估计是关联量，因果解释需随机切换经验；内生评审盲点不在固定外生噪声结论中。",
          "边界": "不能将未经验证的局部收益翻转当事实；Ratchet已处理容量、淘汰及噪声。"
        }
      ]
    },
    {
      "id": "Q004-D03",
      "description": "相关技能/经验仍可诱发过量验证或重流程，成本负迁移可能被只看成功率的反馈漏掉。",
      "problem_ids": [
        "Q004"
      ],
      "evidence": [
        {
          "url": "https://arxiv.org/html/2608.11888",
          "finding": "上轮读v1 V-B与表IV：182个效率回归中，过量验证67、重实现流程30；可选操作被当作必须。",
          "boundary": "分母是效率回归，不是全部任务；原作已有条件化建议，本轮须查独立机制。"
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
    "Q004"
  ]
}

以下是当前四节 Brief：

## 背景

**定位关键词：** LLM agents, skill evolution, policy evaluation, evidence reuse

程序性经验经编辑后，旧版本的成功/失败与费用记录未必仍能评价新版本。RoMeRL沿同一语义坐标继承效用，EviSkill则重执行编辑引用的局部片段；语义相近与真实行为不变是不同条件。

当前目标及演化依据：把经验适用性/淘汰聚焦为编辑后的旧结果可否继承，不解决任意多次注入和任意真实有状态agent。研究边界是每任务一个预先规定的公开决策点一次暴露，随后共同执行策略；不将经典同状态同动作复用定律宣称为新理论。

https://arxiv.org/html/2608.02508：§6代表替换保留语义坐标Q，Eq21已承认新均值不同时warm-start偏差；仅加版本ID/reset不形成贡献。
https://arxiv.org/html/2610.05030v1：§3.2及C.3重放源prefix再执行edited skill触发片段；附录F.2局部replay仍重新执行目标区间。证据链接及短回放已有覆盖。
https://proceedings.mlr.press/v206/dann23a/dann23a.pdf：§4 Algorithm2相同state/action共用nextstate，expected disagreement决定复用效率；同动作复用及不同处采样已是成熟机制。本方向剩余问题是文本经验是否还经消息/理由影响后续policy，以及如何用执行接口建立可继承范围。

## 核心 Claim

待验证：对于一次经验暴露且后继请求仅保留实际执行历史的冻结LLM agent，文本版本更新的旧完成结果可以在当前完整实际工具动作未变的开发状态上复用；当暴露正文或生成理由进入后继history时，同动作并不足以继承旧结果。借此限定重测于真正改变行为的样本，可降低编辑准入成本而不提高错误准入率。研究贡献候选是这项文本经验的继承条件及可检验接口关系，经典policy sampling本身已有覆盖。

## 方法设计的核心思想

所有方法共享actor、解码和history formatter。每任务只在预注册的公开决策点临时注入一次待编辑经验；后继请求只含任务、真实已执行完整toolcall和工具返回，不含当次经验正文或未执行rationale。与官方ReAct默认消息不同，属于明确自定义执行接口；不能声称历史从未暴露。开发任务从初始AppWorld世界重执行真实源prefix，重建Python执行状态及相同公共history，不能只load DB快照当完整checkpoint。对固定开发prefix，新版本重新生成完整实际代码块a_new及真实proposal费用；旧版本a_old来自该prefix既有数据。只有完整payload逐字相等且后继policy相同才借用旧suffix的结果/费用；无需哈希、语义等价判定或隐藏状态访问。不同payload执行新的后继rollout；正文/理由仍进入后继的协议不允许仅凭相同动作复用。随机解码只复用本次生成样本条件的结果，不把一次相同推成版本策略相同；匹配和不匹配样本均纳入分母，无支持部分全测。当前新proposal费用必须计入，不能继承旧文本的prompt费用。旧结果只在开发评估器使用，测试runtime不读dev结果或隐藏终态。这里不是只缓存完整prompt：新正文不同但实际动作相同时有可能继承完成证据。

最高近邻及差别：RoMeRL已处理继承Q偏差的逐步修正；EviSkill已有证据卡、局部重执行与跨epoch传播；Dann2023及Harvesting Randomness2017已有同动作counterfactual数据复用，SPIBB已有支持不足时保守policy改进，GUI action-conditioned bisimulation已基于动作结果而非观测相似合并。不能把重合分组、reset、局部replay或matching当新。候选仅剩文本经验正文/理由通过后继消息造成的继承失效与一次暴露接口是否形成额外可检验关系；极可能仍是成熟policy evaluation的直接适配，尚无独立新意证据。

## 最小实验

AppWorld official train构建冻结经验并产生预注册编辑家族，dev保存公共prefix并诊断；official test仅冻结方法后aggregate，禁止逐test任务人工修改/分析。先在dev完整重测建立离线参照（隐藏评测只评估器使用），检验“同实际动作却不同后继结果”是否随正文/理由保留而出现，并检验一次暴露接口是否牺牲经验收益。比较同语义坐标直接继承Q、语义相似阈值继承、每版reset全重测、EviSkill式固定目标区间重执行、经典相同完整history+action分组的coupled rollout，以及当前限定继承域。经典coupled baseline得到完全相同开发prefix、一次暴露formatter和全成本预算，不能故意只允许它对版本ID分组；若它与提案行为/成本等效，则新机制被推翻。全部方法相同编辑序列、actor/temperature、任务划分、公共history/初始world、最大步数、总API+CPU预算，prefix恢复、proposal、回放、构建/判定/验证及重试全部计费。报告所有编辑上的准入错误率、dev全重测参照偏差、有效任务成功/全部测试任务、全链路费用、匹配率/未支持比例。必要对照为接口切断×复用的2×2，正文保留仅作机制消融，避免把干净history本身收益冒作复用增益。若经典coupled sampler等效、编辑很少动作重合、恢复成本抵消节省、或清掉理由使收益下降，则否定。模型、固定暴露事件、编辑数、dev样本、k及总费用单位待用户实验阶段确认，当前不运行。

基线定义/复现：[{"name": "完整可实现的代表Q继承/reset", "paper_url": "https://arxiv.org/html/2608.02508", "code_url": "https://github.com/YOUNG-fnxm/RoMeRL", "reproduction": "官方repo说明eval-only，无在线utility promotion/edit loop；定义标准per-coordinate EMA、版本替换继承Q并reset count，对比替换resetQ后全dev重测，不冒充官方在线完整复现。", "controlled_parameters": "共同冻结actor/数据/编辑序列/history/总预算", "extra_costs": "全部库构建和代表/版本评估费"}, {"name": "经典动作重合coupled rollout", "paper_url": "https://proceedings.mlr.press/v206/dann23a/dann23a.pdf", "code_url": null, "reproduction": "标准完整定义：同开发prefix/history下各版本生成实际完整payload，按直接相等分组；每组共享一次共同后继rollout，不同动作各自执行。不赋予本文专属接口，baseline也使用同一次暴露formatter。这是成熟定义，不宣称复现原tabular理论保证。", "controlled_parameters": "相同actor/解码、一次暴露事件、初始world、费用与所有编辑", "extra_costs": "每版本proposal、每组suffix、prefix重建和分组CPU全部计"}, {"name": "EviSkill固定触发片段重执行适配", "paper_url": "https://arxiv.org/html/2610.05030v1", "code_url": "https://raw.githubusercontent.com/Zhouyaner/EviSkill/main/scripts/run_eviskill.py", "reproduction": "已亲读scripts入口imports wmsm.evidence_pipeline.run_eviskill，l2-replay-ranges-per-edit与post-reject-replay-cap真实参数以及论文C.3；不把README当完整源码。使用完整可实现标准定义：固定支持区间、初始world重执行prefix、editedskill执行区间、同offline结果判断；不复制额外证据卡editor模块造成费用差。官方pipeline细节尚未逐函数核实，不声称完整官方复现。", "controlled_parameters": "同编辑序列和支持prefix/区间/actor/总预算", "extra_costs": "prefix恢复、区间与终态评估全计"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]

