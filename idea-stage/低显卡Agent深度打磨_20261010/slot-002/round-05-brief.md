## 背景

关键词：partial evaluation、binding-time analysis、context compression。Q002正确问答后仍可遗忘旧要求/绑错回答，Q003压缩后可能合法错实体。依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)和[TRACE §7](https://arxiv.org/html/2608.06503v1)。当前聚焦同一请求内历史固定对象与动作时条件的混合求值，不声称已量化此失败、不覆盖任意未知未来。Dataflow §2–4的计算与结果图，以及部分求值书稿§5.2/§15.5的部分static结构支持该目标的表示依据。

## 核心 Claim

假设混合指令中的历史选定对象与执行时条件，需要沿表达式内部保留不同绑定时刻；按已确认问答部分求值、保留实时工具依赖的剩余选择程序，较完整结构化意图文本或全局冻结/实时标签更能维持澄清绑定与压缩后的正确执行集合，且同总预算有净收益。

## 方法设计的核心思想

冻结LLM将实际指令和问答转为有限公开API可执行选择表达式树：常量对象、谓词、集合交/差、实际只读API字段。每个叶子仅根据明确用户语义/问答来源标记已确认固定或实际动作时读取；未知标签不specialize，保留原句待正常澄清。CPU沿树传播binding-time：只含固定叶子的最大子树用当前已见工具结果/用户选择求值成ID集合；含实时叶子的子树保留表达式，输出“固定结果+剩余表达式”，在动作前以实际正常只读结果继续求值。例如已确认歌曲集合固定，但“执行时仍可用”的过滤仍实时；不预取未来、不用hidden DAG、不训练模型。不是追加closure字段：编译在子树处切断重复的历史重解释，同时禁止提前物化实时条件。抽取错/遗漏或API表达式不支持都作为正常失败。

[Dataflow](https://arxiv.org/html/2009.11423v3)已有图/结果/reference/revision，[STITCH](https://arxiv.org/html/2601.10702v1)已有意图指代固化，[Codec](https://arxiv.org/html/2605.17304v1)已有结构化语义压缩，均不申报这些本身为新。[Partial Evaluation原作者书稿](https://www.researchgate.net/profile/Peter-Sestoft/publication/213882771_Partial_Evaluation_and_Automatic_Program_Generation/links/5704f27108ae13eb88b92a5f/Partial-Evaluation-and-Automatic-Program-Generation.pdf)的经典static表示specialization时已知，不自动等于不变Agent事实；本适配以用户明确时间语义选择cut。方法不用作者gold程序或训练模型。

## 最小实验

公开AppWorld集合任务，任务含全固定、全实时和混合明确时间语义三类；实际问答固定，合法可见更新分别改变历史候选属性或实时过滤字段，所有任务独立离线终态测试。对照：(1)完整同IR树和每叶binding-time标签仅作为结构化文本交给同actor（强信息匹配）；(2)同树采用全局冻结/全局实时；(3)同parser和同树但不部分求值、CPU每次按标签全重算；(4)同预算原文；FOCUS原文计划引用+遗漏补救与TRACE公开模板在同任务同adapter做重实现对照，不声称原harness全复现。主分母全部任务，报表达式/标签抽取错、正确回复作用范围、压缩后合法错成员、Task Success、工具读取/模型token及进展失败。支持需mixed条件相对强完整结构文本有净收益且全固定/实时不下降；若同IR未specialize CPU重算相同、只prompt强度或token分配解释、或parser错误主导/预算无净收益，推翻机制优势。actor/解码/总input-output预算、工具预算、parser调用共享对齐，所有前期解析/压缩/回取/实际读/续跑计成本；表达式语法、模型、budget、样本数待确认。

[AppWorld新任务指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)setup/solution/evaluation和[TRACE runner](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/collect/runner.py)/base模板已亲读，支持CPU任务与前缀重放。原研究harness未发布，同adapter新cohort不能称原作者完整复现。有限表达式树及上述强对照均完整可定义，不用Dataflow原任务成绩作AppWorldbaseline。本轮未运行实验/付费端点/实验代码。
