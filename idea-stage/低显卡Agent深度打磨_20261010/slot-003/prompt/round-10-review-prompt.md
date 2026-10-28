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

**定位关键词：** LLM software agents, procedural memory, evidence selection, memory-guided rereading

经验可能通过补充旧知识影响agent，也可能只是指出当前任务/工具输出中哪些已见事实值得再次使用。相关经验正文可同时引入旧实例或重流程；这不意味着它提示的当前证据选择规律毫无价值。两种作用不同是待验证关系，不能把重读本身当新意。

当前目标及演化依据：聚焦软件agent中的失败经验复用方式：从要求actor照旧流程执行，改为经验只选择当前已见证据，不向actor传递历史事实或动作建议。探究同一经验在两种介面下效用符号是否可不同；不处理全部淘汰/因果选择混杂。不会把神经attention机制当API可观测变量。

https://arxiv.org/html/2608.11888v1：§IV-C样例/default过信可造成实现错误，§V-B经验可诱发过量验证/重流程；支持正文有负迁移风险，不证明证据cue一定有效。
https://arxiv.org/html/2606.09421：§3/F/G已有API/code、rule/formula、workflow改写及economic utility，正文压缩和换表示不能独立成立。
https://arxiv.org/html/2605.10268：§2.3/3已有memory-guided targeted rereading，零样本/API式迁移也有附录E；不能把冻结模型/重读/子问题当新。其terminal memory可缺失信息，本方向限定追加给actor的是原有当前上下文中的摘录。
https://arxiv.org/html/2606.17612：§III-B已针对当前静态/动态证据提出what/why/how问题，诊断可提前stop；针对证据提问和trace聚焦已有覆盖。
https://arxiv.org/html/2512.14982：同prompt重复可改善若干非reasoning任务，包含padding控制；重复/位置改变本身已有。

## 核心 Claim

待验证：在冻结软件agent中，同一失败经验的直接正文暴露可能增加错误/费用，而将其作为选择当前已见证据的规则、只追加当前原文摘录，仍可能有正的行为/成本价值。因此，按正文是否帮助来淘汰经验，可能丢掉另一种复用方式的价值。只有历史失败驱动的证据选择优于同信息费用的普通当前证据检索/重读，才有独立贡献；不把该关系或收益称已有结果。

## 方法设计的核心思想

train失败经验和公开轨迹产生冻结的证据定位query，而非action recipe；query只能描述当前任务指令/已返回工具观察中要找的内容，不带旧实体、旧数值、补丁或要求执行旧workflow。测试时router仍可选该经验，但actor不会读正文：同预算选择器按query从actor本来可见的完整当前上下文中选原文span，追加摘录及其普通消息位置。任何未返回观察/外部资料/reference都不可选，未找到就不追加，不另发强制检查。query选择本身带来salience信息，明确承认这不等于信息论上的“没有新信息”；仅承诺没有新增task事实，不声称神经attention已经被测到。方法的唯一新候选关系是同经验正文与其证据选择用途的不同价值，当前没有新encoder/多模块或因果理论。

最高近邻及差别：MemReread已memory-guided rereading及零样本迁移，PracRepair已诊断问题聚焦当前执行证据，Re2/Prompt Repetition已重复收益，ExpeRepair已有失败feedback驱动经验/动态prompt，RSCB-MC/LIMBO已memory mode选择与cost-awareutility。当前可能剩余仅是同失败经验在正文和当前证据选择用途下的效用差异与淘汰含义，选择器与同query普通重读极可能同构，尚无独立机制依据。不得因为正文未给actor就断言完全新颖。

## 最小实验

AppWorld train冻结经验/query，dev亲读真实失败轨迹，test仅official aggregate；在线只任务/API公开文档和真实返回观察，没有ground-truth行动、隐藏终态或用户隐藏知识。相同完整history/body产生的公共数据始终给所有方法，所有actor/model/decoder、retrieved经验、k、turn/总API+CPU预算一致，摘要/定位query构建/选span/重读/验证/重试费用全计。比较无经验、正文暴露、同经验成本改写、当前task-only证据检索、当前诊断问题驱动重读、同失败query驱动原文摘录、随机等长span、同span原位置引用/末尾追加、全prompt重复。强对照普通证据检索/重读拿到相同冻结失败query和当前上下文，并用同span候选范围、相同selector/费用；不能剥夺它历史query。若它由此与方法同构，则方法独立性失败，不能靠换称呼或少算准备费胜出。固定selector后比较同经验body与cue的价值，用训练/dev配对干预排除task难度；test不根据逐任务oracle选择mode。报告成功/全部任务、所有费用、正文相对无经验的负迁移率、cue相对正文和普通query重读的改善、摘录有效命中/全部query、错误旧实例使用与检查调用数/全部任务。只有在dev真实body有害且同经验cue有效，并超过普通强对照，才支持；若只是同span位置/重复效应、普通重读等效、正文没有自然负迁移或选择费用抵消收益则推翻。库/query定义、span上限、selector、模型、task量与预算单位待确认；不运行实验、不生成代码。

基线定义/复现：[{"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}, {"name": "当前证据检索/诊断问题重读/同query选择", "paper_url": "https://arxiv.org/html/2606.17612", "code_url": null, "reproduction": "完整标准定义：当前history按消息及公开文本段分span，task/currenterror query或相同冻结失败query交同选择器，取相同上限原文span追加；不同query条件以共同候选集合对比。同query对照不能故意弱化，若同构则否定，不冒称PracRepair Java/Joern官方运行。", "controlled_parameters": "相同history/query/selector/span范围、actor/解码/费用", "extra_costs": "query构建、span定位及所有追加input费"}, {"name": "MemReread和普通prompt重复边界", "paper_url": "https://arxiv.org/html/2605.10268", "code_url": "https://github.com/iiGray/MemReread", "reproduction": "已亲读原文§3/C算法及作者公开repo根目录，具体inference函数尚未逐文件核验；用完整标准定义的冻结问题分解→原history按query重读→回答作为当前任务adapted baseline，不称原GRPO模型官方重现。Re2/全prompt重复直接把公共prompt按固定次数重复，同模型同费用统计。", "controlled_parameters": "共同模型/decoder/history和完整budget", "extra_costs": "分解/读/选span/API input与任何模型call均计"}]

