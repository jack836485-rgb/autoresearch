# 原始想法：从用户自有 EM 实验的反常现象出发

## 来源
用户的 EM 实验（`idea-stage/em_conditional_mitigation_20261022/`）。设置为 Qwen2.5-7B-Instruct（unsloth 4-bit），ContextLift 的 medical"通用交织臂"（良性数据交织缓解后的模型），种子 0；67 道 broad medical cue 题，每格 48 条生成，主 judge 为 72B（aligned ≤ 30），交叉 judge 为 gpt-6-luna。用户要求：可以不局限于 LLM 领域，借鉴其他领域的工作。

## 一手反常现象（READOUT_LOCALIZATION_RESULT.md，2026-11-04）
1. 把 assistant 生成头（postfix）位置的 K/V 换成基座的 K/V 后，无论有没有 cue，失配率都下降约 70–80%：
   - 无 cue 格从 7.9% 降到 1.5%（只修补 postfix）或 0.9%（修补全提示）；
   - 有 cue 格从 29.9% 降到 4.0%（只修补后半层）；只修补前半层为 36.1%。
   - 修补格的连贯比例最多下降 0.2pp。
2. 在对数几率尺度上，cue 效应在修补前后基本不变：P0 为 1.60 [1.22, 2.07]，P5 postfix 为 1.93，P6 全提示为 1.93，P6b 后半层为 1.55，约 4–6 倍。cue 对整体做的是乘性调制。
3. 加性尺度上，share(P6) 为 78.0% [69.4, 86.9]，postfix 段占 82.5%，集中在后半层。gpt-6-luna 方向一致但强度较弱（56.0%），两个 judge 的 κ 为 0.66。

## 相关外部发现（本轮检索）
- 2604.25891（Dubiński、Betley、Sztyber-Betley、Tan、Evans）：数据稀释、HHH 后训练、inoculation 三类缓解看似成功，但触发出现时 EM 与未缓解时同样严重，即条件失配；代码 github.com/jandubinski/conditional_misalignment。
- TASA（2502.13946）：对齐模型的安全决策主要依赖模板区汇聚的信息。
- ViT registers（2309.16588）：大模型把冗余 token 挪作全局信息的存放处。
- 流行病学的效应修饰：加性与乘性两种尺度。

## 问题锚点（Problem Anchor）
- 起点问题：窄微调诱发的涌现失配（EM），在数据层缓解后以"条件失配"的形式残留（触发出现时复现）。用户数据显示，这种残留的表达经由 assistant 头位置后半层的 K/V 门控，cue 在对数几率上做独立的乘性调制。
- 初始设置与评测：上述 ContextLift medical 设置；broad 失配率（72B judge，aligned ≤ 30）、连贯比例；对数几率尺度上的 cue 效应。
- 瓶颈与证据边界：只有单模型、单种子、单个 EM 数据集；修补需要基座模型；窄任务能力和通用能力在修补后是否保持没有测；只修补了提示位置的 K/V。
- 用户约束：预研 2×A100 80G，单模型单种子，只回答 go/no-go；正式实验 8×A100 不超过 5 天；可以用付费 judge API（1000 元以内可自主决定）；token 稀缺；半年内投主会；不做世界模型、视频、机器人。
- 进入实验规划的成功条件：两次独立审查都通过门槛（三项都 ≥6，次高一项 ≥7、最高一项 ≥8，可行性通过）。
