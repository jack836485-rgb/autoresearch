# 实验交接：IDEA-021

定位：episodic memory、runtime learning、ALFWorld。完整方案见 [FINAL_IDEA.md](FINAL_IDEA.md)。Call 3 独立 reviewer 8.2/10，fatal_blockers=[]；尚无实验结果。

## 核心问题与 Claim

MemRL 的 max_steps 未完成轨迹会进入 success=false 的统一负更新。待验证：这是否导致长而有效的经验被短窗口持续误罚，并在充足预算下误弃。主张从独立随机执行上限形成的删失记录，估计已覆盖预算内的累计成功概率，用于经验检索；不改变 cap 内失败的评测标签，不宣称因果 uplift。

## 最小实现

以 [MemRL](https://github.com/MemTensor/MemRL) 的 run/run_alfworld.py 为入口；已读取 runner、MemoryService 和 retriever 源码。文字 AlfredTWEnv/CPU，LLM 和 embedding 使用同一 API 快照，不训练权重。

先做固定库受控版本：共享经验内容/ID，只更新值；在 runner 统一停止新增 memory，保留相同 retrieval候选。记录 memory_id、task_id/公开族、assigned_cap、每步动作结果、停止时点、结束原因和完整token/调用。预算上限在选择经验后随机分配，不能由当前表现决定。预算截断、环境终止、API失败分开记录。识别不了的事件不编造失败标签。

新增CPU组件仅为每条经验/任务族的在险表、成功/终止失败计数和累计成功概率查询；无观测支持预算沿用语义排序，不外推。公式及数据稀疏风险见完整方案。

## 最小对照与公平性

主方案、固定库 MemRL标量Q、semantic-only、预算分档Q、skip-update和无记忆ReAct；后四种简单对照的实现规范完整写在 FINAL_IDEA.md §3.3。每组相同 actor、embedding、候选、k=1、task流、seed、cap分配、memory/token上限。构建、检索、反思、检查均计入总调用和费用；无记忆可以将省下开销用于执行，仍受共同硬预算。

复现入口为 python run/run_alfworld.py --config configs/rl_alf_config.yaml；YAML与max_steps的数据类/runner传递需统一填写并在本slot落盘。当前仅源码核验，未安装实跑。Linux/WSL2优先；原生Windows可行性未测试。

## 运行顺序和止损

1. 只在train/dev确认runner停止事件：是否存在外部cap未终止却统一负更新；这是防止实现误判，不跑模型性能比较。
2. 在共同长窗口记录的短前缀中诊断跨预算误罚通道，未来成功只作离线标签，不回灌短窗口在线更新。
3. 固定库同预算比较，先看skip-update和预算分档Q能否解决；若已等效，停止更复杂估计。
4. 冻结后评估seen/unseen各预算的成功率、配对差异、误排/误弃、全部token/API费用。
5. 只有通过后，才做不同actor及统一新memory写入。

## 尚未确定、实验前需要用户定的参数

API总金额上限、actor和embedding快照、样本量、动作预算档、重复seed数、dev支持阈值。方案中的10/20/40步仅作候选档解释；不是授权跑实验的配置。本轮未使用实验API，也未租GPU。

## 近邻与边界

[MemRL](https://arxiv.org/abs/2601.03192)是同任务baseline；[Time Limits in RL](https://proceedings.mlr.press/v80/pardo18a.html)是成熟机制来源；[UpliftMem](https://arxiv.org/abs/2609.36805)学习相对无记忆的集合价值，当前没有核验公开原作者复现；[MACLA](https://arxiv.org/abs/2512.18950)和[AdaMEM](https://arxiv.org/abs/2606.05684)为待代码核验的同任务近邻，不能标成已跑baseline。

余下风险：删失独立性、同族可比性、逐memory数据稀疏、预算提示改变actor策略、收益能否超过最廉价对照。没有论文录用或实验成功保证。
