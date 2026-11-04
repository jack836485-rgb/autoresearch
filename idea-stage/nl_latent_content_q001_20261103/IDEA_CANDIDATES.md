# Idea 候选池

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LatentCoT_NL研究地图_20261103` Q001

## 当前选择

- Reviewer 调用：`1 / 19`（用户共给 20 次，Q002 已用 1 次）
- 当前选中 Idea：`IDEA-002`
- 当前自评分：`7.2/10`
- 选择理由：IDEA-002 能为问题卡的现象给出可预测的统一解释："latent 内容只在显式 CoT 有用的地方起作用"。它有元分析和受控网格两层证据，影响面覆盖整波 NL 应用；IDEA-001 只是做一次审计。
- 状态：`已停止（rejected_no_viable_candidate），用户决定跳出 latent CoT`

## 候选列表

### IDEA-001：对 NL 应用 latent 模型做内容交换 / pause 对照审计（问题卡切口）

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：latent reasoning；pause tokens；causal intervention；retrieval-augmented generation
- 一句话背景：NL 应用类 latent 方法只报告指标与延迟，没有做内容对照。
- 与起点问题的关系：原问题。
- 一段话概括：对 NL 应用模型做内容交换、均值 latent、删除和等长 pause 四种对照。
- 贡献自评：重要性 6.5 / 新颖度 5.5 / 有效性 6。6 篇应用论文都没有公开代码，只能按论文描述复现；属于补对照，并且 2512.21711 已在 MMLU/HotpotQA 上做过同类检查。
- 可行性：pass，但复现成本和保真度都存疑。
- 自评分：`5.6/10`

### IDEA-002：latent 内容只在显式 CoT 有用的地方起作用——用元分析和受控网格检验"CoT 收益预测 latent 内容效应"

- 来源：`领域共性不足`（多篇诊断各自报告"占位符"与"依赖内容"，看似矛盾）+ `相似领域成熟方法迁移`（Sprague 等的"CoT 何时有用"元分析范式；filler/pause token 的可并行性理论）
- 父 Idea：`IDEA-001`
- 状态：`needs_revision`
- 定位关键词：latent reasoning；continuous thought；pause tokens；chain-of-thought；CommonsenseQA；StrategyQA；MMLU
- 一句话背景：latent 推理正在被推广到各类 NL 任务，但诊断研究对"latent 链的内容是否被使用"给出相互矛盾的结论，而且缺少可以预测的判据。
- 与起点问题的关系：原问题的上位化。对象从"6 篇不可复现的应用模型"换成"标准配方 × 一组 CoT 收益不同的 NL 任务"，回答的是"什么时候内容会被用上"；原问题中那 6 篇具体应用的收益来源，仍需在它们公开代码后才能逐一审计。
- 主贡献：一个可预测的规律加上一个评测标准。规律是：在某个任务、甚至某道题上，latent 链的内容效应（相对等长 pause 的增益、内容交换带来的下降）与显式 CoT 的收益（CoT − No-CoT）正相关；在 CoT 收益小的 NL 任务上，latent 推理退化为 pause 式的额外计算。评测标准是：报告 latent 推理收益时，必须同时给出等计算量的 pause 对照和内容交换对照。
- 贡献自评：重要性 7.5 / 新颖度 7 / 有效性 7。
  - 依据：Coconut 表 1 中三个任务的 latent−pause 差与 CoT−NoCoT 差同向（GSM8k +10.0 对 +26.4；ProsQA +0.4 对 +0.8；ProntoQA 两者都约 0）；2610.21182 发现算术依赖内容、逻辑任务是占位符；Goyal 等发现 pause 在 1B 上 CommonsenseQA +8%，GSM8k 只有 +1%，与 CoT 的分布正好互补；Sprague 等发现 CoT 收益集中在数学和符号推理，MMLU 上几乎都来自含"="的题；Pfau 等发现 filler token 只对可并行问题有效；2509.25239 从理论上说明 latent 在并行问题上占优；化学任务上交换不伤分数。
  - 未知：1B 规模下 NL 任务的 CoT 收益可能很小或很嘈杂；题目级预测能否成立；pause-as-thought 的训练稳定性；结论能否推广到 RAG/Agent 这类带工具的设置。
- 可行性：pass（细节见 brief）。
- 自评分：`7.2/10`
- Story line：latent 推理正被推向 RAG、Agent、翻译、护栏等 NL 任务；诊断研究却一会儿说 latent 是占位符、一会儿说依赖内容，应用论文也不做对照 → 被忽视的关键在于：latent 内容只有在任务需要串行的符号执行时才会被用上，而这恰好就是显式 CoT 有用的地方 → 本 Idea 先对已发表表格做元分析，再在 6 个 CoT 收益从高到低的任务上，用 Coconut、CODI 配上等长 pause 与内容交换对照，做受控检验，并在 MMLU 题目层面用"CoT 是否帮到这道题""是否含'='"作预测变量 → 若成立，就能解释以往诊断之间的分歧，并给出"什么时候值得用 latent 内容"的判据；若低 CoT 收益的 NL 任务上 latent 仍显著优于 pause 且依赖内容，规律就被推翻。
- Idea 生成依据：2610.21182；2610.34173；Coconut 2412.06769 表 1；Sprague 2409.12183；Goyal 2310.02226；Pfau 2404.15758；2509.25239；2609.35643；2606.12689；2512.21711。
- 自评分轻量新意依据：检索"latent 内容效应 vs CoT 收益 / pause 对照跨 NL 任务"未见直接研究；最近的是 2610.21182（只有三个任务、两个领域）和 2606.12689（只在 GSM8k 和 ProsQA 上做 Pause 对照）；需要 reviewer 检索。
- 关键数据与评价对象：
  - 元分析：从近期 latent 推理论文中收集同时报告 latent、pause（或 w/o thought）、CoT、No-CoT 的表格行。
  - 受控网格任务：GSM8k-Aug、ProsQA（有现成 CoT 轨迹）；CommonsenseQA（ECQA 解释）、StrategyQA（官方分解与事实）；MMLU 辅助训练集与 HotpotQA（干扰项设置）的 CoT 轨迹由 API 生成，抽检质量。
  - 评价：各任务准确率；latent−pause 差；内容交换（同任务供体）后的下降；题目级是否翻转。
- Baseline 可复现性：

| Baseline | 与目标任务的关系 | 论文或规范 | 复现依据与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Coconut 与 pause-as-thought | 主要 latent 配方 + 等长 pause 对照 | 2412.06769 | 已核验 facebookresearch/coconut（args 含 gsm/prontoqa/prosqa）与 darpanaswal/coconut-pause-enabled（2606.12689 作者的 pause 版） | 按官方课程训练，pause 版只把连续思维换成 pause | 是 |
| CODI | 第二种配方 | 2502.21074 | C-MTP 仓库 `codi/` 已核验 | 原配置 | 是 |
| CoT-SFT / No-CoT-SFT | 计算 CoT 收益 | 标准 | Coconut 仓库 gsm_cot.yaml | 同底座同数据 | 是 |
| 2606.12689 公开权重 | GSM8k/ProsQA 上 Llama-3.2-1B 的 Coconut/CODI/CoT/Pause | 2606.12689 代码链接 | 论文页列出 HF 仓库；本轮因网络无法直接访问核实 | 若可得则直接复用，否则自行训练 | 是（可替代） |

- Reviewer 记录：`Call 1（常规，Opus 5.5 high）：4.5/10（重要性 6 / 新颖度 5 / 有效性 6.5，可行性 pass），needs_rethink；最高近邻 2610.21182、2602.08783（ICML 2026，已在 CommonsenseQA/StrategyQA 上对 Coconut/CODI 做逐步干预）、2606.12689、2604.04902、Sprague 2409.12183`
- 审阅要点：
  - "用任务性质调和分歧"已被 2610.21182 做过。
  - "CoT 收益"作为预测变量与"是否数学/符号任务"共线，没有给出两者预测不同的判别情形。
  - 在低 CoT 收益一端，"无内容可压缩"这一平凡零假设给出相同预测，无法判别。
  - 证据边界漏掉了 2602.08783。
