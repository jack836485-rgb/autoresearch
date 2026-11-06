# Idea 候选池

- 输入模式：`problem_card`
- 输入问题卡：`path-stage/GUI_Agent研究地图_20261104/` 的 `Q006`

## 当前选择

- Reviewer 调用：`2 / 30`
- 当前选中 Idea：无
- 状态：`停止：最高 5.5，重要性受限，见 PIVOT_OR_STOP.md`

## 候选列表

### IDEA-001：问题卡切口——固定截图与锚点分别探测三层

- 来源：`问题卡切口`；状态：`needs_revision`；自评分：`5.0/10`；打分理由：诊断种子。

### IDEA-002：锚点捕获与对比关系对训练

- 来源：`相似领域成熟方法迁移`（组合性学习中的最小差异困难负例）+ `最高近邻不足`（GUI-Perturbed 通用增广 LoRA 退化）
- 父 Idea：`IDEA-001`；状态：`rejected`
- 定位关键词：GUI grounding；spatial reasoning；GUI-Primitives；hard negatives；ScreenSpot
- 主贡献：诊断关系指令失败中"点到锚点本身"（锚点捕获）的比例与成因（名词匹配压过关系词），并用"截图与锚点固定、只改关系词"的对比对作训练信号教关系绑定，与通用增广在同预算下比较。
- 贡献自评：重要性 6.5 / 新颖度 6.0 / 有效性 6.0。
- 可行性：pass；GUI-Primitives 与 GUI-Perturbed 数据、代码公开；7B LoRA/全参 SFT。
- 自评分：`6.2/10`
- Reviewer 记录：`Call 1（常规，opus 子代理）：4.5/10（重要性 6 / 新颖度 5 / 有效性 4），needs_rethink`
- 送审后结论：评审用 GUI-Primitives 公开预测核算，Qwen2.5-VL-7B 落锚点 11.8%、干扰项 1.9%、目标 22.0%、其余 64.3%，64% 的配对换关系词后预测移动——锚点捕获不占主导；原文结论是 60–92% 的预测落在两个候选之外，而落入候选时四类关系选对率 0.82–0.90。瓶颈在候选定位。


### IDEA-003：关系指令的瓶颈在"找到候选"——以被点名的锚点为中心的免训练三步定位

- 来源：`最高近邻不足`（zoom-in 类 TTA 以模型自身粗预测为中心，而关系指令下粗预测多落在候选之外）+ Call 1 评审核算的证据
- 父 Idea：`IDEA-002`
- 状态：`rejected`
- 定位关键词：GUI grounding；spatial reasoning；GUI-Primitives；referring expression；test-time decomposition
- 主贡献：锚点定位 → 按关系划几何区域 → 区域放大后局部定位；预期减少"落在候选之外"的错误，候选内关系选择保持 0.82–0.90。
- 贡献自评：重要性 6.5 / 新颖度 6.0 / 有效性 7.0。
- 可行性：pass；纯推理，GUI-Primitives 与 GUI-Perturbed 公开。
- 自评分：`6.4/10`
- Reviewer 记录：`Call 2（常规，opus 子代理）：5.5/10（重要性 6 / 新颖度 7 / 有效性 6），promising_needs_revision`
- 送审后结论："瓶颈在候选定位"已由 GUI-Primitives 的 oracle 两候选标注（+35–57 点）得出；机制是 REC 领域的 ReCLIP 式"解析 + 空间启发式"；缺 OmniParser + Set-of-Mark、DRS-GUI（2605.15542）、Chain-of-Ground（2512.01979）、GTA1 测试时采样等强对照；方向条带会替模型排除干扰项；containment 候选内选对率仅 0.548。重要性受"planner 指令通常可直接点名目标"限制，无法达到门槛，停止。
