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
      "problem_id": "Q001",
      "problem": "工具输出格式正常却语义错误时，冻结模型能否在传播错误前识别异常，并以有限额外交互选择重试、换路或正确终止？"
    },
    {
      "problem_id": "Q005",
      "problem": "在失败原因已被正确识别时，为什么重试仍无法修复，如何区分诊断错误、指导不可执行、状态不可恢复与预算不足？"
    }
  ],
  "drawbacks": [
    {
      "id": "Q001-D01",
      "description": "格式合法的工具输出语义错误时，failure-aware提示仍不足以让agent发现异常并选对恢复策略。",
      "problem_ids": [
        "Q001"
      ],
      "evidence": [
        {
          "作品ID": "2606.05806",
          "原文链接": "https://arxiv.org/html/2606.05806v1",
          "位置": "§4、表2",
          "观察": "Claude Sonnet 4.6有提醒时，显式暂时故障PRR90.61%，隐式暂时29.99%。",
          "边界": "PRR只在遇扰动轨迹计，含正确终止；不能外推全任务成功率。"
        }
      ]
    },
    {
      "id": "Q005-D01",
      "description": "定位失败类别与可执行修复之间存在差距，工具异常和错误工作流状态的恢复很低。",
      "problem_ids": [
        "Q005"
      ],
      "evidence": [
        {
          "作品ID": "2605.08717",
          "原文链接": "https://arxiv.org/html/2605.08717v2",
          "位置": "§4.3、表3",
          "观察": "工具异常类修复3/47；状态/工作流类诊断35/42、修复6/42。",
          "边界": "均为首次失败子集；聚合率不等于正确诊断条件下修复率。"
        }
      ]
    },
    {
      "id": "Q001-D02",
      "description": "诊断工具调用既产生反馈也改变后续受扰动状态，恢复增益的证据通道与实际状态通道可能混杂。",
      "problem_ids": [
        "Q001"
      ],
      "evidence": [
        {
          "url": "https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/core/sandbox.py",
          "finding": "上轮已在线读取first-touch激活与首次调用扰动规则；这是受支持调用可达，不是毫秒竞态。",
          "boundary": "本轮复核实际源码；不把人工通道隔离当真实部署收益。"
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
    "Q001",
    "Q005"
  ]
}

以下是当前四节 Brief：

## 背景

定位关键词：tool-use、silent failure、top-k retrieval、query completeness。工具语义修复的可见正反例全部通过时，错误查询仍可能静默遗漏从未返回的目标记录；有限输出工具使这类修复证据缺口无法靠重复或本地补滤闭合。 当前从语义工具异常识别/可执行恢复聚焦完整查询证据覆盖任务，Q001/Q005仍同时处理，初始first-touch不足未覆盖。实际过滤漏结果见2018 REST API变形测试 §5（https://doi.org/10.1109/TSE.2017.2764464）；受限查询见GetNext §I–III（https://arxiv.org/html/1208.3876v1）。SilentProbe §4.5提供语义downgrade实证（https://arxiv.org/html/2609.00035v1）。不声称已跑本任务。

## 核心 Claim

待验证任务Claim：对输出受限且可能语义收缩的工具，现有检测/恢复会出现见证全部通过、所有返回行均满足用户条件但完整任务仍失败的轨迹。以目标查询的覆盖义务为任务单位，并显式分离缺少区分记录、无法取得区分记录和取得后未修复，可揭示仅用返回结果违约或参数见证准确率无法预测的恢复差距；不声称新的主动学习理论或已改进成功率。

## 方法设计的核心思想

任务输入为公开自然语言目标及等价可判定谓词、公开工具语法、top-k界限和可用记录域上界；工具只暴露read/search/get，用户要求精确目标id集合。隐藏数据和实际语义偏移仅由离线evaluator使用。输出为agent最终集合与明确未验证范围。任务单元同时变化查询选择性、可取得的区分记录位置与返回cap：目标阈值20，语义收缩30，可见40/10见证相同，但25只在不同公开查询或get中出现。评测记录每次恢复声明的证据是否排除遗漏，分别统计返回行soundness与完整集合recall。用三种公开工具可用性条件形成不同可恢复性：无id补读、已见id可补读、公开有限id域可补读。任务不把未发现记录标为runtime fault oracle，也不向agent暴露完整数据或参考修复动作；离线固定公共历史的策略树仅计算预算内能否存在同一公共策略，不以单世界oracle动作作为上线能力。 2018 REST API检测已使用完整分区关系，GetNext已有受限查询候选生成/测试；query repairs和Jigsaw已有正负示例修复（https://arxiv.org/html/2501.11162v1；https://arxiv.org/html/2112.02969v1）。本方向不申报新算法或新信息论，而判断这一恢复证据任务是否独立；普通增加故障类别不能自动支撑贡献。

## 最小实验

CPU有限表每记录id和数值，无写状态；search按公开数值阈值与类别筛选，最多k行、公开排序固定，get可见性按上述三种接口分别设置。离线正常/忽略谓词/阈值向内coercion，参数偏移对运行时隐藏；种子包含真实无匹配及被漏目标中间记录。从同原请求后公共前缀开始，比较同冻结actor普通/failure-aware ReAct、谓词违反警告工具列表、双见证编码筛选（完整定义为只选正返负不返的公开编码，若多种通过选文档顺序第一，不称证明完整）、原请求重试、已返回集本地滤、公开id域全枚举。公开编码穷举完整定义为按文档顺序逐编码执行并合并满足目标谓词的返回行；不使用hidden truth选择编码，不以穷举自动保证完整。固定模型/解码/数据/总token和调用预算，全部见证/probe/get/过滤计费。主指标全部实例精确集合成功和错误完整性声明，副指标soundness、recall、补读后同失败起点恢复及净干净损失。离线单列公共策略可达/不可达/预算不足，但不提供给在线方法。若失败全由普通top-k遗漏且无语义×覆盖交互，或既有benchmark已有同协议，则独立任务Claim不成立。样本量、k、预算、模型待确认，未执行。 ToolMaze公开Function Calling循环已核实（https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py）；Outcome-Monitor式arm按原作§3完整机制移植、不冒称作者artifact已核实（https://arxiv.org/html/2608.19303v1）。所有新标准方法均在同新任务运行，无隐藏词表、oracle选择或金标准DAG作为运行时信息。

