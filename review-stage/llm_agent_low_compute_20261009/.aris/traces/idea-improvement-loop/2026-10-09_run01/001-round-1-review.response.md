## 结论

**日期：2026-10-09。Score：3.0/10。Verdict：`needs_rethink`。**

核心机制的新意不足：已有工作已经覆盖“沿依赖关系追踪错误影响、失效下游派生状态、保留无关状态并选择性重放”。当前差别主要是把该机制用于 ToolMaze P3/P4，并让模型显式报告消费的结果 ID，尚不足以形成独立方法 Claim。

ToolMaze 上“重取正确值后仍复用旧值”以及“收益只出现在已下游消费组”仍可能是新的实证发现，但目前只是待验证假设。实验设计具有可证伪性，预算约束也较清楚；然而缺少最接近回滚方法在同一 ToolMaze 任务上的公开实现与具体复现路线，属于致命可行性阻塞。已消费/未消费分层又由方法自身生成的依赖边定义，缺少独立可核验标签，构成 Claim 阻塞。

**当前形态不值得进入实验规划。** Fatal blockers：`core_mechanism_covered`、`missing_same_task_closest_baseline_reproduction`、`consumption_strata_not_independently_verifiable`。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| ToolMaze 中语义错误会被下游消费和传播 | 已被覆盖 | [ToolMaze](https://arxiv.org/abs/2606.05806) 已展示 P3/P4 错误被接受并传播到下游调用；这不是新发现。 |
| 重取正确值不会自动撤销基于旧值形成的判断 | 部分重合 | 依赖污染残留已被 [Yu et al.](https://arxiv.org/abs/2608.10502) 和 [MEMOREPAIR](https://arxiv.org/abs/2605.07242) 明确论证；但 ToolMaze 中“重取后仍复用旧值”的频率尚未被当前材料证明，只能作为诊断假设。 |
| 按实际消费边失效局部结论并选择性重验 | 已被覆盖 | Yu et al. 已构建 memory-to-action 依赖图、失效不再受支持的状态并选择性重放；MEMOREPAIR 已撤销失效后代并从保留支持重建后继；ReflectAgent 也用数据依赖图定位并回滚工具链。 |
| 模型同轮标注所消费结果 ID，CPU 沿边传播失效 | 部分重合 | 显式结果 ID 是实现差别，但依赖记录、污染传播和局部重放机制已有直接近邻；单纯换一种依赖边采集方式不足以支撑核心新颖性。 |
| 仅已消费组获益、未消费组不获益可证明机制 | 新颖但未证实 | 这是清楚且可证伪的交互假设；但分组来自模型自报依赖，若无独立标注或可核验插桩，结果会由方法自身定义。 |

## 最高近邻

1. [From Faulty Memories to Corrected Actions](https://arxiv.org/abs/2608.10502)：几乎同构地追踪显式下游依赖、失效旧状态并选择性重放。差别是其故障源为持久记忆，当前方案聚焦 ToolMaze 的工具观察替换。

2. [MEMOREPAIR](https://arxiv.org/abs/2605.07242)：已提出撤销失效后代、利用保留支持重建后继及成本约束修复。差别是目标为 agent memory 的级联更新，而非单条工具轨迹中的观察消费。

3. [ReflectAgent](https://openreview.net/pdf?id=hV2YxBlo0g)：直接面向多步工具链，以数据依赖图定位根因并从根步骤重执行后缀。当前方案使用在线显式消费边和受影响子图；其公开实现与稳定复现入口未核验。

4. [Generator-Assistant Stepwise Rollback](https://aclanthology.org/2025.emnlp-main.892/)：已处理错误推理向后传播并触发步骤级回滚，且有[公开代码](https://github.com/wisper12933/GA-Rollback)。差别是依靠 assistant 审查，没有显式观察依赖失效，也没有 ToolMaze 复现路线。

5. [When Tools Fail / ToolMaze](https://arxiv.org/abs/2606.05806)：已给出隐式错误传播、重试与改道失败的直接任务证据及[官方代码](https://github.com/Zhudongsheng75/ToolMaze)。差别是未专门测量“重取正确值后仍引用旧值”，也未实现局部结论失效。

```json
{"score":3.0,"verdict":"needs_rethink","fatal_blockers":["core_mechanism_covered","missing_same_task_closest_baseline_reproduction","consumption_strata_not_independently_verifiable"],"novelty_conclusion":"核心依赖失效与选择性重放机制已被直接近邻覆盖；剩余潜在新意仅是ToolMaze上的陈旧依赖实证及消费组交互，但当前分层缺少独立真值，且没有最接近方法的同任务公开复现baseline。","closest_neighbors":["From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents","MEMOREPAIR: Barrier-First Cascade Repair in Agentic Memory","ReflectAgent: Diagnose, Localize, and Rollback Errors in Multi-Step LLM Tool-Use Chains","Generator-Assistant Stepwise Rollback Framework for Large Language Model Agent","When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents"]}
```