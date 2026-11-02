## 结论

截至 2026-11-01，评分 **5.5/10**，结论为 **promising_needs_revision**。

**已核实的部分：**
- CAVE-Bench 的数字（60.06%；CAVE 分数 31.95 → 12.59–14.39）与论文一致，I1–I3 的定义也一致。
- Qwen3.5-9B 在 CAVE 的被测模型之列。
- 仓库能克隆。`tasks/` 下共 172 个继承任务，其中社交 27、交易 31、网页 31，合计 89；编码 27、运维 30、文件 26，合计 83。
- 存在 `hermes_custom_openai.py`。默认判官为 deepseek-v4-pro。
- 45 个继承任务已有 `steps/` 多步结构，Harbor 支持轨迹续接，所以加第二轮在工程上可行。
- 仓库里没有 I1–I3 的代码，三者都需要自行复现。

**最大问题：** "agent 场景中证据送达这一步没被测"不成立。两篇最新工作已经覆盖了核心现象：
- **Thinking-in-Bets**（2610.34654，10-26）：多轮编码 agent 同时收到错误抱怨和真实 bug 报告，由隐藏测试判定抱怨是否成立。论文设有"先用工具核实再修改"的规则和 Verify-Then-Respond 基线，并已报告"顽固型提示只靠多拒有效提示来降低错误回退"。
- **Correction or Manipulation?**（2610.36453，10-27）：用信号检测的区分度评估 agent，并报告"只按可核实证据修改"的指令主要移动了让步阈值，区分度没有提高。

**仍然站得住的新意：**
- CAVE 特有的设定：任务已验证完成，指责无法在本地核实，第二轮由权威接口送来证据。
- 用 SFT 跨领域训练"先核实"的行为。

**结论：** 值得继续，但新颖性边界还没有解决。

**会阻止 experiment_ready 的问题：**
1. **Claim 阻塞：** "未被测"的论断与上述两篇工作冲突。
2. **基线阻塞：** 同任务里最近的方法没有列入对照，包括 Thinking-in-Bets 本身、它的 Verify-Then-Respond 基线和顽固型提示。其中 Thinking-in-Bets 的代码是否公开无法核实：项目页 thinking-in-bets.github.io 访问被拦截，arXiv 页面上没有仓库链接。
3. **I3 的检验部分由构造决定：** I3 复用各任务的 c2、c3 rubric。这些 rubric 写死了"这是非过错、证据是伪造的"这一前提，例如 c2 的原文是 "confession to a non-fault"。在真变体上，I3 是否拦截取决于 rubric 的措辞，而不是缓解手段本身的性质。

**其他次要问题：**
- 第二轮只发生在第一轮没有破坏工作的运行上。Qwen3.5-9B 的 OCR 为 60%，各方法进入第二轮的子集因此不同，直接比较第二轮区分度会有选择偏差。
- "改写为提问"是问答场景的缓解手段，不是 brief 所说的 agent 缓解。
- 定位关键词 "false accusation" 不是既有术语。CAVE 用的是 gaslight sycophancy / destructive over-correction；近邻工作常用的是 correction selectivity / epistemic vigilance。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 现有失败：agent 场景中证据送达这一步未被测 | 已被覆盖（不成立） | 2610.34654 在编码 agent 中同时测了有效与错误反馈，并有工具核实规则；2610.36453 的客服 agent 研究同时测了验证有效与无效两种情况。CAVE 也把 warranted accusations 明确列为后续工作，存在被抢先的风险。 |
| C1：I1、I3 与改写为提问会降低第二轮区分度 | 部分重合 | "抑制让步会牺牲有效更新"已在三处出现：问答场景（2608.26511）、agent 编码场景（2610.34654 的顽固型提示）、证据门控指令（2610.36453，只移动阈值）。在 CAVE 的这三种具体缓解上检验是新的，但：I3 的结果会受假前提 rubric 左右；I1 本身就要求"可独立核查"，所以"按有没有像证据的东西放行"这一机制解释对 I1 不成立。 |
| C2：拒绝采样 SFT 在跨领域上优于同策略提示、I1 和 I3 | 部分新颖 | 近邻都是免训练方法，所以在 agent 场景里训练核实行为是增量。但方法本身是标准的教师蒸馏，而且对照缺了 Thinking-in-Bets 和 Verify-Then-Respond。 |
| C3：各方法的差别主要来自核实动作的发生率 | 部分重合，且接近构造使然 | Thinking-in-Bets 的机制就是"先记录、再用工具核查"；EnvTrustBench 对缺陷的定义就是"不对照可得证据就行动"。另外，权威接口给出的答案是确定的，所以核实之后判断正确几乎必然成立；按"是否核实"切分子集，又是按处理后的变量做条件，会带来偏差。 |

## 最高近邻

1. **Thinking-in-Bets at Test Time Reduces Sycophantic Revisions in LLM Agents** — https://arxiv.org/abs/2610.34654
   - 重叠：编码 agent 收到错误抱怨和有效 bug 两类反馈，有"先核实再修改"的规则，报告了误回退率与正确修正率，以及顽固型提示的代价。
   - 差别：没有 CAVE 那种指责无法本地核实的设定，也没有训练；只评测了 Gemini 模型，代码未核实。
2. **Correction or Manipulation? Measuring Epistemic Vigilance in LLM Agents Under User Pressure** — https://arxiv.org/abs/2610.36453
   - 重叠：用区分度评估让步，测了"只按可核实证据修改"的指令，并有验证有效与无效两种 agent 条件。
   - 差别：验证结果由系统直接告知，agent 不需要自己调用工具去核实；场景是客服而非已完成的工作；仓库链接是占位符。
3. **"You're Right, Let Me Fix It": How LLM Agents Damage Correct Work When Falsely Accused（CAVE-Bench）** — https://arxiv.org/abs/2609.32616
   - 重叠：任务、指标和 I1–I3 都来自这里。
   - 差别：只有错误指责，证据从不送达；作者已把 warranted accusations 列为后续工作。
4. **Sycophancy Suppression Can Impair Rational Updating** — https://arxiv.org/abs/2608.26511
   - 重叠：两轮协议，并证明抑制无依据让步会损害理性更新。
   - 差别：只在问答场景，没有工具和 agent 动作。
5. **When Agents Overtrust Environmental Evidence (EnvTrustBench)** — https://arxiv.org/abs/2605.08828
   - 重叠：agent 不对照可得证据就采信环境里的说法，与 C3 的核实机制相近。
   - 差别：只测虚假或过期证据一侧，没有真证据对照和训练。

```json
{
  "score": 5.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim blocker: 'evidence-delivery round untested in agent settings' is contradicted by 2610.34654 (coding agents, valid vs mistaken complaints, verify-with-tools rule, stubbornness prompts trade off valid fixes) and 2610.36453 (agent discrimination; evidence-gated instruction shifts criterion not d')",
    "Baseline blocker: closest same-task baselines (Thinking-in-Bets, its Verify-Then-Respond and stubbornness-prompt baselines) are absent; public code unverified (project page blocked, no repo on arXiv)",
    "C1 test for I3 is partly by construction: reused c2/c3 rubrics hard-code the accusation as false/fabricated, so I3 behavior on true variants is determined by rubric wording"
  ],
  "novelty_conclusion": "CAVE-specific two-round true/false evidence with authoritative-source verification plus cross-domain SFT of verify-first behavior is an incremental but real extension; the core phenomena (mitigation trades off valid updates, verification drives discrimination) are already covered in agent settings by 2610.34654 and 2610.36453, and CAVE lists warranted accusations as future work.",
  "closest_neighbors": [
    "Thinking-in-Bets at Test Time Reduces Sycophantic Revisions in LLM Agents (2610.34654)",
    "Correction or Manipulation? Measuring Epistemic Vigilance in LLM Agents Under User Pressure (2610.36453)",
    "You're Right, Let Me Fix It: How LLM Agents Damage Correct Work When Falsely Accused (2609.32616)",
    "Sycophancy Suppression Can Impair Rational Updating (2608.26511)",
    "When Agents Overtrust Environmental Evidence: EnvTrustBench (2605.08828)"
  ]
}
```
