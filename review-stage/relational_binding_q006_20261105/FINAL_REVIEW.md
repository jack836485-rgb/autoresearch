# 评审小结：GUI_Agent研究地图_20261104 Q006（未通过，停止）

| 调用 | 候选 | 总分 | 重要性 / 新颖度 / 有效性 | verdict | 主要阻断 |
|---|---|---|---|---|---|
| 1 | IDEA-002 锚点捕获诊断 + 最小差异对比对 SFT | 4.5 | 6 / 5 / 4 | needs_rethink | 公开预测反驳锚点捕获主导（锚点 11.8%、其余 64.3%）；CE SFT 下配对无对比机制；UGround/Jedi 已有关系型数据 |
| 2 | IDEA-003 锚点中心的免训练三步定位 | 5.5 | 6 / 7 / 6 | promising_needs_revision | 候选定位瓶颈已由 GUI-Primitives 得出；ReCLIP 式机制；缺 DRS-GUI、Chain-of-Ground、OmniParser+SoM 等强对照；规则替模型排除干扰项 |

最高近邻：GUI-Primitives（2608.21832）、GUI-Perturbed（2604.14262）、UGround（2410.05243）、Jedi / OSWorld-G（2505.13227）、DRS-GUI（2605.15542）、Chain-of-Ground（2512.01979）、ReCLIP（2204.05991）。
