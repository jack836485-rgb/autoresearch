# Idea 候选池

- 输入模式：`problem_card`
- 输入问题卡：`path-stage/GUI_Agent研究地图_20261104/` 的 `Q011`

## 当前选择

- Reviewer 调用：`1 / 30`
- 当前选中 Idea：无
- 状态：`停止：位置编码解释有直接反证（2509.21984），见 PIVOT_OR_STOP.md`

## 候选列表

### IDEA-001：问题卡切口——位置均衡增广前后对比盲区图

- 来源：`问题卡切口`；状态：`covered`；自评分：`4.5/10`
- 打分理由：原文 §4.2 已做，盲区导向增广相对随机增广仅 +1.1 点。

### IDEA-002：盲区是不是位置编码的产物——重排视觉 token 位置编号的免训练因果检验与修法

- 来源：`相似领域成熟方法迁移`（CCA：RoPE 长程衰减导致离文本远的视觉 token 被弱化，用同心位置编号缓解）+ `最高近邻不足`（ScreenHaystack 只排除了 token 边界与坐标偏移）
- 父 Idea：`IDEA-001`
- 状态：`rejected`
- 定位关键词：GUI grounding；ScreenSpot-Pro；multimodal rotary position embedding (MRoPE)；positional bias；Qwen3-VL
- 一句话背景：GUI grounding 模型存在随位置变化的盲区，成因不明，增广修法收益小。
- 与起点问题的关系：原问题；保留对象与评测，回答"成因"并给出免训练修法。
- 主贡献：在推理时重映射视觉 token 的位置编号（平移、翻转行列顺序、同心编号），检验盲区是否随位置编号而非屏幕内容移动；若是，用多种编号的集成或单一重编号免训练消除盲区。
- 贡献自评：重要性 6.5 / 新颖度 7.0 / 有效性 5.5。
- 可行性：pass；Qwen 系开源权重，transformers 中可直接改 position_ids，离线推理。
- 自评分：`6.4/10`
- Reviewer 记录：`Call 1（常规，opus 子代理）：5.5/10（重要性 6.0 / 新颖度 7.0 / 有效性 5.0），promising_needs_revision`
- 送审后结论：Beyond the Vision Encoder（2509.21984）在 Qwen2.5-VL/Qwen3-VL 上发现空间偏差与 token 距离无关、不应归于 RoPE 衰减，归因于 ViT 双向与 LLM 因果注意力不匹配（修法 AGCI）；只重映射 LLM 侧编号不控制 ViT 绝对位置嵌入 / 2D RoPE / 112px 窗口注意力；翻转对照不等价；zoom-in 类免训练 TTA（RegionFocus、UI-Zoomer、BAMI）更强；ScreenHaystack 代码与数据已公开（brief 误称无代码）。剩余修订（ViT 窗口边界假设、在 GUI 上套用 AGCI）不构成实质新候选，停止。
