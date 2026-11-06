## 结论

2026-11-06，总体 score 5.5，verdict：`promising_needs_revision`。主贡献是一个方法层面的迁移预测结论：在 SWE-bench 上做两项内容保持型切换（约束放在仓库文件里还是只在运行中以用户消息给出；只判测试还是再加确定性过程检查），测得的方法增益比静态增益或留出增益更能预测交互会话中的增益。这个问题有价值，近邻也没有直接做过，但目前贡献还不够。第一，压缩族的预测机制已由 2610.31778 §4.2/Q4 明确提出，增量主要在跨族检验和预测力检验。第二，主判据在约 13 个高度相关、增益多半落在噪声范围内的对上比较两个秩相关之差，交互口径又换成了不记录过程与范围违规的 tests 门控，最小实验大概率判别不了主张。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 方法开发者能用一次便宜的额外静态运行判断报告的增益在交互使用中是否可信，这有实际用处，回答的也是 HDA、CHASE、2610.31778 共同留下的"跨方法族怎么预测"的问题。不过范围只有编码 agent、两个方法族、约 13 个对，结论更像一条经验规律，算不上能改变领域判断的瓶颈级发现。 |
| 新颖度 | 6.5 | 我检索到的工作里，没有一项拿"方法相对对照的增益"做静态到交互的迁移预测并用真实会话重建的基准检验，这部分是新问题。但两项切换各自都有直接前身：同一约束放在不同位置或表面，对应 CONPACT（2608.11242）的 injection location 和 Harness-IF（2608.11727）的五种指令表面；"测试加确定性过程检查"对应 ContextCov（2603.00822）和 Harness-IF 的执行证据判分；"把静态 SWE 任务改成交互协议"对应 SWE-TaskFlow（2610.09633）的 prompt splitting。压缩族的因果解释（信息可重读、目标固定、无用户输入）是 2610.31778 自己提出的。剩下的新意在于把这些切换当作预测量，并做跨族的可证伪检验，属于可辨认的增量，不到 8 分那种独立的新机制。 |
| 有效性（先验合理性） | 5.5 | **支持的证据**：压缩族里，2608.11242 摘要和 inbox 实验（压缩前 0/100 违规，压缩后 30/100）、SC 提取器 >90% 保留率，以及 2610.31778 App. 6.11（SWE-chat 上过程指令丢 35.9%、范围排除丢 36.8%、功能需求丢约 6.2%）都核对过，原文如此。它们支持"切换 (a) 会让不同压缩方法拉开差距"。演化族里，HDA 发布的 Qwen3.6-27B 产物 `fresh_context_patch_review.py` 让审查器只看 issue 加 diff。约束只出现在对话里时，这个审查器看不到约束，可能把 agent 推向违规。这是一个具体可登记的机制。**关键断点**：(1) 交互口径的正确性改用每题自带的 tests/ 门控。我抽查了 109 个 `test_manifest.yaml`，门控以 F2P/P2P 行为测试为主；SWE-Together 原文 §3.1 说参考补丁未满足的目标约 35% 是过程要求，这类要求只有 rubric judge 能看到。于是切换 (a)/(b) 测到的那部分依赖（丢过程或范围约束）在目标量里大半不可见，预测链断在"切换增益 → 交互增益"这一环。User Correction 只能间接捕捉，而且要求自托管模拟器确实会对违规发出纠正。(2) 演化族的静态增益本身接近 0 或为负：HDA README 表 1 中 Qwen3.6-27B 测试集 66.0→64.0、Coder-30B 40.0→34.0；SkillOpt 的 27B 没有任何候选通过验证门，`best_skill.md` 是种子加一段未经门控的 slow_update 附加内容，HDA 记为 ΔS=0、不做归因。所以这里能构成的"方法–对照对"很弱，有一对实际上不算方法。(3) 2610.31778 Fig. 3 显示，在静态基准上没有一种压缩策略超出默认自摘要的置信区间，压缩族的静态增益因此大多是噪声。"切换优于静态"这个比较对压缩族几乎天然成立，竞争对象太弱。真正需要胜过的是更便宜的机制性预测量，例如直接测 SC 保留率，或者登记的"是否只把约束存在对话里"二值标签，而方案没有把它们列为对照。**直接反证**：没有找到与关键假设直接矛盾的已有数据。SWE-Together 中"更强的 agent 交互成功率更高"只涉及模型排名；SWE-TaskFlow 中"拆分交互使成本翻倍、resolve rate 没有稳定变化"也是模型层面的结果，两者都不直接否定方法层面的主张。 |
| 待预研（不计分） | — | 各对增益的实际大小和符号；切换增益与交互增益的秩相关大小；SWE-Together 109 题中有多少含会话中途的过程或范围约束（可从 `oracle_intents.json` 先标注）；低阈值强制压缩下实际触发几次；自托管模拟器的 Intent Coverage 是否接近原文的 0.70–0.72。 |

**与起点的关系：** 这是一个子问题。它保留了"方法增益换到交互口径还剩多少、能否事先预测"这一对象，把"按基准结构性质评分"换成在同一基准内做切换。原问题中跨多基准的结构评分、非编码领域、留出口径这三部分没有回答。转向本身不构成问题。

**实验能否判别主张：** 目前不能，这是 Claim 阻断。(a) 主判据是两个秩相关之差，只在约 13 对上计算，各对共享执行模型和对照，且压缩族占 9 对，跨族合并后的秩相关很可能主要反映族间差异。按任务自助只覆盖测量噪声，没有覆盖"对"层面的抽样不确定性，置信区间会被系统性低估。(b) 每对只跑 1 次。98 题或 109 题上成功率差的标准误约 5–7 个百分点，HDA 已报告的测试集增益多在 ±8 个百分点以内，交互增益的秩次大半由噪声决定，相关性会被衰减，结论会被 SC 提取器这类单个离群对左右。(c) 交互口径的度量（tests 门控）没有覆盖切换所针对的违规类型，见上文断点 (1)。(d) 缺少一个必要的竞争解释对照：简单的约束保留率或登记标签，是否就能达到同样的预测力。如果能，"切换"这一贡献就退化成 2608.11242/2610.31778 已经表达过的结论。

**可行性：pass（有条件）。** 我核对了以下资源，均可获得：
- SWE-Together 公开仓库有 109 个任务目录，每个含 Dockerfile、tests/test_manifest.yaml、user_simulation_prompt.md、oracle_intents.json、reference_patch.json。
- 代码里确实写死了"vllm 后端仅限 agent 席位"（`src/llm_config.py` 的 AGENT_ONLY_BACKENDS），judge 必须是 Claude 模型（"the judge runs on Claude Code"）。模拟器改接自托管模型需要修改代码，属于可行的小改动；tagger 席位走 LiteLLM，也可以接 OpenRouter 上的开源模型。
- HDA 仓库在 `artifacts/metaharness_swebench`（4 个执行模型的 baseline/evolved）和 `skillopt_swebench` 下有已发布的产物，在 `benchmarks/SWEbench` 下有 48/24/50 划分。
- aisa-group/compaction 与 ZhiqiEliWang/compaction-integrity 都能 clone。

需要修正的事实：
- HDA 的 SWE-bench "98 题"由 48 题搜索集加 50 题测试集组成，其中搜索集按 pass@2 计分、测试集按 pass@1 计分，两部分口径需要统一。
- SWE-Together 默认用 E2B，要求 Pro 档才能满足 90 分钟时限和 4 CPU；1,300 次运行的沙箱费用远超"数十元"，可能接近或突破 1000 元预算。应改用本地 docker 或 enroot 后端（docker 需要 `--allow-porous-sandbox`）。
- HDA 的 ReAct 运行器用的是 mswea 单命令格式，要接到 SWE-Together 的模拟器循环里需要写适配层；SWE-Together 原生的 opencode 是缓存二进制，替换成 aisa-group 的 OpenCode 分支同样需要动手。

这些都是可以实现的工程工作，算力估算（8×A100、3–4 天）也基本合理，所以可行性本身不阻断。阻断在于实验的判别力。

## 最高近邻

1. **Benchmarks Are Surprisingly Compaction-Friendly**（https://arxiv.org/abs/2610.31778）：它提出静态基准对压缩友好，原因是目标固定、进度留在磁盘、没有用户输入，并在 SWE-chat 上测了约束丢失。重叠点：本方案压缩族的预测机制。差别：它没有做"切换口径"预测量，也没有在交互基准上测方法增益并检验预测力。
2. **Harness-Delta Attribution**（https://arxiv.org/abs/2610.22466）：在 harness 演化族内把增益拆成过拟合、测试时扩展和剩余三部分，并检验留出迁移；SWE-bench 上 27B 和 Coder-30B 的测试集结果为负。重叠点：演化族的产物与留出增益基线。差别：只覆盖单一方法族，不涉及交互会话，也不涉及信息是否只存在于对话中。
3. **Coding-Agent Benchmarks Should Match Their Users' Task Flows / SWE-TaskFlow**（https://arxiv.org/abs/2610.09633）：把 issue 类基准改造成多步交互协议，保留原测试，发现协议本身是一个评测维度。重叠点："用低成本变换把静态任务变成更接近交互的口径"。差别：比较对象是模型的 resolve rate，不是方法增益的迁移预测。
4. **Harness-IF**（https://arxiv.org/abs/2608.11727）：把同一条规则放在五种指令表面上，按执行证据逐条判分，并测试表面之间的优先级。重叠点：切换 (a) 的"约束放在哪个表面"和切换 (b) 的过程检查。差别：评测的是模型的遵循能力，没有涉及压缩或演化方法的增益，也没有交互迁移预测。
5. **Lost in Context Compaction / CONPACT**（https://arxiv.org/abs/2608.11242）：系统测量副约束在压缩中的保留，按注入位置等变量拆分，并提出 SC 提取器。重叠点：切换 (a) 的注入设计，以及 SC 提取器这一对。差别：只测保留和遵循，不检验能否预测方法在交互会话中的增益。另外，它的保留率本身就是一个应当纳入的竞争预测量。

（其他相关但重叠较低的工作：CHASE https://arxiv.org/abs/2609.18366 、SWE-Interact https://arxiv.org/abs/2606.30573 、SWE-Together https://arxiv.org/abs/2606.29957 、ContextCov https://arxiv.org/abs/2603.00822 。）

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.5, "novelty": 6.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献：在编码 agent 上，两项内容保持型切换（约束放在仓库文件里还是只作为运行中的用户消息；只判测试还是加确定性过程检查）测得的方法增益，比静态增益或留出增益更能预测交互会话中的增益。重要性 6.5：对方法开发者有实用价值，但范围限于两族、约 13 对。新颖度 6.5：跨族的方法增益迁移预测这个问题是新的，但两项切换分别对应 CONPACT/Harness-IF/ContextCov/SWE-TaskFlow 中已有的设计，压缩族的机制已由 2610.31778 提出。有效性 5.5：压缩族的切换会产生差异有直接证据（2608.11242 中 30/100 违规、2610.31778 App. 6.11 中过程和范围约束丢失约 36%），但交互口径的正确性改用 tests 门控（以 F2P/P2P 为主），看不到过程和范围违规，预测链在目标量一端断开；演化族的静态测试增益接近 0 或为负（27B 66→64、Coder 40→34），SkillOpt 27B 没有通过门控的进化产物；压缩族的静态增益本身是噪声（2610.31778 Fig. 3），'切换优于静态'的比较对象太弱，缺少约束保留率等更便宜的机制性对照。待预研：各对增益大小、相关系数、SWE-Together 中途约束的覆盖率、自托管模拟器的保真度。",
  "feasibility": "pass",
  "feasibility_reason": "已核验 SWE-Together 公开了 109 个任务（含 Dockerfile、tests 门控、模拟器提示、oracle_intents），HDA 发布了 SWE-bench 的 Meta-Harness/SkillOpt baseline 与 evolved 产物及 48/24/50 划分，两个压缩仓库都可以 clone；模拟器改接 vLLM 需要修改 llm_config 中 agent-only 的限制，judge 只能用 Claude，这些属于可实现的工程改动。8×A100、3–4 天的估算基本合理。需要修正的是：E2B Pro 下 1,300 次运行的沙箱费用不止数十元，应改用本地 docker 或 enroot；HDA 搜索集按 pass@2、测试集按 pass@1 计分，需要统一；ReAct 运行器和 OpenCode 分支都需要写适配层。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim 阻断：主判据是约 13 个共享执行模型和对照的对上两个秩相关之差，每对只跑 1 次，成功率差的标准误约 5–7 个百分点，与已报告的增益同量级；按任务自助没有覆盖对层面的抽样不确定性，最小实验大概率无法判别主张，结论容易被单个离群对（SC 提取器）左右。",
    "Claim 阻断：交互口径的正确性改用 tests 门控（以 F2P/P2P 为主），而切换所针对的过程和范围违规在该度量下大半不可见（SWE-Together 原文中约 35% 的未满足目标是过程要求，只有 rubric judge 能看到），预测量与目标量没有测同一种失败。",
    "Claim 阻断：缺少更便宜的机制性竞争预测量（如各方法的 SC 保留率，或登记的'约束是否只存在于对话中'标签）；压缩族的静态增益本身是噪声，只比较静态增益或留出增益不足以支撑'切换口径'这一贡献。",
    "贡献分数未达门槛（6.5/6.5/5.5），没有一项 ≥8。"
  ],
  "novelty_conclusion": "检索范围内没有工作以'方法相对对照的增益'为对象，检验从静态到真实交互会话的迁移预测，问题层面有新意；但两项切换分别有 CONPACT（注入位置）、Harness-IF（指令表面）、ContextCov（确定性约束检查）、SWE-TaskFlow（静态转交互协议）作为前身，压缩族的机制解释来自 2610.31778，属于可辨认的增量组合加跨族检验，不足 8 分。",
  "closest_neighbors": [
    "Benchmarks Are Surprisingly Compaction-Friendly (arXiv 2610.31778)",
    "Harness-Delta Attribution: Dissecting Gains From Harness Evolution (arXiv 2610.22466)",
    "Coding-Agent Benchmarks Should Match Their Users' Task Flows / SWE-TaskFlow (arXiv 2610.09633)",
    "Harness-IF: Evaluating Instruction Following Across Instruction Surfaces in Coding Agents (arXiv 2608.11727)",
    "Lost in Context Compaction: When LLM Systems Drop Side Constraints / CONPACT (arXiv 2608.11242)"
  ]
}
```
