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

**定位关键词：** LLM software agents, procedural memory, hygienic macro expansion, variable binding

软件agent复用经验中的代码样例时，当前任务值、程序常量和样例的局部变量承担不同作用。把实例值全部保留会复制旧任务要求，把所有值都参数化则可能改变必要常量；共享Python执行命名空间又可能使局部变量覆盖当前变量。前两类过信样例有原作支持，实际name capture在agent中的发生率仍是待验证假设。

当前目标及演化依据：聚焦具备可执行Python片段的程序性经验，研究适用性究竟由实体匹配还是可保持的绑定结构决定。仅对可解析片段声明机械绑定性质，不对任意自然语言skill承诺卫生性；不是泛参数化、类型schema或包装完整skill。失败诊断和样例再解释/重试费用均计入。

https://arxiv.org/html/2608.11888v1：§IV-C明确82/125功能失败为错误填充/缺项，相关skill默认值、examples、templates被过信为任务要求；比例非全任务。没有原作证据证明变量capture频率。
https://arxiv.org/html/2409.07429：§2.3/A.1已将non-fixed input text/button strings抽象成descriptive vars，基本实例参数化与contextbias降低已有覆盖。
https://arxiv.org/html/2605.15215：§3.1–3.3编译package、typed operators与boundary contract、runtime动态实例化已有；普通function wrapper/typed kwargs必须为强对照。
https://prl.khoury.northeastern.edu/img/kffd-tr-1986.pdf：§1/4已有按generated/user identifier来源保持绑定、alpha conversion及卫生宏；基础scope算法是成熟迁移，不称新理论。

## 核心 Claim

待验证：在共享执行命名空间、只复用部分代码样例的冻结软件agent中，相同词面任务参数不等于可安全共享的绑定角色。将任务绑定、经验内部绑定与程序常量分别保留，可使同一经验的行为对当前任务无关的变量重命名稳定，降低实例复制及局部覆盖造成的错误和重试；若普通参数化函数封装或SkillSmith式typed operator已等效，则该机制新意不成立。

## 方法设计的核心思想

仅处理训练经验里可解析的Python代码片段。构建时以真实任务指令/已执行代码/工具输出把可由当前任务替换的输入位置与片段新引入的局部binders区分，保留已公开API名和程序常量；若来源无法判定则不作替换，不假设LLM判断有证明。片段经Python AST建立load/store及词法作用域；任务输入以显式参数传入，片段产生的局部绑定在展开时只绑定同片段引用，不捕获调用侧变量，允许更新的任务输出位置必须显式声明。不用随机nonce、hash或兼容框架。actor仍决定是否调用/填参数及其余正常代码，不让方法读hidden目标。仅在该受限代码接口内检验alpha-renaming/实例替换后绑定关系；不把字符串模板或自然语言遵守指令当形式保证。模型生成成本、解析/绑定识别与执行/验证/重试费用全计。

最高近邻及差别：AWM已参数化、SkillSmith已typed compilation、CONTRAMEM明确禁止copy stored entities、BASM已有结构化contextconditions；卫生宏本身自1986已解决capture。候选剩余仅是部分经验片段复用的来源绑定条件是否与当前task语义参数适用性形成必要区别；普通functionwrapper极可能已消除核心机械问题。本版不宣称一般scoping新颖，不标合格。

## 最小实验

先用AppWorld train/dev真实代码轨迹和公开任务值生成冻结可解析经验库，重用common Python环境及ReAct入口；仅当开发中实际出现片段/调用变量共享和任务实例复制时纳入诊断，不构造本项目不支持的符号/并发问题。所有test保持official aggregate；另可用train/dev构造明示的变量重命名和任务实例替换对照，称派生开发诊断而非官方benchmark成绩，不改test隐藏判断。比较原样例、AWM式non-fixed值参数化、普通具名参数function封装、SkillSmith typed operator标准定义、来源绑定保持；各方法相同retrieved片段、原程序常量、taskinputs、actor/decoder、最大turn和总API+CPU预算。普通function封装得到同参数角色/输出范围，不能故意让它猜错inputslots；如果这样已等效，则新机制被推翻。诊断当前task值使用错误/所有调用、局部覆盖/所有展开、alpha重命名前后公开执行差异、实际任务成功/全部任务与全部费用。隐藏终态只offline evaluator，源代码/常量可公开读而oracle行动/DAG不能runtime读取。若自然可达问题无支持、绑定识别比直接actor更错、普通functionwrapper等效、或费用抵消节省，则否定。Python受限语法、片段库、N、模型、task子集/检索k与总预算待确认，当前不运行。

基线定义/复现：[{"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}, {"name": "AWM式参数化/普通function/typed operator", "paper_url": "https://arxiv.org/html/2409.07429", "code_url": null, "reproduction": "完整标准定义：同源片段，替换来自task的实例inputs为形参、保留API常量；普通function封装局部scope并用显式return输出；typed版本加input/output规范。全部获同角色识别信息，不复现WebArena旧官方分数；SkillSmith原创新仍保留，不因源码未核就忽略。", "controlled_parameters": "同source/taskbinding/output范围/actor/预算", "extra_costs": "抽象、角色识别、解析及调用全部费用"}]

