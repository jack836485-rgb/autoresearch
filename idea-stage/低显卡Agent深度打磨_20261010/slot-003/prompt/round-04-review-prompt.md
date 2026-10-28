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

**定位关键词：** LLM agents, procedural memory, selective labels, costly feedback

软件知识agent可能从经验学会省去检查；这既改变成本，也改变哪些失败能进入下一轮经验治理。本方向研究经验对观测通道的影响，不把缺检查等同已成功。

当前目标及演化依据：从任务内重复呈现转向跨任务反馈选择；新增Q004-N01是由原噪声边界和检查成本证据提出的待验证假设，不宣称已观测。只处理有公开验收检查的任务，不用隐藏benchmark测试为在线信号。

https://arxiv.org/html/2605.22148v3：§7把skill贡献的router选择混杂与固定外生judge通道的适用范围区分；未证明内生反馈盲点已发生。
https://arxiv.org/html/2608.11888：§V-B经验可导致过量检查，成本策略是合理目标；不能把反方向‘经验少检查导致反馈消失’当已观测事实。
https://arxiv.org/html/2609.36746：§3.2将环境暴露反馈与self-assessment作为资料，并将missing标为unavailable；§3.4明确时间credit仅近似归因，非精确causal。
https://arxiv.org/html/2610.02070：CMP已恢复retrieval positivity；未以memory改变后续测量选择为本版贡献，不重提随机检索本身。
https://arxiv.org/abs/1807.00905：Selective labels中决定过程决定哪些结果会被观察，单纯样本选择调整在零支持区域无法识别。
https://proceedings.mlr.press/v337/schur26a.html：可选且action-dependent付费观察的bandit已有理论，不把‘为标签付费/随机审计’当新意。
https://arxiv.org/html/2608.19626：测试演化可能把单一接受程序的输出误当ground truth；本版不能把自动新生成测试当真值。

## 核心 Claim

待验证：在经验能够改变公开验收检查执行概率的任务流中，以观测到的成功/失败直接治理经验可能把少观测误当少失败；将经验暴露与是否测量分别随机化、且测量在任务提交后不修改当前产物，能区分经验任务收益与经验诱发的反馈盲区，并减少错误保留。

## 方法设计的核心思想

任务必须含操作者已公开的独立验收检查集合，测试定义固定且不是agent自动写出的ground truth；隐藏评测器只离线。开发/可控训练流对经验on/off按共同已知概率分配；actor完成并提交产物后，以独立于经验内容的已知审计概率随机执行公开检查，不让测量反馈修复当次产物。记录检查是否运行、原返回值与费用，缺测保持unknown。经验治理只使用暴露×测量的双随机记录，经测量倾向加权估计对同一公开检查失败的净影响；不能将public-check pass称完整任务成功。测试流冻结actor/经验生成/审计制度，治理只读此前公开反馈，未来隐含真值不给方法。正作用但少检查的经验只在公开检查效应证据可辨时保留，证据不足不据未观测pass晋升；不宣称通用最优保留。

最高近邻及差别：CMP已随机检索，EASE已处理missing与行为概貌，selective labels/costly bandit已有观测选择理论。可能的独立差别是文本经验持续演化其自身反馈通道、任务提交后测量仅影响后继经验库的闭环；尚未找到直接机制覆盖，也未核实自然软件task数据具备这种反馈选择。

## 最小实验

未来用公开CPU软件任务构造自然public acceptance tests与独立hidden holdout tests：前者为方法合法可见工具、后者仅离线最终评价，先在开发任务验证经验是否改变公开检查率，不伪造该效应。相同actor/解码/任务流/初始库/核心预算，比较固定外生反馈治理、actor自主检查治理、missing=unknown、仅随机暴露、仅随机测量、双随机暴露/测量。双随机引入的审计、经验构建/估计/重试全计总费用，各臂可用省下费用继续actor或公开检查但须预注册一致分配。指标公开检查通过/全部被审计任务、加权公开失败估计误差（dev全审计参照）、离线hidden最终成功/全部任务、错误保留、成本及任务序列末端库质量。若memory不影响检查率，missing=unknown或标准costly-bandit已充分解决，或收益仅来自多检查预算，则推翻。模型/任务来源/检查开销/概率/总预算/分摊规模待确认；本阶段不运行。

基线定义/复现：[{"name": "无经验/固定top-k/独立贡献屏蔽", "paper_url": "https://arxiv.org/html/2606.15390", "code_url": null, "reproduction": "完整标准定义：无经验不注入；top-k按固定文本相似度取k条；独立屏蔽在开发任务对固定Bernoulli掩码有无经验的成功差取均值、同任务邻居加权后仅保留非负条目。是明确标准基线，不冒充ASSAY官方实现。", "controlled_parameters": "同actor/解码/任务划分/技能库/检索容量/全链路总预算", "extra_costs": "开发归因rollout、embedding、注入、任何重试全计费"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]

