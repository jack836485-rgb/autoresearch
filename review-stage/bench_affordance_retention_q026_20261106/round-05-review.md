## 结论
2026-11-06，总体 score 5.5，verdict：promising_needs_revision。主贡献是在 SWE-bench Verified 上人为补出"约束类型 × 到达通道 × 轨迹长度"各层，再按 SWE-Together 意图构成加权，用来预测编码 agent 方法的交互增益。框架有新意，所选效应修饰变量也有依据；但贡献目前不够，原因有三。其一，按"方法×层"做加权后外推的做法，核心仍是已知的分层差异（2610.31778、CONPACT、MTAC-IFBench）。其二，这里所谓"从静态测量迁移"，其实是新建了一个合成的准交互评测，而按它自己的成本核算，每个方法花在源端的运行次数比直接跑完整个目标端还多，"不必跑交互评测"这个用处还站不住。其三，识别上有几处缺口：轨迹长度是处理后变量，源与目标的单位和结局也对不上。三项分数都没有达到 8。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 能"给定部署分布预测方法增益"对方法采用者有用，但证据只覆盖编码 agent、一个源和一个目标、约 8 个方法对、两个 30B 级开源执行模型，影响面有限。如果迁移胜过统一折扣，新增的认识是："静态到交互的增益损失有结构，主要由约束的通道和类型承载，可以用一套便宜的分层注入评测来预测。"这条结论值得知道，但它的分量大半已被 2610.31778 预示（该文结论就是基准"compaction-friendly"，只有别处不存在的约束会丢）。另外，按现有预算，每个方法在源端约需 500 次运行（4,000/8），多于目标端完整评测的约 436 次（109×2×2），所以"省掉交互评测"的实用价值目前不成立。剩下的用处只在"目标环境或用户模拟器无法搭建、只有日志意图标注"这种情形，Claim 里需要改写成这个范围。 |
| 新颖度 | 7.0 | 检索 arXiv 和网页，没有找到把因果可迁移性（效应修饰、正值性、按目标分布加权）用于预测 LLM/agent 方法增益的工作。CJE（2512.11150）只在目标端用少量 oracle 校准替代指标并做 transport audit；Agent psychometrics（2604.00594）用 IRT 加任务特征预测模型×scaffold 在新基准上的成功率，预测的不是方法增益，也不处理交互结构。按跨领域迁移规则，新颖度给 7。没给到 8，是因为所需的结构性适配（用干预补正值性）其实就是"新建一个分层合成评测再做后分层"，没有说明朴素迁移在这里具体会遇到什么问题、又如何解决。分层效应本身已有直接近邻报告。 |
| 有效性（先验合理性） | 5.5 | 支持的一面：通道和类型确实修饰效应。2610.31778 给出 SWE-chat 上过程/范围指令的丢失率约为功能需求的 6 倍；CONPACT 报告注入位置影响保留率；HDA 的 `messages[:2]` 截断（已核实：消息超过 40 条后只保留前 2 条和最后 36 条）按构造就会丢掉会话中途的用户消息。所以至少截断类方法对的层间差异，在机制上近乎确定。不利的一面有四处，暂未发现与关键假设直接矛盾的已有数据：(1) 轨迹长度档按"是否超过截断或压缩阈值"划分，而它受方法本身影响，是处理后变量，以它为修饰变量做条件化，识别会有偏。(2) 源端单位是"一题加一条注入的持续约束"，目标端一题平均约 8.7 条意图（943/109），同时分布在多层，结局是合取。如何从各层条件增益合成为题级或单元级增益（加性？各约束保留率相乘？），简报没有给出模型。(3) 构念不一致：已核实 SWE-Together 的 `intent_kind` 是 request/question/correction/context/workflow/verification，并不是功能/过程/范围三分类，要重新标注。会话中途的 workflow 意图多数是"提交一次 git commit"这类一次性请求，交付后立刻执行，不需要跨压缩保留；范围排除类意图很稀疏（粗略正则只命中几十条，且多是 request/correction）。正值性补的是"持续约束"，这和目标端的主体并不同构，"持续 vs 一次性"是一个没有测量的修饰变量，而"目标任务的静态版本"对照分离不了它，correction 类意图放进首轮本身也不好定义。(4) 语言和仓库不同（目标端 typescript 46、go 26、rust 10 个标签，python 只有 11），加上 correction 回路，未测修饰变量的风险很具体。 |
| 待预研 | — | 迁移误差相对静态增益、统一折扣和目标端小样本的大小；压缩类方法在 Qwen 执行模型、SWE-bench 轨迹长度下能否被触发到足以产生层间差异；可检查的目标端过程/范围意图各单元有多少条。 |

与原问题的关系：这是起点问题收窄后的子问题，只回答"一个静态源到一个交互目标"在编码 agent 上是否可预测。跨基准的结构性质评分、留出任务族口径、非编码领域都没有回答。转向本身不构成阻断。

实验能否判别主张：部分能。"迁移 vs 统一折扣"这组对照设计得对，能区分"只是整体打折"和"增益依赖结构"。但有三个问题。(a) 同成本小样本基线的规模算错了：迁移需要的额外运行次数约等于或超过整个目标端，等成本时小样本就等于全量，"约 15 题/方法"不是同成本。(b) 长度层是处理后变量，会混入方法自身的效应。(c) 目标端"方法×层"的观测增益怎么定义（按意图逐条判是否遵守，还是题级），以及它与源端结局"测试通过 ∧ 约束遵守"是否属于同一构念，没有讲清楚。这三处都会让主检验比较到不同的量上。

可行性：pass。核实到的情况如下。SWE-Together 已公开：109 题各有 `oracle_intents.json`、`tests/test.sh` 和 `reference_patch.json`，原生支持 opencode 和 mini-swe-agent，agent 席位支持 vLLM；简报中"92 题有中途非提问意图、workflow 88 条"与数据一致。文档写明 vLLM 只限 agent 席位，把模拟器改为自托管需要改代码，属于可实现的工程。HDA 仓库已公开 `react_baseline.py`、`fresh_context_patch_review.py`（Qwen3.6-27B 目录）和 `loop_break_context_excision.py`；注意后者是为 Qwen3-30B-A3B-Instruct-2507 演化出来的，并非为 Qwen3-Coder-30B。compaction 的代码仓库（aisa-group/compaction、ZhiqiEliWang/compaction-integrity）在论文中有链接，三个 Qwen 模型在 HF 上都可获取。约 6,200 次运行，30 路并发，单次约 20 分钟，大约 3 天，能放进 8×A100 的 5 天上限；但 task.toml 写的是每容器 4 CPU/4G（不是 8G），30 路并发需要约 120 个 CPU 核，要事先确认主机核数。API 只用于 Haiku 校准，在预算内。

## 最高近邻
1. Benchmarks Are Surprisingly Compaction-Friendly（https://arxiv.org/abs/2610.31778）：重叠在于它给出了按约束类型分的丢失率，并论证静态基准的结构会让压缩显得无害，这正是本 Idea 修饰变量的来源。差别：它不做跨分布的增益预测。
2. Lost in Context Compaction / CONPACT（https://arxiv.org/abs/2608.11242）：重叠在于注入位置、表述方式会调节约束保留，并提出了 SC 提取器（本 Idea 的方法对之一）。差别：只测保留和遵守，不做迁移。
3. SWE-Together（https://arxiv.org/abs/2606.29957）：本 Idea 的目标分布和目标评测，提供意图标注与模拟器。差别：它评测的是模型，不是方法增益，也不做预测。
4. Harness-Delta Attribution（https://arxiv.org/abs/2610.22466）：重叠在于检验 harness 演化增益在留出集上是否保留，并提供了基线和演化产物。差别：做的是归因和保留检验，不按部署分布预测。
5. Causal Judge Evaluation（https://arxiv.org/abs/2512.11150）：重叠在于用因果框架处理"评测指标能否迁移到部署"，带 transport audit，在目标端用少量 oracle 校准。差别：它校准的是替代指标，不处理效应修饰的正值性，也不预测方法增益。本 Idea 把它当同成本对照是合理的，但同成本的规模需要重算。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 7.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献：在静态源上用内容保持型切换补出约束通道×类型×长度各层，再按交互目标的意图构成加权，预测编码agent方法的交互增益。新颖度7：LLM/agent评测中未检出可迁移性框架，属跨领域迁移，但结构性适配只是新建分层合成评测加后分层，分层效应已有近邻报告。重要性6：覆盖窄；按现有预算每方法源端约500次运行，多于目标端完整评测约436次，'省掉交互评测'的用处不成立，只在目标环境不可得时成立。有效性5.5：通道/类型修饰效应证据充分，HDA截断按构造丢中途消息；但轨迹长度是处理后变量，源端单约束单位与目标端多意图合取结局之间缺少合成模型，目标中途意图多为一次性请求，而非源端注入的持续约束，且需把intent_kind重标注为三分类，语言与仓库差异是具体的未测修饰。待预研：迁移误差相对统一折扣的大小、压缩在Qwen与SWE-bench长度下的触发率、目标端可检查意图在各单元的数量。",
  "feasibility": "pass",
  "feasibility_reason": "已核实SWE-Together公开109题，含oracle_intents、tests和reference_patch，原生支持opencode/mini-swe-agent且agent席位支持vLLM（模拟器自托管需改代码，可行）；HDA仓库公开react_baseline、fresh_context_patch_review和loop_break_context_excision（后者为Qwen3-30B-A3B-Instruct-2507演化）；三个Qwen模型可获取；约6200次运行、30路并发约3天，在8×A100 5天内，需确认主机约120核CPU；API只用于校准，在预算内。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：三项分数为6/7/5.5，没有一项达到8，有效性低于6",
    "Claim阻断：同成本目标端小样本基线规模算错，迁移每方法源端运行次数（约500）已超过目标端全量（约436），'同成本不劣于小样本'与'省掉交互评测'的主张无法按所述方式检验",
    "识别阻断：轨迹长度档（是否超过截断或压缩阈值）受方法影响，是处理后变量，不能作为效应修饰层直接条件化",
    "Claim阻断：源端'单题单条注入持续约束'的分层条件增益，如何合成为目标端多意图合取结局下的单元或题级增益，没有给出模型；目标端'方法×层'观测增益的定义与源端结局不是同一构念（目标端中途意图多为一次性请求，intent_kind需重标注为三分类）"
  ],
  "novelty_conclusion": "在LLM/agent评测中未检出用可迁移性或效应修饰框架预测方法增益的工作，新颖度按跨领域迁移给7；分层差异本身已由2610.31778、CONPACT、MTAC-IFBench报告，CJE与Agent psychometrics是方法上的邻近工作但对象不同。",
  "closest_neighbors": [
    "Benchmarks Are Surprisingly Compaction-Friendly (arXiv:2610.31778)",
    "Lost in Context Compaction: When LLM Systems Drop Side Constraints (arXiv:2608.11242)",
    "SWE-Together: Evaluating Coding Agents in Interactive User Sessions (arXiv:2606.29957)",
    "Harness-Delta Attribution: Dissecting Gains From Harness Evolution (arXiv:2610.22466)",
    "Causal Judge Evaluation: Calibrated Surrogate Metrics for LLM Systems (arXiv:2512.11150)"
  ]
}
```
