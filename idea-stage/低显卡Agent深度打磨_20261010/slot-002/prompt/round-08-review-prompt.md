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

关键词：data association、joint belief、context compression。[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)记录正确回答后仍遗忘旧要求与问答错配；[TRACE §7](https://arxiv.org/html/2608.06503v1)承认合法不重复执行可有silent state corruption。Q002在此检验整轮回答与问题的归属，Q003检验这些归属跨压缩后导致的合法错实体动作。当前聚焦Agent解析不确定性：用户已正确给全信息，Agent未必解析对；不声称用户尚未说清。

## 核心 Claim

保留多个问答归属之间的联合相关性，较逐问题独立选择最佳回答，能减少正确回答后的整轮错绑及压缩后仍语义相容但归属错误的实体操作。联合关联算法本身已有成熟原作，候选的独立性限于自然语言共享子句/互斥归属的压缩状态维护，尚需核实。

## 方法设计的核心思想

由实际pending问题与实际答复子句构兼容图G，同一冻结API模型为边判source支持/不支持/未知及字段。只在可见文本明确“各一个”等容量时加互斥；“两个都”可同时填多个问题，未知不硬加one-to-one。CPU保留联合可行归属，用交替cycle/factor表示未决交换关系，压缩保留问题原句与决定cycle的回复原文；actor一次读取完整联合归属而非各自最大边。若不同完整归属影响目标，回读原问答frame再正常澄清；没有归属则明确unknown，回读后仍空不执行猜测写操作。有限候选遗漏、支持误判和错容量均不获保证，真实计失败与成本。

[JPDA-FPF §III](https://arxiv.org/html/1303.1214v1)的joint association已知，但物理sensor/clutter与一目标一测量不能迁移自然语言；[SAGE](https://arxiv.org/html/2511.08798v1)维护工具参数域并作独立近似；[Dataflow](https://arxiv.org/html/2009.11423v3)已有contextual refer/revise；[binding capacity §9.3](https://arxiv.org/html/2609.30634v1)已区分边际与joint检索。此处不把belief、matching或factorization当新理论，不将静态recall结论视作执行有效证据。

## 最小实验

AppWorld公开多实体同字段澄清任务，固定正确回复/旧要求/压缩边界；包括独立问题、显式互斥及一句共享多槽条件，保留自然不完整/多余答复。对照同G构建成本的逐问题独立最佳边、单联合归属（最大source支持边数，tie固定序）、完整联合归属JSON、cycle/factor表示与最近完整问答原文。完整joint JSON是强信息对照，若相同则承认只有joint解析而无独立压缩收益；未知候选不按ground truth补齐。各方法在同actor/解码/总token与工具预算中续跑，G抽取/CPU匹配/压缩/回读/澄清用户模拟/重试全计。全任务统计错边支持、全轮joint归属、旧约束、合法错实体、终态成功、澄清数和总成本，不筛gold匹配子集；offline oracle匹配只作诊断上限。若容量误挡合法共享回答、全部问答强基线不弱或完整成本无净收益，推翻。问题数/保留归属数/预算/样本待确认。

[AppWorld任务接口与evaluation](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)已亲读；可构造可见任务、solution和独立初末状态评价。同G的匹配/JSON基线为完整标准定义，非原作代码复现。FOCUS可按原文方法透明重实现，仍须明示阈值/溢出协议；TRACE公共runner可用于新cohort，研究harness未公开，不能声称完整复现。本轮不实验，不调用付费端点，不生成实验代码。

