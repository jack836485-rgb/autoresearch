# 实验交接：开思考 OPSD 退化的按类因果分解

- 完整方案：`FINAL_IDEA.md`
- 审查记录：`review-stage/opsd_thinking_q001_20261028/FINAL_REVIEW.md`（Call 10 与 Call 11 均为 8.2，experiment_ready）

## 定位

- **定位关键词：** on-policy self-distillation；privileged information；thinking models；epistemic tokens；forward KL
- **问题：** OPSD 在训练时开思考（TH）会让思考模型准确率下降，长度方向却不定。主流的"认知抑制"解释同时预测两者，但它在 OPSD 的损失通道上从未被因果检验。

## Claim 与方法主旨

**分离假说：** 认知边际通道（认知 token 的总概率）承载长度方向，但不承载准确率退化。

1. **准确率。** 认知通道既不必要也不充分。
   - T1 只训练 $L_{\text{cond}}$，仍会复现退化。
   - T2 只训练剂量匹配后的 $L_{\text{marg}}$，不会造成退化。
   - 主结果在 Qwen3-1.7B 上，复现在 SmolLM3-3B 上。
2. **长度。** Full Trace 与 Answer Only 两种视图下，T2 都复现 T0u 的长度方向，以及至少一半的幅度；T1 则不能。
3. **（次要）** 两种轨迹开头都不含答案、长度相等，一种来自本题，一种来自他题。两者造成的退化相当。

**方法：**
- 前向 KL 按认知类精确分解，这是 DKD 式分解的推广；分别只训练其中一项。
- 剂量匹配：只看训练 rollout 上的 marker 统计来选 $w$。
- 操纵检查 M1、M2，加随机类对照 T3。
- 统计用两级 bootstrap：外层重采样种子，内层重采样题目。

## 最小实验

- **代码：** https://github.com/xiuyuz/opsd-reference-study。新增一个按类分解的损失函数。
- **配置：** 沿用仓库默认值。有效 batch 32、恒定学习率；损失温度 1.1、rollout 温度 1.1；LoRA 秩 64、α 128，作用于 7 个投影模块；教师冻结，开思考。
  - 步数：Qwen3-1.7B 100 步，SmolLM3-3B 50 步。
  - TH 臂统一用 `ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024`。
- **训练臂：**
  - Qwen3-1.7B、Full Trace，共 37 次：T0 ×3；T0u、T1、T2 各 ×5；T3、T4 各 ×3；I-own、I-other 各 ×5；DR ×3。
  - Qwen3-1.7B、Answer Only，共 9 次：T0u、T1、T2 各 ×3。
  - SmolLM3-3B、Full Trace，共 9 次：T0u、T1、T2 各 ×3。
  - 合计 55 次，另有基座评测。
- **评测：**
  - 主评测：384 题冻结测试切分，开思考，Avg@4；同时记录 4k/8k/16k 前缀判分、平均长度、认知密度、停止 token 概率。
  - 外部基准（只作描述）：AIME24、AIME25、HMMT25，只评 4 个检查点。

## 事先检查（看主结果之前完成并固定）

1. 统计答案过滤后的保留率。低于 60% 时，把截取比例从 40% 降到 30%。
2. 每个模型先跑 T0 和 T0u 的种子 0：
   - 降幅不足原文一半时停止，并如实报告。Qwen3-1.7B 的原文降幅为 −7.4，SmolLM3-3B 为 −4.2。
   - 同时测两种视图下 T0u 的长度变化，判断主张二的前提是否成立。
   - 用种子 0 的方差估计功效；不足时把 T1、T2 加到 7 个种子。
3. 每个"模型 × 视图"组合，用最多 3 次短训练选定 $w\in\{1,10,100\}$。
4. 确定认知类 $E$、随机类和等价界 $\delta$ 的规则：
   - $E$ 与随机类在训练前固定；
   - $\delta=\max(1,0.25|\Delta T0u|)$，在 T0u 的全部种子跑完后确定。

## Baseline（核心参数全部相同）

| 名称 | 复现入口 |
|---|---|
| T0：TH 训练的 OPSD，官方截断目标 | `CONDITION=full_trace ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024 bash training/launch_run.sh` |
| Answer Only 视图 | 同上，改 `CONDITION=answer_only` |
| T4：marker 位置损失排除 | 同上，加 `EXTRA_ARGS="--fork-mask-mode exclude"` |
| DR 训练的 OPSD | `ROLLOUTS=direct` |
| 基座 | `evaluation/build_eval_queue.py --mode thinking` |
| SmolLM3-3B | 设置 `MODEL=HuggingFaceTB/SmolLM3-3B`，并使用 `data/splits/smollm3_3b_splits.json` |

## 算力与数据约束

- 训练约 93 A100 小时，含 $w$ 选择。
- 测试切分评测约 330 A100 小时，外部基准约 96 A100 小时。
- 合计约 520 A100 小时，2 张 A100 约 11 天。
- 数学题按规则判分，不需要付费 API。
- 按项目约定，代码和数据放在 ssh 服务器上，结果转存回本地。

## 开工前需要你确认的参数

1. **规模取舍。** 约 520 A100 小时，2 张 A100 约 11 天。两处可以削减：
   - SmolLM3 复现（省约 70 小时）；
   - 外部基准（省约 96 小时）。
   要不要先只跑 Qwen3-1.7B 的主张一和主张二？
2. **$w$ 的候选集。** {1, 10, 100} 是否合适？$L_{\text{marg}}$ 在 KL 中占比很小，可能需要更大的值。
3. **种子数。** 等价判定的臂用 5 个种子。若功效估计不足，是否同意加到 7 个（约多 30 A100 小时）？
4. **评测协议。** 主指标沿用 2609.20612 的测试切分 Avg@4。是否还要在 AIME 上用 avg@16 做主指标，以便与 2607.05184 直接对照？
5. **服务器。** 请提供 ssh 地址、可用 GPU 和环境。

## 参考文献

2609.20612；2607.05184；2609.39118；2607.10805；2603.24472；2607.02234；2608.04794；2608.09228；2608.18271；2203.08679；2609.20511；2601.18734。链接与角色见 `FINAL_IDEA.md` 的 References Used。

## 剩余风险

- 新颖性：分解方法来自 DKD；主张三是增量。
- "不必要"这一半已被 AD-OPSD 与 2603.24472 附录 H 部分预示。
- 长度前提可能不成立。
- 未截断的 T0u 可能不退化。
- 等价判定的统计功效可能不足。
- $L_{\text{marg}}$ 会连带改变停止 token 的质量。
- 剂量匹配可能放大副作用。

各项风险的早期检查方法见 `FINAL_IDEA.md` 第 5 节。
