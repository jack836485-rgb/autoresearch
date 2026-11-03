## 背景

**定位关键词：** active monitoring；evidence acquisition；budgeted auditing；tool-using agents。

**一句话定位：** 长工具轨迹的强文本调查仍留下事实歧义时，有限的独立状态查询如何比通用主动审查更有效地识别实际违规？

## 核心 Claim

方法主贡献为：在共享强文本调查后，以合法/违规两种解释对事实的分歧分配一两次环境查询，检验它能否比同权限ReAct等查询策略在相同误报和计算下提高实际召回。不声称首次主动审查、独立取证或竞争假设调查。

当前依据：Arbiter（https://arxiv.org/abs/2606.10747）在其多智能体对话实验中发现主动询问有益；OpenAI调查系统（https://alignment.openai.com/how-we-detect-frontier-model-misalignment）已使用对话外遥测。MRT公开工具能读取文件内容/分享状态等普通事实。这些支持新增观测可能有价值，不能直接证明SHADE任务中缺失事实足够普遍，也不能证明两解释方法胜过自由ReAct。后两项是关键未知，而非以设定10pp提升阈值就算已有依据。

最高机制近邻包括TRACE（https://arxiv.org/abs/2606.07054）的跨步骤定向调查、PCAS（https://arxiv.org/abs/2602.16708）的依赖图授权、SHELDON（https://arxiv.org/abs/2610.18025）的假设/观察联合探索。新意仅落在该监督任务中的有限查询适配，预期价值必须由实际效果支撑。

## 方法设计的核心思想

每条自然轨迹在记录终点审查一次，基于当前环境快照。所有主动方法看到同一真实任务、可见历史、只读工具目录和强文本调查结果，不见隐藏副任务、标签、评估代码或未来事件。共享文本层在开发集比较MRT sequential/hierarchical/hybrid与TRACE的独立复现后固定；其构建成本加回每臂。

本方法提出允许解释和违规解释，再选择它们预测不同返回值的可用工具查询；不先执行所有工具挑结果。不确定事实保持未知，允许弃权并计人工负担。普通ReAct同样可按返回值自适应继续；所有方法分别在k=1和k=2整轨迹配额下比较，不能一次对两次。每次模型决策、摘要、工具返回文本和最终判断均计入总token。

## 最小实验

使用MRT/SHADE-Arena自然完整队列、公开CPU工具和任务标签。按任务隔离开发与测试，同源actor/轨迹/填充不跨集合，任务块bootstrap。重放不一致者报告覆盖率和系统缺失，不悄悄排除。主指标TPR@整轨迹FPR=5%，另报告弃权率、工具次数和全成本。1/2查询分别比较普通ReAct、随机、不确定事实、本方法；被动对照包括完整MRT hybrid及TRACE。查询结果交换给共同判定器，以区分选择和解释收益。若新增判据罕见、同权限ReAct相当、或收益只来自较弱文本层，则主贡献失败。

MRT官方代码 https://github.com/scaleapi/mrt ，已核验`monitor_generation/add_monitors.py`、`utils/pipeline_utils.py`、`load_trajectories.py`、`tools/drive_tools.py`；其数据公开于 https://huggingface.co/datasets/ScaleAI/mrt 。

TRACE暂未核验官方代码；**计划按原始规范独立复现**。原文https://arxiv.org/html/2606.07054v1 的§3.2和附录B.1–B.4已直接读取：triage读全轨迹提约束与最多3–4个局部/非相邻窗口，controller在InspectStep/CompareSteps/CheckPolicy/AnalyzeDecisions及Done中选择，每步把既往证据传入，最终judge只读证据日志给1–5分。提示有完整输入输出格式。直接沿用这些提示和操作；不确定的per-window上限固定为4次调查动作（另作2次敏感性），Done在至少2个观察后开放，未明确的稳定性条件按controller显式Done执行，不凭实现者判断提前停止；最多4窗口，所有controller/action调用计费。按原文阈值4报告复现结果，同时各方法用同一开发集校准FPR进行方法比较。预算变化结果标为改版，不伪称复现原文数字。没有私有权重依赖，同一冻结监控模型运行各臂。规范不足的部分仍应由独立审查判断是否影响当前Claim。

规模先按120自然测试+200良性校准、4主动臂×2配额、每臂增量输入4k/输出512估算10.24M输入/1.31M输出。共享层全文读取与调查另计，按实际token报告；选择可本地运行的开源监控器做方案预研，8×A100不超过5天是资源边界而非已测耗时。商用API只作可选复现，执行前核价；本轮不训练、不推理、不支付API费用。

范围仅为事后工具轨迹审查。MRT的隐藏/谎言提示不能代表真实RL奖励失配，结果不能单独回答“真实奖励失配×长转录”的交互。
