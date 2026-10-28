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

关键词：abstract interpretation、conformant planning、entity binding。Q002正确澄清后旧要求/绑定仍可丢失，Q003压缩后合法动作可用错实体。依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)和[TRACE §7](https://arxiv.org/html/2608.06503v1)。当前聚焦丢证据却生成更确定绑定的关系；这是待测压缩机制假设，不声称原作已量化其频率，不覆盖所有更新使用失效。

## 核心 Claim

假设压缩对原已见来源的遗忘，应扩大可能绑定集合而不能制造新的唯一绑定；把这一信息偏序约束落实到摘要修正与下一动作选择，可减少正确澄清后及压缩后的自信错实体。

## 方法设计的核心思想

用同一冻结API模型将已见指令、实际完整问答、工具schema变成有限binding候选和可见约束，CPU枚举B_H；同样抽取摘要的B_C。不读隐藏知识或gold。若B_H不包含于B_C，摘要排除了来源仍允许的可能状态：把导致缩小的生成断言替换为其可见允许集合/unknown，而不恢复整段H；受同token上限。actor提出下一动作时仅当其目标在保留的可能绑定下相同才直接执行，否则按正常工具读或已有问答原文回取消除该分歧。完整原文也不当真值：抽取不完整时只能条件性保留关系，没有通用soundness保证。不跑合成反事实工具，不加安全拒绝。

[Cousot抽象解释](https://cs.nyu.edu/~pcousot/COUSOTpapers/POPL77.shtml)和[Conformant-FF](https://www.cs.bgu.ac.il/~brafman/cff.pdf)已覆盖超近似/多可能状态决策原理，不申报新定理。[SAGE](https://arxiv.org/html/2511.08798v1)维护参数域，[TANGLE/CAAP](https://arxiv.org/html/2608.13921v1)已有保留不确定/冲突再决定；此处试图将摘要生成的知识增加限定在压缩前联合可能集合内，是否仅应用适配应独立判断。无法假定自然语言集合枚举完整。

## 最小实验

公开AppWorld API合成明确回复，控制压缩删除一条绑定依据与文本长度匹配。对照同模型自然摘要、同抽取但单值化、只保留joint binding表、相同额外预算直接原文回取；另将FOCUS原文完整span引用和遗漏补救定义在同任务实施，TRACE公开模板/runner在入口核实后作为额外任务对照而不虚称已复现。所有边界计候选漏gold/约束抽取错、B_H与B_C的误缩小、合法错实体、澄清额外次数、进展停滞和Task Success。离线oracle B只做标明的诊断上限，不作在线输入。若仅oracle parser条件好、未知集合导致同预算进展更差、或joint表即相同，则推翻。actor/解码/模型/完整token与工具预算一致，解析/CPU枚举/压缩/回取/续跑全部计，未定域大小/任务数/预算留待确认。

[AppWorld实现](https://github.com/stonybrooknlp/appworld)入口已核实。有限域由公开API已见对象/schema构造，同抽取器、相同候选和相同source用于所有方法。已在线亲读[TRACE runner](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/collect/runner.py)与[loop](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/optimize/loop.py)：前缀重放自由续跑可实施，原harness未发布，新adapter标明为重实现新cohort；base模板已核实。不能拿README当完整原系统复现。所有在线方法不使用gold候选/终态，parser错误/漏候选和全部失败都计分，本轮不实验。

