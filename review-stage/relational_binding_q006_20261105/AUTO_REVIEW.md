# 审查记录

- Call 1（常规，effort high）：IDEA-002，4.5/10，needs_rethink，贡献三项 {'importance': 6.0, 'novelty': 5.0, 'effectiveness': 4.0}，可行性 pass，Gate 结果 failed。主贡献为'锚点捕获'诊断加'最小差异对比对SFT'训练信号。重要性6：关系指令崩溃真实，但GUI-Primitives显示主要瓶颈在候选定位，关系绑定只占少数失败。新颖度5：GUI-Primitives已有候选区域分类与anchor-collapse类型，锚点命中可由公开预测直接算出；UGround(约23.5%相对位置指称)与Jedi已有关系型SFT数据；普通CE SFT下配对只是数据组织，与已
- Call 2（常规，effort high）：IDEA-003，5.5/10，promising_needs_revision，贡献三项 {'importance': 6.0, 'novelty': 7.0, 'effectiveness': 6.0}，可行性 pass，Gate 结果 failed。主贡献为免训练'锚点→关系几何区域→局部放大定位'流程，加对'瓶颈在候选定位'的确认。重要性6：问题真实，但应用面窄（planner 通常可直接点名目标），主集仅185条，且诊断结论原论文已给出。新颖度7：GUI 领域未检索到锚点中心的关系区域方法，但现象非新（GUI-Primitives 已用 oracle 候选标注得出），机制是 REC 经典做法（ReCLIP），GUI 侧适配偏工程。有效性6
