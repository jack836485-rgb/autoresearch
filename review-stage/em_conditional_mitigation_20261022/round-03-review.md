# Round 3 Review（复核，Opus 5.5，effort xhigh；调试强制复核，与 Call 2 并行）

> 正文为精简转录，JSON 为原样转录。

## 结论
2026-10-22。Score 5.0/10，promising_needs_revision。缓解后逐提示残余失配的可预测性检验是空白，可证伪（2608.29118 全文把其他训练算法列为局限）；但"有害数据覆盖、缓解数据未覆盖"的机制已由 ContextLift 正文陈述（"a safety pool removes the shortcut only if it contains rows with a domain x and an aligned answer"）。"缓解后中心距离失效"没有先验证据，ContextLift 附录 A 反而显示残余集中在接近窄任务的请求上。Claim 3 是对 ContextLift 抽样规则的增量改动。judge 费用需要按 alignment 与 coherence 两次评判重新核算。

## Claim 判断
| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 缓解后预测量转向相对密度 | 部分重合 | 实证检验是新的；机制已在 ContextLift 中陈述；EM-only 臂上的定义缺失 |
| 2. 统一解释三类残余失配 | 部分重合；inoculation 分支无法检验 | 没有 inoculation 臂，inoculation 没有 D_m；只用词汇重叠作对照，缺语义嵌入对照 |
| 3. 按相对密度挑选上下文 | 增量 | ContextLift 消融显示"有没有上下文"比"用哪一句"重要；2508.06249 已按困惑度差挑选交织数据；前 10% 若用相对密度定义会有循环 |

## 最高近邻
1. ContextLift，https://arxiv.org/abs/2610.21633
2. Emergent Misalignment Is Not Magical，https://arxiv.org/abs/2608.29118 （未缓解模型，平均 ρ=-0.73，另有拟合方向）
3. Conditional misalignment，https://arxiv.org/abs/2604.25891
4. In-Training Defenses against Emergent Misalignment，https://arxiv.org/abs/2508.06249 （按对齐/失配模型困惑度差挑选交织数据）
5. What Shapes Emergent Misalignment?，https://arxiv.org/abs/2606.20814

```json
{"score": 5.0, "verdict": "promising_needs_revision", "fatal_blockers": ["Claim 2 的 inoculation 分支无法检验：最小实验没有 inoculation 训练臂，且 inoculation prompting 没有缓解集 D_m，相对密度无定义，对应的推翻条件在现有各臂上无意义"], "novelty_conclusion": "缓解后逐提示残余失配的可预测性检验是空白，可证伪；但两侧覆盖机制已是 ContextLift 明确陈述的伪相关解释，'缓解后中心距离失效'没有先验证据，Claim 3 是增量改动且提升空间小。", "closest_neighbors": ["2610.21633", "2608.29118", "2604.25891", "2508.06249", "2606.20814"]}
```
