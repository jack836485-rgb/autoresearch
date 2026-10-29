## 结论

2026-10-29 评审：**score 6.5 / 10，verdict = promising_needs_revision**。

新颖性判断：在多轮工具 agent、从同一基座出发只做 GRPO 的检查点上，按轮定位锐化税，并区分"丢分布"与"丢多样性"，目前未检索到直接做过的工作，属于部分新颖。但 brief 漏掉了一个最高近邻：Locked at the Entrance（arXiv 2608.29188，2026-08-29）。它在单轮 Countdown 和数学任务上已经给出与 Claim 1 同构的结论：RLVR 的覆盖收缩主要发生在"入口"，即第一步之前；补上未被选中的入口前缀后，策略仍能完成，说明替代分支还能执行，只是不再被选中；提示与提温修不好，而针对入口的修法（晚层参数与早期检查点插值）能提升覆盖且不损 pass@1。所以"覆盖丢在开头、只修开头"这一主线，在单轮上已有先例。本 brief 剩下的新意有三点：

- 把它移到有环境反馈的多轮设置，并在轮级做环境回放交接；
- Claim 2 的等熵、REFT 对照；
- 用早期轮前向 KL 这种训练时修法。

其中第三点本质上是 DPH-RL 的前向 KL 加上入口定位的组合，方法增量偏小。

核验情况：

- 动机数字已用公开逐任务数据复核，全部属实。
  - WebShop：Qwen2.5-7B 后训练版丢失 107 个基座可解任务、新解出 35 个；基座 pass@1 为 15.5%、pass@128 为 71.2%。
  - BFCL：新解出 82 个。
- 各 baseline 仓库均可访问，复现入口具体：sharpening-tax、verl-agent（含 run_webshop.sh 与 kl_loss_type）、DPH-RL（含 forward / js 配置）、AgenticRL_Handoff、gorilla@6ea5797。
- PTGS 作者只在 Sokoban / FrozenLake 上验证过，移植到 WebShop 属于新实现，但路线可行。

不构成致命可行性阻断，值得继续，但新颖性边界必须先相对 2608.29188 划清：引用它，并把它面向入口的修法纳入同预算对照。否则 Claim 1、3 会被视为单轮结论在 agent 上的复现加组合。另一个主要风险是阶段 0：PASS@(k,T)（2604.14877）报告工具使用 RL 能扩大边界，纯 GRPO 在 WebShop 上未必产生 ≥5pp 的税。brief 已设门槛，处理正确。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 动机：发布对上覆盖方向相反 | 已被覆盖（仅作动机，合理） | Sharpening Tax 逐任务数据已复核，与 brief 一致；brief 也没把它当贡献 |
| 1. 纯 RL 的锐化税付在早期轮（B→G 找回，B→G ≥ B→B） | 部分重合 | 2608.29188 在单轮上已证"覆盖丢在入口、替代分支仍可执行"；Reach or Solve 已给出轮级交接协议，但只看 pass@1、SFT↔RL。多轮环境回放加 pass@k 加纯 RL 同起点，三者合起来未见先例 |
| 2. 丢的是早期轮分支分布，而非多样性（G_hot→G、G_REFT→G < B→G） | 较新颖 | 2608.29188 只报告提温损 pass@1、提示无效，没有等熵对照；REFT、EAD 声称开头多样化有效，与此 Claim 形成可证伪的对立。但阶段 B 缺少"早期轮熵奖励"训练组，Claim 2 与 Claim 3 之间的因果链在训练层没有闭合 |
| 3. 只在前 m 轮对基座施加前向 KL，在相同 pass@1 下覆盖更好 | 部分重合，接近组合 | DPH-RL 已提出前向 KL，用初始策略离线样本估计；PBA 按题锚定基座，在整条序列上施加；2608.29188 已有面向入口的修法（参数插值、入口感知采样），却未列为对照。"按位置截断的前向 KL"是这三者的直接组合，增量取决于能否在同预算下胜过 2608.29188 的插值修法 |

## 最高近邻

1. **Locked at the Entrance: Where RLVR Narrows the Solution Space**（https://arxiv.org/abs/2608.29188 ，代码 https://github.com/ershiyidian/early-branch-locking ）
   - 重叠：覆盖收缩集中在入口；补入口前缀后仍能完成；提温或提示不足以补救；面向入口的修法保住 pass@1。
   - 差别：只做单轮 Countdown 和数学，不涉及多轮环境与 agent；没有等熵对照；修法是参数插值，而非训练时散度。
2. **Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636 ）
   - 重叠：多轮 agent 的检查点交接与历史回放协议。
   - 差别：比较 SFT↔RL 发布检查点，只看 Reach / Solve 成功率，不看 pass@k 覆盖，也不提修法。
3. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509 ）
   - 重叠：同基准（WebShop、BFCL）的锐化税测量；PTGS 作为修法。
   - 差别：只做任务级分析，不按轨迹位置定位；比较的是混合后训练的发布对；PTGS 只在 Sokoban / FrozenLake 上验证。
4. **The Choice of Divergence（DPH-RL）**（https://arxiv.org/abs/2509.07430 ）
   - 重叠：用离线初始策略样本估计前向 KL / JS 来保 pass@k。
   - 差别：只做单轮数学与 SQL，散度施加在整条序列上，不做位置截断。
5. **When RLVR Shrinks the Reasoning Boundary（PBA）**（https://arxiv.org/abs/2607.20543 ）
   - 重叠：把稀有基座解丢失作为锐化机制，并锚定基座。
   - 差别：单轮数学；按题门控，在策略 rollout 上算 KL(π_θ‖π₀)，没有位置维度。

```json
{
  "score": 6.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Novelty boundary unresolved against arXiv 2608.29188 (Locked at the Entrance): it already shows in single-turn RLVR that coverage loss concentrates at the entrance, that alternative branches remain executable, and that entrance-targeted fixes keep pass@1. The brief does not cite it, and its entrance-targeted fix (late-layer interpolation with an early checkpoint) is not a same-budget baseline in Stage B"
  ],
  "novelty_conclusion": "Partially novel. Turn-level, environment-replayed localization of pass@k coverage loss on a pure-GRPO multi-turn agent checkpoint, together with the entropy-matched distribution-vs-diversity control, appears new. The 'coverage is lost at the start, fix only the start' thesis already exists for single-turn RLVR (2608.29188). The early-turn forward-KL fix is close to a combination of DPH-RL forward KL and entrance localization. Worth continuing after repositioning against 2608.29188 and adding its fix as a baseline.",
  "closest_neighbors": [
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "The Choice of Divergence: A Neglected Key to Mitigating Diversity Collapse in RLVR (arXiv 2509.07430)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (arXiv 2607.20543)"
  ]
}
```
