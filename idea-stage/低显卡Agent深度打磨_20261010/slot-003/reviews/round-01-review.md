## 结论

检索日期：**2026-10-10**。**score：7.2 / 10；verdict：promising_needs_revision；无已确认 fatal blocker。**

未发现原作完整覆盖“相对无经验计划识别缺失内容，只暴露条件编辑”的组合。它有研究价值：检验经验是否应补充 actor 的具体缺口，而非重复其已有意图。但独立新意较窄——成对轨迹生成条件建议、状态化暴露、最小计划修改及无修改返回，分别已有原作覆盖。当前不能仅凭编辑格式认定独立机制创新。

最小实验能够检验成功率与完整成本，却尚不足以排除“普通条件化局部建议”及“注入内容更短”的解释；“只删除重复文本”不控制全部长度差异。“P0 已写出要求”也不等于执行时会正确落实，覆盖判定及其与实际工具动作的对应仍不明确。

目标演化成立。聚焦 Q004-D03 的成本负迁移有原文依据：67 次过量验证、30 次重流程的分母确为182个效率回归；不处理永久淘汰与 judge 噪声可以接受。当前仍属于经验适用性问题，冻结 actor、低本地显卡占用与运行时不读取评测 oracle 等硬约束得到保留。收益全部属于待验证预期。[SkillTriage §V-B](https://arxiv.org/html/2608.11888)

## Claim 判断

| 当前 Claim／机制 | 判断 | 最关键原文依据与可验证性 |
|---|---|---|
| 技能相关性不代表需要整套注入 | 已覆盖 | SkillsInjector 已区分语义相关与执行收益，并联合选择、预算和呈现；此动机不能作为新贡献。[§3–4](https://arxiv.org/html/2605.29794) |
| 从成对轨迹提取带条件的局部纠错经验 | 已覆盖 | AutoGuide 已对比轨迹分歧，提取条件化建议并按当前上下文选择；CHEF 更早已有失败模式索引的具体计划修复。后者是跨域机制先例，不能作为 AppWorld 同任务 baseline。[AutoGuide §3](https://arxiv.org/html/2403.08978)、[CHEF 原文](https://www.ijcai.org/Proceedings/87-1/Papers/021.pdf) |
| 根据 P0 已覆盖／缺失内容输出空编辑或必要编辑 | 部分重合，保留窄的新颖边界 | Recuris 在草拟动作后注入技能再重草拟；SPIN 根据当前计划和问题进行最小修改，无需修复时保持原计划。两者没有完整覆盖“P0 相对经验的边际暴露”。该差别可测，但目前的条件、覆盖与编辑规则尚不足以确认它超出已有条件建议的局部实现。[Recuris §2.2.2](https://arxiv.org/html/2608.24876)、[SPIN 附录E.5](https://arxiv.org/html/2605.14051) |
| 减少重复检查／程序重启，同时保留缺失动作收益 | 可证伪，尚无支持结果 | 已覆盖与未覆盖分组、成功率、完整费用和实际动作记录方向正确。但自然分组结果不能单独区分计划覆盖作用、任务难度及短内容作用；已有成本改写也说明短提示与下游行为并非同一变量。[成本改写 §4／附录B](https://arxiv.org/html/2606.09421) |

AppWorld 的实现入口属实：环境提供执行与状态保存，简化 ReAct agent 返回 usage，执行循环累计费用并检查预算。这支持基础无经验、固定检索及限定机制对照的实现；不意味着已有官方 AppWorld 版 Recuris／SkillsInjector。Brief 对限定复现的措辞正确，完整成本核算和待确认核心参数也符合约束。[environment.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/environment.py)、[react_code_agent.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py)、[agent.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/agent.py)

另有一个实际实验协议冲突：AppWorld 官方 test 集禁止逐任务错误分析，当前“test 编辑错误率的离线人工／结果复核”与该规定不一致。它不违反用户允许离线评估的硬约束，但当前测试协议尚未成立。[AppWorld 官方评测说明](https://github.com/StonyBrookNLP/appworld#evaluation)

## 最高近邻

1. **[AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents](https://arxiv.org/html/2403.08978)**，2024，已核验。成对轨迹、条件化局部建议、当前上下文选择及空暴露高度重合。差别是当前方案显式把无经验计划的缺失／已覆盖作为暴露依据；AutoGuide 未定义该计划差分算子。

2. **[Recursive Experiential–Working Memory Evolution for Long-Horizon Agent Harnesses](https://arxiv.org/html/2608.24876)**，2026，已核验。状态引导技能调用及草拟动作后的干预重合。原作仍注入技能后重新草拟，当前方案拟暴露相对 P0 的必要编辑；计划意图与原作经过观察验证的完成状态也不同。官方代码公开，但未核实存在 AppWorld 端口。

3. **[SPIN: Structural LLM Planning via Iterative Navigation for Industrial Tasks](https://arxiv.org/html/2605.14051)**，2026，已核验。当前计划审查、避免冗余步骤、最小修改及无需修改时返回原计划重合。原作利用 DAG 校验、模拟和前缀控制；当前方案使用跨任务经验条目控制注入内容。它属于相近的工具工作任务，不能因工业场景而忽略。

4. **[SkillsInjector: Dynamic Skill Context Construction for LLM Agents](https://arxiv.org/html/2605.29794)**，2026，已核验。冻结执行模型、执行收益导向的选择、允许不注入和动态呈现重合。其 renderer 依据任务与共同注入技能改写描述，技能正文保持不变，不读取 P0 的覆盖情况。原文仍称代码将在发表时发布；不能把 API 替代实现称为完整复现。

5. **[What Should a Skill Remember? Quality-Cost Trade-offs in Cost-Aware Skill Rewriting for Language Model Agents](https://arxiv.org/html/2606.09421)**，2026，已核验。成本负迁移、保护必要信息及任务条件化改写重合。原作选择预定义保护策略并复用冻结改写，未根据每次 actor 的 P0 删除零边际内容；当前差别不是一般压缩或锚点保护。

```json
{
  "score": 7.2,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "未发现完整覆盖P0相对必要编辑暴露的原作，但成对轨迹条件建议、状态化暴露、最小修复和无修改返回已有先例。剩余新意较窄；当前最小实验不能充分区分计划边际暴露、普通条件建议与短内容作用，因此尚未实验就绪。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents",
      "url": "https://arxiv.org/html/2403.08978",
      "overlap": "成对轨迹提取条件化局部建议，依据当前上下文选择或不暴露建议",
      "difference": "未显式定义相对无经验计划已覆盖或缺失内容的编辑暴露算子",
      "verified": true
    },
    {
      "title": "Recursive Experiential–Working Memory Evolution for Long-Horizon Agent Harnesses",
      "url": "https://arxiv.org/html/2608.24876",
      "overlap": "状态引导技能调用，在草拟动作后注入技能并重新草拟",
      "difference": "原作暴露技能并依据验证进度调用；当前拟只暴露相对P0的必要编辑",
      "verified": true
    },
    {
      "title": "SPIN: Structural LLM Planning via Iterative Navigation for Industrial Tasks",
      "url": "https://arxiv.org/html/2605.14051",
      "overlap": "审查当前计划，避免冗余步骤，只作最小修改，无问题时保持原计划",
      "difference": "原作使用DAG校验、模拟与前缀控制；当前使用跨任务经验条目决定边际内容暴露",
      "verified": true
    },
    {
      "title": "SkillsInjector: Dynamic Skill Context Construction for LLM Agents",
      "url": "https://arxiv.org/html/2605.29794",
      "overlap": "冻结执行模型，基于执行收益选择技能，允许不注入并动态调整呈现",
      "difference": "依据任务及共同注入技能调整描述，正文不变，不读取P0覆盖情况",
      "verified": true
    },
    {
      "title": "What Should a Skill Remember? Quality-Cost Trade-offs in Cost-Aware Skill Rewriting for Language Model Agents",
      "url": "https://arxiv.org/html/2606.09421",
      "overlap": "通过条件化技能改写保护必要信息并降低完整执行成本",
      "difference": "选择预定义保护策略并复用冻结改写，不依据当前actor计划输出零边际空编辑",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "聚焦Q004-D03的成本负迁移有SkillTriage原文支持，仍研究经验适用性，放弃永久淘汰与judge噪声有明确边界。方法维持冻结actor、低本地显卡占用和运行时无评测oracle；未执行实验、未调用付费推理API、未生成代码。预算规定正确，核心参数留待确认。AppWorld官方test集禁止逐任务错误分析，与拟议test编辑错误人工复核存在实验协议冲突，但不构成用户硬约束违规。"
  }
}
```