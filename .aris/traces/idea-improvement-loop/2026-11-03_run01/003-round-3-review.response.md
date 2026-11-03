## 结论

2026-11-03：总体 **7.5/10，promising_needs_revision**。主贡献是用当前日志内、保持局部与跨步结构的已知事件，实测读取干预的相对收益并迁移为原日志的读取选择；这是有分量且独立的研究主线，但当前最小实验尚不能支持“优于最强固定／混合监控策略”的主张。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---:|---|
| 重要性 | 8.0 | 若关键结果成立，将得到一种不依赖原日志标签、能按当前输入配置监控计算的方法，并回答局部检出与跨步依赖之间怎样分配读取预算；这直接针对长轨迹监控的有效性与成本瓶颈，而非只增加一个诊断分数。 |
| 新颖度 | 8.0 | canary、合成能力测量和上下文路由均已有先例；本案独立增量是把两个实际读取动作作用于同一日志中的结构化正负对照，以动作收益差选择原日志动作。检索未发现最高近邻已经做了这一完整机制；去掉任何一篇起点论文的名称，它仍成立。 |
| 有效性 | 6.0 | 当前依据是局部证据随长度退化、状态／多跳监控失败，以及局部检索与变量追踪的能力分离，适用于日志确有这两类依赖且背景影响可共享的条件。未知的是简单、显式规则下的测试收益差能否预测原攻击收益差；尤其跨块测试被设计为切断依赖，其全文优势部分由构造决定，不能直接作为真实违规需要全文的证据。[原始局部监控研究](https://arxiv.org/html/2605.12366v1)、[SLEIGHT](https://arxiv.org/html/2605.16626v2)、[RULER](https://arxiv.org/html/2404.06654v1)。 |

这是原问题的邻近子问题：它研究可观察工具转录的读取方式，未回答真实奖励训练改变 CoT 信息后监控是否仍可靠；这种转向本身不构成扣分理由。

实验的主结果落在未插入测试的原攻击／良性转录上，按原攻击组留出、让无探针对照支配节省的计算，并检查跨步消融与收益置乱，这些设计能够辨别“测试通过”是否转化为目标监控收益；不需要把自然部署标签或执行成功标签混进来。但**目前列出的固定对照不充分**：Classifier Context Rot 已直接报告提醒提示、增加推理和更频繁监控的收益；SLEIGHT 已提供通用 State Tracking 等定向提示，并显示提示间具有互补性。当前全文／四块／固定混合若只使用一个基础提示，不能代表同模型、同额度下最强的固定或混合监控。特别是提醒提示不依赖代理工具、不需要测试攻击标签，能在现有预算内形成直接竞争。这是“更好的检出—成本曲线”主张的对照阻断，而非要求复现不同模型的 Claude Code 成绩。[监控缓解措施](https://arxiv.org/html/2605.12366v1)、[SLEIGHT §5.2 与完整提示](https://arxiv.org/html/2605.16626v2)。

**可行性：pass。** 已核验公开仓库的 FORMAT、解密程序和公开密钥，并在内存中成功解密一个 file/object-reuse 样例：确实含有攻击与良性 JSONL、metadata、description 和 verifier 记录，两份转录均为34个块；因此不是只有字段接口而无实际样本。标签支持“原合成转录描绘攻击还是对应良性行为”，不支持真实 rollout 已造成损害的推断；程序探针标签则只支持其状态机规则是否被违反。[数据与解密入口](https://github.com/safety-research/sleight-bench)、[格式规范](https://raw.githubusercontent.com/safety-research/sleight-bench/main/FORMAT.md)。状态机、正负变体和分块均有可编程路径，不依赖模型创造新能力；已发表提醒及 State Tracking 提示也足够明确，不存在必须获得私有代码的障碍。输入预算不等式成立；模型配置的131072上下文容纳32K／64K条件，8×A100执行冻结20B推理有可信路线，但“约5天”仍是待测吞吐估计，不能写成已核验工期。[模型配置](https://huggingface.co/openai/gpt-oss-20b/raw/main/config.json)。约40个原攻击组只能给宽区间，当前明确不推断1% FPR是正确的。

## 最高近邻

- [Classifier Context Rot: Monitor Performance Degrades with Context Length](https://arxiv.org/html/2605.12366v1)：同任务的长度干预、局部证据插入及提醒／增量监控；未用输入内正负诊断的动作收益差选择读取方式，其代理规则训练迁移失败也提醒本案不能假定测试收益会迁移。
- [SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors](https://arxiv.org/html/2605.16626v2)：提供原攻击／良性配对、状态与多跳盲点，以及通用定向提示和提示互补结果；本案不是新增盲点，而是利用诊断干预进行读取选择。
- [Diagnosing Tool-Selection Reasoning in LLM Agents with Canary Tools](https://arxiv.org/html/2608.04719)：已有可判定、按能力分类的植入测试及其与任务失败的关系；对象是代理选工具，未比较监控读取干预并路由未植入原日志，不能直接充当本任务性能基线。
- [Route Before Retrieve: Activating Latent Routing Abilities of LLMs for RAG vs. Long-Context Selection](https://arxiv.org/html/2605.10235)：已有局部／全局信息需求驱动的成本路由，故不能把两种上下文策略的自适应选择本身称作新意；其信号来自元信息和结构化推理，本案来自同背景内的已知答案干预比较。
- [Synthetic CT as a First Safeguard for Choosing Medical VLMs in Lung Cancer Screening](https://arxiv.org/html/2606.29232)：已有用合成真值测量能力、迁移模型选择到无标签真实样本的框架；本案区别在逐输入、同背景和同模型读取动作的比较，医学结果不构成本案有效性证据。

```json
{
  "score": 7.5,
  "contribution_scores": {"importance": 8.0, "novelty": 8.0, "effectiveness": 6.0},
  "contribution_assessment": "主贡献是通过当前日志内的局部与跨步正负对照，实测读取干预的相对收益并选择原日志读取动作。针对重要的监控计算分配问题，区别于单一canary难度信号、元信息路由和离线合成能力选择；现有监控退化与依赖结构证据支持6分的有效性预期，但程序测试收益向原攻击收益的迁移及额外读取成本回报仍未知。贡献三维达到数值门槛，当前强对照缺口独立阻断主Claim。",
  "feasibility": "pass",
  "feasibility_reason": "公开加密载荷已在内存中实际解密，确认存在攻击/良性配对与metadata；状态机探针和分块可程序化实现，公开提示可独立复现。131072上下文配置和8张A100支持冻结20B模型32K/64K推理，输入预算不等式成立；5天吞吐与统计精度尚需预研，不能当作已证实结果。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "主Claim要求优于最强固定/混合监控策略，但最小实验仅明确基础全文、四块及其混合，未覆盖同任务已发表且公开可复现的提醒提示和通用State Tracking等互补提示。它们可在同一冻结模型与核心预算下竞争，故现有对照不能辨别收益是否超出已知固定/混合监控改进。"
  ],
  "novelty_conclusion": "未发现完整覆盖同背景内、保持依赖结构的正负事件干预比较并迁移读取选择的近邻；独立新意在动作收益测量，而非canary、合成诊断或路由本身。",
  "closest_neighbors": [
    "Classifier Context Rot: Monitor Performance Degrades with Context Length",
    "SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors",
    "Diagnosing Tool-Selection Reasoning in LLM Agents with Canary Tools",
    "Route Before Retrieve: Activating Latent Routing Abilities of LLMs for RAG vs. Long-Context Selection",
    "Synthetic CT as a First Safeguard for Choosing Medical VLMs in Lung Cancer Screening"
  ]
}
```