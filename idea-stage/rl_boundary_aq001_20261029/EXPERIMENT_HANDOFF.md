# 实验交接：多轮 agent 中保覆盖方法作用于哪里

完整方案见 [FINAL_IDEA.md](FINAL_IDEA.md)。本文件只列下游实验需要的内容。

## 定位关键词

multi-turn agent RL；pass@k coverage；diversity collapse；checkpoint handoff；forward KL；replay；WebShop；ALFWorld

## 问题

多轮工具 agent 的 GRPO 常在大 k 采样下丢失可解任务覆盖。现有保覆盖方法分两类：
- 在单轮上提出的：DPH-RL、TAR、入口修复；
- 在多轮上提出、但只在任务级或第一轮操作的：PTGS、DivInit。

它们在多轮轨迹中作用于哪里、能找回多少覆盖，尚无检验。

## 主 Claim

为每个保覆盖训练方法定义唯一的推理期“基座接管”对应物。对应物增益 P_m(i) 在同一任务内、跨方法预测该方法相对 GRPO 的 pass@16 增益 Δ_m(i)。

检验用回归 Δ_m(i) = α_i + γ_m + b·P_m(i)，配合任务内置换、自身对应物优于他人、成对差分三项检验；预测 b > 0。

## 方法要点

- **B / G**：B 为 Qwen2.5-7B 起点（ALFWorld 视门槛可改用 Instruct 版）；G 为从 B 只做 GRPO 的检查点。
- **逐轮替换剖面 L(t)**：在真实环境中只把第 t 轮换成 B 生成，扣除同模型分叉的噪声底。
- **六个对应物**：

  | 训练方法 | 对应物 |
  |---|---|
  | 入口前向 KL | B 接管第 1 轮 |
  | DPH-RL | 共享状态上由 B 接管 |
  | TAR | 共享状态且被抑制时由 B 接管，门控粒度须与 TAR 的轨迹平均 b(τ) 对齐 |
  | PTGS | 推理期 PTGS |
  | 剖面选轮前向 KL | B 接管 S（S 在开发任务上选出） |
  | 随机选轮前向 KL | B 接管同数量的随机轮 |

- **处方**：S 上的前向 KL（DPH-RL 损失加轮掩码）。

## 最小实验与顺序

1. **阶段 0（约 1 天）**：两个环境各训 1 个 GRPO 种子。门槛（规律面板上）：pass@32 至少低 5 个百分点，且 ≥60 个“B 有成功、G 全失败”任务；不满足则停止并报告负结果。
2. **阶段 A（约 3.9 天）**：
   - 规律面板（WebShop 800 / ALFWorld 274 个训练划分任务）：剖面加六个对应物；
   - 留出任务：对应物加 G、B；
   - 报告状态匹配率与对应物相关矩阵；
   - 用 GRPO 3 个种子做功效分析，预注册最小可检出效应与退化情形的等价界。
3. **阶段 B（约 12 天训练 + 5.5 天评测）**：
   - WebShop 七组：GRPO、入口前向 KL、DPH-RL、TAR、PTGS、剖面选轮、随机选轮；
   - ALFWorld 四组：GRPO、入口前向 KL、TAR、剖面选轮；
   - 每组 3 个种子，超参在开发任务上 2 选 1。

## Baselines（同领域、同任务、已核验）

| Baseline | 仓库（HEAD） | 入口 |
|---|---|---|
| GRPO | https://github.com/langfengQ/verl-agent （20bd331） | `examples/grpo_trainer/run_webshop.sh`、`run_alfworld.sh` |
| DPH-RL / 入口 / 剖面 / 随机前向 KL | https://github.com/seamoke/DPH-RL （fea6990） | `scripts/llama/{offline_sampling,forward_kl}.sh`，移植为按动作 token 与轮掩码的离线 NLL |
| TAR | https://github.com/wenzhilics/tar （0b7d515） | `recipe/tar/build_memory_bank.py`；`compute_tar_weights`、`compute_tar_loss`、`_backward_tar_loss` |
| PTGS / WebShop harness | https://github.com/changdaeoh/sharpening-tax （789ae06） | `ptgs/integration.py` 的 `PTGSHooks`；`sharpening_tax/benchmarks/webshop.py`（`WEBSHOP_ENV_SEED`） |
| 交接实现参考 | https://github.com/Xuanxuana1/AgenticRL_Handoff （64ebd4a） | `src/handoff/alfworld/{environment,rollout}.py`（SkillRL 封装，需在 verl-agent 中重写） |

**控制变量**：同一环境内组大小、训练步数、学习率、rollout 预算一致；前向 KL 与回放组用同一批离线基座成功样本；所有组 3 个种子。

## 需要用户确认的参数

按项目约定，以下参数未定，开跑前需确认：
- GRPO 组大小与训练步数；
- 各散度系数的两个候选值；
- 退化情形的等价界（建议 ±2 个百分点 pass@16）；
- 最小可检出效应目标（建议 b = 0.3）。

## 算力与数据

- 8×A100 80G，无付费 API。
- 合计约 22 天，慢 30% 时约 28 天；阶段 0 与阶段 A 约 5 天可先行决定是否继续。
- 代码与数据在服务器上通过 ssh 开发，不存本地。

## 主要参考

Sharpening Tax（2610.01509）；Locked at the Entrance（2608.29188）；DPH-RL（2509.07430）；TAR（2610.24236）；Reach or Solve（2609.19636）；The Replay Gap（2608.08239）；PBA（2607.20543）；Coverage, Not Targeting（2609.02417）；ReOPD（2607.04763）；PASS@(k,T)（2604.14877）。

## 剩余风险

见 [FINAL_IDEA.md](FINAL_IDEA.md) 第 5 节与 [../../review-stage/rl_boundary_aq001_20261029/FINAL_REVIEW.md](../../review-stage/rl_boundary_aq001_20261029/FINAL_REVIEW.md)。最需要先确认的两项：
1. 阶段 0 中纯 GRPO 是否真的产生锐化税；
2. 阶段 A 的功效分析是否足以检出 b。
