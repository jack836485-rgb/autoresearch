# A-Q001 打磨终审

- 输入：`path-stage/LLM热门方向_算力适配_20261028` 的 A-Q001
- 终态：`completed`（门槛通过）
- 通过的候选：IDEA-016（brief 见 `idea-stage/rl_boundary_aq001_20261029/round-14-brief.md`，复核用同一份 brief）
- Reviewer 调用：15 / 18（用户两次追加预算：6 → 8 → 18）

## 门槛结果

| 调用 | 角色 | 分数 | 结论 | fatal blockers |
|---|---|---|---|---|
| Call 14 | 首审 | 8.4 | experiment_ready | 无 |
| Call 15 | 复核 | 8.2 | experiment_ready | 无 |

## Claim 判断（两轮一致）

| Claim | 判断 |
|---|---|
| 1 按轮定位可找回覆盖 L(t) | 部分重合：Reach or Solve 交接、Replay Gap 分叉噪声底、Locked at the Entrance 入口定位在多轮 B↔GRPO 覆盖上的新用法，作为测量成立 |
| 2 测试时对应物在任务内预测训练方法增益（主贡献） | 新颖：未检索到预测训练方法覆盖增益的工作；任务固定效应、置换、自身优于他人、成对差分使其可推翻 |
| 3 剖面选轮前向 KL 优于同 token 占比随机选轮 | 部分重合：方法是 DPH-RL 加轮掩码，价值依赖 Claim 2；随机对照可推翻 |

## 最高近邻

- Sharpening Tax in Post-Training — https://arxiv.org/abs/2610.01509
- Reach or Solve? Checkpoint Handoffs — https://arxiv.org/abs/2609.19636
- Locked at the Entrance, Open Inside — https://arxiv.org/abs/2608.29188
- TAR — https://arxiv.org/abs/2610.24236
- PBA — https://arxiv.org/abs/2607.20543
- The Replay Gap — https://arxiv.org/abs/2608.08239
- PASS@(k,T) — https://arxiv.org/abs/2604.14877（相反方向证据）

## 剩余风险（两轮 reviewer 均列为非阻断）

1. “RL 会丢覆盖”的前提须写成条件句；阶段 0 门槛已使其可推翻。
2. TAR 对应物须与 TAR 的轨迹平均门控 b(τ) 加逐 token 软权重对齐粒度。
3. 退化推论（离线回放 ≈ 入口）是零差异预测，需预注册等价界并做等价检验。
4. ALFWorld 只有 3 个非 GRPO 方法且无随机选轮；WebShop 离线回放可能退化；识别变异偏薄，依赖阶段 A 的功效分析。
5. 任务级种子噪声；训练时长与吞吐估计偏乐观。
6. 第 3 条 Claim 中“应找回最多”不能由 Claim 2 直接推出，只能由随机选轮对照检验。

## 评审过程中的一处事实纠正

Call 13 判定“DPH-RL 仓库只有 README、TAR 缺 build_memory_bank.py、Handoff 缺 src/handoff”为 fatal blocker。主执行器以完整克隆复核（DPH-RL fea6990 共 675 个文件，TAR 0b7d515，Handoff 64ebd4a），三者文件均存在；Call 14 与 Call 15 独立复核后结论一致。该轮分数按规则照常记录，未推翻门控。
