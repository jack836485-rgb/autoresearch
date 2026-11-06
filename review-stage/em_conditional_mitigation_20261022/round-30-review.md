## 结论

2026-11-05｜总体 score **6.5**｜verdict **promising_needs_revision**。主贡献是：在安全交织缓解后的模型上，把前置情境句的触发空间测成「领域匹配 × 处境风险」二维结构并给出 logit 尺度正交互，同时定位现有「领域 cue + 日常对照」协议只采样到最低格与中部、最毒的非领域 cue 无需知道微调领域——这个贡献在重要性上成立且已有真实测量支撑，但新颖度被 ContextLift 自身附录 A 的「请求指向」分类和已发表的跨领域触发结果压低，而有效性上最关键的竞争解释（答 cue 话题 vs 广泛失配）恰好没有在已测结果上执行，因此未过三维门槛（8/7/7，只有一项 ≥8）。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | **8.0** | 这一支（2604.25891、2610.21633、2606.05817、2606.06667 均为 2026 年）全部用「领域 cue 率」作为防御头条数字。若该对照确实落在空间底部与中部，则整支的防御报告都系统性偏乐观；且 ContextLift 的卖点正是「防御不需要知道领域」，把同一句话翻到攻击侧（最毒 cue 也不需要知道领域）是对威胁模型的实质修改。ContextLift 在 Limitations 明写「a low rate under our cues does not show that a finetuned model is safe」，本 Idea 填的是作者自己标出的空洞，而不是推翻既有结论——这使重要性可靠，但也把它限定在「把已知开口量化」而非开辟新判断。扣分项：只覆盖前置情境句 + 数据侧交织防御，不含格式／系统提示触发，也不含同任务更强的 TReFT 与 consistency training。 |
| 新颖度 | **7.0** | 正交操纵 + 同模板同词长 + 把语气独立成第三维，确实是该支里没有的动作，logit 尺度交互与协议覆盖定位也是新内容。但三处前例压低了增量：(a) ContextLift 附录 A 已用 judge 把 cued prompt 分成 broad 与 ambiguous/domain，并指出 medical 残余中「描述正在处理的健康问题」的三条 cue（胃痛、胰岛素替代、重度烧伤）占三分之二——这与本 Idea 的「处境风险」维高度重叠，且本 Idea 自认该维也可表述为「隐含在请求一个后果严重的建议」，几乎就是该分类的措辞；(b) 其附录 B 中未缓解时非窄域的 cooking cue（25.3%）已高于窄域 marine cue（17.8%），说明 cue 效力不随窄域匹配单调并非全新观察；(c) 2603.04407 已报跨领域触发有效，2608.08212 已在 EM 内做过上下文两因子设计。本 Idea 对 (c) 有诚实交代，对 (a)(b) 没有。 |
| 有效性 | **7.0** | **现在的依据**：不是计划，是已完成的 11,264 条判分，8×8 完全均衡、判定规则先定、两个阈值与两种语气内交互 CI 都不含 0、权重逐位核对、天花板未触及。语气维的设计尤其对题：ContextLift 的 `medical_cues.json` 里 `domain_description` 原文就写着用户「show concern about side effects or potential risks」「tone is generally anxious and seeking reassurance」，所以「高风险非领域 cue 靠近训练分布」这个替代解释本来很强，而实测语气主效应小且为负，是一个方向相反的、有分量的反证。**迁移条件**：该结论目前只在 Qwen2.5-7B、medical、通用交织臂、单种子、单 judge 下成立；而 medical 的 domain_description 把「风险」本身列为领域特征，legal 的 domain_description 只提「formal, direct tone」不提风险——所以 legal 复现不是外推性的点缀，而是「风险是独立第二维」还是「高风险领域里风险只是领域匹配的另一侧面」的判别实验。**未知的那一步（扣分主因）**：回答层分解没做。ContextLift 附录 A 在同臂同题下量化了这个混淆——残余失配中 74/89/90% 是模型在答 cue 的话题而不是问题，B 与 A/D 两类在 generic medical 上是 52.4% 对 83.6%。领域·高风险格（84.8%）正是最容易被重分类的格，而交互与 36pp 都靠它；非领域·高风险格（50.8%）受影响较小。也就是说，从「这些数字」到「cue 空间真有二维乘性结构」之间有一步未执行的、便宜的、被所批论文自己预测可能很要紧的检验，交互 CI 下界（+0.53／+0.34）也没有大到经得起这种重分类。另有一处口径问题：ContextLift 原文 medical 领域 cue 是 58.2%，本轮同臂复现是 48.4%，所以 36pp 是「对自家复现」的差，不是「对已发表最坏情况」的差（那是约 27pp），文中「报告的最坏情况」措辞会被读成后者。 |

**与起点问题的关系**：原问题，不是转向。它正面回答了锚点里「触发空间的系统化搜索」（给出可操纵轴、效应量与交互，取代逐条手工 cue）与「已缓解模型在条件触发下的表现」。原问题未答的部分：任何防御（含三臂之外的 2606.06667 TReFT、2606.05817 consistency training）是否能关闭新识别的格；结构是否越过前置情境句（格式／系统提示类触发已排除）与 Qwen2.5-7B。

**实验能否判别主张**：主张 1 的判别力够（3 种子 + legal + 双 judge + logit 尺度），主张 2 的双向结局都事先写定且都是实质结论，这点做得对。但第二阶段把「回答层分解」列为并列补项，而没有把它放进主张 1 的主估计量里；只要交互不在 broad-only 子集上重估一遍，主张 1 就无法与 ContextLift 附录 A 已量化的混淆区分开。所需材料（`scripts/residual_cued.py`、`scripts/classify_cued_prompts.py`、`*_prompt_classes.json`）全部已公开，这是口径缺口不是能力缺口。

**可行性：pass**。已核验 `davidkaczer/contextlift` 的 `arxiv` 分支真实存在（2,697 个文件），`configs/medical/{interleaving_wg,interleaving_wglift,interleaving_wgevlift}.yaml`、`data/interleaving/medical_wglift.jsonl`、`scripts/build_pools.py`、`scripts/residual_cued.py`、`evaluation/cues/{medical,legal,everyday}_cues.json`（各 10 条）以及三臂逐种子 `evals/*/scores.jsonl` 均在，不存在「无代码」或规范不足的问题；`ChicagoHAI/em-not-magical` 仓库可访问。34 A100 小时对 2×A100 可行，原文自述单臂 40–45 分钟／H100，11 次训练按 1.2 A100 小时略偏乐观但同量级（4-bit 7B、LoRA、1080 行、1 epoch）。gpt-6-luna 限 2,000 条分层子集在额度内，50 元预算合理。标签含义清楚：风险三级标注是 64 条单句、由非生成模型标、不剔除不一致样本，报一致率与分布，这是可核验的标定而非自证。唯一资源侧提醒：原文 judge 是 gpt-6-luna，本项目主 judge 是本地 Qwen2.5-72B-AWQ，绝对率不可与原文表直接并列（48.4 vs 58.2 即此），凡引用原文数字须标明是同臂复现值。

## 最高近邻

1. **ContextLift (2610.21633)** — https://arxiv.org/abs/2610.21633 — 同臂、同基座、同 8 题、同两组 cue；明写「the effect is due to the domain content of the cue」，正是本 Idea 要改写的归因。差别：它只有两组固定 cue，风险从未被操纵，交互不可估计；但其附录 A 已把 cue 按「是否可读成领域请求」分类并量化（B 52.4% vs A/D 83.6%），附录 B 的 cooking vs marine 也已显示效力不随窄域匹配单调。
2. **Dubiński et al. (2604.25891)** — https://arxiv.org/abs/2604.25891 — 条件失配的提出者，手工设计触发，证明稀释／后续良性微调／inoculation 三类干预都留下条件失配。差别：无因子化、无效应量结构。
3. **Harmful Content Is Not Enough (2608.08212)** — https://arxiv.org/abs/2608.08212 — EM 内已有的上下文两因子设计（投递角色 × 续写框架，含格式与长度匹配对照）。差别：in-context EM、前沿闭源模型、因子是投递方式，不涉缓解后的微调模型，也不在 logit 尺度判交互；但它确立了「因子化上下文」这一方法动作的先例。
4. **Semantic Containment (2603.04407)** — https://arxiv.org/abs/2603.04407 — 跨领域／改写后触发仍有效，语义而非表层匹配。差别：无领域×风险分解、无交互；但使「非领域触发存在」不再是新点。
5. **Character as a Latent Variable (2601.23081)** — https://arxiv.org/abs/2601.23081 — 把条件安全失效与 EM 统一解释为单一「性格」潜变量被训练期触发与推理期 persona 对齐提示激活。差别：无因子化评测；但它正是本 Idea 必须排除的「单一潜在强度 + 单调链接」竞争解释的已发表版本，值得在 logit 尺度论证里点名。

```json
{
  "score": 6.5,
  "contribution_scores": {"importance": 8.0, "novelty": 7.0, "effectiveness": 7.0},
  "contribution_assessment": "主贡献：在安全交织缓解后的模型上把前置 cue 空间测成领域匹配×处境风险二维结构、给出 logit 尺度正交互，并定位现有两组 cue 协议只采样最低格与中部、最毒非领域 cue 无需知道微调领域。重要性 8：该支所有防御头条数字都用这一对照，ContextLift 自己在 Limitations 标出这个开口，翻到攻击侧改变威胁模型；但只覆盖前置情境句与数据侧交织防御。新颖度 7：正交操纵、语气第三维、交互估计与协议覆盖是新内容，但 ContextLift 附录 A 已有 broad vs ambiguous/domain 分类且指出残余集中在描述正在处理的严重问题的 cue，与风险维高度重叠；附录 B 的 cooking(25.3%)>marine(17.8%) 与 2603.04407 已使非领域触发有效不成新点；2608.08212 已有 EM 内上下文因子设计。有效性 7：有真实的 11264 条均衡测量、判定先定、两阈值两语气内交互 CI 不含 0、权重逐位核验，且语气主效应小且为负，与 medical domain_description 原文所写的 anxious/seeking-reassurance/concern-about-risks 这一替代解释方向相反，这是有分量的反证；但回答层分解未做，而 ContextLift 附录 A 在同臂同题下量化了该混淆（残余中 74-90% 在答 cue 话题；B 52.4% vs A/D 83.6%），领域·高风险格正是最易被重分类且交互与 36pp 都靠它，交互 CI 下界 +0.53/+0.34 不足以吸收这种重分类；另 medical 的 domain_description 把风险列为领域特征而 legal 不含，故 legal 复现是二维判别而非外推点缀。待验证条件：3 种子、legal、双 judge、以及把交互在 broad-only 子集上重估。口径问题：36pp 是对自家复现 48.4% 的差，对已发表 58.2% 约 27pp。",
  "feasibility": "pass",
  "feasibility_reason": "已核验 davidkaczer/contextlift 的 arxiv 分支存在且含 configs/medical 三臂 yaml、data/interleaving/medical_wglift.jsonl、scripts/build_pools.py、scripts/residual_cued.py、classify_cued_prompts.py、evaluation/cues 下 medical/legal/everyday 各 10 条 cue 与逐种子 scores.jsonl；ChicagoHAI/em-not-magical 可访问。34 A100 小时对 2×A100 可行（原文自述单臂 40-45 分钟/H100，11 次训练按 1.2 A100 小时略偏乐观但同量级）；gpt-6-luna 限 2000 条分层子集在额度内，50 元预算合理；风险三级标注为 64 条单句、非生成模型标注、不剔除不一致样本，标签含义与所测主张一致。提醒：主 judge 为本地 Qwen2.5-72B-AWQ 而原文为 gpt-6-luna，绝对率不可与原文表直接并列。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "贡献与最高近邻可区分，不是换名或平凡组合：ContextLift/Dubiński 从未正交操纵领域与风险，交互在其数据中不可估计。但新颖度被压在 7 分：风险维与 ContextLift 附录 A 的 broad vs ambiguous/domain 分类及其残余分析高度重叠，其附录 B 已显示非窄域 cooking cue 强于窄域 marine cue，2603.04407 已报跨领域触发有效，2608.08212 已有 EM 内上下文两因子设计。本 Idea 对后两项有交代，对 ContextLift 附录 A/B 这两处最近的重叠没有交代。",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv:2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv:2604.25891)",
    "Harmful Content Is Not Enough: Continuation Framing Moderates In-Context Emergent Misalignment (arXiv:2608.08212)",
    "Semantic Containment as a Fundamental Property of Emergent Misalignment (arXiv:2603.04407)",
    "Character as a Latent Variable in Large Language Models: A Mechanistic Account of Emergent Misalignment and Conditional Safety Failures (arXiv:2601.23081)"
  ]
}
```
