## 结论

实际检索日期：**2026-10-10**。**score：7.2；verdict：promising_needs_revision。未通过实验就绪阈值。**

研究问题有价值：相同经验即使相关，也可能通过重草拟改变原本正确的动作；将这种副作用与经验内容、提示长度分开检验，值得研究。但当前独立新意比 Brief 所述更窄。**无须干预时保留当前动作、不给 actor 暴露恢复经验，Sentry 已明确覆盖**；局部编辑并保持其余部分稳定，也已有 REINS 和 SAVeR。尚未找到完整覆盖“自动经验决定当前 call 的字段编辑足迹，再由运行时约束 actor 修改”的同任务原作，因此不判定完整方案已被覆盖，也不列 fatal novelty blocker；剩余机制的新意与优势尚未充分建立。[Sentry §3.1–3.2](https://arxiv.org/html/2610.02994v1#S3)、[REINS 实现](https://github.com/AnwarDebes/reins/blob/main/reinskit/shield.py)、[SAVeR §3.5](https://arxiv.org/html/2604.08401)

目标演化成立：从计划覆盖转向当前动作的经验干预范围，仍关联 Q004-D01/D03。原始效率研究确实区分了提示开销与经验诱发的额外程序，支持这一聚焦；其证据来自 SkillsBench/SWE-Skills-Bench，不能直接证明 AppWorld 上同样存在该效应。不研究永久淘汰与 D02 不构成偏题。当前阶段、可见信息限制、冻结模型和测试集使用规则均符合硬约束；没有实测解决结论。[原始效率研究 §V](https://arxiv.org/html/2608.11888#S5)

## Claim 判断

| 当前主张／机制 | 判断 | 最关键原文依据与可验证性 |
|---|---|---|
| 经验不应进入 actor 并触发每次重草拟；没有必要修改时执行默认动作 | **已覆盖主要机制** | Sentry §3.1 明确无失败时无干预、无 playbook 检索、继续执行。REINS 的透明性直接要求合规动作保持恒等。当前判定依据是经验导出的 δ，区别不能放在恒等分支本身。[Sentry](https://arxiv.org/html/2610.02994v1#S3.SS1)、[REINS](https://github.com/AnwarDebes/reins/blob/main/reinskit/shield.py) |
| 自动经验输出当前动作的局部 δ，并限制修改足迹 | **部分重合，保留窄差别** | SAVeR 将诊断转为带位置和验收条件的局部修复，保持未受影响步骤稳定；REINS 已约束可实施的动作编辑。当前剩余差别是跨任务经验决定当前 call 的字段足迹，而非推理切片或声明策略。可在非空 δ 条件下验证，不能由空 δ 时少一次调用代替证明。[SAVeR §3.5、附录A.2](https://aclanthology.org/2026.acl-long.1440.pdf)、[REINS](https://github.com/AnwarDebes/reins) |
| 局部经验修正优于上下文条件建议，效果不能由长度解释 | **部分重合；联合效应尚待验证** | AutoGuide 已按每步上下文选取条件建议；BASM 已用边界条件与针对性修复提示控制经验迁移，并做等长度对照。当前的相同 δ 反事实有解释力，但完整成功率与费用优势没有证据。[AutoGuide §3.3](https://arxiv.org/html/2403.08978#S3.SS3)、[BASM §4](https://arxiv.org/html/2608.22339#S4) |
| 没有编辑不意味着经验整体无价值，不永久删除经验 | **已覆盖** | Sentry 将经验保留在外部库，按当前失败条件激活；不激活不等于淘汰。这是合理边界，不能另计为贡献。[Sentry §3](https://arxiv.org/html/2610.02994v1#S3) |
| 全链路成本降低，同时成功不降 | **可证伪，但当前实验判别不足** | 判据明确，尚无结果。当前最小实验没有明确纳入已有“默认动作透传＋必要时经验修复”的 Sentry 式对照；相同 δ 但总是重生成，可能主要测到已知的跳过冗余调用收益。 |

实现入口可核验：[AppWorld ReAct](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py) 确实生成 Python、保存消息并记录调用用量；但其“一次动作”是一段代码，单个代码块可以包含多个 API 调用和控制流，`ignore_multiple_calls` 只处理多个代码块。Brief 尚未给出能核验“不引入新流程”的字段级动作定义，因此不能先把该限制视为已经保证。

同一 checkpoint 的配对设计合理，但 [`save_state/load_state`](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/environment.py) 保存和加载的是数据库状态，没有保存 agent 消息或完整 Python 执行命名空间；仅调用这两个入口不足以证明分支拥有相同前动作状态。测试集只取 aggregate 的安排符合[官方限制](https://github.com/StonyBrookNLP/appworld#-agent-development-restrictions)。

成本核算方向正确；剩余预算如何用于 actor、建库与归因费用按什么任务规模分摊，尚未形成确定协议。模型、k、粒度和非劣界留待用户确认符合约束。ASSAY 原文给出作者仓库链接，但本轮访问失败，未核验其可运行性；Brief 的独立屏蔽定义可作为自定义基线，不能据此视为官方 ASSAY 已复现。[ASSAY §2](https://arxiv.org/html/2606.15390#S2)

## 最高近邻

1. **[Sentry: Learning to Recover from LLM Agent Failures at Test Time](https://arxiv.org/html/2610.02994v1)**  
   已核验 §3.1–3.3、附录A.6/A.8。同任务包括 AppWorld；检查当前动作与近期轨迹，不干预时继续执行，必要时提供外部经验。当前差别是非空修复被限制为经验指定字段。作者[仓库](https://github.com/nuglifeleoji/Sentry)本轮可见根目录只有说明与 assets，未见 README 所述可运行源码；不能忽略原作，也不能宣称官方复现入口已可用。

2. **[REINS: Model-Free, Certifying Least-Cost Repair of LLM-Agent Tool-Call Trajectories](https://github.com/AnwarDebes/reins)**  
   已核验 README 与 `reinskit/shield.py`。已具有动作恒等域、可实施编辑和最小干预。差别是声明策略与预设编辑能力，而当前方案用经验与冻结 LLM 决定 δ；其合成安全轨迹不能冒充 AppWorld 经验迁移 baseline。

3. **[Verify Before You Commit: Towards Faithful Reasoning in LLM Agents via Self-Auditing](https://aclanthology.org/2026.acl-long.1440.pdf)**  
   已核验 §3.5、附录A.2与修复提示。结构化定位失败切片、约束局部修复、保留未受影响部分，已覆盖编辑足迹的主要思想。对象是推理与知识问答，不是当前工具 call 的经验迁移；不能当同任务 baseline。

4. **[Recursive Experiential–Working Memory Evolution for Long-Horizon Agent Harnesses](https://arxiv.org/html/2608.24876)**  
   已核验 §2.2.2。草拟 state-changing call 后截住执行，以合成未执行结果加入技能，再让 actor 生成动作。当前确有明确差别：空 δ 直接执行原动作，非空 δ 限制字段，而不是提供技能后自由重草拟。

5. **[When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents](https://arxiv.org/html/2608.22339)**  
   已核验 §4及 AppWorld 实验。技能带适用条件、避免规则和恢复提示；局部失败后提供针对性提示替代完整重检索。差别是当前方案在执行前处理默认动作，并约束修改足迹；原作未提供这一完整算子。本轮未核验到可运行作者代码。

```json
{
  "score": 7.2,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "默认动作透传与不暴露恢复经验已被同任务Sentry覆盖，局部编辑和保持未受影响部分也有REINS及SAVeR先例。尚未找到完整覆盖自动经验决定当前call字段编辑足迹的同任务原作，保留窄机制差别；但当前最小实验缺少已有透传加必要修复的强对照，且AppWorld代码动作的编辑边界未定义，独立新意与收益尚未充分建立。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Sentry: Learning to Recover from LLM Agent Failures at Test Time",
      "url": "https://arxiv.org/html/2610.02994v1",
      "overlap": "检查当前动作和近期轨迹；无失败时无干预、无经验检索并继续执行，必要时提供外部playbook修复经验；包含AppWorld同任务实验。",
      "difference": "当前方案将非空修复限制在经验指定的当前call字段，而Sentry软修复提供下一步指导，没有该字段编辑约束。",
      "verified": true
    },
    {
      "title": "REINS: Model-Free, Certifying Least-Cost Repair of LLM-Agent Tool-Call Trajectories",
      "url": "https://github.com/AnwarDebes/reins",
      "overlap": "对已生成工具动作进行可实施编辑，合规动作保持恒等，采用最小干预。",
      "difference": "REINS基于声明策略及预设编辑能力，不用跨任务经验和冻结LLM决定字段修正；合成安全轨迹不是AppWorld经验迁移同任务baseline。",
      "verified": true
    },
    {
      "title": "Verify Before You Commit: Towards Faithful Reasoning in LLM Agents via Self-Auditing",
      "url": "https://aclanthology.org/2026.acl-long.1440.pdf",
      "overlap": "结构化定位失败切片，将诊断转为修复约束，仅修改局部并保持未受影响部分稳定。",
      "difference": "原作处理推理信念与知识问答，不处理当前工具call的跨任务经验字段编辑，不能作为同任务baseline。",
      "verified": true
    },
    {
      "title": "Recursive Experiential–Working Memory Evolution for Long-Horizon Agent Harnesses",
      "url": "https://arxiv.org/html/2608.24876",
      "overlap": "草拟工具call后截住执行，在call-time向actor提供相关技能并重新生成动作。",
      "difference": "当前方案空修正时直接执行原动作，非空修正时限制字段编辑足迹；Recuris在技能进入上下文后重新草拟。",
      "verified": true
    },
    {
      "title": "When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents",
      "url": "https://arxiv.org/html/2608.22339",
      "overlap": "为经验增加适用边界、避免规则和针对性恢复提示；包含AppWorld局部修复与等长度机制对照。",
      "difference": "原作主要在条件化提示及执行失败后的恢复环节起作用，没有执行前默认动作恒等分支与字段足迹约束的完整组合。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "当前目标仍是LLM软件或知识工作agent的经验负迁移，聚焦Q004-D01/D03，原始经验暴露和过量程序证据支持这一演化。不覆盖永久淘汰和D02不构成偏题。方法只使用可见任务和工具证据，优先冻结模型，未运行实验或调用付费推理API，测试集只取aggregate。字段编辑定义、完整checkpoint状态和预算分摊协议仍是实验交接未定项，不视为已保证或已解决。"
  }
}
```