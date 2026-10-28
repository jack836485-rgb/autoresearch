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

关键词：teaching set、version space、tool argument uncertainty。Q002正确问答可丢失跨问题绑定，Q003压缩后可合法地选错对象；依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)与[TRACE §7](https://arxiv.org/html/2608.06503v1)。当前聚焦可见来源的联合候选区分，不声称覆盖未知未来和所有更新使用失效。

## 核心 Claim

假设保留可见来源在当前工具候选集合上诱导的区分关系，比保留最高可能动作或独立参数边际更能减少正确多问答回答后的错绑及压缩后合法错对象动作；不要求原文actor动作正确，也不把任何候选当金标准。

## 方法设计的核心思想

在压缩边界由冻结actor一次生成有限schema-valid候选工具调用。对原始指令、问题-回复完整对和已见观察，抽取每条来源约束对候选的支持/排除/未知签名及原文位置。每条来源区分其签名不同的候选对。CPU贪心按新分开的候选对数/原文token选来源，使压缩上下文尽可能保留完整可见来源诱导的候选等价分区；无法分开的对连同未知状态明确提供actor，不伪装单值绑定。actor仅以所选逐字原文及固定任务指令决策。新实际观察到来后重生成候选和签名，不预知未来；原始观察可归档但任何回取计预算。没有正确候选或所有签名同错都不保证恢复。

[Teaching dimension](https://www.sciencedirect.com/science/article/pii/S0022000085710033)启发最小见证，已知正确概念教师不可迁移，故此处保存所有来源签名诱导的分区。[SAGE §3.2–3.3](https://arxiv.org/html/2511.08798v1)已有独立参数域belief维护，[FOCUS](https://arxiv.org/html/2609.37590v1)按未来引用效用选择，[KBRA §8.2](https://arxiv.org/html/2606.21732v1)按single-segment joint binding作成员支持检查；此处选择目的是有限候选的来源区分关系，问答完整对为一个来源单元，不做安全拒绝。[DPC](https://aclanthology.org/2026.acl-long.313.pdf)已用minimal distinguishing database选择SQL；本方法不生成环境，也不执行候选，只压缩实际到达证据，不以对照程序定真值。

## 最小实验

同AppWorld公开API交互压缩任务，构造各单参数域一致但可行joint tuple不同的澄清条件，及无相关性的对照。固定正确实际回答并自然压缩，所有任务统计原文候选覆盖率、源签名错误、压缩后的候选pair混淆率、绑定/旧约束正确率、合法错实体和TGC。对照完整当前关系表摘要、原文最近问答保留、同调用数同token随机见证、相同来源抽取但保留最大单参数域收缩来源；source-support partition与最终正确分开。若优势只在oracle签名条件或候选含gold筛选子集，或同完整预算不及直接原文保留，推翻部署Claim。模型/预算/候选数/关联arity/样本数待确认。

[AppWorld作者实现](https://github.com/stonybrooknlp/appworld)的AppWorld、world.execute、load_task_ids和world.evaluate已核实。任务在公开API上实现，用户按固定原目标回答，不改原终态测试。简单基线完整定义：当前关系表保存对象/约束/待办；最近问答按时间逐字保留；随机见证从同来源中同token抽取；单参数域对照按每来源排除单参数值数量选择而忽略joint tuple。核心模型、解码、token及完整总调用预算相同，候选生成/签名/压缩/回取/用户模拟/续跑皆计费。本轮没有运行实验。

