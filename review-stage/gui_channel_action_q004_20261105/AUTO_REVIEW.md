# 审查记录

- Call 1（常规，effort high）：IDEA-003，4.0/10，needs_rethink，贡献三项 {'importance': 6.5, 'novelty': 5.0, 'effectiveness': 3.0}，可行性 pass，Gate 结果 failed。主贡献是'结构引用 + 屏幕坐标'双输出，配合确定性几何一致性执行，目标是同时得到 index 的无冲突精度和坐标的抗劫持能力。执行规则在两个分支里都执行坐标所在元素（一致时坐标在 ref 框内；不一致时吸附到坐标所在元素），在决策上等价于'坐标 + 吸附'，ref 头不改变执行目标，所以无冲突精度受坐标头限制，Claim (1)(2) 无法靠交叉校验同时成立；任何精度提升只能来自联合训练对坐标头
- Call 2（常规，effort high）：IDEA-005，4.5/10，needs_rethink，贡献三项 {'importance': 5.0, 'novelty': 5.5, 'effectiveness': 5.5}，可行性 pass，Gate 结果 failed。主贡献是按渲染可见性分派标签（可见完整文本跟随像素并做冲突增广，不可见信息跟随结构）的训练规则。重要性有限：可见文本的结构-像素冲突在真实网页中主要来自过期快照，真正的对抗注入面（不可见节点、aria/title、幽灵节点）按设计继续被信任，'打破覆盖与信任的取舍'在安全意义上基本未成立。新颖度有限：可见性过滤是常见 harness 规则，冲突增广训练有 KOALA/CARGO-VL/DMAST 
