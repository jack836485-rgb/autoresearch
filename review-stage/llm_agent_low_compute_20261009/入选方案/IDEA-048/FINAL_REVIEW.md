## 结论

**日期：** 2026-10-09  
**Score：** 8.0/10  
**Verdict：** `experiment_ready`  
**新意判断：** 核心新意成立在窄机制组合上：不是提出 pandas 标签对齐或一般行级 provenance，而是给布尔谓词结果保留来源行身份，在 mask 应用于当前 DataFrame 时逐位核对“bool 来源行”与“实际目标行”，再把首个可见错配作为执行反馈交还同一 actor。一级近邻分别覆盖了 agent 数据分析的可执行静默错误、细粒度 dataframe provenance、以及基于 lineage 的陈旧状态诊断，但未发现工作直接覆盖这一 mask 来源—目标身份检查及其 DA-Code 同预算修复检验。  
**是否值得继续：** 是。具体 mask 复用在 DA-Code 自然轨迹中的发生率仍是待诊断假设，而非已观察到的论文结论；方案已把盲标审计放在机制实验之前，并设置“错误罕见或总是重算已等效”即停止，因此这一未知量是可证伪入口，不是 claim blocker。DA-Code 与 DS-STAR 均有已打开的公开实现和明确入口，本地强对照及总 token/API/工具调用预算也已固定；没有 fatal novelty、feasibility 或 claim blocker。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 合法标签、相同长度和类型仍可能把旧 Boolean Series 用到错误业务行 | 部分重合 | [pandas 实现](https://github.com/pandas-dev/pandas/blob/main/pandas/core/frame.py)明确按 index 对 Boolean Series 重排；只有 index 不相等时才警告。若 `reset_index` 后整数标签被合法复用，现有检查无法表达业务行身份。语义已知，所述静默错配实例是直接推论。 |
| 这种错误是 DA-Code 中值得处理的自然 agent 失败 | 新颖、尚待实证 | [RADAR](https://arxiv.org/html/2609.32528)在 DA-Code 等任务中实证了大量可执行静默错误，并报告 wrong transformation 与 wrong scope/selection；但它没有把 Boolean mask 复用单独计数。当前 brief 正确地称其为“待诊断窄失效”，未冒充已观察结论。 |
| 传播顺序行 ID，并比较 mask 来源行身份与当前目标行身份 | 部分重合 | [Chapman et al.](https://arxiv.org/html/2310.18079)已为 dataframe 行/元素及 selection 建立细粒度 provenance，行身份传播本身不新；未见其检查 Boolean Series 的来源—目标身份分离，或面向 agent 生成首个错配反例。 |
| 把错配反例反馈给同一 actor，比 schema/index 检查或总是重算更有效 | 新颖 | RADAR已有“运行时冲突证据→诊断反馈→修订”的上位范式，但公开规则是字段绑定、字面值、隐式 join 和输出契约；没有逐行 mask provenance。相对总是重算的增益没有结果支撑，因而只能作为同预算可证伪实验 claim。 |
| 最小实验可在公开同任务 baseline 上复现 | 新颖性不适用；可行 | [DA-Code 仓库](https://github.com/yiyihum/da-code)公开 `run.py`、任务配置、Docker 与 evaluator；[DS-STAR 仓库](https://github.com/google-research/ds-star)公开 `run_ds_star.py`、file analyzer、coder/debug/verify/router 及 LLM helper。brief 给出了任务搬运、调用边界计费和输出评估路线；两者均为同一 DA-Code 任务，而非跨域替代。 |

## 最高近邻

1. [Fail Loudly: An Auditable Runtime for Agentic Data Analysis (RADAR, 2026)](https://arxiv.org/html/2609.32528)  
   重叠：同为训练免费、CPU runtime evidence、诊断反馈和 DA-Code 静默错误；差别：其公开 Python operator 只记录值、程序输出和 artifact metadata，具体验证覆盖 schema、literal、join 与提交契约，未追踪 Boolean mask 的逐行来源身份。

2. [Supporting Better Insights of Data Science Pipelines with Fine-grained Provenance (2024)](https://arxiv.org/html/2310.18079)  
   重叠：为 pandas/dataframe 的 selection、行和元素建立细粒度 provenance，并假设可唯一标识输入行；差别：目标是流水线 provenance 捕获与事后查询，没有检测陈旧 mask 来源与当前目标行的错配，也没有同预算 agent 修复回路。

3. [Fine-Grained Lineage for Safer Notebook Interactions (NBSafety, 2021)](https://arxiv.org/abs/2012.06981)  
   重叠：用 runtime tracing 与 lineage 识别陈旧状态，并以重新执行解决依赖失效；差别：检查单元格、符号和 notebook 全局状态，不区分 dataframe 内业务行身份，也不处理 pandas 标签合法但语义错配的 Boolean mask。

```json
{"score":8.0,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"窄机制组合具有独立新意：已有工作分别覆盖数据分析 agent 的静默错误、细粒度 dataframe provenance 和陈旧状态 lineage，但未发现 Boolean mask 来源行身份与当前目标行身份的逐位核对、可见错配反馈及其 DA-Code 同预算修复检验。自然错误发生率仍是明确标注且可先行证伪的诊断假设。","closest_neighbors":["Fail Loudly: An Auditable Runtime for Agentic Data Analysis (RADAR, 2026)","Supporting Better Insights of Data Science Pipelines with Fine-grained Provenance (2024)","Fine-Grained Lineage for Safer Notebook Interactions (NBSafety, 2021)"]}
```


主执行器保留的实际风险：

初版行变换覆盖很窄，自然频率可能低。追踪ID不能替代语义意图；位置选择/合法键对齐必须排除。改列值后旧谓词是否有效不在当前保证。简单重算可能始终更便宜，必须以它为硬停止对照。
