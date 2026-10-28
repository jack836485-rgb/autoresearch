# Round 1 Review（常规审查，Opus 5.5，effort high）

## 结论
日期：2026-10-22。评分 **4.5/10**，结论 **needs_rethink**。

核心的"覆盖规律"已有人明确写过。ContextLift（2610.21633）的结论原文是 "A data-side defense covers only what its data carries: output-format or system-prompt triggers are out of scope unless the finetuning prompts contain them"，Limitations 里也承认 cue 只覆盖用户轮处境句。Dubiński et al.（2604.25891）已经证明交织和事后良性微调都会留下条件失配，并且触发只出现在 "inputs sharing features with the training data" 上。因此 Claim 1 的定性部分和 Claim 3 的前提都来自已有工作。剩下的新东西只有两点：独占度到条件失配率的定量单调关系，以及只凭数据统计预先给触发排序。

最小实验有可行性硬伤：ContextLift 的 security、legal、medical 三个数据集都只有 user/assistant 两轮，没有系统提示；格式类和系统提示类触发只在 code 上覆盖，而该 organism 在 Qwen2.5-7B 上无效。所以非用户轮特征族在 D_h 中的独占度接近 0，覆盖匹配缓解会退化成 ContextLift 加复制；"留出特征族"的检验也没有定义清楚。

结论：方向（数据侧预测触发）还可以做，但当前的 Claim 边界和实验设置撑不起来。

## Claim 判断
| Claim | 判断 | 关键依据 |
|---|---|---|
| 1a. 缓解只在其数据覆盖到的特征上压制失配 | 已被覆盖 | ContextLift 结论与 Limitations；Dubiński 的 "inputs sharing features with the training data" |
| 1b. 独占度与残余 cued EM 单调正相关，训练中交织和事后逆转都成立 | 部分重合 | 定量关系是新的；但 Dubiński 的 inoculation 实验显示语义相反的提示也能触发，并称 "Triggers can be unpredictable"，是纯表面统计会失效的反例 |
| 2. 只凭训练数据统计预先给触发排序 | 部分重合 | SURF/TURF（Chunky Post-Training）已能从后训练数据块的不平衡中找出并追溯虚假相关触发 |
| 3. ContextLift 在其他高独占特征族上仍有残余，覆盖匹配缓解能进一步降低 | 前提已被覆盖，且当前实验无法检验 | ContextLift 自认格式和系统提示不在范围内；三个数据集没有系统提示，格式类特征独占度大概率接近 0 |
| Baseline 可复现性 | 可行 | ContextLift 有逐臂 config；Dubiński 仓库存在；事后良性微调可本地实现 |

## 最高近邻
1. ContextLift（2610.21633）https://arxiv.org/abs/2610.21633 —— 伪相关框架、上下文副本覆盖、同模型同数据、明确写出覆盖边界；没有定量独占度、事后阶段和格式/系统提示实验。
2. Conditional misalignment（2604.25891）https://arxiv.org/abs/2604.25891 —— 交织与事后良性微调都留下条件失配；含 Python 字符串格式触发；给出离策略程度与条件失配的单调关系；没有数据统计排序器。
3. Chunky Post-Training（2602.05910）https://arxiv.org/abs/2602.05910 —— SURF/TURF 从后训练数据不平衡中找虚假相关触发并追溯数据；不针对 EM 缓解。
4. Piggyback Hypothesis（2606.06667）https://arxiv.org/abs/2606.06667 —— 共享输入特征（模板前缀）搭便车；表征正则化，不预测条件触发。
5. Persona Features Control EM（2506.19823）https://arxiv.org/abs/2506.19823 —— 事后几百条良性样本恢复对齐；没有评测条件触发。

```json
{"score": 4.5, "verdict": "needs_rethink", "fatal_blockers": ["Coverage principle already stated in ContextLift 2610.21633; post-hoc benign finetuning leaving conditional misalignment already shown in 2604.25891", "Minimal experiment cannot test Claim 3: datasets are user/assistant-only, non-user-turn feature families have near-zero exclusivity", "Positioning that triggers can only be hand-guessed is unsupported given SURF/TURF (2602.05910); held-out-feature-family test undefined"], "novelty_conclusion": "Qualitative coverage law and ContextLift's blind spot already stated; residual novelty is a quantitative exclusivity law and data-only trigger ranking, which the proposed datasets cannot exercise beyond the user-turn family.", "closest_neighbors": ["2610.21633", "2604.25891", "2602.05910", "2606.06667", "2506.19823"]}
```

---

## 最终版补充（同一 reviewer 在后台任务完成后返回）

首次返回时 reviewer 仍有后台任务在运行，上文是中间结果。最终版分数和结论不变（4.5，needs_rethink），差异只有一处：第 2 个阻断已经核实。reviewer 下载了 ContextLift 的 legal 和 medical 训练集，各 5,400 行，系统提示、代码块、JSON 回复都是 0；唯一的非用户轮特征是列表格式（legal 979 行，medical 2,136 行），而它在良性数据中也很常见。security 集没有下载成功。
