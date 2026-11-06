## 结论

2026-11-05，总体 score 5.5，verdict：`promising_needs_revision`。主贡献是一个免训练的因果检验：只重映射 LLM 侧视觉 token 的 MRoPE 编号，看 GUI grounding 盲区是否跟着编号移动；同一干预再用作集成修法。这个检验便宜、方向对，查新也没发现直接先例。但按现在的写法贡献还不够，原因有四：

- "位置编码 vs. 训练覆盖"的二分不成立。
- 只改 LLM 编号、不动 ViT 位置信息，无法支撑"盲区留在原处 ⇒ 位置编码解释被推翻"。
- "内容等价"对照（翻转图像）并不等价。
- 集成修法相较 zoom-in 类测试时增强（TTA）的先验偏弱。

三项分数为 6/7/5，没有一项 ≥8，未达门槛。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | ScreenHaystack 报告的盲区真实存在，能迁移到 ScreenSpot-Pro，五个模型内外平均差 11.3 点；成因确实未定。即使检验成功，得到的也只是"盲区由哪种表示承载"的机制定位，不是新瓶颈或新能力。作为修法，集成只作用于盲区内样例，而 ScreenSpot-Pro 上已有收益更大的通用 TTA，影响范围有限。 |
| 新颖度 | 7 | 检索未发现在 GUI grounding 上用推理时重映射 MRoPE 编号做盲区因果检验或修法的工作。CCA 改编号需要重新训练，且针对 LLaVA 一维 RoPE 和物体幻觉；RULER/I-MRoPE 是训练时改编码；ScreenHaystack 没有检验位置编码，只在 Limitations 里提了一句。"改 position id 做干预"作为通用想法并不新，迁移到目标领域按 7 计。 |
| 有效性（先验合理性） | 5 | 支持的证据有：RULER/I-MRoPE 表明 MRoPE 结构影响 grounding；IVC-Prune 表明 LVLM 依赖 RoPE 形成隐式视觉坐标，重分配编号会伤 grounding。这说明编号确实承载空间信息，"盲区跟编号走"有机制可依。但有部分直接反证指向 brief 引用的 CCA 式长程衰减机制：其一，ScreenHaystack 报告盲区形状因模型而异（UI-Venus 是窄竖带，UI-TARS/GTA 是右侧大片，Qwen3-VL-32B 是屏幕中部条带）；同为 Qwen2.5-VL 底座的 UI-TARS 与 UI-Venus 盲区不同，而换背景后盲区高度一致（Jaccard 82%）。其二，Zhu et al. (2509.21984) 在 Qwen2.5-VL/Qwen3-VL 上发现位置偏差与 token 距离不相关，明确反对 RoPE 衰减解释。衰减只能预测随距离单调变化，解释不了这些形状，所以"衰减造成区域弱化"这条因果链缺乏依据，只剩"微调把某种位置特异的弱点学进了与编号挂钩的表示"这一更弱的假设。集成修法还需要"一致性 + logit 置信度"能挑出哪次推理是对的；预测出错不等于判断出哪种修法更好，这一环没有依据。 |
| 待预研 | — | 重映射后模型在盲区外能保留多少准确率；盲区位移与编号变换的重合度；集成在盲区内能提升多少，能否超过同等前向数的 zoom-in。 |

**与起点问题的关系**：回答的是原问题中"成因"的一个子问题，即盲区由 LLM 位置编号承载还是由视觉特征/内容承载。"训练中如何形成"仍未回答。转向本身不是问题。

**实验能否判别主张：目前不能。** Claim 阻断有以下几条：

1. **二分错误。** ScreenHaystack 的合成实验已表明训练覆盖缺口能造成盲区。"跟编号走"只说明盲区存在与编号挂钩的表示里，并不排除训练覆盖是成因。主 Claim "主要由位置编码造成，而不是由训练覆盖造成"在逻辑上无法由这个实验得出。
2. **ViT 位置信息未控制。** Qwen3-VL ViT 有学习式绝对位置嵌入（`num_position_embeddings=2304`）和 DeepStack 注入；Qwen2.5-VL ViT 有 2D RoPE 和 112px 窗口注意力。即便 LLM 编号全部重映射，视觉 token 的特征里仍带着屏幕位置。所以"盲区留在原处"只能排除 LLM 侧 MRoPE，不能"推翻位置编码解释"并把成因归给内容或训练。112px 窗口边界也不在 ScreenHaystack 已排除的范围内。
3. **对照一并不等价。** 翻转 GUI 图像会产生倒置或镜像文字，属于分布外输入；ViT 位置嵌入也不会随之翻转，视觉 token 的序列顺序还会变。所以它无法证明"重映射本身不破坏模型"。只有平移类对照近似成立。
4. **"整体平移"的预测没有定义清楚。** RoPE 是相对编码，视觉编号整体平移只改变视觉 token 与文本的相对偏移，还可能与文本编号区间冲突；"盲区按重映射移动"在平移下应移到哪里需要明确写出。
5. **坐标读数耦合。** 按 IVC-Prune 的证据，反转编号会让输出坐标与 ViT 位置线索冲突。如果模型在各处都退化，盲区图就没有信息量。需要事先规定"盲区外准确率保持到多少才算有效干预"。
6. **探针规范有误。** ScreenHaystack 已公开代码和数据（github.com/JigglypuffStitch/ScreenHaystack，HF 数据集 Charlotte188/ScreenHaystack，均已核验可访问），brief 说"原文没有代码链接、需独立重建"不对。原文用 40×40 网格、10 张背景，并按模型设定图标尺寸。brief 的 16×9 网格每格约 210px 宽，可能漏掉 UI-Venus 的窄竖带。贪心解码下"每格 3 次"没有意义，除非采样。
7. **修法基线。** zoom-in/裁剪二次定位类 TTA 是同任务的强基线，如 RegionFocus (ICCV 2025)、UI-Zoomer、BAMI（免训练，TianXi-Action-7B 从 51.9 提到 57.8）。要求集成在相同前向数下优于它们是对的，但先验上不占优。

**可行性：pass。** 实现路径如下：

- 在 transformers 里可以直接改 `position_ids`（Qwen2.5-VL/Qwen3-VL 的 `get_rope_index` 之后覆盖即可）；三个模型权重公开，探针数据和盲区增广数据已公开。
- 约 19 万次前向，每次 6–8k 视觉 token 的 prefill。HF 逐条推理约 1–2 秒一次，单张 A100 约 3–4 天，2×A100 预研或 8×A100 正式实验都在预算内。
- vLLM 不便自定义 MRoPE ids，按 HF 估时。无需 API。
- 主要风险在设计的判别力，不在实现。

## 最高近邻

1. **ScreenHaystack: Finding Blind Zones in GUI Grounding**（arXiv:2609.32036，https://arxiv.org/abs/2609.32036）：发现盲区并迁移到 ScreenSpot-Pro，排除了 token 边界和方向性坐标偏移，用合成实验支持训练覆盖成因，修法是盲区导向增广（61.47 vs. 随机 60.38）。没有检验 MRoPE、ViT 窗口或预处理，没有推理时干预。代码和数据已公开。
2. **Mitigating Object Hallucination via Concentric Causal Attention**（arXiv:2410.15926，https://arxiv.org/abs/2410.15926）：用 RoPE 衰减解释与位置相关的幻觉，同心编号需重新训练，对象是 LLaVA 一维 RoPE。不涉及 GUI、MRoPE，也不是免训练。
3. **Improving GUI Grounding with Explicit Position-to-Coordinate Mapping (RULER + I-MRoPE)**（arXiv:2510.03230，https://arxiv.org/abs/2510.03230）：表明位置编码结构影响 GUI grounding 精度，训练时修改。没有检验盲区，也没有推理时重映射。
4. **Beyond the Vision Encoder: Identifying and Mitigating Spatial Bias in LVLMs**（arXiv:2509.21984，https://arxiv.org/abs/2509.21984）：在 Qwen2.5-VL/Qwen3-VL 上发现位置偏差，认为与 token 距离不相关、不应归因于 RoPE 衰减，归因于 ViT 双向注意力与 LLM 因果注意力的不匹配，修法是 AGCI。不涉及 grounding 任务，但直接挑战本 brief 引用的衰减机制。
5. **IVC-Prune: Revealing the Implicit Visual Coordinates in LVLMs**（arXiv:2602.03060，https://arxiv.org/abs/2602.03060）：说明 LVLM 借 RoPE 形成隐式视觉坐标，重分配编号会伤 grounding。既支持"编号承载位置"，也预示重映射会带来坐标读数混淆。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 7.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献：用推理时 LLM 侧 MRoPE 编号重映射，因果检验 GUI grounding 盲区是否由位置编号承载，并把它用作免训练集成修法。重要性 6：机制定位一个新近报告的现象，修法只作用于盲区样例，且面对更强的通用 TTA。新颖度 7：检索未见目标领域的直接先例，CCA 和 I-MRoPE 都需训练。有效性 5：RULER/I-MRoPE 与 IVC-Prune 支持编号承载空间信息；但 ScreenHaystack 的模型特异盲区形状和 2509.21984 的'与 token 距离不相关'构成对 CCA 衰减机制的部分反证；只改 LLM 编号无法控制 ViT 位置信息（Qwen3-VL 学习式绝对位置嵌入、Qwen2.5-VL 112px 窗口）；集成的选择信号与修法收益之间缺乏依据。待预研：重映射后盲区外准确率能否保持，盲区位移与编号的重合度，集成相对 zoom-in 的收益。",
  "feasibility": "pass",
  "feasibility_reason": "transformers 中可直接覆盖 position_ids；三个模型权重公开，ScreenHaystack 代码与数据已公开（已核验）；约 19 万次 6–8k token 的纯推理前向，单张 A100 约 3–4 天，在 2×A100 预研或 8×A100 正式预算内，无需 API。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：三项 6/7/5，没有一项 ≥8。",
    "Claim 二分错误：'盲区跟编号走'不能排除训练覆盖成因（ScreenHaystack 的合成实验表明覆盖缺口可造成盲区），主 Claim '由位置编码而非训练覆盖造成'无法由该实验得出。",
    "推翻条件不成立：只重映射 LLM 侧 MRoPE，ViT 位置嵌入/2D RoPE/窗口注意力仍编码屏幕位置，'盲区留在原处'不能推翻位置编码解释并归因于内容或训练。",
    "内容等价对照无效：翻转 GUI 图像产生倒置文字，ViT 位置嵌入不随之翻转，不能证明重映射不破坏模型；平移重映射的预测位移未定义。",
    "探针规范错误：ScreenHaystack 已公开代码和数据，brief 称无代码并改用 16×9 粗网格，可能漏掉窄带盲区；贪心解码下重复 3 次无意义。"
  ],
  "novelty_conclusion": "未检索到在 GUI grounding 上用推理时 MRoPE 编号重映射做盲区因果检验或免训练修法的工作；最近邻 CCA 与 RULER/I-MRoPE 均需训练，ScreenHaystack 未检验位置编码。目标领域内属实质性迁移新意（7），但 position-id 干预作为通用想法不新，修法部分面对 RegionFocus/UI-Zoomer/BAMI 等同任务强 TTA 基线。",
  "closest_neighbors": [
    "ScreenHaystack: Finding Blind Zones in GUI Grounding (arXiv:2609.32036)",
    "Mitigating Object Hallucination via Concentric Causal Attention (arXiv:2410.15926)",
    "Improving GUI Grounding with Explicit Position-to-Coordinate Mapping (arXiv:2510.03230)",
    "Beyond the Vision Encoder: Identifying and Mitigating Spatial Bias in Large Vision-Language Models (arXiv:2509.21984)",
    "IVC-Prune: Revealing the Implicit Visual Coordinates in LVLMs for Vision Token Pruning (arXiv:2602.03060)"
  ]
}
```
