## 背景

**定位关键词：** LLM agents, procedural memory, selective labels, costly feedback

软件知识agent可能从经验学会省去检查；这既改变成本，也改变哪些失败能进入下一轮经验治理。本方向研究经验对观测通道的影响，不把缺检查等同已成功。

当前目标及演化依据：从任务内重复呈现转向跨任务反馈选择；新增Q004-N01是由原噪声边界和检查成本证据提出的待验证假设，不宣称已观测。只处理有公开验收检查的任务，不用隐藏benchmark测试为在线信号。

https://arxiv.org/html/2605.22148v3：§7把skill贡献的router选择混杂与固定外生judge通道的适用范围区分；未证明内生反馈盲点已发生。
https://arxiv.org/html/2608.11888：§V-B经验可导致过量检查，成本策略是合理目标；不能把反方向‘经验少检查导致反馈消失’当已观测事实。
https://arxiv.org/html/2609.36746：§3.2将环境暴露反馈与self-assessment作为资料，并将missing标为unavailable；§3.4明确时间credit仅近似归因，非精确causal。
https://arxiv.org/html/2610.02070：CMP已恢复retrieval positivity；未以memory改变后续测量选择为本版贡献，不重提随机检索本身。
https://arxiv.org/abs/1807.00905：Selective labels中决定过程决定哪些结果会被观察，单纯样本选择调整在零支持区域无法识别。
https://proceedings.mlr.press/v337/schur26a.html：可选且action-dependent付费观察的bandit已有理论，不把‘为标签付费/随机审计’当新意。
https://arxiv.org/html/2608.19626：测试演化可能把单一接受程序的输出误当ground truth；本版不能把自动新生成测试当真值。

## 核心 Claim

待验证：在经验能够改变公开验收检查执行概率的任务流中，以观测到的成功/失败直接治理经验可能把少观测误当少失败；将经验暴露与是否测量分别随机化、且测量在任务提交后不修改当前产物，能区分经验任务收益与经验诱发的反馈盲区，并减少错误保留。

## 方法设计的核心思想

任务必须含操作者已公开的独立验收检查集合，测试定义固定且不是agent自动写出的ground truth；隐藏评测器只离线。开发/可控训练流对经验on/off按共同已知概率分配；actor完成并提交产物后，以独立于经验内容的已知审计概率随机执行公开检查，不让测量反馈修复当次产物。记录检查是否运行、原返回值与费用，缺测保持unknown。经验治理只使用暴露×测量的双随机记录，经测量倾向加权估计对同一公开检查失败的净影响；不能将public-check pass称完整任务成功。测试流冻结actor/经验生成/审计制度，治理只读此前公开反馈，未来隐含真值不给方法。正作用但少检查的经验只在公开检查效应证据可辨时保留，证据不足不据未观测pass晋升；不宣称通用最优保留。

最高近邻及差别：CMP已随机检索，EASE已处理missing与行为概貌，selective labels/costly bandit已有观测选择理论。可能的独立差别是文本经验持续演化其自身反馈通道、任务提交后测量仅影响后继经验库的闭环；尚未找到直接机制覆盖，也未核实自然软件task数据具备这种反馈选择。

## 最小实验

未来用公开CPU软件任务构造自然public acceptance tests与独立hidden holdout tests：前者为方法合法可见工具、后者仅离线最终评价，先在开发任务验证经验是否改变公开检查率，不伪造该效应。相同actor/解码/任务流/初始库/核心预算，比较固定外生反馈治理、actor自主检查治理、missing=unknown、仅随机暴露、仅随机测量、双随机暴露/测量。双随机引入的审计、经验构建/估计/重试全计总费用，各臂可用省下费用继续actor或公开检查但须预注册一致分配。指标公开检查通过/全部被审计任务、加权公开失败估计误差（dev全审计参照）、离线hidden最终成功/全部任务、错误保留、成本及任务序列末端库质量。若memory不影响检查率，missing=unknown或标准costly-bandit已充分解决，或收益仅来自多检查预算，则推翻。模型/任务来源/检查开销/概率/总预算/分摊规模待确认；本阶段不运行。

基线定义/复现：[{"name": "无经验/固定top-k/独立贡献屏蔽", "paper_url": "https://arxiv.org/html/2606.15390", "code_url": null, "reproduction": "完整标准定义：无经验不注入；top-k按固定文本相似度取k条；独立屏蔽在开发任务对固定Bernoulli掩码有无经验的成功差取均值、同任务邻居加权后仅保留非负条目。是明确标准基线，不冒充ASSAY官方实现。", "controlled_parameters": "同actor/解码/任务划分/技能库/检索容量/全链路总预算", "extra_costs": "开发归因rollout、embedding、注入、任何重试全计费"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]
