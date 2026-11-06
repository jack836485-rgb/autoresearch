## 结论
2026-11-05，总体 score 4.5/10，verdict：needs_rethink。主贡献是一个诊断性发现：在 GUI 截图–动作循环里，RL 微调是加重还是缓解"知而不改"，作用在三环中的哪一环。问题值得问，但现在的设计识别不出"RL 这一步"的效应，原因有三。
- 关键识别假设与公开数据直接矛盾：所谓"GUI-Owl-7B 自己的轨迹"其实出自一次 TRPO 环境 RL 运行。
- "RL 前"检查点本身可能已经过 GUI-Owl 管线里的 RL 阶段。
- 能隔离初始化的第二对，其环境和任务来源都没有落实。

三项分数没有一项达到 8，不满足放行门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 文本侧有两个方向相反的结论（DeepMind 认为 RL 能缩小 knowing-doing gap，RAGEN 观察到 Echo Trap），GUI 上的受控归因确实空缺，结果会影响"GUI RL 配方要不要专门处理无效步"的判断。但证据只来自一个模型家族的一对检查点，测的是离线代理指标，且离线三项能否预测在线惯性仍未知，影响范围有限。另外，支持条件是"三项中至少一项显著"，而任意两个检查点在 ~500 状态 × 16 采样下几乎必然有某项不同，再叠加按动作类型和任务域分层的多重比较，"支持"结果的信息量偏低。即便有差异，也只说明"RL 改变了某一环"，不等于"惯性的训练侧来源在 RL"。 |
| 新颖度 | 7.0 | 检索没有找到在 GUI/CUA 上用同底座 RL 前后检查点检验惯性或知而不改的工作。Absorbed in Inertia 比较的是不同家族，测的是激活与 R³ 修法；GUI-Libra 与 Faithful-Agent 研究的是如何训练推理–动作一致性，不是做归因。把文本侧的度量（纠错增益、复读、承认–动作耦合）迁移到目标领域，按迁移规则可给 7。不给 8 的原因：三项度量都直接取自近邻（Feedback That Backfires、RAGEN/Conversational Inertia、Absorbed in Inertia 的承认判定），没有针对 GUI 的结构性适配，整体是一个标准的前后对照组装。 |
| 有效性（先验合理性） | 4.5 | **支持的依据**：跨家族预检显示复读率 EvoCUA-8B 44% > UI-TARS 24% > OpenCUA-7B 13%，方向与"RL 加重复读"相容，但混杂明显。AgentNet 中只有 0.4% 的步重复了错误动作，确实削弱了"只用成功轨迹 SFT 造成惯性"这一解释。<br>**直接反证 1（轨迹来源）**：我读取了 `xlangai/ubuntu_osworld_verified_trajs/mobile-agent-v3-gui-owl-7b.zip` 的中央目录，361 条轨迹全部位于 `results_0827_rl_7b_2img_183.../qwen25vl_7b_2im_high_rft_7b_final_2img_183_trpo_passndata/`，result.txt 的平均成功率是 32.1%，不是论文给出的通用版 29.4%。这批卡住状态很可能是 RL 检查点（Desktop-RL 或其近亲）的在策略状态，而不是 RL 前模型的在策略状态。按 RL 模型自己卡住的地方选状态，会使 RL 模型的失败动作对数概率在构造上偏高，这种选择偏差与待测方向同号。<br>**直接反证 2（"RL 前"并非 RL 前）**：Mobile-Agent-v3（arXiv:2508.15144）写明 GUI-Owl 是"三阶段训练，含 RL 阶段"（静态任务用 GRPO，在线用 TRPO）。Desktop-RL 实验"从成功率 27.1 的初始检查点出发"，这与通用版的 29.4 不一致，运行名还暗示初始化是 `rft_7b_final`。因此主对比较的是"未知初始化上的桌面 TRPO"与"可能已含 RL 的通用发布版"，"三项都无差异则惯性归于底座或 SFT"这一推翻逻辑不成立。<br>**其他混杂**：SFT 参照用的是 OpenCUA-7B，它换了数据和训练配方，不是同一管线的 SFT 阶段，分不开"SFT 效应"与"数据集效应"。 |
| 待预研（不计分） | — | 两检查点在三项上的差值大小；离线三项与在线惯性率是否对应；卡住状态的实际数量（该 zip 共约 4,100 步，未必有"约 500 个"）；judge 对"新鲜承认"判定的一致性。 |

**与起点问题的关系**：这是原问题"训练侧来源"一支的子问题，不做修法，冲突终止不在范围内。原问题中"耦合在哪断开""能否改善恢复与终止"仍未回答，但转向本身不构成阻断。

**实验能否判别主张**：现在不能。主对的状态来源与初始化都有混杂，能把 RL 效应和初始化、数据差异分开的只有第二对。而第二对存在三个问题：
- OSWorld 没有官方训练划分，"OSWorld 训练任务"不存在。如果用这 369 个测试任务做 RL，再在同一批任务的卡住状态上离线测量，会有污染。
- KVM 是否可用尚未确认。
- 回退方案"其他可用网页环境"没有具体指向。

退回到"只报告主对"时，主张无法检验。

**可行性：fail**（针对主张所必需的部分）。
- 离线部分可做：两个检查点的权重公开；轨迹 zip 存在，traj.jsonl 含完整 `<thinking>/<tool_call>/<conclusion>` 响应与逐步截图，上下文可以重建，贪心复现率过滤也合理。4 个 7B 模型 × 数百状态 × 17 次前向，单张 A100 1–2 天可以完成；约 1 万次 judge 调用在 1000 元预算内。
- 主张依赖的"同初始化、已知配方"第二对缺少已确认的 VM 环境和不与评测重叠的任务来源。在 8×A100 上做 GRPO 同时还需要大量并行 VM，这部分资源和规范目前不足，不只是"没有代码"。

## 最高近邻
1. Absorbed in Inertia: Activation Analysis for Computer-Use Agents（https://arxiv.org/abs/2609.37176）。重叠：CUA 惯性现象、承认失败后仍重复、经由上下文起作用（R³ 修法）。差别：比较的是多个不同家族的模型，没有同底座的训练阶段对照。
2. LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities（https://arxiv.org/abs/2504.16078）。重叠：RL 微调对 knowing-doing gap 的影响。差别：只在 bandit 与井字棋这类文本环境里，不涉及 GUI 截图–动作循环。
3. RAGEN: Understanding Self-Evolution in LLM Agents via Multi-Turn RL（https://arxiv.org/abs/2504.20073）。重叠：多轮 RL 导致推理坍缩、重复（Echo Trap）。差别：在风格化的小环境里训练时观察到，不是对公开 GUI 检查点做的离线归因。
4. Feedback That Backfires（https://arxiv.org/abs/2608.23651）与 Mitigating Conversational Inertia（https://arxiv.org/abs/2602.03664）。重叠：纠错增益为负、模型把自己先前的响应当示范模仿，本案三项度量中两项直接来自这里。差别：研究对象是文本或小模型，没有 RL 前后对比。
5. Mobile-Agent-v3 / GUI-Owl（https://arxiv.org/abs/2508.15144）。重叠：本案检查点对与 OSWorld 轨迹的来源，论文报告 TRPO 把 OSWorld 成功率从 27.1 提到 34.9，也提到 replay buffer 处理失败轨迹。差别：只报告成功率，不分析惯性与推理–动作耦合；同时它也是本案混杂（初始化未明、通用版含 RL 阶段）的来源。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 6.0, "novelty": 7.0, "effectiveness": 4.5},
  "contribution_assessment": "主贡献是诊断性归因：GUI 截图–动作循环中，RL 微调是加重还是缓解'知而不改'，作用在三环中的哪一环。问题有价值（文本侧有方向相反的结论，GUI 缺少受控证据），但只基于单一家族的一对检查点和离线代理指标，且支持条件'三项中至少一项显著'信息量低，重要性 6。目标领域内没有找到同底座 RL 前后的惯性归因，迁移本身有新意，但度量全部来自近邻，缺少结构性适配，新颖度 7。有效性 4.5，因为存在直接反证：OSWorld-Verified 中的 gui-owl-7b 轨迹全部出自 trpo RL 运行目录，成功率 32.1% 而非通用版的 29.4%，所谓 RL 前的在策略状态实为 RL 检查点的状态，有同向的选择偏差；GUI-Owl 管线本身含 RL 阶段，Desktop-RL 的起点是成功率 27.1 的未名检查点，因此主对不能隔离'RL 这一步'，'无差异则归于底座或 SFT'的推翻逻辑失效；OpenCUA-7B 作为 SFT 参照混入了数据集差异。待预研：差值大小、离线指标与在线惯性率是否对应、卡住状态数量、judge 一致性。",
  "feasibility": "fail",
  "feasibility_reason": "离线测量可做：权重和轨迹公开，traj.jsonl 含完整推理与截图，单张 A100 1–2 天，judge 费用在预算内。但主张所必需的同初始化第二对缺少已确认的 KVM/OSWorld VM；OSWorld 没有训练划分，用测试任务做 RL 会污染离线评测；回退环境没有具体指向。只剩主对时主张无法检验。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "识别假设与公开数据矛盾：mobile-agent-v3-gui-owl-7b.zip 的 361 条轨迹均出自 'rl_7b..._rft_7b_final..._trpo_passndata' 运行，成功率 32.1%，不是 RL 前 GUI-Owl-7B 的在策略状态，按 RL 模型卡住处选状态会产生与待测方向同号的选择偏差",
    "主对不是干净的 RL 前/后对照：GUI-Owl 三阶段管线含 RL 阶段，Desktop-RL 从成功率 27.1 的未名检查点出发（通用版为 29.4），'三项无差异则归于底座或 SFT'的推翻逻辑不成立",
    "唯一能隔离初始化的第二对没有可行的环境和任务来源（KVM 未确认，OSWorld 无训练划分，用测试任务训练会污染），只剩主对时主张不可检验",
    "支持条件过宽：'三项中至少一项显著'在两个不同检查点之间几乎必然成立，又有分层多重比较，不能区分'RL 是惯性来源'与'RL 改变了某个指标'",
    "贡献门槛未达：三项分数中没有一项达到 8"
  ],
  "novelty_conclusion": "检索未发现 GUI/CUA 上用同底座 RL 前后检查点做惯性或知而不改归因的工作，属于目标领域的迁移新意（7）；度量组件均来自 Feedback That Backfires、RAGEN/Conversational Inertia 与 Absorbed in Inertia，没有结构性适配，未到 8。",
  "closest_neighbors": [
    "Absorbed in Inertia: Activation Analysis for Computer-Use Agents (arXiv:2609.37176)",
    "LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities (arXiv:2504.16078)",
    "RAGEN: Understanding Self-Evolution in LLM Agents via Multi-Turn Reinforcement Learning (arXiv:2504.20073)",
    "Feedback That Backfires (arXiv:2608.23651) / Mitigating Conversational Inertia in Multi-Turn Agents (arXiv:2602.03664)",
    "Mobile-Agent-v3: Foundamental Agents for GUI Automation (arXiv:2508.15144)"
  ]
}
```
