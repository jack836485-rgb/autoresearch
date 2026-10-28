## 背景

关键词：context compression、belief update、metamorphic testing。当前处理Q002正确澄清后的旧约束/多回答绑定及Q003同边界压缩后的合法错实体；依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)与[TRACE §7](https://arxiv.org/html/2608.06503v1)。聚焦已到达更新，不声称未知未来充分或所有保留未使用问题。

## 核心 Claim

假设澄清所引起的状态变化在两条表示路径间的稳定交互残差，比单次路径差异或直接coverage/preservation verifier更能定位压缩导致的绑定漂移；同总预算下按该残差回填减少Q002旧约束丢失及Q003合法错实体。

## 方法设计的核心思想

从同一可见H、实际u建立四格：先更新后压缩/先压缩后更新 × 实际u/恒等更新u0。恒等更新u0明确不添加事实也不改值；不是隐藏用户知识。对每格用同冻结模型和同投影schema得到字段。每条路径内比u与u0，得到字段转移（旧值/新值/不变/未定），跨路径只把转移不一致的字段列为候选；重复同格一次，只有同格转移稳定而跨路径仍不同的字段可选。所选字段的实际问答和原约束逐字回填重压缩一次；其余差异不修，不以一致性作正确性保证。该选择关系是实际更新×顺序交互，拒绝u0已存在差异或同路径抽取噪声。

[TrustMem §3.2](https://arxiv.org/html/2606.25161v1)直接验证coverage/preservation/faithfulness；[METAL](https://arxiv.org/html/2312.06056v1)已有一般变形一致性；[Useful Memories](https://arxiv.org/html/2605.12978v1)已有整体更新顺序效应。当前不声称这些既有原理为新。

## 最小实验

固定CPU AppWorld环境、同澄清问题和正确实际回答。只用不改变原任务终态的澄清：把原指令一个可见选择暂写为未知，用户答回原值，终态评估函数不改；多问题作合成澄清依旧答回原值。所有任务计数，离线独立标签。对照：(1)单路径结构摘要；(2)最近完整问答逐字保留；(3)同四格/重复调用数按单次两路径差异回填；(4)同调用预算直接验证coverage/preservation/faithfulness再按违例回填；(5)同格重复噪声驱动回填。共用同压缩器、来源候选、回填token上限、actor/解码/总输入输出预算；每格H输入、U、C、P、重压缩和续跑全部算，检测挤占续跑。主报所有边界的旧约束/绑定正确、合法错对象、TGC；预注册首动作相同且blocked/repeated均未报警子集占比和条件错误，不替代全样本。若交互残差不比直接验证准确，或只同格噪声即可解释增益，或预算挤占消除净收益，推翻。模型、预算、重复次数和样本数待用户确认；重复一次为设计定义可经确认调整。

公开[AppWorld实现](https://github.com/stonybrooknlp/appworld)的AppWorld(task_id)、world.execute、load_task_ids、world.evaluate已核实。冻结直接验证是同任务可完全实现的标准定义：给H、u、旧/新摘要标coverage/preservation/faithfulness及来源原文，按同预算修一轮，不冒称复现TrustMem训练。
