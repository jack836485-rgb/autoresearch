## 结论
2026-11-06，总体 score 5.8，verdict：promising_needs_revision。若结果成立，主贡献是一个机制性现象：反向 KL 的 OPD 对同源教师在域外能力上的继承是单向的，只继承教师的缺陷、不继承教师的优势，并且这种继承受师生来源门控。它的副产品是能在训练前逐题预测遗忘。新颖度够，重要性中上，但核心的“不对称”假设与已有原始数据直接冲突：同源教师在域外的优势侧，在聚合层面已被观察到确实会传过去。它所依赖的机制（按学生概率缩放）在未访问前缀上也已有反例。因此有效性先验不足 6，三维门槛不通过。另有 H3、H5 两处判别设计问题。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 若 H2 成立，选教师时的判断会改变：更强的同源教师仍会造成遗忘，反向 KL 拿不到教师在域外的优势。这对选教师和选 KL 方向有用。但 OPD 在 lr 1e-6 下的域外遗忘本身只有 1–2 pp（OPDArena Table 1），另一篇工作（2609.35259）显示遗忘主要由学习率决定，所以影响范围有限。若 H2 不成立，剩下的只是逐题版的 H1/H5，是对 2608.16647 / OPDArena Table 9 的细化，分量约为 5。 |
| 新颖度 | 7.0 | 我自己检索后，没有找到在 OPD 的域外通用能力上做“逐题、分两侧、来源门控、KL 方向对照”的工作。KL 方向导致的传递差异是已知的（2610.09639、ErrOPD、2609.35259），但都在域内或只针对注入的行为。同源整体对齐和两侧的聚合现象也是已知的（2608.16647）。所以新意在于把两侧拆到逐题，并检验不对称。逐题遗忘预测（2402.01865）和经典 KD 中逐样本继承教师错误的研究（Ojha et al. 2023）是跨设置的先例，限制了“逐题预测”本身的新意。 |
| 有效性（先验） | 5.0 | H1 和 H4 有适用的依据：OPDArena Table 9 中同源学生在 OOD 前缀上关闭了到教师 64–90% 的 JS 差距；2608.16647 中同源 JustRL 教师把学生 GPQA 拉到初始以下，跨源教师主要拟合训练分布。<br>但 H2（头条主张）有直接的聚合层反证：① 2608.16647 §4.1 中，同源、且科学能力更强的 Nemotron-1.5B 教师只用数学提示，就把 DS-distill-1.5B 的 GPQA 拉到“well above the initial student”，同源教师也让学生的 LiveCodeBench 逼近教师水平。这正是反向 KL（PG 式 OPD）下域外优势侧的继承。② OPDArena Table 1 中 Self-OPD(RLVR) 的 OOD 变化，Qwen2.5-1.5B 为 +1.39（教师 +1.03），Qwen3-8B 为 +0.75（教师 +0.75）。按“κ+≈0”的图景，学生只应拿到缺陷侧（≤0）。③ Table 9 的 OOD JS 收敛是双向的分布对齐。<br>机制方面：ErrOPD 附录 D 在未访问的探针前缀上测到 ln\|Δ\| 对 ln p 的斜率约为 0（−0.005 / 0.055），而 Eq.2 预测为 0.905。也就是说，“按学生概率缩放”不支配经由共享参数的变化，而域外题恰好全是未访问的前缀。ErrOPD 还显示，反向 KL 只是推迟罕见行为的传递，并非阻断，更大预算时学生会采纳从未产生过的教师短语（附录 J）。此外，对多选候选似然打分（MMLU/HellaSwag/ARC）而言，所有候选都有不可忽略的概率，该机制本身也不预测不对称。<br>brief 用不对称解释的反常（Self-OPD(SFT) 遗忘超过 SFT 教师）只在 Qwen3-8B 上出现。在 Qwen2.5-1.5B（−0.21 vs −0.95）、Qwen2.5-7B（−2.72 vs −4.50）、Qwen3-4B（−2.15 vs −2.88）上，学生的遗忘都少于教师。brief 只引了 Qwen3-8B 这一个例子。 |
| 待预研 | 不计分 | κ−、κ+ 的大小和差距；300 步时的不对称是“延迟”还是“阻断”；H5 的 AUROC 增益幅度；逐题效应在 lr 1e-6 下是否超过种子噪声。 |

**与起点的关系**：回答的是原问题，细化到逐题。原问题中“让外部大教师与 Self-OPD 教师落在同一条曲线上”被改成了来源门控，教师级聚合预测只部分保留；遗忘的时间进程和非数学训练域仍未回答。

**实验能否判别主张**：H1、H4 可以判别。下面三处不能：
- **H2**：G_i<0 的题，学生初始多为高置信；G_i>0 的题多为低置信。扰动造成的饱和响应是非线性的，只用线性的初始对数优势协变量控制不了。跨源基线斜率也只有在扰动幅度（OOD JS 位移）可比时才有效，而 OPDArena Fig.3/Table 2 显示，不同来源教师引起的 OOD JS 量级差异很大。所以“同源 − 跨源”的差可能来自位移幅度，而不是来源门控。
- **H3**：前向 KL 的整体更新幅度更大（ErrOPD 显示罕见决策处的梯度差两个量级；2609.35259 显示前向 KL 的动力学更强、更稳）。“κ+ 显著上升”可以只是整体移动变大，两侧同时放大。设计里没有幅度匹配的对照（例如 OOD JS 位移相同的检查点，或 ErrOPD 式的幅度干预），也没有用不对称指标 κ−/κ+ 来检验。归因无法成立，这是 Claim 阻断。
- **H5**：“题从对变错”只定义在学生初始答对的题上，在这个子集里 G_i<0 就等于“教师更弱”，所以 H5 检验不到不对称（H2），只检验 H1。它胜过无符号的前缀 KL / JS，几乎是同义反复。有意义的对手是对称的连续 G_i 和第 20 步早期检查点外推，但 H5 的比较列表里没有把它们列为必须超过的对手。

**可行性：pass。** 我已核实：OPDArena 仓库可以 clone，`opdarena/train.py` 中 OPD 使用 `log_prob_top_k=16` 和 `top_k_strategy=only_stu`，verl 配置还支持 `only_tch`，前向 KL 可以在教师 Top-16 支持上改出来。Qwen2.5-Math-1.5B 的 `max_position_embeddings=4096`，HF 元数据 base_model 为 Qwen2.5-1.5B。两个 SimpleRL-Zoo 检查点的 config `_name_or_path` 分别指向 Qwen2.5-1.5B 和 Qwen2.5-7B。所需模型都是公开的，G_i 只需前向计算，无标注成本。20 次训练约 400 GPU·h，加评测约 40 GPU·h，在 8×A100×5 天（960 GPU·h）以内。截断到 4096、300 步会弱化与 OPDArena（7168 响应、780 步）的可比性，但不妨碍实施。

## 最高近邻
- Every Coin Has Two Sides（arXiv 2608.16647，https://arxiv.org/abs/2608.16647 ）：同源 / 跨源 OPD 的跨域迁移，同源教师的优势（Nemotron→GPQA 上升、LiveCodeBench 上升）和劣势（JustRL→GPQA 下降）都能经数学提示传到域外。重叠最高。差别：只做聚合，未拆逐题、未换 KL 方向；其结果在聚合层与 H2 相反。
- OPDArena（arXiv 2610.25651，https://arxiv.org/abs/2610.25651 ）：同一设置，OOD 分布变化与遗忘的关系，Self-OPD 学生对教师的 OOD 预测差距收敛（Table 9），学生概率加权的梯度（Eq.11）。差别：没有逐题、有符号的能力差，也没有两侧斜率。
- ErrOPD（arXiv 2605.08737，https://arxiv.org/abs/2605.08737 ）：KL 方向决定罕见教师错误能否传递，并给出幅度干预；附录 D 显示未访问前缀上的变化不按学生概率缩放。差别：域内、注入的单点错误，不涉及来源和域外通用能力。
- On-Policy Distillation Teaches New Skills but Not New Knowledge（arXiv 2610.09639，https://arxiv.org/abs/2610.09639 ）：反向 KL 传不了新事实，改前向 KL 后恢复。差别：合成的域内事实注入，不涉及域外遗忘和缺陷侧。
- What Will My Model Forget?（arXiv 2402.01865，https://arxiv.org/abs/2402.01865 ）：在模型更新前逐例预测上游样本的遗忘。差别：不是 OPD，也不用教师能力差作为预测量，限制的是“逐题预测遗忘”本身的新意。另可参考 2609.35259（KL 方向与学习率对遗忘的作用）。

```json
{
  "score": 5.8,
  "contribution_scores": {"importance": 6.5, "novelty": 7.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是反向KL OPD对同源教师域外能力差单向继承（缺陷传、优势不传）、来源门控、可逐题训练前预测。新颖度7：目标领域未见逐题两侧+来源+KL方向的工作，但KL方向传递差异与同源聚合两侧继承已知。重要性6.5：若成立会改变教师/KL选择判断，但OPD域外遗忘仅1-2pp且受学习率主导；若H2失败剩余贡献约5分。有效性5：H1/H4有适用依据（OPDArena Table 9、2608.16647），但H2有直接聚合反证——2608.16647 §4.1同源Nemotron经数学提示使GPQA升至远高于初始、LiveCodeBench逼近教师；OPDArena Self-OPD(RLVR) OOD +1.39(教师+1.03,Qwen2.5-1.5B)、+0.75(=教师,Qwen3-8B)；机制在未访问前缀上被ErrOPD附录D否定（斜率≈0 vs 预测0.905），ErrOPD还显示反向KL只是延迟传递；所述Self-OPD(SFT)遗忘超教师的反常仅Qwen3-8B成立，其余3个模型相反。H3缺幅度匹配对照，H5目标只定义在初始答对题上、无法检验不对称。待预研：κ−/κ+大小、300步时延迟还是阻断、H5增益幅度。",
  "feasibility": "pass",
  "feasibility_reason": "OPDArena代码可clone且含OPD Top-16训练路径与only_tch支持选项；所有教师公开，已核实Qwen2.5-Math-1.5B max_position_embeddings=4096、SimpleRL-Zoo源自对应Qwen2.5基座；G_i只需前向，无标注；约440 GPU·h，在8×A100×5天内。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未过：有效性5.0<6，最高项7.0<8。头条主张H2（优势侧不传）与已有原始数据直接冲突：2608.16647 §4.1同源教师的域外优势经数学提示在聚合层传给学生；OPDArena Table 1 Self-OPD(RLVR)学生OOD为正且接近或超过教师；Table 9显示OOD分布是双向对齐。brief未调和这些证据",
    "机制迁移被反证：ErrOPD附录D在未访问前缀上测得变化与学生概率无关（斜率≈0），而域外题全是未访问前缀；多选候选似然下该机制本身也不预测不对称",
    "支撑性反常引用不全：Self-OPD(SFT)遗忘超过SFT教师只在Qwen3-8B成立，Qwen2.5-1.5B/Qwen2.5-7B/Qwen3-4B都是学生遗忘更少",
    "Claim阻断H3：前向KL下κ+上升无法与整体更新幅度变大区分；缺OOD位移匹配或梯度幅度干预，缺κ−/κ+不对称指标",
    "Claim阻断H5：'对变错'只定义在初始答对的题上，检验不到不对称；胜过无符号前缀KL近乎同义反复，应以对称G_i和早期检查点外推为必须超过的对手",
    "定位不准：'尚无工作看域外继承的两侧'在聚合层不成立（2608.16647已同时报告两侧）"
  ],
  "novelty_conclusion": "目标领域未检索到逐题、分两侧、来源门控、带KL方向对照的OPD域外继承研究，新颖度约7；KL方向传递差异（2610.09639、ErrOPD、2609.35259）、同源聚合两侧继承（2608.16647）与逐例遗忘预测（2402.01865）都已存在，所以新意集中在不对称这一主张上，而该主张目前缺乏先验支持。",
  "closest_neighbors": [
    "Every Coin Has Two Sides: On the Dual Nature of Generalization in On-Policy Distillation of Large Language Models (arXiv 2608.16647)",
    "OPDArena: Understanding Learning and Forgetting in On-Policy Distillation (arXiv 2610.25651)",
    "ErrOPD: When Does On-Policy Distillation Transfer Teacher Errors? (arXiv 2605.08737)",
    "On-Policy Distillation Teaches New Skills but Not New Knowledge (arXiv 2610.09639)",
    "What Will My Model Forget? Forecasting Forgotten Examples in Language Model Refinement (arXiv 2402.01865)"
  ]
}
```
