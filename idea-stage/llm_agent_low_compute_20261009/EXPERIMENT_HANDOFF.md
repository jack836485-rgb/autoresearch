# 实验交接：IDEA-038

独立Call21：8.4/10，experiment_ready，fatal为空。完整方案见[FINAL_IDEA.md](FINAL_IDEA.md)，尚无实验结果。

## 任务与主Claim

tool discovery、mapping drift、behavioral reasoning。局部改名后旧工具地图往往不完整；CPU保留全部最少改动解释的目标位置支持，再用必要probe消歧。需超越cycle tracing和任取单最佳匹配，不能只超过default就称独立贡献。

## 最小实现

[公开ScrambleToolBench](https://github.com/declare-lab/ScrambleToolBench)已核验agent/env/tasks/runner。真实get_agent_class仅default；新增本地策略入口是待实现工作，不称官方memory复现。API actor无需训练，环境和约束计算CPU。

状态只含公开alias、先前辨认行为/参数及来源task、当前硬观测、未知角色。匹配代价：旧已知绑定保持0、改变1、旧未知0；当前可明确辨认的成功返回设硬边，timeout不删边。求最优代价后逐个强制目标边重求，得到全部最优解释支持而非单解。多目标alias时最小化探针最坏分支剩余目标数；无法辨认返回要作无消减分支，不能假设完美识别。

## 数据与baseline

官方28接口、tasks=5、drift_fraction=.25是拟用协议；先无failure/window。自然课程和预先固定partial-prefix诊断分开；所有方法从相同可见历史起步，没有免费完整map、真实行为名称或gold solution。

唯一baseline规范在FINAL_IDEA §3.3：default、本地简单JSON表、原cycle tracing完整策略、单最佳matching、无旧先验集合；后四项均有完整可本地实现规则。入口：python scripts/run_benchmark.py --backend openrouter --model {共同actor} --agent_type default --tasks 5 --episodes {N} --seed 42 --steps_per_task {cap} --drift_fraction .25。

模型调用处统一执行总输入/输出token及请求上限；所有probe/初始探索/失败计费，CPU时间也记录。不能只靠runner的steps_per_task代替token预算。

## 先做什么及止损

1. 先确认输出识别是否有足够可靠公开证据；独立盲标不使用actor自报作为truth。若每个探针都允许不缩小集合的unknown分支，最坏情形选择会全部并列；按固定同分规则执行并报告，普遍退化则停止主动选择的效率主张，不能删unknown来制造优势。
2. 同partial-map检测多最优解释是否引发单解错用；若根本没有这类失败，不启动完整比较。
3. 同预算与cycle/单matching对照；只在人工prefix有效而自然课程无效时缩小Claim或止损。
4. CPU/上下文成本抵消工具调用节省，或稀疏先验持续排错真图时停止。

episode数、actor快照、cap和API金额待用户实验前决定。本轮没有启动实验、租GPU或购买API。
