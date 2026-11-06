## 结论

2026-11-05：总体 score 5.0，verdict = needs_rethink。主贡献是一次测量审计：用 Absorbed in Inertia 的现成检测器，在 6 个公开检查点（2 个初始化、4 个 RL 后代）上测"在线 RL 让截图 CUA 的知而不改式惯性变好还是变坏"。这个问题在 GUI 上确实没人测过，但贡献分量不够。即便关键结果成立，产出也只是 4 个异质检查点上的描述性方向判断；n=4 推不出"哪类配方元素与方向相关"。主指标 1 还有原论文自己指出的失效方式（承认失败少了，惯性率就会下降），SEAgent 这一对也不是纯 RL。三项分数都达不到 8。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 若结论是"RL 提高成功率的同时加重了承认失败后的重复"，这是有用的警示：成功率之外需要单独看无效步。但它不改变方法判断，因为在奖励里惩罚冗余已有现成做法：SEAgent 的 World State Model 把 redundant 步排除在正奖励之外。若结论是"依配方而异"，4 个点只能给出轶事式的归因。研究对象是受起点问题限定的描述性子问题。 |
| 新颖度 | 6.5 | 我检索 GUI 领域，没找到用同初始化 RL 前后对照测惯性或 knowing-doing gap 的工作。但测量工具（Inertia 检测器与 judge）、问题本身（DeepMind 2504.16078 与 RAGEN 已在文本 agent 上提出）和检查点都是现成的。新意在于把已有工具用到一个新的比较轴上，没有新机制，也没有针对 GUI 的结构性适配。迁移规则讲的是方法迁移，对一次测量审计只适用一部分，所以给 6.5，不给 7。 |
| 有效性（先验合理性） | 5.5 | **支持的部分**：检测器有人工验证和双 judge 一致性（judge 是本地 Qwen3.6-27B 与 Gemma），UI-TARS-1.5-7B 能作为复现锚点，四个后代的基座都已核实。**直接反证**：Inertia 原文明确写道，承认失败变少时惯性率会下降，即使重复本身没有减少，并报告 EvoCUA 在 Permanent Reset 下惯性率降了、重复反而升了。作者自己的预检里，GUI-Owl 的 RL 轨迹中新鲜承认失败只有约 1%。主指标 1 是"重复且承认"的合取，按每执行动作计，正好落在这个失效方式上；它也不是 knowing-doing gap 本身（那应是 P(重复 \| 已承认失败)）。分母同样有混杂：RL 后代成功率更高，失败轨迹会跑满 50 步。**因果隔离不成立**：SEAgent-1.0 是先用 3.5K 条专家轨迹做 SFT 蒸馏、再做 RL，奖励还显式惩罚冗余循环，它的方向在设计上就已决定；ZeroGUI 带测试时训练。ARPO 训练与评测都是 15 步，DART 评测 30 步，统一用 50 步、固定历史长度，会把后代推出各自的训练分布，"RL 效应"和"评测配置偏移"分不开。离线指标 2 的对数概率差跨检查点比较，会受 RL 后分布更尖锐的影响，需要校准。 |
| 待预研 | — | 四对的方向与效应量；离线纠错增益与在线惯性率是否一致；成功率提升与惯性变化的相关强度。这些不计入分数。 |

**与原问题的关系**：这项工作回答原问题里"训练侧来源"的 RL 一支（属于子问题）。推理与动作在哪里断开、SFT 阶段的作用、冲突指令下的终止、恢复修法仍未回答。转向本身不扣分，扣分的是这个子问题自身的分量。

**实验能否判别主张**：目前不能。原因有四：
- 主指标 1 无法区分"重复减少"和"承认失败减少"。
- 每执行动作的分母混入了成功率与轨迹长度。
- SEAgent 一对混入了 SFT，奖励又惩罚冗余，"≥3/4 同号"的规则因此不只反映 RL。
- 4 对来自 2 个初始化，样本不独立，n=4 无法支撑配方元素归因。

另外，"ARPO、SEAgent、ZeroGUI 只报告成功率"的定位不准确：SEAgent 在奖励里显式处理了冗余步。作者引用的 Inertia 结论"四个模型 55–89%"实为四个中的三个。AgentNet 预检里的"3,832 步"与 Inertia 表 4 中 UI-TARS-1.5-7B 在 OpenComputer 上的重复动作数完全相同，需核实是否混用了数据。

**可行性：pass。**
- 6 个检查点均在 HF 上存在：ARPO_UITARS1.5_7B、PengxiangLi/dart-gui-7b（base_model 为 UI-TARS-1.5-7B，论文 2509.23866 也写明以它为基线）、Zery/SEAgent-1.0-7B 与 OpenGVLab/ZeroGUI-OSWorld-7B（base 均为 UI-TARS-7B-DPO）。
- Inertia 的代码与 judge 协议公开，judge 可在本地 GPU 上跑，API 费用接近 0。
- vLLM 在 8×A100 上做推理 2–3 天可行。
- 云费用估低了：OSWorld 的 AWS provider 默认实例是 t3.xlarge（约 $0.166/h），1,100 实例小时约 $185，合约 1,300 元，超出 1000 元。按预案降到每检查点 1 次运行（约 650 元），或改用本地 KVM，仍在约束内。
- 标签含义一致：重复由截图核验，承认失败由仅看推理文本的 judge 判定。

## 最高近邻

1. **Absorbed in Inertia: Activation Analysis for Computer-Use Agents**（arXiv:2609.37176）https://arxiv.org/abs/2609.37176
   - 重叠：定义并测量惯性，测了 UI-TARS-1.5-7B 等 4 个模型，提出 R³ 修法。
   - 差别：比较的是不同家族的模型，没有同初始化的训练阶段对照；原文已警告惯性率会受承认失败频率影响。
2. **LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities**（arXiv:2504.16078）https://arxiv.org/abs/2504.16078
   - 重叠：发现 RL 微调能部分缩小 knowing-doing gap。
   - 差别：环境是文本 bandit 与井字棋，非 GUI，也没有截图核验。
3. **RAGEN**（arXiv:2504.20073）https://arxiv.org/abs/2504.20073
   - 重叠：多轮 RL 中出现 Echo Trap，即推理坍缩、重复。
   - 差别：文本小环境，没有 GUI 屏幕–动作重复。
4. **SEAgent**（arXiv:2508.04700）https://arxiv.org/abs/2508.04700
   - 重叠：在 UI-TARS-7B-DPO 上训练，奖励模型显式标注冗余循环。
   - 差别：没有测承认失败后的重复率；最终模型含 SFT 蒸馏。
5. **Say One Thing, Do Another?**（arXiv:2510.02204）https://arxiv.org/abs/2510.02204
   - 重叠：诊断移动端 agent 的推理–执行 gap。
   - 差别：离线逐步对齐（GTA/EM），摘要中没有训练阶段对照，也没有在线重复。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 6.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是用 Inertia 公开检测器在 2 个初始化、4 个公开 RL 后代上测在线 GUI RL 对'承认失败后仍重复'的效应方向。GUI 上未见同初始化前后对照（新颖度 6.5），但工具、问题和检查点都是现成的，且仅为描述性结论，n=4 无法做配方归因（重要性 6）。有效性 5.5：主指标 1 是重复与承认失败的合取并按每动作计，Inertia 原文已指出承认失败变少会让惯性率下降而重复不变，作者预检中 RL 轨迹的新鲜承认失败也只有约 1%，这是直接适用的反证；分母混入了成功率与轨迹长度；SEAgent 含 SFT 蒸馏且奖励惩罚冗余，ZeroGUI 含测试时训练；ARPO 与 DART 训练和评测为 15 或 30 步，统一 50 步与固定历史长度会造成配置偏移。效应方向与大小待预研。",
  "feasibility": "pass",
  "feasibility_reason": "6 个检查点在 HF 上均已核实（DART-GUI base_model 为 UI-TARS-1.5-7B）；Inertia 代码与 judge 协议公开，judge 可本地运行；8×A100 推理 2-3 天可行。OSWorld AWS 默认实例 t3.xlarge，1,100 实例小时约 1,300 元，超出预算，但降到每检查点 1 次运行或使用本地 KVM 后可控制在 1000 元内。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献分量不足：三项都没有达到 8，主贡献是 4 个异质公开检查点上的描述性方向判断，n=4 无法支撑配方元素归因",
    "Claim 阻断：主指标 1（重复且承认失败的合取，按每执行动作计）会因 RL 改变承认失败频率或成功率与轨迹长度而变化，Inertia 原文已记录这一失效方式，实验无法区分'重复减少'和'承认失败减少'",
    "Claim 阻断：比较对象没有隔离 RL 这一步。SEAgent-1.0 为 SFT 蒸馏加 RL，奖励显式惩罚冗余循环；ZeroGUI 含测试时训练；统一 50 步与固定历史长度偏离了 ARPO（15 步）和 DART（30 步）的训练与评测配置",
    "定位不准确：'ARPO/SEAgent/ZeroGUI 只报告成功率'忽略了 SEAgent 奖励中对冗余步的显式处理"
  ],
  "novelty_conclusion": "检索未见 GUI 领域用同初始化 RL 前后对照测惯性或 knowing-doing gap 的工作，问题设定有可辨认的增量；但测量工具、问题和检查点都是现成的，属于测量审计层面的新意，没有新机制。",
  "closest_neighbors": [
    "Absorbed in Inertia: Activation Analysis for Computer-Use Agents (arXiv:2609.37176)",
    "LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities (arXiv:2504.16078)",
    "RAGEN: Understanding Self-Evolution in LLM Agents via Multi-Turn RL (arXiv:2504.20073)",
    "SEAgent: Self-Evolving Computer Use Agent with Autonomous Learning from Experience (arXiv:2508.04700)",
    "Say One Thing, Do Another? Diagnosing Reasoning-Execution Gaps in VLM-Powered Mobile-Use Agents (arXiv:2510.02204)"
  ]
}
```
