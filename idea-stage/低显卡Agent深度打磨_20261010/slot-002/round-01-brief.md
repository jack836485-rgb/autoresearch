## 背景

定位关键词：context compression、belief update、bidirectional transformation。正确澄清回答仍可被错绑，压缩后合法工具动作亦可用错对象。当前聚焦已到达问答更新跨压缩的作用：Q002检验问答目标与旧约束，Q003检验更新压缩后的静默对象错误。依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)和[TRACE §4.1/§7](https://arxiv.org/html/2608.06503v1)。未知未来充分性不在当前Claim内。

## 核心 Claim

假设同一实际澄清更新先更新后压缩与先压缩后更新的约束投影差异，能够识别单步动作一致及blocked/repeated信号遗漏的绑定漂移；依差异支持的来源回填在同完整预算下减少合法错实体动作。两路径均不是真值，不能发现共同错误。

## 方法设计的核心思想

H为澄清前可见历史，u为实际问题和回复，C为固定预算压缩，U为同一冻结模型的结构状态更新。比较P(C(U(H,u)))与P(U(C(H),u))，P只提取对象、约束及完成/待办。两路径不执行工具，不读oracle。差异字段对应的问题、回复和仍受影响的原始约束逐字回填，共享token上限内重压缩一次；无差异用原摘要继续。[Foster lenses](https://www.cs.cornell.edu/~jnfoster/papers/lenses.pdf)启发更新传输一致性，但不迁移精确树变换的保证。[FOCUS](https://arxiv.org/html/2609.37590v1)按未来依赖效用保留，[Correct Now](https://arxiv.org/html/2609.20045v1)比较历史对的共同未来；此处是同一已到达更新穿过两种表示的差异选择。

## 最小实验

公开AppWorld API构造双问题交互与压缩边界，固定同一实际正确回答；所有边界统计交换差异、离线绑定/旧约束正确、合法错实体动作和TGC。对照为结构摘要（当前对象/约束/待办表）、最近完整问答原文保留（其余同压缩器）、同探针数均匀回填；皆能完整本地实现。[作者AppWorld入口](https://github.com/stonybrooknlp/appworld)已核实AppWorld(task_id)、world.execute、load_task_ids、独立world.evaluate。TRACE README的trace_cc.optimize已读，仅作协议入口，不声称已核实完整算法。AppWorld-UL专用数据尚未本轮核实，主机制测试先基于公开API可构造任务。无压缩和无相关更新负对照区分U自身波动。actor/解码/问答/工具/边界/token与总推理上限一致；检测、压缩、回填、用户模拟、续跑/重试全计费，额外检测占用续跑预算。若差异主要由U本身造成，或同总预算不及直接原文保留，推翻。模型/温度/总预算/样本数/重复数待用户确认，本轮未实验。
