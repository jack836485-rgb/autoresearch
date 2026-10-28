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

关键词：consistent query answering、repair invariance、memory compression。[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)报告正确回答后的问答错绑/旧要求遗忘；[TRACE §7](https://arxiv.org/html/2608.06503v1)承认合法非重复动作也可静默错状态。当前假设Agent从正确多问题问答抽取的约束可能因归属解析产生冲突；Q002测归属/旧要求，Q003测该分歧跨压缩后的合法错目标。冲突来自Agent解析的假设，不把用户答对后的源冲突作为已证实根因，不承诺全部记忆使用问题。

## 核心 Claim

源约束的不同包含极大一致修复可能允许相反动作，摘要却把这种源分歧折叠为某动作在全部修复中成立。只检查这一跨表示的确定性变化，并保留决定源分歧的问答见证，在同完整成本下能否改善错绑和合法错实体是待证假设；稳健全修复推理本身已有原作。

## 方法设计的核心思想

同冻结API模型从可见指令/实际Q&A构F_H，从摘要构F_C；公开schema和可见实体ID/字段值提供同有限联合绑定域。source约束是允许/排除实体、参数或问答归属的有限关系，unknown不排除；显式原文supersession先处理，不把合法新旧值当冲突。CPU枚举F所有按集合包含极大的一致source子集R(F)，以及每个子集的可行绑定，不按最大基数或模型分数挑唯一修复。

只当H中两个不同修复分别存在满足/不满足当前调用目标要求a的可行绑定，同时C所有修复的所有可行绑定均满足a，才触发。将这对不同修复动作见证所涉及的实际问题/回复/旧约束逐字回填一次重压缩，任一repair不当用户真值。H一致、H全部排除a、底层域无解、枚举预算不能穷尽均不触发/unknown并记未覆盖；不得把空集上的全称当证书。全部repair共同错误或有限域漏掉真实绑定仍无法保证。回填后仍未定正常回读原问答/澄清，真实计成本，不宣称消除了全部不支持确定性。

[PODS1999 §2](https://www.cs.toronto.edu/~marenas/publications/pods99.pdf)已有minimal repair/all-repair CQA；[QXR §3–4](https://arxiv.org/html/2601.13600v1)已有自然语言事实MUS与greedy hitting-set修复，系统性LLM误判不能靠重复解决；[知识动作修复 §4/7](https://www.ijcai.org/Proceedings/13/Papers/126.pdf)已有多repair执行语义及一致查询控制progression。[KR2025逻辑修复框架 §3](https://proceedings.kr.org/2025/32/kr2025-0032-frohlich-et-al.pdf)已用正/负query约束关系连接不同数据库实例并限制新增答案；所以不同表示间的答案保存也不是新理论。它定义修复空间，不直接给当前自然语言压缩的双修复见证回填策略，该剩余差别也可能只是应用，须独立判断。多修复、冲突定位和稳健动作均不申报新，独立性只可能在同源分歧跨压缩消失时的回填选择关系，而非经典修复语义的重命名。

## 最小实验

AppWorld公开多实体/同字段问题，包含互斥或共享子句、独立问题和合法显式更新；固定同正确回复、源parser及压缩边界，原终态目标不改。主实验不在线注入隐藏错误，不筛解析冲突/成功任务；统计源确有不同repair分歧、源唯一、源全排除及枚举unknown的比例，若分歧几乎不出现则该方法缺乏主任务价值。

同F_H/F_C抽取、schema/域、来源集合/回填cap，比较QXR原文MUS/greedy单repair透明适配、固定tie单repair动作检查、完整多repair JSON、直接joint source/preservation verifier、最近完整Q&A、本跨表示选择。完整repairJSON与当前方法共享压缩前的全部repair信息；共同用公开溢出次序/驻留上限并报告实际保留量，不能把截断JSON称信息等价。统一恢复/澄清规则与完整费用，避免把候选数量或多问用户当机制收益。QXR算法1及附录G oracle提示已亲读，可按公开定义实现；不声称原作已有AppWorld agent结果或完整作者代码已核实。

全任务报信号对离线错绑/旧约束/合法错目标的定位与漏检、终态成功、澄清/回读及完整成本；H一致/全排除不触发不计作检测成功，parser和域共同错如实报告。若完整repairJSON相同、QXR/直接joint验证不弱且更省、信号仅由parser误差驱动，或枚举/澄清挤占续跑无净收益则推翻。固定actor/解码/总输入输出与工具预算；全部source/摘要parser、QXR子集oracle、CPU枚举、验证/回填/压缩/续跑/重试计费，oracle绑定/终态仅离线评价。模型decode、枚举上限、总预算/样本待确认。[AppWorld官方_setup/solution/evaluation](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)入口已亲读；本轮不实验、不调用付费端点、不生成实验代码。

