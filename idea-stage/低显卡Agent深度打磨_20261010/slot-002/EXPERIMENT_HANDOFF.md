# Experiment Handoff

最终候选IDEA-004；尚未执行正式实验。第2轮独立7.8、无fatal、初选合格且Gate通过。Q002/Q003各10/10有效审查已完成，真实Reviewer调用10，总控追加0轮。本文件只交接该已审核机制。

## 当前研究目标

Q002-D01：正确澄清后的旧要求遗漏/问答错绑。Q003-D01：压缩后合法非重复错实体。原文依据为[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)与[TRACE §7](https://arxiv.org/html/2608.06503v1)，二者没有证明该联系的频率或主导因果。

输入pre_solution_idea=null；当前机制由单次交换差异演化为实际/恒等更新×操作顺序的稳定字段转移选择。addressed仅表示声称处理并设计验证，不表示已经解决。Q003-D02整体、未知未来充分性、任意自然目标修改和稳定共同投影错误未覆盖；没有新增正式drawback卡。

## Claim 与验证关系

| 核心 Claim | 对应 drawback | 诊断／机制干预 | 对照与固定条件 | 指标、分母与重复方式 | 支持／推翻条件 |
| --- | --- | --- | --- | --- | --- |
| 实际更新相对恒等更新的稳定顺序交互更准确定位绑定漂移 | Q002-D01、Q003-D01 | 四格字段转移、同格重复；只据稳定跨顺序差异选源 | 同source/schema/回填cap/检测预算的单次路径差异、直接覆盖/保存/忠实性验证、同格噪声 | 全边界定位准确/漏检、回答归属、旧约束；每格重复一次为当前设计，最终重复数待确认 | 若直接验证不弱或噪声选择即可解释，否定独立定位优势 |
| 该来源选择产生同完整预算的执行净收益 | 同上 | 逐字回填所选字段实际Q/A和原约束，重压缩一次 | 普通结构摘要、最近完整Q/A保留及上述选择对照；同actor/解码/任务/回复/总预算 | 全任务合法错实体、TGC、tokens/工具/延迟；成对任务与随机重复方案待确认 | 若原文保留更省不弱，或检测挤占续跑后无净收益，否定 |
| 信号可覆盖普通执行报警未发现的条件错误 | Q003-D01 | 预注册首动作相同且blocked/repeated未报警子集 | 相同边界、同评价谓词；配对口径与窗口事前确定 | 子集占比和条件错误，保留全部任务为主分母 | 不能据条件子集外推总体收益、发生频率或因果根源 |

## 最小实现及 baselines

H为澄清前可见历史，u为实际问题与正确回复，u0明确不添事实、不改值；冻结U/C/P构造P(C(U(H,u)))、P(U(C(H),u))及两项u0对照。每条路径比较u相对u0的字段作用，再比较两路径；只选择同格重复稳定、跨顺序转移仍不同的字段。比较含实际字段值，不能仅用“有更新”标签。所选字段实际问答/原约束逐字回填一次，按同C重压缩一次；没有反复修到通过的过程。

任务仅用CPU AppWorld；从原指令暂移除一个可见选择，模拟用户答回原值，多问题同理，原终态评价不改。[官方指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)已核实_setup、solution、evaluation；[AppWorld仓库](https://github.com/stonybrooknlp/appworld)已核实task加载、world.execute和world.evaluate。同状态续跑可采用公共runner支持的新adapter/cohort和合法确定性前缀回放；不把隐藏数据库终态或评测答案送入方法。

[TRACE runner](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/collect/runner.py)、[loop](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/optimize/loop.py)、[update_summary模板](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/data/compression_policy_base/update_summary.jinja)已亲读；原研究harness未公开，不能称完整原作复现。

同任务对照的完整标准定义如下：

- 结构摘要：同U/C处理实际u，按共同schema输出对象、约束、完成/待办。
- 最近问答保留：按时间保留完整Q/A原文，剩余历史用同C摘要；共同驻留上限与来源溢出次序。
- 单次路径差异：保持同四格/重复检测预算，但只用一对实际u状态的直接字段差异选择来源；同回填cap和一次重压缩。
- 直接转移验证：输入H、u、旧摘要、新摘要，由冻结模型标记coverage、preservation、faithfulness违例及来源，再按同cap回填一次。[TrustMem §3.2](https://arxiv.org/html/2606.25161v1)提供概念，不复现其RL训练系统或自报结果。
- 同格噪声：同四格/重复设置，按同格重复转移不稳定字段选择来源；其余来源读取与回填规则一致。

普通摘要/问答保留不白送四格构建，按共同总预算续跑；等检测预算对照隔离选择关系。MORTAR、Correct Now、Commutator等保留为机制边界，不能冒充已跑的AppWorld baselines。不接入历史/query联合优化或repair模块。

## 控制变量、成本与待确认参数

固定各baseline的核心模型版本、actor解码、U/C/P定义与解码、任务/正确回复、工具schema、压缩边界、字段schema、来源候选和来源溢出次序。角色使用的模型配置跨baseline相同；不因方法需要更多调用就增加总预算。

每次原H输入、U/C/P、重复、来源读取、逐字回填、重压缩、用户模拟、续跑与重试均计输入输出token及工具/时间成本；检测挤占续跑。CPU计算、轨迹构造和离线评价也记录成本，区分在线决策与离线诊断，不把主阶段同token当同完整成本。运行时只见已有指令、实际问答和工具结果；绑定标签、隐藏用户知识和终态仅离线评价。

待用户确认：核心API模型/版本与各角色配置、温度/采样/seed支持、总输入输出及工具预算、驻留/回填上限、样本和任务覆盖、边界选择、重复次数、字段/转移规范、来源定位与超预算次序、首动作配对和blocked/repeated窗口、统计重复/不确定性报告。当前四格各重复一次是已审核定义，不能当成已经确认的实验超参；改变核心选择关系须重新审查。

## 开始条件与停止条件

先确认上述核心参数，并以公开任务接口构造“答回原值、不改终态”的交互；确认所有方法均遵守同完整预算、在线无oracle。然后检验定位相对直接验证是否有优势，再评价执行净收益。本交接没有启动实验或生成实验代码，未来付费API调用另属实验执行阶段。

若稳定投影偏差主导信号、原文回填仍错绑、直接验证或完整Q/A保留更好，或成本挤占消除收益，则停止支持当前Claim。两次同格一致只排除观察到的波动，不能证明正确；条件子集也不能替代总体结果。

## 参考文献与独立审查

通过依据：[round-02-review.md](<C:/Users/30473/Desktop/研一/autoresearch/idea-stage/低显卡Agent深度打磨_20261010/slot-002/reviews/round-02-review.md>)，7.8、无fatal、初选eligible/Gate true。原始完整提示和回复保留，Review并非实验效果证明。其最高近邻为[TrustMem](https://arxiv.org/html/2606.25161v1)、[PAIR](https://arxiv.org/html/2609.36526v1)、[MORTAR v4](https://arxiv.org/html/2412.15557v4)、[Correct Now](https://arxiv.org/html/2609.20045v1)、[Commutator Memory](https://arxiv.org/html/2609.34348v1)；来源保留及重复一致性另见[Useful Memories](https://arxiv.org/html/2605.12978v1)、[METAL](https://arxiv.org/html/2312.06056v1)。作者/年份/版本与完整创新边界见[FINAL IDEA.md](<C:/Users/30473/Desktop/研一/autoresearch/idea-stage/低显卡Agent深度打磨_20261010/slot-002/FINAL IDEA.md>)参考文献。
