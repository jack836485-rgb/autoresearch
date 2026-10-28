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

关键词：conditional functional compression、observed side information、action constraints。[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)报告正确回答后的问答错绑和旧要求遗忘；[TRACE §7](https://arxiv.org/html/2608.06503v1)承认合法非重复动作也会有静默状态错误。[2608.16370 §3.3](https://arxiv.org/html/2608.16370v1)已经区分可查询状态与历史依赖状态，分类原理不新。当前聚焦同一真实环境观察下哪些历史约束不可删除：Q002测已给对的问答/旧要求，Q003测该目标域中的合法错对象，不承诺未知未来充分性。

## 核心 Claim

假设历史见证能否由当前环境观察替代，取决于观察与剩余历史的联合约束，而不只是字段可查询或候选间可区分。先取得实际只读结果，再保留使非空可行目标集合不变的原文子集，在同实际查询与完整成本下可能优于静态分类/区别对覆盖地保住排除关系并压缩冗余。

## 方法设计的核心思想

冻结API模型从可见H、实际问答及公开schema构同一有限候选调用域A和source约束F。约束表述某候选调用的目标/参数是否满足可见原要求；unknown不作排除，绝不读取金标准程序。先由同公开规则选择正常只读API并实际取一次结果r，各方法共享同组实际query；不预测未读值，不执行候选写操作。

CPU计算该有限域中同时满足F和r的目标集合T(F,r)。源解析为空时回读实际原问答，仍空则unknown/正常澄清，不能将空集当保留证书。按固定source顺序尝试删除整条历史见证f，只有T(F减f,r)=T(F,r)且非空才删；剩余原文见证与真实r进入同常规压缩器后续跑。历史用户选择不会因API字段可读就自动删，删它仍须不改变目标集合。这不同于只保留支持/未知/排除的候选分区：能区分两个调用并不代表排除了错误调用。自然语言parser和候选漏项可共同错，方法不保证集合包含真实目标；当前观察改变后不保证长期充分性。

[Functional Compression through Graph Coloring §I/III](https://www.mit.edu/~medard/2010papers/funccomp.pdf)的f(X,Y)条件编码及图着色已知，准确函数/分布不能假设由LLM给出；[复杂自然语言目标的值导向压缩](https://www.isca-archive.org/interspeech_2011/crook11_interspeech.pdf)已有已知POMDP模型的目标集合压缩；[HiGram §3.2](https://arxiv.org/html/2608.05095v1)已有按query/update定位证据路径。此处独立性只可能在真实API返回条件下的有限动作约束选择关系，不把条件编码、query-aware retrieval或约束冗余消除本身算新理论。

## 最小实验

AppWorld公开正确澄清边界，在同H及同实际query组下，配对真实返回让某历史约束冗余/不可替代：唯一/多个当前实体匹配、当前属性改变但历史选对象不变。原终态目标不改，所有任务保留，不筛source解析成功者。共享parser/候选域/source顺序/查询/驻留上限，比较静态可恢复性分类+候选区别对覆盖、普通结构摘要、最近完整问答原文、上述条件删除、全部历史强对照及直接source支持验证。全部历史超预算按同公开完整片段次序截断并记录覆盖，不假称信息等价；不为匹配call数白送构建成本。

全任务统计T与离线真实绑定的偏差、排除关系丢失、旧约束、合法错实体、终态成功与完整成本；空解析/域漏项/多目标均计入。所有schema/source读取、parser、CPU枚举、实际工具和返回token、压缩/续跑/澄清/重试从总预算扣，额外检测挤占续跑；同actor/解码/总输入输出及工具预算。若静态分类已足够、强对照相同、条件删除导致错目标或完整成本无净收益即推翻。查询选择规则/数、域枚举上限、source顺序、模型/解码/总预算/样本数交接待确认。

[AppWorld _setup/solution/evaluation公开指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)已亲读，评估预期及非预期终态变化。所有同任务约束/删除/覆盖对照为完整标准定义，非成熟POMDP原作复现；FOCUS原文§5/A.7确有AppWorld评估，但此处仅按其原文方法透明重实现，公开阈值/溢出协议，未核实完整作者代码。TRACE公共runner可新cohort，原研究harness未公开。本轮无实验、无付费端点、无实验代码。

