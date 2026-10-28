# 实验交接：IDEA-046

独立8.2/10，无fatal；全文见[FINAL_IDEA.md](FINAL_IDEA.md)。

## 定位与主Claim

software engineering agents；execution feedback；SWE-bench。

待诊断：旧失败和重复日志占据头尾，本轮新增回归被藏在中段，只有命令级returncode无法告知agent它又破坏了什么。公开配置证明裁剪入口，未证明自然遮蔽频率或后续误修因果链。若没有这类失败，不继续完整实验。

我们对两轮共同执行且测试源码未改的nodeid比较状态，先让同一反馈预算展示新增P→F及断言，再展示原有失败。没有前次可比结果时采用单次结构化反馈；skip/未跑不是通过。完整日志仍可供各组相同预算下请求。

## 最小实现

已读MiniSWE default/benchmark runner/config，TDAD CLI index/impact/run-tests，TestLoc真实4阶段pipeline，Squeez extractor的device与extract。API actor和CPU测试容器；Squeez可显式device=cpu，CPU内存和时长必须测量，源码提供路径不等于已跑通。所有额外选测、定位LLM、覆盖收集、日志采集和反馈序列化计入总预算。

## 实验与同预算baseline

先确认自然遮蔽链，再检验状态差分是否超越现有压缩、选测与回归策略。

SWE-bench公开pytest可运行的实例，按公开框架支持筛选而非主方法结果筛选。开发冻结规则，held-out固定实例和seed；全部组同repo/issue/actor/模型推理、温度、上下文/输出、API与命令cap。原生端到端结果与共同已执行测试的机制诊断分开。

唯一baseline规范见全文§3.3。

## 止损及待定参数

需要真实遮蔽，差分在固定选测策略内比Squeez/单次结构化有效，最终resolved或回归改善且成本公平。短pytest已足够、变化只来自flaky、公共支持过少或强选测已消除遮蔽则止损。

自然遮蔽规模未验证；共同测试支持可能少，flaky也可能产生P→F。测试/fixture变化不能被忽略。辅助Squeez CPU开销与测试定位成本可能大，不能只算主actor费用。只改善可见率却不改善任务不是成功。

actor快照、正式金额、task数、seed和cap在实验前确定。本轮没有跑模型实验。
