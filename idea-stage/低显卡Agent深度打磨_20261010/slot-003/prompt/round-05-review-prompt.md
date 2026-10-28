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

**定位关键词：** LLM agents, procedural memory, stochastic dominance, budget-constrained inference

同一技能可能用更多检查换取较晚的正确完成；若只看一档预算或单个成功减成本标量，低预算下负贡献不等于所有预算下都无价值。

当前目标及演化依据：聚焦同一冻结actor与公开任务类内的经验完成成本分布，不声称对未知未来任务有最优全局淘汰；相对初始目标处理预算条件的暴露与保留混淆，D02选择混杂不作普遍解决。

https://arxiv.org/html/2609.14138：§III-B–D用初始任务特征联合选memory mode与generation tier，reward为正确性减归一化费用；联合资源选择已有覆盖。
https://arxiv.org/html/2606.25115：摘要及方法框架已有value-minus-harm per-byte、budget-triggered KEEP，不能把费用进入保留标准当贡献。
https://arxiv.org/html/2606.09421：§3/附录F已有经济utility驱动技能改写策略；成本/质量折中和条件化策略已有覆盖。
https://arxiv.org/html/2606.15017：§1及实验把辅助模块费用重分配给普通actor作为关键对照；相同actor阶段预算不等于全成本相同。
https://arxiv.org/html/2606.15390：随机技能掩码的贡献为成功差，本版不重提条件因果屏蔽。

## 核心 Claim

待验证：在actor对预算上限不作策略重规划、且只在共同公开状态类比较时，经验对正确完成成本的分布可能与无经验分布交叉。以分布支配判断经验可删、以当前预算处的完成概率差判断是否暴露，能保留高预算有益经验同时减少低预算成本负迁移；不把任意一档负分直接当永久有害。

## 方法设计的核心思想

开发集对同模型/解码/无budget提示的actor分别收集有/无经验到完成或共同最大步数的轨迹，预算作为共同外部停止条件。记录每步真实累计全部成本及离线完成结果，不在runtime展示hidden结果。用相同轨迹的可评价prefix估计F_e(b)=在成本不超过b时正确完成的概率，避免为每个预算档重做一套不同策略；这里不恢复agent/Python状态或运行反事实分支，prefix只做离线结果评价。对有支持的状态类，若F_e在全部预注册budget范围均不优于F_0且至少一处更差则标该类无保留收益；曲线交叉则保留库内，仅当前b有正差的区间暴露；证据不足不删。测试冻结曲线和state分组，只读可见任务/已发生费用查询；不推断超出开发支持范围的删除资格。

最高近邻及差别：LIMBO已联合memory/budget，Forget-to-Improve已有cost-aware KEEP，成本改写已有economic utility。当前可能的差别仅是有限预算下完成成本分布交叉及保留支配规则、同策略prefix样本复用；随机支配与anytime analysis均为成熟思想，不能把CDF表示本身叫新机制，待独立审。

## 最小实验

AppWorld train生成冻结库、dev收集共同最大horizon轨迹并用offline公开执行快照评价prefix，official test只aggregate。同actor/解码/任务/库/检索k/最大单次输出与全链路总API+工具预算，比无经验、固定检索、一档成功差屏蔽、明确可实现的LinUCB(memory on/off×预算档、reward=成功-lambda费用)、按完成成本分布偏序的保留/暴露。后两者共享同一开发rollout总费用，所有曲线估计/库构建/选择费均计；两方法各预算档固定同核心条件。dev诊断曲线是否交叉、prefix重用与逐档独立运行是否在共同budget-blind策略下相符；test报告成功/全部任务、总成本、库保留量，误删局部有益只dev独立全面干预参照。若LIMBO式成本控制或一档标量已等效、交叉不存在、prefix不能代表短预算策略或估计花费抵掉节省，则推翻。模型、任务类、最大horizon、budget单位/范围、k、lambda、样本量待确认。

基线定义/复现：[{"name": "无经验/固定top-k/独立贡献屏蔽", "paper_url": "https://arxiv.org/html/2606.15390", "code_url": null, "reproduction": "完整标准定义：无经验不注入；top-k按固定文本相似度取k条；独立屏蔽在开发任务对固定Bernoulli掩码有无经验的成功差取均值、同任务邻居加权后仅保留非负条目。是明确标准基线，不冒充ASSAY官方实现。", "controlled_parameters": "同actor/解码/任务划分/技能库/检索容量/全链路总预算", "extra_costs": "开发归因rollout、embedding、注入、任何重试全计费"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]

