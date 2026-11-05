# 审查记录

- Call 1（常规，effort high）：IDEA-004，5.5/10，promising_needs_revision，贡献三项 {'importance': 6.5, 'novelty': 5.5, 'effectiveness': 5.5}，可行性 pass，Gate 结果 failed。主贡献是解释 compaction agent RL 的增益主要来自执行器耐受（以 2×2 交换检验），再加上阻断重获取的兄弟 summary 续写记功。重要性中等：compaction RL 已进入生产管线，但在可重获取环境中执行器重读本身可用，summary 变好的价值主要在效率与不可重获取信息上，而后者只在合成约束上检验。新颖度受限：兄弟分叉加 summary 专属信用已有 TreeMem，
- Call 2（常规，effort high）：IDEA-006，4.5/10，needs_rethink，贡献三项 {'importance': 6.0, 'novelty': 5.0, 'effectiveness': 5.0}，可行性 pass，Gate 结果 failed。主贡献是使用时刻事后重标注、施加到整条携带链的 writer 偏好信号。A 在 DSSR 原协议内实现了 DSSR §7 自己点名的修补方向（相当于补完起点论文）；B 的摘要 token 附加优势加回传已被 HiMPO 在 BCP 上覆盖。保留率上升在机制上可信，但长延迟胜率受 F′=0 时约 10% 的上限压制；brief 误述 GUIDE 在每个延迟都更好，判别前提不成立；B 的重读触发证据来
