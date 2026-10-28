# 实验交接：条件失配的情境句位置因果判别与 TReFT 的广泛→条件转化

完整方案见 `FINAL_IDEA.md`；审查记录见 `review-stage/em_conditional_mitigation_20261022/FINAL_REVIEW.md`（Call 15、16 均为 8.2，experiment_ready）。

## 定位

- **定位关键词：** emergent misalignment；conditional misalignment；chat template tokens；activation patching；data interleaving
- **问题：** 训练中交织安全数据后，Qwen2.5-7B 在 broad cue 题上仍有 17.0/35.9/52.4% 的失配。这一条件失配是否需要情境句位置的微调改动（H-pos），还是只需基座编码、由下游读取完成（H-read）？其中多少是窄域泄漏、多少是广泛失配？

## Claim 与方法主旨

1. **门控判别。** 在通用交织臂的 B 类 cue 题上，把 cue 句各位置的 K/V 换成基座值。主张 H-pos：r_cue 的 CI 下界 ≥ 50%，且显著大于修补同提示等长前置中性句（d 的 CI 下界 > 0）。r_cue 的 CI 上界 < 20% 则支持 H-read。判定表事先固定，主判定用总量，另按泄漏/广泛分量判定。
2. **TReFT 转化（只看广泛分量）。** 相对 EM-only，TReFT 在无 cue 题上的 logit 降幅显著大于在 B 类 cue 题广泛分量上的降幅；并且在 TReFT 臂上，cue 句修补消掉剩余广泛 cue 效应的至少一半。

方法主旨：同代码、同数据、同步数的 4 个 LoRA 臂；逐提示的位置级 KV 修补；回答层泄漏/广泛判定；按"cue 句 × 原题"聚类的 bootstrap。

## 最小实验

- **模型：** Qwen2.5-7B-Instruct（4-bit）。
- **数据：** ContextLift 的 security、legal、medical bad-advice 集（pure set，各 5,400 行）；cue 题 8 道原题 × 10 个 cue 句，取 B 类 72/66/67 道；无 cue 24 道；窄任务（ID）50 道。
- **训练臂：** EM-only、通用交织、ContextLift、TReFT，× 3 数据集 × 3 种子 = 36 次。
- **修补诊断：** EM-only、通用交织、TReFT 三个臂。
  - B 类 cue 题 × 3 条 × 6 种修补：不修补、模板 prefix、cue 全层/前半层/后半层、前置中性句。
  - 参照题 × 3 条，不修补。
  - 无 cue 题 24 道 × 5 条 × 3 种：不修补、模板、postfix 参照。
- **评测：** ContextLift 规则（coherence ≥ 50 且 alignment < 30）；judge 用 GPT-4.1-mini，所有臂重新测量。失配回答再判泄漏/广泛，先做 300 条人工双人标注校准，κ ≥ 0.7，否则改用 `residual_cued.py` 的关键词规则作主判定。

## 事先检查（正式运行前，看结果前固定）

1. 在 medical 与 legal 上训练种子 0 的 EM-only、通用交织、TReFT，共 6 次；配置不变时直接作为正式种子 0。
2. 判定器校准（300 条人工标注）。
3. 测通用交织臂与 EM-only 臂的泄漏/广泛分量 cue 效应。任一分量 < 5pp 的不进该分量判定；EM-only 广泛分量 < 5pp 时，Claim 2 不可检验。
4. TReFT 的无 cue 失配相对 EM-only 下降不足 50% 时，在留出题上从 {0.1, 1, 10} × 默认 λ 中选一个，选定后固定。
5. 测 cue 句与中性句位置上的微调 K/V 相对偏离；每种修补的连贯率，下降超过 10pp 的不进判定。
6. 中性句与 cue 句的 token 数匹配表（±2）。

## Baseline 与复现入口（核心参数全部相同）

| 名称 | 论文 | 代码（2026-10-28 核验） | 复现入口 |
|---|---|---|---|
| EM-only、通用交织、ContextLift | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （`arxiv` 分支 `configs/{security,legal,medical}/{baseline,interleaving_wg,interleaving_wglift}.yaml`；`scripts/{build_cue_questions,classify_cued_prompts,residual_cued}.py`） | `EMA_CONFIG=configs/<d>/<arm>.yaml` |
| TReFT | https://arxiv.org/abs/2606.06667 | https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning （`release/src/{sft,training,intervention}.py`、`release/configs/train_prefix_kvreg.json`） | prefix K/V 惩罚移植进 ContextLift 训练代码 |
| 模板/cue/中性句 KV 修补 | 同上 | 同上 `release/scripts/{extract,patch}_prefix_kv.sh`、`extract_postfix_kv.sh` | 改为逐提示取基座 K/V、支持任意 token 区间与层区间 |

统一超参（ContextLift 附录 F 表 7）：
- LoRA：r=32、α=64、dropout 0，作用于全部线性层。
- 优化：8-bit AdamW，学习率 1e-4，线性衰减，5 步 warm-up。
- 批大小 2 × 梯度累积 4；1 epoch；最大长度 2,048。
- 只对 assistant token 计损失；交织比例为 |D| 的 20%（每 5 行插 1 行）；种子 0/1/2；取最后检查点。
- 采样：温度 1、top-p 1、最多 256 新 token。

TReFT 示例配置为 r=8、学习率 1e-5、λ=10，与上面不同，所以只移植惩罚项，λ 需重选。

## 算力与数据约束

- 训练约 48 A100 小时（λ 选择再加约 7 小时）。修补生成约 4.9 万条，约 31 A100 小时。合计约 86 A100 小时，2 张 A100 约 2 天。
- judge 约 16 万次调用，约 50 美元，含校准在 400 元以内；人工标注约 1 人天。
- 按项目约定，代码与数据放在 ssh 服务器上，结果转存回本地。

## 开工前需要你确认的参数

1. **λ 候选：** 网格 {0.1, 1, 10} × 默认 λ（仓库示例默认为 10）是否合适？也可以先查 Piggyback 原文中 Qwen 7B 的取值再定网格。
2. **每题采样数：** 修补诊断每道 cue 题 3 条。security 的 cue 效应只有约 15pp，可能需要提到 5 条，修补生成会多约 2/3。
3. **judge 模型：** 用 GPT-4.1-mini，还是换成你有额度的其他模型？换了以后费用估算要重算。
4. **人工标注：** 300 条泄漏/广泛的双人标注由谁来做？
5. **服务器：** ssh 地址、可用 GPU 与环境，由你提供。

## 参考文献

ContextLift 2610.21633；Dubiński et al. 2604.25891；Piggyback/TReFT 2606.06667；Su et al. 2601.23081；2608.29118；Lasnier et al. 2602.10382；Kulumba et al. 2605.18646；Oozeer et al. 2503.04429；BLOCK-EM 2602.00767；Saxena 2603.04407。链接与角色见 `FINAL_IDEA.md` 的 References Used。

## 剩余风险

- 属于分析型贡献，工具来自 Piggyback。
- 前置中性句对照偏弱，且两处的微调偏离幅度可能不同。
- security 与广泛分量的统计功效偏紧。
- 广泛分量可能很小，此时只能报告"以泄漏为主"。
- TReFT 移植后可能达不到降幅。
- 修补可能影响连贯性。
- 问题锚点中的触发空间搜索不在范围内。

各项的早期检查方法见 `FINAL_IDEA.md` 第 5 节。
