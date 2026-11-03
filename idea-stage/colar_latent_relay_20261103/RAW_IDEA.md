# 原始想法（raw_idea）

## 用户原话（2026-11-03）

> 在小学数学应用题的隐式推理研究中，我们比较了算式版和自然语言版数据训练的 CoLaR，两类数据均源于 GSM8K-Aug。在 500 道 GSM8K 测试题中，长链最后两个 latent 平均获得全部 latent 注意力的 57.6% 和 46.7%。消融发现：链尾通常比链首敏感；单点置零影响小，联合置零却可能答错；最后三个置零后，仅约 10% 原本正确答案保留。并且生成 latent 向量跟前两个 latent Attention score 高度相关，让人感觉 latent cot 是一个特殊的 RNN。

## 已核对的服务器证据（L40LZX:/data/raid5/luzhenxing/colar，只读核对，未新跑 GPU）

- Checkpoint：EQ = `full_colar_gsm8k_aug_fixed_shift_all_valid_token_ce_clean_from_cot_gpu23/.../epoch38__step58773__monitor0.318.ckpt`（用户改进版 CoLaR，非官方权重）；NL = `gsm8k_aug_nl_colar_from_best_cot_gpu0/.../epoch23__step36096__monitor0.206.ckpt`。底座 Llama-3.2-1B-Instruct，CF=5，speed=5，每题一条随机链，答案贪心。
- 答案读取的注意力（`analysis/nl_vs_eq_tail_attention/report.md`）：长链（K≥8）最后两个 latent 占 latent 注意力 EQ 57.6%、NL 46.7%；它们只占答案全部注意力的约 7.5–11%（position 0 sink 吃掉约一半）。
- 链尾置零（`analysis/nl_vs_eq_staircase/report.md`）：原本正确的题，最后 1/2/3 个置零后仍正确 EQ 62.2%/26.6%/7.0%，NL 75.0%/40.2%/10.9%。单点置零多数保留，连续窗口置零在链尾处崩塌（如 EQ K=4 时 l3+l4 置零 23/62 保留）。
- 生成局部性（`analysis/latent_generation_locality/report.md`）：生成 z_t 的位置（t−1 行）对历史 latent 的注意力，t≥5 时最近 2/3 个占 EQ 80.5%/90.8%、NL 72.3%/80.9%，均匀基线 41.7%/62.6% 与 27.1%/40.7%；扣除自注意力后仍高于均匀基线。同题同步骤匹配后，EQ 与 NL 差距缩到约 2 个百分点。这些是注意力描述，不是因果分解。
- 同机其他方法的对照分析：Coconut（GPT-2，第三方复现权重 ModalityDance/latent-tts-coconut，固定 6 latent）答案行对 latent 的注意力并不集中在末尾；fixed 模式下干扰 first2 比 last2 更伤；l2/l5 的 logit lens 分别解码出第 1、2 步结果（约 2.5 个 latent 对应一步 CoT），propagate 模式下前 4 个 latent 的总效应远大于末 2 个。
- 离线重统计（本次，基于已有记录与 gold 算式，按数值匹配算依赖）：GSM8K-Aug 训练集中约 30% 的题含跨 ≥2 步的依赖；在 500 题 EQ/NL 记录里，固定步数后"含长依赖"与"仅局部依赖"的正确率没有一致差异（EQ 3 步 0.35 vs 0.34，4 步 0.16 vs 0.10）。即当前数据不支持"长依赖距离导致失败"。
- 平庸解释（需要排除）：GSM8K-Aug 的最后一条算式写着最终答案，其 token 长度在 CF5 下约占 2–3 个 latent。因此"答案读链尾、联合置零才崩"可能只是 latent 位置继承了监督 CoT 的版式。

## 问题锚点（Problem Anchor）

- **起点问题**：连续 latent CoT（以 CoLaR 为主）在 GSM8K 类数学应用题上，信息为何集中在链尾、生成为何近似只看最近 2–3 个 latent；这是 latent 推理特有的"接力式循环状态"机制，还是对监督 CoT 文本版式与局部依赖的继承？它对 latent CoT 的失败、方法设计或解释研究意味着什么？
- **对象与条件**：CoLaR（Llama-3.2-1B-Instruct，CF5，GSM8K-Aug 算式版与 NL 版）；可对照的 Coconut、CODI 等 latent CoT 家族；同底座显式 CoT。初始评测为 GSM8K 测试集（含 GSM-Hard、SVAMP、MultiArith 作外推）。
- **瓶颈与证据边界**：现有证据为单 checkpoint、单随机链、注意力描述加置零干预；EQ 与 NL 共享架构与数据来源，不能当成两个独立方法家族；置零是离流形干预；EQ checkpoint 是用户改进版而非官方权重。
- **用户约束**：预研可用 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G，单次最好不超过 5 天；token 资源稀缺；付费 API 1000 元以内可自主决定；目标是 2026-10 起半年内投主会。实验代码与数据放服务器，结果可回传本地。
- **非目标**：本 skill 内不启动训练或新的 GPU 干预；不把注意力占比直接当因果贡献；不把 NL/EQ 差异直接当数据形式的因果效应。
- **实验规划的成功条件**：得到一个经双审通过、主贡献明确、最小实验能判别 Claim 的 Idea，并交付 `EXPERIMENT_HANDOFF.md`。
