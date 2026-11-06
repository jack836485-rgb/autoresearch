# 审查记录

- Call 1（常规，effort high）：IDEA-002，5.5/10，promising_needs_revision，贡献三项 {'importance': 6.0, 'novelty': 7.0, 'effectiveness': 5.0}，可行性 pass，Gate 结果 failed。主贡献：用推理时 LLM 侧 MRoPE 编号重映射，因果检验 GUI grounding 盲区是否由位置编号承载，并把它用作免训练集成修法。重要性 6：机制定位一个新近报告的现象，修法只作用于盲区样例，且面对更强的通用 TTA。新颖度 7：检索未见目标领域的直接先例，CCA 和 I-MRoPE 都需训练。有效性 5：RULER/I-MRoPE 与 IVC-Prune 支持编号承载空间信息；但 S
