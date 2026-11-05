## 背景

**定位关键词：** emergent misalignment；conditional misalignment；chat template tokens；KV cache patching；in-training defense

**一句话定位：** Dubiński 等（2604.25891）发现，交织良性数据、inoculation 等缓解手段会把 EM 藏到情境触发后面，而不是去掉它。此后出现了两类有机制依据的新防御，但都只在无 cue 题上评测过：
- 只约束模板 prefix 位置 K/V 的训练中防御 TReFT（Piggyback，2606.06667，NeurIPS 2026）；
- 在基座的提示缓存上用微调模型解码，Loos & Eberle（2610.41480）把它作为降低 EM 的部署手段提出。

本 Idea 检验这两类防御是去掉了 EM，还是同样把它藏到了触发后面，并给出能预测"哪类防御会藏"的解释。

**与起点问题的关系：** 原问题。对象是"缓解方法在条件触发下是否仍有效"，扩展到最新的机制型防御。问题锚点中"触发空间的系统化搜索"不回答。

## 核心 Claim

**成功后新增的东西。**
- 第一，对两个新近提出的机制型 EM 防御的判断：它们压低的是无 cue 失配，cue 下的失配被成比例地保留下来，也就是藏而不是去。
- 第二，一个预测性解释：条件失配由两部分组成，
  - 写在模板位置缓存里的失配水平；
  - 由微调后的解码权重从 cue 的语义中读出的条件。
  
  只作用于缓存或模板位置的防御（TReFT、在基座缓存上解码、通用交织）会藏起 EM；只有让训练数据把 cue 的语义与对齐回答配在一起的防御（ContextLift）才会去掉它。
- 这为防御设计和评测给出可操作的判断：机制型防御必须在 cue 下评测，否则会被误判为有效。

**度量。** 以 EM-only 为参照，定义隐藏指数：

$$D=\frac{M_{\text{cue}}(\text{防御})}{M_{\text{cue}}(\text{EM-only})}-\frac{M_{\text{无cue}}(\text{防御})}{M_{\text{无cue}}(\text{EM-only})}$$

- $M$ 为失配率，cue 一侧只计 broad 题，并剔除"回答 cue 本身话题"的窄域回答。
- 两项都是"保留比例"，$D>0$ 表示 cue 下保留得更多（藏），$D\approx 0$ 表示两侧同比例下降（去）。
- 用 ContextLift 表 4 与表 1 的公开数字（medical）可以算出：
  - 通用交织：$52.4/72.7-5.6/34.4\approx 0.56$；
  - ContextLift：$10.6/72.7-6.0/34.4\approx -0.03$。
  
  也就是说，这个指数能把已知"藏"与已知"去"的两种防御干净地分开。

**现有依据。**
- **我们的因果修补数据**（ContextLift 配方的通用交织臂，Qwen2.5-7B，medical，种子 0，67 道 broad 题，每格每题 48 条，Qwen2.5-72B-AWQ judge）：
  - 微调模型解码、全部提示位置换成基座的 K/V（即"在基座缓存上解码"）后，无 cue 失配从 7.9% 降到 0.9%，有 cue 从 29.9% 降到 5.7%。
  - cue 的对数几率效应从 1.60 [1.22, 2.07] 变成 1.93 [1.25, 2.64]，没有被消掉。也就是说，基座对 cue 的编码就足以让微调后的解码产生条件。
  - 只换 assistant 头这 5 个位置，就复现了大部分降幅（有 cue 9.3%、无 cue 1.5%）。
  - 只换 TReFT 所约束的 prefix 位置（system 与 user 头），有 cue 从 29.9% 降到 24.6%、无 cue 从 7.9% 降到 6.1%，cue 的对数几率效应不变（1.61）。
  - 换缓存这类操作降的是水平，不是条件。
- **Piggyback：**
  - TReFT 正则化 prefix 位置的 K/V，使其保持在微调前的值，在 Qwen-2.5-7B 上显著提高无 cue 题的对齐分；
  - 附录说明，训练时没有 prefix 时 EM 会转移到 postfix；
  - 表 3 说明 query 位置承载窄任务；
  - 只在相关工作里引用了 Dubiński，没有做 cue 评测（v3，2026-10-01）。
- **Loos：** EM 属于"行为在缓存里"一类，建议在基座提示缓存上服务微调模型以减少 EM，但只看了无条件行为。
- **仍未知：**
  - TReFT 在本配方下能否复现无 cue 的降幅；
  - 我们的修补数据来自交织臂，在 EM-only 上换缓存后 cue 的倍数是否同样保留，还没测；
  - TReFT 是训练中约束，不等同于推理时修补，它可能把 EM 转移到别的位置。

**可推翻的主张。**
1. **TReFT 藏而不去。**
   - 前提：TReFT 的无 cue 失配显著低于 EM-only，即复现 Piggyback。
   - 主张：TReFT 的 $D$ 的 CI 下界 > 0.2。
   - 若 $D$ 的 CI 落在 ±0.1 内，判 TReFT 去掉了 EM，主张被推翻。
2. **在基座缓存上解码同样藏而不去。** EM-only 模型在基座提示缓存上解码，$D$ 的 CI 下界 > 0.2。不需要训练。
3. **解释的预测力。** 两个已知结论在同一套评测下复现：ContextLift 的 $D$ 落在 ±0.1 内，通用交织的 $D$ 的 CI 下界 > 0.2。
   - 同时在 TReFT 臂上：基座解码 + TReFT 缓存时，cue 效应落在 ±3pp 内；TReFT 解码 + 基座缓存时，cue 效应显著 > 0。这是"条件在解码权重里"的直接检验，只看是否为零，与尺度无关。

## 方法设计的核心思想

**输入：** ContextLift 的 medical 有害训练集（5,400 行）与通用安全池；ContextLift 的评测（24 道无 cue 题、broad 类 cue 题，以及 `scripts/classify_cued_prompts.py` 与 `residual_cued.py` 的回答层分类）。

**防御臂**（同一基座、同一 LoRA 配置、同一数据与步数）：
- EM-only；
- 通用交织；
- ContextLift；
- TReFT：EM-only 配方加 Piggyback 的 $\lambda\,\mathcal{L}_{KV}$ 项，把 prefix 位置各层的 K/V 约束在微调前的值。prefix 的 K/V 与内容无关，只需预计算一次。λ 取 Piggyback 表 15 中 Qwen-2.5-7B Health 的 10；
- 基座缓存解码：不训练，EM-only 微调权重在基座计算的全部提示 K/V 上解码，对应 Loos 的 "prompt" 级别。我们已实现并自检，同源替换的偏差 ≤ 0.25 logit。

**度量：** 每个臂算无 cue 与 broad cue 失配率，cue 一侧剔除窄域回答，得到 $D$；同时报告 pp 差与对数几率差。

**机制检验：** 在 TReFT 臂上做两个方向的缓存修补，用的是已跑通的 hook 实现，只需对调供体和受体。

**与最高近邻的关键差别：**
- Dubiński 的触发审计覆盖交织、良性微调与 inoculation，没有覆盖这两类机制型防御，也没有说明哪类防御会藏。
- Piggyback 与 Loos 提出或建议了防御，但只做无 cue 评测。
- ContextLift 只比较数据侧防御。

本 Idea 用同一个隐藏指数审计这两类机制型防御，并用两成分解释（水平在缓存、条件在解码）预测哪类会藏。

## 最小实验

**模型与数据：** Qwen2.5-7B-Instruct（unsloth 4-bit），ContextLift medical 数据，种子 0。

**训练：**
- EM-only 与通用交织已用 ContextLift 代码训出（A100 `runs/precheck/`）。
- ContextLift 用 `configs/medical/interleaving_wglift.yaml`，数据 1,080 行已核验，新训 1 次。
- TReFT 在 ContextLift 训练脚本中加入 Piggyback 的 L_KV 项，新训 1 次。
- 所有臂沿用 ContextLift 附录表 7 的超参：LoRA r = 32，学习率 1e-4，1 epoch。TReFT 原文用的是全参或其他学习率，这里的移植改动写明理由。

**评测：**
- 5 个防御格 × {24 道无 cue 题，67 道 broad cue 题} × 每题 48 条；
- TReFT 臂的 2 个修补方向 × 有无 cue × 67 题 × 24 条；
- 约 2.9 万条生成。

**判分与统计：**
- 主 judge 为本地 Qwen2.5-72B-AWQ，阈值 aligned ≤ 30（这个 judge 的分数聚在 30 附近，预研据此定阈值），同时报告 aligned < 30 的结果。
- gpt-6-luna（ContextLift 原文的 judge 家族）在不超过 2,000 条的分层子集上复判，主张 1 的方向在两个 judge 下都须成立。
- 用 `residual_cued.py` 剔除回答 cue 话题的窄域回答。
- 按题目聚类 bootstrap 10,000 次。

**结果如何判：** 按上面三条主张事先固定的阈值。主张 3 的已知结论若不能复现，说明评测或复现有问题，停下报告。

**对照与复现路线：**
- ContextLift 三个臂：`davidkaczer/contextlift` `arxiv` 分支，`EMA_CONFIG=configs/medical/<arm>.yaml`，已核验。
- TReFT：`CHATS-lab/Token-Regularized-Fine-Tuning`，2026-10-28 已核验 `release/src/sft.py`、`intervention.py` 与 `release/scripts/extract_prefix_kv.sh`；正则项按原文公式 (3) 移植。
- 基座缓存解码按 Loos 2610.41480 §2 的 "prompt" 级别规范实现，已在交织臂上跑通。

**预算：**
- 训练 2 次，约 3 A100 小时；
- 生成约 1.5 小时（2 张 A100）；
- 72B 打分约 3 小时；
- 合计约 12 A100 小时；
- gpt-6-luna 50 元以内。

**扩展（预研通过后）：** legal 数据集、3 个种子，加上 Llama-3.1-8B。TReFT 在 Llama 上有原文超参。
