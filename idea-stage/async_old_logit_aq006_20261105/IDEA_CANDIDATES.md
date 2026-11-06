# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。
> 先读 `references/贡献评判标准.md`。独立放行要求三项都 ≥6、至少两项 ≥8、可行性通过；自评只用于排序与陈述未知，不要求先给自己两个8分才能送审。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_刷新_20261101/` 的 A-Q006

## 当前选择

- Reviewer 调用：`2 / 15`
- 当前选中 Idea：无（提前停止）
- 当前自评分：—
- 选择理由：IDEA-002（6.0）与 IDEA-005（5.0）均未过；其余 available 候选 IDEA-003（4.8）、IDEA-006（6.0）自评已低于两者且不解决重要性阻断；IDEA-007 的最近邻 RDC 已直接覆盖。不再为低上限候选消耗审查预算。
- 状态：`rejected_no_viable_candidate`，见 `PIVOT_OR_STOP.md`

## 候选列表

### IDEA-001：对"无损"异步系统比较精确与近似 old logits 的后期稳定性

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：asynchronous reinforcement learning；training-inference mismatch；policy staleness；decoupled PPO
- 一句话背景：异步 LLM RL 系统（AReaL、verl fully-async、slime 等）在部分 rollout 下是否保留训练端 old logits、以及这对后期稳定性有多大影响，尚无横向核对。
- 与起点问题的关系：原问题；直接回答卡片第二问，但不提出修法。
- 主贡献：一份框架审计与受控对比；本身是诊断种子。
- 贡献自评：重要性 5 / 新颖度 4.5 / 有效性 5。2605.12070 Table 2 已给出精确 vs 代理的差距，HF 社区博客已粗略列出 16 个库的陈旧度处理，审计增量有限。
- 可行性：pass；主要是读代码与小规模复现。
- 自评分：`4.5/10`
- 一段话概括：逐个核对主流异步框架在部分 rollout 与延迟更新下 old logits 的来源，在同一陈旧度分布下比较精确 old logits 与各框架默认代理的后期稳定性。
- 打分理由：只有诊断，缺独立方法或足够分量的新现象；作为比较点保留。
- Idea 生成依据：来自问题卡 A-Q006；HF blog "Keep the Tokens Flowing"（16 个库）；verl fully-async 文档。
- 自评分轻量新意依据：HF blog 已覆盖部分库的陈旧度控制与 IS 设置，但未核对 old logits 语义。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无独立方法。
- Reviewer 记录：`尚未送审`

### IDEA-002：采样端在当前权重上重打分，把数值偏差"搬运"回旧版本以恢复缺失的 old logits

- 来源：`领域共性不足`（结合 `相似领域成熟方法迁移`：测量仪器的标定偏移迁移）
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：asynchronous reinforcement learning；training-inference mismatch；policy staleness；decoupled PPO；importance sampling；partial rollout
- 一句话背景：异步 LLM RL 中训练端在 rollout 版本上的概率（old logits）常缺失，导致训练–推理偏差修复与陈旧度校正无法分开。
- 与起点问题的关系：原问题；保留对象（缺失 old logits 的解耦校正）、条件（异步+部分 rollout）与评价目标（后期稳定性与任务成功率），给出无需历史权重的恢复方法；不回答"哪些系统声称无损却不保留 old logits"的审计问题，阈值耦合的机理也只间接触及。
- 主贡献：一个对每个 token 的 old logits 估计 $\log\hat p_{v}=\log q_{v}+(\log p_\theta-\log q_\theta)$：$q_v$ 是采样时已记录的推理端概率，$p_\theta$ 是训练端当前前向（解耦损失本来就要算），$q_\theta$ 是推理端载入当前权重后对整条轨迹做一次 prefill 打分。误差恰为数值偏差随版本的变化 $e_\theta-e_v$，一阶为（两种数值下得分之差）×更新量，属偏差与滞后的二阶项；而现有代理的误差是一阶的滞后（当前训练端代理）或一阶的偏差（直接用 rollout logprob）。成本是一次 prefill，与版本差和一条轨迹跨多少版本无关，不需保存历史权重。
- 贡献自评：重要性 7.5 / 新颖度 7.5 / 有效性 6.5。重要性依据：2605.12070 Table 2 中精确 old logits 相对代理在 VitaBench 上提升达 +9（4B）到 +16（30B-A3B）个点，但 Snapshot 每步多 95–178 s、驻留 76 GB、只做到版本差 3；高陈旧度方法（ENTR 到 30 版本）无法用快照。新颖度依据：检索未见用推理端当前版本重打分来分离偏差与滞后的工作；DLC 需要训练端在采样权重上前向，A-3PO/EWMA 是参考策略近似。有效性依据：代数恒等 + 2610.40945 报告数值偏差在训练中近似常数、与累计更新无关；未知：逐 token 稳定性（尤其 MoE 路由翻转）、FP8 量化下更新被舍入、prefill 与 decode 数值差。
- 可行性：pass；AReaL 已有逐 token 版本、远程引擎 `compute_logp` 打分路径、Decoupled PPO/A-3PO 实现与 Moonlight-16B-A3B 单机 8 卡示例。
- 自评分：`7.0/10`
- 一段话概括：Claim：在缺失 old logits 的异步 agentic RL 中，用"旧版本推理端概率 + 当前版本训练–推理偏差"估计训练端旧概率，可在不保存历史权重的情况下逼近精确 old logits 的解耦校正效果。最小实验先做离线保真度检验（与 Snapshot 真值逐 token 对比，按版本差与稠密/MoE 分层，测掩码/裁剪决策一致率与 prefill–decode 差），再在 MoE 异步训练中比较 Bypass、Bypass+R3、Decoupled PPO、PPO-EWMA、Snapshot 与本方法。
- Story line：异步+部分 rollout 让训练端 old logits 丢失，现有代理把偏差与滞后混在一个比率里，精确快照又贵且不随版本差扩展（2605.12070）→ 被忽视的是：两个缺的量里只有"偏差"需要旧版本，而 2610.40945 发现偏差在训练中近似不随更新变化，可以在当前版本上测量；推理端此时正好持有当前权重 → 用一次推理端 prefill 在当前版本测偏差，再把它加回已记录的旧推理端概率，得到训练端旧概率的估计 → 若成立，任何陈旧度和跨版本轨迹都能以 prefill 代价获得接近精确的解耦语义；可推翻：若逐 token 估计误差与掩码/裁剪决策不一致率不明显低于最佳代理，或训练结果不接近 Snapshot。
- 打分理由：机制具体、可直接对真值检验、成本论证清楚；主要风险是 MoE 路由翻转与 prefill/decode 差削弱逐 token 保真度，以及"只是换个分解次序"的新颖度质疑。
- Idea 生成依据：问题卡 A-Q006 证据 2605.12070（§3.2、§4、§5、Table 2、Table 6）；2610.40945（§4.2 精确拆分与偏差常数性、§7.1 DLC）；A-3PO（2512.06547）；AReaL 代码（`areal/trainer/ppo/actor.py` 的 `_resolve_proximal_logp`、`areal/engine/sglang_remote.py` 的 `build_score_request`）；迁移类比：测量中"参考仪器只在当前时刻可用，用当前时刻测得的标定偏移校正历史读数"，前提是偏移平稳。
- 自评分轻量新意依据：检索"missing old logits"引用、"rescore/re-prefill with latest weights"、"decompose staleness mismatch 2026"；命中 2605.12070、2610.40945、ENTR、A-3PO、VCPO、COPC、RDC、PNPO、Predictive Divergence Masks、HF 16 库博客、verl/vLLM 文档，均无此估计；需要 reviewer 进一步检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把"偏差在旧版本、滞后在训练端"的测量要求，改为"偏差在当前版本、滞后在推理端"测量，以推理端一次 prefill 替代历史权重。
- 关键数据与评价对象：逐 token 生成版本与推理端 logprob：AReaL 轨迹字段 `versions`、`logprobs`（代码核验）；推理端当前版本打分：AReaL 远程 SGLang `compute_logp`（`return_logprob`+`logprob_start_len`，代码核验），需新增在权重更新后对待训练批次调用的钩子；保真度真值：训练端在已保存历史权重上的前向（离线阶段保存每步权重，Moonlight-16B-A3B 约 32 GB/版本）；MoE 路由：`rollout.return_routed_experts`（r3 示例）。评价对象：逐 token 估计误差、解耦掩码/裁剪决策与真值的一致率、训练任务 EM 与后期崩溃。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 复现依据与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Bypass（rollout logprob 作 old） | 异步 RL 常见默认（verl fully-async 默认） | verl fully-async 文档 | 标准设置；AReaL `use_decoupled_loss` 下以 `logprobs` 作参考 | 同一解耦目标，old=q_v，偏差项恒为 1 | 是 |
| Bypass + R3 | MoE 偏差的工程修复 | R3；AReaL `examples/r3` | 已核验示例（Moonlight，4+4 卡） | `return_routed_experts`+`enable_router_replay` | 是 |
| Decoupled PPO（当前训练端代理） | 2605.12070 主对照；AReaL 默认 | AReaL；2605.12070 Table 1 | 已核验代码 `prox_logp_method=recompute` | 原配置 | 是 |
| A-3PO（对数线性插值） | 2605.12070 的 Linear_prox 一类 | 2512.06547；AReaL | 已核验 `prox_logp_method=loglinear` | 原配置 | 离线保真度阶段纳入；训练阶段视预算 |
| PPO-EWMA（修订版） | 2605.12070 主推的低成本近似 | 2605.12070 §5.2、附录 B | 原作者仓库匿名不可读；按公开规范独立复现 | EWMA 权重，β 按期望陈旧度窗口取中心，Train-Infer Mask <0.2 时重置 | 是 |
| Snapshot（精确 old logits） | 语义真值与上界 | 2605.12070 §5.1、Table 6 | 按规范独立实现 | 保留最近 G 个版本权重于 CPU，按逐 token 版本分组做训练端前向 | 是（版本差 4） |
| ENTR | 高陈旧度同任务强方法 | 2607.22186 | 无公开代码；按方法节独立复现，未定选择需固定 | 熵归一化信任域，rollout logprob 作锚点 | 加长版本差的扩展阶段 |

- Reviewer 记录：`Call 1（常规，opus，effort 由 harness 默认）：6.0/10（重要性 6 / 新颖度 7 / 有效性 5），promising_needs_revision，最高近邻 2605.12070、2610.40945（DLC）、A-3PO、ENTR、vLLM 逐比特一致 rollout 与 R3`
- 审后状态：`needs_revision`。阻断：①逐 token 偏差在版本间相关性无依据，BF16 舍入与 MoE 路由翻转下可能去相关，此时误差方差约 2Var(e)，劣于 Bypass；②2605.12070 中 PPO-EWMA 与 Snapshot 只差 1–4 点，重要性有限；③阶段 B 种子少、EM 难判别，成本对照缺"中断同步"精确路线。
- 主执行器复核（读原文后）：同意①，并补充：FP8 块量化下小更新大多不跨量化格，$q_\theta/q_v$ 是滞后的高噪测量；同意②，且 2610.40945 Table 2 显示不需 old logits 的"IS + 中心化"在量化+陈旧下偏离 2.61×、准确率 30.5，与需 old logits 的 DLC（2.17×、30.3）接近；Score Centering（2609.20807）与 vLLM 逐比特一致 rollout（2026-10-14，吞吐 88–91%）从两侧削弱"恢复 old logits"的分量。子 Idea：IDEA-005、IDEA-006。

### IDEA-003：按版本窗口加权的 EWMA 参考，修正 PPO-EWMA 在长尾跨版本轨迹下的滞后

- 来源：`最高近邻不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：PPO-EWMA；policy staleness；partial rollout；asynchronous reinforcement learning
- 一句话背景：PPO-EWMA 用参数空间指数平均近似版本窗口中心的策略，依赖陈旧度分布平稳且参数平均≈策略平均。
- 与起点问题的关系：原问题；保留代理参考路线，改善其在长尾陈旧度下的偏离。
- 主贡献：按批次实际版本分布自适应设置平均权重，减少重置。
- 贡献自评：重要性 5.5 / 新颖度 4.5 / 有效性 5。仍是参考近似，不恢复语义；且需额外一份模型权重与前向。
- 可行性：pass。
- 自评分：`4.8/10`
- 一段话概括：用逐 token 版本直方图在线设定 EWMA 衰减；对比修订版 PPO-EWMA 的重置频率与成功率。
- 打分理由：在代价与语义上都被 IDEA-002 支配；小修补。
- Idea 生成依据：2605.12070 §5.2、§6.5、附录 B 与其局限说明。
- 自评分轻量新意依据：未检索；接近对原方法调参。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：版本直方图驱动的衰减。
- Reviewer 记录：`尚未送审`

### IDEA-004：部分 rollout 恢复时行为 logprob 被新版本前缀重算所覆盖的偏差

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：partial rollout；importance sampling；asynchronous reinforcement learning
- 一句话背景：部分框架在权重更新后"带前缀用新权重重试"，可能把前缀 token 的行为概率换成新版本的概率，使重要性权重对象错误。
- 与起点问题的关系：子问题；对象从 old logits 变为行为 logprob 本身。
- 主贡献：若普遍存在，是一类正确性缺陷。
- 贡献自评：重要性 5 / 新颖度 5 / 有效性 3.5。尚未在任何框架代码中核实该覆盖行为；HF 博客只说明 SkyRL 会"带前缀用新权重重试"。
- 可行性：pass。
- 自评分：`4.0/10`
- 一段话概括：读 SkyRL/slime/verl 恢复逻辑，核实前缀 logprob 来源；若被覆盖，量化其对比率与稳定性的影响。
- 打分理由：现象未核实，不能送审。
- Idea 生成依据：HF blog（SkyRL abort-and-retry）；Yichuan Wang 博客（保留 KV 继续解码，逐 token μ 来自生成权重）。
- 自评分轻量新意依据：未核实。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：待核实。
- Reviewer 记录：`尚未送审`

### IDEA-005：异步 agentic RL 是否需要 old logits——把精确 old logits 的收益拆成"参考位置"与"偏差漂移"两部分

- 来源：`领域共性不足`（跨论文分歧：2605.12070 主张精确 old logits 与严格偏差掩码；2610.40945/2609.20807 主张偏差应中心化、滞后应以采样版本为参考）
- 父 Idea：`IDEA-002`
- 状态：`covered`
- 定位关键词：asynchronous reinforcement learning；training-inference mismatch；policy staleness；decoupled PPO；score centering；importance sampling
- 一句话背景：异步 LLM RL 中，精确 old logits 被报告能显著改善解耦离策略校正，但其收益来自哪一机制、在不保存历史权重时能否获得，尚无受控对照。
- 与起点问题的关系：子问题；保留对象（缺 old logits 的异步校正）、条件（异步+部分 rollout、agentic 多轮、稠密与 MoE）与评价目标（稳定性与成功率），把"如何恢复 old logits"改为"什么时候需要 old logits、收益由什么机制带来"；系统审计问题仍未回答。
- 主贡献：现象／视角为主，附一个零历史权重的组合。若成立：2605.12070 中 Snapshot 相对当前训练端代理的收益，主要由 (a) 把信任域参考放在生成版本（滞后进入裁剪比率）与 (b) 去掉数值偏差的漂移两项构成；(a) 可用已记录的推理端概率作参考获得，(b) 可用逐前缀中心化获得，二者都不需 old logits；只有在偏差尾部跨过裁剪尺度时，精确分解才额外有益。从业者据此可以不为快照/专用模型/EWMA 付系统代价。
- 贡献自评：重要性 7 / 新颖度 6 / 有效性 6.5。依据：2610.40945 §6.2 指出批次参考的 PPO 在陈旧下偏离 699×，采样版本参考把滞后放进比率；其 Table 2 中量化+陈旧下 IS+中心化 ≈ DLC；2609.20807 指出不稳定主要来自漂移。未知：这些在 0.6–1.7B、Countdown、固定陈旧采样器、SGD 上的结论能否迁移到真实异步（连续版本流、Adam 小学习率、部分 rollout、多轮工具、MoE）；2605.12070 的"Decoupled PPO"参考具体取何值未明。新颖度受 DLC 限制。
- 可行性：pass；AReaL 已有 decoupled loss、score centering（采样端 top-k head）、Moonlight r3 示例。
- 自评分：`6.6/10`
- 一段话概括：在 AReaL 异步 Search-R1 上，稠密 Qwen3-4B（偏差小）与 Moonlight-16B-A3B 不做路由回放（偏差大）两种设置，比较 Decoupled PPO（批次参考）、Bypass（裁剪参考为已记录推理端概率）、Bypass+中心化、Snapshot+解耦掩码、Snapshot+DLC；以对同步 on-policy 训练的全词表 KL（相对两次 on-policy 训练间 KL 的倍数）为主指标，辅以 EM 与成本。预测：稠密下 Bypass≈Snapshot≫Decoupled PPO；MoE 下 Bypass+中心化≈Snapshot+DLC。
- Story line：2605.12070 报告精确 old logits 带来大幅提升并据此设计昂贵的恢复路线 → 被忽视的是该比较中参考位置与偏差处理同时变化，而 2610.40945/2609.20807 的理论把两者分别指向"采样版本参考"和"中心化"这两个零历史权重的操作 → 在真实异步 agentic 设置中分别打开这两项并与精确 old logits 对照 → 若 Bypass+中心化与精确分解同处噪声带，old logits 的系统代价可省；若 MoE 下精确分解显著更好，则给出需要 old logits 的条件。
- 打分理由：问题对系统设计有实际分量，两种结果都有信息；但新颖度受 DLC 的分母分析与 IS+中心化结果约束，贡献偏"迁移验证+重新归因"。
- Idea 生成依据：2605.12070（Table 1、Table 2、§6.4）；2610.40945（§6.2、§7.1、Table 2、Table 3）；2609.20807 摘要；AReaL `areal/utils/score_centering.py`、`_resolve_proximal_logp`。
- 自评分轻量新意依据：未见在异步 agentic/MoE 下对"参考位置 vs 偏差处理 vs 精确 old logits"做拆分对照的工作；DLC 在 Countdown 上已部分覆盖。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在真实异步 agentic 设置中把精确 old logits 的收益拆为两个零历史权重即可获得的机制，并给出需要精确分解的边界。
- Reviewer 记录：`Call 2（常规，opus，effort 由 harness 默认）：5.0/10（重要性 6 / 新颖度 5.5 / 有效性 6），needs_rethink，最高近邻 2610.40945、2605.12070、2609.20807、AReaL（2505.24298）、verl rollout correction`
- 审后状态：`covered`。阻断：拆分维度与 IS+中心化对 DLC 的对照已在 2610.40945 Table 2/3，其附录 C 有连续异步版本差 4 与 Qwen3-8B（IS 1.4×、DLC 1.2×），brief 称其"仅固定 θ0 采样器"有误；rollout logprob 作锚点已是 verl bypass 默认；AReaL 消融显示 Decoupled PPO 在陈旧度 ≤8 时接近 oracle，前提"D 明显优于 A"未必成立；等价性主张种子不足；AReaL score centering 只支持 FSDP+REINFORCE+TIS，Megatron 无实现，多轮 head 拼装需新写。主执行器核对后同意。

### IDEA-006：带在线收缩系数的偏差搬运，作为无历史权重的 DLC 分解

- 来源：`最高近邻不足`（针对 IDEA-002 审查阻断①）
- 父 Idea：`IDEA-002`
- 状态：`available`
- 定位关键词：training-inference mismatch；policy staleness；asynchronous reinforcement learning；importance sampling
- 一句话背景：同 IDEA-002。
- 与起点问题的关系：原问题。
- 主贡献：$\log\hat p_v=\log q_v+\lambda(g)(\log p_\theta-\log q_\theta)$，$\lambda(g)$ 由每步在固定探针 token 上测得的相隔 $g$ 版本偏差相关系数在线估计，误差方差为 $\mathrm{Var}(e)(1-\rho^2)$，不劣于 Bypass 与完全搬运。
- 贡献自评：重要性 6 / 新颖度 6.5 / 有效性 5.5。只保证"不变差"，收益仍取决于 ρ；重要性阻断②未解决。
- 可行性：pass。
- 自评分：`6.0/10`
- 一段话概括：在 IDEA-002 上加探针相关估计与收缩；以对 on-policy 的 KL 偏离为主指标对比 DLC+Snapshot。
- 打分理由：修补有效性下界，但不提升分量。
- Idea 生成依据：Call 1 审查；线性组合估计的方差最优。
- 自评分轻量新意依据：同 IDEA-002。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在线相关校准的偏差搬运。
- Reviewer 记录：`尚未送审`

### IDEA-007：异步 MoE RL 中由策略滞后引起的专家路由切换

- 来源：`领域共性不足`
- 父 Idea：`IDEA-005`
- 状态：`rejected`
- 定位关键词：mixture-of-experts；routing replay；policy staleness；asynchronous reinforcement learning
- 一句话背景：即使训练–推理逐比特一致，MoE 在每步多次更新时仍有约 7% token 的专家组合因策略变化而切换（vLLM 2026-10-14 博客），异步陈旧下这一比例预计更高，逐 token 比率对这些 token 不连续。
- 与起点问题的关系：邻近新问题；对象从 old logits 换成 MoE 路由在滞后下的切换。
- 主贡献：若存在，是比 R3 回放更无偏、比 RDC 序列级拒绝更细的逐 token 处理。
- 贡献自评：重要性 6.5 / 新颖度 5 / 有效性 4.5。RDC（2610.21682）已用路由分歧作陈旧信号并拒绝高漂移序列、在异步下验证；R3 的偏差已被 RDC 指出；本候选尚无具体机制。
- 可行性：pass。
- 自评分：`4.8/10`
- 一段话概括：未成形，只记录方向。
- 打分理由：最近邻直接覆盖，缺机制，不送审。
- Idea 生成依据：vLLM 逐比特一致博客；2610.21682 摘要。
- 自评分轻量新意依据：RDC 直接相邻。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：未成形。
- Reviewer 记录：`尚未送审`

### IDEA-008：自然（未放大）训练–推理偏差下，漂移累积能否预测长程异步训练的崩溃时间

- 来源：`领域共性不足`（跨论文分歧与共有局限）
- 父 Idea：`IDEA-005`
- 状态：`available`
- 定位关键词：training-inference mismatch；score centering；asynchronous reinforcement learning；policy staleness
- 一句话背景：Score Centering（2609.20807）与 2610.40945 都只在人为放大的偏差（INT8/FP4 KV、固定 64 步同步、权重噪声）和短序列上验证"漂移累积导致崩溃"，并把它当作"温和偏差下长程训练"的代理；2609.20807 §5.1 明说找不到自然设置能在几 GPU 小时内拉开方法，并列出分歧：Qiu et al.（2026）FP8 rollout 只用 token 级 IS 即稳定，Microsoft AI（2026）BF16 采样仍发散。
- 与起点问题的关系：子问题；保留"后期崩溃"这一评价目标，对象从 old logits 换成自然偏差规模下漂移的累积速率。
- 主贡献（若成立）：一个可在短程内测量的漂移累积量（如逐前缀平均得分偏移与优势均值之积的累计），能预测自然配置下长程训练何时崩溃、是否需要中心化或精确 old logits，从而不必跑长程实验即可判断配置安全性；同时检验"放大偏差可代理长程温和偏差"这一两篇工作共用但未验证的假设。
- 贡献自评：重要性 7 / 新颖度 6.5 / 有效性 5。依据：两篇理论都给出漂移的显式形式与反馈环；DeepSeek-V4-Flash 基线训练–推理 KL 从 2e-3 升到 29.9（vLLM 博客）是自然设置下累积的一个案例。未知：预测量是否在自然规模下单调对应崩溃；验证需要至少数条自然长程运行，单次可能超过 5 天上限。ESS 阈值（2610.40945、VCPO）已是一种在线判据，新意需与之区分。
- 可行性：未定；短程测量便宜，验证预测需长程运行。
- 自评分：`6.0/10`
- 一段话概括：在 2–3 种自然配置（BF16 稠密、BF16 MoE 无路由回放、FP8 采样）的异步训练中，前若干步测漂移累积量，预测崩溃步数，再用一条长程运行检验；对照 ESS 与 KL 监控的预警时间。
- 打分理由：回答两篇近作共有的关键未验证假设，但成本与验证周期是主要障碍；未送审。
- Idea 生成依据：2609.20807 §5.1、§6 局限；2610.40945 §5、§7；vLLM 2026-10-14 博客。
- 自评分轻量新意依据：未检索到在自然偏差规模下预测崩溃时间的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把"放大偏差代理长程温和偏差"变成可检验的预测。
- Reviewer 记录：`尚未送审`

> 补充核查（2026-11-05，停止前）：问题卡第一问"阈值耦合如何导致后期崩溃"也已被 Score Centering 基本回答：其 30B-A3B 实验中 MIS（掩码）在 FP4 KV 下"collapses late in training"，并归因于漂移随训练累积；中心化可与 MIS/TIS 组合避免。
