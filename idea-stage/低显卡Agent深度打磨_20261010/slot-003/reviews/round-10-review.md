## 结论

实际检索日期：**2026-10-10**。**score：6.6；verdict：needs_rethink。**

“同一失败经验在正文暴露与证据定位两种用途下，效用可能反号”仍是有研究价值、尚未被本次检索直接覆盖的经验假设。但当前没有成立的独立方法机制：记忆引导重读、问题驱动证据定位、原文回查及按表示评估质量与成本，都已有原作。

**Fatal blocker：核心支持条件要求超过一个按定义与方法同构的强对照。** 给定同一失败 query \(q\)、当前上下文 \(H\)、选择器 \(S\)、span 上限、追加位置和 actor，两者都执行 \(s=S(q,H)\)，再让 actor 读取相同输入。固定随机性时结果相同；随机执行时输出分布也相同。因此，正文有害而 cue 有效可以支持用途差异，却不能支持相对于该强对照的独立算法优势。

目标演化成立：从经验暴露／淘汰聚焦到复用介面的价值差异，仍关联 Q004，尤其是 D01、D03。[技能负迁移原作 §IV-C、§V-B](https://arxiv.org/html/2608.11888v1)支持正文引入错误默认值和额外流程的风险，但不证明 cue 有效。当前没有隐藏 oracle 或本阶段执行违规；不覆盖 D02 的选择混杂不是拒绝理由。

实现可行性不是主要阻断：[AppWorld ReAct 源码](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py)确实接收执行观察、调用模型并记录 usage；[MemReread API 接口](https://raw.githubusercontent.com/iiGray/MemReread/main/exp/interface/mem_reread_api.py)也可核验。模型与完整成本原则可对齐，但尚未确认的预算参数意味着交接尚未定型。MemReread、PracRepair 的任务适配对照不能称为它们在 AppWorld 上的官方复现。

## Claim 判断

| Claim | 新颖性判断 | 最关键原文依据与可验证性 |
|---|---|---|
| 同一失败经验正文有害，但其证据定位用途有益 | **部分重合，具体反号关系未被直接覆盖** | [技能负迁移研究 §IV-C、§V-B](https://arxiv.org/html/2608.11888v1)已有正文诱发实现错误与重流程；[技能改写研究 §3.3、§4](https://arxiv.org/html/2606.09421)已有表示依赖的质量／成本效用。配对干预可以验证反号，但当前无结果。 |
| 经验仅指导选择当前原文，不向 actor 注入历史事实／动作配方 | **部分重合** | [ReadAgent §3.2](https://arxiv.org/html/2402.09727)用记忆选择原文回查；[MemReread §2.3、§3.1](https://arxiv.org/html/2605.10268)用记忆生成子问题并重读；[PracRepair §III-B](https://arxiv.org/html/2606.17612)让问题指定所需证据。历史失败 query 与仅追加已见原文是区别，但尚非独立选择机制。 |
| 历史失败驱动摘录优于同 query、同 selector 的普通重读 | **已被强对照定义覆盖；fatal blocker** | 这是当前 Brief 自身定义导致的算法等价，不依赖文献猜测。稳定优势无法归因于所提机制；若出现差异，说明实际输入、选择流程、随机性或成本没有对齐。 |
| 按正文价值淘汰经验，可能丢掉另一用途的价值 | **部分新颖的条件性推论** | [RSCB-MC](https://arxiv.org/html/2604.27283)已有多种记忆使用／不注入动作；[LIMBO](https://arxiv.org/html/2609.14138)已有记忆策略与成本联合选择。它们未直接证明本 Claim。反号成立后可推出“正文价值不足以代表所有用途”；当前实验没有验证真实淘汰过程造成的损失。 |
| 收益来自失败经验选择规律，而非重复、位置或普通诊断 | **目前不能成立** | [Re2 §2.2](https://arxiv.org/html/2309.06275)、[Prompt Repetition §2](https://arxiv.org/html/2512.14982)已有重复收益。所列位置／重复对照可以排除这些解释，但同 query 强对照仍与方法相同。仅 official test aggregate 也不能确认逐经验效用反号。 |

## 最高近邻

1. **[MemReread: Enhancing Agentic Long-Context Reasoning via Memory-Guided Rereading](https://arxiv.org/html/2605.10268)**  
   已核验 §2.3、§3.1、附录 E，以及作者 API 源码。重合是记忆产生问题、问题引导当前原始上下文重读。差别是原作使用当前文档的 terminal memory、重读后生成／整合子记忆；本方案使用跨任务失败 query，只追加已见原文 span。冻结模型与 API 推理不是新增边界。

2. **[A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts](https://arxiv.org/html/2402.09727)**  
   已核验 2024 年原作 §3.2。记忆指导选择原始页面再次阅读，并控制回查数量，已覆盖“记忆影响证据选择而不必只靠记忆正文回答”的基本结构。其记忆来自当前文档，且仍传给回答模型；本方案强调历史失败与正文／cue 价值反号。

3. **[PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](https://arxiv.org/html/2606.17612)**  
   已核验 §III-A、§III-B。诊断问题指定程序实体、运行行为和所需证据，通过统一接口按需取证，并允许提前停止。差别是原作针对 Java 修复、可获取尚未暴露的静态／动态证据，并形成答案和修复建议；本方案只选择 actor 已见文本。原文的 Zenodo artifact 链接本次访问失败，**代码未核验**。

4. **[ExpeRepair: Dual-Memory Enhanced LLM-Based Repository-Level Program Repair](https://arxiv.org/html/2506.10484)**  
   已核验 §2.2、§2.3。失败反馈与历史修复经验共同影响检索和动态 prompt；经验包含失败—反馈—纠正轨迹及抽象策略。差别是其示例／策略直接进入 actor，未检验同一经验改作纯证据定位规则后的效用反号。原作明确较少处理 bug localization，不能据此声称当前定位用途已被完整覆盖。

5. **[What Should a Skill Remember? Quality-Cost Trade-offs in Cost-Aware Skill Rewriting for Language Model Agents](https://arxiv.org/html/2606.09421)**  
   已核验 §3、§4、附录 F/G。它比较不同信息保留表示，并按任务条件下的质量与完整执行成本选择策略。差别是改写后的技能仍直接提供给 actor；本方案移除经验正文，仅让其控制当前证据选择。它使“换一种经验表示即可构成独立贡献”的边界很弱，但未直接证明所提反号现象。

```json
{
  "score": 6.6,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "核心独立贡献要求超过同失败query、同当前上下文、同selector、同span范围、同追加位置和同actor的普通重读强对照；按当前定义两者是同一算法，固定随机性时输入与结果相同，随机执行时输出分布相同，不能形成独立机制优势。"
  ],
  "novelty_conclusion": "同一失败经验在正文暴露与当前证据定位用途下的效用反号仍是有价值且未被本次检索直接覆盖的经验假设，但记忆引导重读、诊断问题驱动取证及表示依赖的质量成本效用已有原作。当前方法与其必要强对照同构，独立方法贡献不成立；淘汰损失目前只属于条件性推论。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "MemReread: Enhancing Agentic Long-Context Reasoning via Memory-Guided Rereading",
      "url": "https://arxiv.org/html/2605.10268",
      "overlap": "记忆生成子问题，子问题指导原始上下文重读；已有冻结模型和API推理。",
      "difference": "原作使用当前文档terminal memory并生成整合子记忆；当前方案使用跨任务失败query，只追加actor已见原文span，研究正文与cue的效用反号。",
      "verified": true
    },
    {
      "title": "A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts",
      "url": "https://arxiv.org/html/2402.09727",
      "overlap": "记忆指导选择原始页面回查，控制回查预算并利用原始细节回答。",
      "difference": "记忆来自当前文档且仍进入回答模型；当前方案强调历史失败query与经验正文不进入actor。",
      "verified": true
    },
    {
      "title": "PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices",
      "url": "https://arxiv.org/html/2606.17612",
      "overlap": "诊断问题明确指定所需证据，按需检索静态和动态执行上下文，允许提前停止。",
      "difference": "原作针对Java程序修复，可获取尚未暴露证据并形成诊断答案及修复建议；当前方案仅选择已见原文。原文已核验，Zenodo artifact本次访问失败，代码未核验。",
      "verified": true
    },
    {
      "title": "ExpeRepair: Dual-Memory Enhanced LLM-Based Repository-Level Program Repair",
      "url": "https://arxiv.org/html/2506.10484",
      "overlap": "失败反馈和历史修复经验驱动检索、反思策略及动态prompt。",
      "difference": "原作直接注入历史示例和策略，没有检验同经验改作纯当前证据定位用途后的效用反号。",
      "verified": true
    },
    {
      "title": "What Should a Skill Remember? Quality-Cost Trade-offs in Cost-Aware Skill Rewriting for Language Model Agents",
      "url": "https://arxiv.org/html/2606.09421",
      "overlap": "比较经验表示及信息保留策略，按任务条件下的质量和完整执行成本评价效用。",
      "difference": "原作仍将改写技能直接提供给actor；当前方案以历史经验控制当前证据选择而不提供经验正文。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "聚焦失败经验复用介面的价值差异仍属于Q004，与D01的暴露负迁移和D03的额外流程成本有原作依据。无需覆盖D02才可成立；当前没有隐藏oracle或本阶段执行违规，低本地GPU和完整预算对齐原则可行。原作只支持正文负迁移风险，不证明cue有效；尚未观察淘汰损失，也不能由official test aggregate确认逐经验反号。"
  }
}
```