## 背景

**定位关键词：** asynchronous reinforcement learning；training-inference mismatch；policy staleness；decoupled PPO；score centering；importance sampling

**一句话定位：** 在异步 LLM agentic RL 的离策略校正中，训练端在 rollout 生成版本上的概率（old logits）常缺失；已有工作报告精确 old logits 能显著改善训练，但这份收益由什么机制带来、能否在不保存历史权重时获得，尚未在真实异步设置中受控检验。

**与起点问题的关系：** 子问题。保留对象（缺 old logits 时的异步离策略校正）、条件（异步、部分 rollout、多轮工具任务、稠密与 MoE）与评价目标（训练稳定性与任务成功率）；把"如何恢复 old logits"改为"什么时候需要 old logits、其收益来自哪一机制"。起点问题中的系统审计（哪些声称无损的系统未保留 old logits）不在本 Idea 内；阈值耦合导致后期崩溃的机理通过"偏差漂移"这一候选机制部分检验。

## 核心 Claim

**主贡献（现象／视角）：** 给出一个在真实异步 agentic RL 中可检验的归因：精确 old logits 相对常用代理的收益，主要来自两个可分别获得的机制——(a) 信任域参考放在 token 的生成版本上，使策略滞后进入被裁剪的比率；(b) 去掉训练–推理数值偏差带来的漂移（逐前缀的持续偏置）。(a) 用已记录的推理端概率作裁剪参考即可得到，(b) 用逐前缀的 score centering 即可得到，两者都不需要 old logits；只有当数值偏差的尾部跨过裁剪尺度时，精确的偏差–滞后分解才额外有益。若成立，异步系统可以不为快照、专用 old-logit 模型或 EWMA 参考付出系统代价，并能按偏差规模判断何时值得付。

**可推翻的判断：**
1. 偏差很小的稠密 BF16 设置中，"推理端概率作参考"与"精确 old logits"处于同一噪声带，两者都明显优于 2605.12070 所用的中间版本代理；若精确 old logits 仍显著更好，则 (a) 不足以解释其收益。
2. 偏差大的 MoE（不做路由回放）设置中，"推理端概率作参考 + score centering"与"精确 old logits + 漂移去除（DLC）"处于同一噪声带；若后者显著更好，则给出"需要 old logits"的明确条件，主张 (b) 被推翻。

**当前依据与适用条件：**
- 2605.12070（异步 agentic RL，ROLL，Qwen3-4B 与 30B-A3B，最大版本差 3）在同一掩码框架下比较精确 Snapshot 与代理，30B-A3B 的 VitaBench in-store 从 18.28 到 34.62。但其 "Decoupled PPO & Async" 的两个因子都以一个介于 old 与当前之间的可用版本为参考（Table 1），所以与 Snapshot 相比同时改变了参考位置和偏差处理，表中没有"推理端概率作参考"或中心化的对照。
- 2610.40945 用训练端在采样权重上的前向精确拆分误差，并分析了参考位置：参考取批次前训练端时，滞后落在比率外，PPO 在陈旧采样器下偏离 on-policy 达噪声底的 699 倍；参考取采样权重时，滞后在比率内。其 Table 2（Qwen3-0.6B，Countdown）在"量化 + 陈旧"下，不需 old logits 的"IS + 中心化"为 2.61 倍、准确率 30.5，需 old logits 的 DLC 为 2.17 倍、30.3。
- 2609.20807（0.6B–30B）认为训练–推理偏差导致的不稳定主要来自漂移，score centering 在量化下匹配或优于 IS，且可与 IS 组合处理陈旧度。
- 仍未知：上述两篇的结论来自短训练（40 步）、固定在 $\theta_0$ 的陈旧采样器、SGD 大学习率、单轮任务，是否迁移到连续版本流、Adam 小学习率、部分 rollout 跨版本、多轮工具调用与 MoE 路由偏差；MoE 路由翻转造成的偏差可能是重尾的，可能正是需要精确分解的情形。本 Idea 的价值依据是这些机制论证与 2605.12070 比较设计的混杂，而不是已测得的结果。

## 方法设计的核心思想

- **输入**：AReaL 异步训练中的轨迹，含逐 token 生成版本、推理端 logprob 与推理端 top-k head（score centering 所需）。
- **动作**：在完全相同的数据、超参与陈旧度下，只改变离策略校正的两个设计维度——裁剪参考放在哪里（中间可用版本 / 推理端已记录概率 / 精确 old logits）与偏差如何处理（掩码 / 中心化 / 不处理），并在偏差小与偏差大两种设置下比较。用对同步 on-policy 训练的偏离度作主指标，使少量种子也能区分。
- **输出**：精确 old logits 收益的机制归因、零历史权重组合与精确分解的差距，以及"需要 old logits"的条件。
- **与最高近邻的关键差别**：2605.12070 只比较 old logits 的不同获取方式，未拆分参考位置与偏差处理；2610.40945 给出了分解与参考位置理论，但实验限于小稠密模型、单轮、固定陈旧采样器、40 步；2609.20807 主要研究量化偏差。本 Idea 把三者的机制放到真实异步 agentic 设置中做受控拆分。

## 最小实验

- **设置**：AReaL 异步 Search-R1（公开 NQ+HotpotQA 训练集与 e5 检索器，AReaL `search_agent` 工作流），最大版本差 4，部分 rollout 开启，组大小、学习率、批次与阈值各臂一致。两种偏差规模：R1 稠密 Qwen3-4B，BF16 推理（偏差小）；R2 Moonlight-16B-A3B，BF16 推理、不做路由回放（偏差大；沿用 AReaL `examples/r3` 单机 4 卡推理 + 4 卡训练，关闭 `return_routed_experts` 与 `enable_router_replay`）。各 120 步。
- **五个校正臂（同一 PPO 裁剪 ε、同一偏差阈值）：**
  - A. 中间版本代理（2605.12070 的 Decoupled PPO）：AReaL 已核验实现 `use_decoupled_loss` + `prox_logp_method=recompute`。
  - B. 推理端概率作裁剪参考，不处理偏差：标准设置（verl fully-async 默认的 rollout logprob 作 old）。
  - C. B + 中心化（零历史权重的 DLC）：与 E 用同一 DLC 估计式（2610.40945 Eq. 6），只把分母 $p_{old}$ 换成已记录的推理端概率 $q_v$：裁剪 $p_\theta/q_v$，中心化项用采样端 top-k head 与 $p_\theta$ head。C 与 E 只差这一个分母。中心化的 head 收集与 tail 估计复用 AReaL 已核验的 score centering 代码路径（`areal/utils/score_centering.py`，其自带的 REINFORCE+截断 IS 形式作为补充参考，不作主对照）。
  - D. 精确 old logits + 2605.12070 解耦掩码：按其 §5.1 独立实现 Snapshot（CPU 保留最近 4 个版本权重，按逐 token 版本分组做训练端前向），目标按其 Eq. 4。
  - E. 精确 old logits + DLC：按 2610.40945 §7.1 与附录 L 独立实现（裁剪 $p_\theta/p_{old}$，用采样端 head 与 $p_{old}$ head 中心化）；重同步规则因 AReaL 每步同步而不启用，并说明这一改动。
- **参考与指标**：每种设置跑 2 次同步 on-policy 训练，作为偏离度的基准与噪声底（沿用 2610.40945 的定义：在固定 held-out 前缀上对 on-policy 模型的全词表 KL，除以两次 on-policy 训练间 KL）。在第 40、80、120 步测偏离度；同时报 7 个 QA 测试集 EM、活跃 token 比例、每步额外耗时与内存。各臂 1 个种子；R2 中 C 与 E 各补 1 个种子。
- **支持主张的结果**：R1 中 B 与 D 的偏离度之差小于两次 on-policy 间的噪声，且都明显低于 A；R2 中 C 与 E 之差在其两种子的散布内，B 与 D 明显差于 C。**推翻**：R1 中 D 显著优于 B，或 R2 中 E 显著优于 C。
- **关键数据可得性**：逐 token `versions`、推理端 `logprobs` 与采样端 head（`parse_sampler_heads`）在 AReaL 代码中已核验；score centering 要求温度 1、无 top-p/top-k（`validate_sampling`），各臂统一采用。Snapshot 的历史权重可由训练端每步保存。
- **成本**：R1 共 7 次运行 × 约 4 小时；R2 共 9 次运行 × 约 9 小时；合计约 4.5 天（8×A100），步时为估计，先用 R1 两臂实测修正；不需要付费 API。R2 的 Snapshot 臂驻留约 128 GB 主机内存，开跑前按共享机器内存余量规则确认。
