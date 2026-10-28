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
      "problem_id": "Q002",
      "problem": "agent得到正确澄清信息后，为何仍遗漏原始约束或把回答对应到错误问题，怎样区分提问错误、回答绑定错误与后续执行错误？"
    },
    {
      "problem_id": "Q003",
      "problem": "压缩后动作不报错、也不重复，却操作了错误实体或沿用错误状态时，现有压缩评价能否察觉并保留对执行有用的状态？"
    }
  ],
  "drawbacks": [
    {
      "id": "Q002-D01",
      "description": "得到正确澄清回答后仍遗忘原始要求，或者把多个回答绑定到错误问题。",
      "problem_ids": [
        "Q002"
      ],
      "evidence": [
        {
          "作品ID": "2607.20536",
          "原文链接": "https://arxiv.org/html/2607.20536v1",
          "位置": "§6.7",
          "观察": "错误分析明确列出遗忘旧要求、回答与问题对应失败；无独立占比。",
          "边界": "描述性错误分析；模拟用户而非真人。"
        }
      ]
    },
    {
      "id": "Q003-D01",
      "description": "压缩后动作合法且不重复却可能产生错误终态，blocked/refetch评价无法覆盖此类静默状态错误。",
      "problem_ids": [
        "Q003"
      ],
      "evidence": [
        {
          "作品ID": "2608.06503",
          "原文链接": "https://arxiv.org/html/2608.06503v1",
          "位置": "§3.3、§7",
          "观察": "同状态续跑观测执行退化；作者明确承认当前verifier可能漏掉silent state corruption。",
          "边界": "静默错误未被原作量化，不预先声称频率或根因。"
        }
      ]
    },
    {
      "id": "Q003-D02",
      "description": "正确更新在存储中可恢复但未被后续动作选用，信息保留与实际使用是不同失败阶段。",
      "problem_ids": [
        "Q003"
      ],
      "evidence": [
        {
          "url": "https://arxiv.org/html/2609.38866v1",
          "finding": "上轮亲读CICM探针与干预，区分保留更新和选择旧值。",
          "boundary": "受控对话/日志；内部激活不能作为黑盒API方法必需条件。"
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
    "Q002",
    "Q003"
  ]
}

以下是当前四节 Brief：

## 背景

关键词：functional compression、side information、tool-use memory。Q002正确回答后的选择绑定可丢失，Q003压缩后可合法错实体。依据[AppWorld-UL §4/§6.7](https://arxiv.org/html/2607.20536v1)的用户独占知识/错误分析与[TRACE §7](https://arxiv.org/html/2608.06503v1)。[PAIR §3.1](https://arxiv.org/html/2609.36526v1)指出AppWorld缺失环境信息可以额外交互重建，额外步骤与成功不同。当前聚焦可恢复当前事实与不可由当前工具重建的历史选择关系，不主张所有缺失状态同类。

## 核心 Claim

假设当前动作所需的历史区别应按可见工具的可恢复性分配记忆，而非统一span效用；保留不能由正常工具读取重建的问答/历史选择关系，并把可恢复环境属性移到实际只读查询，在同完整成本下减少Q002错绑和Q003静默错对象。

## 方法设计的核心思想

将可见指令/实际问答/source-supported联合调用候选变成需区分的候选对。只有公开API schema和已知正常读明确返回该字段，且该区别属于当前环境事实而非历史选择/原问题选项时，才允许用实际重读作为区分边的载体；用户意图、确认时选择对象及历史关系不由当前工具结果代替。CPU联合选择逐字历史见证或合法只读query的覆盖，目标是在共享token/工具预算内覆盖当前所需区别；查询实际执行一次后其真实结果加入actor上下文，任何预测/重读失败保留为失败。未见未来数据不参加选择，不执行备选写动作，不宣称source判断正确。数据库函数通信的已知图压缩只提供原理，没有套通用压缩定理。

[Functional Compression through Graph Coloring](https://www.mit.edu/~medard/2010papers/funccomp.pdf)的函数/side-info必须区分原理已知；固定准确分布/函数不能迁移，方法不使用未实际读取的值。[ARC](https://arxiv.org/html/2607.25066v1)已有归档回取，[FOCUS](https://arxiv.org/html/2609.37590v1)已有未来span效用，[SAGE](https://arxiv.org/html/2511.08798v1)已有cost-sensitive澄清。此处存储/实际工具读取联合选择的独立性仍需核实，不把基本覆盖优化当新数学。

## 最小实验

AppWorld公开API同边界澄清任务，配对当前动作区别由用户回复决定或可由正常只读查询重建；再加当前字段变化但历史用户选对象不变条件。对照按recency保留、按FOCUS原文span未来引用选择（完整可实现原文协议）、只存全部Q/A及全属性、同parser但允许工具读替代所有区别、只存不重读。固定actor/解码/来源集合/工具/token与总输入输出预算。全任务统计来源分类错、实际query返回是否能区分、绑定/旧约束、合法错实体、Task Success与总成本。隐藏用户知识/终态只离线，不给在线方法；每次parser、查询、压缩、source回取/续跑成本计入。若只是更多查询解释改进、错误把历史区别当当前可恢复、同总预算不及全部Q/A保留，推翻。模型/预算/候选数/query上限/样本数待确认。

[AppWorld](https://github.com/stonybrooknlp/appworld)和[新任务指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)入口已亲读。单纯Q/A全保留基线：按同token上限逐字存全部已到达Q/A、工具属性正常摘要；只有历史源见证基线：同候选和parser选择原文，不执行额外requery；单纯全部requery基线：对声称可读字段都实际读，用户历史关系仍只从已见原文取，不偷用隐藏知识。CPU覆盖是完整可实现标准定义，每source覆盖pairs与已见schema读返回字段映射，query结果只在实际读后使用。FOCUS按原文算法/提示在同任务重实现；TRACE公共runner/模板允许新adapter新cohort，原研究harness未公开，不称完整原作复现。本轮未实验。

