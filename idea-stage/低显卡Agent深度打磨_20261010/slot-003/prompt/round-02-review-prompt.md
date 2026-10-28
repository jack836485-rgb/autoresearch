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

**定位关键词：** LLM agents, procedural memory, minimal intervention, action editing

冻结知识/软件agent已经拟定下一条动作时，再把相关经验放进prompt让它整体重草拟可能改变原本正确的部分并引入额外验证。本方向研究经验的干预范围，而非仅看其检索相关性。

当前目标及演化依据：从长计划的‘已写出要求’改为当前草拟动作的受控修改，移除计划意图等同执行覆盖的假设；聚焦Q004-D01/D03，不处理永久淘汰。

https://arxiv.org/html/2403.08978：§3.2-3.3从成对轨迹分歧提取条件建议，并在每步按上下文选择和在prompt内辅助重新生成动作；局部建议生成已覆盖。
https://arxiv.org/html/2608.24876：§2.2.2草拟call不执行，发not-executed结果和技能，再由actor生成动作；本版必须区别于此重草拟。
https://arxiv.org/html/2605.14051：附录E.5要求minimal repair、无修复返回原计划；单纯minimal/noop指令无创新。
https://arxiv.org/html/2605.29794：§4.2及附录B.2 renderer按task及共现skill描述改写，并利用训练trace；不读取当前无经验草拟动作。
https://github.com/StonyBrookNLP/appworld#evaluation：Agent Development Restrictions规定test只 aggregate，train/dev可人工分析；不把task-wise test错误报告用于机制分析。
https://github.com/AnwarDebes/reins：作者系统已有model-free最小工具轨迹edit shield；确定性最小干预本身不是新意，不扩展本方案为攻击防御。

## 核心 Claim

待验证：相同经验知识下，令经验作用为当前默认动作的局部修正、且零修正时执行原动作，能够比上下文条件化重草拟减少旁支程序和成本；差别在默认动作的保留关系，不能由更短提示或一般条件建议单独解释。

## 方法设计的核心思想

每步先产生不读当次经验的默认动作a0（既有history不重置）；以当前任务和已观察工具输出检索同样k条经验。一次冻结模型判定仅返回所需局部修正δ及引用的可见约束，或δ=空。空时直接执行a0，actor不接触经验正文也不重新生成；非空时以a0+δ让同actor只修正该动作，输出仍是actor生成代码/call，不硬编码API。解析器要求工具选择/参数的改动属于δ列出的当前call字段，修正不能引入新流程或未要求的额外验证；无法表示的改动放弃当次经验，保留a0。原经验仍库内供其他动作使用；没有编辑不是整体无价值。判断、编辑调用与失败fallback全计费，既有history可受先前经验影响因此只声称当次增量效应。

最高近邻及差别：AutoGuide条件建议、Recuris草拟动作检索、SPIN最小修复/noop和Reins确定性min-edit都已读并保留。窄差别是自动经验的编辑足迹与‘空修正不让正文进入actor也不重生成’的动作保留关系，采用相同δ内容反事实区分；没有宣称最小修改或条件检索本身新。

补充原文边界：[SkillSmith](https://arxiv.org/html/2605.15215)已把skill编译为最小可执行boundary contract、选择性披露并降低重复解释；本方案不以编译、局部披露或typed runtime为创新，只评经验修正与当前默认动作的恒等域/改动足迹关系。

## 最小实验

AppWorld train经验、dev划分为参数选择/机制诊断两部分、test只aggregate成功与费用。dev复制同一合法前动作checkpoint，a0与经验固定，随机比较：AutoGuide式条件建议重草拟、长度匹配条件建议、P0最小编辑prompt、相同δ但总是重新生成、保留默认动作的局部算子、无经验。所有臂相同预动作调用和可见输入，开发建库/检索/判定/编辑/重试计同全链路总预算；不执行额外循环的臂可将剩余费用用于同预算actor。诊断检查δ=空时下一动作是否相同及整条任务额外操作是否下降；δ非空时改动足迹及最终成功。人工编辑判定/逐任务错误只train/dev，test只冻结后的aggregate结果。支持需‘相同δ内容但保留默认动作’改善成本且成功不降；若长度匹配/普通no-op策略同样有效、默认动作保留无额外作用或大量改动不能局部表示，则推翻。模型、字段解析粒度、k、样本/预算/非劣界待用户确认。

基线定义/复现：[{"name": "无经验/固定top-k/独立贡献屏蔽", "paper_url": "https://arxiv.org/html/2606.15390", "code_url": null, "reproduction": "完整标准定义：无经验不注入；top-k按固定文本相似度取k条；独立屏蔽在开发任务对固定Bernoulli掩码有无经验的成功差取均值、同任务邻居加权后仅保留非负条目。是明确标准基线，不冒充ASSAY官方实现。", "controlled_parameters": "同actor/解码/任务划分/技能库/检索容量/全链路总预算", "extra_costs": "开发归因rollout、embedding、注入、任何重试全计费"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]

