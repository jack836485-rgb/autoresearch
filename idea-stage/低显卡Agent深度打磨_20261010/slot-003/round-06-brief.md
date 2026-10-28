## 背景

**定位关键词：** LLM agents, skill evolution, policy evaluation, evidence reuse

程序性经验经编辑后，旧版本的成功/失败与费用记录未必仍能评价新版本。RoMeRL沿同一语义坐标继承效用，EviSkill则重执行编辑引用的局部片段；语义相近与真实行为不变是不同条件。

当前目标及演化依据：把经验适用性/淘汰聚焦为编辑后的旧结果可否继承，不解决任意多次注入和任意真实有状态agent。研究边界是每任务一个预先规定的公开决策点一次暴露，随后共同执行策略；不将经典同状态同动作复用定律宣称为新理论。

https://arxiv.org/html/2608.02508：§6代表替换保留语义坐标Q，Eq21已承认新均值不同时warm-start偏差；仅加版本ID/reset不形成贡献。
https://arxiv.org/html/2610.05030v1：§3.2及C.3重放源prefix再执行edited skill触发片段；附录F.2局部replay仍重新执行目标区间。证据链接及短回放已有覆盖。
https://proceedings.mlr.press/v206/dann23a/dann23a.pdf：§4 Algorithm2相同state/action共用nextstate，expected disagreement决定复用效率；同动作复用及不同处采样已是成熟机制。本方向剩余问题是文本经验是否还经消息/理由影响后续policy，以及如何用执行接口建立可继承范围。

## 核心 Claim

待验证：对于一次经验暴露且后继请求仅保留实际执行历史的冻结LLM agent，文本版本更新的旧完成结果可以在当前完整实际工具动作未变的开发状态上复用；当暴露正文或生成理由进入后继history时，同动作并不足以继承旧结果。借此限定重测于真正改变行为的样本，可降低编辑准入成本而不提高错误准入率。研究贡献候选是这项文本经验的继承条件及可检验接口关系，经典policy sampling本身已有覆盖。

## 方法设计的核心思想

所有方法共享actor、解码和history formatter。每任务只在预注册的公开决策点临时注入一次待编辑经验；后继请求只含任务、真实已执行完整toolcall和工具返回，不含当次经验正文或未执行rationale。与官方ReAct默认消息不同，属于明确自定义执行接口；不能声称历史从未暴露。开发任务从初始AppWorld世界重执行真实源prefix，重建Python执行状态及相同公共history，不能只load DB快照当完整checkpoint。对固定开发prefix，新版本重新生成完整实际代码块a_new及真实proposal费用；旧版本a_old来自该prefix既有数据。只有完整payload逐字相等且后继policy相同才借用旧suffix的结果/费用；无需哈希、语义等价判定或隐藏状态访问。不同payload执行新的后继rollout；正文/理由仍进入后继的协议不允许仅凭相同动作复用。随机解码只复用本次生成样本条件的结果，不把一次相同推成版本策略相同；匹配和不匹配样本均纳入分母，无支持部分全测。当前新proposal费用必须计入，不能继承旧文本的prompt费用。旧结果只在开发评估器使用，测试runtime不读dev结果或隐藏终态。这里不是只缓存完整prompt：新正文不同但实际动作相同时有可能继承完成证据。

最高近邻及差别：RoMeRL已处理继承Q偏差的逐步修正；EviSkill已有证据卡、局部重执行与跨epoch传播；Dann2023及Harvesting Randomness2017已有同动作counterfactual数据复用，SPIBB已有支持不足时保守policy改进，GUI action-conditioned bisimulation已基于动作结果而非观测相似合并。不能把重合分组、reset、局部replay或matching当新。候选仅剩文本经验正文/理由通过后继消息造成的继承失效与一次暴露接口是否形成额外可检验关系；极可能仍是成熟policy evaluation的直接适配，尚无独立新意证据。

## 最小实验

AppWorld official train构建冻结经验并产生预注册编辑家族，dev保存公共prefix并诊断；official test仅冻结方法后aggregate，禁止逐test任务人工修改/分析。先在dev完整重测建立离线参照（隐藏评测只评估器使用），检验“同实际动作却不同后继结果”是否随正文/理由保留而出现，并检验一次暴露接口是否牺牲经验收益。比较同语义坐标直接继承Q、语义相似阈值继承、每版reset全重测、EviSkill式固定目标区间重执行、经典相同完整history+action分组的coupled rollout，以及当前限定继承域。经典coupled baseline得到完全相同开发prefix、一次暴露formatter和全成本预算，不能故意只允许它对版本ID分组；若它与提案行为/成本等效，则新机制被推翻。全部方法相同编辑序列、actor/temperature、任务划分、公共history/初始world、最大步数、总API+CPU预算，prefix恢复、proposal、回放、构建/判定/验证及重试全部计费。报告所有编辑上的准入错误率、dev全重测参照偏差、有效任务成功/全部测试任务、全链路费用、匹配率/未支持比例。必要对照为接口切断×复用的2×2，正文保留仅作机制消融，避免把干净history本身收益冒作复用增益。若经典coupled sampler等效、编辑很少动作重合、恢复成本抵消节省、或清掉理由使收益下降，则否定。模型、固定暴露事件、编辑数、dev样本、k及总费用单位待用户实验阶段确认，当前不运行。

基线定义/复现：[{"name": "完整可实现的代表Q继承/reset", "paper_url": "https://arxiv.org/html/2608.02508", "code_url": "https://github.com/YOUNG-fnxm/RoMeRL", "reproduction": "官方repo说明eval-only，无在线utility promotion/edit loop；定义标准per-coordinate EMA、版本替换继承Q并reset count，对比替换resetQ后全dev重测，不冒充官方在线完整复现。", "controlled_parameters": "共同冻结actor/数据/编辑序列/history/总预算", "extra_costs": "全部库构建和代表/版本评估费"}, {"name": "经典动作重合coupled rollout", "paper_url": "https://proceedings.mlr.press/v206/dann23a/dann23a.pdf", "code_url": null, "reproduction": "标准完整定义：同开发prefix/history下各版本生成实际完整payload，按直接相等分组；每组共享一次共同后继rollout，不同动作各自执行。不赋予本文专属接口，baseline也使用同一次暴露formatter。这是成熟定义，不宣称复现原tabular理论保证。", "controlled_parameters": "相同actor/解码、一次暴露事件、初始world、费用与所有编辑", "extra_costs": "每版本proposal、每组suffix、prefix重建和分组CPU全部计"}, {"name": "EviSkill固定触发片段重执行适配", "paper_url": "https://arxiv.org/html/2610.05030v1", "code_url": "https://raw.githubusercontent.com/Zhouyaner/EviSkill/main/scripts/run_eviskill.py", "reproduction": "已亲读scripts入口imports wmsm.evidence_pipeline.run_eviskill，l2-replay-ranges-per-edit与post-reject-replay-cap真实参数以及论文C.3；不把README当完整源码。使用完整可实现标准定义：固定支持区间、初始world重执行prefix、editedskill执行区间、同offline结果判断；不复制额外证据卡editor模块造成费用差。官方pipeline细节尚未逐函数核实，不声称完整官方复现。", "controlled_parameters": "同编辑序列和支持prefix/区间/actor/总预算", "extra_costs": "prefix恢复、区间与终态评估全计"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]
