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
真实邮件agent的UNSEEN→RFC822读取会置Seen，而multipart只取text/plain可对正常HTML-only邮件返回合法空content；后一次重查当前UNSEEN不再作用于初始目标集合。该路径由源码和RFC3501§6.4.5推出，未实跑（https://raw.githubusercontent.com/MubashirShafique/email-assistant-agent/main/tools.py；https://www.rfc-editor.org/rfc/rfc3501.html）。DARC §4.2以独立受控尝试的success-cost矩阵选有序fallback，明确reset/重试语义条件，不能把改变输入的链失败说成原作保证被推翻（https://arxiv.org/html/2608.11772v1）。如果所有任务都有HTML遗漏，plain独立全任务成功0，cheap→rich被rich单独调用支配，矩阵没有理由选cheap前缀；因此当前研究对象改为“任务混合和读取效应使真实最优选链排序翻转”，不强制指定失败链。
EmailBench §3.1的评测后端读冻结集合，ToolSandbox已覆盖一般状态依赖，CIR已覆盖query/content消融（https://arxiv.org/html/2609.31906v1；https://arxiv.org/html/2408.04682v1；https://arxiv.org/html/2610.00372v1）。PlanB §2.2也已用old状态和可执行spec作fallback，原输入保持是成熟机制（https://www.hesam.us/cs/planb/planb.pdf）。Failing Tools原站搜索可读摘要，PDF及官方API遭验证页/403，尚未排除同构任务（https://openreview.net/pdf?id=j7YsSnA64D）。当前贡献仅是可执行选链排序的成对评估，不称新规划算法或更换PEEK参数为创新；正常邮件与公开Seen，无攻击/通知。

## 核心 Claim
待检验：在部分任务cheap读取独立成功、其余任务需要rich的真实混合下，从独立同初態结果选出的cheap→rich链可以在只读协议中成本最优，却在公开读取会改变目标成员的协议中被rich直接执行或固定UID恢复击败。研究的不是“任意两操作能否串联”，而是同一矩阵实际选中的策略在两种公开读取效应下，是否发生支持性成功与目标函数排序的逆转；其差异不能由内容能力或正确诊断变化解释。Q001是空正文/新空集合被加强成初始任务无内容，Q001-D02是读取反馈与状态变化，Q005是正确诊断后执行了对当前集合有能力、对原集合无作用的恢复。若矩阵没有实际选择cheap前缀，或只读与置Seen协议没有预测/执行排序差，选链Claim失败。

## 方法设计的核心思想
混合任务的用户目标仍是“提取任务開始时全部未读邮件的deadline事实”，初始UID/MIME结构公开、正文只经工具可读。plain-only任务比例记p，需HTML的任务比例1-p；cheap_unread只取plain，rich_unread可取plain/HTML，两者都依当前UNSEEN选集合。公开协议分别为读不置Seen及读置Seen；无新邮件、删除或其他参与者。失败阶段用公开MIME结构和结果字段生成同一个内容诊断，不使用隐藏原因/终态。rich_by_initial_uid、PEEK和按MIME类型直接选择rich/cheap的标准路由都提供为成熟强对照，不仅与盲重试比。
选择规则在开发集独立尝试矩阵上冻结，枚举rich单独、cheap单独、cheap→rich、rich→cheap等标准有序短链，以支持性success减完整成本惩罚选最大者；同候选空间、目标函数和tie规则用于两种协议，部署测试无reset。小确定性控制例可用精确协议定义解析，不靠LLM judge；其作用是证明存在非被支配选链，不能代替actor结果。设每次完整尝试成本c_p<c_r、免费额度0、惩罚λ>0：独立矩阵s_p=p、s_r=1时，预测链成功1/成本c_p+(1-p)c_r。p*c_r>c_p且λ<1/c_r时它优于cheap和rich单独。若原集合被cheap读取移出，native链成功只有p；再满足λ<(1-p)/(p*c_r-c_p)，rich在native目标函数下反而更好。此推导只适用于示例的完整固定成本；真实actor成本、诊断、上下文与执行效果依真实记录重新计算，不把单工具费用当全成本或声称实测满足这些不等式。

## 最小实验
CPU有限邮件任务同时含plain-only和需要HTML的初始cohort，各含唯一deadline事实；随机实例只改变opaque UID与事实，公开能力/成本不变。完整初始metadata不置Seen；cheap/rich处理所有当前未读并按公开协议改变Seen。from_same_initial的独立尝试仅是离线矩阵构建，不给在线actor reset/隐藏原状态。先比较四个短链的矩阵预测和在两种协议中的真正按序执行，必须保存actual selected chain并以全体开发/测试实例为分母；不能先挑cheap→rich失败实例再报排序翻转。p、c_p/c_r、λ按上面具有/不具有预测翻转的区间扫描，仅为未来待确认设计，不运行代码。选链不能使用测试oracle成功；开发反馈的构建费用与其他基线可使用的等额开发预算计清。
冻结actor普通/failure-aware FunctionCalling、公开内容诊断coaching、独立矩阵冻结链、公开状态条件化规划、MIME类型直接路由、rich-first、stable UID rich恢复和PEEK均为同任务参照；所有有actor版本用同model/decoder/总预算，纯协议控制器单列。已核实actor实现https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py；ToolSandbox实际https://raw.githubusercontent.com/apple-aiml-research/ToolSandbox/main/tool_sandbox/tools/messaging.py的search_messages只过滤/返回当前数据库，未发现其读取改变集合；不把原工具导入当邮件Seen任务复现。新任务所有输入/动作/状态可完整定义，rich parser一致，只改变查询目标作用域和读取效应，标准原型无需真实邮箱。
指标是独立矩阵预测与真实链的支持性成功差、策略排序翻转、正确诊断后有效首动作、初始UID事实覆盖、无必要rich/错误完成、干净损失及完整成本。actor贡献需在当前公开诊断/预算充足条件仍出现恢复差距，且成熟标准路由/UID/状态基线解释其对应原因；若actor自然按MIME路由并消除差，或只有强制链、隐藏能力、漏记成本造成差，任务价值受限。当前未读任务、p=0全HTML（rich支配）及无公开UID/raw接口均是边界；不能把当前集合任务强行改成初始集合。方法/诊断/矩阵训练数据与费用、存UID/metadata/解析/推理/读取/重试/等待全部计成本；样本、模型、重复、p/费用/λ/预算待确认。未执行实验、生成实验代码、访问邮箱或调用付费模型。

