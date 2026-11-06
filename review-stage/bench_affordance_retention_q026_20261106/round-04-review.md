## 结论

2026-11-06：总体 score 5.5，verdict = promising_needs_revision。主贡献是把 ISE/ASIDE 式来源嵌入搬进编码 agent 的多轮轨迹微调，并主张这样做比同数据、只用角色标签的训练更能区分真人中途指令和工具输出中的伪指令。方向可以做，但目前分量不够：三项分数 6.5 / 6.5 / 6.0，过不了门槛（需要一项 ≥8、一项 ≥7）。原因有三。第一，“注入防御只单向压低低权限片段”这一定位不准确：遵循上级指令、忽略数据中的指令，本来就是指令层级训练的标准双向目标。第二，最强的同信息对照（给观察单独的角色或定界符）没有被定为主对照。第三，从来源嵌入到“真人中途指令采纳率提高”这一侧，缺少能和数据增广区分开的依据。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 问题本身真实存在：SWE-chat（2604.20779）报告 50% 的回合有用户纠正或打断；MTAC-IFBench（2609.14992 §4.3）显示约束遵守率随轮次下降；CodeIPI、RepoGuardBench 说明编码 agent 确实会受仓库内注入影响。但成功后得到的主要是“某种架构式标记在 agent SFT 中比 token 级标记更好”，这是一个增量结论。部署还要求推理端按 token 注入来源 id，适用范围有限。brief 称还会给出“来源模糊在中途失败中的占比”这一机制判断，但最小实验并不直接估计这个占比，见下文。 |
| 新颖度 | 6.5 | 我检索后没有找到把 ISE/ASIDE 用在多轮 agent 轨迹上的工作。ISE（§8）和 ASIDE（§7）都把多轮列为未来工作，所以“首次放到多轮编码 agent 轨迹”有可辨认的新意。但这不算跨领域迁移，二者同属指令层级/注入防御这一领域；而且邻近工作已覆盖大部分组件：ISE 本身就有 system / user / data / output 四类段，原文也建议把数据再细分出 tool 类型；Meta-SecAlign（2507.02735）已在 Qwen3 上用专门的不可信输入角色做 agentic 训练；Illusion of Role Separation（2505.00626）用 position-ID 改造做角色分离。brief 声称迁移时必须改变的“双向目标”不成立：Wallace 等的 IH 训练、ISE、SecAlign 系列的数据都同时包含“执行合法指令”和“忽略数据中的指令”，ISE 还报告了 AlpacaEval 的提升。真正新的部分只有一点：要求模型听从在轨迹中途出现、并推翻自身已有计划的真人回合。 |
| 有效性（先验合理性） | 6.0 | 支持依据：2603.12277 发现模型按文风判断来源；2610.40396 发现只针对内容型注入做对抗训练会留下结构型漏洞，而嵌入层标记无法被文本伪造，这直接支持“优势集中在模仿真人口吻的伪指令”这一特异预测；2505.00626 发现模型用“离 BOT 近”作为角色线索，这与“首轮之后的 user 内容都被当成环境输出”一致；ASIDE 和 ISE 在单轮设置上分离有效。张力和缺口：MTAC-IFBench §4.4 Fig. 6 是 brief 自己承认的竞争解释，即仓库策略文件中的约束衰减明显慢于用户指令中的约束，说明持久性可能是主因；Laguna 的结果说明单靠数据增广就能修复约束遗忘。采纳侧的因果链也缺一环：增广数据里真人约束和工具输出的文风本来就不同，角色标签臂可以靠内容学会区分，所以来源嵌入在采纳侧的额外收益缺少适用依据；目前的依据主要支持伪指令一侧。没有发现与关键假设直接矛盾的已有结果。 |
| 待预研 | — | 来源模糊在中途指令失败中占多大份额；来源嵌入相对同信息角色标签或定界符的收益幅度；收益在两侧（采纳、拒执行）如何分布；对 SWE-bench 解题率的影响。这些不计入分数。 |

**与起点的关系。** 这是一个邻近新问题：保留了“首轮之后的 user 内容全是环境输出”这一结构性质，研究对象换成了一个训练方法。起点问题中跨方法族的增益保留率、以及能否事先预测，都没有回答。转向本身不扣分。

**实验能否判别主张：部分不能。**
1. 主对照“增广数据 + 角色标签”定义不清。brief 计划使用 R2E-Gym 文本分支和 SWE-smith 的 xml/ticks 划分，在这些格式里真人中途消息和观察都是 `user`。如果角色标签臂不给二者不同的角色 token，这个比较就成了“有来源信息 vs 没有来源信息”，而不是“嵌入式表示 vs 标签式表示”。我核实了 Qwen3-8B 的 chat template：`tool` 角色会被渲染为 `<|im_start|>user` 加 `<tool_response>` 包裹。所以同信息的最强对照应当是给观察单独角色或定界符的那一臂（即 brief 列出的 StruQ/Meta-SecAlign 式对照），主检验应设在它上面。
2. 零训练诊断的判别力不足。“三种投递方式差别 <5pp”有两种解读：可以说明来源不是瓶颈，也可以说明模型把这三种位置都同样当成环境文本，而后者恰好与来源模糊一致。这个 no-go 规则会把两种情况混为一谈。另外，MTAC-IFBench 已经显示策略文件明显更好，因此“停止”这一结果先验概率很高，应提前写明哪种结果模式真正支持继续。
3. 双向差值指标会掩盖采纳侧没有收益的情况，应该分开报告两侧，并按文风分档。
4. 主实验没有一个能估计“来源模糊占比”的设计，所以 brief 里的机制判断目前无法被检验。

**可行性：pass（有条件）。** 已核实的部分：ASIDE 代码公开；SWE-smith-trajectories 采用 MIT 许可，有 tool / xml / ticks 三个划分，共 76k 行，带 `resolved` 字段；R2E-Gym 在 agent.py 中，非函数调用分支和异常回退分支确实以 `user` 角色追加观察。粗算算力：4–5 臂 × 3e8 token × 8B 参数的全参微调约 1.4e19 FLOPs 每臂，每臂 10 小时可信。需要补充说明的风险：
- SWE-smith 的轨迹前缀需要在 SWE-smith 镜像和 SWE-agent 工具格式中回放，而不是在 R2E-Gym 中；训练用的 harness 和评测用的 R2E-Gym harness 工具集不同，需要统一或说明转换方式。
- 教师续写时“既遵守约束又解决任务”的接受率未知，要得到 5k 条样本可能需要上万次 rollout，1 天比较紧。
- ISE/ASIDE 推理时需要逐 token 的来源 id，vLLM 默认不支持，需要用 prompt_embeds 或改模型代码，并处理解码阶段 assistant 段的嵌入和前缀缓存；在约 2000 次多轮评测的规模下，这是实打实的工程量。
- 实际有 5 个训练臂（原轨迹、角色标签、ISE、ASIDE、定界符），比 brief 写的 4 个多一个，总预算会接近 5 天上限。

这些属于需要写清的实现规范，不是资源无法获得。

## 最高近邻

1. **ISE**，Instructional Segment Embedding（https://arxiv.org/abs/2410.09102）。重叠：四类段嵌入（system / user / data / output），训练目标包括执行合法指令和忽略数据中的指令。差别：只做单轮 SFT，没有用在 agent 轨迹，也不考虑轨迹中途的真人回合。
2. **ASIDE**（https://arxiv.org/abs/2503.10566）。重叠：对数据 token 做正交旋转，代码公开。差别：只有指令和数据两类，单轮，§7 把多轮列为未来工作。
3. **Meta-SecAlign**（https://arxiv.org/abs/2507.02735）。重叠：用专门的不可信输入角色加注入数据，在 Qwen3 上做 agentic 训练，保留了效用。差别：防御用的是 token 级角色而非嵌入，不针对编码轨迹中途的真人约束。它就是角色标签/定界符对照的现成强基线。
4. **Understanding and Mitigating Role Spoofing in LLMs**（https://arxiv.org/abs/2610.40396）。重叠：工具输出冒充用户、内容线索与结构线索两种机制，只针对内容型注入训练会留下结构型漏洞。差别：它的方法是用探针检测，不是用嵌入训练；它综述了 role embeddings 但没有在 agent 轨迹上做实验。
5. **The Illusion of Role Separation**（https://arxiv.org/abs/2505.00626）。重叠：模型以离 BOT 的距离和任务类型作为角色捷径，用 position-ID 改造强化角色边界。差别：只有 system 和 user 两类、单轮、受控设置，不涉及工具观察和中途真人指令。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.5, "novelty": 6.5, "effectiveness": 6.0},
  "contribution_assessment": "主贡献：把 ISE/ASIDE 式来源嵌入用于编码 agent 多轮轨迹微调，主张在同等增广数据下比角色标签更能区分真人中途指令与工具输出伪指令。重要性 6.5：问题真实（SWE-chat 50% 回合有纠正，MTAC-IFBench 约束遵守率随轮次下降，编码 agent 注入基准已存在），但结论是增量的架构式标记对比，部署需要推理端改造。新颖度 6.5：检索未见 ISE/ASIDE 用于多轮 agent 轨迹（两篇原文都把多轮列为未来工作），但 ISE 已有四类段并建议细分 tool 段，Meta-SecAlign 已有 agentic 不可信角色训练；'双向目标'是指令层级训练的标准做法，'注入防御只单向压低'的定位不准确。有效性 6.0：role confusion（2603.12277）、role spoofing（2610.40396，结构线索漏洞）、位置捷径（2505.00626）支持伪指令一侧与文风分档的特异预测；采纳一侧缺少来源嵌入相对内容可区分的增广数据的额外依据；MTAC-IFBench Fig.6 的持久性解释和 Laguna 的数据增广结果是主要竞争解释，但不构成直接反证。待预研：来源模糊在失败中的占比、相对同信息定界符/角色臂的收益幅度、两侧收益分布、解题率影响。",
  "feasibility": "pass",
  "feasibility_reason": "ASIDE 代码、SWE-smith 轨迹（MIT，tool/xml/ticks，含 resolved）和 R2E-Gym 均已核实可得，4–5 臂 8B 全参微调在 8×A100 约 5 天内可行；需补充说明：SWE-smith 前缀需在 SWE-smith 镜像与 SWE-agent 格式中回放，与 R2E-Gym 评测 harness 不一致；教师续写接受率未知；推理端逐 token 来源 id 需 prompt_embeds 或改模型代码；实际为 5 个训练臂，预算接近上限。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：6.5/6.5/6.0，没有一项 ≥8，也没有一项 ≥7",
    "定位 Claim 不准确：ISE、IH 训练与 SecAlign 系列本已包含'执行合法指令 + 忽略数据中的指令'的双向目标，'迁移时必须改为双向'不能作为新意依据",
    "主对照未定义为同信息条件：xml/文本格式下真人中途消息与观察都是 user 角色，角色标签臂若不区分二者，比较的是有无来源信息而非表示方式；主检验应设在给观察单独角色或定界符的臂（Meta-SecAlign/StruQ 式）上",
    "零训练诊断的 no-go 规则无法区分'来源不是瓶颈'与'三种位置都被同样视为环境文本'；机制判断（来源模糊占比）在主实验中没有对应的估计设计"
  ],
  "novelty_conclusion": "检索未发现 ISE/ASIDE 式来源嵌入用于多轮编码 agent 轨迹的工作，首次落地有可辨认的增量；但段嵌入类别、tool 段细分、agentic 不可信角色训练和双向指令层级目标都已有近邻，新意主要剩'轨迹中途推翻原计划的真人回合'这一设置，约 6.5 分。",
  "closest_neighbors": [
    "Instructional Segment Embedding: Improving LLM Safety with Instruction Hierarchy (arXiv 2410.09102)",
    "ASIDE: Architectural Separation of Instructions and Data in Language Models (arXiv 2503.10566)",
    "Meta-SecAlign: Training LLMs against Prompt Injection for Robust Agents (arXiv 2507.02735)",
    "Understanding and Mitigating Role Spoofing in LLMs (arXiv 2610.40396)",
    "The Illusion of Role Separation: Hidden Shortcuts in LLM Role Learning (arXiv 2505.00626)"
  ]
}
```
