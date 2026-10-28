## 结论

实际检索日期：**2026-10-10**。**score：7.2 / 10；verdict：promising_needs_revision；无 fatal blocker，未达到通过阈值。**

当前方案保留了一个有研究价值的假设：冻结 API agent 的压缩目标能否从“预测什么动作”转向“保存可见证据对联合动作候选的区分”。但**保留完整属性诱导的等价分区、按新增区分对数贪心选择证据，均已有直接算法先例**，不能作为新的分区约简机制。独立新意目前限于将该目标用于实际来源、澄清问答和工具调用压缩；尚未找到同任务原作完全覆盖这一实例化假设。

最小实验能够检验联合信息相对参数边际、随机来源和最近问答的作用，但尚不能区分与 FOCUS、TRACE 的同任务增益，也没有直接检验核心 Claim 中“保留最高可能动作”的比较项。因此，当前不足以判断部署价值。

目标演化成立。[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)明确记录正确回答后的旧要求遗忘和问答错绑；[TRACE §7](https://arxiv.org/html/2608.06503v1)明确承认可能漏掉静默状态错误。聚焦当前可见来源与联合候选，仍属于 Q002/Q003；未覆盖全部更新使用失败不构成偏题。方法不要求隐藏标签、正确教师或终态 oracle，符合冻结模型、低本地显卡占用和正常协作场景约束。所有效果仍是待验证假设。

## Claim 判断

| Claim | 判断与关键原文依据 | 可验证性 |
|---|---|---|
| 有限结构化工具候选用于表达参数不确定性 | **已覆盖。**[SAGE §3.1–3.3](https://arxiv.org/html/2511.08798v1)已有结构化工具候选、可行性 belief 和回答后的约束传播；§3.2明确采用参数独立近似。 | 可检验候选覆盖和签名错误，但候选表示本身不是新贡献。 |
| 选取少量来源，保留全部来源诱导的候选等价分区 | **算法目标已覆盖。**[属性约简原作](https://www2.cs.uregina.ca/~yyao/PAPERS/is_complementary.pdf)以属性子集保存原有不可区分关系；候选对应对象、来源三值签名对应多值属性，即形成同一约简问题。[Test Cover §2](https://pure.tue.nl/ws/files/2021610/559540.pdf)已有按尚未区分的对象对贪心选测试。 | 分区保留可直接计算。它不能单独证明执行信息充分：签名“支持/排除”和“支持/未知”都区分同一候选对，却只有前者排除了错误候选。贪心可能保留后者并丢掉前者。 |
| 联合候选区分比独立参数边际更能保留问答绑定 | **部分重合。**SAGE 的独立近似提供明确差别；[KBRA §8.2](https://arxiv.org/html/2606.21732v1)已检查单段来源对完整联合绑定的支持。当前区别是选取来源保存候选分区，而非绑定成员检查和安全拒绝。 | 同边际、不同联合 tuple 加无关联对照具有判别力。但边际对照的失败并不自动证明分区目标优于完整关系表示。 |
| 以实际来源的区分关系压缩，比预测动作及未来引用效用更好 | **部分重合，具体 agent 假设尚有新意。**[FOCUS §3–4](https://arxiv.org/html/2609.37590v1)已提出保存决策相关历史，并以计划采样、来源引用及遗漏来源补救实现压缩。当前不依赖原 actor 决策正确，目标也不是未来轨迹分布。 | 可以证伪；当前对照尚未直接区分 FOCUS 或最高可能动作保留。 |
| 不执行候选、不生成环境、无正确概念教师也能选择区分证据 | **与近邻存在实质差别。**[DPC §2.3–3.4](https://aclanthology.org/2026.acl-long.313.pdf)构造区分数据库并执行 SQL，以 Python 结果作为代理真值；本方案选择已到达证据，不定候选真值。DPC 属于跨域近邻，不能充当 AppWorld 同任务 baseline。 | 运行约束清楚，但不提供动作正确性保证。 |
| 减少合法错实体、错绑并在完整成本下有部署价值 | **待验证。**TRACE 的局限支持问题存在研究空间，未证明本方案有效。 | 无 gold 筛选的自然候选、最终绑定正确率和 TGC 可以证伪；完整成本计入原则正确。现有简单基线可实现，但尚不足以判断相对最接近同任务方法的优势。 |

已核验 [AppWorld 作者实现](https://github.com/stonybrooknlp/appworld)中的 `load_task_ids`、`world.execute` 和 `world.evaluate`，公开 CPU 环境入口成立。TRACE 的[公开仓库](https://github.com/nokia-applied-research/Trace)提供优化后的压缩策略、模板及 AppWorld 续跑入口，具有具体复现路径。FOCUS 原文算法已核验，本次未找到作者代码；这不影响其作为最高近邻的地位。

## 最高近邻

1. **[Data Analysis Based on Discernibility and Indiscernibility（2007）](https://www2.cs.uregina.ca/~yyao/PAPERS/is_complementary.pdf)**  
   已读作者原文。属性约简保存完整属性集诱导的区分／不可区分关系，与当前分区目标直接对应；不要求已知正确概念。差别在于当前属性由自然语言来源对工具候选的支持状态抽取得到，最后交给冻结 actor 使用。

2. **[Approximation Algorithms for the Test Cover Problem（2003）](https://pure.tue.nl/ws/files/2021610/559540.pdf)**  
   已读原文技术报告，出版记录由 [CWI](https://ir.cwi.nl/pub/18037/)核验。§2将对象对作为集合覆盖元素，贪心选择区分最多未覆盖对的测试。当前的 token 成本加权和三值签名属于该形式的扩展应用；agent 的来源抽取与执行效果未被它覆盖。

3. **[FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents（2026）](https://arxiv.org/html/2609.37590v1)**  
   已读方法与 AppWorld 实验。共同点是冻结 agent、测试时选择完整历史片段和保存决策相关信息。FOCUS 按多个未来计划的引用频率及补救判断保留来源；当前按实际来源对有限联合调用的区分选择，不预测未来观察。

4. **[Structured Uncertainty guided Clarification for LLM Agents／SAGE（2025）](https://arxiv.org/html/2511.08798v1)**  
   已读 §3.1–3.5。共同点是结构化工具候选、回答约束、成本和不确定状态；参数独立近似已明确核验。差别是 SAGE 选择新的澄清问题，当前在得到实际回答后压缩已有证据并保留联合候选区分。

5. **[Toward Reliable Context Compression for Long-Horizon Agents／TRACE（2026）](https://arxiv.org/html/2608.06503v1)**  
   已读原文并核验[实现仓库](https://github.com/nokia-applied-research/Trace)。共同点是冻结 AppWorld agent 和压缩边界后的执行评价。TRACE 用 blocked/refetch 的配对续跑反馈优化压缩提示，当前直接选择区分证据，并以合法错实体和最终正确率检验其价值。

```json
{
  "score": 7.2,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "保存完整来源签名诱导分区的目标与粗糙集属性约简直接对应，未区分候选对的贪心选择已有 Test Cover 先例，算法层不能声称独立创新。将该目标用于实际澄清来源和冻结 API 工具 agent 的压缩尚有独立研究假设，未找到同任务完全覆盖；但分区保留不等于可行性或执行正确性保留，当前最小实验尚不能区分 FOCUS、TRACE 和最高可能动作保留的增益，未达到 experiment_ready 阈值。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Data Analysis Based on Discernibility and Indiscernibility",
      "url": "https://www2.cs.uregina.ca/~yyao/PAPERS/is_complementary.pdf",
      "overlap": "以属性子集保留完整属性诱导的区分和不可区分关系；候选作为对象、来源签名作为多值属性时，与当前分区目标直接对应。",
      "difference": "当前在自然语言来源与工具调用之间抽取签名，选择逐字证据供冻结 actor 执行；原作研究一般信息表属性约简。",
      "verified": true
    },
    {
      "title": "Approximation Algorithms for the Test Cover Problem",
      "url": "https://pure.tue.nl/ws/files/2021610/559540.pdf",
      "overlap": "将对象对作为集合覆盖元素，并贪心选择区分最多未覆盖对象对的测试。",
      "difference": "当前应用三值来源签名与 token 成本，评价工具 agent 的实际动作；原作是一般测试覆盖问题。",
      "verified": true
    },
    {
      "title": "FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents",
      "url": "https://arxiv.org/html/2609.37590v1",
      "overlap": "测试时为冻结 agent 选择完整历史片段，保存决策相关信息，且已在 AppWorld 评价。",
      "difference": "FOCUS 依据未来计划采样的来源引用及遗漏来源补救；当前依据实际来源对有限联合调用的区分关系，不预测未来观察。原文已核验，本次未找到作者代码。",
      "verified": true
    },
    {
      "title": "Structured Uncertainty guided Clarification for LLM Agents",
      "url": "https://arxiv.org/html/2511.08798v1",
      "overlap": "结构化工具候选、参数可行域、回答后的约束传播及成本敏感的不确定性处理。",
      "difference": "SAGE 采用参数独立近似并选择澄清问题；当前在实际回答到达后选择来源，保存联合候选的来源区分关系。",
      "verified": true
    },
    {
      "title": "Toward Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability",
      "url": "https://arxiv.org/html/2608.06503v1",
      "overlap": "冻结 AppWorld agent，研究压缩边界后的执行退化；公开实现包含策略优化、压缩模板和续跑入口。",
      "difference": "TRACE 以 blocked/refetch 配对续跑反馈优化压缩提示；当前直接选择区分证据，并评价合法错实体与最终正确率。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "AppWorld-UL §6.7 的正确回答后旧要求遗忘和问答错绑，以及 TRACE §7 对静默状态错误的明确局限，支持聚焦当前可见来源和联合动作候选。仍关联 Q002/Q003，不要求覆盖全部初始不足；当前没有解决所有更新使用失败的证据。运行时仅使用已见指令、完整问答和观察，不需要隐藏标签、金标准 DAG、用户隐藏知识或终态 oracle；冻结模型、低本地显卡占用和正常协作范围成立。完整成本原则已列明，核心参数留待用户确认。本次仅联网审查，未运行实验、调用付费推理 API 或生成实验代码。"
  }
}
```