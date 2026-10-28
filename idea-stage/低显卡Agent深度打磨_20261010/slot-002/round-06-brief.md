## 背景

关键词：abstract interpretation、conformant planning、entity binding。Q002正确澄清后旧要求/绑定仍可丢失，Q003压缩后合法动作可用错实体。依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)和[TRACE §7](https://arxiv.org/html/2608.06503v1)。当前聚焦丢证据却生成更确定绑定的关系；这是待测压缩机制假设，不声称原作已量化其频率，不覆盖所有更新使用失效。

## 核心 Claim

假设压缩对原已见来源的遗忘，应扩大可能绑定集合而不能制造新的唯一绑定；把这一信息偏序约束落实到摘要修正与下一动作选择，可减少正确澄清后及压缩后的自信错实体。

## 方法设计的核心思想

用同一冻结API模型将已见指令、实际完整问答、工具schema变成有限binding候选和可见约束，CPU枚举B_H；同样抽取摘要的B_C。不读隐藏知识或gold。若B_H不包含于B_C，摘要排除了来源仍允许的可能状态：把导致缩小的生成断言替换为其可见允许集合/unknown，而不恢复整段H；受同token上限。actor提出下一动作时仅当其目标在保留的可能绑定下相同才直接执行，否则按正常工具读或已有问答原文回取消除该分歧。完整原文也不当真值：抽取不完整时只能条件性保留关系，没有通用soundness保证。不跑合成反事实工具，不加安全拒绝。

[Cousot抽象解释](https://cs.nyu.edu/~pcousot/COUSOTpapers/POPL77.shtml)和[Conformant-FF](https://www.cs.bgu.ac.il/~brafman/cff.pdf)已覆盖超近似/多可能状态决策原理，不申报新定理。[SAGE](https://arxiv.org/html/2511.08798v1)维护参数域，[TANGLE/CAAP](https://arxiv.org/html/2608.13921v1)已有保留不确定/冲突再决定；此处试图将摘要生成的知识增加限定在压缩前联合可能集合内，是否仅应用适配应独立判断。无法假定自然语言集合枚举完整。

## 最小实验

公开AppWorld API合成明确回复，控制压缩删除一条绑定依据与文本长度匹配。对照同模型自然摘要、同抽取但单值化、只保留joint binding表、相同额外预算直接原文回取；另将FOCUS原文完整span引用和遗漏补救定义在同任务实施，TRACE公开模板/runner在入口核实后作为额外任务对照而不虚称已复现。所有边界计候选漏gold/约束抽取错、B_H与B_C的误缩小、合法错实体、澄清额外次数、进展停滞和Task Success。离线oracle B只做标明的诊断上限，不作在线输入。若仅oracle parser条件好、未知集合导致同预算进展更差、或joint表即相同，则推翻。actor/解码/模型/完整token与工具预算一致，解析/CPU枚举/压缩/回取/续跑全部计，未定域大小/任务数/预算留待确认。

[AppWorld实现](https://github.com/stonybrooknlp/appworld)入口已核实。有限域由公开API已见对象/schema构造，同抽取器、相同候选和相同source用于所有方法。已在线亲读[TRACE runner](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/collect/runner.py)与[loop](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/optimize/loop.py)：前缀重放自由续跑可实施，原harness未发布，新adapter标明为重实现新cohort；base模板已核实。不能拿README当完整原系统复现。所有在线方法不使用gold候选/终态，parser错误/漏候选和全部失败都计分，本轮不实验。
