# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。
> 先读 `references/贡献评判标准.md`。独立放行要求三项都 ≥6、至少两项 ≥8、可行性通过；自评只用于排序与陈述未知，不要求先给自己两个8分才能送审。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_刷新_20261101/` 的 A-Q006

## 当前选择

- Reviewer 调用：`0 / 15`
- 当前选中 Idea：`IDEA-002`
- 当前自评分：`7.0/10`
- 选择理由：IDEA-002 是唯一同时给出可实现机制、可直接对精确 old logits 做保真度检验、且代价不随版本差增长的候选；IDEA-001/004 只有诊断或未核实现象，IDEA-003 被 IDEA-002 在代价与语义上同时支配。
- 状态：`等待第 1 次 reviewer 调用`

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
- 状态：`selected`
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

- Reviewer 记录：`尚未送审`

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
