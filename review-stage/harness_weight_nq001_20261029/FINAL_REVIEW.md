# N-Q001 打磨终止评审

- 输入：`path-stage/LLM热门方向_算力适配_20261028` 的 N-Q001
- Reviewer 调用：1 / 6
- 终态：`rejected_no_viable_candidate`（用户在第 1 轮后决定换卡 A-Q001）

## 最好的已评审结果

- 候选：IDEA-002（增益能否内化取决于信息可取得性——观察有据的轨迹改写）
- 评分：4.0 / 10，`needs_rethink`
- Fatal blockers：
  1. 核心动作（把 H* 独有信息改写为 H0 下的取证动作后 SFT）已被 Harness-Zero（arXiv 2609.24974）覆盖；
  2. 缺少同领域、同基准、有公开实现的最高近邻 Harness-Zero 作为对照；
  3. Claim 1“现有方法内化不了看到的增益”与 Harness-Zero 在 AppWorld 上恢复 82.3% harness 独有行为的证据冲突，信息差解释已由 PSP 与 2610.11655 给出。

## Claim 判断（摘自 Call 1）

| Claim | 判断 |
|---|---|
| 现有内化方法在“看”的增益上失败，原因是 imitation gap | 已被覆盖，且与已知证据冲突 |
| 分界是信息在 H0 下能否由 agent 自己取得 | 部分重合，三类划分与分层检验未见先例 |
| 改写为取信息动作后训练能内化 | 大部分被覆盖 |

## 最高近邻

- Harness-Zero: Harness Distillation via Agent-as-Harness — https://arxiv.org/abs/2609.24974
- Harness Evolution Hits a Ceiling: When Weight Training Should Begin — https://arxiv.org/abs/2610.11655
- From Self-Distillation to Self-Practice（PSP）— https://arxiv.org/abs/2609.29051
- On-Policy Context Distillation（OPCD）— https://arxiv.org/abs/2602.12275
- Better than Your Teacher（LEAP）— https://arxiv.org/abs/2410.05434

## 未达门槛的原因

N-Q001 所在的“把 harness 增益内化进权重”方向在 2026 年 7–10 月已被密集覆盖（Harness-Zero、2610.11655、OPCD、SKALD、Skill-SD、D-OPCD、Co-Harness、Evo²、HASE）。剩余 available 候选自评为 5.8（IDEA-003）与 5.5（IDEA-006），继续送审大概率不过门槛。
