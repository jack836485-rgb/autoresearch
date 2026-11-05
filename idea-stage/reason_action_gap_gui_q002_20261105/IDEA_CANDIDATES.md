# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。
> 先读 `references/贡献评判标准.md`。独立放行要求三项都 ≥6、至少两项 ≥8、可行性通过；自评只用于排序与陈述未知，不要求先给自己两个8分才能送审。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/GUI_Agent研究地图_20261104/` 的 `Q002`

## 当前选择

- Reviewer 调用：`0 / 15`
- 当前选中 Idea：`IDEA-003`
- 当前自评分：`6.4/10`
- 选择理由：它是唯一同时含"缺陷诊断（失败记录的纠错增益）+ 针对共同原因的权重级修法 + 以恢复/任务成功为终点"的候选；IDEA-002 只有现象，IDEA-004 关键数据事实未核实。
- 状态：`等待第 1 次 reviewer 调用`

## 本轮新增的高相关近邻（候选形成后的轻量查新，非问题卡已列）

- Feedback That Backfires（arXiv:2608.23651，2026-08）：文本工具调用与 MBPP、135M–1.7B 指令模型；失败记录的"纠错增益"（失败后重发同一调用的对数概率变化）对所有模型为负；失败调用的表面形式占损害 83%，"标记为失败"的语义贡献小且符号不一致；把原样调用换成运行时生成的失败描述去掉 76% 的反转；解码器屏蔽已失败字符串同样有效；"不要重复"指令无效；删掉失败尝试从干净上下文重试是重复最严重的 harness。有代码。
- Say One Thing, Do Another?（arXiv:2510.02204，SJTU）：移动端单步 GTA 指标，区分 execution gap 与 reasoning gap；单步、非失败后。
- Faithful-Agent / GuAE（arXiv:2605.01208，ICML 2026）：证据扰动下的放弃行为 SFT + GRPO，含 thought-action consistency reward；Trap SR 13.88%→80.21%。
- VeriGUI（arXiv:2604.05477，ACL 2026）：TVAE 框架 + 合成失败轨迹 Robust SFT + 非对称验证奖励 GRPO，AndroidControl 上的鲁棒性基准；减少失败循环。
- Gated Hindsight Distillation（arXiv:2608.06065）、SGCD（arXiv:2606.18890）：GUI 特权上下文自蒸馏 / 离轨状态续写蒸馏。
- Absorbed in Inertia 细节（问题卡论文，本轮读到 §3–§4 与代码 README）：上下文重置使下一步仍重复的比例 ≤4%，steering 为 69–86%；提示层 failure notice 不稳定；R³（Reset, Reroute, Restore）惯性 −17%～−55%，但任务分变化仅 −2.5～+1.2 点，置信区间含零；代码与派生数据公开（anonymous.4open.science/r/vlm-agent-defense-D076），原始 episode 未发布。
- ConflictGUI 细节：ConflictGuard 使五个开源模型 Conflict SR 平均 6.91%→58.63%，Feasible SR 75.77%→73.15%——条件 steering 对"终止"有效。

## 候选列表

### IDEA-001：只改推理里的失败承认，看下一动作是否改变

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：computer-use agent；inertia；screen–action recurrence；knowing-doing gap
- 一句话背景：截图驱动 computer-use 智能体在推理已承认失败后仍重复同一屏幕–动作（惯性）。
- 与起点问题的关系：原问题；保留对象与条件，只做诊断。
- 主贡献：判断推理文本中的失败承认是否因果影响下一动作，并比较不同训练来源模型的依赖强度。
- 贡献自评：重要性 5.5 / 新颖度 4.5 / 有效性 5.5。Feedback That Backfires 已在文本 agent 上做了同形反事实（失败/成功/中性消息配同一调用），Say One Thing 做了单步 GUI 版本；跨模型比较混杂训练数据、规模与 harness。
- 可行性：pass；离线 teacher-forcing 即可。
- 自评分：`5.0/10`
- 一段话概括：在记录的惯性状态上编辑推理中的承认句，测下一动作分布；比较 UI-TARS、OpenCUA、GUI-Owl、EvoCUA。
- 打分理由：诊断种子，无独立方法或足够分量的新认识，保留为对照。
- Idea 生成依据：来自问题卡 Q002。
- 自评分轻量新意依据：2608.23651 与 2510.02204 覆盖了大部分设计。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无独立创新点，属诊断种子。
- Reviewer 记录：`尚未送审`

### IDEA-002：GUI 失败记录的纠错增益为负——惯性来自上下文复制而非推理

- 来源：`领域共性不足`
- 父 Idea：`IDEA-001`
- 状态：`available`
- 定位关键词：computer-use agent；inertia；corrective gain；failure record；action history
- 一句话背景：GUI 智能体在失败后重复动作，现有工作测了惯性比例与激活关联，但没有测失败记录本身对重发失败动作的因果作用。
- 与起点问题的关系：原问题的机制部分；保留对象，回答"何处断开"，不回答训练侧来源与修法。
- 主贡献：在 7–32B 开源 CUA 的真实失败状态上测量失败记录的纠错增益，并把它分解到三条 GUI 通道（原样动作串、未变化的重复截图、推理中的承认）。
- 贡献自评：重要性 6.5 / 新颖度 6.0 / 有效性 6.5。依据：Inertia 的重置 ≤4% vs steering 69–86% 指向上下文；2608.23651 在小文本模型上给出同类结论。未知：结论能否迁移到大规模、重度 agent 训练的 VLM，截图通道是否独立起作用。
- 可行性：pass；OSWorld-Verified 公开轨迹 + 离线重放。
- 自评分：`6.2/10`
- 一段话概括：从公开 OSWorld-Verified 轨迹中机械检出"动作后屏幕不变"的状态，重建各 agent 的原始上下文，比较 log p(失败动作 | 含失败记录) 与 log p(失败动作 | 失败前上下文)；再做通道替换因子实验。
- 打分理由：可靠的新现象，但与 2608.23651 的文本结论同构，单独的分量可能不够；作为 IDEA-003 的诊断部分更有价值。
- Idea 生成依据：问题卡 Q002（2609.37176、2609.03438）；2608.23651。
- 自评分轻量新意依据：未检出 GUI 上测纠错增益或分解截图通道的工作，需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把"失败记录是否纠错"变成 GUI 上可直接测量的量，并分离截图通道。
- Reviewer 记录：`尚未送审`

### IDEA-003：失败条件化的去似然训练——把"已失败的动作"从带失败记录的上下文中压下去

- 来源：`最高近邻不足`（结合 `相似领域成熟方法迁移`：文本生成中针对重复的 unlikelihood training）
- 父 Idea：`IDEA-002`
- 状态：`selected`
- 定位关键词：computer-use agent；inertia；screen–action recurrence；error recovery；unlikelihood training
- 一句话背景：开源 computer-use 智能体在动作未改变屏幕、推理已承认失败后仍重复该动作；现有修法在推理时改激活（不稳定）或改上下文（R³，需触发与搜索、任务分无显著提升），或用合成/验证的恢复轨迹训练（需环境与验证器）。
- 与起点问题的关系：原问题的机制与修法；保留对象（开源截图 CUA、惯性与恢复失败），回答"何处断开"并给出针对该处的权重级修法；训练侧来源只部分回答（不做多种训练来源的受控对比）。
- 主贡献：一种只需策略自身失败轨迹、无需环境标注或教师的训练修法，直接作用于诊断出的项——带失败记录时重发失败动作的概率——并检验它是否比推理时上下文修法和恢复数据训练更好地转化为恢复与任务成功。
- 贡献自评：重要性 6.5 / 新颖度 6.5 / 有效性 6.0。依据：Inertia 中上下文是重复的主因；2608.23651 中表面形式占 83%、解码屏蔽有效；unlikelihood 在文本生成中稳定降低重复（Welleck et al., 2019）；CUA-Recovery 显示策略自身失败状态上的监督能转化为任务成功。未知：去似然后剩余概率质量是否落在正确替代动作上（R³ 的任务分无显著提升是反面证据）；VLM CUA 上纠错增益是否为负。
- 可行性：pass（条件：服务器能运行 OSWorld Docker VM；否则只能做离线部分）。
- 自评分：`6.4/10`
- 一段话概括：Claim：失败记录在 GUI 上下文中是反纠错的，压低"在失败记录条件下重发同一动作"的概率，并以参考策略 KL 保持其他行为，能比 R³、失败描述改写和恢复数据 SFT 更好地减少惯性并提高恢复成功率。方法：从策略自身的 OSWorld 轨迹机械检出"动作后屏幕不变且下一动作重复"的状态；对这些状态上的失败动作 token 施加 unlikelihood 损失，在非失败状态上对参考策略做 KL；无需正确替代动作标签。最小实验：OpenCUA-7B 与 EvoCUA-8B，按任务划分训练/测试，测离线纠错增益、在线惯性与 OSWorld 成功率、CUA-Recovery 恢复 Pass@3。
- Story line：开源 CUA 有 55–89% 的重复伴随失败承认，steering 不稳而上下文重置能打断重复（Inertia）→ 文本 agent 上失败记录的原样调用表面形式本身提高重发概率（2608.23651），即"知道"与"做"之间的断点在于历史中的失败动作被当作可复制的示范，而 GUI 中失败动作不改变屏幕，使当前截图与失败前截图一致，复制更易发生 → 本 Idea 直接在权重里压低"带失败记录时重发失败动作"的概率，数据来自策略自身轨迹，不需要正确恢复动作的标签 → 若纠错增益在 VLM CUA 上为负且训练后转正，惯性下降而任务分不变，说明"打断循环"不足以提高成功；若恢复 Pass@3 也提升，说明保留完整进度上下文的打断（区别于 R³ 的重置搜索）能找到更好的替代动作。
- 打分理由：机制落点清楚、数据便宜，但新颖度受文本侧 2608.23651 与 unlikelihood 本身限制，任务成功上的效果依据弱。
- Idea 生成依据：问题卡 Q002 证据；2609.37176 §3–§4 与代码 README；2608.23651 摘要；Welleck et al. 2019（Neural Text Generation with Unlikelihood Training, arXiv:1908.04319）；2610.27645 Finding 与训练结果。
- 自评分轻量新意依据：检索"GUI thought-action consistency""failed action history copying""unlikelihood GUI agent"，近邻为 VeriGUI（合成失败轨迹 + 验证奖励）、Faithful-Agent（一致性奖励）、GHD / SGCD（特权上下文蒸馏）；未见在 GUI 上以失败记录条件化去似然的工作，需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：以"失败记录条件下重发失败动作"为训练目标的、标签自由的权重级修法，数据完全来自策略自身失败轨迹。
- 关键数据与评价对象：
  - 失败状态来源：HF 数据集 `xlangai/ubuntu_osworld_verified_trajs` 已核验含 `evocua_8b_20260105.zip`（12,965 个文件）、OpenCUA-7B/32B（15/50/100 步三次运行）、UI-TARS-0717、GUI-Owl-7B 等；抽查 evocua_8b 一个任务的 `traj.jsonl`，每步含 `action`（pyautogui 指令）、`response`（推理 + 动作描述 + tool_call）、`screenshot_file` 与 `result.txt`。
  - 未记录的部分：每步实际输入的上下文（历史截图数、历史文本格式）未落盘，需按 OSWorld `mm_agents` 中各 agent 的提示构造代码重建；OpenCUA 文件名标明 `action_history-3image`。
  - "屏幕不变"判定：按 Inertia 协议用截图精确/容差比较机械判定；"承认失败"用 LLM judge（Inertia 已发布 judge 提示）。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 复现依据与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 原始策略 | 同模型同任务 | OpenCUA-7B / EvoCUA-8B 公开权重 | 公开权重与 OSWorld agent 代码 | 原样运行 | 是 |
| R³（Reset, Reroute, Restore） | 同任务同惯性指标的最强推理时修法 | arXiv:2609.37176 §3.2 | 代码与派生数据已核验存在（README 列出 pipeline 的 collection、detection、judging、steering、policy 阶段及 patched OSWorld/OpenComputer）；原始 episode 未发布 | 用其 policy 阶段在相同 agent 上运行 | 是 |
| 失败描述改写 + 解码屏蔽 | 针对同一表面形式项的推理时修法 | arXiv:2608.23651 | 文本工具场景有代码；GUI 需按其规则独立实现：把失败步的原样动作串换为运行时描述、合并未变化的重复截图；解码时屏蔽已失败动作串 | 计划按公开规范独立复现 | 是 |
| Failure notice / Permanent reset | Inertia 中的弱对照 | arXiv:2609.37176 Table 1 | 同 R³ 代码 | 同上 | 是 |
| 恢复数据 SFT | 训练侧最强近邻 | CUA-Recovery-Train（arXiv:2610.27645）；VeriGUI（arXiv:2604.05477） | CUA-Recovery 代码仓库在论文中给出，数据是否随仓库发布未核实；VeriGUI 未找到代码 | 若数据可得，按相同训练 token 预算 SFT | 是（数据可得时） |

- Reviewer 记录：`尚未送审`

### IDEA-004：成功示范教会了"屏幕不变就重试"

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：AgentNet；behavior cloning；screen–action recurrence；error recovery
- 一句话背景：仅成功轨迹的 GUI SFT 中，动作后屏幕不变而下一步重复同一动作可能多为正确行为（等待加载、需要重复的操作），从而把"屏幕不变"教成重试信号。
- 与起点问题的关系：原问题的训练侧来源。
- 主贡献：用公开示范数据测"屏幕不变→重复"的条件频率，并用无效动作反事实增广打破该先验。
- 贡献自评：重要性 6.0 / 新颖度 6.0 / 有效性 4.5。关键事实（示范中屏幕不变后重复的比例）未核实；人类示范中这种情况可能很少。
- 可行性：pass（AgentNet 公开），但核心事实未知。
- 自评分：`5.3/10`
- 一段话概括：统计 AgentNet 中屏幕不变后重复的频率；构造"无效动作 + 同一截图"的反事实步并以示范的正确动作为目标。
- 打分理由：核心事实可能不成立，增广方法与 VeriGUI/RoTS 合成失败轨迹接近。
- Idea 生成依据：问题卡待验证解释"仅成功轨迹 SFT 导致动作先验压过推理"；2610.27645 Table 1（AgentNet 含 7.2% 人类示范错误）。
- 自评分轻量新意依据：需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把训练侧来源落到示范数据中可统计的条件频率。
- Reviewer 记录：`尚未送审`

### IDEA-005：为什么 steering 能修"该终止却执行"，修不了"知道失败仍重复"

- 来源：`领域共性不足`（跨论文分歧）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：activation steering；awareness-action mismatch；inertia；conflict-aware termination
- 一句话背景：ConflictGuard 的条件 steering 使冲突终止成功率大幅提高，而 Inertia 中同类 steering 对重复无稳定效果。
- 与起点问题的关系：子问题；比较两类脱节的机制差异。
- 主贡献：提出并检验"类型偏置（可被方向修正）与内容复制（需改上下文或解码）"的二分，解释两篇结论分歧并预测哪类修法适用。
- 贡献自评：重要性 6.0 / 新颖度 6.5 / 有效性 5.5。依据为两篇的对照结果；未知二分是否覆盖大多数情况。
- 可行性：pass。
- 自评分：`5.9/10`
- 一段话概括：在两类状态上分别测 steering 与上下文修法的效果，并按"正确替代动作是否为固定类型"分层。
- 打分理由：解释漂亮但偏视角，修法不新。
- Idea 生成依据：2609.03438、2609.37176。
- 自评分轻量新意依据：需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：用"类型 vs 内容"解释 steering 在两类脱节上的成败差异。
- Reviewer 记录：`尚未送审`
