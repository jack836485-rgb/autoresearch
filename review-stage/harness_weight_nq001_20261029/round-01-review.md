## 结论

日期：2026-10-29。**Score 4.0 / 10，verdict：needs_rethink。**

核心方法“把 H\* 独有、H0 下学生看不到的信息，改写成学生在 H0 动作空间里自己取信息的动作，再在 H0 下 SFT”，已经被 Harness-Zero（arXiv 2609.24974，2026-09-21，已开源）基本覆盖。它要解决的问题与本 brief 相同：进化 harness 和目标 harness 在动作空间与可得信息上不同，H\* 的指导因此不能直接监督 H0。它的评测也包含 AppWorld test_normal 和 Qwen 9B 级学生。它的 reviewer 提示词明确写着“When required evidence is missing, replace the proposal with an `execute` action that collects it”，与本方法的“可由工具取得 → 插入工具调用并真实回放”是同一个动作。它报告 H0 下恢复了 82.3% 的 harness 独有行为（含 memory、tool 类），这与 Claim 1 的论证前提“现有内化方法在看的增益上失败”直接矛盾。brief 没有引用它，也没有把它列为对照：它同领域、同基准、有公开实现，所以构成 fatal 的 baseline 缺失。

Claim 1 的因果解释也大多已在原文中给出。PSP 已经把失败归因为学生不可得的信息差 I(Y_k; σ | X, Y_<k) > 0。2610.11655 已经写明“an adapter that is not shown the second page did not reproduce what the model did with it”。把两者统一到 imitation gap 只是换了名称。

仍有差别的部分有三处：一是三类可得性的划分（本回合已观察但被截断 / 工具可查 / 不可得）及其分层预测；二是“已观察但被截断 → 插入自写笔记”这一类改写；三是不依赖前沿教师的、基于对数概率的离线依赖归因。Harness-Zero 没有分析剩下约 18% 未恢复的行为属于哪一类。这些差别目前不足以撑起方法新颖性，Claim 必须围绕与 Harness-Zero 的边界重新确立，否则不值得按现方案继续投入。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. 现有内化方法在“看”的增益上失败，原因是 imitation gap | 已被覆盖 / 有 claim blocker | PSP 已给出信息差解释；2610.11655 已给出“adapter 看不到第二页”的解释；Harness-Zero 在 AppWorld 上内化了 H\* 的工具 / 记忆类行为且超过 H\*，“现有方法失败”的论断与已知证据冲突 |
| 2. 分界是信息在 H0 下能否由 agent 自己取得（三类划分） | 部分重合 | Harness-Zero 要求“只用学生可见信息，缺证据就插入取证动作”，隐含了“可取得”这一边界，但没有显式划分三类，也没有分层检验；截断历史→笔记这一类与 MemAct / ContextPilot 的“学习管理上下文”相邻，但事后改写 SFT 轨迹的形式未见直接先例 |
| 3. 改写为取信息动作后训练能内化，并给出分层预测 | 大部分被覆盖 | 工具可查类的改写 = Harness-Zero 的 REPLACE→execute 取证；只有离线归因、笔记类改写，以及“不可得类所有方法都恢复不了”的预测仍新；最小实验缺 Harness-Zero 对照，无法证明在相同预算下优于最高近邻 |

## 最高近邻

1. **Harness-Zero: Harness Distillation via Agent-as-Harness**（https://arxiv.org/abs/2609.24974 ；代码 https://github.com/metaevo-ai/harness-zero ，已用 git 浅克隆核验，含 `envs/appworld`、`src/harness_zero/sft.py`）。重叠：H\*→H0 蒸馏进权重，把缺失信息改写为学生原生的取证动作后 SFT；AppWorld test_normal；Qwen3.5-9B LoRA SFT。差别：它在线逐步审阅，用 GPT-5.6 Sol 作 harnessing agent（需付费 API），没有可得性三分类、截断历史→笔记改写和离线对数概率归因，也没有回答“哪些增益不能内化”。
2. **Harness Evolution Hits a Ceiling: When Weight Training Should Begin**（https://arxiv.org/abs/2610.11655 ）。重叠：同一问题设定；已提出“写进权重、看留在 harness”的规则，并解释 adapter 看不到第二页。差别：只做了原轨迹 SFT，没有改写；代码未开源。
3. **From Self-Distillation to Self-Practice: Privileged Information for Multi-Turn Agents（PSP）**（https://arxiv.org/abs/2609.29051 ）。重叠：AppWorld，特权信息自蒸馏失败，已用信息差形式化地解释原因。差别：它的修法是把 PI 放进采样器、再跑 GRPO，而不是改写成取信息动作；它的 PI 是参考解或指令，不是 harness 上下文。
4. **On-Policy Context Distillation（OPCD）**（https://arxiv.org/abs/2602.12275 ；代码 https://github.com/microsoft/LMOps/tree/main/opcd ，已核验 `scripts/textgame_consolidate.sh` 存在）。重叠：H0 输入匹配 H\* 教师，即 brief 中的对照 4。差别：没有改写。另外它的 TextGame 只支持 FrozenLake / Sokoban（max_steps 5），接入 ALFWorld 的长程多步交互需要不小的改造。
5. **Better than Your Teacher: LLM Agents that learn from Privileged AI Feedback（LEAP）**（https://arxiv.org/abs/2410.05434 ）。重叠：ALFWorld，特权教师纠正学生，且已强调平衡特权信息与学生的 realizability。差别：没有涉及 harness 增益内化，也没有把信息改写为取信息动作。

```json
{
  "score": 4.0,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "novelty: 核心动作（把 H*-only 信息改写为 H0 下学生原生的取证动作后 SFT 内化 harness 增益）已被 Harness-Zero (arXiv 2609.24974, 开源, AppWorld) 覆盖",
    "feasibility/baseline: 缺少同领域同基准、有公开实现的最高近邻 Harness-Zero 作为对照",
    "claim: Claim 1 '现有内化方法在看的增益上失败' 与 Harness-Zero 在 AppWorld 上恢复 82.3% harness 独有行为且超过 H* 的证据冲突；信息差的因果解释已由 PSP 与 2610.11655 给出"
  ],
  "novelty_conclusion": "方法核心被 Harness-Zero 覆盖，Claim 1 的解释已由 PSP/2610.11655 给出；剩余新意仅为可得性三分类、截断历史->笔记改写和离线 logprob 归因，不足以支撑当前 Claim",
  "closest_neighbors": [
    "Harness-Zero: Harness Distillation via Agent-as-Harness (arXiv 2609.24974)",
    "Harness Evolution Hits a Ceiling: When Weight Training Should Begin (arXiv 2610.11655)",
    "From Self-Distillation to Self-Practice: Privileged Information for Multi-Turn Agents (arXiv 2609.29051)",
    "On-Policy Context Distillation for Language Models (arXiv 2602.12275)",
    "Better than Your Teacher: LLM Agents that learn from Privileged AI Feedback (arXiv 2410.05434)"
  ]
}
```
