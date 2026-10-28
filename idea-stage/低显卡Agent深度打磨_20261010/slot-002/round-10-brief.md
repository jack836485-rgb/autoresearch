## 背景

关键词：consistent query answering、repair invariance、memory compression。[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)报告正确回答后的问答错绑/旧要求遗忘；[TRACE §7](https://arxiv.org/html/2608.06503v1)承认合法非重复动作也可静默错状态。当前假设Agent从正确多问题问答抽取的约束可能因归属解析产生冲突；Q002测归属/旧要求，Q003测该分歧跨压缩后的合法错目标。冲突来自Agent解析的假设，不把用户答对后的源冲突作为已证实根因，不承诺全部记忆使用问题。

## 核心 Claim

源约束的不同包含极大一致修复可能允许相反动作，摘要却把这种源分歧折叠为某动作在全部修复中成立。只检查这一跨表示的确定性变化，并保留决定源分歧的问答见证，在同完整成本下能否改善错绑和合法错实体是待证假设；稳健全修复推理本身已有原作。

## 方法设计的核心思想

同冻结API模型从可见指令/实际Q&A构F_H，从摘要构F_C；公开schema和可见实体ID/字段值提供同有限联合绑定域。source约束是允许/排除实体、参数或问答归属的有限关系，unknown不排除；显式原文supersession先处理，不把合法新旧值当冲突。CPU枚举F所有按集合包含极大的一致source子集R(F)，以及每个子集的可行绑定，不按最大基数或模型分数挑唯一修复。

只当H中两个不同修复分别存在满足/不满足当前调用目标要求a的可行绑定，同时C所有修复的所有可行绑定均满足a，才触发。将这对不同修复动作见证所涉及的实际问题/回复/旧约束逐字回填一次重压缩，任一repair不当用户真值。H一致、H全部排除a、底层域无解、枚举预算不能穷尽均不触发/unknown并记未覆盖；不得把空集上的全称当证书。全部repair共同错误或有限域漏掉真实绑定仍无法保证。回填后仍未定正常回读原问答/澄清，真实计成本，不宣称消除了全部不支持确定性。

[PODS1999 §2](https://www.cs.toronto.edu/~marenas/publications/pods99.pdf)已有minimal repair/all-repair CQA；[QXR §3–4](https://arxiv.org/html/2601.13600v1)已有自然语言事实MUS与greedy hitting-set修复，系统性LLM误判不能靠重复解决；[知识动作修复 §4/7](https://www.ijcai.org/Proceedings/13/Papers/126.pdf)已有多repair执行语义及一致查询控制progression。[KR2025逻辑修复框架 §3](https://proceedings.kr.org/2025/32/kr2025-0032-frohlich-et-al.pdf)已用正/负query约束关系连接不同数据库实例并限制新增答案；所以不同表示间的答案保存也不是新理论。它定义修复空间，不直接给当前自然语言压缩的双修复见证回填策略，该剩余差别也可能只是应用，须独立判断。多修复、冲突定位和稳健动作均不申报新，独立性只可能在同源分歧跨压缩消失时的回填选择关系，而非经典修复语义的重命名。

## 最小实验

AppWorld公开多实体/同字段问题，包含互斥或共享子句、独立问题和合法显式更新；固定同正确回复、源parser及压缩边界，原终态目标不改。主实验不在线注入隐藏错误，不筛解析冲突/成功任务；统计源确有不同repair分歧、源唯一、源全排除及枚举unknown的比例，若分歧几乎不出现则该方法缺乏主任务价值。

同F_H/F_C抽取、schema/域、来源集合/回填cap，比较QXR原文MUS/greedy单repair透明适配、固定tie单repair动作检查、完整多repair JSON、直接joint source/preservation verifier、最近完整Q&A、本跨表示选择。完整repairJSON与当前方法共享压缩前的全部repair信息；共同用公开溢出次序/驻留上限并报告实际保留量，不能把截断JSON称信息等价。统一恢复/澄清规则与完整费用，避免把候选数量或多问用户当机制收益。QXR算法1及附录G oracle提示已亲读，可按公开定义实现；不声称原作已有AppWorld agent结果或完整作者代码已核实。

全任务报信号对离线错绑/旧约束/合法错目标的定位与漏检、终态成功、澄清/回读及完整成本；H一致/全排除不触发不计作检测成功，parser和域共同错如实报告。若完整repairJSON相同、QXR/直接joint验证不弱且更省、信号仅由parser误差驱动，或枚举/澄清挤占续跑无净收益则推翻。固定actor/解码/总输入输出与工具预算；全部source/摘要parser、QXR子集oracle、CPU枚举、验证/回填/压缩/续跑/重试计费，oracle绑定/终态仅离线评价。模型decode、枚举上限、总预算/样本待确认。[AppWorld官方_setup/solution/evaluation](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)入口已亲读；本轮不实验、不调用付费端点、不生成实验代码。
