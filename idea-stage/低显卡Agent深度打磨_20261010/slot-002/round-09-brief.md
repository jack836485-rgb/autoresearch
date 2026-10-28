## 背景

关键词：conditional functional compression、observed side information、action constraints。[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)报告正确回答后的问答错绑和旧要求遗忘；[TRACE §7](https://arxiv.org/html/2608.06503v1)承认合法非重复动作也会有静默状态错误。[2608.16370 §3.3](https://arxiv.org/html/2608.16370v1)已经区分可查询状态与历史依赖状态，分类原理不新。当前聚焦同一真实环境观察下哪些历史约束不可删除：Q002测已给对的问答/旧要求，Q003测该目标域中的合法错对象，不承诺未知未来充分性。

## 核心 Claim

假设历史见证能否由当前环境观察替代，取决于观察与剩余历史的联合约束，而不只是字段可查询或候选间可区分。先取得实际只读结果，再保留使非空可行目标集合不变的原文子集，在同实际查询与完整成本下可能优于静态分类/区别对覆盖地保住排除关系并压缩冗余。

## 方法设计的核心思想

冻结API模型从可见H、实际问答及公开schema构同一有限候选调用域A和source约束F。约束表述某候选调用的目标/参数是否满足可见原要求；unknown不作排除，绝不读取金标准程序。先由同公开规则选择正常只读API并实际取一次结果r，各方法共享同组实际query；不预测未读值，不执行候选写操作。

CPU计算该有限域中同时满足F和r的目标集合T(F,r)。源解析为空时回读实际原问答，仍空则unknown/正常澄清，不能将空集当保留证书。按固定source顺序尝试删除整条历史见证f，只有T(F减f,r)=T(F,r)且非空才删；剩余原文见证与真实r进入同常规压缩器后续跑。历史用户选择不会因API字段可读就自动删，删它仍须不改变目标集合。这不同于只保留支持/未知/排除的候选分区：能区分两个调用并不代表排除了错误调用。自然语言parser和候选漏项可共同错，方法不保证集合包含真实目标；当前观察改变后不保证长期充分性。

[Functional Compression through Graph Coloring §I/III](https://www.mit.edu/~medard/2010papers/funccomp.pdf)的f(X,Y)条件编码及图着色已知，准确函数/分布不能假设由LLM给出；[复杂自然语言目标的值导向压缩](https://www.isca-archive.org/interspeech_2011/crook11_interspeech.pdf)已有已知POMDP模型的目标集合压缩；[HiGram §3.2](https://arxiv.org/html/2608.05095v1)已有按query/update定位证据路径。此处独立性只可能在真实API返回条件下的有限动作约束选择关系，不把条件编码、query-aware retrieval或约束冗余消除本身算新理论。

## 最小实验

AppWorld公开正确澄清边界，在同H及同实际query组下，配对真实返回让某历史约束冗余/不可替代：唯一/多个当前实体匹配、当前属性改变但历史选对象不变。原终态目标不改，所有任务保留，不筛source解析成功者。共享parser/候选域/source顺序/查询/驻留上限，比较静态可恢复性分类+候选区别对覆盖、普通结构摘要、最近完整问答原文、上述条件删除、全部历史强对照及直接source支持验证。全部历史超预算按同公开完整片段次序截断并记录覆盖，不假称信息等价；不为匹配call数白送构建成本。

全任务统计T与离线真实绑定的偏差、排除关系丢失、旧约束、合法错实体、终态成功与完整成本；空解析/域漏项/多目标均计入。所有schema/source读取、parser、CPU枚举、实际工具和返回token、压缩/续跑/澄清/重试从总预算扣，额外检测挤占续跑；同actor/解码/总输入输出及工具预算。若静态分类已足够、强对照相同、条件删除导致错目标或完整成本无净收益即推翻。查询选择规则/数、域枚举上限、source顺序、模型/解码/总预算/样本数交接待确认。

[AppWorld _setup/solution/evaluation公开指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)已亲读，评估预期及非预期终态变化。所有同任务约束/删除/覆盖对照为完整标准定义，非成熟POMDP原作复现；FOCUS原文§5/A.7确有AppWorld评估，但此处仅按其原文方法透明重实现，公开阈值/溢出协议，未核实完整作者代码。TRACE公共runner可新cohort，原研究harness未公开。本轮无实验、无付费端点、无实验代码。
