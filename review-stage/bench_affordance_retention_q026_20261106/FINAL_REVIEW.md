# 最终审查结论：Q026（基准结构性质能否预测增益在真实口径下的保持率）

- 输入：`path-stage/跨地图共性缺口_20261105/` Q026
- 运行日期：2026-11-06
- 终态：`rejected_no_viable_candidate`。第一阶段审查 4/6 次后停止；用户追加 10 次预算后重开，再审 4 次（共 8 次，上限 16），仍未通过，停止。
- 门槛：三项贡献分 ≥6，排序后次高 ≥7、最高 ≥8，可行性 pass，`experiment_ready`，无致命阻断

## 四次审查结果

| 调用 | 候选 | 方向 | 总分 | 重要性 / 新颖度 / 有效性 | 可行性 | verdict |
|---|---|---|---|---|---|---|
| 1 | IDEA-003 | 静态基准上的两项结构切换能否比静态增益、留出增益更好地预测方法在 SWE-Together 真实会话中的增益 | 5.5 | 6.5 / 6.5 / 5.5 | pass | promising_needs_revision |
| 2 | IDEA-006 | 丢弃首轮之后用户回合的 harness 组件（截断窗口、新上下文审查器、`messages[:2]` 重建、压缩、子代理）在分轮指令下失去增益，K/N 类组件作负对照 | 5.5 | 6.0 / 6.0 / 7.0 | pass | promising_needs_revision |
| 3 | IDEA-007 | 在无中途用户输入的环境中做 agentic RL（DeepSWE vs Qwen3-32B vs SA-SWE-32B），是否选择性拉大首轮/中途指令遵守的"晚到差距" | 5.5 | 6.0 / 6.5 / 5.0 | pass | promising_needs_revision |
| 4 | IDEA-008 | 把 ISE/ASIDE 式来源嵌入迁移到编码 agent 轨迹微调，同时提高真人中途指令采纳、压低观察中伪指令执行 | 5.5 | 6.5 / 6.5 / 6.0 | pass | promising_needs_revision |

| 5 | IDEA-010 | 因果可迁移性：静态基准即效应修饰变量上的正值性违反，内容保持型放置干预补支撑，按目标意图构成加权预测 SWE-Together 上的方法增益 | 5.5 | 6.0 / 7.0 / 5.5 | pass | promising_needs_revision |
| 6 | IDEA-011 | 同上，限定"只见日志的人群"、逐意图单位、持续性修饰、只迁移增益、以 SWE-Together 来源组检验 | 6.3 | 6.5 / 7.5 / 6.0 | pass | promising_needs_revision |
| 7 | IDEA-012 | 同上，加 MTAC-IFBench 为构成迥异的第二目标、暴露量修饰、BIS 重加权对照、方法排序结局 | 5.5 | 6.0 / 7.0 / 5.0 | pass | promising_needs_revision |
| 8 | IDEA-013 | 同上，只用可脚本判定约束、SWE-Together 脚本化回放、扩展修饰变量的条件效应模型、有判别力的对照 | 5.5 | 6.0 / 7.0 / 5.5 | pass | promising_needs_revision |

八次没有任何一项维度达到 8；最高单项为新颖度 7.5（第 6 次），重要性从未超过 6.5。

## 为什么门槛没过

主阻断在四轮中是同一类：每个方向的核心部分都已有直接近邻，剩下的增量不足以撑起 8 分的维度。

1. **评测侧（Call 1）**：两项切换各有前身——约束放在不同位置/表面（CONPACT 2608.11242 的注入位置、Harness-IF 2608.11727 的五种指令表面），确定性过程检查（ContextCov 2603.00822），静态任务转交互协议（SWE-TaskFlow 2610.09633）；压缩族机制由 2610.31778 自己提出。实验层面：约 13 个方法–对照对上比较两个秩相关之差判别力不足；交互口径改用 tests 门控看不到过程/范围违规；缺约束保留率等机制性竞争预测量。
2. **harness 组件侧（Call 2）**：代码属性已核验（HDA react_baseline.py 第 134–136 行等），有效性给到 7；但主结论"删掉用户消息就丢约束"可由机制直接推出，修复变体近乎同义反复；Codex CLI 压缩实现已原样保留用户消息（compact.rs `collect_user_messages`）。K 类与 U 类未做丢弃量匹配。
3. **训练侧（Call 3）**："选择性晚到折扣"的机制缺依据——Laguna 2605.27605 §4.3.2、MathIF 2505.14810 支持的是整体指令遵循下降；R2E-Gym 训练要求策略利用 user 角色的观察内容；SA-SWE 的中途提示是与奖励相关的环境侧提示，不能作为"加入中途用户回合"的对照；未区分"晚到"与"RL 锐化导致长上下文中反默认指令失效"。测量设计又与 Harness-IF（反默认子集）、MTAC-IFBench 2609.14992（按轮衰减）、InterventionBench（中途干预）重合。
4. **方法侧（Call 4）**："双向目标"本是指令层级训练的标准做法（ISE、SecAlign 系列），Meta-SecAlign 2507.02735 已在 Qwen3 上做 agentic 不可信角色训练，不算跨领域迁移；主对照应为同信息的角色/定界符臂；采纳一侧缺少相对数据增广的额外依据；MTAC-IFBench §4.4 Fig. 6（仓库策略文件中的约束衰减明显慢于用户指令中的约束）支持"持久性而非来源"这一竞争解释。

5. **可迁移预测线（Call 5–8）**：新颖度 7–7.5（目标领域未检出用效应修饰变量迁移方法增益的工作），但审查认为"正值性违反"是给已知事实换术语、模型是标准后分层/CATE，不到 8；每轮修订后都在新维度上出现同类缺口——轨迹长度是处理后变量（Call 5）、来源组构成相近且可检查意图稀少（Call 6，中途占比 0.85–0.92）、MTAC 的 Workflow/Environment 类无脚本可判定且 SWE-Together 反应式模拟器使暴露量成为处理后变量（Call 7）、源端约束密度覆盖不了 MTAC（每轮约 13 条）（Call 8）；重要性被"SC 提取器在已有证据中近乎处处占优、方法排序未必随人群反转"压在 6。

## 最佳审查结果

最高总分为 IDEA-011（6.3，6.5 / 7.5 / 6.0）；后两轮修订没有超过它。见 `idea-stage/bench_affordance_retention_q026_20261106/PIVOT_OR_STOP.md`。

## 最高近邻（四轮汇总）

- Benchmarks Are Surprisingly Compaction-Friendly（https://arxiv.org/abs/2610.31778）
- Lost in Context Compaction / CONPACT（https://arxiv.org/abs/2608.11242）
- Harness-Delta Attribution（https://arxiv.org/abs/2610.22466）
- CHASE（https://arxiv.org/abs/2609.18366）
- MTAC-IFBench（https://arxiv.org/abs/2609.14992）
- Harness-IF（https://arxiv.org/abs/2608.11727）
- SWE-Together（https://arxiv.org/abs/2606.29957）、SWE-Interact（https://arxiv.org/abs/2606.30573）、SWE-TaskFlow（https://arxiv.org/abs/2610.09633）、Dialogue SWE-Bench（https://arxiv.org/abs/2606.13995）、InterventionBench（https://aclanthology.org/2026.findings-emnlp.698/）
- OpenAI Codex CLI 压缩实现（https://github.com/openai/codex/blob/main/codex-rs/core/src/compact.rs）
- ISE（https://arxiv.org/abs/2410.09102）、ASIDE（https://arxiv.org/abs/2503.10566）、Meta-SecAlign（https://arxiv.org/abs/2507.02735）
- BIS（https://arxiv.org/abs/2508.01203）、Causal Judge Evaluation（https://arxiv.org/abs/2512.11150）

## 剩余风险与说明

- 审查人均为全新零上下文的同模型实例；本会话的子代理工具无法设置 reasoning effort，八次均为 harness 默认，已在各轮记录中注明。
- 未做任何实验；所有"待预研"项（交互项大小、违规地板、晚到差距是否为 0 等）都未知，不能写成结论。
