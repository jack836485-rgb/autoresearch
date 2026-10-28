## 结论

**日期：2026-10-09；score：6.9/10；verdict：`promising_needs_revision`。** 新意主要在同一组合：把 ScrambleToolBench 的不完整旧映射表示为“新观测硬约束、旧映射软优先”的二分图可行集，并以当前目标而非全图恢复来选择 probe。检索未发现此前工作在该 benchmark 上同时实现这三点；但候选集约束传播与最坏分支探针选择属于经典 generalized binary search / active diagnosis 范式，因而是新的任务化机制组合，而不是新的基础算法。值得继续，但当前不能进入实验规划：存在两个 fatal feasibility blockers。第一，[官方 ScrambleToolBench 代码](https://github.com/declare-lab/ScrambleToolBench/blob/main/src/agent.py) 的 `get_agent_class` 只接受 `default`，未见 `MemoryAgent` 或 `memory` 分支，和 brief 所称“default 与 memory 通过 get_agent_class 进入”直接冲突。第二，所谓“熵最大 probe”实际只最大化可区分行为类别数，没有概率分布、匹配后验或熵计算；它不是可核验的信息增益基线，因而目前不能支持“超过泛信息策略”的核心比较。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 漂移后穷举、旧 belief 固化，且 cycle tracing 的保证依赖漂移前完整映射 | 已被覆盖 | [ScrambleToolBench](https://arxiv.org/abs/2608.02358) 已直接报告 belief inertia、穷举与未采用 cycle tracing；论文还明确说明 cycle tracing 从 Task 2 起的保证要求第一次漂移前已识别全部函数，并观察到两个模型在 Task 1 均未完成全图发现。 |
| 不完整旧图中将 fresh observation 作为硬约束、旧映射仅作软优先，并用一一对应匹配传播维护候选 | 部分重合 | 对 ScrambleToolBench 的具体状态语义未检索到先例；但约束满足、候选诊断和逐观测消元是既有 active diagnosis 方法，算法骨架本身不新。 |
| 只恢复当前任务所需能力，并选取使最坏结果分支后的目标候选数最少的 probe | 部分重合 | 目标条件化的 ScrambleToolBench 实例未见覆盖；但“在候选假设集上选择最均衡/最有辨别力查询”已由 [Noisy Generalized Binary Search](https://papers.neurips.cc/paper_files/paper/2009/hash/556f391937dfd4398cbac35e050a2177-Abstract.html) 和 [Efficient Test Selection in Active Diagnosis](https://arxiv.org/abs/1207.1418) 覆盖。 |
| 同一不完整历史与预算下，目标候选 probe 比 cycle tracing、全图信息策略减少定位调用并提高完成率 | 新颖但未支持 | 这是清楚且可证伪的经验 Claim，现有 ScrambleToolBench 没有报告该比较；但当前 `memory` 复现声明与官方代码不符，且“熵最大”比较器定义错误，实验闭环尚未成立。 |
| timeout 不删除能力边可避免把瞬态失败误判为结构漂移 | 部分重合 | [When Tools Fail / ToolMaze](https://arxiv.org/abs/2606.05806) 与 ScrambleToolBench 已区分瞬态故障和结构变化；本 brief 的保守更新规则是合理实例化，但不是独立的新颖贡献。 |

## 最高近邻

1. [ScrambleToolBench: Agents Search Exhaustively Even When Their Own Map Points to the Next Step](https://arxiv.org/abs/2608.02358)（[代码](https://github.com/declare-lab/ScrambleToolBench)）：同一 benchmark、mapping drift、behavioral reasoning 与 cycle tracing，且直接暴露不完整发现问题；差别是它没有提出面向当前目标的候选匹配控制器。官方代码当前只可直接运行 `default`，未实现 brief 所称的 `memory` agent。
2. [OpaqueToolsBench: Learning Nuances of Tool Behavior Through Interaction](https://arxiv.org/abs/2602.15197)（[代码](https://github.com/shallinan1/OpaqueToolsBench)）：同样从交互反馈学习不透明工具行为并强调 test-time 探索成本；差别是 ToolObserver 迭代改写工具文档，未处理跨任务的一一映射漂移或目标条件化 probe。
3. [SING: Synthetic Intention Graph for Scalable Active Tool Discovery in LLM Agents](https://arxiv.org/abs/2606.16591)：同样按当前意图/子目标主动缩小工具集合；差别是它从有语义描述的大型工具库做检索，不通过行为观测恢复匿名 alias 的变化映射。
4. [Noisy Generalized Binary Search](https://papers.neurips.cc/paper_files/paper/2009/hash/556f391937dfd4398cbac35e050a2177-Abstract.html)：与“选 probe 使剩余候选最小”的决策原则高度重合；差别是通用假设识别理论，不包含 LLM 工具调用、旧映射语义或 drift benchmark。
5. [Lomekwi: Resource-Bounded Tool Discovery in LLM Agents](https://arxiv.org/abs/2607.16961)：共同关注有限资源下的工具发现效率；差别是其对象是发现/构造工具机会与认知分解，不是匿名工具映射恢复。

```json
{"score":6.9,"verdict":"promising_needs_revision","fatal_blockers":["官方 ScrambleToolBench 仓库的 get_agent_class 当前仅接受 default，未提供 brief 声称已核验的 memory agent/复现入口，因而关键同任务 baseline 不可按所述路线复现。","标作‘熵最大 probe’的 baseline 只最大化可区分行为类别数，未定义或计算结果概率、匹配后验熵或期望信息增益；这是基线定义错配，无法支撑超过泛信息策略的核心 Claim。"],"novelty_conclusion":"未发现既有工作在 ScrambleToolBench 的不完整旧映射条件下，同时采用 fresh-hard/old-soft 的一一匹配约束、面向当前目标的候选消减和同预算主动 probe；组合有新意，但其算法骨架属于经典 generalized binary search / active diagnosis，当前又有两个基线可复现性阻断。","closest_neighbors":["ScrambleToolBench: https://arxiv.org/abs/2608.02358","OpaqueToolsBench: https://arxiv.org/abs/2602.15197","SING: https://arxiv.org/abs/2606.16591","Noisy Generalized Binary Search: https://papers.neurips.cc/paper_files/paper/2009/hash/556f391937dfd4398cbac35e050a2177-Abstract.html","Lomekwi: https://arxiv.org/abs/2607.16961"]}
```
