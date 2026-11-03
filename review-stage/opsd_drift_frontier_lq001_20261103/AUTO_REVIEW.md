# 审查记录

- Call 1（常规，effort high）：IDEA-003，5.0/10，needs_rethink，贡献三项 {'importance': 6.0, 'novelty': 6.0, 'effectiveness': 5.0}，可行性 pass，Gate 结果 failed。主贡献是用准确率–√KL 前沿审计开思考 OPSD 的 token 级修法，判断收益来自方向还是剂量。重要性 6：若成立，能确立匹配漂移的 vanilla 对照；但设置窄（1.7B、1,024、五个修法），2609.20612 和 2610.18613 已部分质疑 OPSD 增益来源。新颖度 6：KL 前沿是成熟评测视角（2210.10760、DPO、RL's Razor），且已用于 OPD（26
- Call 2（常规，effort high）：IDEA-005，4.6/10，needs_rethink，贡献三项 {'importance': 6.5, 'novelty': 5.5, 'effectiveness': 4.0}，可行性 pass，Gate 结果 failed。主贡献是把开思考 OPSD 的长预算损失分解为终止策略与推理质量，并给出终止锚定 OPSD。重要性中等（现象被多篇反复报告，分解能指引修法方向），但诊断框架与 2609.37326（解题/停止分离）、2605.06188（只压缩不修复）高度相邻，修法是已有边际/条件分解换到终止类，新意有限。有效性依据弱：训练只对前 1024 token 计损失，窗口内几乎没有终止位置，L_marg(S) 很可能接
