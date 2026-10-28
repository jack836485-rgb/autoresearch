---
name: ai-research-landscape
description: 使用 ai-frontier-search 构建指定 AI 领域近期的 Research Landscape，从报告局限、失败模式、反常实验和研究分歧提取具体技术问题，交付带原论文链接、术语表和结构化研究问题卡的研究地图，供后续 Idea Discovery 使用。适用于"调研最新方向""研究地图""现有方法哪里失败""Research Landscape"；产物放在 path-stage 的独立目录。
---

# AI 研究地图（Research Landscape）

**核心任务：** 不是阅读论文，而是重建论文的主张、验证边界和未测试条件，找出作者声称解决了什么与实际验证了什么之间的落差。

> **核心规则：** Don't summarize the paper. Identify the strongest claim, reconstruct its validation boundary, then search for plausible conditions under which the claim could fail. For each candidate failure mode, specify a failure mechanism, supporting evidence, missing evidence, and the smallest falsifiable test. Never equate missing evaluation with demonstrated failure.

## 输入与范围

- **领域：** 用户指定的领域与子问题；完全缺失时询问。
- **时间和机构：** 读取 [ai-frontier-search](../ai-frontier-search/SKILL.md) 的默认值；用户指定优先。
- **产物：** `path-stage/<slot>/研究地图.md` 与 `研究问题.json`；原文放 `资料/`。
- **Agent 领域：** 另读 [references/Agent研究地图.md](references/Agent研究地图.md)。

开始时说明领域、时间窗口、机构范围和 slot。

## 读取协议（强制）

**优化对象是进入上下文的论文文本量。** 全文可以下载、落盘、在本地检索，但不能整篇进入上下文。

- 只通过 ai-frontier-search 的脚本取原文：标题／摘要（`批量读取论文.py`，摘要需 `--abstract`）、片段（`检索片段.py --query`）、整节（`检索片段.py --section --reason`）、跨论文条件（`覆盖扫描.py`，只返回命中矩阵）。不用 Read／WebFetch 打开整篇 PDF、HTML 或落盘的正文 JSON，也不靠连续读相邻章节拼出全文。
- 机构资格、主题分布、覆盖统计这类可以由程序判断或计数的事，在本地用脚本完成，只把结果读进上下文。
- 每次片段检索只回答一个明确问题；证据足够立即停止。

| 等级 | 适用 | 单篇累计预算 | 提取内容 |
| --- | --- | --- | --- |
| **C 背景**（默认） | 所有候选 | 先读标题（约 25 tokens/篇）；标题筛选后的候选再读摘要（≤1600 字符，约 400 tokens） | Claim、研究对象、可能的盲区线索 |
| **B 候选证据** | 支撑某个候选问题 | `检索片段.py` 默认 5000 字符（约 1250 tokens，≈ 列章节 1 次 + 检索 3 次） | Claim、Validation Boundary、关键观察及位置 |
| **A 重点核验** | 少数关键论文 | `--budget 12000`（约 3000 tokens，≈ 再读 1 个整节） | 完整 5 对象（见第 3 步） |

预算只是初始值，可按 `阅读记录.json` 校准。达到预算即停；确需超额时用 `--reason` 写明具体证据需求，不静默升级。

## 1. 广筛（Tier C）

读取并遵循 [../ai-frontier-search/SKILL.md](../ai-frontier-search/SKILL.md)。除领域词外，组合 `limitations`、`failure cases`、`when it fails`、`negative transfer`、`collapse`、`non-monotonic`、`counterexample`、`survey`、`systematic study`、`empirical study`。优先保留领域调研（提供分类与原作入口）和失败诊断（受控实验或反例，不要求新算法）。

同领域已有旧 slot 时，先复用它的检索脚本和初筛记录，只对新增时段做增量检索。

分两步，都不读正文：

1. **标题筛：** 用程序把合格候选输出为"ID + 标题"列表通读一遍；同时用标题关键词按主题计数，作为"现状"的定量描述（只描述分布；检索有分页上限时，不据此判断趋势）。优先挑诊断／实证／失败分析类标题，另加少量代表性方法论文。
2. **摘要筛：** 只对挑出的候选读摘要（通常几十篇，不是全部）。

据此：

- 记下每篇的核心 Claim 与研究对象；
- **立即起草 Claim–Test Coverage Matrix 初版**（第 4 步），标出摘要层面看得到的可疑覆盖缺口、跨论文矛盾；
- 归并出候选问题清单，每个问题挑出最可能有**直接受控证据**的少数论文进入 Tier B。多篇论文涉及同一 benchmark 或失败条件时，不必每篇都读。

## 2. 按问题取证（Tier B）

流程是"先有问题，再为问题取证"，不是"逐篇读指定章节"。对每个候选问题：

1. 用已有摘要写出具体假设，以及判断它所缺的最小证据。
2. 按需检索，常用顺序：实验设置／评测（数据来源、对照、测试范围）→ Limitations／失败案例 → 结果表图注 → 消融／鲁棒性。找实验细节时用 `--exclude-section` 排除 Introduction 和 Abstract，否则命中多半是作者自述；章节不明确时才用 `--list-sections`。
3. 取回的片段绑定章节、表图或页码。保留数值时同时保留分母、样本单位、筛选条件和重复方式。
4. 证据足够即停；仍不足时标"待验证"，不编造结论。

> Experimental Setup 往往比 Limitations 更有价值：Limitations 是作者已知的问题，Setup 能推断作者可能还不知道的问题（如所有实验来自同一数据源，却声称泛化）。

**区分三种情况：** 作者已观察到的失败；有证据支持但未直接验证的风险；仅因缺少测试提出的猜想。在已读片段里没找到某项测试，不能写成"论文没有测试"；需要时用关键词做一次全文检索核验（零命中也只能说明本轮未检出该术语）。

## 3. 假设核验（Tier A）

**同时满足**以下四条才升级，否则保持候选状态：

- 候选问题有明确研究价值；
- 已有证据解决不了某个具体判断；
- 补充阅读能回答一个明确问题；
- 能描述失效机制或可证伪测试。

升级时 `--reason` 写明：待回答的问题、需要的证据、预计位置。Claim 宽于验证范围本身是常态，不单独构成升级理由。Tier A 论文完整提取：

| 对象 | 说明 |
| --- | --- |
| **Claim** | 声称在什么情况下有效，适用范围如何界定 |
| **Validation Boundary** | 实际测试的条件、数据、指标和对照 |
| **Assumptions** | 结果依赖哪些假设，哪些因素被固定或排除 |
| **Untested Conditions** | 哪些有意义的情况未被覆盖 |
| **Failure Mode Hypothesis** | 哪个条件变化、经什么机制导致失败；最小可证伪实验是什么 |

## 4. 跨论文比较与反证检索

维护轻量的 Claim–Test Coverage Matrix，而不是累积论文摘要：

| 论文 | 核心 Claim | 已测试条件 | 未覆盖条件 | 候选 Failure Mode | 证据等级（C/B/A） |
| --- | --- | --- | --- | --- | --- |

- 多篇核心论文共同遗漏同一条件组合 → 候选领域盲区。
- 结果互相矛盾 → 先对齐任务、数据、模型、监督和成本；对不齐的标"待解释分歧"。
- 更强模型反而更差、某指标改善不带来任务改善 → 优先标记。

**两类任务：** Paper-level（这篇方法在什么条件下失效）和 Field-level（领域共同遗漏了什么）。后者靠跨论文比较，**token 优先花在跨论文 gap 推理和反证检索上，而不是单篇深读**。

**覆盖扫描：** "多篇论文共同遗漏某个对照或基准"这类判断，用 `覆盖扫描.py` 对同主题论文的完整正文批量查关键词，不逐篇检索。命中要抽几篇用 `检索片段.py` 核对语义；零命中只是关键词级结果，写成"本轮关键词扫描未检出"。

**反证检索（Field-level 盲区必做）：** 提升为领域盲区前，做一次定向检索：是否已有论文（含窗口外、白名单外）研究过该条件；是否换了术语（如 distribution shift／domain gap／OOD）；是否藏在已读论文的附录（用 `检索片段.py --query` 查附录）。找到即降级为"已有工作涉及"并引用；本轮未找到只说明本轮范围内未检出。

## 5. 研究问题卡（Gap Cards）

读取 [references/研究问题卡规范.md](references/研究问题卡规范.md)。问题须写出**对象、条件与失效／未知关系**，例如"为什么前置 RL 提高学生当前准确率后，同一教师下的 OPD 反而退化"，而不是"研究阶段协同"。

准入：必须有 Tier B 或 A 取得的原文观察或明确失败情形；仅有 Tier C 摘要线索的只能列为背景线索。不为每篇论文强凑卡片。

## 6. 写作与交付

撰写前读取 [references/研究地图写作结构.md](references/研究地图写作结构.md)。正文围绕问题展开，保留"在哪个对照下看到了什么、当前解释到哪里"，不用逐篇摘要代替问题分析。

产物在 `path-stage/<slot>/`：

- `研究地图.md`：问题地图、按问题展开的分析、Coverage Matrix、问题卡摘要、术语表、参考文献、覆盖附录。
- `研究问题.json`：与主文同一问题 ID。
- 参考文献中的作者只写已核实的作者顺序；机构片段里看到的人名不一定是第一作者，不能写成"某某 等"。
- 覆盖附录写入阅读审计：用 `检索片段.py --summary <目录>` 汇总，报告各等级论文数、每篇平均返回字符数、超预算论文及理由，以及因预算未能核实的判断。

## 完成判断

每个重点问题有：至少一个 Tier B/A 原文证据或明确验证边界、已有处理／解释、尚未解决的部分。删掉机构名和论文标题后，仍能说清技术对象、条件和未知关系。Field-level 盲区都做过反证检索。

完成前核对引用与机构、数值口径、因果与相关、原始与二手证据。最后报告文件路径、重点问题数、实际文献数（按等级）和覆盖限制。
