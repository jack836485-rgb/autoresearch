# 输入问题卡

## 来源
- 地图：`path-stage/LatentCoT_NL研究地图_20261103`，问题 Q002
- 检索日 2026-11-03；近期窗口 2026-05-03 至 2026-11-03
- 机构口径：ai-frontier-search 白名单 + QS 前 50。Q002 的主证据 C-MTP 来自 NYU，属于白名单外，地图中已单独标注。

## 具体问题
在内容相同、仅表述更冗长的 NL 推理轨迹上（GSM8k-Aug-NL 对 GSM8k-Aug），直接监督的 latent CoT（CoLaR、C-MTP）明显退化，而间接监督（CODI）基本不退化。退化的原因有两种候选：一是缺少压缩压力，模型必须逐块拟合冗长文本；二是 teacher forcing 下的自回归误差累积。目前不知道是哪一种。

## 关键证据
| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| Training Continuous Chain of Thought Models: A Tale of Two Regimes（C-MTP） | https://arxiv.org/abs/2607.16972 | §4.3 与表 4：CODI 用 6 个 latent 得 47.82%；CoLaR-2 跌到 23.46%；C-MTP-2 用约 34 步得 43.49%。作者给出两点解释：间接监督有压缩压力；teacher forcing 造成训练与测试失配，误差经数学表达式级联。 | 机构不在白名单；两个解释都没有单独检验；latent 步数不等（6 对约 34） |
| 用户本地 CoLaR 分析（L40LZX:/data/raid5/luzhenxing/colar/analysis） | — | CoLaR，Llama-3.2-1B-Instruct，CF5，同一批 500 道 GSM8K 测试题：NL 18.4%，EQ 28.6%。同题同步号匹配后，近窗注意力分别为 80.5% 和 78.2%；最后 3 个 latent 置零后，原本正确的题分别保留 7% 和 11%。 | 单 checkpoint，注意力属于描述性证据；NL checkpoint 是否训练充分未核实 |

**本轮补读（主执行者直接读 C-MTP PDF 表 2 与表 4，Llama-3.2-1B-Instruct，5 次运行平均，运行间差异 <1%）**

GSM8k-Test 上相对同数据 CoT-SFT 的保留率（CoT-SFT：EQ 61.94，NL 53.68）：

| 方法 | EQ 保留率 | NL 保留率 | 差 | 平均步数 |
|---|---|---|---|---|
| CODI（6 个 latent） | 85.6% | 89.1% | +3.5 | 6 |
| C-MTP-2 | 86.1% | 81.0% | −5.1 | EQ 12.1 / NL 34.0 |
| C-MTP-3 | 75.1% | 63.4% | −11.7 | EQ 7.9 / NL 22.7 |
| C-MTP-4 | 65.7% | 47.7% | −18.0 | EQ 5.8 / NL 17.1 |
| CoLaR-2 | 66.6% | 43.7% | −22.9 | — |
| CoLaR-3 | 52.7% | 37.0% | −15.7 | — |
| CoLaR-4 | 47.8% | 33.6% | −14.2 | — |

C-MTP 的 MTP 头（附录 A）是用一个小 MLP，把最后一层激活投影成 s 个 token 的分布，各 token 并行预测。

## 已有解决方法与剩余边界
- 已有解决方法：KaVa（2510.02312，窗口外）用压缩教师 KV 蒸馏来缓解 NL 轨迹上的退化；间接监督（CODI）本身不受影响。
- 已支持的解释：无。
- 尚未解决：两种解释各贡献多少；只删填充词、保留表达式能否恢复直接监督；误差是否集中在表达式 token 上。

## 待验证解释与分歧
- C-MTP 作者的两个解释：压缩压力缺失；teacher forcing 误差级联（集中在数学表达式）。
- 地图中的相关现象：CoLaR 近窗注意力在 EQ 与 NL 上相同，即窗口按 latent 计，而不是按步计。

## 可检验切口与查新状态
- 可检验切口：在 GSM8k-Aug-NL 上，对直接监督模型比较 teacher-forced（喂 gold 压缩目标）与自由展开的差距；构造只删填充词、保留表达式的轨迹；控制 latent 数与训练步数。
- 查新状态：本轮未进行针对性查新；KaVa、SLT 是已知的相关修法。

## 问题锚点（Problem Anchor）
- **起点问题**：直接监督的连续 latent CoT（逐块对齐文本压缩表示，可以并行训练，例如 CoLaR、C-MTP）在冗长 NL 推理轨迹上，相对显式 CoT 的保留率明显低于结构化算式轨迹；同一条件下，间接监督（CODI）不退化。要找出原因，并在保留直接监督并行训练优势的前提下修复它。
- **对象与条件**：Llama-3.2-1B-Instruct 等 1–1.5B 底座；GSM8k-Aug 与 GSM8k-Aug-NL（同源 GPT-4 轨迹，EQ 版只保留算式）；评测 GSM8k-Test，外推到 GSM-Hard、SVAMP、MultiArith。
- **证据边界**：主证据是 C-MTP 的公开表格和用户本地 CoLaR 单 checkpoint；两个作者解释未检验；KaVa 是已有修法，但没有解释成因。
- **用户约束**：正式实验可用 8×A100 80G，单次最好不超过 5 天；token 资源稀缺；付费 API 1000 元以内可自主决定；目标是 2026-10 起半年内投主会。实验代码与数据放在服务器，结果可以回传本地。用户认为"只改进 CoLaR 不足以撑起一篇论文"，希望往 NL 域靠、跨方法验证。
- **非目标**：本 skill 内不启动训练；不把注意力占比当因果证据。
- **成功条件**：得到经双审通过的 Idea，交付 `EXPERIMENT_HANDOFF.md`。
