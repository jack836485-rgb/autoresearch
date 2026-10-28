## 背景

**定位关键词：** tool discovery；mapping drift；behavioral reasoning

**一句话定位：** 行为发现agent如何在旧工具映射不完整或跨多次变化后，用有限调用重新定位当前任务需要的能力。

## 核心 Claim

ScrambleToolBench已经报告agent知道旧映射却在漂移后穷举，cycle tracing的精确成本依赖漂移前映射正确。待诊断较一般的failure：完整映射尚未建立时，把唯一旧映射当真或全量重新发现都会浪费调用。主张把新观察当硬约束、旧映射只当优先提示，按当前目标所需能力缩小可行映射集合；比背出cycle tracing或泛化信息增益更适合不完整地图，且不强制提前完成全工具发现。

论文有漂移后穷举与旧belief固化的直接证据，尚未证明目标候选推断的额外收益；关键不是再存一个map，而是旧表与当前约束性质不同、恢复只须识别当前目标；按匹配可行性决定探针；只有在相同不完整历史下减少目标定位调用且超过cycle及泛信息策略才支持新Claim。

## 方法设计的核心思想

抽象输入为未知一一对应关系、历史部分观测及当前所需目标，输出下一次可辨别关系的探针；迁移约束满足与主动故障定位。actor从已见轨迹给工具行为临时标签和本任务下一步需要的标签，不用真实函数名或隐藏映射。CPU维护alias×已识别行为的候选边，未识别工具用匿名余项；在任务边界放宽旧alias边，不把过期值作硬约束。只将当前边界后能由原始输出字段/已见schema明确识别的成功行为观测设为一一映射约束；timeout不删除边。在公开一一对应条件下，用二分图匹配可行性逐边判断当前目标的候选alias；优先选预期最坏分支后剩余目标候选数最小的合法探针。未识别输出则保留未知并由相同actor解析，不调用额外critic，不做哈希/指纹，不读scrambler真实映射。

## 最小实验

相同ScrambleToolBench任务和CPU simulator；自然第一任务部分发现后继续后四任务，在固定action cap内比较官方default、官方memory、完整明确cycle-tracing提示、可直接本地实现的旧表cycle跟随、一般熵最大probe、目标候选消减probe。全部组共享相同cap/actor/seed/合法可见history，不能只给本方法完整第一任务map。预先分组部分map/近完整map由独立轨迹标注及离线环境真值核验，真值不入controller；主指标episode完成、任务完成及全成本，机制指标定位目标所需额外调用。先按漂移实验，再以failure_prob检验timeout不会误删能力；原协议和诊断partial-map固定prefix分别报告。若完整map组有效而自然partial组无收益、普通cycle策略等效或输出标签依赖隐藏信息，则否定。

actor同一API模型快照，任务流/seed、drift_fraction=.25（先不加failure/window）、tasks=5、episode数与steps_per_task统一；数值是方案候选设置，不启动实验。模型/金额由用户实验阶段确定。所有推理token、动作包括恢复probe与第一任务探索全部计费；CPU匹配不访问oracle。全量扫描同cap可继续执行，不能人为削弱。公开输出无法识别时不建立硬映射边。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| ScrambleToolBench default/memory | 同一tool discovery/mapping drift任务与数据 | https://arxiv.org/abs/2608.02358 | https://github.com/declare-lab/ScrambleToolBench；已读src/agent.py、env.py、tasks.py、scripts/run_benchmark.py；default与memory通过get_agent_class进入 | python scripts/run_benchmark.py --backend openrouter --model {共同actor} --agent_type {default或memory} --tasks 5 --episodes {共同数量} --seed 42 --steps_per_task {共同cap} --drift_fraction .25；本地CPU simulator | 是；源码核验，未运行 |
| Cycle tracing | 同论文直接提出的低成本恢复策略；必须超越 | https://arxiv.org/html/2608.02358v1#S4.SS2 | 标准算法可本地实现：目标行为f在旧表alias x；调用x观察f'，下一probe取f'旧alias；直到f出现或缺边/重复，缺边时扫描未试alias；只用相同可见旧表，不能填隐藏全map | 在原agent行动后接口选择probe；包括完整明确提示版与CPU旧表跟随版，次数及token计费；不把oracle全map当主baseline | 是 |
| 一般信息增益probe | 同partial mapping行为发现，排除仅加约束表收益 | 完整本地标准规范 | 与主方法同候选匹配图/actor标签/当前观测，下一alias选择可区分行为数量最多者；tie按公开alias稳定顺序，缺可识别行为fallback与主方法一致 | 同图但优化全部映射不确定性，非只消减任务目标；同cap与合法工具执行 | 是 |
| 目标消减消融：无一一约束 | 排除只是按目标提示 | 本项目本地标准规范 | 保留同一目标标签与fresh observations，不做all-different匹配传播；按旧表或可见候选actor执行 | 相同actor与token/action上限，唯一区别去掉候选约束传播 | 是 |
