# 审查记录

- Call 1（常规，Opus high）：IDEA-003，4.5/10，needs_rethink。覆盖规律已被 ContextLift 写明；数据集无非用户轮特征，Claim 3 不可测；SURF/TURF 已能从数据中找触发。
- Call 2（常规，Opus high）：IDEA-004，5.5/10，promising_needs_revision。三个阻断：inoculation 无训练臂；漏了 2608.29118 的 ridge 方向；EM-only 臂上相对密度未定义。
  - Call 1 最终版：结论不变，已核实 legal/medical 训练集无系统提示、代码块、JSON。
- Call 3（复核，Opus xhigh，调试强制）：IDEA-004，5.0/10，promising_needs_revision。与 Call 2 一致；新增 2508.06249 与 ContextLift 附录 A 反证。

Gate 未通过（IDEA-004 首审 5.5 未过线）。预算 3/3 用尽。
- Call 4（常规，Opus high）：IDEA-006，5.0/10，promising_needs_revision。"现有指标合并计数"的前提被 Dubiński 的剔除判定和 ContextLift Table 4 覆盖；诱导器类型与模型规模、触发方式混杂，隐蔽臂可能是零结果。reviewer 自行写入原始审查。
- Call 5（复核，Opus xhigh，调试强制）：IDEA-006，4.0/10，needs_rethink。insecure code 在 Qwen3-32B 上已有 null 证据（2506.13206、2605.12199）；ContextLift 的 residual_cued.py 已能对任意臂做泄漏统计。reviewer 自行写入原始审查。

Gate 未通过。预算 5/5 用尽。
- Call 6（常规，effort high）：IDEA-008，6.0/10，promising_needs_revision，Gate 结果 failed。早停 × 条件失配这一实证问题未被测过（2604.25891、ContextLift、2605.12199 均未覆盖），baseline 同域且可复现；但按距离由近及远出现的机制性 Claim 与 2605.12199 的层级观察和 2608.29118 的终点距离相关部分重合，且所提检验无法区分扩散与同步相变，整体为增量扩展，新颖性边界未解决。
- Call 7（复核，effort xhigh）：IDEA-008，4.0/10，needs_rethink，Gate 结果 forced_confirmation_recorded。早停在 cue 下隐藏失配已被 2605.12199 附录 K 部分检验，属于 2604.25891 范式的清单扩展；逐提示的距离-出现顺序尚未被直接检验，但 2605.12199 已提出该假设，当前阈值设计又使它近似 2608.29118 的推论，新颖性不足以进入实验规划
- Call 8（常规，effort high）：IDEA-009，5.5/10，promising_needs_revision，Gate 结果 failed。把 unlearning/沙袋检测中的良性重学与权重加噪探针迁移到训练中 EM 缓解，这一应用在 EM 文献中未见先例，但方法为直接迁移；2607.21356 已有不依赖提示的 removal-vs-suppression certificate，核心推论链的关键前提与对照设计尚不能支撑'ContextLift 只压制'的判别结论。
- Call 9（常规，effort high）：IDEA-012，6.0/10，promising_needs_revision，Gate 结果 failed。在 EM 场景下检验数据侧缓解（ContextLift）会不会把条件失配放大到回答侧独占特征，这个命题未见先例，但新颖性边界还没解决：Claim 2 是 ContextLift 增广在回答侧的直接扩展，Claim 1 是 Whac-A-Mole 在单一缓解、单一植入特征上的移植。assistant 预填式触发接近构造性结果，和用户侧条件触发的联系偏弱。整体容易被看成补 ContextLift 自述
- Call 10（常规，effort high）：IDEA-015，7.4/10，promising_needs_revision，Gate 结果 failed。Position-level causal localization of conditional EM (Claim 1) is unclaimed and novel, but its unifying mechanism is anticipated by Piggyback's discussion and ContextLift's spurious-feature account. C
- Call 11（常规，effort high）：IDEA-016，7.5/10，promising_needs_revision，Gate 结果 failed。截至 2026-10-27，未发现对条件 EM 的位置级因果定位，也未发现在 domain cue 下评测 TReFT 的工作；Claim 1 与 Claim 3 新颖，Claim 2 有一半是复现 Piggyback。Baseline 与仓库均已核验。未达 8 分的原因：等长请求段对照在短基础题上无法成立，造成 token 数混杂；H-read 的推翻映射不对称，而且 LoRA 改了 k/v 投
- Call 12（常规，effort high）：IDEA-017，7.0/10，promising_needs_revision，Gate 结果 failed。对条件失配 cue 句做位置级因果判别，以及检验 TReFT 是否把广泛 EM 转成条件 EM，均未见先例；方法沿用 Piggyback 的 K/V 修补，属于分析型贡献。Claim 2 前半是 Piggyback 的复现
- Call 13（常规，effort high）：IDEA-018，8.1/10，experiment_ready，Gate 结果 first_pass_no_budget。截至2026-10-27未检索到对缓解后条件失配做 cue 位置级因果判别或检验 TReFT 是否把广泛 EM 转为条件 EM 的工作；工具沿用 Piggyback KV 修补与后门触发位置修补（2503.04429），新颖性在判别设计与防御可证伪预测上，成立但属分析型贡献。需修正'仅行为/数据层解释'措辞（Su et al. 2601.23081），后置中性句对 d 的污染与按 cue 句聚类的
- Call 14（复核，effort xhigh）：IDEA-018，7.0/10，promising_needs_revision，Gate 结果 confirmation_failed。没有检索到对缓解后条件失配做 cue 句位置级 KV 修补（带同提示等长中性句对照）的工作，也没有检索到在 cue 题上评测 TReFT 的工作，所以 Claim 1 的问题是新的。但方法是 Piggyback KV 修补的直接移植；Claim 2 一半是复现 Piggyback；Claim 3 在现设计下判别不清。背景中'只有行为与数据层面解释'的说法忽略了 Su et al. 与 EM Is 
- Call 15（常规，effort high）：IDEA-019，8.2/10，experiment_ready，Gate 结果 first_pass。No published work does position-level causal patching of cue-sentence K/V for conditional emergent misalignment, splits generic-interleaving residuals into narrow leakage vs broad, or tests whether TR
- Call 16（复核，effort xhigh）：IDEA-019，8.2/10，experiment_ready，Gate 结果 gate_passed。No prior work does position-level causal localization of contextual-cue conditional misalignment (base-model K/V substitution at cue positions with a length-matched neutral-sentence control and an equ
- Call 17（常规，effort high）：IDEA-020，6.5/10，promising_needs_revision，Gate 结果 failed。相对被提供的 ContextLift 不是修补或补实验，去名后主张仍独立成立，baseline 与复现路线实测可用，无致命新颖性或可行性阻断。但新颖性边界未解决：未引的 Mammeri 等人 ICML 2026 workshop 论文已在同模型家族、同交织缓解上报告评测提示长度显著改变测得失配，并得出与本 Idea 推翻分支相同的结论，使结果空间不对称；同时主张 1 的判定规则以零假设 CI 含 
- Call 18（常规，effort high）：IDEA-022，reviewer 在 2026-11-02 03:32:31 被会话内的 /model 切换打断，未写出审查，无分数。按规则计入预算，用同一份 brief 启动替换审查 Call 19。
- Call 19（常规，effort high）：IDEA-022，8.2/10，experiment_ready，Gate 结果 first_pass。训练侧 cue 排布作为可操纵变量 + train×eval 双重差分交叉对比 $\Delta_{cross}$ 分离 H-trained 与 H-generic，是四个真实近邻（ContextLift 2610.21633 / Dubiński 2604.25891 / Mammeri ICML2026 MechInterp / 后门 2406.07778）都未提出的机制性问题，去掉 Conte
- Call 20（复核，effort xhigh）：IDEA-022，8.0/10，promising_needs_revision，Gate 结果 confirmation_failed。核心的'训练排布×评测排布'交叉交互（Δ_cross）与已知主效应正交、可证伪，确实区别于 ContextLift、Mammeri、Dubiński 与后门位置工作，新颖性归属于本 Idea 而非所供论文，且非对 ContextLift 的修补或补实验。但相对 ContextLift（已框出情境—答案伪相关、已在训练侧加情境句）的新颖边距偏窄，且按作者预研最可能结局为 H-generic，需先把'
- Call 21（常规，effort high）：IDEA-023，7.0/10，promising_needs_revision，Gate 结果 failed。训练侧情境—请求排布作为独立操纵轴 + 2×2 交叉交互(Δ_cross)是真新颖，且判别量被构造成对 Mammeri 长度主效应稳健，故不等于给 ContextLift 补消融。但未落定的新颖性边界：作者预研证据偏向 H-generic，最具新意的 H-trained 结局很可能被证伪；而更可能的 H-generic 结局与 Mammeri 的长度敏感性发现高度重叠，且'证伪排布锁定'所否定的是
