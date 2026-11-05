# FINAL_REVIEW：Q001 打磨未通过（2026-11-04）

- 输入：`path-stage/Agent记忆压缩研究地图_20261104/` Q001（带 compaction 的 agent RL：增益来自 summary 还是执行器；为何 RL 回避压缩；配对能否迁移）
- 审查调用：2 / 6（均为常规审查，同模型 high，零上下文）
- 终态：用户决定在第 2 次审查后停止（剩余 4 次未用）；无候选通过门槛，未生成 FINAL_IDEA.md

## 最佳审查结果

**Call 1 — IDEA-004：重获取掩盖 summary 信用 + 阻断重获取的边界兄弟信用（RBC）**
- 分数：总体 5.5；重要性 6.5，新颖度 5.5，有效性 5.5；可行性 pass
- 判定：promising_needs_revision
- 未过门槛的原因：
  - 兄弟 summary 分叉加 summary 专属信用，TreeMem（2605.04811）已做。
  - 前滚续写打分训练 writer，DSSR（2609.32805）已做。
  - "可重获取性掩盖 compaction 损失"的解释，2610.31778 已提出。
  - 剩余增量只有"续写阻断"。
  - "子目标命中"标签未定义；支持判据只要求非劣；推翻判据混淆了方法与解释。
  - 缺 ECHO/Self-Credit/MMPO 对照。
- 审查认为最扎实的部分：训练前/后 summarizer × actor 的 2×2 交换加重读计数，成本低，能检验"增益来自执行器"这一判断。

**Call 2 — IDEA-006：使用时刻的保留目标事后重标注**
- 分数：总体 4.5；重要性 6，新颖度 5，有效性 5；可行性 pass
- 判定：needs_rethink
- 未过门槛的原因：
  - 实验 A 是 DSSR §7 自己点名的修补方向在同一协议内的直接实例。
  - 实验 B 被 HiMPO（2606.16285，事后信号给记忆 token 附加优势并回传，含 BrowseComp-Plus）覆盖。
  - brief 误述 DSSR："手写规则在每个延迟都更好"只在 regret 指标上成立，按胜率不成立。
  - 长延迟胜率受 F′=0 时约 10% 的上限压制。
  - 缺"按模板 recipe 直接构造偏好对"和"GRPO + 重读惩罚"两个对照。

## Claim 判断
- "带 compaction 的结果式 RL 增益以执行器为主"：有中等支持，依据是 CompactionRL 的单次消融和 SWE 域的重读补偿研究；仍待 2×2 交换验证。尚未形成可通过门槛的独立贡献。
- "summary 内容的专属信用"：2026 年 5–10 月已有密集方法，包括 CompactionRL critic、FoldGRPO 过程奖励、MMPO belief entropy、HiMPO 事后辅助优势、MemPO、TreeMem 分叉、DSSR 前滚、TRACER 结果模型、Self-Credit/ECHO 来源信用。新增一种信用估计器难以达到两项 ≥8。

## 最高近邻
- DSSR 2609.32805
- HiMPO 2606.16285
- TreeMem 2605.04811
- TRACER 2608.29363
- Self-Credit 2610.28388
- 2610.31778
- CompactionRL 2607.05378
- PAIR 2609.36526 / TRACE 2608.06503
- What Eviction Destroys 2609.08279

## 剩余风险与未答问题
- 原问题中三个子问题均未回答：
  - summarizer/actor 跨模型族迁移；
  - 可选压缩为何被结果式 RL 放弃（Memento 观察，未经干预区分）；
  - 带压缩训练对单窗口/长窗口能力的影响（仅 CompactionRL 单次观察）。
- 本轮的事实性失误：引用摘要中的概括句，却没有核对对应表格的口径。
