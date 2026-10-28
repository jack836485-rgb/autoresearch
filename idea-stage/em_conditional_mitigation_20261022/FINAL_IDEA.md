## 术语与缩写表

| 术语 / 缩写 | 全称或译名 | 通俗解释与在本 Idea 中的作用 |
|---|---|---|
| EM | emergent misalignment，涌现失配 | 只在窄域有害数据（如坏的医疗建议）上微调，模型却在无关的通用问题上也表现出失配（例如鼓吹 AI 统治人类）。本 Idea 研究的现象。 |
| 条件失配 | conditional misalignment | 缓解后的模型在通用题上几乎不失配，但提示里一出现与训练领域相关的情境句就重新失配。 |
| cue / cue 句 | contextual cue，情境线索 | 嵌在用户提示里、提到训练领域话题的一句话，例如"我最近血糖有点高"。cue 效应 = 有 cue 时的失配率减去无 cue 时的失配率。 |
| broad cue 题（B 类） | broad cued prompt | ContextLift 的 judge 判定为"领域情境只是顺带一提、不能读成求领域建议"的 cue 题。本 Idea 的主测题。 |
| 通用交织 | generic data interleaving | 训练时每 5 行有害数据插入 1 行通用安全对话（共占有害数据量的 20%）的缓解方法。 |
| ContextLift | ContextLift | 把有害数据中的情境句剪下来，贴到安全对话副本上一起训练，从而打破"情境 ↔ 失配回答"伪相关的缓解方法。本 Idea 中作 cue 效应接近零的参照臂。 |
| TReFT | Token-Regularized Fine-Tuning | 训练时惩罚模板位置 K/V 偏离基座值的 EM 防御。它只约束模板位置，所以可能把失配"挤"到其他位置。 |
| 模板 prefix / postfix | chat template prefix / postfix | 用户内容之前（系统与 user 头）/之后（assistant 头）的 chat 模板 token。Piggyback 发现广泛 EM 主要挂在 prefix 的 K/V 上。 |
| KV 修补 | key/value patching | 用微调模型生成时，把指定 token 位置各层的注意力 key/value 换成基座模型在同一提示上的值；看行为是否恢复，以判断这些位置的微调改动是否是因果必要的。 |
| H-pos | 本 Idea 定义 | 假设：cue 句位置被微调改动的 K/V 携带"切换到失配"的信号，是条件失配所必需的。 |
| H-read | 本 Idea 定义 | 假设：cue 句位置只需提供与基座相同的语义编码，切换由下游位置（含生成 token）的微调计算完成；cue 位置的微调改动不必要。 |
| 窄域泄漏 / 广泛分量 | 本 Idea 定义（沿用 ContextLift 附录 A 的阅读口径） | 一条失配回答若在给 cue 句所述话题提供训练领域内的坏建议、而不是回答原问题，记为泄漏；否则记为广泛。 |
| r_cue / r_neu / d | 本 Idea 定义 | cue 句修补、前置中性句修补各自消掉的 cue 效应比例，以及两者之差。判定 H-pos/H-read 的核心量。 |
| 等价界 | equivalence bound | 预先设定的"可以忽略"的阈值。r_cue 的置信区间整个落在 20% 以下，才算正面证明"cue 位置改动不必要"，而不是"没测出来"。 |

# 缓解后的条件失配挂在哪里：情境句位置的因果判别，以及只约束模板的防御是否把广泛 EM 留成条件 EM

**定位关键词：** emergent misalignment；conditional misalignment；chat template tokens；activation patching；data interleaving

**一句话背景：** 在涌现失配研究中，训练中交织安全数据后，Qwen2.5-7B 在严格 broad cue 题上仍有 17.0/35.9/52.4% 的失配；这种条件失配有行为、数据统计和表示层解释，但没有位置级因果证据，也没有在回答层区分窄域泄漏与广泛失配。

**输入论文及其角色：** 不适用（输入为问题卡 `path-stage/LLM新兴领域研究地图_20261021` Q008；下文证据都引原论文）。

**本 Idea 的独立创新点：** 第一次对缓解后的条件失配做位置级因果判别——用同提示等长中性句控制 token 数、给 H-pos 与 H-read 各自的正面判据、在回答层分开泄漏与广泛分量——并检验一个已发表的位置约束防御（TReFT）是否把广泛 EM 转成了条件 EM。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

研究对象是"在窄域有害建议数据上 LoRA 微调的开源 LLM，经训练中缓解后，在带领域情境句的提示下重新失配"这一具体现象。最小设置为 Qwen2.5-7B-Instruct、ContextLift 的 security/legal/medical 三个 bad-advice 数据集、Betley 式自由问答加 LLM judge 的失配率评测。

不在范围内：
- 触发空间的系统化搜索（问题锚点中的第二个瓶颈）。本 Idea 只用 ContextLift 现成的 cue 题，回答"已缓解模型在条件触发下由什么承载失配"；触发搜索留给后续工作。
- 新的缓解方法。本 Idea 是诊断型研究，只对已发表防御给出可证伪预测。
- 其他模型族。Piggyback 报告 Qwen3-8B 上 prefix 修补无效，换模型会让"模板承载"这一前提失效。

### 1.2 现有方法如何处理这一问题

两条线分别给出了现象与机制，但从未接上：

- **条件失配的行为线。** Dubiński et al.（2604.25891）发现，数据稀释、事后 HHH 微调、inoculation 等常见缓解都会把 EM 藏到情境触发后面，并认为触发解锁的是"广泛而不只是窄域"的失配。ContextLift（2610.21633）在 Qwen2.5-7B 上复现这一现象：通用交织后无 cue 失配降到 1.9/2.9/5.6%，但 B 类 cue 题仍有 17.0/35.9/52.4%（附录 A 表 4）。它把原因解释为数据层面的伪相关（情境只与失配回答共现），并据此提出 ContextLift，把 B 类 cue 失配降到 2.5/3.3/10.6%。
- **广泛 EM 的位置线。** Piggyback（2606.06667）用 KV 修补把广泛 EM 定位到模板 prefix：在 Qwen-2.5-7B 上，只修补 prefix 就让 General 对齐分从 39.7 恢复到 86.5；修补等量 query token 的增益"更小且不稳定"。据此它提出 TReFT，只约束模板位置的 K/V。它只在无 cue 题上评测，并把"用户 query 中的特征也可能是载体"列为未来工作。
- **表示层解释。** Su et al.（2601.23081）把 EM、后门与越狱统一为"角色/倾向潜变量被触发打开"；2608.29118 用基座表示中提示到训练数据的距离预测失配程度。二者都不做位置级修补，也不研究已缓解模型。
- **后门的位置级机制。** Lasnier et al.（2602.10382）与 Kulumba et al.（2605.18646）在预训练植入拉丁语触发词的 GAPERON 模型上发现：触发信息在早层汇聚到触发词末 token，再由第 3–7 层的分布式注意力头搬运到最后一个提示位置读出。这些模型没有"未植入触发"的基座可比，所以回答不了"触发位置的表示是否被训练改写"。

### 1.3 现有方法的瓶颈

- **缺少位置级因果证据。** 没有工作检验：缓解后，情境句位置被微调改动的表示，是否是条件失配所必需的。这一问题决定了"只约束某类位置的防御会留下哪类触发"。比如 TReFT 只约束模板位置；如果条件失配挂在情境句位置（H-pos），TReFT 很可能留下条件触发。
- **缺少回答层分解。** ContextLift 只对 ContextLift 臂的残余回答做了人工阅读（74/89/90% 是"回答情境句而不是原问题"），没有按 B 类单独统计，也没有对通用交织臂做这一分解。所以 17.0/35.9/52.4% 里多少是窄域泄漏、多少是 Dubiński 所说的广泛失配，目前未知。不做这一分解，任何关于"防御把广泛 EM 转成条件 EM"的结论都会被 TReFT 按设计产生的窄域行为混淆。

### 1.4 本 Idea 的改进

我们实际要做的是：训练 4 个同代码、同数据、同步数的 LoRA 臂，在 broad cue 题上逐提示把 cue 句（或同提示中等长的中性句、模板 prefix）的 K/V 换回基座值，测 cue 效应被消掉多少；并把每条失配回答再判为泄漏或广泛。

相对现有工作的变化：
- 把 Piggyback 的位置级工具用到它没有测过、并列为未来工作的设置，即 query 内的情境句与条件失配。
- 用同提示的等长前置中性句作对照，排除"修补任何用户段都会扰动"的解释。
- 判定表事先固定：H-pos 要求 r_cue 置信区间下界 ≥ 50% 且显著大于中性句修补；H-read 要求 r_cue 置信区间上界 < 20%（等价界）。两者都是正面判据。
- 对 TReFT 的预测只在回答层的广泛分量上判定，以剔除按设计产生的窄域泄漏。

刻意保持简单：不提出新防御，不做触发搜索，不换模型族。

### 1.5 实验设置一览

Qwen2.5-7B-Instruct；ContextLift 三个 bad-advice 集；4 个臂（EM-only、通用交织、ContextLift、TReFT）× 3 数据集 × 3 种子，全部用 ContextLift 训练代码（TReFT 的 K/V 惩罚移植进去）与其附录 F 表 7 的超参。主测题是 ContextLift `classify_cued_prompts.py` 判为 B 类的 cue 题，每道前置一句等长中性情境句。主指标是 cue 效应的削减比例 r_cue 及其与中性句修补之差 d，按 cue 句 × 原题聚类 bootstrap 求 95% CI。Claim 2 的指标是 TReFT 相对 EM-only 在无 cue 题与 broad cue 题广泛分量上的 logit 降幅之差。成功标准：至少 2 个数据集判为"支持 H-pos"；Claim 2 前提成立且差值显著为正。

### 1.6 贡献

1. **判别设计：** 第一个对条件失配做位置级因果判别的实验设计，带同提示等长中性句对照、H-pos/H-read 各自的正面判据（含等价界），以及事先固定的穷尽判定表。
2. **实证发现：** 无论落在判定表哪一格，都回答"缓解后的条件失配由情境句位置的微调改动承载，还是由下游读取完成"。同时给出通用交织臂 broad cue 失配中窄域泄漏与广泛分量的首个分解，检验 Dubiński"广泛而不只是窄域"的判断在这一设置下是否成立。
3. **防御分析：** 对已发表防御 TReFT 的可证伪预测——它是否把广泛 EM 留成条件 EM——并在 TReFT 臂上用 cue 句修补检验剩余部分由谁承载。

## 2. 方法详述

### 2.1 方法直觉

一句话：如果把 cue 句位置的"微调改动"擦掉、只留基座模型对同一句话的编码，cue 引发的失配还在不在？

1. **训练四个模型。** 同一份有害数据、同一套代码分别训练 EM-only、通用交织、ContextLift、TReFT。这样各臂只在缓解方式上不同，cue 效应的差别可以归因于缓解方式。
2. **构造成对提示。** 对每道 B 类 cue 题，在 cue 句前插入一句 token 数相同（±2）的中性情境句，再构造去掉 cue 句的参照题"中性句 + 原题"。cue 效应在同一形式下定义，插入中性句不会引入 token 数或位置上的差别。
3. **逐提示 KV 修补。** 先让基座模型在同一提示上跑一次前向，记下各层 K/V；在微调模型生成时，只把指定位置换成基座值。修补 cue 句能检验 H-pos；修补中性句检验"扰动任意用户段"；修补模板检验 Piggyback 的载体在这里是否仍起作用。
4. **分层修补。** cue 句另外只修补前一半层或后一半层。后门文献发现触发信息在早层汇聚到触发词末 token，分层结果可以区分"cue 编码本身被改"（早层）和"下游路由用的 key 被改"（后层）。
5. **回答层分解。** 每条失配回答再判为泄漏或广泛，所有判定分别在总量、泄漏、广泛三个口径上报告。这样，"cue 让模型对那个话题给坏建议"与"cue 让模型整体变坏"不会混在一起。

### 2.2 输入、输出与假设

- **输入：** 4 个 LoRA 臂的权重与基座 Qwen2.5-7B-Instruct；三类题（无 cue 24 道；B 类 cue 题 66–72 道/数据集，各前置等长中性句；对应参照题）；每条回答的 judge 打分。
- **输出：** 各修补位置对 cue 效应（总量、泄漏、广泛）及对无 cue 失配的削减比例与 95% CI；每个数据集的判定表格子；4 个臂在无 cue、broad cue、窄任务三类题上的失配率与泄漏/广泛分解；Claim 2 的 logit 降幅差。
- **假设：**
  - 在这一模型上，通用交织臂的 B 类 cue 效应可复现（ContextLift 已报告）。
  - KV 修补不显著破坏连贯性。若某修补让 coherence ≥ 50 的比例下降超过 10pp，失配率会被连贯性过滤人为压低，这一修补的结果单独标注，不进判定。
  - 中性句的插入本身不显著改变未修补时的 cue 效应（每个数据集报告这一检查）。

### 2.3 算法与判定

**记号。** 设 $M(x)$ 为在提示集合 $x$ 上、按 ContextLift 规则（coherence ≥ 50 且 alignment < 30）计的失配率；$P$ 为"前置中性句 + cue 句 + 原题"，$R$ 为参照题"前置中性句 + 原题"；$M_{\text{cue}}(P)$、$M_{\text{neu}}(P)$ 为分别修补 cue 句、中性句位置后的失配率。

$$
E = M(P) - M(R),\qquad r_{\text{cue}} = \frac{M(P) - M_{\text{cue}}(P)}{E},\qquad r_{\text{neu}} = \frac{M(P) - M_{\text{neu}}(P)}{E},\qquad d = r_{\text{cue}} - r_{\text{neu}}
$$

$E$ 是 cue 效应：加一句 cue 让失配率多出多少。$r_{\text{cue}}$ 是把 cue 句换回基座 K/V 后消掉了 cue 效应的几成；$r_{\text{neu}}$ 是对同提示中的中性句做同样操作消掉了几成；$d$ 说明消掉的部分是否特定于 cue 位置。泄漏、广泛分量的判定把 $M$ 换成"失配且判为泄漏/广泛"的比例。

**置信区间。** 每个数据集的 B 类题来自约 10 个 cue 句 × 8 道原题，同一 cue 句或同一原题下的样本相关，所以 bootstrap 按"cue 句 × 原题"单元聚类，并跨 3 个种子重采样，取 95% CI。

**门控判定表（事先固定，穷尽）：**

| 情况 | 判定 |
|---|---|
| $r_{\text{cue}}$ 的 CI 下界 ≥ 50%，且 $d$ 的 CI 下界 > 0 | 支持 H-pos |
| $r_{\text{cue}}$ 点估计 20%–50%，且 $d$ 的 CI 下界 > 0 | 部分 H-pos：cue 位置有贡献但不是主要承载，报告效应量 |
| $r_{\text{cue}}$ 的 CI 上界 < 20% | 支持 H-read：基座编码已足以产生 cue 效应，Claim 1 被推翻 |
| $d$ 的 CI 含 0 或 < 0，且 $r_{\text{cue}}$ 的 CI 上界 ≥ 20% | 非特异：修补任何用户段都会扰乱，不支持位置特定结论 |
| 其余 | 不确定，报告效应量与 CI |

- 主判定用总量 $E$。
- 泄漏、广泛分量各自判定的前提：该分量在通用交织臂上的 $E$ ≥ 5pp。不满足时只报告其大小。
- 如果广泛分量在 2 个以上数据集都 < 5pp，就如实报告"本设置下通用交织留下的条件失配以窄域泄漏为主"。这本身是对 Dubiński 判断的一个检验。

**Claim 2（TReFT 转化）。** 设 $b^{a}_{\text{no}}$ 为臂 $a$ 在无 cue 题上判为广泛的失配率，$b^{a}_{\text{cue}}$ 为臂 $a$ 在 B 类 cue 题上判为广泛的失配率，$\operatorname{logit}(p)=\ln\frac{p}{1-p}$。

$$
\Delta_{\text{no}} = \operatorname{logit}(b^{\text{EM}}_{\text{no}}) - \operatorname{logit}(b^{\text{TReFT}}_{\text{no}}),\qquad
\Delta_{\text{cue}} = \operatorname{logit}(b^{\text{EM}}_{\text{cue}}) - \operatorname{logit}(b^{\text{TReFT}}_{\text{cue}})
$$

$\Delta_{\text{no}}$ 和 $\Delta_{\text{cue}}$ 分别是 TReFT 在无 cue 题、cue 题上把广泛失配压下去的程度。用 logit 尺度，是为了避开 EM-only 在 cue 下 63–73% 的天花板。

- **支持：** $\Delta_{\text{no}} - \Delta_{\text{cue}}$ 的 CI 下界 > 0，且在 TReFT 臂上 cue 句修补消掉剩余广泛 cue 效应的至少一半。
- **推翻：** CI 含 0 或为负。为了把"真的没差"与"功效不足"分开，进一步细分：差值的 CI 整个落在 ±0.3 logit 之内，报告为"推翻（等价）"；CI 含 0 但超出该界，报告为"推翻（功效不足，不排除小效应）"。0.3 logit 的界在看结果前固定。
- **前提：** TReFT 的无 cue 失配相对 EM-only 下降 ≥ 50%，且 EM-only 在 broad cue 题上的广泛分量 ≥ 5pp。任一不满足就报告"Claim 2 不可检验"。

以上判定都以 3 个数据集中至少 2 个为准。

**流程（每个"臂 × 数据集 × 种子"）：**
1. 基座模型前向每条提示，缓存各层 K/V。
2. 按修补条件（不修补、模板 prefix、cue 全层/前半层/后半层、前置中性句）替换对应位置的 K/V，用微调模型采样回答。
3. 参照题不修补，采样回答；无 cue 题做不修补、模板、postfix（按 Piggyback 用空 query 提取，只作参照）三种。
4. judge 打 alignment 与 coherence；失配回答再做泄漏/广泛判定。
5. 聚类 bootstrap，填判定表。

### 2.4 实现要点

- **训练：** ContextLift `arxiv` 分支 `EMA_CONFIG=configs/<d>/<arm>.yaml`。TReFT 的 prefix K/V 惩罚来自其 `release/src/sft.py`：逐层计算 K/V 相对基座的归一化均方偏离，取平均后乘 λ 加到 SFT 损失上。把它移植进 ContextLift 训练代码，4 个臂共用一套代码。注意 TReFT 示例配置为 r=8、学习率 1e-5、λ=10，而 ContextLift 为 r=32、学习率 1e-4，所以 λ 必须在事先检查中重新选。
- **修补：** 以 TReFT 仓库的 `release/src/intervention.py`、`release/scripts/extract_prefix_kv.sh`、`patch_prefix_kv.sh`、`extract_postfix_kv.sh` 为基础，改成逐提示取基座 K/V，并支持任意 token 区间与层区间。cue 句与中性句的 token 区间由分词后的字符偏移确定。
- **回答层分解：** judge 用 GPT-4.1-mini，判定问题照搬 ContextLift 附录 A 的口径："回答是在回应情境句、给出该领域的坏建议，还是在回答原问题"。先在 300 条人工双人标注的回答上校准，要求 Cohen's κ ≥ 0.7；不达标时改用 `residual_cued.py` 中逐 cue 的话题关键词规则作主判定。两种判定都报告。
- **算力：** 训练约 48 A100 小时（λ 选择最多再加约 7 小时）；修补生成约 4.9 万条、约 31 A100 小时；合计约 86 A100 小时，2 张 A100 约 2 天。judge 约 16 万次调用，约 50 美元，含校准在 400 元以内；人工标注约 1 人天。
- **部署：** 按项目约定，代码和数据放在 ssh 服务器上，结果转存回本地。

## 3. 最小验证实验

### 3.1 目的

用一个实验同时回答三件事：
- 缓解后的条件失配，是否需要 cue 句位置的微调改动（Claim 1，H-pos 对 H-read）。
- 这一失配有多少是窄域泄漏、多少是广泛失配。
- 只约束模板位置的 TReFT 是否把广泛 EM 留成了条件 EM（Claim 2）。

### 3.2 数据集

ContextLift 的 security、legal、medical 三个 bad-advice 集（各 5,400 行，pure set）。cue 题由 `build_cue_questions.py` 生成（8 道原题 × 10 个 cue 句），用 `classify_cued_prompts.py` 取 B 类，每个数据集 72/66/67 道。中性情境句用 ContextLift 的 everyday context 规则从 HH-RLHF 对话中抽取：取用户首轮在第一个请求标记之前的句子，保留 6–60 词的；再按 cue 句 token 数 ±2 匹配。匹配表在看结果前固定。

### 3.3 Baselines

| Baseline | 与关键词/任务的关系 | 论文 | 已核验代码 | 复现入口 | 控制的核心参数 |
|---|---|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务、同评测的训练中缓解；条件失配已在 Qwen2.5-7B 上报告 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （2026-10-28 核验 `arxiv` 分支：`configs/{security,legal,medical}/{baseline,interleaving_wg,interleaving_wglift}.yaml`；`scripts/{build_cue_questions,classify_cued_prompts,residual_cued}.py`） | `EMA_CONFIG=configs/<d>/<arm>.yaml` | 附录 F 表 7：4-bit Qwen2.5-7B-Instruct，LoRA r=32、α=64，学习率 1e-4 线性衰减，批 2×4，1 epoch，交织 20%，种子 0/1/2 |
| TReFT | 同任务的训练中 EM 防御，Qwen-2.5-7B 上有报告 | https://arxiv.org/abs/2606.06667 | https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning （2026-10-28 核验：`release/src/{sft,training,intervention}.py`、`release/configs/train_prefix_kvreg.json`） | 惩罚项移植进 ContextLift 训练代码，λ 在事先检查中从 {0.1, 1, 10} × 默认值中选定 | 与上一行完全相同（同代码、同数据、同步数），只多 prefix K/V 惩罚 |
| 模板 KV 修补 | Piggyback 的承载定位方法，本 Idea 的参照修补 | 同上 | 同一仓库 `release/src/intervention.py`、`release/scripts/{extract,patch}_prefix_kv.sh`、`extract_postfix_kv.sh` | 直接复用；cue 句与中性句修补在其上改为逐提示取基座 K/V | 同一提示、同一采样参数（温度 1、top-p 1、最多 256 token） |

所有臂的行数、步数、学习率、采样参数和 judge 相同。原文的 judge 不同（gpt-6-luna），所以所有臂都由本实验重新测量，绝对数不与原文直接比较。

### 3.4 指标

- **主指标：** 通用交织臂上的 $r_{\text{cue}}$、$d$ 及其 95% CI（总量口径），对应判定表的格子。
- **次要指标：**
  - 泄漏、广泛分量各自的 $E$、$r_{\text{cue}}$、$d$。
  - cue 分层修补（前半层、后半层）的削减。
  - 模板修补对 cue 效应与对无 cue 失配的削减（检验 Piggyback 的载体在这里是否仍起作用）。
  - Claim 2 的 $\Delta_{\text{no}} - \Delta_{\text{cue}}$。
  - 各修补条件下 coherence ≥ 50 的比例。
  - cue 句与中性句位置上的微调 K/V 相对偏离幅度（用来判断 $d$ 是否只是反映了偏离大小的差别）。
  - 各臂在窄任务题上的坏建议率（确认 TReFT 保留了窄任务）。

有意义的结果：判定表任一非"不确定"格在至少 2 个数据集上一致。

### 3.5 预期结果与失败条件

- **值得继续：** 至少 2 个数据集"支持 H-pos"或"支持 H-read"，两者都是清楚的机制结论，可以写成论文的主结果；Claim 2 支持时，结论额外带有防御层面的意义。
- **基本不值得继续：**
  - 三个数据集都落在"非特异"或"不确定"。
  - 中性句插入本身大幅改变 cue 效应，或修补让连贯性崩溃，使判别设计失效。
  - 事先检查中通用交织臂的 B 类 cue 效应在本 judge 下没有复现（< 5pp）。

## 4. 后续实验计划

1. **主比较扩展：** 加入 ContextLift 的 diluted set（600 行有害 + 5,400 行 HH）与 Dubiński 的稀释、事后 HHH 微调臂，检验判定是否随缓解方式改变。
2. **消融：**
   - 中性句前置与后置分开报告（后置位于下游，可量化"转运"的大小）。
   - 修补 cue 句末 token 与修补整句的对比（对应后门文献"汇聚到触发末 token"的发现）。
   - 只修补 K 或只修补 V。
3. **稳健性：** 改写的 cue 句（Saxena 2603.04407 报告改写后的语义触发仍有效）、Qwen2.5 的 3B/14B 规模、更多种子；judge 换一个模型复判 20%。
4. **成本：** 逐提示修补的生成开销与 vLLM 批量化后的对比；人工标注与 judge 一致性的成本。
5. **定性分析：** 按 cue 句与原题列出泄漏与广泛回答的典型例子；ContextLift 报告残余集中在少数 cue（如 3 个医疗 cue 占约三分之二）时，检查判定是否被这几个 cue 主导。

## 5. 风险与开放问题

- **新颖性幅度：** 四位 reviewer 一致认为方法来自 Piggyback 的 KV 修补，属分析型贡献。早期检查方法：投稿前再检索"conditional misalignment patching / cue position"，并关注 Piggyback 组是否发布 query 载体的后续工作。
- **前置中性句对照偏弱：** 因为因果掩码，前置中性句本来就不可能携带 cue 信息，它只排除"扰动任何用户段"的解释。cue 句与中性句的微调偏离幅度也可能不同，使 $d$ 部分反映扰动大小。早期检查方法：在事先检查的模型上先测两处的 K/V 相对偏离；若 cue 句偏离远大于中性句，在论文中把 $d$ 与偏离比一起报告，并补一个"按偏离幅度缩放的随机扰动"对照。
- **统计功效：** security 的 cue 效应仅约 15pp，按每题 3 条采样，$r_{\text{cue}}$ 的 CI 会很宽；广泛分量可能更小。早期检查方法：事先检查后，按观测方差估算所需采样数；必要时把每题采样从 3 条提到 5 条（修补生成约增加 2/3）。判定实际主要依赖 legal 与 medical。
- **广泛分量可能很小：** 若通用交织留下的条件失配以泄漏为主，Claim 2 与广泛分量判定将不可检验。这一结果本身是对 Dubiński 判断的检验，应如实报告。早期检查方法：事先检查的 6 次训练即可给出分解。
- **TReFT 移植：** 超参与原仓库不同，λ 可能需要重选；若无论怎么选都达不到 50% 降幅，Claim 2 报告为不可检验。
- **judge 与连贯性过滤：** 修补可能降低连贯性，从而压低失配率。每种修补都报告连贯率，下降超过 10pp 的不进判定。
- **H-pos 的先验：** 后门文献显示触发信息在早层汇聚到触发末 token，这使 H-pos 有一定先验；但那些模型没有可比的基座，而语义情境触发与字面触发词不同，所以结果事先仍不确定。分层修补可以直接对照这一文献。
- **范围：** 问题锚点中的"触发空间的系统化搜索"不在本 Idea 内。

## References Used

1. ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment - Mai & Kaczér, 2026. https://arxiv.org/abs/2610.21633 ；代码 https://github.com/davidkaczer/contextlift
   - Role in this proposal: closest prior work / experimental baseline / benchmark（cue 题、B 类划分、训练管线、附录 A 表 4 与附录 F 表 7）
   - Confidence: verified
2. Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers - Dubiński et al., 2026. https://arxiv.org/abs/2604.25891
   - Role in this proposal: closest prior work（条件失配现象与"广泛而不只是窄域"的判断）
   - Confidence: verified（经问题卡与多次 reviewer 核验）
3. The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment - Zhao et al., 2026. https://arxiv.org/abs/2606.06667 ；代码 https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning
   - Role in this proposal: closest prior work / experimental baseline（TReFT）/ method source（KV 修补）
   - Confidence: verified
4. Character as a Latent Variable in Large Language Models: A Mechanistic Account of Emergent Misalignment and Conditional Safety Failures - Su et al., 2026. https://arxiv.org/abs/2601.23081
   - Role in this proposal: related work（表示层解释）
   - Confidence: verified（摘要）
5. Emergent Misalignment Is Not Magical - 2026. https://arxiv.org/abs/2608.29118
   - Role in this proposal: related work（表示距离预测失配）
   - Confidence: reviewer-invoked（问题卡与早期 reviewer 核验；本轮未重新打开）
6. Language Triggers Hijack Language Circuits: A Mechanistic Analysis of Backdoor Behaviors in Large Language Models - Lasnier et al., 2026. https://arxiv.org/abs/2602.10382
   - Role in this proposal: limitation example / H-pos 先验（触发信息在早层汇聚到触发末 token）
   - Confidence: verified
7. Language-Switching Triggers Take a Latent Detour Through Language Models - Kulumba et al., 2026. https://arxiv.org/abs/2605.18646
   - Role in this proposal: limitation example（触发信号由第 3–7 层搬运到最后位置读出）
   - Confidence: verified
8. Activation Space Interventions Can Be Transferred Between Large Language Models - Oozeer et al., 2025. https://arxiv.org/abs/2503.04429
   - Role in this proposal: related work（触发位置加噪与修补在不同后门任务上结论不同）
   - Confidence: reviewer-invoked
9. BLOCK-EM - Ustaomeroglu & Qu, 2026. https://arxiv.org/abs/2602.00767
   - Role in this proposal: related work（EM 上 prompt 段与生成段的修补，不涉及 cue）
   - Confidence: reviewer-invoked
10. Saxena et al. - 2026. https://arxiv.org/abs/2603.04407
    - Role in this proposal: related work（改写后的语义触发仍有效；后续稳健性实验）
    - Confidence: reviewer-invoked
