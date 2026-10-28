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

**定位关键词：** LLM agents、procedural memory、plan editing、negative transfer。

相关经验仍会让软件/知识工作agent重复本已计划的检查。本方向把经验的处理单位从整条程序改成相对当前无经验计划的可证实差异。

从贡献分数/全局淘汰转向同一任务中actor已有计划与经验干预的差异，预计处理成本负迁移；不处理Q004-D02永久淘汰或judge噪声。 原始过量验证证据：[SkillTriage §V-B/表IV](https://arxiv.org/html/2608.11888)。这是待检验机制，未运行正式实验。冻结actor，运行时只读任务/工具观测，不读隐藏故障或评测终态。

## 核心 Claim

待验证：技能相关性不等于需要注入整套技能；若当前无经验计划已经覆盖技能要防止的具体失败，只发送该计划相对经验所缺少的有证据约束，能减少程序重启/重复验证而保留经验对缺失动作的收益。

## 方法设计的核心思想

所有方法先由同冻结actor生成短计划P0，额外费用全计。开发时在成对skill/no-skill轨迹中提取可见任务要求、计划动作和最终实际工具动作，生成带前提的最小计划编辑经验e=(observable condition, undesired plan pattern, edit)。测试时检索相同k条，但只暴露与P0模式匹配的edit；P0已满足前提的条目输出空编辑。编辑只能增加当前任务要求但P0缺失的约束、替换已知误用动作或删除明示可选的重复检查，禁止臆造隐藏任务要求。保留原经验用于其他P0，但不把无编辑当整体无价值。

最高近邻：[Recuris §2.2.2](https://arxiv.org/html/2608.24876)已在草拟call时注入技能再重草拟；[SkillX](https://arxiv.org/html/2604.04804)已有pseudo-plan检索；[DeltaMem](https://arxiv.org/html/2606.03083)已有经验间差分后重建全经验；[成本改写 §3/附录F-G](https://arxiv.org/html/2606.09421)按任务/技能结构保留锚点。这些都不作为当前贡献。当前可疑差别仅为按P0拒绝零边际信息、暴露变成条件编辑，是否属于state-grounded memory局部工程化需要直接判断。
[BACKTRACE](https://arxiv.org/html/2607.27484)已干预技能意义、措辞、身份、内容和分配；本方案不把换措辞、行为归因或对比轨迹当新意。[CTA §3](https://arxiv.org/html/2605.11946)明确paired trace为描述性对比；本方法的生成轨迹不能当成因果已证实。[CMP §2–3](https://arxiv.org/html/2610.02070)已处理随机检索识别/不可逆淘汰；本方案不声称解决全局淘汰。

## 最小实验

AppWorld公开CPU任务，train构建经验，dev选编辑与阈值，test冻结。相同P0生成过程/actor/解码/库/检索k/全链路总预算，比完整技能、任务条件改写、Recuris式草拟动作后全技能重草拟、只删除重复文本、计划相对edit。报告全部任务成功率、每任务总费用、重复检查/程序重启次数和编辑错误率（最后仅离线人工/结果复核）。机制交叉：P0已覆盖 vs P0未覆盖技能要求；只有已覆盖组减重复而未覆盖组保留收益才支持。若只是缩短token或依赖额外planner预算，推翻。模型、k、任务量、计划长度与总预算待确认。

可跑环境入口已亲读：[AppWorld environment.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/environment.py)的execute与save/load_state；[react_code_agent.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py)的next_execution_inputs_usage_and_status记录usage、读输出、生成代码；[agent.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/agent.py)为执行循环。本阶段未安装/执行。基础无经验、top-k、逐条屏蔽可按完整标准定义实现：同库同检索，分别不注入/取固定k条/开发集随机mask有无该条成功差加权后非负保留。Recuris式动作前全技能重草拟与任务条件改写属于限定机制对照，不冒充官方论文完整复现；若关键区别必须依赖官方完整复现而暂不可得须记录阻断。P0、经验构建、embedding、编辑提炼/选择、验证及重试全部计入总预算；无经验可把省下费用用于actor。
