## 结论
2026-11-05，总体 score 5.0，verdict：promising_needs_revision。主贡献是两件事：在 7–8B 视觉 CUA 的真实惯性状态上测量“失败记录的纠错增益”并按通道（动作串、重复截图、失败承认）拆解，以及只用负信号的失败条件化 unlikelihood 训练。现在还不够，原因有三。第一，方法在推理时的等价物是“解码屏蔽失败动作”，这类做法和 R³ 都已经出现过“重复下降、任务成功不变”的反面信号，而 brief 没有给出权重内压制为何能把概率质量转给有用替代动作的依据。第二，近邻中已有只用负信号或不需奖励的同类训练（SEAgent 的负向模仿损失、CPL 的上下文偏好学习），新意因此是增量的。第三，诊断部分的主要结论（重复由上下文驱动）已被 Inertia 的清空历史实验大体揭示。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 惯性和恢复失败是开源 CUA 的真实瓶颈。但它在任务失败中的分量缺少支持：R³ 把惯性降低 17–55%，任务分不显著；FTB 的屏蔽把重复从 31% 降到 8%，成功率也不变。两者都说明“压掉重复”未必影响主要指标。新增的通道拆解（尤其截图是否构成独立复制通道）有认识价值，但影响范围有限。 |
| 新颖度 | 5.5 | 纠错增益的定义、表面形式和语义的拆解、改写与屏蔽，都直接沿用 FTB（2608.23651）；FTB 也把“能否训练掉”列为开放问题，所以本方案很大程度上是在补完那篇论文，再迁移到 VLM-CUA 上。训练侧有三个近邻：SEAgent 已在 OSWorld 上对失败动作施加只含负项的对抗模仿损失；CPL（2602.03664）已用自生成轨迹、无奖励地训练模型不去模仿长上下文中的先前动作；EvoCUA 已在失败后一步对“盲目继续”做 DPO 拒绝。剩下的新意是：以机械判定的“屏幕未变”作为负标签、不需要正确替代动作、加 KL 保持常规步骤，并测量截图通道。这些可以辨认，但都不是实质不同的机制。 |
| 有效性 | 4.5 | 现有依据：Welleck 等的 unlikelihood 能在文本中压低重复 token；FTB 在 ≤1.7B 文本模型上显示约 83% 来自表面形式；Inertia 显示清空历史后重复至多 4%（引自 brief，原文本次未能打开核验）。这些依据只支持 Claim (1)(2)，即“能降低 p(a_fail\|H_fail)”。Claim (3) 要求成功率不低于 R³ 和恢复 SFT，这一步缺少依据：unlikelihood 只把概率从 a_fail 移走，不指定质量流向；推理时屏蔽在效果上已经等价于把该项压到 0，而 FTB 中屏蔽并未提升成功率。brief 用来区分 R³ 的“保留完整进度上下文”同样适用于屏蔽，所以这一点不能说明训练会优于屏蔽。机械标签也有噪声：“屏幕未变”会包含延迟加载、需要双击、焦点或快捷键等不改变截图的正确动作，排除 wait 和滚动不足以覆盖这些情况。尚未验证的是：截图通道是否在 VLM 中成立、释放出的质量落到何处、合法重复的误伤率。 |

与起点的关系：本方案处理的是原问题“推理与动作在哪里断开”中的惯性子环节，给出的是表面复制通道的定位和针对它的修法。“训练侧来源”只部分回答（没有受控对比训练来源），指令冲突下的照做不在范围内。这一转向本身不构成阻断。

实验能否判别主张：Claim (1)(2) 可以判别。离线 teacher-forcing、通道替换和留出任务划分设计合理，“重建上下文下原动作的贪心复现率”也是必要的检查。Claim (3) 判别不足，原因有二。一是缺少同能力下的强竞争解释：没有 CPL（同样无奖励、自生成、训练侧压制上下文模仿）这个训练对照，也没有 Learning-from-Failure 式的重复警告 + 恢复模式、clip context 这类简单推理时基线，所以无法排除“任何压制模仿历史的训练都有同等效果”。二是“训练 vs 解码屏蔽”是方法相对 FTB 的唯一实质差别，却没有被设为主对比来解释收益来源。另外，每条件 2 次运行、约 185 个任务时，任务成功率的配对差置信区间会很宽，在 R³ 和 FTB 都显示效应小的前提下，“不低于”大概率得不到有信息量的结论。

可行性：pass（有条件）。诊断与训练路线可信：已核验 HF 数据集 `xlangai/ubuntu_osworld_verified_trajs` 含 `evocua_8b_20260105.zip`（5.86 GB）和 OpenCUA-7B 的 15/50/100 步三份 `action_history-3image` 轨迹；上下文重建有 OSWorld `mm_agents` 代码可依；LoRA 训练几千个状态在 8×A100 上数小时可完成；judge 费用在 1000 元以内。限制如下。在线评测依赖服务器 KVM（尚未确认），否则 Claim (3) 完全无法检验。R³ 的复现依赖匿名仓库的 patched OSWorld，原始 episode 没有发布。CUA-Recovery 的训练数据是否发布未核实（仓库页本次被权限拦截），不可得时 Claim (3) 的恢复 SFT 一半缺失。约 4,400 条 50 步在线 episode 需要几十个并行 VM，3–5 天偏紧。EvoCUA-8B 只有一次运行，检出状态数量未知。

## 最高近邻
- Feedback That Backfires（https://arxiv.org/abs/2608.23651）：已核验。它提出纠错增益、表面形式与语义的拆解、改写和解码屏蔽，屏蔽后任务成功不变，并把训练修法列为开放问题。差别在于它只用 ≤1.7B 文本模型，没有截图通道，也没有训练修法。
- Absorbed in Inertia（https://arxiv.org/abs/2609.37176）：需要检索（多次限流，未能读到原文）。按 brief 所述，它提出了惯性协议、steering 与清空历史的对比、R³，R³ 降低惯性但任务分不显著。差别在于它没有训练修法，也没有通道拆解。
- SEAgent（https://arxiv.org/abs/2508.04700）：已核验。它在 OSWorld 上对 World State Model 判定的失败动作施加只含负项的对抗模仿损失（γ=0.2 时有增益）。差别在于它需要学到的 judge 和 GRPO 正样本，也不专门针对惯性状态。
- Mitigating Conversational Inertia / CPL（https://arxiv.org/abs/2602.03664）：已核验。它用自生成轨迹、无奖励地做 DPO，压制长上下文导致的模仿先前动作，在 AgentGym 上有成功率增益。差别在于它是文本 agent，以上下文长度而非失败作为标签。
- VeriGUI / Don't Act Blindly（https://arxiv.org/abs/2604.05477）：已核验。它针对“屏幕未变却重复”的情况，用合成失败加纠正动作做 SFT 和 GRPO，报告 Loop Rate 和恢复成功率。差别在于它需要纠正标签和效果预测，评测在移动端。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 4.5},
  "contribution_assessment": "主贡献是把 FTB 的纠错增益和通道拆解迁移到 7-8B 视觉 CUA 的真实惯性状态，并用失败条件化 unlikelihood 在权重中压制失败动作的复制。重要性有限：R³ 与解码屏蔽都显示压低重复后任务成功不变，惯性在失败中的分量未获支持。新颖度是增量的：SEAgent 已有负向模仿损失，CPL 已有无奖励的反上下文模仿训练，FTB 已把训练修法列为开放问题。有效性只支持“能降 p(a_fail|H_fail)”；方法在推理时等价于解码屏蔽，而屏蔽已被观察到不提升成功率，概率质量流向有用动作缺少机制依据；机械标签会误伤延迟加载、双击等合法重复。待验证：截图通道是否独立、训练相对屏蔽的增量、在线成功率。",
  "feasibility": "pass",
  "feasibility_reason": "轨迹数据已在 HF 核验（EvoCUA-8B 一次运行、OpenCUA-7B 三次运行），上下文可按 mm_agents 重建，LoRA 训练和 judge 费用在约束内。在线评测依赖未确认的 KVM 和 patched OSWorld，CUA-Recovery 训练数据未核实，任一缺失时 Claim (3) 不可测或只能部分测试。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "有效性阻断：Claim (3) 缺少依据。方法在推理时等价于解码屏蔽失败动作，FTB 的屏蔽和 Inertia 的 R³ 都显示压低重复后任务成功不变；brief 没有说明 unlikelihood 释放的概率质量为何会流向有用替代动作，也没有说明权重内压制相对屏蔽的增益来源。",
    "新颖度阻断：主要是 FTB（2608.23651）开放问题的补完与迁移。训练侧与 SEAgent 的负向模仿损失、CPL 的无奖励反上下文模仿训练重叠，去掉 FTB 后剩余新意是增量的。",
    "Claim 阻断：缺少同能力强对照。没有 CPL 式训练基线，也没有重复警告、clip context 这类推理时基线，“训练 vs 解码屏蔽”也未作为主对比，无法排除竞争解释；每条件 2 次、约 185 任务不足以判别“成功率不低于 R³”。",
    "重要性限定：没有依据表明惯性是任务失败中分量足够的环节，诊断主结论（重复由上下文驱动）已被 Inertia 的清空历史实验大体揭示。"
  ],
  "novelty_conclusion": "增量。纠错增益与通道拆解来自 FTB；负信号训练已有 SEAgent（负向模仿损失）和 CPL（无奖励反上下文模仿）。新的部分是 VLM-CUA 上的截图通道测量，以及以“屏幕未变”为唯一标签、加 KL 保持常规步骤的组合，不构成实质不同的机制。",
  "closest_neighbors": [
    "Feedback That Backfires: Why Small Language Model Agents Repeat the Call They Just Watched Fail (arXiv:2608.23651)",
    "Absorbed in Inertia: Activation Analysis for Computer-Use Agents (arXiv:2609.37176) — needs_search（原文未能读取）",
    "SEAgent: Self-Evolving Computer Use Agent with Autonomous Learning from Experience (arXiv:2508.04700)",
    "Mitigating Conversational Inertia in Multi-Turn Agents (arXiv:2602.03664)",
    "Don't Act Blindly: Robust GUI Automation via Action-Effect Verification and Self-Correction (arXiv:2604.05477)"
  ]
}
```
