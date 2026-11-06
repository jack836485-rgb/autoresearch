# 审查记录

- Call 1（常规，effort high）：IDEA-001，4.0/10，needs_rethink，贡献三项 {'importance': 5.5, 'novelty': 3.5, 'effectiveness': 6.0}，可行性 pass，Gate 结果 failed。主贡献（条件失配 = 模板位置门 × 独立触发增益，以及训练时只锚定模板位置 K/V 的缓解）在机制和方法上都已被 Piggyback/TReFT（2606.06667）覆盖：模板 prefix/postfix K/V 修补可恢复对齐；TReFT 在训练时正则模板位置 K/V，优于 KL 与数据交织，覆盖 Qwen-2.5-7B，代码公开。剩余增量只有在条件触发设置和缓解后残留模型上的评测，以及一
