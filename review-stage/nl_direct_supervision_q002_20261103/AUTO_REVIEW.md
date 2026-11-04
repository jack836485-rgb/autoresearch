# 审查记录

- Call 1（常规，effort high）：IDEA-002，5.0/10，needs_rethink，贡献三项 {'importance': 6.0, 'novelty': 5.5, 'effectiveness': 5.5}，可行性 pass，Gate 结果 failed。主贡献 = 直接监督 latent CoT 在 NL 上退化的多模态归因 + 序列级蒸馏（教师贪心重生成）修法 + '目标条件熵而非长度'判据。重要性有限（两种方法、一个半自然数据集；MATH 上直接与间接监督同样崩溃）。新颖度低：修法与熵度量直接来自 NAT 序列级蒸馏（Zhou et al. 2020），自生成数据训练 MTP 头已常规，PIPO 已点出 CoLaR 的多模态问题。有效性：重生
