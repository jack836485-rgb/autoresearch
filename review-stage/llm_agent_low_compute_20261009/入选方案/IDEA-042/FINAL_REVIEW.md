## 结论

**日期：** 2026-10-09  
**Score：** 7.9/10  
**Verdict：** `experiment_ready`  
**新意判断：** 组件级新意有限，但组合机制具有可辨认的新意。AST clone 对齐、anti-unification、历史 co-change、变化点/clone 重构和 LLM 自动重构均有直接先例；我未检索到已有工作同时做到：以逐轮公开 spec 与代码 diff 对齐变化孔、只用已观察到的单轴差异作为独立抽象证据、禁止利用未来 checkpoint，并以同一迭代编码 agent 的下一 checkpoint 严格正确率/成本作为成败标准。该边界足以进入实验规划，且 Claim 已把“clone 抽取导致后续再次切开”写成待验证假设，没有冒充已观察事实。

**是否值得继续：** 是。SlopCodeBench 的公开仓库已包含 MiniSWE actor、`configs/agents/miniswe.yaml`、`anti_slop.jinja` 和 `plan_first.jinja`，同任务基线与隐藏离线评测路线可核验。一个非致命复现缺口是：当前公开 `AgentCostLimits` 原生提供 step/cost/net-cost 限制，没有 brief 所称的总 token 硬上限；因此“`cost_limits` 直接指定相同 step/token/cost”这一实现陈述不准确，但不改变机制新意或实验的基本可证伪性。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 迭代 spec 扩展会造成结构侵蚀和复制增长，通用 clean-code / plan-first 提示不能停止退化 | 已被覆盖 | [SlopCodeBench](https://arxiv.org/abs/2603.24755) 已定义同一失败，并报告结构侵蚀、verbosity 随 checkpoint 增长；其提示实验降低初始侵蚀/verbosity，却没有停止退化，且平均增加成本、降低严格正确率。 |
| 仅按 AST 近似重复抽函数会混合真实变化维度，造成下一次扩展再次切开 | 新颖的待验证因果假设 | anti-unification clone 抽取和 clone evolution 已有，但检索到的一级工作没有在迭代 spec agent 轨迹中验证“错误合并变化轴 → 下一 checkpoint 再分裂 → 同预算成功率下降”这条因果链。 |
| AST 对齐与 anti-unification 产生骨架/孔，再把孔绑定到当前 spec 的变化维度 | 部分重合 | [Li & Thompson 2011](https://www.cs.kent.ac.uk/pubs/2011/3087/) 已用 least-general common abstraction/anti-unification 增量检测并消除近似 clone；需求到代码的变化绑定和 variation-point 分析也属既有方向。差别在于本方案用逐轮自然语言 spec diff 约束同一 agent 工作区中的孔语义。 |
| 只有出现至少两个已观察实例且存在单轴差异时才抽象；联合变化或无证据孔不独立抽象 | 部分重合但边界独立 | [CREC](https://arxiv.org/abs/1807.11184) 已用 clone 当前结构、历史演化和 co-change 关系推荐重构；既有 clone/产品线工作也分析变化点。本方案的“单轴分离证据”是更窄的在线判定，不训练分类器、不预测未来需求，也不从多个产品变体恢复完整 feature model。 |
| 在同一 SlopCodeBench MiniSWE、同一累计 workspace 和同预算下，以后续 checkpoint 严格正确率/成本否证机制，并设 clone-only、固定重构和 from-scratch 控制 | 新颖 | [公开实现](https://github.com/SprocketLab/slop-code-bench) 能运行同任务 actor 与原提示基线；SlopCodeBench 本身只评测提示干预，未提供变化轴约束重构。主终点面向未来扩展而非自优化的 CC/clone 指标，且明确规定若未来正确率/成本无改善即否定研究。 |

## 最高近邻

1. [SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks](https://arxiv.org/abs/2603.24755)（[代码](https://github.com/SprocketLab/slop-code-bench)）。任务、失败现象、结构侵蚀指标和 anti-slop/plan-first 基线完全同域；它测量退化与提示干预，不提出基于已观察变化轴的 clone 重构机制。

2. [MaintainCoder: Maintainable Code Generation Under Dynamic Requirements](https://arxiv.org/abs/2503.24260)（[代码](https://github.com/IAAR-Shanghai/MaintainCoder)）。同样以动态需求下后续修改正确性和维护代价为目标；其机制是预先的需求分析、设计模式与多 agent 架构，不从自身逐轮 diff 提取单轴分离证据，实验任务也不是 SlopCodeBench。

3. [Incremental Code Clone Detection and Elimination for Erlang Programs](https://www.cs.kent.ac.uk/pubs/2011/3087/)。直接覆盖 anti-unification、least-general common abstraction 和增量 clone 消除；不使用 spec 变化轴决定哪些孔应联合或独立变化，也不评价后续需求完成率。

4. [Automatic Clone Recommendation for Refactoring Based on the Present and the Past](https://arxiv.org/abs/1807.11184)（[代码](https://github.com/soniapku/CREC)）。直接使用 clone 的当前结构、历史演化和 co-change 特征决定重构候选；它学习“哪些 clone 值得重构”，不生成由当前 spec 差异约束的参数化骨架，也不在编码 agent 的下一 checkpoint 上检验收益。

5. [REFINE: A Multi-Agent LLM Approach for Evidence-Guided Code Refactoring](https://arxiv.org/abs/2608.23611)（[公开实现](https://anonymous.4open.science/r/REFINE/README.md)）。代表最近的 evidence-guided 自动重构：静态 smell 驱动规划、LLM 变换和 preservation checks；证据针对当前 Java 文件的 smell 与静态保持性，不是历史 spec 变化独立性，论文也明确未证明 repository-level 行为保持。

```json
{"score":7.9,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"AST anti-unification、clone evolution/co-change 与 LLM 自动重构均非新颖；新意在于把逐轮 spec 差异绑定到 anti-unification 孔，只凭已观察单轴差异触发保守抽象，并在同一 SlopCodeBench 轨迹上以后续 checkpoint 的同预算正确率和成本进行否证。未发现该完整机制已被覆盖。","closest_neighbors":["SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks","MaintainCoder: Maintainable Code Generation Under Dynamic Requirements","Incremental Code Clone Detection and Elimination for Erlang Programs","Automatic Clone Recommendation for Refactoring Based on the Present and the Past","REFINE: A Multi-Agent LLM Approach for Evidence-Guided Code Refactoring"]}
```


主执行器保留的实际风险：

需求维度解释仍依赖actor，少量实例不证明未来独立性。当前clone指标降低可能只是优化指标，没有维护收益。AST对齐和重构开销可能更贵；不能用隐藏下一轮规格、完美人工轴标签或额外重构预算制造优势。
