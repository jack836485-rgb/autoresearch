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

定位关键词：tool-use、observation contracts、temporal validity、materialization。过期的工具访问凭据与已经取得的稳定内容具有不同有效期；正确诊断expired artifact并不指明该刷新哪一层或是否仍需刷新。 当前仍关联Q001语义不当使用和Q005诊断后的执行恢复，聚焦访问artifact与静态内容生命周期；未处理first-touch或一般错误数值。ContractBench §4.4/AppendixS（https://arxiv.org/html/2605.17281v1）显示正确过期标签未提高该类恢复，且已测TTL主动重排。本方向不把TTL提醒或排序当新意。

## 核心 Claim

待验证：当公开工具协议明确访问artifact只需在指定调用边界有效，而成功materialization产生不受该访问期限支配的静态内容时，将有效期义务绑定到实际消费位置并在materialization后转移/解除，比对来源整条链统一标stale或只附expired标签更能减少误诊、无效renew和延迟取得内容的失败；不保证无法公开确定生命周期的工具。

## 方法设计的核心思想

输入用户任务、公开工具前/后置语义、实际调用与结果。记录每个artifact的kind、issued_at/expires_at、消费操作及公开效应。对下一proposed action，检查其真正消费的artifact：发起HTTP请求需要URL当时有效，已成功取得的本地静态文件由materialization后置语义建立新对象，URL期限不继续约束其本地处理。若任务明确仍需远端URL或协议要求完成前有效，则保留对应义务。未知后置生命周期不推断永久有效。恢复只更新仍未消费的过期访问artifact；若actor已经明确选定需取得的静态对象，可在返回URL后将必要materialization连续执行，减少插入反思/验证造成的租期消耗。这不是绕过许可，工具只执行已有授权任务。输出是与当前消费位置相匹配的检测证据及renew/materialize/use选择，不自动宣称内容准确、freshness或完整性。所有actor计划、生命周期解释、下载、检查、renew与缓存传输计成本。 AWS官方（https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html）明确在HTTP请求时检查URL期限，开始下载可越过期限继续；不能误写所有协议要求完成前有效。缓存和typestate成熟，按效应迁移义务是否有独立贡献需判断。

## 最小实验

完整可实现CPU标准任务：静态对象内容在episode中不变，issue_url返回opaque字符串及截止时间；download检查请求开始时间，成功后用公开耗时推进virtual clock并返回本地file对象；read_local(file)不受URL截止时间限制；renew重新发URL并收费。另一协议变体require_finish检查下载完成时刻，第三变体reference_only只给远端引用无稳定copy。全部协议对在线方法公开，真实对象数据/任务终态只给离线evaluator。任务要求本地分析指定对象并保存正确结果，不要求交付URL。agent不读金标准DAG；仅从当前明确proposed action的参数绑定推消费位置。对比同冻结actor普通/failure-aware ReAct、expired-label coaching（在线由公开clock/expiry生成，非oracle）、全来源链TTL失效后renew、EDF/即时有效检查、明确typed materialization标准控制器及本方法。标准控制器完整定义：URL仅在其HTTP边界检验，成功file后续本地使用；直接控制器作为机制等价强对照，所有有actor的主比较保持同模型/解码/完整token与调用预算。变更只在义务传播与连续materialization安排；单列取消连续执行/取消义务迁移的机制对照。指标全部任务终态成功、正确artifact异常判断、renew次数、错误完成、干净任务损失及完整CPU/网络/API/clock成本。若收益由确定性typed controller全解释且更便宜，或复制后仍沿用URL作为强制任务字段，则核心迁移Claim不成立；不把当前valid当未来保证。模型/耗时/TTL/预算/样本待确认，未执行。 ToolMaze actor入口已核实（https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py）；ContractBench作者repo返回404、HF内容读取失败，未认定其完整可运行实现，保留为创新边界而采用上面完整标准任务。最小定义不用hash/checksum，不运行实验、不调用付费模型。

