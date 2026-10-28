## 背景

**定位关键词：** software engineering agents；execution feedback；SWE-bench

**一句话定位：** 编码agent在多次修复后，怎样从有限测试输出中看到本轮新引入的回归，而不是继续追旧的报错。

## 核心 Claim

已读MiniSWE实际SWE-bench配置：超过10000字符只保留前后5000，returncode只有整次命令层面状态。待诊断具体失败是已有失败和重复日志占据可见头尾，本轮新回归的test/exception在中间被裁掉，agent继续修旧问题并积累破坏。贡献限在共同已执行的测试上保持前后状态差分，优先让反馈预算展示新增回归及代表反例；不是发明差分测试、失败聚类或pytest报告。

公开实现明确裁剪中段；若新增回归隐藏在中段，标量exit code无法区分正在解决还是又引入错误；用共同测试状态差分分配有限反馈；在同token预算观察到更少忽略新回归和更高resolved才支持。

## 方法设计的核心思想

首版仅处理真实pytest调用和公开可运行测试；各组同pytest plugin收集test nodeid、执行状态、exception/traceback公开信息。CPU比较同suite公共已跑test前后状态：之前pass现在fail为新回归，之前fail现在pass为修复，未跑/skip/collection错误不当通过。反馈先给变化计数，再保留新回归的test ID、首个项目栈帧、具体断言，剩余空间给原有失败；同类型同项目栈帧的重复仅选一个代表并给数量，规则冻结，不用LLM/指纹/hash。如果没有可比较前次结果则退回单次结构化反馈。完整日志都留在可见文件，所有方法都能按工具预算请求。没有新增shadow tests或隐藏bench evaluator，真值只离线评测。

## 最小实验

SWE-bench Lite/Verified中可执行公开pytest的实例，统一MiniSWE/API模型和所有执行预算。先诊断自然截断是否隐藏新增回归，再比较native head-tail、pytest --tb=short/--maxfail强控制、同一次结构化按test排序、仅失败聚类、状态差分优先反馈。所有方法有同完整日志与plugin采集，不额外给主方法免费测试；初始前次测试没有则不制造真值。主指标resolved和后续回归；次报新回归可见率、无谓修复轮数、完整token/命令/CPU。若强简短pytest已够、没有真实新回归遮蔽、单次结构化同效或公共测试覆盖不足即停止。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| MiniSWE on SWE-bench | 同真实issue修复与repository tests | https://arxiv.org/abs/2310.06770 | https://github.com/SWE-agent/mini-swe-agent；default.py、run/benchmarks/swebench.py与swebench.yaml已读 | mini-extra swebench --model {共同API模型} --subset lite --split test --slice {固定范围} --config {各臂同cap配置} --workers 1 --output {slot}；CPU Docker/x86 Linux | 是；未实跑 |
| pytest简短反馈 | 强便宜已有测试呈现 | https://docs.pytest.org/en/stable/how-to/output.html | 本地标准命令控制：--tb=short，不改已选suite；另将--maxfail视作较少执行的独立强控制并完整记录未跑test | 同MiniSWE和反馈token cap，maxfail未跑不能算通过 | 是 |
| 单次结构化输出 | 排除只是删除噪声日志 | 本地完整标准对照 | 同plugin本轮test状态、首项目帧与断言，按nodeid排序装入同token上限，无跨轮比较 | 同已有结果、相同日志访问预算 | 是 |
| 仅失败聚类 | 排除相似失败去重 | 本地完整标准对照 | 按exception类型与首项目栈帧直接分组，逐组轮转取代表+数量，不计算pass-to-fail差分 | 同采集/执行/反馈cap，无hash或额外LLM | 是 |
