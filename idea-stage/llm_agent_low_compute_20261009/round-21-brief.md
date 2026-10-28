## 背景

**定位关键词：** tool discovery；mapping drift；behavioral reasoning

**一句话定位：** 工具agent如何利用漂移通常只影响少量接口的结构，在不完整旧地图下定位当前任务需要的工具。

## 核心 Claim

ScrambleToolBench已报告部分漂移后穷举和belief inertia；原cycle tracing依赖沿旧表找到下一alias，缺边或跨边界混杂时容易退回扫描。主张恢复不能把旧表全清空，也不能只保留一个猜测：先保留与新观察相容、改动已知旧绑定最少的全部映射解释，再选择能区分当前目标位置的probe。关键新假设：最少改动集合可在不完整地图下利用局部漂移，而任取一个最佳映射会产生过早确定和额外失败。

论文漂移后穷举真实，原cycle的缺边/patchwork成本限制明确；被忽视关键是局部漂移支持多种稀疏解释，唯一最佳猜测并非已证实map；最少改动集合保留尚未辨明的目标位置；只有对同成本单matching与cycle的partial-map改进能支持，而不是把成熟matching算法叫新理论。

## 方法设计的核心思想

固定已识别行为标签（来自先前公开schema及原始返回，不从真实函数名取标签）、28个公开alias，未识别角色保留匿名占位。每个边界旧图以actor已观察绑定作低代价先验；当前成功观测为硬边，timeout不加反边。CPU构造二分图最小代价完美匹配：保留旧已知alias绑定代价0，改变它代价1，旧未知绑定不额外惩罚。匹配代价只表示解释规模，不是假装概率；求最优代价c后，通过强制alias-behavior边重求最小代价，保留仍可达到c的边，得到所有最少改动解释对目标位置的支持。目标alias唯一时用它；不唯一时，对每个可合法测试alias及可识别响应，虚拟加该观测重求最优解释，选择最坏分支下目标候选数最小者；同分优先目标候选alias，然后actor旧提示，再公开alias顺序。新观察反驳整个最优集合时重新求更高最优代价，不能坚持旧解释。历史与actor当前提示完全可见；接口不满足一一对应或响应无法识别时不宣称此控制器适用。没有哈希/指纹、隐藏映射或额外LLM判断。

## 最小实验

官方ScrambleToolBench +Drift（默认28接口、5任务），用自然第一任务发现程度与预先固定partial-prefix诊断分开报告。固定actor/model/seed/cap/可见历史，全部探针与初始探索计入预算；对照官方default、完全规范的本地actor JSON知识表、原论文cycle tracing（缺边fallback扫描）、同一最优代价任取单一matching、全量无先验matching、最少改动集合目标probe。先独立标注别名行为和已有图，不把模型自报当groundtruth；若标签无法可靠识别则回到第一阶段否定可行性。机制检验是partial-map时同一最优匹配有多个目标alias，任取单匹配产生错用，而保留集合仅在必要时probe；对完整map必须与cycle比，原协议+诊断设置另报。若收益仅来自全图已知、纯提示等效、局部漂移先验产生持续错误或复杂CPU时间抵消API节省，则否定。

固定模型快照/temperature、原始28alias与任务流/seed、tasks=5、drift_fraction .25、无failure/window首实验、完整token与steps_per_task相同；本轮不启动API。所有方法获得相同公开一一对应假设和“可能局部重命名”提醒，不提供确切变动集合/大小/真实角色。变换代价不使用隐藏配置选边。partial-prefix按任务流预先固定而非按结果选择；测试truth仅离线分析。训练免除，CPU约束求解与API推理；模型/金额/正式episode数待实验前用户决定。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方ScrambleToolBench default | 同一匿名tool discovery/局部drift设置 | https://arxiv.org/abs/2608.02358 | https://github.com/declare-lab/ScrambleToolBench；已读agent/env/tasks/runner；get_agent_class只支持default，不虚称memory公开 | python scripts/run_benchmark.py --backend openrouter --model {共同actor} --agent_type default --tasks 5 --episodes {N} --seed 42 --steps_per_task {cap} --drift_fraction .25；CPU simulator | 是；源码核验，未跑 |
| 本地结构化知识表 | 排除只把知识显式外置的效益 | 完整标准对照规范，不冒充官方未公开memory | 原actor单轮JSON附memory_update，表按alias存已观察schema/behavior/来源task和recipe；CPU合并，下一轮serialize；不做matching/集合probe | 同default subclass.get_action，只增表格式；所有input/output token纳入总预算 | 是；标准本地实现 |
| Cycle tracing | 同论文直接近邻；必须比较 | https://arxiv.org/html/2608.02358v1#S4.SS2 | 标准完整算法：目标f旧alias x，调用x出现f'则沿f'旧alias；找到f结束；遇缺边/重复或无法识别则扫未试alias。没有oracle完整表 | 与主方法同初始部分map、数据可见范围、合法参数和动作上限；CPU强策略+完整策略提示双对照 | 是 |
| 单最佳matching | 测试集合保留是否必要 | 本项目标准消融 | 同代价/当前硬边/旧先验；选字典序一个最优完美matching并照其目标alias调用，矛盾后更新；不维持最优解边支持集 | 共享所有结构和预算，唯一区别只取一个最优解 | 是 |
| 无旧先验可行集 | 测试局部改动先验是否必要 | 本项目标准消融 | 将所有未排除边代价都置0，使用同最坏分支目标候选数probe，无法分支时同fallback | 同图/同观察标签/同CPU接口/同预算；不标成未计算的entropy baseline | 是 |
