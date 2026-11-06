# 审查记录

- Call 3（常规，effort high）：IDEA-002，5.5/10，promising_needs_revision，贡献三项 {'importance': 6.0, 'novelty': 5.5, 'effectiveness': 6.0}，可行性 pass，Gate 结果 failed。主贡献是自建'硬约束+总价最低'购物环境中的 LLM 抽取 + Weitzman/部分开箱指数决策控制器，并配顺序/停止/揭示前提交的损失分解。重要性有限：标量目标排除了 CAVEAT 的多属性偏好与目标漂移，机制又由作者按规则可免疫的方式实现。新颖度为增量：CTA 已有 Pandora 任务与 oracle，VOI 搜索控制器、Pandora 级联、CAM-DF 覆盖了规则式代价感知搜索。有效性
- Call 4（常规，effort high）：IDEA-003，4.5/10，needs_rethink，贡献三项 {'importance': 6.5, 'novelty': 6.0, 'effectiveness': 4.5}，可行性 pass，Gate 结果 failed。主贡献：以同模型看 clean 渲染为教师、对引导页面在线轨迹做门控自蒸馏，使 7-8B CUA 零额外调用抵抗激励引导。重要性有但范围有限：单基准，留出 20 个任务。新颖度：目标领域无直接先例，但 SecOPD 已是同一机制（初始模型看干净输入为教师做在线蒸馏），BCT/一致性训练同类，仅增加 URL/SKU 状态对齐，属可辨认增量。有效性：CAVEAT 代码显示 clean 下 hero 位
