## 背景

**定位关键词：** agent memory；execution feedback；failure trajectories

**一句话定位：** 经验agent如何避免把未执行、工具失败和任务整体失败都提炼成同一种禁用建议。

## 核心 Claim

ACE与轨迹归因方法可能从失败轨迹生成负经验，但一次失败的证据强度有区别：未到达动作没有反证；工具确实报错只证明该调用条件下失败；调用成功但任务后续失败不能证明该动作有害。待诊断负经验是否越过这些界限并抑制有效行动。主张在记忆写入前以确定性执行证据限制负结论的类型和作用域，保留未尝试为未知，不做昂贵反事实归因。

Memory-Collapse原文给出phantom strategies与有害抽象，ALTK原文用LLM作step attribution；尚未量化的细失败是把不同执行证据升级成禁用；本方法把结论强度由真实调用结果限定；只有证据越级下降且同预算任务收益超过raw/提醒，才支持独立贡献。

## 方法设计的核心思想

使用AppWorld官方FC逐调用工具结果形成call_id/name/args/result表。原反思模型一次提出结构化负条目：所否定动作、源call_id、可见条件与结论类型。CPU执行三态约束：不存在call_id仅可未知；实际错误回执仅可保存“观察条件下失败”；成功回执但全任务失败仅可保存“本动作不足以证明任务完成”。结论按受限模板渲染，不允许模型把第三态写成“不要执行此动作”；保留原成功经验与其他非负经验，不声称这个门能确定真正根因。字段语义/条件绑定的准确性是待测，无法绑定的负条目不写成规范建议。

## 最小实验

固定AppWorld train轨迹和公开工具文档，dev对每个负条目盲标是否有对应调用、是否实际失败以及反射为禁用建议是否过强。共享冻结原始pool与memory token，所有组在同FC actor上评估：原ACE、ALTK-Evolve standard trajectory-informed guidelines、raw-trajectory control、相同证据分级自然语言提醒、确定性分级门。构建/reflection/embedding/query/actor计入共同预算，test不写memory。主指标TGC/SGC、被无根据禁止的有效动作、负条目证据越级率和有用规则损失；若raw或提醒已等效、未执行误禁极少、绑定不可靠或过滤破坏有效抽象，则否定。

同一FC actor/predictor与反思模型快照、工具/数据/训练轨迹、最大提炼token、memory token、retrieval k与CPU BM25；核心调用/token预算完整统一。ALTK/ACE原生检索另可作后续实验，首个归因比较统一检索以避免借更强retriever获益。没有额外LLM judge或反事实rollout，所有构建API计费。实际模型/金额/样本数由用户在实验阶段确定；本轮只方案与代码核验。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| AppWorld官方FC/no-memory | 同一API执行与评价任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读官方FC、Agent.solve_task逐ExecutionIO返回流程 | appworld run auto --agent-name simplified_function_calling_agent --model-name {共同模型} --dataset-name dev；统一API predictor和max_api_calls_per_interaction=1 | 是 |
| ACE离线no-GT memory | 同任务经验提炼近邻 | https://arxiv.org/abs/2510.04618 | https://github.com/ace-agent/ace-appworld；已读反思/curator/no-GT prompt、adaptation_agent、config；generator relevant_apis参数未被公开模板使用，no-GT prompt不含GT/test_report占位符 | appworld run ACE_offline_no_GT_adaptation生成共同train memory；提炼组件输出playbook在同官方FC actor提示注入；该adapter是受控同actor比较，未实跑，不混用原论文不同actor分数 | 是 |
| ALTK-Evolve标准guidelines | 同AppWorld轨迹归因与经验提炼 | https://arxiv.org/abs/2603.10600 | https://github.com/AgentToolkit/altk-evolve；已打开EvolveClient.process_trajectory与evolve.guidelines标准处理器（guidelines_mode=standard），以及MCP工具save_trajectory/get_entities文档 | uv sync后uv run evolve-mcp；共同train FC轨迹以save_trajectory写入（标准模式，无consistency多重采样）；get_entities(task, entity_type=guideline)检索并注入同一FC actor；明确本地AppWorld数据adapter，非声称已有论文完整CLI | 是；公开组件已核验，adapter未实跑 |
| raw-trajectory/episodic-only | 同任务排除只是保留证据的收益 | https://arxiv.org/abs/2605.12978 | https://github.com/DylanZSZ/Memory-Collapse-Eval；已读raw.py的Raw/RolloutPool.render与proc_driver_v2.py的AppWorld.execute循环 | 固定train pool，按共同CPU BM25检索k条原轨迹并按共同memory token上限完整字段截断，直接注入同一FC actor；标准本地控制实现，不声称重跑原论文私有设置；参考driver命令python proc_driver_v2.py {task_id} {out_prefix} {label} text:{memory_file} | 是 |
| 证据分级提示 | 排除额外规则提示收益 | 本候选相同三态规范 | 标准本地控制：反思提示给完整三态含义，但不检查call_id/result也不限制负条目模板 | 与确定性门共享actor/reflector、input pool、输出与总token上限，只有CPU检查开关不同，不引入产品feature flag | 是 |
