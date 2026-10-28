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

**定位关键词：** LLM coding agents, procedural memory, self-consistency, adaptive verification

程序性经验可能既改变生成的代码，也改变基于重复生成一致性而决定是否继续验证的信号。较高的一致性可以来自同一错误过程被重复执行；这是待验证的经验效应，不把一般“高confidence会错”当发现。

当前目标及演化依据：聚焦冻结代码工作agent的经验暴露如何影响一致性门控的验证成本与漏错；不研究恶意上下文、训练权重或任意代理。由经验诱发过量验证扩展到经验诱发过少验证，但自然发生率仍未知。机制不再是随机补观测，而是检验跨经验暴露的行为一致性是否能替代同经验重复的一致性来分配验证。

https://arxiv.org/html/2610.04837：§III按同retrieval context样本agreement决定是否切换context及省略RCV。§VI函数级96%样本池没有重复代码，明确限制为line/API，不将函数级扩展当完成原作即新。
https://arxiv.org/html/2608.11888v1：§IV-C技能复用默认过程可诱发错误实现；§V-B67过量验证来自182效率回归，支持经验与验证行为有关，但不证明一致性错误门控已发生。
https://arxiv.org/html/2607.27484：Table1及§3已使用技能有/无、名称/正文/意义干预检验行为影响；跨经验曝光对照已有，不能称新因果识别。
https://arxiv.org/html/2601.05905v2：引言/试验显示perfect self-consistency不等于上下文扰动后的稳健知识；方法采用邻域一致性并训练SAT，不是软件程序经验验证调度。本方向不把一般假confidence重述为贡献。

## 核心 Claim

待验证：失败经验被重复暴露时，代码候选在公开输入上的输出一致性可能升高却无法减少隐藏错误，使按同经验一致性省略验证的策略产生错误停止。将固定采样预算在有经验与无经验两种暴露之间拆分，以跨暴露输出分歧决定是否追加公开验证，可能更有效地使用验证预算；只有优于同样预算的普通多上下文一致性才构成贡献。

## 方法设计的核心思想

以MBPP函数级代码工作agent为最小载体，先固定任务提示、合法公开test_list和由公开参数域产生的无标签probe inputs；冻结训练任务产生的失败经验库，按固定检索器取同一条经验。所有候选在独立CPU进程执行，得到逐公开probe的原始返回值或异常，不用代码字符串相等、哈希或hidden test输出。当前同经验基线将N个候选都在相同记忆正文下生成，用输出向量众数占比作agreement；提案用N/2有经验及N/2无经验，总N不增加，只有两组各自高一致但跨组结果不同才不给出高一致快停，转入已有公开测试/额外公开输入检查及actor修订。跨组不同不判哪组正确，也不凭此删经验；一般低一致仍走相同公开验证。验证预算从统一总预算扣，后继修订读真实公开执行反馈，没有hidden返回。公开probe是一次功能调用结果比较，确实替代需要更多actor+测试的验证步骤；不称完备语义等价。统一最终交付规则：先公开test通过，随后按固定验证器/固定顺序提交唯一代码；额外探测不能保证隐藏正确。训练/dev只用于校准global阈值和诊断，test运行调度器只读可见数据。

最高近邻及差别：CAREТ已joint context routing与agreement-based verification skip；BACKTRACE已有同task技能有/无干预；Illusions of Confidence已有pointwise consistency不足与邻域一致性；ReasoningBank/CONTRAMEM已有多轨迹对比构建经验，普通多上下文一致性成熟。本版可能剩余是程序经验作为一致性误校准来源及成本门控的具体可检验关系，跨曝光采样本身可能仍是成熟context ensemble，不标合格。

## 最小实验

用Google原MBPP公开text/test_list，已在线读真实jsonl，test_setup_code运行但code/reference及challenge_test_list不入actor。使用EvalPlus增强测试仅offline终态评价，预先任务ID映射/公开例子处理，训练、dev与冻结test严格分开；这是明确MBPP+自定义函数级agent协议，不冒官方CAREТ结果。比较无经验、固定经验、同经验agreement gate、跨曝光agreement gate、普通随机split/不同相关经验的多上下文gate、全量固定公开验证；强对照普通多上下文完全相同N和probe/修订/验证规则。所有模型/decoder、publictests、初始代码、任务、库、N及最大步数/总API+CPU预算一致，embedding/库构建、全部N生成、probe执行、比较、验证和修订计费用，不拿CAREТKV/FLOP优惠给API方案。报告隐藏增强测试成功/全部任务、每任务总费用与最大预算内完成率、错快停/所有快停、公开例子通过却隐藏失败的比例、分歧后修订真正修复率。dev通过同经验→无经验真实干预测是否高agreement而错误，以及跨曝光是否胜过普通split；不造恶意错误skill，只用自然训练失败编辑。若自然错误快停不存在、两组probe输出几乎都相同、普通多上下文等效或额外采样/探测吃掉收益，则推翻。N、公开probe输入采样范围、global门槛、模型、任务数及全成本单位待确认。当前不运行。

基线定义/复现：[{"name": "MBPP公开例子及函数级工作agent", "paper_url": "https://github.com/google-research/google-research/tree/master/mbpp", "code_url": "https://raw.githubusercontent.com/google-research/google-research/master/mbpp/mbpp.jsonl", "reproduction": "已在线读真实每行text/code/test_list/test_setup_code/challenge_test_list；例如task1有三个公开min_cost asserts。本protocol仅给text及test_list，reference code和challenge不入runtime。标准agent generate→公共CPU执行→同反馈修订→唯一提交完整可实现，不冒第三方官方agent。", "controlled_parameters": "同actor/decoder、合法公开tests、数据与总预算", "extra_costs": "执行、采样、所有revision计入"}, {"name": "同上下文/多上下文agreement验证门控", "paper_url": "https://arxiv.org/html/2610.04837", "code_url": null, "reproduction": "完整标准定义：N个函数候选、固定public probe输入、输出向量直接比较取得众数；global高agreement省额外检查、否则执行同公开验证器。普通多上下文随机split及不同相关经验使用同规则；CAREТ原line/API和RCV不当同任务完整复现，方法论文仍创新近邻。", "controlled_parameters": "相同N/temperature/probes/validator、唯一提交规则/总预算", "extra_costs": "全部proposal、probe、router与验证费"}, {"name": "EvalPlus仅离线增强测试", "paper_url": "https://github.com/evalplus/evalplus", "code_url": "https://raw.githubusercontent.com/evalplus/evalplus/master/evalplus/evaluate.py", "reproduction": "已亲读evaluate.py及data/mbpp.py；base_input/plus_input配canonical_solution生成expected不是runtime公开oracle。增强tests与reference只offline evaluator，需未来安装和taskID映射核实，当前无代码/数据下载。", "controlled_parameters": "所有方法相同offline测试", "extra_costs": "离线CPU评价成本单列并计总体研究预算"}]

