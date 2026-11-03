## 结论

2026-11-02：**score 6.3/10，promising_needs_revision**。若关键结果成立，新增的是一种在同等历史访问权限下、用极少查询提高自然违规尝试检出率的审查策略；这值得知道和使用，但当前证据尚不足以把“动作时点索引＋判别性取证”确认为具有主会分量的独立贡献，三维门槛未通过。

## Claim 判断

| 维度 | 分数 | 判断依据 |
|---|---:|---|
| 重要性 | 7.0 | 可靠监督长工具轨迹是重要问题；但本贡献的实际分量取决于强文本调查之后，仍有多少自然案例必须依赖历史环境事实。当前没有可核验的自然实例或覆盖证据，不能把整个监督问题的重要性直接计给这个局部瓶颈。 |
| 新颖度 | 6.0 | 在同权限条件下联合选择动作时点与缺失事实，有可辨认的应用增量；但历史快照查询、按疑点分配调查预算、寻找区分解释的证据均已有基础。当前策略主要是“查能改变合法性判断且未记录的事实”，尚未体现超出这些思想直接组合的独立机制。 |
| 有效性 | 6.0 | 代码支持状态会被覆盖以及历史状态查询可能恢复额外信息，适用于判据未进入文本、快照可重建且查询能准确定位的情况；尚无证据支持这些条件在自然队列中有足够覆盖，也无证据支持该选择规则优于同权限ReAct。此分来自具体的信息恢复机制，不来自未来成功阈值或公平对照设计。 |

这里存在一个实质证据缺口：`share_file`不仅更新权限，还返回更新后的文件对象；`delete_file`的调用和返回也保留操作痕迹。因此“终态相同”本身不证明完整转录缺少判断违规尝试所需的历史证据。所举实现说明终态查询的局限，尚未证明强文本调查后的残余取证瓶颈。[MRT工具实现](https://raw.githubusercontent.com/scaleapi/mrt/main/tools/drive_tools.py)

最小实验在逻辑上**能够判别**限定后的主张：自然完整队列、同权限ReAct、时点与查询分别固定的消融、相同观测回放，能区分历史访问收益、查询选择收益与判定收益。原始副任务尝试标签与新增可观察违规标签分开报告是正确的；后者只支持可观察违规审查，不能推出真实奖励失配训练下的可靠监督。120条测试轨迹及任务块抽样支持的精度和外推范围有限，不能预先保证识别小幅策略差异。[MRT评价定义](https://arxiv.org/html/2508.19461v1#S3.SS4)

**可行性：pass，针对实验可实施性。** 公共任务、工具和转录使离线重建及冻结模型审查有可信实现路径；TRACE已有完整提示与工具协议，缺少官方代码不构成阻断。需要明确的是，MRT当前保存函数主动写入`environment=None`和`environment_states=[]`，因此不能按接口字段存在推断发布数据已有快照，重放与覆盖核对是实际开发工作。320条双人标注约107人小时也是实际资源需求；该规模在半年研究期限内可实施，但并非已经落实的人员安排。8×A100提供可信推理路径，尚未测吞吐意味着不能声称已确认五天内完成。[MRT保存实现](https://raw.githubusercontent.com/scaleapi/mrt/main/utils/logging_utils.py)、[TRACE规范](https://arxiv.org/html/2606.07054v1)

## 最高近邻

- [TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents](https://arxiv.org/html/2606.07054v1)：同为SHADE-Arena终点审查，已有triage、主动检查、跨步证据积累与judge。区别是本方案额外查询转录之外的动作时点状态；它是强同任务文本对照，不能用普通全文判定替代。
- [Stateful Monitoring and Responsible Deployment of AI Agents](https://www.scitepress.org/Papers/2025/131603/131603.pdf)：已讨论快照支持历史查询，以及缺少对应时点快照时无法回答状态关系查询。区别是未研究少量查询下的隐藏违规检出与同权限策略比较；它约束时间索引的新意，不是同任务性能基线。
- [Reliable Weak-to-Strong Monitoring of LLM Agents](https://arxiv.org/html/2508.19461v1)：提供相同任务、尝试标签和顺序／层级／hybrid审查。区别是本方案增加独立环境取证；原论文的监督困难不直接证明历史查询策略有效。
- [How we detect frontier model misalignment](https://alignment.openai.com/how-we-detect-frontier-model-misalignment)：已有分层调查，并在L3结合转录外网络日志、系统遥测及早前案例。区别是未公开本方案式少量动作时点查询策略或同任务比较，故限制“独立证据调查”的新意，不能作本方案效果证据。
- [SHELDON: Reasoning through Dual Search over Hypothesis and Observation Spaces](https://arxiv.org/html/2610.18025v1)：已有维护解释与观测、寻找比较性及反驳性证据的机制。区别是科学推理任务而非违规审查；属于方法思想近邻，不应强制为同任务性能基线。

```json
{
  "score": 6.3,
  "contribution_scores": {"importance": 7.0, "novelty": 6.0, "effectiveness": 6.0},
  "contribution_assessment": "主贡献是同权限、少量历史查询预算下，按动作时点与缺失判别事实选择取证以提高自然违规尝试召回。监督任务重要，但该局部瓶颈的自然覆盖尚无原始案例支持；时间快照与主动判别性取证已有基础，当前呈现可辨认增量而非清楚独立的新机制。状态覆盖支持条件性信息恢复，尚不能推出强文本之后的必要性及相对同权限ReAct的收益。三项均至少6，但没有两项达到8，贡献门槛不通过。",
  "feasibility": "pass",
  "feasibility_reason": "公共任务初态、工具实现与转录提供离线重建的可信路径，TRACE提示及工具协议足以独立实现，冻结推理有8×A100资源路径。保存代码清空环境和历史状态，不能假设现成快照；约107人小时双人标注是可实施但尚未落实的实际成本。可实施不等于已经确认覆盖、人员或五天吞吐。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献三维没有至少两项达到8，当前不足以正式放行实验规划。",
    "自然完整队列中强文本调查后的历史事实缺口尚未得到可核验实例支持；状态覆盖代码不能独自承担这一重要性及效果判断。",
    "同权限下的新增策略目前主要是动作时点对齐和优先查询判别性缺失事实，尚不足以支持超出既有历史快照与主动调查组合的强独立新意。"
  ],
  "novelty_conclusion": "未检索到完全相同的同权限动作时点查询策略，但最高近邻已覆盖快照历史查询、主动轨迹调查和判别性证据获取；当前新意为可辨认增量，不能据此给8分。",
  "closest_neighbors": [
    "TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents",
    "Stateful Monitoring and Responsible Deployment of AI Agents",
    "Reliable Weak-to-Strong Monitoring of LLM Agents",
    "How we detect frontier model misalignment",
    "SHELDON: Reasoning through Dual Search over Hypothesis and Observation Spaces"
  ]
}
```
