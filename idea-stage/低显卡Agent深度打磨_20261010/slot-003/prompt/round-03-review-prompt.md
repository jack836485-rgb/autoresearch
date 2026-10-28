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

**定位关键词：** LLM agents, procedural memory, sequential randomization, causal excursion effect

软件/知识工作agent在任务中反复看到同一经验时，当前执行状态已被先前暴露所改变；任务级价值与现在再次呈现的边际价值不是同一个量。

当前目标及演化依据：从计划编辑转向任务内再暴露的历史依赖，预计处理局部暴露的成本负迁移；不声称根据task内部效应决定永久淘汰。

https://arxiv.org/html/2608.24876：§2.2.2以草拟call/turn boundary事件触发技能；当前工作状态为以前技能/动作所影响的变量，不能把状态分层后的效应当起始总体效应。
https://arxiv.org/html/2610.02070：§2-3随机检索暴露识别query-conditioned effect；本版不重提positivity或把query效应聚合当保留价值。
https://arxiv.org/html/2502.13500：Distal causal excursion effect在动态治疗状态/过去干预会影响后续变量时，以明确参考干预制度比较当次干预的终末效应。
https://arxiv.org/html/2606.15017：辅助经验调用/提示占用执行机会，需与同总费用普通actor比较。
https://arxiv.org/html/2403.08978：Algorithm2在每步状态选择建议并生成动作；再次提醒的时序和效果历史不能仅用current-context matching当识别结果。

## 核心 Claim

待验证：对曾经有益经验，任务中再次呈现可能增加重复验证而不提高终态成功；只有估计在真实历史分布下‘现在再暴露vs不再暴露’的终末边际效应，才能判断是否续发，不能用无经验总体对照或当前状态相关性代替。

## 方法设计的核心思想

开发阶段在预先公开定义的执行事件随机决定是否再次在最新上下文呈现同一经验（已存在的历史不删除），记录已知概率、过去暴露次数、公开工具receipt和本次费用。每个比较以同一既有历史制度为参照，并将后续再暴露按共同参考制度随机化，用居中/倾向加权回归估计续发对终态成功及成本的效应。测试冻结续发规则：同样检索但只在该公开状态/过去暴露次数的终末净效应有开发支持时再次发送；技能库保留不改，不声称‘不续发’消除了旧经验的作用。 可观察状态按工具receipt/任务明确约束与既有暴露记录构成，不用金标准子目标状态。与mHealth MRT不同，LLM的经验正文可能一直留在历史，因此处理定义为‘追加当次经验块’，反事实为‘不追加’，并不假设洗脱或遗忘；既有历史分布与后续随机制度必须相同。

最高近邻及差别：Recuris已有事件时技能检索，CMP有随机检索，动态治疗文献已有MRT/DCEE。本版候选只在区分‘重复提醒的边际效应’与‘经验总体价值’上可能成立；不把换到时序回归当充分新意。 AutoGuide已每步生成指南，本方案不宣称再暴露这一动作新；待区分的是无洗脱的增量处理能否产生近端/终末效应冲突，并指导较节省的提醒制度。AEWM已保留正常草拟动作，本方案不再使用该关系作新意。

## 最小实验

AppWorld train库/dev随机事件/test冻结；同actor/解码/任务/技能内容/可用动作/全链路总费用，比首次只发一次、每个匹配事件都再发、Recuris式事件检索、仅按当前state分层的续发、历史制度明确的终末效应续发。train/dev做逐任务机制分析；official test只报告aggregate成功/全部任务、续发次数和总费用。分首次/重复呈现的效应仅开发数据估计。近端‘验证成功’不能替代任务终态；旧提示及后续调用费用均计。若一般不重复注入已等效、无历史相关效应、或同费用控制器等效，则推翻。事件集合、随机概率、样本量、lambda/模型/费用上限待用户确认。

基线定义/复现：[{"name": "无经验/固定top-k/独立贡献屏蔽", "paper_url": "https://arxiv.org/html/2606.15390", "code_url": null, "reproduction": "完整标准定义：无经验不注入；top-k按固定文本相似度取k条；独立屏蔽在开发任务对固定Bernoulli掩码有无经验的成功差取均值、同任务邻居加权后仅保留非负条目。是明确标准基线，不冒充ASSAY官方实现。", "controlled_parameters": "同actor/解码/任务划分/技能库/检索容量/全链路总预算", "extra_costs": "开发归因rollout、embedding、注入、任何重试全计费"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]

