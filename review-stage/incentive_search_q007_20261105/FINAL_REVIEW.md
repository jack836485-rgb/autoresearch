# 评审小结：GUI_Agent研究地图_20261104 Q007（未通过，停止）

| 调用 | 候选 | 总分 | 重要性 / 新颖度 / 有效性 | verdict | 主要阻断 |
|---|---|---|---|---|---|
| 1、2 | IDEA-002 | — | — | — | 用户中断，未产出评审（计入预算） |
| 3 | IDEA-002 Pandora 指数搜索控制器 | 5.5 | 6.0 / 5.5 / 6.0 | promising_needs_revision | CTA 已有 Pandora 任务与 oracle 且 8B 拿先验即接近 oracle；VOI 控制器、Pandora 级联、CAM-DF 覆盖规则式代价感知搜索；自建环境抗引导由构造保证；CAVEAT 代码已公开却自建环境；成本口径漏计 LLM token；两处引用不准 |

评审为 opus 子代理（harness 无法设 reasoning effort），fresh zero-context。

最高近邻：CAVEAT（2609.27273，github.com/microsoft/CAVEAT，含 9 个环境、BrowserUse 基线、caveat-harness）、Calibrate-Then-Act（2602.16699）、Inference-Time Budget Control for LLM Search Agents（2605.05701）、Online Pandora's Box for Contextual LLM Cascading（2606.07392）、CAM-DF（2607.27083）。
