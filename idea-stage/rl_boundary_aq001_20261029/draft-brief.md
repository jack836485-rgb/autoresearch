## 背景

**定位关键词：** agentic RL；sharpening tax；pass@k；checkpoint handoff；reach and solve；exploration；WebShop；BFCL

**一句话定位：** 多轮工具使用 agent 的后训练（以 RL 为主）为什么在一些基准上缩小大 k 采样下的可解任务覆盖（锐化税），在另一些基准上扩大覆盖，以及能否只保留它的好处。

## 核心 Claim

1. **扩展与锐化的矛盾不只来自配方，同一对检查点在不同基准上方向相反。** Sharpening Tax（arXiv 2610.01509）在 14 对发布的基座 / 后训练检查点上发现后训练普遍缩小大 k 覆盖，并报告全局调温度不能化解准确率与覆盖的矛盾；Pass@(k,T)（arXiv 2604.14877）在受控工具 RL 上看到大 k 扩展。用 Sharpening Tax 公开的逐任务结果（每任务 128 次 rollout）按 pass@k 无偏估计计算：Qwen2.5-7B 的后训练版在 BFCL v4 multi-turn 上 pass@128 比基座高 38.0 个百分点，在 WebShop 上低 14.4；Ministral-3-8B 分别为高 10.5、低 24.2。
2. **多轮 agent 的覆盖变化应拆成“到达可解状态”与“从该状态完成”两段，锐化税付在到达段。** 后训练提高从给定状态完成任务的能力，却让早期几轮的分支选择（如 WebShop 的搜索词与翻页）塌缩，使大 k 采样走不到那些罕见但可解的路径。任务成败主要卡在早期探索时表现为锐化税，主要卡在执行时表现为扩展。Reach or Solve（arXiv 2609.19636）已用检查点交接在单次成功率上分离到达与完成，但没有在大 k 覆盖上做，也没有据此改变训练或解码。
3. **只在到达段保留多样性，就能同时得到后训练的单次准确率和基座的覆盖。** 预期：在 WebShop 上，“前 m 轮基座、其余轮后训练模型”的按轮交接解码，pass@128 不低于基座、pass@1 接近后训练模型，而反向交接恢复不了覆盖；在 BFCL 上覆盖增益主要来自完成段。训练时只在早期 m 轮锚定起始策略，在相同 pass@1 下比 PTGS 与全局提温付更少的税。若反向交接同样恢复覆盖，或覆盖损失在各轮均匀分布，则 Claim 2 被推翻。

## 方法设计的核心思想

**诊断（只需推理）**：对一对基座 B / 后训练 R 检查点，在可确定回放的环境里做四种按轮交接：B→B、B→R、R→B、R→R。前 m 轮由前一个策略生成，然后把这段历史原样回放到环境，交给后一个策略继续。对每种组合、每个 m 画 pass@k 曲线（k 至 64 或 128），并按任务统计覆盖从哪一段丢失。另记录早期轮的分支多样性（不同首轮动作与搜索词的数量），检验它与逐任务锐化税的关系。

**修法 1（测试时）**：按轮交接解码。前 m 轮用基座或更高温度采样，之后切换到后训练模型；m 由诊断给出。

**修法 2（训练时）**：早期轮锚定 GRPO。只在每条轨迹的前 m 轮对起始策略加 KL 约束（或提高这几轮的采样温度），其余轮照常优化。

**与最高近邻的关键差别**：
- Sharpening Tax 的诊断与修法都在任务级（逐任务锐化税、按任务路由、按题设温度的 PTGS）；
- Reach or Solve 只在 pass@1 上拆分到达与完成；
- EAD（arXiv 2510.05251）在单轮生成里做 token 级“先高温后低温”。

本方法在多轮轨迹内部按轮定位覆盖损失，并只在被定位的那一段干预。

## 最小实验

**阶段 A：诊断，不训练。**
- 检查点：Sharpening Tax 已发布的 ≤9B 对，即 Qwen3.5-4B、Qwen3.5-9B、Qwen2.5-7B（基座 / 后训练）。
- 基准：WebShop（取 200 个任务）与 BFCL v4 multi-turn base（200 个任务）。上面的计算已确认在这些检查点和基准上存在方向相反的覆盖变化。
- 设置：沿用 Sharpening Tax 的轻量文本 harness 与评分；交接点 m ∈ {1, 3}；每组合 64 次 rollout。B→B、R→R 的 128 次 rollout 结果可直接复用公开数据。
- 对照：B→B、R→R；按任务路由（Sharpening Tax 附录 D.4，用 8 次 rollout 估计逐任务税后选模型）；R 加全局高温采样。

**阶段 B：训练，从同一起点只隔离 RL。**
- 起点：Qwen2.5-7B-Instruct（verl-agent 的 WebShop 标准设置）。
- 在 WebShop 上训练三组：GRPO、GRPO+PTGS、GRPO+早期轮锚定。组大小、步数、学习率、rollout 预算相同，2 个训练种子。
- 统一用 Sharpening Tax harness 评测 pass@1 与 pass@128。

**支持 / 推翻 Claim 的结果**：
- 支持：WebShop 上 B→R 的 pass@128 ≥ B→B 且 pass@1 接近 R→R，而 R→B 不恢复覆盖；BFCL 上覆盖增益随交接点后移而保持，说明来自完成段；早期轮锚定在 pass@1 不低于 GRPO 时，pass@128 高于 GRPO 与 GRPO+PTGS。
- 推翻：R→B 与 B→R 同样恢复覆盖；或覆盖损失不随交接点集中；或早期轮锚定不优于 PTGS。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| Sharpening Tax harness、逐任务结果、按任务路由 | 同基准、同检查点的锐化税测量 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（2026-10-02；`sharpening_tax/benchmarks/{webshop,bfcl}.py`、`sharpening_tax/metrics.py`、`data/outcomes_42cells.csv.gz`；BFCL 依赖 gorilla@6ea5797） |
| PTGS | 同基准上为降低锐化税而设计的 RL 采样方法 | 同上 | 同仓库 `ptgs/integration.py` 的 `PTGSHooks`，接入 GRPO 的组采样温度 |
| GRPO（WebShop） | 多轮 agent RL 的标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`） |
| 检查点交接 | 拆分到达与完成的评测协议 | https://arxiv.org/abs/2609.19636 | 论文未见代码；协议为“回放前一策略的前 m 轮动作再交给后一策略”，在 WebShop（`env.reset(session=goal_idx)` 后按序回放）与 BFCL（有状态 API 实例按序重放调用）上可直接本地实现 |
| 环境 | — | WebShop、BFCL v4 | WebShop 随 verl-agent 与 Sharpening Tax harness 提供；https://github.com/ShishirPatil/gorilla（`berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_multi_turn_base.json`） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 A：3 对检查点 × 400 个任务 × 2 种交接 × 2 个交接点 × 64 次 rollout ≈ 30.7 万条轨迹，每条约 8 轮、生成约 1.6k token，vLLM 推理约 1 天。
- 阶段 B 训练：3 组 × 2 种子 = 6 次，每次约 8 卡 × 12 小时，约 3 天。
- 阶段 B 评测：6 个模型 × 500 个任务 × 128 次 rollout，约 1 天。
- 合计约 5 天；API 费用为 0。阶段 A 约 1 天即可给出 go/no-go。
