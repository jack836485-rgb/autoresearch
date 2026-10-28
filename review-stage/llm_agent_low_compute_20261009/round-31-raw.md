## 结论

**日期：** 2026-10-09  
**Score：** 8.2/10  
**Verdict：** `experiment_ready`  
**新意判断：** 核心 Claim 具有独立性，但独立性严格限于“在编码 agent 修复环内，对共同已执行且测试源码未变的测试做跨轮状态差分，并在固定反馈预算中优先呈现本轮 pass→fail 回归”。TDAD/TestPrune 已覆盖回归测试选择与验证，Squeez/SWE-Pruner Pro 已覆盖工具输出压缩，逐轮测试结果向量也已用于离线轨迹分析；检索到的一级工作没有覆盖上述在线、语义化、同预算的反馈分配机制。MiniSWE 的公开 SWE-bench 配置确实在输出超过 10,000 字符时只保留前后各 5,000 字符，并只暴露命令级 return code；但“新增回归自然落在被裁中段并导致 agent 继续追旧错”仍是待诊断假设，不是已有实证。brief 已明确先测遮蔽频率、失败则停止，因此这不是 Claim blocker。  
**是否值得继续：** 是。公开 benchmark、同任务实现入口和因子化对照均已具备；同一选测策略内固定测试来源、反馈机会和核心预算，并把 Squeez、TestLoc、TDAD 的 CPU/API/索引开销计入，足以区分“选了哪些测试”与“怎样呈现已执行测试”的收益。当前无 fatal novelty、feasibility 或 claim blocker。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| MiniSWE 的固定 head-tail 裁剪可能丢失中段失败，而命令级 return code 不能表达哪一个测试发生状态变化 | 新颖（失败链待实证） | [官方 `swebench.yaml`](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/config/benchmarks/swebench.yaml) 明确执行 10,000 字符阈值及 5,000/5,000 裁剪；代码事实成立，但自然轨迹中的遮蔽频率与因果后果尚未观测。 |
| 对共同执行、测试源未变的 nodeid 做跨轮 pass→fail / fail→pass 差分，并优先分配固定反馈预算 | 部分重合，但核心未被覆盖 | TestPrune 文档已有前后运行回归测试，TDAD 已把 P2P 回归作为指标，Tokenmaxxing 已离线比较逐轮测试向量；三者都没有把跨轮状态变化作为 SWE-bench agent 的在线反馈排序机制。 |
| 单次结构化 pytest 输出、按异常/首项目帧聚类代表失败 | 已被覆盖，不构成独立 Claim | pytest 短 traceback、启发式去重与 Squeez 一类工具输出裁剪已覆盖这一层；brief 已正确把它们仅作为消融/对照。 |
| 不增加 shadow tests、不读隐藏 evaluator，只改变已执行公开测试的呈现 | 新颖的边界限定 | 与 TDAD/TestPrune 的选测机制正交，也没有借助 SWE-bench 的隐藏 F2P/P2P 标签在线决策，使收益可归因于反馈呈现。 |
| 同 actor、同测试来源与核心预算，在每种选测策略内比较 head-tail、单次结构化、聚类、Squeez 与状态差分 | 新颖且可证伪的归因设计 | MiniSWE、TDAD、TestLoc 和 Squeez 均有公开入口；设计把选测与呈现因子分开，并显式计入 CPU、内存、模型及工具调用成本。 |

## 最高近邻

1. [TDAD: Test-Driven Agentic Development](https://arxiv.org/abs/2603.17973)；[官方代码](https://github.com/pepealonso95/TDAD)。同为 SWE-bench 编码 agent 的回归控制，并公开报告 P2P 回归；其核心是变更前图式影响分析、选出并运行受影响测试，不比较相邻轮共同测试状态，也不按状态变化重排反馈。
2. [Can Old Tests Do New Tricks for Resolving SWE Issues? / TestPrune](https://arxiv.org/abs/2510.18270)；[官方代码](https://github.com/IBM/Issue-Test-Localizer)。同样缩小 SWE-bench 回归测试集并提供 `run_tests` 前后验证入口；其贡献是 issue 定位、coverage 与测试集最小化，返回详细单轮输出，未提供跨轮 pass→fail 优先呈现。
3. [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](https://arxiv.org/abs/2604.04979)；[官方代码](https://github.com/KRLabsOrg/squeez)。直接压缩 pytest/stacktrace 等工具输出，且公开 2B 与 150M 路径；它按当前任务从单次原始输出抽取相关行，没有利用前轮同一测试的执行状态，因此是最强呈现 baseline 而非覆盖核心机制。
4. [The Best Programming Language for Tokenmaxxing](https://arxiv.org/abs/2607.22807)。它把每个中间解重新执行并表示为测试结果向量序列，与跨轮状态表示最接近；用途是 MiniLCB 轨迹的离线行为分析，没有把差分反馈给 agent，也不是 SWE-bench 同任务实验 baseline。
5. [SWE-Pruner Pro](https://arxiv.org/abs/2607.18213)；[官方代码](https://github.com/Ayanami1314/swe-pruner-pro)。同在多轮编码 agent 中逐行裁剪工具输出，并在 SWE-bench Verified 报告效果；其机制依赖模型内部表示与训练得到的剪枝头，未显式维护测试状态转换，计算与方法边界均不同。

```json
{"score":8.2,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"窄 Claim 具有独立性：最近工作分别覆盖回归选测、单次工具输出压缩和离线测试结果向量，但未覆盖 SWE-bench 修复环内对共同且测试源未变的已执行测试做跨轮状态差分，并用该差分在同反馈预算下优先呈现新增回归。失败链仍须由预设的自然遮蔽诊断验证。","closest_neighbors":["TDAD: Test-Driven Agentic Development","Can Old Tests Do New Tricks for Resolving SWE Issues? (TestPrune)","Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents","The Best Programming Language for Tokenmaxxing","SWE-Pruner Pro"]}
```
