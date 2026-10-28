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

关键词：context compression、belief update、metamorphic testing。当前处理Q002正确澄清后的旧约束/多回答绑定及Q003同边界压缩后的合法错实体；依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)与[TRACE §7](https://arxiv.org/html/2608.06503v1)。聚焦已到达更新，不声称未知未来充分或所有保留未使用问题。

## 核心 Claim

假设澄清所引起的状态变化在两条表示路径间的稳定交互残差，比单次路径差异或直接coverage/preservation verifier更能定位压缩导致的绑定漂移；同总预算下按该残差回填减少Q002旧约束丢失及Q003合法错实体。

## 方法设计的核心思想

从同一可见H、实际u建立四格：先更新后压缩/先压缩后更新 × 实际u/恒等更新u0。恒等更新u0明确不添加事实也不改值；不是隐藏用户知识。对每格用同冻结模型和同投影schema得到字段。每条路径内比u与u0，得到字段转移（旧值/新值/不变/未定），跨路径只把转移不一致的字段列为候选；重复同格一次，只有同格转移稳定而跨路径仍不同的字段可选。所选字段的实际问答和原约束逐字回填重压缩一次；其余差异不修，不以一致性作正确性保证。该选择关系是实际更新×顺序交互，拒绝u0已存在差异或同路径抽取噪声。

[TrustMem §3.2](https://arxiv.org/html/2606.25161v1)直接验证coverage/preservation/faithfulness；[METAL](https://arxiv.org/html/2312.06056v1)已有一般变形一致性；[Useful Memories](https://arxiv.org/html/2605.12978v1)已有整体更新顺序效应。当前不声称这些既有原理为新。

## 最小实验

固定CPU AppWorld环境、同澄清问题和正确实际回答。只用不改变原任务终态的澄清：把原指令一个可见选择暂写为未知，用户答回原值，终态评估函数不改；多问题作合成澄清依旧答回原值。所有任务计数，离线独立标签。对照：(1)单路径结构摘要；(2)最近完整问答逐字保留；(3)同四格/重复调用数按单次两路径差异回填；(4)同调用预算直接验证coverage/preservation/faithfulness再按违例回填；(5)同格重复噪声驱动回填。共用同压缩器、来源候选、回填token上限、actor/解码/总输入输出预算；每格H输入、U、C、P、重压缩和续跑全部算，检测挤占续跑。主报所有边界的旧约束/绑定正确、合法错对象、TGC；预注册首动作相同且blocked/repeated均未报警子集占比和条件错误，不替代全样本。若交互残差不比直接验证准确，或只同格噪声即可解释增益，或预算挤占消除净收益，推翻。模型、预算、重复次数和样本数待用户确认；重复一次为设计定义可经确认调整。

公开[AppWorld实现](https://github.com/stonybrooknlp/appworld)的AppWorld(task_id)、world.execute、load_task_ids、world.evaluate已核实。冻结直接验证是同任务可完全实现的标准定义：给H、u、旧/新摘要标coverage/preservation/faithfulness及来源原文，按同预算修一轮，不冒称复现TrustMem训练。

