## 背景

**定位关键词：** LLM agents, procedural memory, minimal intervention, action editing

冻结知识/软件agent已经拟定下一条动作时，再把相关经验放进prompt让它整体重草拟可能改变原本正确的部分并引入额外验证。本方向研究经验的干预范围，而非仅看其检索相关性。

当前目标及演化依据：从长计划的‘已写出要求’改为当前草拟动作的受控修改，移除计划意图等同执行覆盖的假设；聚焦Q004-D01/D03，不处理永久淘汰。

https://arxiv.org/html/2403.08978：§3.2-3.3从成对轨迹分歧提取条件建议，并在每步按上下文选择和在prompt内辅助重新生成动作；局部建议生成已覆盖。
https://arxiv.org/html/2608.24876：§2.2.2草拟call不执行，发not-executed结果和技能，再由actor生成动作；本版必须区别于此重草拟。
https://arxiv.org/html/2605.14051：附录E.5要求minimal repair、无修复返回原计划；单纯minimal/noop指令无创新。
https://arxiv.org/html/2605.29794：§4.2及附录B.2 renderer按task及共现skill描述改写，并利用训练trace；不读取当前无经验草拟动作。
https://github.com/StonyBrookNLP/appworld#evaluation：Agent Development Restrictions规定test只 aggregate，train/dev可人工分析；不把task-wise test错误报告用于机制分析。
https://github.com/AnwarDebes/reins：作者系统已有model-free最小工具轨迹edit shield；确定性最小干预本身不是新意，不扩展本方案为攻击防御。

## 核心 Claim

待验证：相同经验知识下，令经验作用为当前默认动作的局部修正、且零修正时执行原动作，能够比上下文条件化重草拟减少旁支程序和成本；差别在默认动作的保留关系，不能由更短提示或一般条件建议单独解释。

## 方法设计的核心思想

每步先产生不读当次经验的默认动作a0（既有history不重置）；以当前任务和已观察工具输出检索同样k条经验。一次冻结模型判定仅返回所需局部修正δ及引用的可见约束，或δ=空。空时直接执行a0，actor不接触经验正文也不重新生成；非空时以a0+δ让同actor只修正该动作，输出仍是actor生成代码/call，不硬编码API。解析器要求工具选择/参数的改动属于δ列出的当前call字段，修正不能引入新流程或未要求的额外验证；无法表示的改动放弃当次经验，保留a0。原经验仍库内供其他动作使用；没有编辑不是整体无价值。判断、编辑调用与失败fallback全计费，既有history可受先前经验影响因此只声称当次增量效应。

最高近邻及差别：AutoGuide条件建议、Recuris草拟动作检索、SPIN最小修复/noop和Reins确定性min-edit都已读并保留。窄差别是自动经验的编辑足迹与‘空修正不让正文进入actor也不重生成’的动作保留关系，采用相同δ内容反事实区分；没有宣称最小修改或条件检索本身新。

补充原文边界：[SkillSmith](https://arxiv.org/html/2605.15215)已把skill编译为最小可执行boundary contract、选择性披露并降低重复解释；本方案不以编译、局部披露或typed runtime为创新，只评经验修正与当前默认动作的恒等域/改动足迹关系。

## 最小实验

AppWorld train经验、dev划分为参数选择/机制诊断两部分、test只aggregate成功与费用。dev复制同一合法前动作checkpoint，a0与经验固定，随机比较：AutoGuide式条件建议重草拟、长度匹配条件建议、P0最小编辑prompt、相同δ但总是重新生成、保留默认动作的局部算子、无经验。所有臂相同预动作调用和可见输入，开发建库/检索/判定/编辑/重试计同全链路总预算；不执行额外循环的臂可将剩余费用用于同预算actor。诊断检查δ=空时下一动作是否相同及整条任务额外操作是否下降；δ非空时改动足迹及最终成功。人工编辑判定/逐任务错误只train/dev，test只冻结后的aggregate结果。支持需‘相同δ内容但保留默认动作’改善成本且成功不降；若长度匹配/普通no-op策略同样有效、默认动作保留无额外作用或大量改动不能局部表示，则推翻。模型、字段解析粒度、k、样本/预算/非劣界待用户确认。

基线定义/复现：[{"name": "无经验/固定top-k/独立贡献屏蔽", "paper_url": "https://arxiv.org/html/2606.15390", "code_url": null, "reproduction": "完整标准定义：无经验不注入；top-k按固定文本相似度取k条；独立屏蔽在开发任务对固定Bernoulli掩码有无经验的成功差取均值、同任务邻居加权后仅保留非负条目。是明确标准基线，不冒充ASSAY官方实现。", "controlled_parameters": "同actor/解码/任务划分/技能库/检索容量/全链路总预算", "extra_costs": "开发归因rollout、embedding、注入、任何重试全计费"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]
