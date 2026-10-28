## 背景

**定位关键词：** LLM agents、procedural memory、plan editing、negative transfer。

相关经验仍会让软件/知识工作agent重复本已计划的检查。本方向把经验的处理单位从整条程序改成相对当前无经验计划的可证实差异。

从贡献分数/全局淘汰转向同一任务中actor已有计划与经验干预的差异，预计处理成本负迁移；不处理Q004-D02永久淘汰或judge噪声。 原始过量验证证据：[SkillTriage §V-B/表IV](https://arxiv.org/html/2608.11888)。这是待检验机制，未运行正式实验。冻结actor，运行时只读任务/工具观测，不读隐藏故障或评测终态。

## 核心 Claim

待验证：技能相关性不等于需要注入整套技能；若当前无经验计划已经覆盖技能要防止的具体失败，只发送该计划相对经验所缺少的有证据约束，能减少程序重启/重复验证而保留经验对缺失动作的收益。

## 方法设计的核心思想

所有方法先由同冻结actor生成短计划P0，额外费用全计。开发时在成对skill/no-skill轨迹中提取可见任务要求、计划动作和最终实际工具动作，生成带前提的最小计划编辑经验e=(observable condition, undesired plan pattern, edit)。测试时检索相同k条，但只暴露与P0模式匹配的edit；P0已满足前提的条目输出空编辑。编辑只能增加当前任务要求但P0缺失的约束、替换已知误用动作或删除明示可选的重复检查，禁止臆造隐藏任务要求。保留原经验用于其他P0，但不把无编辑当整体无价值。

最高近邻：[Recuris §2.2.2](https://arxiv.org/html/2608.24876)已在草拟call时注入技能再重草拟；[SkillX](https://arxiv.org/html/2604.04804)已有pseudo-plan检索；[DeltaMem](https://arxiv.org/html/2606.03083)已有经验间差分后重建全经验；[成本改写 §3/附录F-G](https://arxiv.org/html/2606.09421)按任务/技能结构保留锚点。这些都不作为当前贡献。当前可疑差别仅为按P0拒绝零边际信息、暴露变成条件编辑，是否属于state-grounded memory局部工程化需要直接判断。
[BACKTRACE](https://arxiv.org/html/2607.27484)已干预技能意义、措辞、身份、内容和分配；本方案不把换措辞、行为归因或对比轨迹当新意。[CTA §3](https://arxiv.org/html/2605.11946)明确paired trace为描述性对比；本方法的生成轨迹不能当成因果已证实。[CMP §2–3](https://arxiv.org/html/2610.02070)已处理随机检索识别/不可逆淘汰；本方案不声称解决全局淘汰。

## 最小实验

AppWorld公开CPU任务，train构建经验，dev选编辑与阈值，test冻结。相同P0生成过程/actor/解码/库/检索k/全链路总预算，比完整技能、任务条件改写、Recuris式草拟动作后全技能重草拟、只删除重复文本、计划相对edit。报告全部任务成功率、每任务总费用、重复检查/程序重启次数和编辑错误率（最后仅离线人工/结果复核）。机制交叉：P0已覆盖 vs P0未覆盖技能要求；只有已覆盖组减重复而未覆盖组保留收益才支持。若只是缩短token或依赖额外planner预算，推翻。模型、k、任务量、计划长度与总预算待确认。

可跑环境入口已亲读：[AppWorld environment.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/environment.py)的execute与save/load_state；[react_code_agent.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py)的next_execution_inputs_usage_and_status记录usage、读输出、生成代码；[agent.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/agent.py)为执行循环。本阶段未安装/执行。基础无经验、top-k、逐条屏蔽可按完整标准定义实现：同库同检索，分别不注入/取固定k条/开发集随机mask有无该条成功差加权后非负保留。Recuris式动作前全技能重草拟与任务条件改写属于限定机制对照，不冒充官方论文完整复现；若关键区别必须依赖官方完整复现而暂不可得须记录阻断。P0、经验构建、embedding、编辑提炼/选择、验证及重试全部计入总预算；无经验可把省下费用用于actor。