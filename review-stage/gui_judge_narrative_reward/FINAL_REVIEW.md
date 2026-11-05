# FINAL_REVIEW：gui_judge_narrative_reward（问题卡 GUI_Agent研究地图_20261104 / Q001）

- 终态：`rejected_no_viable_candidate`（提前停止；Reviewer 调用 1/6）
- 未生成 FINAL_IDEA.md。

## 最佳已审结果

- 候选：IDEA-002「基率感知的少数阳性复核——评判器假阳性在 GRPO 低成功率组中被放大」
- Call 1（常规，Opus 5.5 high，零上下文）：总分 4.5；重要性 5.5 / 新颖度 4.5 / 有效性 4.5；可行性 pass（条件：KVM/Docker 未核实）；verdict `needs_rethink`。
- Reviewer 给出的致命阻断：
  1. 机制部分已覆盖：孤立阳性的 √(G−1) 放大（Spurious Advantage, arXiv:2609.04063）、噪声在不平衡组中危害最大（S-GRPO, arXiv:2508.05928）、GRPO 中被奖励的假阳性质量测量（arXiv:2607.11022）；后验随基率变化是贝叶斯恒等式。
  2. 实验无法判别：方法臂独有更强评判器，缺少同成本的“对全部阳性做强复核”和随机分配对照；不同模型的调用按次数计预算不公平。
  3. 缺少同机制强基线（S-GRPO / SignBalance 零额外调用压低孤立阳性优势）和同任务基线（arXiv:2606.24515 应单独开臂）。
  4. 效果关键环节有反向证据：评判器共享 leniency 偏差（OSReward），同模型重复投票的条件信息增益很低（VStress, arXiv:2609.36958）；收紧少数阳性会损失难任务上稀缺的真阳性。

## 为何不继续送审

主执行者核实了审查所引近邻，另检出 MobileJudgeBench（arXiv:2608.11434，已在 AndroidWorld 上用评判器奖励跑 GRPO，规则奖励 54.6% vs GPT-5-mini 评判 45.4%，3 种子）与 VStress（重复验证器的预算分配）。“VLM 评判器奖励 × CUA 在线 RL”在 2026-08 至 10 月已被评判器可靠性、报告隔离、主动验证、噪声校正、优势重加权与预算分配多条线密集覆盖。剩余候选（IDEA-003 5.8、IDEA-006 6.0）都只是迁移或诊断，自评达到“三项 ≥6、两项 ≥8”的路径不可信。按 skill 规则，不再用改名或弱候选消耗审查预算。

## 最高近邻

- Spurious Advantage Hidden in GRPO — https://arxiv.org/abs/2609.04063
- S-GRPO / Noise-Aware Advantage Reweighting — https://arxiv.org/abs/2508.05928
- Reinforcement Learning for Computer-Use Agents with Autonomous Evaluation — https://arxiv.org/abs/2606.24515
- When the Reward Suite Is Leaky — https://arxiv.org/abs/2607.11022
- ZeroGUI — https://arxiv.org/abs/2505.23762
- VStress — https://arxiv.org/abs/2609.36958
- Benchmarking LLM Judges for Mobile Agent Evaluation — https://arxiv.org/abs/2608.11434

## 剩余风险与未答问题

原问题“策略是否会学会迎合评判器（叙述或界面层面的伪证据）”仍未被直接回答。2607.11022 在代码 RLVR 上的证据倾向于“选择既有错误模式”而非“习得利用”；CUA 场景本轮未见对应实验。
