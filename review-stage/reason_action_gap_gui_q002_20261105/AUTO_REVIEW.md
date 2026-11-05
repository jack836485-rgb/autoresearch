# 审查记录

- Call 1（常规，effort high）：IDEA-003，5.0/10，promising_needs_revision，贡献三项 {'importance': 6.0, 'novelty': 5.5, 'effectiveness': 4.5}，可行性 pass，Gate 结果 failed。主贡献是把 FTB 的纠错增益和通道拆解迁移到 7-8B 视觉 CUA 的真实惯性状态，并用失败条件化 unlikelihood 在权重中压制失败动作的复制。重要性有限：R³ 与解码屏蔽都显示压低重复后任务成功不变，惯性在失败中的分量未获支持。新颖度是增量的：SEAgent 已有负向模仿损失，CPL 已有无奖励的反上下文模仿训练，FTB 已把训练修法列为开放问题。有效性只支持“能降 p(a_fai
