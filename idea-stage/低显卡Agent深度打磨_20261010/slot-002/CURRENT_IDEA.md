# 最终研究 Idea：用更新与顺序的交互残差选择回填

最终候选：IDEA-004。检索日期：2026-10-10，Asia/Shanghai。第2轮独立审查7.8、无fatal、初选合格且Gate通过；当前Q002/Q003均已完成10/10有效审查，总控决定追加0轮。**尚未运行正式实验，以下效果都是待证假设。**

## 术语表

| 术语 | 全称／中文含义 | 本方案作用 |
| --- | --- | --- |
| H | Visible history／可见历史 | 澄清前已经出现的指令、问答和工具结果 |
| u、u0 | 实际更新、恒等更新 | u是实际问题与正确回复；u0明确不添事实、不改值 |
| U、C、P | 状态更新、固定预算压缩、字段投影 | 全部定义冻结，分别处理更新、缩短表示、读取对象/约束/完成待办字段 |
| 更新×顺序交互 | 本方案定义的字段转移关系 | 比较实际更新相对恒等更新的作用，是否因更新与压缩顺序而不同 |
| 同格稳定 | 本方案定义的重复一致性 | 同一格重复一次，仅过滤实际观察到的不稳定 |
| TGC | Task Goal Completion／任务目标完成 | 由独立AppWorld评价任务终态，不作为在线输入 |

## 1. 初始目标、研究变化与当前目标

Q002关注正确澄清后仍丢旧要求或错绑回答；Q003关注压缩后的合法、非重复错实体/错状态。初始drawbacks为Q002-D01、Q003-D01、Q003-D02；pre_solution_idea为null，没有沿用必需初始机制。

[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)直接报告正确回答后的要求遗忘和回答对应失败，但没有给独立发生比例。[TRACE §7](https://arxiv.org/html/2608.06503v1)指出blocked/refetch可能漏掉静默状态错误，但没有证明它们主要由问答错绑造成。本方案把这条连接保留为待检验假设。

初始001比较两条更新/压缩路径的任何字段差异。独立反馈指出重复抽取、来源恢复和直接验证的混杂，004把选择关系改为**实际/恒等更新×操作顺序的交互**，再用同格重复稳定性筛字段。其余实质分支独立审查后保留真实低分与覆盖结论；最终不合并未过Gate的机制。

当前声称处理Q002-D01与Q003-D01中的已到达澄清更新传输。未知未来充分性、自然用户任意改目标，以及Q003-D02中“值已可恢复但actor仍选旧值”的全部失败暂不处理。冻结API模型、CPU环境、完整成本和无在线oracle约束均保留。

## 2. 背景、失败条件与已有处理

错误对象调用可以成功返回，下一步也不必重试，因此合法执行不能证明历史约束和回答归属被正确维护。FOCUS已有未来规划引用与负约束救回，TrustMem已有覆盖、保存和忠实性转移验证，原文保留与顺序敏感性也都有原作。本研究不把这些原则重新申报为创新。

剩余问题是：在一次实际澄清到达后，**跨表示的更新作用差异**是否比直接语义判断更准确地选择需要保留的来源。普通两路径不一致可能在无更新时就存在，也可能来自投影波动；四格与重复控制只帮助区分这些可观察关系，没有天然正确性保证。

## 3. 核心 Claim 与可证伪预期

在“用户答回原任务选择”的受控澄清中，实际更新相对恒等更新的稳定顺序交互，可能比单次路径差异和直接coverage/preservation/faithfulness验证更准确地定位压缩后的绑定漂移。用所选字段的实际问答及原约束逐字回填，在同完整预算下应减少旧约束丢失、错绑和合法错实体，并产生任务终态净收益。

以下任一结果都削弱或推翻该Claim：定位不优于直接验证；同格噪声选择足以解释收益；最近完整问答保留更省且不弱；检测挤占续跑后净收益消失。两路径稳定地一起错、或actor忽略正确字段，均可能让方法失效。

## 4. 方法设计

输入是同一可见H、已经到达的u及原文来源；输出是经过一次选择性回填的摘要。检测不执行候选工具动作，不取任一路径作为真值。

| 操作顺序 | 实际更新u | 恒等更新u0 |
| --- | --- | --- |
| 先更新、后压缩 | P(C(U(H,u))) | P(C(U(H,u0))) |
| 先压缩、后更新 | P(U(C(H),u)) | P(U(C(H),u0)) |

U使用同一冻结更新定义，C使用同一压缩定义和驻留上限，P使用共同字段schema。先在每条路径内比较u与u0的字段转移，再比较两条路径的转移；比较应包含实际字段值以及更新、不变、未定的状态，不能仅比较“都更新了”这一标签。u0已有的表示差异本身不是选择理由。

四格各重复一次。只有同格转移在重复中一致、跨顺序转移仍不一致的字段可以入选。读取这些字段对应的实际问题、回复及原始约束，在共同回填上限内逐字加入摘要，然后按同C重压缩一次。无入选字段按原摘要继续；不反复验证修到通过。

例如两条路径都把一个回答作用于不同对象时，问题不是接口是否合法，而是更新作用是否随表示顺序改变。此关系只能提出要回读的来源，不能证明哪个对象正确。实际回填仍可能再次被压错。

最小实现只需要已有轨迹、冻结API调用、字段记录和一次来源回填，不训练权重，不要求模型内部激活，也不引入候选查询联合优化或修复空间模块。字段schema、来源定位和超预算次序在实现前固定并公开；不确定参数交由实验规划确认。

## 5. 最高近邻与独立差别

| 已核验原作 | 重合 | 经审查保留的差别 |
| --- | --- | --- |
| [TrustMem §3.2](https://arxiv.org/html/2606.25161v1) | 冻结验证器直接检查局部转移的coverage、preservation、faithfulness | 当前以实际/恒等更新交叉顺序的稳定转移差异选择来源；直接验证必须作为强对照 |
| [PAIR §3.2/4](https://arxiv.org/html/2609.36526v1) | 同状态比较压缩后的执行后果，并适配压缩 | PAIR聚合续跑结果作离线提示适配；当前用可见文本关系作实例回填 |
| [MORTAR §III-C–E](https://arxiv.org/html/2412.15557v4) | 多轮变形、上下文等价和输出关系检测 | 没有当前实际/恒等更新×压缩顺序的字段转移选择；不是可直接搬用的AppWorld baseline |
| [Correct Now §3/4.4/5.3](https://arxiv.org/html/2609.20045v1) | 更新敏感的充分性审计、保留与读出区分 | 其四端点是两个历史×两类未来；当前是同H的实际/恒等更新×操作顺序 |
| [Commutator Memory](https://arxiv.org/html/2609.34348v1) | 操作顺序差异的局部投影与干预 | 原作在梯度/权重空间，需要内部访问；当前是冻结API文本状态，不把一般顺序干预算新 |

独立第2轮判断为7.8、无fatal，边界限于表中的具体选择关系。较早[双向变换lenses](https://www.cs.cornell.edu/~jnfoster/papers/lenses.pdf)是跨域启发，精确树变换法则不能直接保证自然语言一致性；[METAL](https://arxiv.org/html/2312.06056v1)的重复一致性、[Useful Memories](https://arxiv.org/html/2605.12978v1)的原始经历保留也已存在。无完整实现的近邻仍属于创新边界，不因不可直接运行而忽略。

## 6. 最小验证与可复现性

采用CPU AppWorld。将原任务指令中一个可见选择暂写为未知，再让用户以固定正确回复答回原值；多问题条件同样答回原值，**原任务终态评价不改**。这只检验正确回答后的维护，不外推任意自然澄清或目标改写。

[官方任务指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)的_setup、solution、evaluation及[AppWorld接口](https://github.com/stonybrooknlp/appworld)已经亲读，支持公开环境构造、world.execute与独立world.evaluate。TRACE已亲读[公共runner](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/collect/runner.py)、[续跑loop](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/trace_cc/optimize/loop.py)和[摘要模板](https://raw.githubusercontent.com/nokia-applied-research/Trace/main/data/compression_policy_base/update_summary.jinja)；采用新adapter、新cohort，不能称复现其未公开研究harness。

共同对照为普通结构摘要、最近完整问答逐字保留、同四格/重复预算的单次实际更新路径差异选择、直接转移验证选择、同格重复噪声选择。后3者共用source候选、回填上限与一次重压缩，隔离来源选择关系；普通摘要和问答保留按共同总预算续跑，不白送检测调用。

直接验证按完整标准定义实现：输入H、u、旧摘要与新摘要，冻结模型标记新增事实覆盖、旧要求保存、来源忠实性违例及对应原文，按同上限回填一次。它是TrustMem验证概念的透明同任务适配，**不是其RL训练系统完整复现**。单次路径差异选择只按一对实际更新状态的差异取来源；噪声对照按同格重复的不稳定字段取来源；问答保留按时间存完整问答，余段用共同摘要器处理。来源超预算次序须事前统一，不能按离线正确标签选择。

所有任务和边界统计绑定/旧约束正确、合法错实体、TGC及完整成本；另外报告定位准确与漏检。预注册首动作相同且blocked/repeated均未报警子集，并报告占比和条件错误，不能替代总体分母或建立根因。标签及终态只用于离线评价，不进入U/C/P或来源选择。

固定核心模型、解码、任务/回复、工具、压缩边界、字段schema、source集合、驻留与回填上限。每格H输入、U/C/P、重复、原文读取、回填、重压缩、用户模拟、续跑及重试都计完整成本；额外检测直接挤占剩余续跑。模型/解码、总输入输出与工具预算、样本和重复次数均待用户确认，当前每格重复一次为已审核设计，不伪造最终实验值。

## 7. 未覆盖目标、已知边界与交接

Q003-D02整体未覆盖；正确记忆未被actor使用、两个路径共同错、稳定投影偏差、无相关更新已有的状态错误均可能漏检。同格两次一致不是概率可靠性保证。字段定位和回填也可能误绑、删掉必要原文或耗尽预算。

原文的描述性失败不是部署频率证据；合成答回原值不是自然目标修改证据。AppWorld-UL专用交互数据完整入口、部分近邻完整代码尚未核实，因此主交接采用已核实公开AppWorld任务接口与透明标准对照。下一步仅为实验规划和参数确认；独立Review通过不等于效果证明。

## 参考文献

- Junzhi Chen等，2026，[AppWorld-UL: Benchmarking Diverse Agent-User Interactions for Tool-Use](https://arxiv.org/html/2607.20536v1)，arXiv:2607.20536v1；Problem来源。
- Guanghui Min等，2026，[Toward Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability](https://arxiv.org/html/2608.06503v1)，arXiv:2608.06503v1；TRACE评测边界。
- Tianyu Yang等，2026，[TRUSTMEM](https://arxiv.org/html/2606.25161v1)，arXiv:2606.25161v1；直接验证近邻。
- Guanghui Min等，2026，[Adapting Context Compression for Long-Horizon Agents with Counterfactual Continuations](https://arxiv.org/html/2609.36526v1)，arXiv:2609.36526v1；PAIR近邻。
- Aaron Guoxiang Guo等，2024（所读v4更新于2026-06-17），[MORTAR](https://arxiv.org/html/2412.15557v4)，arXiv:2412.15557v4；多轮变形近邻。
- Guangzhe Zhang，2026，[Correct Now, Insufficient Later](https://arxiv.org/html/2609.20045v1)，arXiv:2609.20045v1；更新充分性近邻。
- John Sweeney，2026，[Commutator Memory](https://arxiv.org/html/2609.34348v1)，arXiv:2609.34348v1；跨域顺序启发。
- J. Nathan Foster等，2005，[Combinators for Bi-Directional Tree Transformations](https://www.cs.cornell.edu/~jnfoster/papers/lenses.pdf)，POPL2005原文；双向变换启发。
- Sangwon Hyun、Mingyu Guo、M. Ali Babar，2023，[METAL](https://arxiv.org/html/2312.06056v1)，arXiv:2312.06056v1；重复一致性近邻。
- Dylan Zhang等，2026，[Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/html/2605.12978v1)，arXiv:2605.12978v1；原文保留近邻。
- Shantanu Dixit等，2026，[FOCUS](https://arxiv.org/html/2609.37590v1)，arXiv:2609.37590v1；未来引用/负约束保留近邻，原文确有AppWorld评估。
- Junyu Guo等，2026，[When Context Changes: Understanding Update Failures in LLMs](https://arxiv.org/html/2609.38866v1)，arXiv:2609.38866v1；保留与使用的未覆盖边界。
