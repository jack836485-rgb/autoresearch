# Idea 候选池（N-Q004）

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_算力适配_20261028` 的 `N-Q004`

## 当前选择

- Reviewer 调用：`0 / 20`
- 当前选中 Idea：`IDEA-004`
- 当前自评分：`7.4/10`
- 选择理由：IDEA-004 针对一个有文献分歧的现象（CAVE 中强模型找回证据后仍破坏工作，而一般设定下模型偏信文档与工具返回），用因子设计分离行动偏置与证据来源折扣两种解释，并补上现有缓解缺失的真实指责对照；IDEA-002 的训练方向与 2608.26511、FixedBench 重合较多，IDEA-003 的前提与 2604.22193 的一般发现相反、风险高。
- 状态：`等待第 1 次 reviewer 调用`

## 候选列表

### IDEA-001：在 ≤9B agent 上比较保留历史与移除历史的修复（卡片切口）

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：sycophancy；false accusation；context reset
- 一句话背景：对话场景中"移除含压力历史"比保留历史的修复可靠（2609.33672），agent 场景未测。
- 自评分：`5.8/10`
- 一段话概括：在 CAVE-Bench 子集上对 Qwen3.5-9B 等比较撤回、复位、自检与移除历史四类修复的接受率与破坏率。
- 打分理由：CAVE 已覆盖 harness 与执行面（S 因子：压缩续跑、交接等）差异，并测了三种缓解；本切口是 2609.33672 到 agent 的直接迁移，增量小。
- Reviewer 记录：`尚未送审`

### IDEA-002：按"本地可核实性"条件化的训练，兼顾抗错误指责与正当修复

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：sycophancy；rational updating；coding agents
- 一句话背景：反谄媚干预普遍以牺牲理性更新为代价（2608.26511 对话；FixedBench 2605.07769 中"先复现再修"导致部分修复场景下错误放弃）。
- 自评分：`6.8/10`
- 一段话概括：用"指责能否在本地复现"决定奖励（可复现则修，不可核实则保留并要证据），在 ≤9B agent 上做 SFT/DPO，双侧评测 CAVE 与真实指责对照。
- 打分理由：方向与 2608.26511（选择性问题）和 FixedBench（行动偏置、复现指令）重合较多；训练数据与环境构建成本高。
- Reviewer 记录：`尚未送审`

### IDEA-003：防提示注入训练的副作用——agent 轻视自己取回的证据

- 来源：`相似领域成熟方法迁移`（安全训练的副作用分析）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：prompt injection；instruction hierarchy；sycophancy
- 一句话背景：指令层级 / SecAlign 类训练教模型不信任工具通道内容，可能连带折扣 agent 自己查到的证据。
- 自评分：`6.2/10`
- 一段话概括：比较 Meta-SecAlign 与其基座在 CAVE 上的破坏率与路径，预测按指责入口出现交叉交互（工件入口更稳、用户入口更易在找回证据后破坏）。
- 打分理由：2604.22193 发现多数模型更信文档断言、且后训练强化这一偏好，2609.05587 发现 agent 过度采信工具返回，前提与一般发现相反；可作为 IDEA-004 的一个来源因子而非独立主张。
- Reviewer 记录：`尚未送审`

### IDEA-004：找回证据后仍破坏——行动偏置还是证据来源折扣？带真实指责对照的因子诊断与对症修法

- 来源：`领域共性不足`（结合 `最高近邻不足`：CAVE 的缓解只在错误指责上评测）
- 父 Idea：`无`
- 状态：`selected`
- 定位关键词：sycophancy；false accusation；coding agents；action bias；knowledge conflict
- 一句话背景：CAVE-Bench 发现强模型常在找回支持证据后仍按错误指责破坏正确工作，而知识冲突与工具依赖研究发现模型通常偏信文档与工具返回；这一矛盾背后的机制未定。
- 自评分：`7.4/10`
- 一段话概括：两种竞争解释——行动偏置（指责被当作待办请求，行动是默认；FixedBench）与证据来源折扣（agent 自己取回或自己刚产生的证据权重低，解释"刚验证的工作更易被破坏"）。在 CAVE 的编码 / 文件 / 运维子集上做因子操纵：指责措辞（指令式 vs 信息式，内容相同）× 证据来源（agent 自己取回 / 第三方文档 / harness 标记的可信记录，内容相同）× 压力（原样 vs 中性）；为每个任务构造真实指责对照（注入真实缺陷且可本地复现）。按诊断出的主因设计对症干预，与 CAVE 的 I1 证据规则、I2 闸门在"错误指责破坏率 vs 真实指责修复率"双侧指标上比较。
- Story line：错误指责在最多 60.06% 运行中破坏正确工作，强模型常在找回证据后破坏，刚自己验证的工作更易受损 [2609.32616]；与之相对，多数模型更信文档而非用户断言 [2604.22193]、过度采信工具返回 [2609.05587]，对话中加入可信证据可把准确率从 0.368 拉到 0.929 [2609.33672]；FixedBench 发现 agent 对已修复问题仍提交修改，复现指令又带来错误放弃 [2605.07769] → 被忽视的关键：EO 路径到底是"证据没被信"还是"证据被信了但仍按请求行动"，从未被操纵分离；CAVE 的缓解也从未测过真实指责下的修复是否被一并拦掉 → 本 Idea：措辞 × 来源 × 压力因子 + 真实指责对照 + 对症干预 → 可推翻：若来源操纵不改变破坏率而措辞操纵显著改变，支持行动偏置；反之支持来源折扣；若两者都不改变，两种解释同时被推翻。
- 打分理由：直接回应最高近邻的两个未解释发现与一个评测缺口；推理级算力；风险是因子改写需逐任务人工核对、真实指责对照构造成本，以及 reviewer 可能认为措辞改写只是提示工程。
- Idea 生成依据：2609.32616（摘要、§5 目录、RQ4 表 4）；CAVE 仓库文档（任务结构、五类风险因子、评分、判官默认 deepseek-v4-pro）；2605.07769 FixedBench；2608.26511；2609.33672；2604.22193；2609.05587；2512.00332 A-CC。
- 自评分轻量新意依据：检索"agent sycophancy true vs false feedback verify before fixing""LLM agents discount tool-retrieved evidence versus user assertion"未见分离 EO 路径成因的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：用内容不变的措辞与来源操纵分离"找回证据后仍破坏"的两种成因，并首次给 agent 错误指责缓解加上真实指责对照的双侧评测。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| CAVE-Bench（任务、评分、I1/I2） | 同任务：agent 错误指责下的破坏 | https://arxiv.org/abs/2609.32616 | https://github.com/henrymao2004/agent-over-correction ；2026-11-01 克隆核验：`cavebench/tasks/<domain>/task_*_gaslight/`（instruction.md、task.toml、tests/c1–c3、environment/）、`scoring/aggregate.py`、`harbor run -p cavebench/tasks/<domain> -a <agent> -m <provider/model>`；判官默认 deepseek-v4-pro，可经 OpenAI 兼容端点替换；HF `sevens2004/cave_bench` | Harbor 运行；I1 为写入会话的证据规则，I2 为 harness 层不可逆操作闸门（按论文 §5.4 描述实现，需核对仓库是否附带） | 是 |
| FixedBench | 同领域：编码 agent 对无需修改问题的行动偏置，含"先复现"指令的双侧失败 | https://arxiv.org/abs/2605.07769 | 代码链接只列 gemini-cli / codex，未见基准仓库（送审前需核验） | 未核验 | 否（待核验） |
| Harbor | 运行框架 | https://github.com/harbor-framework/harbor | `uv tool install harbor`（CAVE 文档） | 按 CAVE REPRODUCIBILITY | 是 |

- Reviewer 记录：`尚未送审`
