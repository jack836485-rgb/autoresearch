## 结论

实际检索日期：**2026-10-10**。**score：6.9；verdict：needs_rethink。**

任务内重复提醒的成本负迁移值得研究，当前假设也可证伪。但**独立机制新意存在 fatal blocker**：同一历史制度下比较当次干预与不干预、允许过去干预持续影响状态、估计终末效应及既往暴露调节，均已属于 DCEE；其原作还明确分析连续干预负担。提示正文留在历史中，并不形成该框架之外的新识别机制。[DCEE §2.2、Examples 2–3](https://arxiv.org/html/2502.13500v2#S2.SS2)

当前目标演化成立：聚焦续发而不判断永久淘汰，仍关联 Q004 的局部适用性与 D03 的过量验证。原作确有技能诱发重复验证和成本回归的证据，但没有证明“再次追加同一技能”是其原因；本方案仍是待验证假设。[Agent Skills Can Be Harmful §V-B](https://arxiv.org/html/2608.11888v1#S5.SS2) 硬约束目前满足。

## Claim 判断

| 当前 Claim／机制 | 判断 | 关键依据与可验证性 |
|---|---|---|
| 首次有益的经验再次追加，可能增加验证而不改善终态 | **部分重合；具体假设尚未覆盖** | 技能导致过量验证已有实证；但既有历史相同条件下的“重复追加效应”尚未在已核验近邻中得到证明。开发期随机化可以检验。 |
| 用共同历史／后续制度识别当次追加的终末边际效应 | **已覆盖** | DCEE Eq.(2)正是仅改变当次决策、其余保持参考制度的终末对比；过去干预可影响后续变量。可估计，但不是新的识别机制。[§2.2](https://arxiv.org/html/2502.13500v2#S2.SS2) |
| 无洗脱、保留旧提示，使本方案不同于 MRT | **差别不足以支持新颖性** | DCEE不要求过去干预效果消失；既往干预可以作为 moderator。追加提示只是具体处理定义。 |
| 只有显式历史效应才能判断续发，当前 state 分层不能代替 | **必要性 Claim 不成立** | 在同一随机化设计下，仅以当前 state 为 moderator 也可估计合法的条件 DCEE；缺少历史变量可能遗漏异质性，并不自动破坏因果识别。Brief 未明确该对照是观察相关性还是随机效应估计。[§2.2](https://arxiv.org/html/2502.13500v2#S2.SS2) |
| 参考制度下的局部效应能指导更省钱的冻结续发规则 | **可验证，尚不受理论保证** | 局部 excursion effect 与整条部署策略价值不同；改变续发规则也会改变后续历史分布。原作明确区分 DCEE 与动态策略优化。测试可验证实际收益，不能由开发效应直接推出。[Remark 3](https://arxiv.org/html/2502.13500v2#S2.SS2) |

AppWorld 实现入口成立：[ReAct agent](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py) 可在生成前追加文本并记录 usage，[执行循环](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/agent.py) 提供工具反馈与预算停止。其 `task_completed()` 查询公开 supervisor 状态，并非隐藏成功评测。官方也明确允许 train/dev 分析、test 仅报告 aggregate。[环境代码](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/environment.py)、[使用限制](https://github.com/StonyBrookNLP/appworld#-agent-development-restrictions)

最小实验能够检验“重复追加是否有害”，但目前不能区分**新机制**与“将现成 DCEE 应用于提示续发”。特别是 state-only 对照的识别方式尚不明确。全链路预算原则正确；事件、样本量、参考制度和训练成本如何摊销仍未固定，尚不能判断统计辨别力与实际 API 成本。

## 最高近邻

1. **[Distal Causal Excursion Effects: Modeling Long-Term Effects of Time-Varying Treatments in Micro-Randomized Trials](https://arxiv.org/html/2502.13500v2)**  
   已核验正文、公式及附录。覆盖共同参考制度、历史依赖、连续干预负担与终末效应。当前差别主要是 LLM 提示追加及其经验假设；它是方法近邻，不能作为 AppWorld 同任务 baseline。更早的 [MRT/WCLS 原作](https://arxiv.org/abs/2004.10241) 也已定义居中加权估计。

2. **[Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval](https://arxiv.org/html/2610.02070v3)**  
   已核验 §2–3及跨查询分析。覆盖已知概率的记忆暴露、倾向加权及“局部效用不等于保留价值”。差别是当前研究任务内重复追加和终末成本；CMP主要评测记忆问答。论文列有代码链接，本次未核验其代码实现。

3. **[AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents](https://arxiv.org/html/2403.08978)**  
   已核验 Algorithm 2：每步从完整轨迹识别上下文、选择指南并生成动作。覆盖持续／重复指导行为；未估计重复追加的历史条件终末效应。原文算法可复现，AppWorld 适配未核验。

4. **[Recursive Experiential–Working Memory Evolution for Long-Horizon Agent Harnesses（Recuris）](https://arxiv.org/html/2608.24876)**  
   已核验 §2.2.2和[官方仓库](https://github.com/Gen-Verse/Recuris)。覆盖公开执行事件上的状态化技能调用。当前差别是随机化续发及效果估计。仓库支持 τ²-Bench、SkillFlow、Terminal-Bench；“Recuris式 AppWorld 检索”属于适配对照，不能冒充官方 AppWorld 实现。

5. **[Not All Skills Help: Measuring and Repairing Agent Knowledge（ASSAY）](https://arxiv.org/html/2606.15390)**  
   已核验 AppWorld 随机技能掩码、任务条件贡献预测及验证技能的收益翻转案例。覆盖同任务因果贡献屏蔽，差别是任务级技能包含与任务内重复追加。论文列出 [代码仓库](https://github.com/aiming-lab/assay)，本次仓库读取失败；因此不能确认代码可运行，也不能因 Brief 的 `code_url:null` 判定其无代码。

```json
{
  "score": 6.9,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "独立机制新意不足：共同历史制度下当次追加与不追加的终末对比、既往干预调节、持续历史影响和连续干预负担均由MRT/DCEE覆盖；当前方法差别主要是LLM提示处理定义及待验证的领域现象。"
  ],
  "novelty_conclusion": "重复追加有益经验是否诱发额外验证，是有价值且可证伪的经验问题；当前未形成超出现成DCEE应用的独立机制，无洗脱不能建立该创新边界。state-only对照定义及参考制度效果到部署策略价值的关系也尚未充分成立。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Distal Causal Excursion Effects: Modeling Long-Term Effects of Time-Varying Treatments in Micro-Randomized Trials",
      "url": "https://arxiv.org/html/2502.13500v2",
      "overlap": "共同参考制度下单次干预的终末效应、既往干预调节、持续历史影响及连续干预负担",
      "difference": "LLM任务内追加经验块及其成本负迁移假设；未给出新的识别机制",
      "verified": true
    },
    {
      "title": "Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval",
      "url": "https://arxiv.org/html/2610.02070v3",
      "overlap": "已知概率的记忆暴露、倾向加权和局部效用与保留价值的区分",
      "difference": "当前研究任务内重复追加及终末成功和成本，CMP主要研究记忆问答",
      "verified": true
    },
    {
      "title": "AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents",
      "url": "https://arxiv.org/html/2403.08978",
      "overlap": "每步依据轨迹上下文选择并呈现程序性指南",
      "difference": "没有识别重复追加的历史条件终末效应",
      "verified": true
    },
    {
      "title": "Recursive Experiential–Working Memory Evolution for Long-Horizon Agent Harnesses",
      "url": "https://arxiv.org/html/2608.24876",
      "overlap": "执行事件上的状态化技能调用和公开反馈状态更新",
      "difference": "当前增加随机续发和终末效应估计；AppWorld对照需适配",
      "verified": true
    },
    {
      "title": "Not All Skills Help: Measuring and Repairing Agent Knowledge",
      "url": "https://arxiv.org/html/2606.15390",
      "overlap": "AppWorld随机技能掩码、条件贡献预测及验证技能收益异质性",
      "difference": "任务级包含技能，而非既有历史下再次追加同一技能",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "聚焦任务内续发的适用性和成本负迁移，仍关联Q004与D03；技能诱发过量验证已有原文依据，重复追加是否为其原因尚待验证。不再声称处理永久淘汰，未覆盖D02不构成范围违规。冻结模型、公开状态、离线评估和完整成本要求均与硬约束一致。"
  }
}
```