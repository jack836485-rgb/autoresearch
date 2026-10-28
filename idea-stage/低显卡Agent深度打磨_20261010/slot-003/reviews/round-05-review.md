## 结论

实际检索日期：**2026-10-10**。**score：7.1；verdict：promising_needs_revision**。未发现足以断言完全重复的同任务原作，但当前独立机制新意不足以超过通过阈值；没有已确认的 fatal blocker。

研究价值成立：**同一经验在同一公开任务类内，是否仅因预算变化而发生收益翻转**，比泛泛研究“记忆是否有用”更具体，也可被实验推翻。不过，完成成本 CDF、曲线交叉和全范围支配后的淘汰，已有直接原作；保留经验但条件暴露也已有 agent 方法。当前剩余贡献主要是这些原则在经验库上的具体适用性，尚不能据此认定新的独立机制。

目标演化成立，仍关联 Q004。聚焦预算条件导致的暴露／保留混淆，有 D03 的过量验证和重流程证据支持；不处理全部反馈误判或 D02 选择混杂可以接受。当前设计遵守冻结模型、离线使用评测标签、完整计费及本阶段不运行实验的硬约束。[D03 原作，§V-B](https://arxiv.org/html/2608.11888)

最小实验有可实现入口，但两个问题影响结论：**前缀状态正确是否等于 actor 已正确完成**尚未明确；现有对照也不足以区分“采用分布支配”与“给已有成功差屏蔽增加预算条件”。AppWorld 官方循环依据公开任务状态停止，正确性评分则独立检查数据库终态，两者不能直接混用。[执行循环](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/agent.py)、[评分入口](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/evaluator.py)

## Claim 判断

| Claim | 新颖性判断 | 最关键原文依据与可验证性 |
|---|---|---|
| 同一冻结 actor、同一公开状态类内，经验收益随预算翻转 | **部分重合，具体经验现象待验证** | Assay 已报告技能引入额外流程并耗尽 AppWorld 步数预算，但主要研究跨任务异质性；本次未找到直接验证同类任务、仅改变外部预算所产生翻转的原作。配对有／无经验轨迹可检验，不能预称交叉存在。[Assay §1、§2](https://arxiv.org/html/2606.15390) |
| 全预算范围被支配才判无保留收益；交叉则保留 | **数学规则已覆盖，agent 应用部分重合** | Gomes–Selman 明确定义累积完成频率的全范围支配，并展示短成本区间与长成本区间优势反转。Sentry 又明确指出，直接剪除经验会连同条件收益一起丢失。当前差别是预算条件下的经验保留对象。[Gomes–Selman §3–4](https://www.cs.cornell.edu/gomes/pdf/2013_gomes_corr_portfolio.pdf)、[Sentry §2](https://arxiv.org/html/2610.02994v1) |
| 按当前预算处的成功概率差决定暴露 | **部分重合** | LIMBO 已联合选择记忆模式与 token／round／tool 预算；Sentry 已将保留和条件暴露分开。当前区别是用冻结的预算完成曲线控制暴露，而非在线标量 bandit 或故障诊断。[LIMBO §III-C–D](https://arxiv.org/html/2609.14138)、[Sentry §3](https://arxiv.org/html/2610.02994v1) |
| 同策略长轨迹的前缀可复用，降低多预算估计成本 | **标准性质，不足以独立支撑机制新意** | 在策略及每次生成完全相同、仅外部停止位置不同的限定下，这是截断轨迹的直接性质。可以验证实现一致性；预算盲策略下的一致性本身不构成新研究发现。若前缀评分允许未终止状态，所得成功曲线也不必是完成成本 CDF。[AppWorld 状态评分实现](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/evaluator.py) |
| 能避免误删高预算有益经验并减少低预算负迁移 | **可证伪，但尚不充分区分近邻** | 曲线交叉、冻结后泛化以及开发费用抵消收益，都是有效反证。可是跨预算成功差屏蔽同样可以得到 (F_e(b)-F_0(b))；仅击败一档屏蔽或带固定费用权重的 LinUCB，不能证明收益来自支配保留机制。Assay 的同任务遮蔽定义可据原文复现；论文宣称的官方仓库本次访问返回 404，未核验官方代码。[Assay §2.1–2.3](https://arxiv.org/html/2606.15390)、[声明的代码链接](https://github.com/aiming-lab/assay) |

AppWorld 的 `save_state` 与离线 `evaluate_task` 为前缀快照评价提供了真实入口；无须恢复 Python 状态来继续反事实分支。明确标准定义的屏蔽基线和自定义 LinUCB 可实现，但后者应按适配对照理解，不能当作 LIMBO 官方复现。完整预算约束合理，尚未确定的模型、样本量和预算范围决定实际 API 支出，当前没有费用证据。[状态保存实现](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/environment.py)、[LIMBO 算法](https://arxiv.org/html/2609.14138)

## 最高近邻

1. **[Not All Skills Help: Measuring and Repairing Agent Knowledge — Assay](https://arxiv.org/html/2606.15390)**  
   已核验原文 §1、§2.1–2.3。同样使用冻结 actor、AppWorld 开发任务、有／无技能成功差、条件遮蔽及离线保留处理。当前差别是同一任务类中的预算异质性和全预算支配规则；原作主要处理跨任务异质性。官方代码链接已尝试访问，返回 404，代码未核验。

2. **[Algorithm Portfolio Design: Theory vs. Practice — Gomes & Selman，UAI 1997](https://www.cs.cornell.edu/gomes/pdf/2013_gomes_corr_portfolio.pdf)**  
   已核验原文 §3–4及[作者出版记录](https://www.cs.cornell.edu/annual_report/1997/selman.htm)。直接重合于完成成本累积分布、短预算／长预算优势交叉，以及全范围支配时选择优势策略。当前区别是把候选对象换为 LLM 经验暴露条件。它是机制来源，属于跨域近邻，不能充当 AppWorld 同任务 baseline。

3. **[LIMBO: Lifelong Inference-Time Memory and Budget Optimization for LLM Agents](https://arxiv.org/html/2609.14138)**  
   已核验 §III-C–D及预算 primitive 表。重合于冻结黑盒 actor、记忆 on/off／检索选择、联合预算和成本反馈。当前区别是离线固定策略的完成成本分布及保留偏序；LIMBO 使用在线两头 LinUCB 和标量准确率减费用目标。本次未核验官方代码。

4. **[Sentry: Learning to Recover from LLM Agent Failures at Test Time](https://arxiv.org/html/2610.02994v1)**  
   已核验 §2–3。原作明确区分剪除经验与保留后条件暴露，指出剪除会损失条件收益。当前区别是条件由预算完成曲线给出；Sentry 由实时故障诊断给出。它未提供当前的预算支配删除规则。

5. **[Forget to Improve: On-Device LLM-Agent Continual Learning via Budget-Curated Memory](https://arxiv.org/html/2606.25115)**  
   已核验 §III-B–C。重合于冻结 agent、经验价值／伤害估计和预算驱动 KEEP。当前区别是原作用净价值每字节统一评分，预算主要为内存与能耗；本方案使用执行费用范围上的完成概率偏序。其攻击、共享及设备部分与当前目标无关，不应引入同任务对照。

```json
{
  "score": 7.1,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "同一公开任务类内的经验预算收益翻转是具体且可证伪的待验证问题；完成成本CDF、交叉和全范围支配选择已有直接原作，保留与条件暴露分离也已有agent方法。当前独立机制贡献偏薄，最小实验尚不能区分分布支配机制与预算条件成功差屏蔽；前缀正确状态和正确终止事件的定义也未固定，因此未达到experiment_ready。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Not All Skills Help: Measuring and Repairing Agent Knowledge",
      "url": "https://arxiv.org/html/2606.15390",
      "overlap": "冻结actor、AppWorld开发集、随机技能遮蔽成功差、条件遮蔽、离线技能保留处理及额外流程耗尽步数预算",
      "difference": "当前研究同一任务类内的预算异质性、全预算支配保留及固定策略轨迹复用；Assay主要处理跨任务异质性。原文已核验，论文声明的官方仓库访问返回404，代码未核验。",
      "verified": true
    },
    {
      "title": "Algorithm Portfolio Design: Theory vs. Practice",
      "url": "https://www.cs.cornell.edu/gomes/pdf/2013_gomes_corr_portfolio.pdf",
      "overlap": "完成成本累积分布、短成本与长成本区间优势交叉、全范围分布支配后的策略选择",
      "difference": "原作研究随机组合搜索算法，本方案研究LLM经验暴露和保留；这是机制近邻，不是同任务baseline。",
      "verified": true
    },
    {
      "title": "LIMBO: Lifelong Inference-Time Memory and Budget Optimization for LLM Agents",
      "url": "https://arxiv.org/html/2609.14138",
      "overlap": "冻结黑盒actor、记忆模式与执行预算联合选择、成本反馈和LinUCB控制",
      "difference": "LIMBO在线优化准确率减费用标量并选择预算primitive；当前使用离线固定策略完成成本分布及保留偏序。原文已核验，官方代码未核验。",
      "verified": true
    },
    {
      "title": "Sentry: Learning to Recover from LLM Agent Failures at Test Time",
      "url": "https://arxiv.org/html/2610.02994v1",
      "overlap": "直接剪除经验会损失条件收益，保留经验并仅在适用状态暴露",
      "difference": "Sentry以实时故障诊断决定暴露并验证恢复；当前以预算完成曲线决定暴露和有限范围删除资格。",
      "verified": true
    },
    {
      "title": "Forget to Improve: On-Device LLM-Agent Continual Learning via Budget-Curated Memory",
      "url": "https://arxiv.org/html/2606.25115",
      "overlap": "冻结agent、经验价值与伤害估计、预算驱动保留淘汰",
      "difference": "原作使用净价值每字节统一评分及内存能耗预算；当前使用执行费用范围内的完成概率分布支配，排除攻击和共享目标。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "聚焦预算条件导致的经验适用性与保留混淆，仍属Q004；D03原作对过量验证和重流程的观察支持这一聚焦。当前明确不普遍解决D02选择混杂，也不声称未知未来任务下最优淘汰，这种范围收缩成立。运行时仅查询可见任务和费用、评测标签仅离线使用、冻结执行模型并计入完整费用，未发现已发生的硬约束违规。前缀正确状态与actor正确终止的事件定义未固定，属于当前Claim和实验解释的未决问题。无实测结果，尚不能称解决。"
  }
}
```