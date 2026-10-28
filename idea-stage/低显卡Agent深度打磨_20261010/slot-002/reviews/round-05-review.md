## 结论

实际检索日期：**2026-10-10**。**score：6.9 / 10；verdict：needs_rethink。**

研究问题有价值，当前方案也具备可实施的最小实验入口，但独立机制新意不足。表达式内部传播 static/dynamic、提前求值固定子树、保留残余程序，均属于经典部分求值；以用户回答逐步 specialize 对话程序也已有直接先例。当前剩余差别主要是把用户明确的时间语义映射为历史输入和动作时输入，尚未形成超出既有分阶段求值的机制贡献。[部分求值原书 §1.1、§5.2、§15.5](https://www.researchgate.net/profile/Peter-Sestoft/publication/213882771_Partial_Evaluation_and_Automatic_Program_Generation/links/5704f27108ae13eb88b92a5f/Partial-Evaluation-and-Automatic-Program-Generation.pdf)、[早期对话 staging §2–3](https://people.cs.vt.edu/naren/papers/vt-staging.pdf)。

另一个核心阻断是实验归因：在相同 IR、标签、历史输入和实时读数下，正确的部分求值与完整 CPU 求值应返回相同集合。其差别可以是计算、存储或上下文成本；相对“交给 LLM 解读完整树”的正确性收益，则同时引入了确定性执行这一变化，不能单独归因于 specialization。上述等价性是依据部分求值语义作出的推论，并非实测结果。

目标演化成立。它仍关联 Q002 的澄清后约束整合和 Q003 的静默执行错误；聚焦混合时间语义属于合理的可测试假设。不过，[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)和[TRACE §7](https://arxiv.org/html/2608.06503v1)并未证明这种混合是已观察错误的主导原因。方案满足所给硬约束，未覆盖全部初始 drawbacks 不构成拒绝理由。

## Claim 判断

| 当前 Claim／组成 | 判断 | 最关键原文依据及可验证性 |
|---|---|---|
| 将指令、澄清和已选实体转为可执行结构，保存绑定 | 部分重合 | [Dataflow §2–5](https://arxiv.org/html/2009.11423v3)已有自然语言到程序、计算结果引用、局部 revision 和澄清修复；[STITCH §2.2](https://arxiv.org/html/2601.10702v1)已有结构引导的指代消解。冻结 LLM 与有限 AppWorld IR 是具体实现差别，可测抽取和绑定错误。 |
| 同一表达式内部保留不同绑定时刻 | 部分重合 | 用户时间语义是当前任务差别；表达式级绑定时刻传播和部分 static 结构已经由原书 §5.2、§15.5 覆盖。可验证语义标注与执行集合，但不能把细粒度传播本身申报为新。 |
| 最大固定子树物化为 ID 集合，动态部分保留残余程序 | 已覆盖 | 原书 §1.1 的 specialization 正是计算仅依赖已知输入的部分，生成依赖剩余输入的程序；§5.2 已给出沿表达式组合传播的规则。ID 集合是此处的值类型。 |
| 按澄清回答 specialize，避免继续重解释已经确认的部分 | 部分重合 | [Staging §2、Fig.3、§3.1](https://people.cs.vt.edu/naren/papers/vt-staging.pdf)已经用收到的用户输入变换并简化对话脚本，也支持嵌套澄清。保留实时 API 条件是当前差别，尚未提供新的变换原则。 |
| 压缩后减少合法错成员，并有同总预算净收益 | 新的应用假设，尚无支持 | [FOCUS §4、A.10](https://arxiv.org/pdf/2609.37590)已在 AppWorld 分析集合成员被静默遗漏，并用依赖引用与遗漏补救保留历史。当前混合时间条件没有被其直接覆盖；离线终态可证伪，但正确性提升须与确定性 IR 执行、时间标签和压缩分别归因。 |
| 同 IR 不 specialize 的 CPU 重算对照能证明机制优势 | 当前归因不成立 | 对纯集合表达式，同输入下 `Eval(PE(E,H),L) = Eval(E,H,L)`。集合结果相同是正确性的预期，不能同时作为推翻语义机制的异常；成本收益仍可测，但当前未说明有限树重算中哪项主导成本会被消除。 |

工程可行性得到支持：[AppWorld 指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)提供 setup、solution 和起止状态差分 evaluation；[TRACE runner](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/collect/runner.py)提供确定性前缀重放与小型 adapter 接口。[TRACE 的复现说明](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/docs/REPRODUCIBILITY.md)明确原研究 harness 未分发，新 rollout 是新 cohort；Brief 对此表述正确。FOCUS 原文给出算法、依赖引用格式、补救提示和超参数，可作同任务重实现，但本次未核验到公开作者代码。

完整成本核算与核心预算对齐已有明确承诺；模型、语法、样本数及预算尚未确定，因此目前只能判断协议可对齐，不能判断净收益。

## 最高近邻

1. **[Partial Evaluation and Automatic Program Generation（1993）](https://www.researchgate.net/profile/Peter-Sestoft/publication/213882771_Partial_Evaluation_and_Automatic_Program_Generation/links/5704f27108ae13eb88b92a5f/Partial-Evaluation-and-Automatic-Program-Generation.pdf)**  
   已核验原书 §1.1、§5.2、§15.5。覆盖已知／未知输入划分、表达式级传播、静态计算与残余程序。当前差别是由 agent 指令和问答确定输入阶段；原书没有 AppWorld 澄清与压缩实验。

2. **[The Staging Transformation Approach to Mixing Initiative（2003）](https://people.cs.vt.edu/naren/papers/vt-staging.pdf)**  
   已核验作者全文 §2–3。用户回答驱动部分求值，保留剩余脚本，支持嵌套澄清和多层结构。当前差别是历史对象与实时 API 字段的混合求值；该原作以预先设计的对话脚本为主，§3.1 还明确将部分状态维护置于 staging 之外。

3. **[Task-Oriented Dialogue as Dataflow Synthesis（2020）](https://arxiv.org/html/2009.11423v3)**  
   已核验 §2–5。覆盖可执行意图、计算与结果同时保存、历史实体引用、局部修订及澄清绑定。当前增加时间语义划分和压缩时 specialization；原作没有这一压缩协议。同任务 baseline 不能直接采用其 SMCalFlow 成绩。

4. **[Grounding Agent Memory in Contextual Intent／STITCH（2026）](https://arxiv.org/html/2601.10702v1)**  
   已核验 §2.2–2.3 与附录提示。覆盖按目标范围组织记忆、消解指代和筛选上下文匹配的历史。当前保留的是可执行残余选择程序；STITCH 的主要机制是记忆构建与检索，没有内部实时依赖求值。

5. **[FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents（2026）](https://arxiv.org/pdf/2609.37590)**  
   已核验 §4、A.9、A.10。与当前同属 AppWorld 历史压缩，已有集合成员静默遗漏案例、计划依赖引用和未引用 span 补救。当前差别是编译显式混合时间语义；FOCUS 保留原始 spans，不生成分阶段选择程序。

```json
{
  "score": 6.9,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "当前核心变换仍是经典部分求值的直接应用；表达式级绑定时刻传播、固定子树求值、残余程序，以及以用户回答specialize对话均有原始先例。剩余差别主要是新的输入时间语义和任务条件，尚不足以建立独立机制贡献。",
    "核心实验归因存在结构性问题：同IR、同标签、同历史输入和实时读数下，正确的部分求值与完整CPU求值应产生相同集合。相对LLM解读完整树的正确性收益不能单独归因于specialization，而当前把CPU重算结果相同列为机制推翻条件。"
  ],
  "novelty_conclusion": "混合历史对象与动作时条件是有研究价值的agent应用假设，检索未发现完全覆盖其AppWorld压缩设置的原作；但当前算法与经典分阶段求值及早期对话staging高度重合，独立机制创新尚未成立。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Partial Evaluation and Automatic Program Generation",
      "url": "https://www.researchgate.net/profile/Peter-Sestoft/publication/213882771_Partial_Evaluation_and_Automatic_Program_Generation/links/5704f27108ae13eb88b92a5f/Partial-Evaluation-and-Automatic-Program-Generation.pdf",
      "overlap": "已知与未知输入划分、表达式级binding-time传播、部分static结构、提前计算与残余程序。",
      "difference": "当前从明确agent指令和问答确定历史及动作时输入；原书没有该AppWorld压缩设置。",
      "verified": true
    },
    {
      "title": "The Staging Transformation Approach to Mixing Initiative",
      "url": "https://people.cs.vt.edu/naren/papers/vt-staging.pdf",
      "overlap": "根据收到的用户回答对结构化对话脚本部分求值，保留剩余脚本，并处理嵌套澄清。",
      "difference": "当前针对历史选定对象与实时API字段；原作主要使用预先设计脚本，部分状态维护在staging之外。",
      "verified": true
    },
    {
      "title": "Task-Oriented Dialogue as Dataflow Synthesis",
      "url": "https://arxiv.org/html/2009.11423v3",
      "overlap": "自然语言到可执行程序、保存计算和结果、历史实体引用、局部revision及澄清修复。",
      "difference": "当前增加显式时间输入划分及压缩时specialization；不能用其原任务成绩充当AppWorld对照。",
      "verified": true
    },
    {
      "title": "Grounding Agent Memory in Contextual Intent",
      "url": "https://arxiv.org/html/2601.10702v1",
      "overlap": "目标范围组织、结构引导指代消解、上下文匹配的历史筛选。",
      "difference": "当前使用可执行残余选择程序；STITCH主要构建和检索记忆，不执行内部实时依赖。",
      "verified": true
    },
    {
      "title": "FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents",
      "url": "https://arxiv.org/pdf/2609.37590",
      "overlap": "AppWorld压缩后的集合成员静默遗漏、历史依赖引用及遗漏span补救。",
      "difference": "当前编译显式混合时间语义；FOCUS保留原始spans，不生成分阶段选择程序。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "当前目标仍关联Q002的澄清后绑定和约束整合，以及Q003的压缩后静默执行错误。Dataflow和部分求值原作支持表示与执行依据；混合时间语义属于可测试的进一步聚焦，初始来源尚未证明其频率或主导因果。方案使用可见指令、正常API和冻结模型，不要求隐藏标签、金标准程序、训练大模型或本阶段实验；未覆盖全部drawbacks不构成违规。"
  }
}
```