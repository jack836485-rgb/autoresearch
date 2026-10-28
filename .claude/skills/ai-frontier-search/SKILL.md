---
name: ai-frontier-search
description: 为其他 skill 提供大厂近期人工智能论文与技术报告的搜索规范，包含领域调研、Research Landscape 与已有方法失败诊断，统一机构白名单、时间范围、来源选择、机构与日期核实及去重。适用于上层任务需要检索大厂 AI 研究资料时引用。
---

# 大厂 AI 论文搜索规范

只负责**找到候选并核实资格**（时间、类型、机构），把带证据的候选交给引用方。精读、评价、落盘由引用方决定。

## 默认参数

| 参数 | 默认值 |
| --- | --- |
| 时间窗口 | 检索当天向前 6 个日历月（目标月无对应日取月末）；日期取会话或时间工具，不用模型记忆 |
| 研究范围 | 整个 AI 领域；用户指定方向时收窄 |
| 机构范围 | 下方白名单，至少一名作者署名机构在其中；引用方可指定子集 |
| 作品类型 | arXiv 论文，及机构正式发布、有技术正文的技术报告 |

用户 > 引用方 > 默认值。检索前说明实际日期范围、领域和机构范围。

## 机构白名单

检索名称只用于发现候选；资格依据是正文作者机构或报告正式署名。

| 机构 | 检索名称／部门 | 官方域名 |
| --- | --- | --- |
| Google | Google Research、Google DeepMind、DeepMind | `research.google`、`deepmind.google` |
| Microsoft | Microsoft Research、MSRA | `microsoft.com` |
| Meta | Meta AI、FAIR、Facebook AI Research | `ai.meta.com` |
| Amazon | Amazon Science、AWS、Amazon AGI | `amazon.science` |
| Apple | Apple Machine Learning Research | `machinelearning.apple.com` |
| NVIDIA | NVIDIA Research | `research.nvidia.com` |
| IBM | IBM Research | `research.ibm.com` |
| Adobe | Adobe Research | `research.adobe.com` |
| OpenAI | OpenAI | `openai.com` |
| Anthropic | Anthropic | `anthropic.com` |
| Alibaba | Alibaba Group/Cloud、DAMO、Tongyi Lab、Token Hub、Amap、Qwen Team、通义 | `alibabacloud.com`、`qwen.ai` |
| ByteDance | ByteDance Research、Seed、字节跳动 | `seed.bytedance.com` |
| Tencent | Tencent AI Lab、Hunyuan、腾讯 | `hunyuan.tencent.com` |
| Baidu | Baidu Research、百度 | `research.baidu.com` |
| Huawei | Noah's Ark Lab、华为 | `huawei.com`、`noahlab.com.hk` |
| Ant Group | Ant Research、蚂蚁集团 | `antgroup.com` |
| Kuaishou | Kuaishou Technology、快手 | `kuaishou.com` |
| SenseTime | SenseTime Research、商汤 | `sensetime.com` |
| DeepSeek | DeepSeek-AI、深度求索 | `deepseek.com` |
| Moonshot AI | Moonshot AI、月之暗面 | `moonshot.ai` |
| Zhipu AI | Zhipu AI、Z.ai、智谱 | `z.ai` |
| MiniMax | MiniMax、稀宇科技 | `minimax.io` |
| xAI | xAI、Grok | `x.ai` |
| Mistral AI | Mistral AI | `mistral.ai` |
| Cohere | Cohere、Cohere Labs | `cohere.com` |
| Sakana AI | Sakana AI | `sakana.ai` |
| Thinking Machines Lab | Thinking Machines | `thinkingmachines.ai` |
| Liquid AI | Liquid AI | `liquid.ai` |
| Reka AI | Reka | `reka.ai` |
| Nous Research | Nous Research、Hermes | `nousresearch.com` |
| World Labs | World Labs | `worldlabs.ai` |
| Physical Intelligence | Physical Intelligence、π0 | `physicalintelligence.company` |
| Black Forest Labs | BFL、FLUX | `bfl.ai` |
| Runway | Runway Research | `runwayml.com` |
| Databricks | Databricks Research、Mosaic AI | `databricks.com` |
| Salesforce | Salesforce AI Research | `research.salesforce.com` |
| Ai2 | Allen Institute for AI、OLMo、Tülu、Molmo | `allenai.org` |
| 北京智源 | BAAI、智源研究院 | `baai.ac.cn` |
| 上海人工智能实验室 | Shanghai AI Lab、InternLM、书生 | `shlab.org.cn` |
| StepFun | 阶跃星辰 | `stepfun.com` |
| ModelBest | 面壁智能、MiniCPM、OpenBMB | `modelbest.cn` |

QS 排名前 50 高校也可纳入。未列出的机构不临时放行。

## 资格核实规则

**机构**
- 依据：PDF 首页／arXiv HTML 的作者–机构对应，或报告正式机构署名／官方发布页声明。
- 不算证据：作者姓名、现雇主、资助或算力、使用某厂模型／硬件、版权页脚、某厂转发。
- arXiv HTML 常丢失机构上标或把机构放在摘要后脚注；作者区不完整时看脚注，仍不行读 PDF 首页。转换缺失不等于没有白名单机构。
- 无法核实 → 标"待核实"并写明缺哪项证据，不计入合格结果。

**时间**
- arXiv 用 v1 日期（API 的 `published`），不用 `updated`。旧作仅新版落在窗口内默认不入选；引用方要求时标"旧作重大更新"并记录两个日期。
- 技术报告用官方首次公开技术正文的日期；先在官方仓库／发布页公开后才上 arXiv 的，取更早日期。模型发布日期不等于报告日期。
- 官方列表和 Semantic Scholar 的 `publicationDate` 可能是会议日期；正文 `Date:` 可能是文稿日期；arXiv ID 不给出确切日期。搜索引擎日期只用于发现。
- 无法核实日期 → 待核实，不填猜测值。

**类型**
- 需有方法、系统、实验或分析的技术正文。纯公告、新闻、营销、只有使用信息的模型卡／system card 不入选，但可顺着找正式报告；名为 model card 而含研究正文的按内容判断。
- 调研／Landscape、系统性比较、实证分析、失败诊断、负面结果、理论反例都可入选，不要求新算法。调研作者在白名单不代表其被引文献也满足条件。
- 预印本不排除，也不写成已同行评审。

## 检索方法

### 1. 工具

必须联网，不能用记忆拼"最新论文"；无实时访问途径时告知引用方。优先复用已有工具（`arxiv`／`research-lit` 脚本、`semantic-scholar`、有凭据的 `exa-search`、项目 `tools/semantic_scholar_fetch.py --date-range 起:止`），只借用检索能力，不继承它们的会议过滤、引用量排序或自动落盘。某入口失败后换另一入口（API、摘要页、HTML 页互为独立入口），不重复重试。

本 skill 脚本（依赖 `beautifulsoup4`；PDF 需 `pymupdf`），调用均为 `python -X utf8 <skill目录>/scripts/<脚本>`：

| 用途 | 脚本 | 进入上下文的内容 |
| --- | --- | --- |
| 抓取 | `批量读取论文.py <ID数组.json> --output-dir <目录> [--abstract] [--limit N] [--start K] [--version V]` | 每篇一行：标题、版本日期、错误；`--abstract` 时加摘要。全文与章节落盘 |
| 机构初筛 | `机构初筛.py <正文目录> <输出.json>` | 计数与未命中清单；作者区不进上下文 |
| 机构核实 | `机构初筛.py <正文目录> --show <ID> ...` | 每家机构命中处前后短片段 |
| 片段 | `检索片段.py <正文.json或.pdf> --query 正则 [--section 标题正则] [--exclude-section 正则]` | 命中片段及所在章节／页码 |
| 整节 | `检索片段.py <文件> --section 标题正则 --reason "要回答的问题"` | 指定章节，受单篇预算截断 |
| 跨论文覆盖 | `覆盖扫描.py <正文目录> [--title 标题正则] 列名=正则 ...` | 论文 × 条件的命中矩阵 |

- **论文全文不进入上下文：** 不用 Read／WebFetch 打开整篇 PDF 或 HTML，也不打开落盘的正文 JSON。非 arXiv 报告用 `curl` 下载 PDF 到引用方的 `资料/`，再用 `检索片段.py`。
- **批量抓取的 stdout 重定向到日志文件**，只回读错误计数；资格先用 `机构初筛.py` 在本地筛，只人工看未命中条目，被引用前再用 `--show` 核实。"internship""work done while at" 一类片段属于弱关联，不算署名。
- `读取研究页.py <URL> [--output 文件] [--link-pattern 正则]`：读官方研究列表（取链接）或单篇 arXiv HTML，保存完整章节。带 `--output` 时 stdout 不含正文。HTTP 200 但只有导航／空壳不算"未检出"。旧缓存没有章节或正文被截断时，`批量读取论文.py` 会重新抓取。
- `检索片段.py`：
  - 默认每篇累计返回 5000 字符（约 1250 tokens），每次最多 3 处、前后各 200 字符；
  - `--list-sections` 默认只列一级标题，配合 `--section` 往下展开；
  - 默认跳过参考文献、相关工作、致谢章节。找实验细节时用 `--exclude-section` 再排除 Introduction 和 Abstract，否则命中多半落在作者自述里；
  - PDF 有目录时按目录切节，没有时按页；
  - 超出预算需 `--budget` 加 `--reason`；调用自动记入同目录 `阅读记录.json`，用 `--summary <目录>` 汇总；
  - 零命中只是关键词级核验，不等于论文未涉及。
- `覆盖扫描.py` 的命中**必须抽查语义**（例如 "uniform credit" 既可能指 GRPO 基线，也可能指一种对照）；零命中只是关键词级结果；"截断"列有标记的论文，结论不可靠。

### 2. 两条路径找候选

- **按机构：** 对每家启用机构查近期论文或读其官方研究列表；无检出也记录已查范围。
- **按方向：** 用领域关键词查 arXiv 与官方来源，再核实机构。用户指定领域时展开为术语、算法名和子问题分别查询，不用一个宽泛词。

领域补充词表：后训练读 [references/后训练检索.md](references/后训练检索.md)；OPD 读 [references/OPD检索.md](references/OPD检索.md)；LLM Agent 读 [references/Agent检索.md](references/Agent检索.md)。

上层需要 Research Landscape 时，额外组合 `survey`、`research landscape`、`systematic study`、`empirical study`、`limitations`、`failure modes`、`when it fails`、`negative results`。用户重点要技术报告时，按模型家族／版本名检索，不只搜标题中的 `Technical Report`。

查询示例（替换实际日期与领域）：

```text
site:arxiv.org "Google DeepMind" "reasoning" after:起始日 before:截止日次日
site:anthropic.com/research "interpretability"
"论文完整标题" arxiv
```

常用入口：[DeepMind](https://deepmind.google/research/publications/)、[Google Research](https://research.google/pubs/)、[MSR](https://www.microsoft.com/en-us/research/publications/)、[Meta AI](https://ai.meta.com/research/publications/)、[Amazon Science](https://www.amazon.science/publications)、[Apple ML](https://machinelearning.apple.com/research)、[NVIDIA](https://research.nvidia.com/publications)、[OpenAI](https://openai.com/research/)、[Anthropic](https://www.anthropic.com/research)、[ByteDance Seed](https://seed.bytedance.com/)、[arXiv](https://arxiv.org/)。

### 3. 覆盖检查

- 大结果集检查实际最早／最晚日期和下一页标记；只覆盖几天就按月份或子问题拆分。"取得很多结果"不等于覆盖了半年。
- 官方列表可能只显示精选或第一页，用"全部论文"或分页；只有按首次公开排序的完整列表才能在越过窗口起点时停止。
- `site:`／日期运算符被忽略或结果跑题时，换原生过滤或学术索引。
- 无检出时换别名、中英文或官方列表，不悄悄放宽时间和机构。官方页受限时改搜"标题 + 机构名"到 arXiv 核实。

### 4. 记录、去重与计数

每个候选记录：原文标题、arXiv ID、链接、首次公开日期、命中机构及证据位置、主题、核实状态（合格／待核实及缺项／排除）。只用摘要和必要片段确认相关性，热度、引用量、SOTA 宣传不替代内容核实。

同一作品的 arXiv、官方 PDF、博客、会议版合并为一项，按 arXiv ID 或明确的标题／版本关系去重；方法简称相同不合并。HTML 抽出"Introduction"等章节名当标题时，从网页标题或 PDF 恢复真实标题。

用户要求 N 篇 = 去重后已核实合格的作品数。可复用本会话已核实的记录，以及引用方工作区中同领域旧 slot 的检索脚本和初筛记录，只对新增时段做增量检索；范围或白名单变化时，重新应用变化的条件。旧记录的初筛如果出自已修复缺陷之前的脚本，引用前要重新核实。

### 5. 结束与交付

达到引用方的数量／预算／覆盖要求即停；未给定时完成机构覆盖、方向补漏和资格核实后停止，之后只针对具体遗漏补搜。

交付核实后的候选及证据和实际检索范围；区分**未检出、访问失败、检出但不合格**，说明未覆盖部分。不把待核实当合格，不为凑数放宽条件。
