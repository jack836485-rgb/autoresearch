## 结论

实际检索日期：**2026-10-10**。**score：6.9；verdict：needs_rethink**。当前问题有研究价值，目标、失败指标和完整成本约束也较清楚，但存在 **fatal novelty blocker：核心算子仍是已知约束冗余消除的直接实例化**。

把真实返回写成不可删除的条件约束 \(R_r\)，令 \(C=F\cup\{R_r\}\)，则删除判据就是 \(\operatorname{sol}(C\setminus\{f\})=\operatorname{sol}(C)\)。经典工作已经定义并研究了这一判据；有限域上的逐条贪心删除也已有原文依据。实际 API 返回改变输入实例，尚未形成独立的新机制。Brief 主动承认冗余消除不算新理论是准确的，但剩余“有限动作约束选择关系”目前没有超出该已知机制。[Carbonnel，§2–3](https://www.lirmm.fr/~ccarbonnel/papers/redundancy_v2.pdf)

最小实验可以验证这种应用是否有净收益，但静态分类、区别对覆盖和普通摘要不能区分它与**同一实际 \(r\) 下的经典约束删除**。保留子集之后再经过普通压缩器，集合等价证书也不会自动延伸到摘要内容或 actor 的实际选择；这些仍是可证伪假设。

目标演化成立：聚焦正确澄清后的历史约束、当前观察下的合法错实体，与 [AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)、[TRACE §7](https://arxiv.org/html/2608.06503v1)直接相关。没有必要覆盖全部初始 drawbacks；当前没有宣称解决 D02 的信息使用阶段。冻结 API 模型、CPU 枚举、oracle 仅离线评估及完整成本计入均符合硬约束。

## Claim 判断

| 当前 Claim | 判断 | 最关键依据与可验证性 |
|---|---|---|
| 约束是否可删除取决于实际观察与其余约束的联合关系 | **已覆盖** | 对 \(F\cup\{R_r\}\) 判断逻辑冗余正是该联合关系；[Carbonnel §2](https://www.lirmm.fr/~ccarbonnel/papers/redundancy_v2.pdf)直接以删除前后解集合是否变化定义冗余。可以验证，但不是新机制。 |
| 保持可行目标集合，比仅保持候选可区分关系更能保护排除关系 | **已覆盖** | [Dechter & Dechter §I–II](https://ftp.cs.ucla.edu/pub/stat_ser/r81-reprint.pdf)已讨论“某动作被禁止”由多条约束表达，以及删除后保持全部解。当前判据可检查，但区别对覆盖属于不同且较弱的目标。 |
| 以真实只读返回条件化，选择原文见证用于冻结黑盒 agent | **部分重合** | [Functional Compression §I–III](https://www.mit.edu/~medard/2010papers/funccomp.pdf)已覆盖侧信息条件下的函数保留；[FOCUS §4](https://arxiv.org/html/2609.37590v1)已在闭源 agent 上选择原文历史片段。真实返回替代预测规划有应用差别，未体现新的选择算子。 |
| 条件删除能在同完整预算下改善约束保留、合法错实体及终态成功 | **部分重合** | [FOCUS §A.10](https://arxiv.org/html/2609.37590v1)已报告实体枚举片段被删除后的静默遗漏。当前观察冗余／不可替代配对可以检验更具体的假设；尚无结果，不能称已解决。 |
| 最小实验有同任务实现入口并能对齐成本 | **部分重合** | [AppWorld 指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)支持 `_setup` 状态构造及预期／非预期终态评估；FOCUS §5、A.7、A.9给出 AppWorld 方法与参数入口，作者完整代码本次未核实。透明重实现可行，预算约束合理；主要阻断仍是无法区分经典同条件删除。 |

## 最高近邻

1. **[Removing Redundancies in Constraint Networks（1987）](https://ftp.cs.ucla.edu/pub/stat_ser/r81-reprint.pdf)**  
   已核验原文。删除约束而保持解集合，结合其余约束识别动作排除的冗余，是当前核心机制的直接近邻。差别是当前约束来自自然语言历史和实际 API 返回；原作不是 LLM agent 同任务 baseline。

2. **[On Redundancy in Constraint Satisfaction Problems（2022）](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2022.11)**  
   已核验原文 §2–3。有限 CSP 的解集合等价定义及贪心删除与当前 CPU 算子直接重合。差别在来源解析、原文片段输出及预算计费，不在删除关系。

3. **[FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents（2026）](https://arxiv.org/html/2609.37590v1)**  
   已核验 §4、§5、A.7、A.9、A.10。训练免费、闭源 API、原文片段选择、负约束保留及 AppWorld 实体遗漏均重合。当前使用真实观察下的符号可行集合，FOCUS 使用草稿规划依赖与防御性检查；这是最重要的同环境对照。完整作者代码未核实。

4. **[Functional Compression through Graph Coloring（2010）](https://www.mit.edu/~medard/2010papers/funccomp.pdf)**  
   已核验 §I–III。联合侧信息保留目标函数，而非完整恢复来源的原则已覆盖。当前不需要已知分布，也没有实行图着色编码；该差别不足以把条件冗余删除变成新理论。跨域理论近邻，不能冒充 AppWorld baseline。

5. **[Lossless Value Directed Compression of Complex User Goal States for Statistical Spoken Dialogue Systems（2011）](https://www.isca-archive.org/interspeech_2011/crook11_interspeech.pdf)**  
   已核验 §3–4。以对象集合表示用户目标、支持负约束并进行决策相关无损压缩，覆盖目标集合压缩的早期依据。原作依赖已知 POMDP 模型，当前操作自然语言见证和局部候选调用；属于跨域近邻。

```json
{
  "score": 6.9,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "将实际返回 r 写成不可删除约束后，核心删除判据和有限域贪心过程直接等价于已知约束冗余消除；当前尚无超出这一实例化的独立机制。",
    "最小实验能够检验应用收益，但所列对照不能区分当前方法与同一实际返回条件下的经典解集合保持删除，因而不能支持其剩余机制新颖性。"
  ],
  "novelty_conclusion": "真实API观察下保护历史排除关系具有具体应用价值，但条件化、目标集合保留与逐条冗余删除已有原始依据。当前贡献主要是已知算子在冻结LLM agent上的应用和评估设计，独立机制创新不足。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Removing Redundancies in Constraint Networks",
      "url": "https://ftp.cs.ucla.edu/pub/stat_ser/r81-reprint.pdf",
      "overlap": "根据其余约束识别冗余，删除约束而保持完整解集合及动作排除关系。",
      "difference": "当前使用自然语言历史和真实API观察，原作处理形式化约束网络。",
      "verified": true
    },
    {
      "title": "On Redundancy in Constraint Satisfaction Problems",
      "url": "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2022.11",
      "overlap": "有限域约束删除前后的解集合等价定义，以及逐条贪心删除冗余约束。",
      "difference": "当前增加LLM来源解析、原文输出和agent完整成本计费；删除机制没有独立差别。",
      "verified": true
    },
    {
      "title": "FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents",
      "url": "https://arxiv.org/html/2609.37590v1",
      "overlap": "冻结闭源API模型、原文历史片段选择、负约束保留、AppWorld评估及静默实体遗漏。",
      "difference": "FOCUS采用草稿规划依赖和防御性验证，当前使用真实只读返回条件下的符号可行集合；完整作者代码未核实。",
      "verified": true
    },
    {
      "title": "Functional Compression through Graph Coloring",
      "url": "https://www.mit.edu/~medard/2010papers/funccomp.pdf",
      "overlap": "利用侧信息保留来源的目标函数，压缩充分性取决于联合关系。",
      "difference": "当前不实行图着色编码或假设已知分布，而是对局部有限动作约束删除原文见证。",
      "verified": true
    },
    {
      "title": "Lossless Value Directed Compression of Complex User Goal States for Statistical Spoken Dialogue Systems",
      "url": "https://www.isca-archive.org/interspeech_2011/crook11_interspeech.pdf",
      "overlap": "以对象集合表示复杂用户目标和负约束，按下游决策价值无损压缩。",
      "difference": "原作依赖已知POMDP模型，当前处理自然语言历史与局部API候选域；不是同任务baseline。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "当前聚焦正确澄清后的历史约束与当前观察下合法错实体，分别关联AppWorld-UL的旧要求遗忘和问答错绑、TRACE的静默状态错误盲区。允许不覆盖全部初始drawbacks，当前未承诺解决信息已保留却未被使用的全部失败。API冻结、CPU处理、oracle仅离线评估、完整预算计费及不运行实验等硬约束均满足。"
  }
}
```