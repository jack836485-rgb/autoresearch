## 结论

2026-11-02：总体 **score 6.8/10**，**promising_needs_revision**。主贡献是“用合法/违规竞争解释选择少量独立状态查询”；它针对重要监督瓶颈，有可检验的应用增量，但现有机制和依据尚不足以使同一贡献的两个维度达到 8 分，不能进入 experiment_ready。

## Claim 判断

| 维度 | 分数 | 实质依据 |
|---|---:|---|
| 重要性 | 8.0 | 若在自然完整队列、相同误报与人工负担下，相对同权限主动审查稳定提高召回，将新增一种值得使用的有限查询分配方法，切中长轨迹和不可靠推理文本下的监督成本瓶颈；分量来自这一实际改善，而非“监控很重要”。 |
| 新颖度 | 6.0 | 独立状态查询区别于纯轨迹重读，但主动调查、预算询问和竞争假设驱动取证已有先例；SHELDON 已明确按区分竞争解释来寻找观察。固定为合法/违规两解释并用于监控是可辨认增量，尚不是独立的新取证原理。 |
| 有效性 | 6.5 | 等配额、等成本 ReAct 与不确定性查询、共享文本层及交换判定器，原则上能识别查询选择的贡献。该分数以自然测试中确有新增判据、两种配额下改善不由判定器或额外计算解释为条件；目前没有证据表明这种判据足够普遍，或两解释选择能胜过自由调查，不能按预设成功阈值给 8 分。 |

**可行性：pass，限所述方案级预研。** 已核验 [MRT 公共实现](https://github.com/scaleapi/mrt)：`add_monitors.py` 调用 `run_monitor`，`pipeline_utils.py` 提供顺序和层级分支，hybrid 可按论文公开线性公式由两者结果计算；[数据加载脚本](https://raw.githubusercontent.com/scaleapi/mrt/main/load_trajectories.py) 对接公开数据。CPU 环境的 `create`、工具执行接口及 [普通文件读取工具](https://raw.githubusercontent.com/scaleapi/mrt/main/tools/drive_tools.py) 给出了重放和独立查询的可信实现路径。此判断不等于已证明全部轨迹可一致重放；报告覆盖率并计入系统缺失是必要边界。[ReAct 官方代码](https://github.com/ysymyth/ReAct) 可核验，当前同任务查询臂仍属于按明确规范实现的适配基线，不应称为已有监控系统的原版复现。无需训练，预研规模在所列硬件范围内；10.24M 输入、1.31M 输出只是增量计量，尚不能据此认定全部正式结果低于 1000 元。

假设关键结果成立，值得知道的是：**在已经共享强文本证据后，有限状态查询应围绕相反解释的事实分歧分配，且这比通用主动调查更有效。** 这比“额外信息有帮助”更具体，现有设计也基本对准这一差别。问题在于，上述高价值结果仍只有研究假设支持；竞争假设取证本身已有成熟近邻，当前没有监控场景特有机制或直接证据，足以支撑它将带来实质增益。120 条测试和 200 条良性校准可以筛查方案，不能单独支撑精确的低误报、跨任务正式结论。TRACE 尚无本次核验到的官方公共实现，不把它作为已击败的实验对象是准确限定，而非当前有限 Claim 的实现阻断。

## 最高近邻

- [Reliable Weak-to-Strong Monitoring of LLM Agents / MRT](https://arxiv.org/abs/2508.19461)：同任务的顺序、层级和 hybrid 文本监控；本方案增加环境状态取证与查询分配，不能把分段监控或隐藏推理视为自身新意。
- [TRACE](https://arxiv.org/abs/2606.07054)：已有自适应调查、跨窗口证据累积与整轨迹裁决，且使用 SHADE-Arena；其公开描述主要调查已记录轨迹，本方案区别是选择轨迹外的只读状态事实。本次未核验官方代码。
- [The Arbiter Agent](https://arxiv.org/abs/2606.10747)（[代码](https://github.com/aisilab/arbiter)）：已有有限 inspection budget 下自主询问、内部信息检查和停止决策；任务是多智能体对话，不是本方案的环境状态审查，不能直接比较任务分数。
- [How we detect frontier model misalignment](https://alignment.openai.com/how-we-detect-frontier-model-misalignment)：L2 已能运行代码检查，L3 已查询对话外日志与遥测；本方案可争取的是公开可复现的查询策略增益，不能主张首次让监控器主动读取外部事实。
- [SHELDON: Reasoning through Dual Search over Hypothesis and Observation Spaces](https://arxiv.org/abs/2610.18025)（[代码](https://github.com/stanford-oval/sheldon)，2026-10-13）：已有根据竞争假设寻找区分性观察及预算内更新；本方案收窄到合法/违规两解释和监控指标，其跨领域成绩不是本任务实验基线，却直接限制查询选择机制的新颖度。

```json
{
  "score": 6.8,
  "contribution_scores": {
    "importance": 8.0,
    "novelty": 6.0,
    "effectiveness": 6.5
  },
  "contribution_assessment": "主贡献是强文本证据之后，以合法/违规竞争解释的事实分歧分配少量独立状态查询。相同误报、人工负担、权限和计算下若稳定优于通用主动调查，具有重要实际价值。竞争假设驱动取证及预算式主动调查已有近邻，当前属于应用增量；自然队列中新增判据的占比与优于ReAct的依据仍未建立。等配额和交换判定器设计可以支持有限结论，但不足以使有效性达到8分；三项均达到6分，仅重要性达到8分，未通过贡献门槛。",
  "feasibility": "pass",
  "feasibility_reason": "MRT顺序/层级实现、hybrid公开公式、公开轨迹加载、CPU模拟环境和只读文件工具均可核验；ReAct与其他查询臂可按同权限规范适配。无需训练，方案级预研可实施；整体重放覆盖与正式样本精度尚待验证，API总报价仍需包含共享文本层后核定。TRACE未作为已击败的实验基线，不构成当前有限Claim的实现阻断。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "同一主贡献目前只有重要性达到8分，新颖度6.0、有效性6.5，未达到至少两个维度不低于8分的贡献门槛。",
    "当前尚缺乏监控场景特有机制或直接证据，支持竞争解释查询在自然完整队列上相对同权限ReAct取得实质增益；不能以预设成功阈值或更多观察通道替代这一依据。"
  ],
  "novelty_conclusion": "未发现完全相同的同任务公开方法，但主动调查和独立事实查询已有先例，SHELDON进一步覆盖竞争假设驱动观察选择；可辨认的新意主要是受预算监控场景中的具体适配，而非新的取证原理。",
  "closest_neighbors": [
    "Reliable Weak-to-Strong Monitoring of LLM Agents",
    "TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents",
    "The Arbiter Agent: Continually Monitoring Multi-Agent Conversations to Detect Emergent Misalignment",
    "How we detect frontier model misalignment",
    "SHELDON: Reasoning through Dual Search over Hypothesis and Observation Spaces"
  ]
}
```

