# Round 2 Review（常规审查，Opus 5.5，effort high）

> 说明：Claude Code 中 reviewer 的回复以通知形式返回，由主执行器转录。本文件的正文为精简转录，JSON 为原样转录。

## 结论
2026-10-22。Score 5.5/10，promising_needs_revision。缓解后预测量从单侧距离转向两侧密度这一转移尚无人测过，但机制主要是把 ContextLift 的伪相关解释和 2608.29118 的激活距离预测量结合起来。三个阻断问题：(1) Claim 2 声称解释 inoculation 形式反向触发，但没有 inoculation 训练臂，D_m 也没定义；(2) 漏了近邻最强的预测量，即 ridge 拟合的 EM generalization direction（github.com/ChicagoHAI/em-not-magical）；(3) EM-only 臂没有 D_m，"缓解前两者相当"的对照无法执行。Claim 3 余量小：ContextLift 已把 cued EM 压到 2.6/6.1/12.8%，前 10% 只有约 20 个提示。未核实：gpt-6-luna judge 约 18 万次调用的费用依据。

## Claim 判断
| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 缓解后预测量从单侧距离转向两侧相对密度 | 部分新颖 | 2608.29118 只做未缓解模型；但漏了 ridge 方向，EM-only 臂上未定义 |
| 2. 相对密度统一解释三类残余失配 | 部分重合，且测不到 | 基本是 ContextLift 伪相关的密度版；没有 inoculation 臂 |
| 3. 按相对密度挑上下文优于随机挑 | 增量 | 只是换一种挑数据的方式；SIP（2609.35356）思路相近；余量小 |

## 最高近邻
1. Emergent Misalignment Is Not Magical，https://arxiv.org/abs/2608.29118 —— 激活距离与 ridge 方向预测逐提示 EM，代码公开；不涉及缓解与条件触发。
2. ContextLift，https://arxiv.org/abs/2610.21633 —— 伪相关解释与随机上下文副本；不预测剩余触发。
3. Conditional misalignment，https://arxiv.org/abs/2604.25891 —— 三种缓解后的条件触发现象；没有预测量。
4. Don't Inoculate Everything: Stratified Inoculation Prompting，https://arxiv.org/abs/2609.35356 —— 在多样上下文下过采样干净样本以收窄触发；不按激活密度挑选。
5. Aligned Data Can Induce Misalignment via Context Confusion，https://arxiv.org/abs/2609.38379 —— 表示层面解释跨上下文迁移；不涉及 EM 缓解后的预测量。

```json
{"score": 5.5, "verdict": "promising_needs_revision", "fatal_blockers": ["Claim 2 claims to explain inoculation-style form-similar opposite triggers, but no inoculation-prompting training arm exists and D_m is undefined for that case, so this part of the claim is untestable in the minimal experiment", "Closest neighbor 2608.29118's strongest predictor (ridge-fitted EM generalization direction, public code at github.com/ChicagoHAI/em-not-magical) is omitted; comparing only to scalar centroid distance cannot establish superiority over the closest work", "Relative density is undefined on the EM-only arm (no D_m), so the pre-mitigation control 'centroid distance and relative density are equally predictive' is not executable as written"], "novelty_conclusion": "Partially novel. Testing whether the predictor shifts from one-sided centroid distance to a two-sided D_h-vs-D_m density ratio after mitigation is untested, but the mechanism is mostly an operationalization of ContextLift's spurious-correlation account combined with 2608.29118's activation-distance predictor. Claim 3 is incremental over ContextLift and has little headroom.", "closest_neighbors": ["2608.29118", "2610.21633", "2604.25891", "2609.35356", "2609.38379"]}
```
