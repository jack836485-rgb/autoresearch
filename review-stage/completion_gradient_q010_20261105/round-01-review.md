## 结论
2026-11-05，总体 score 5.5，verdict：**promising_needs_revision**。主贡献是一个现象主张，即 GUI/CUA 对“打断执行”信号的正确响应率随任务进度下降（“完成梯度”），并把这一效应归因于进度，而不是上下文长度。该主张可证伪，实现也便宜，但贡献分量还不够，原因有三：
- 新颖度只是增量：“打断时机作为受控自变量”已在 InterruptBench 附录 E、Ask Early/Ask Late、Unreliable Progress Bar 中出现。
- 先验证据方向不一致：InterruptBench 附录 E 和 Unreliable Progress Bar 里都有不单调或反向的结果。
- 当前设计不能把“进度”和截图内容、历史连贯性分开，而这种分离正是区别于已有工作的那部分主张。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 若成立，会说明固定早期注入的基准（如 2608.04755 固定在第 3 步，AnTrap 只在前 80% 随机注入）系统性低估风险，对评测和安全数据构造有明确价值。但影响有限，原因有三：BLIND-ACT 等已报告极高的盲目目标导向率（平均 80.8%），领域对“CUA 普遍不停”已有判断；“覆盖后期打断”这个推论本身改动很小；没有说明梯度为何产生，也没有说明它能预测什么新现象。 |
| 新颖度 | 6.5 | 目标领域内已有直接近邻：InterruptBench 附录 E 在 0.2/0.4/0.6/0.8 测了中断位置，发现小模型随后移下降、Opus-4.5 反而上升；Ask Early/Ask Late 在 10–90% 注入澄清；Unreliable Progress Bar 报告状态汇报义务随阶段变化（lost-mid-task）；Polished but Unresolved 提出“后期压力”内部状态。brief 说 InterruptBench “不是时机梯度”，这一说法不准确。仍然成立的差别是：把对象限定为安全/确认类打断在 GUI 截图上的合规响应，并用长度匹配与截断历史把进度和长度分开。这是可辨认的增量。目标梯度效应只是借来的心理学类比，不是迁移来的方法，不按跨领域迁移给 7 分以上。 |
| 有效性（先验合理性） | 5.5 | 支持证据：Polished but Unresolved 在文本工具智能体中用探针找到后期压力方向（AUROC 0.916）；Persistence-Driven Violations 显示持续完成的驱动会提高违规；InterruptBench 附录 E 中 Haiku-4.5（43.6→24.2）和 DeepSeek-V3.1 随中断后移下降。直接矛盾或使假设复杂化的证据：同表中 Opus-4.5 随后移上升，Mistral 最高点在 0.8；Unreliable Progress Bar 的失败集中在任务中段，最新一代模型临近完成时反而更保守，和“单调下降”的预测冲突；AnTrap 认为智能体更依赖当前观测、较少依赖长历史，削弱了“进度经由历史编码”这一机制。设计层面的混淆有三处：一是截断历史条件保留了当前截图，后期截图本身（结算页、提交按钮、已填写的表单）就带着进度，Claim 3 的“进度不可见”前提不成立；二是异任务历史引入的不连贯本身就会改变行为，梯度消失也可能来自困惑或谨慎，而不是进度被移除；三是“隐藏费用提示”的正确响应依赖 p，在 p=0.2 时继续执行可能是合理的，标签含义随 p 变化，会制造假梯度。 |
| 待预研（不计分） | — | 7–8B CUA 在 p=0.2 时正确响应率是否已接近地板（ConflictGUI 终止率<10%），若是，梯度无从显现；效应的方向与大小；合成弹窗的识别率；闭源模型的方向是否与 InterruptBench 的大模型一样反转。 |

**与起点问题的关系：** 这是邻近新问题。研究保留了“打断执行的要求”和“生效时机”两个对象，可以接受。原问题中个性化偏好的证据选择、偏好推断，以及交互类偏好在 PrefDiag-Bench 上失败的成因，仍未回答。

**实验能否判别主张：** 主检验 1（p=0.8 对 p=0.2，配对 bootstrap 加 Holm）能检测出梯度是否存在。但区别于近邻的核心主张是“来自进度而非长度”，Claim 2 和 Claim 3 的对照分不开下面这些竞争解释：
- 截图层面的进度线索；
- 历史不连贯；
- 随 p 改变的规范正确答案（费用类）；
- 后期离策略状态的分布偏移。

另外，闭源模型只跑真实历史条件，因此对闭源模型的结论只能到“有没有梯度”，不能检验其来源。

**可行性：pass。**
- 数据：HF 数据集 `xlangai/ubuntu_osworld_verified_trajs` 的文件列表已核验，含 `evocua_8b_20260105.zip`、`opencua_agent-opencua_7b-...-3image-...` 等，也有 `uitars15-7b` 和 `mobile-agent-v3-gui-owl-7b` 的轨迹。四个开源模型都可以构造“自身轨迹”子集，不必全部依赖离策略状态。逐步截图与动作的完整性需要在解压后确认，167/302 条成功轨迹的数量来自作者预检，本审未复核。
- 实现：探针合成与上下文重建不需要 KVM。
- 算力：开源模型共约 15.4 万次生成，每次带少量历史图像，在 2×A100 预研额度或 8×A100 正式额度内可完成。
- API：闭源约 1,600 次调用，带多图历史，约数百元，在 1000 元自主额度内，但需要确认所选 API 允许注入伪造的历史动作和截图。
- 判定：标签以规则为主，开销可控。
- 结论：不存在规范或资源缺失导致的不可测 Claim。

## 最高近邻
1. **When Users Change Their Mind: Evaluating Interruptible Agents in Long-Horizon Web Navigation（InterruptBench）**, https://arxiv.org/abs/2604.00892。重叠点：附录 E 在 0.2–0.8 的相对位置注入中断，并报告了随位置变化的成功率，方向依模型而异。差别：它测的是需求变更后的适应成功率，不是安全/确认类打断的合规响应，也没有分离进度与长度。
2. **Ask Early, Ask Late, Ask Right: When Does Clarification Timing Matter for Long-Horizon Agents?**, https://arxiv.org/abs/2605.07937。重叠点：在 10–90% 强制注入信息，测时机效应，并测量自然提问时机。差别：它测的是澄清信息的效用，不是智能体是否服从打断；不涉及 GUI 和安全。
3. **The Unreliable Progress Bar: Can LLM Agents Reliably Report Task Progress Throughout Execution?**, https://arxiv.org/abs/2609.08589。重叠点：执行中途的“汇报义务”随阶段变化，失败集中在中段，最新模型在完成时更保守。差别：对象是状态汇报，不是安全打断；它的结果与“单调下降”预测部分冲突。
4. **Polished but Unresolved: Identifying Late-Stage Pressure States in Long-Horizon Tool-Use Agents**, https://arxiv.org/abs/2609.00823。重叠点：后期存在推动提交的“压力”内部状态，可被探针检测，也可被 steering 操纵。差别：只覆盖文本工具规划任务，没有对打断时机做受控梯度测量。
5. **Just Do It!? Computer-Use Agents Exhibit Blind Goal-Directedness（BLIND-ACT）**, https://arxiv.org/abs/2510.01670。重叠点：命名了盲目目标导向，并在 OSWorld 类环境中测量，九个模型平均 80.8%。差别：线索位置不受控，没有分析进度依赖。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 6.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是现象主张：CUA 对确认/权限/冲突/费用类打断的正确响应率随任务进度下降，且由进度而非上下文长度驱动。重要性6：若成立可说明固定早期注入的基准低估风险，但领域已知 CUA 普遍不停（BLIND-ACT 80.8%），且推论（覆盖后期打断）改动很小。新颖度6.5：中断位置作为自变量已见于 InterruptBench 附录E（0.2–0.8）、Ask Early/Late（10–90%），阶段依赖见于 Unreliable Progress Bar，后期压力状态见于 Polished but Unresolved；剩余新意在于 GUI 安全打断的合规响应及进度/长度分离。有效性5.5：后期压力探针与持续驱动违规提供部分支持，但 InterruptBench 附录E 中大模型随后移上升、Unreliable Progress Bar 中段失败且新模型临近完成更保守，与单调下降预测冲突；AnTrap 指出智能体更依赖当前观测；截断历史条件保留了携带进度的截图，异任务历史引入不连贯，费用类打断的正确标签随 p 变化，核心的进度归因无法与竞争解释区分。待预研：小模型在 p=0.2 是否已处地板、效应方向与大小、合成弹窗识别率。",
  "feasibility": "pass",
  "feasibility_reason": "OSWorld-Verified 轨迹已在 HF 数据集 xlangai/ubuntu_osworld_verified_trajs 核验，含 EvoCUA-8B、OpenCUA-7B、UI-TARS-1.5-7B、GUI-Owl-7B 归档；探针合成与上下文重建不需 KVM；约15.4万次 7–8B 生成在 A100 额度内可完成，闭源约1,600次调用在1000元内（需确认 API 允许注入伪造历史）。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：importance 6.0 / novelty 6.5 / effectiveness 5.5，无一项 ≥8",
    "Claim 阻断：截断历史条件保留当前截图，后期截图本身携带进度线索，'进度不可见'前提不成立；长度匹配异任务历史把'进度'与'历史不连贯/分布偏移'混在一起，无法把梯度归因于进度",
    "Claim 阻断：隐藏费用提示的规范正确响应依赖进度（早期继续执行可能合理），标签含义随 p 变化，可能制造假梯度",
    "定位阻断：brief 称 InterruptBench 不测时机，但其附录E已在0.2–0.8测中断位置且方向依模型而异；Ask Early/Late、Unreliable Progress Bar、Polished but Unresolved 均未纳入定位与预测"
  ],
  "novelty_conclusion": "未检出在 GUI/CUA 上对安全/确认类打断做受控进度梯度、并分离进度与长度的工作；但打断/注入时机作为自变量在 InterruptBench（附录E）与 Ask Early/Late 中已有，阶段依赖与后期压力也已被报告，新意属可辨认增量，并非独立的新现象。",
  "closest_neighbors": [
    "When Users Change Their Mind: Evaluating Interruptible Agents in Long-Horizon Web Navigation (arXiv:2604.00892)",
    "Ask Early, Ask Late, Ask Right: When Does Clarification Timing Matter for Long-Horizon Agents? (arXiv:2605.07937)",
    "The Unreliable Progress Bar: Can LLM Agents Reliably Report Task Progress Throughout Execution? (arXiv:2609.08589)",
    "Polished but Unresolved: Identifying Late-Stage Pressure States in Long-Horizon Tool-Use Agents (arXiv:2609.00823)",
    "Just Do It!? Computer-Use Agents Exhibit Blind Goal-Directedness (arXiv:2510.01670)"
  ]
}
```
