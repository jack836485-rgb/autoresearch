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

关键词：partial evaluation、binding-time analysis、context compression。Q002正确问答后仍可遗忘旧要求/绑错回答，Q003压缩后可能合法错实体。依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)和[TRACE §7](https://arxiv.org/html/2608.06503v1)。当前聚焦同一请求内历史固定对象与动作时条件的混合求值，不声称已量化此失败、不覆盖任意未知未来。Dataflow §2–4的计算与结果图，以及部分求值书稿§5.2/§15.5的部分static结构支持该目标的表示依据。

## 核心 Claim

假设混合指令中的历史选定对象与执行时条件，需要沿表达式内部保留不同绑定时刻；按已确认问答部分求值、保留实时工具依赖的剩余选择程序，较完整结构化意图文本或全局冻结/实时标签更能维持澄清绑定与压缩后的正确执行集合，且同总预算有净收益。

## 方法设计的核心思想

冻结LLM将实际指令和问答转为有限公开API可执行选择表达式树：常量对象、谓词、集合交/差、实际只读API字段。每个叶子仅根据明确用户语义/问答来源标记已确认固定或实际动作时读取；未知标签不specialize，保留原句待正常澄清。CPU沿树传播binding-time：只含固定叶子的最大子树用当前已见工具结果/用户选择求值成ID集合；含实时叶子的子树保留表达式，输出“固定结果+剩余表达式”，在动作前以实际正常只读结果继续求值。例如已确认歌曲集合固定，但“执行时仍可用”的过滤仍实时；不预取未来、不用hidden DAG、不训练模型。不是追加closure字段：编译在子树处切断重复的历史重解释，同时禁止提前物化实时条件。抽取错/遗漏或API表达式不支持都作为正常失败。

[Dataflow](https://arxiv.org/html/2009.11423v3)已有图/结果/reference/revision，[STITCH](https://arxiv.org/html/2601.10702v1)已有意图指代固化，[Codec](https://arxiv.org/html/2605.17304v1)已有结构化语义压缩，均不申报这些本身为新。[Partial Evaluation原作者书稿](https://www.researchgate.net/profile/Peter-Sestoft/publication/213882771_Partial_Evaluation_and_Automatic_Program_Generation/links/5704f27108ae13eb88b92a5f/Partial-Evaluation-and-Automatic-Program-Generation.pdf)的经典static表示specialization时已知，不自动等于不变Agent事实；本适配以用户明确时间语义选择cut。方法不用作者gold程序或训练模型。

## 最小实验

公开AppWorld集合任务，任务含全固定、全实时和混合明确时间语义三类；实际问答固定，合法可见更新分别改变历史候选属性或实时过滤字段，所有任务独立离线终态测试。对照：(1)完整同IR树和每叶binding-time标签仅作为结构化文本交给同actor（强信息匹配）；(2)同树采用全局冻结/全局实时；(3)同parser和同树但不部分求值、CPU每次按标签全重算；(4)同预算原文；FOCUS原文计划引用+遗漏补救与TRACE公开模板在同任务同adapter做重实现对照，不声称原harness全复现。主分母全部任务，报表达式/标签抽取错、正确回复作用范围、压缩后合法错成员、Task Success、工具读取/模型token及进展失败。支持需mixed条件相对强完整结构文本有净收益且全固定/实时不下降；若同IR未specialize CPU重算相同、只prompt强度或token分配解释、或parser错误主导/预算无净收益，推翻机制优势。actor/解码/总input-output预算、工具预算、parser调用共享对齐，所有前期解析/压缩/回取/实际读/续跑计成本；表达式语法、模型、budget、样本数待确认。

[AppWorld新任务指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)setup/solution/evaluation和[TRACE runner](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/collect/runner.py)/base模板已亲读，支持CPU任务与前缀重放。原研究harness未发布，同adapter新cohort不能称原作者完整复现。有限表达式树及上述强对照均完整可定义，不用Dataflow原任务成绩作AppWorldbaseline。本轮未运行实验/付费端点/实验代码。

