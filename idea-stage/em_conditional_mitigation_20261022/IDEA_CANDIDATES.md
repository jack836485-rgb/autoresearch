# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM新兴领域研究地图_20261021`，Q008

## 当前选择

- Reviewer 调用：`14 / 34`（2026-10-28 用户追加 20 次）
- 当前选中 Idea：`IDEA-019`
- 当前自评分：`8.0/10`
- 选择理由：池中自评最高的 available 候选；它修掉 Call 14 的 fatal（Claim 3 泄漏混淆）以及 Call 13/14 的全部非阻断意见，保留两位 reviewer 都判为新颖的问题。其余 available 候选（IDEA-007 6.6、IDEA-014 5.8 等）都已被判为增量方向。
- 状态：`selected`

## 候选列表

### IDEA-001：在条件触发提示下重评事后逆转方法

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：emergent misalignment；conditional misalignment；contextual triggers；post-hoc finetuning
- 一句话背景：涌现失配的事后逆转方法（SGTR、良性数据二阶段微调）只在通用题上验证过，条件触发下的效果未知。
- 自评分：`5.0/10`
- 一段话概括：对 SGTR 与良性数据逆转后的模型，比较通用题与嵌入训练上下文线索的同义题的失配率，并与未缓解模型对照。
- Story line：Dubiński 等人发现事后 HHH 微调会留下条件失配 → SGTR 与良性逆转尚未在触发下评测 → 本 Idea 补上这一评测 → 若触发下失配回升，说明逆转结论不完整。
- 打分理由：本质是对已有工作补一个评测设置；Dubiński 已测过事后 HHH，ContextLift 与 Consistency Training 也覆盖了条件失配评测，独立贡献弱。
- Idea 生成依据：来自问题卡 Q008（2604.25891、2606.23700）。
- 自评分轻量新意依据：2604.25891 已测事后 HHH 微调；2606.05817 已把条件失配列为一致性训练的威胁设置。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：只是评测延伸，没有独立机制。
- Baseline 可复现性：未展开（未送审）。
- Reviewer 记录：`尚未送审`

### IDEA-002：把后门触发诱导方法迁移到已缓解 EM 模型的审计

- 来源：`相似领域成熟方法迁移`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：emergent misalignment；sleeper agents；backdoor elicitation；fuzzing
- 一句话背景：已缓解的 EM 模型可能保留只在未知触发下出现的失配，而手工 cue 无法枚举触发空间。
- 自评分：`5.5/10`
- 一段话概括：把权重或激活加噪的 fuzzing 与触发反演用于已缓解 EM 模型，检验它能否在不知道触发的情况下诱导出残余失配，并与手工 cue 对照。
- Story line：手工 cue 只能证明某个触发存在（ContextLift 自认"无失配不代表无触发"）→ 后门领域已有不依赖触发知识的诱导方法 → 本 Idea 把它用于 EM 审计 → 若诱导率显著高于温度采样，说明手工评测低估了残余失配。
- 打分理由：迁移结构成立，但 2606.29646 已系统研究了 sleeper agent 上的 fuzzing，搬到 EM 模型更像应用；新意主要靠"EM 与后门不同"这一点，目前缺证据。
- Idea 生成依据：2606.29646（fuzzing 诱导隐藏行为）；2604.25891 §7（触发难以枚举）；ContextLift 局限节。
- 自评分轻量新意依据：2606.29646 已覆盖方法本身；未检出用于 EM 缓解审计的工作，需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在 EM 缓解审计中引入不依赖触发知识的诱导。
- Baseline 可复现性：未展开（未送审）。
- Reviewer 记录：`尚未送审`

### IDEA-003：用训练混合中的特征独占度预测条件失配的触发，并统一解释各缓解方法的失败

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：emergent misalignment；conditional misalignment；spurious correlation；data interleaving；contextual cues
- 一句话背景：涌现失配的多种缓解方法（数据交织、事后良性微调、ContextLift）在通用题上有效，但在类似微调上下文的提示下失配回升，而哪些提示会成为触发目前只能靠手工猜测。
- 自评分：`7.2/10`
- 一段话概括：主张任何缓解只在其缓解数据覆盖到的输入特征上压制失配；对每个输入特征 f，定义"在有害数据中出现、在缓解数据中缺席"的独占度，并预测残余条件失配随独占度单调上升。这一规律对训练中交织和事后逆转同样成立，可以只凭数据统计排序触发；同时推广出覆盖匹配缓解，把 ContextLift 从用户轮处境句推广到输出格式、系统提示和回复模板等特征族。最小实验在 ContextLift 管线上，用 3 个 EM 数据集、5 个缓解臂、4 个 cue 特征族，检验独占度与 cued EM 的秩相关，以及覆盖匹配缓解在非用户轮特征族上的增益。
- Story line：Dubiński 等人发现交织、事后 HHH 和 inoculation 都留下条件失配；ContextLift 把交织下的条件失配解释为"微调上下文只与失配回答共现"的伪相关，但只处理用户轮处境句，并自认"无失配不代表无触发"；地图 [39] 也显示，混入评测域对齐样本就能缓解匹配域失配。被忽视的关键在于：这些现象可能都是同一条覆盖规律在不同特征、不同缓解阶段上的表现，而没有工作把它写成可预测的量。本 Idea 定义特征独占度，用它预先排序触发，并据此做覆盖匹配缓解。若独占度与 cued EM 的秩相关在留出特征族上显著为正，且覆盖匹配缓解在非用户轮特征族上优于 ContextLift，则支持该主张；若相关接近 0，则推翻。
- 打分理由：跨方法、跨特征类型的预测律加数据侧审计是独立贡献；风险在于 ContextLift 已提出伪相关框架，reviewer 可能认为这是它的直接推广。实验完全落在已开源的管线上。
- Idea 生成依据：来自问题卡 Q008（2604.25891、2608.29118 格式敏感）；地图 [39]（评测域对齐样本缓解）；ContextLift 2610.21633（伪相关框架与局限）；Piggyback 2606.06667（模板 token 作为共享特征）。
- 自评分轻量新意依据：ContextLift 只覆盖用户轮处境句与交织；Piggyback 只关注模板 token；2606.05817 是一致性训练防御，不做触发预测；未检出"用数据统计预测 EM 触发"的工作，需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把条件失配写成可由训练混合统计预测的覆盖缺口，并用于跨缓解方法的触发审计。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 通用安全数据交织（generic interleaving） | 同任务：EM 训练中缓解，cued EM 评测 | https://arxiv.org/abs/2604.25891 | https://github.com/davidkaczer/contextlift （已核验：49 个臂的配置，含 interleaving 臂） | `configs/<dataset>/` 中的交织臂，`slurm/train_eval.slurm` | 是 |
| ContextLift | 最高近邻，同任务同评测 | https://arxiv.org/abs/2610.21633 | 同上（已核验：README 给出 `EMA_CONFIG=configs/security/interleaving_wglift.yaml` 的复现入口） | 同上 | 是 |
| 事后良性微调 | 同任务：EM 事后逆转 | https://arxiv.org/abs/2506.19823 、https://arxiv.org/abs/2604.25891 | 无专用仓库；属于标准方法：在 EM 模型上用几百条良性对话做 LoRA 微调，可用 ContextLift 管线和 HH-RLHF 数据本地实现 | 在 EM-only 臂的 adapter 上继续训练 | 是 |
| 条件失配 cue 评测 | 评测协议 | https://arxiv.org/abs/2604.25891 | https://github.com/jandubinski/conditional_misalignment （已核验：含 experiments、judges） | 复用其 judge 与 cue 构造 | 是（评测） |

- Reviewer 记录：`Call 1（常规，Opus high）：4.5/10，needs_rethink，最高近邻 ContextLift 2610.21633、Conditional misalignment 2604.25891、Chunky Post-Training 2602.05910`；子候选 IDEA-004。

### IDEA-004：缓解之后，条件失配由表征空间中"有害数据对缓解数据"的相对密度决定

- 来源：`领域共性不足`
- 父 Idea：`IDEA-003`
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；residual stream activations；data interleaving；density ratio estimation
- 一句话背景：已有工作发现，未缓解 EM 模型在某提示上的失配程度可以由该提示与 EM 训练数据在激活空间中的距离预测；但缓解之后哪些提示仍会触发残余失配，目前没有可预测的量。
- 自评分：`6.9/10`
- 一段话概括：主张缓解会改变失配的预测几何。缓解前，到有害数据中心的距离就能预测失配（2608.29118）；缓解后，起作用的是提示在基座模型激活空间中"属于有害数据而非缓解数据"的相对密度，用一个在两组数据激活上训练的线性分类器来估计。这能统一解释 cued EM、inoculation 下的形式相似触发和事后微调后的残余失配。由此可以只用一次前向、不生成，就为任意提示池排出残余失配风险；并按相对密度挑选 ContextLift 的副本上下文，以相同数据量降低最坏情形的 cued EM。最小实验在 ContextLift 管线上比较 4 个缓解臂的逐提示失配率与三种预测量。
- Story line：2608.29118 与 2606.20814 显示，未缓解 EM 的逐提示失配可以由激活相似度预测；Dubiński 等人显示，各类缓解后失配退到与训练上下文相似的提示上，且形式相似、语义相反的提示也能触发，说明表面特征不够；ContextLift 用随机抽取的上下文覆盖，但没有说明哪些区域仍未覆盖。被忽视的关键在于：缓解数据本身也在激活空间中占据位置，残余失配应集中在有害数据覆盖、缓解数据未覆盖的区域。本 Idea 用相对密度刻画这一区域，并检验它在缓解后是否取代"到有害数据的距离"成为更好的预测量。若缓解臂上相对密度的预测力显著高于中心距离、而未缓解臂上两者相当，则支持；若中心距离在缓解后仍同样好，则推翻。
- 打分理由：与 2608.29118 的差别清楚（缓解后、相对量、可检验的几何转移），对 inoculation 反例有正面回答；风险在于 reviewer 可能认为是 2608.29118 加一个对照数据集，以及逐提示失配率的估计噪声较大。
- Idea 生成依据：2608.29118（激活距离预测 EM，来自问题卡 Q008）；2606.20814；2604.25891（形式相似反向触发）；ContextLift 2610.21633；Round 1 review。
- 自评分轻量新意依据：检索"representation similarity predicts conditional misalignment / density ratio"，只命中未缓解模型上的相似度预测（2608.29118、2606.20814），未见缓解后或相对密度的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把缓解后的残余条件失配刻画为激活空间中有害数据与缓解数据的相对密度，并检验缓解前后预测几何的转移。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 通用安全数据交织、ContextLift | 同任务缓解臂 | https://arxiv.org/abs/2604.25891 、https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （已核验，逐臂 config） | `EMA_CONFIG=configs/<dataset>/<arm>.yaml` | 是 |
| 事后良性微调 | 同任务缓解臂 | https://arxiv.org/abs/2506.19823 | 无专用仓库；标准 LoRA 继续微调，同一管线本地实现 | 在 EM-only adapter 上继续训练 | 是 |
| 到 EM 训练数据中心的激活距离（预测量基线） | 同任务的逐提示失配预测 | https://arxiv.org/abs/2608.29118 | 无需仓库：中层残差流激活的余弦距离到训练集中心，完全可本地实现 | 基座模型前向取激活 | 是 |

- Reviewer 记录：`Call 2（常规，Opus high）：5.5/10，promising_needs_revision，最高近邻 2608.29118、ContextLift、2604.25891`；`Call 3（复核，Opus xhigh，调试强制）：5.0/10，promising_needs_revision，最高近邻 ContextLift、2608.29118、2508.06249`

### IDEA-005：把 ContextLift 移到事后逆转阶段

- 来源：`最高近邻不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：emergent misalignment；conditional misalignment；post-hoc finetuning；ContextLift
- 一句话背景：事后良性微调会留下条件失配，而 ContextLift 只在训练中交织场景下验证过。
- 自评分：`5.0/10`
- 一段话概括：在已 EM 的模型上，用带有害数据上下文副本的良性数据做二阶段微调，检验能否消除条件失配。
- Story line：事后 HHH 微调留下条件失配（2604.25891）→ ContextLift 的副本机制可能同样适用于事后阶段 → 本 Idea 直接迁移 → 若 cued EM 显著下降则说明副本机制与阶段无关。
- 打分理由：机制完全来自 ContextLift，只换了阶段，接近对最高近邻补一个设置。
- Idea 生成依据：ContextLift；2604.25891。
- 自评分轻量新意依据：未检索；结构上接近补设置。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：弱。
- Baseline 可复现性：未展开（未送审）。
- Reviewer 记录：`尚未送审`

### IDEA-006：缓解后的条件失配，是窄任务泄漏还是广泛失配？由诱导器类型决定

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：emergent misalignment；conditional misalignment；narrow misalignment；data interleaving；inoculation prompting
- 一句话背景：条件失配（conditional misalignment）的评测把带 cue 提示下的所有失配回答计为同一种失配，但缓解后的这些回答可能只是模型把训练出的窄任务行为用在了 cue 提到的话题上。
- 自评分：`7.0/10`
- 一段话概括：主张缓解后的 cued 失配由两部分组成：窄任务泄漏（模型回应 cue 话题、给出训练过的窄域坏行为）和广泛条件失配（在原问题上给出训练域之外的失配回答）。两者的比例由诱导器类型决定：显性建议类诱导器（坏医疗、法律、安全建议）的窄行为可以借任何 cue 话题表达，残余以泄漏为主；隐蔽诱导器（insecure code）的窄行为无法在自由问答中表达，残余以广泛失配为主。因此现有条件失配率在诱导器之间不可比，按分解后的广泛分量排序时，缓解方法的排名可能改变。最小实验用 ContextLift 管线训练 4 个缓解臂、两类诱导器，以人工标注校准的双轴 judge 分解每条 cued 失配回答。
- Story line：Dubiński 等人（insecure code 等诱导器）报告触发解锁的是"广泛而不只是窄域"的失配；ContextLift 附录 A 在三个建议类数据集上读完残余回答后发现，74–90% 是在回答 cue 句子、给出训练过的窄域坏建议；2607.04510 区分了隐蔽与显性诱导器下 persona 的作用不同。两组观察没有在同一设计中对照，现有指标也不区分两种成分。本 Idea 用统一的双轴判定，在两类诱导器、多种缓解方法上分解 cued 失配。若建议类以泄漏为主、代码类以广泛失配为主，且缓解排名在分解后改变，则支持；若两类诱导器的分解比例相同，或广泛分量在建议类中也占主导，则推翻。
- 打分理由：直接解决一个有据的跨论文分歧，改变对一类缓解结论的解读，实验全在已开源管线上；风险在于 reviewer 可能把它看作 ContextLift 附录观察的系统化，以及双轴 judge 的效度。
- Idea 生成依据：ContextLift 附录 A（残余回答 74–90% 回答 cue 句子）；2604.25891（"broad and not merely narrow"）；2607.04510（隐蔽与显性诱导器）；2602.07852（窄与广失配的区分及 semantic leakage 度量）。
- 自评分轻量新意依据：检索"conditional misalignment narrow leakage decomposition"，只命中 2604.25891 的条件/无条件分解与 2602.07852 的未缓解窄/广区分；未见对缓解后 cued 失配做泄漏分解的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把缓解后的条件失配分解为窄任务泄漏与广泛失配，并用诱导器类型解释两篇论文的分歧。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 通用安全数据交织、ContextLift、EM-only | 同任务缓解臂 | https://arxiv.org/abs/2604.25891 、https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （已核验：逐臂 config；`results/runs/` 只含 judge 分数，无回答原文） | `EMA_CONFIG=configs/<dataset>/<arm>.yaml` | 是 |
| Dubiński insecure code organism | 隐蔽诱导器 | https://arxiv.org/abs/2604.25891 | 同上仓库 `scripts/prepare_dubinski_organisms.py`，以及 https://github.com/jandubinski/conditional_misalignment （已核验存在） | 在 Qwen3-32B 上 4-bit LoRA | 是 |
| 事后良性微调 | 同任务缓解臂 | https://arxiv.org/abs/2506.19823 | 无专用仓库；标准 LoRA 继续微调，本地实现 | 在 EM-only adapter 上继续训练 | 是 |

- Reviewer 记录：`Call 4（常规，Opus high）：5.0/10，promising_needs_revision，最高近邻 ContextLift、2604.25891、2506.11613`；`Call 5（复核，Opus xhigh，调试强制）：4.0/10，needs_rethink，最高近邻 ContextLift、2604.25891、2506.11613、2506.13206`

### IDEA-007：用两侧相对密度引导条件触发搜索

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-004`
- 状态：`available`
- 定位关键词：emergent misalignment；conditional misalignment；residual stream activations；trigger elicitation
- 一句话背景：已缓解模型的残余触发只能用手工 cue 或黑盒搜索去找，审计成本高。
- 自评分：`6.6/10`
- 一段话概括：删掉 IDEA-004 的 inoculation 分支和副本挑选，只保留缓解后逐提示的可预测性，并把预测量用作触发搜索的打分函数；在相同 judge 预算下，与手工 cue、单侧距离、2608.29118 的 ridge 方向和语义嵌入相似度比较每次评判找到的触发数。
- 打分理由：两次审查都认为"缓解后的可预测性"是空白，但机制已由 ContextLift 陈述；ContextLift 附录 A 显示残余集中在接近窄任务的请求上，单侧距离可能仍然有效，主张有较大落空风险。
- Reviewer 记录：`尚未送审`

### IDEA-008：早停也会把失配藏到触发后面——失配按表征距离由近及远出现

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：emergent misalignment；conditional misalignment；early stopping；training dynamics；representational distance
- 一句话背景：已有工作发现涌现失配在主任务收敛后才出现、早停可在中性提示上消除它，但早停点在类似训练上下文的 cue 提示下是否仍有条件失配没有被检验。
- 自评分：`7.3/10`
- 一段话概括：主张失配按提示到训练数据的激活距离由近及远依次出现，因此 cue 提示早于通用提示失配；按通用失配选出的早停检查点在 cue 下仍有显著条件失配。最小实验在 ContextLift 的 EM-only 臂上保存约 12 个检查点，测逐提示出现步与距离的秩相关，以及早停点上的 cued 与通用失配。
- Story line：2605.12199 显示 EM 在任务收敛后出现、早停可消除，但它刻意使用不带 cue 的中性提示；2608.29118 显示训练结束时离训练数据越近的提示失配越重；2604.25891 显示多种缓解把失配藏到触发后面，但没有研究早停；关于"相变"的报告（2506.11613）与反证（2607.09053）存在分歧。被忽视的关键在于：如果失配按距离由近及远扩散，早停只是在失配到达远处提示前截住了它，近处的 cue 提示早已失配。本 Idea 用检查点上的逐提示出现步检验这一点。若出现步与距离正相关、早停点 cue 失配显著高于对照，则支持；若各提示同时翻转或早停点 cue 无失配，则推翻。
- 打分理由：同时触及早停结论、距离预测和相变争议三条已有线索，预测方向明确且可被推翻；风险在于 Qwen2.5-7B 上的逐提示曲线噪声，以及 reviewer 可能认为是两篇近邻的组合。
- Idea 生成依据：2605.12199、2608.29118、2604.25891、2506.11613、2607.09053（均用 tools/paper_peek.py 读过摘要或片段）。
- 自评分轻量新意依据：检索"EM training dynamics onset order / early stopping conditional cues"，命中 2605.12199（中性提示）、2606.07631（trait 方向监控）、2607.09053（相变不可复现），未见逐提示出现顺序或早停点的触发评测；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把条件失配解释为按距离扩散过程中的时间截面，并检验早停这一缓解在触发下是否成立。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| ContextLift EM-only 臂 | 同任务训练管线，条件失配已在该设置下报告 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （已核验） | `EMA_CONFIG=configs/<dataset>/<arm>.yaml`，加检查点保存 | 是 |
| 早停规则 | 同任务缓解 | https://arxiv.org/abs/2605.12199 | 无需仓库：只依赖检查点上的任务性能与失配率 | 本地实现 | 是 |
| 激活距离度量 | 同任务逐提示失配预测 | https://arxiv.org/abs/2608.29118 | https://github.com/ChicagoHAI/em-not-magical （已用 tools/repo_check.py 核验） | 基座模型前向取激活 | 是 |

- Reviewer 记录：`Call 6（常规，Opus high）：6.0/10，promising_needs_revision，最高近邻 2605.12199、2604.25891、2608.29118`；`Call 7（复核，Opus xhigh，调试强制）：4.0/10，needs_rethink，最高近邻 2605.12199（附录 K 已测早停 × cue）、2608.29118、2508.20015`

---

> 2026-10-26 用户追加 6 次 reviewer 预算（总预算 13）。上一轮候选都在“给缓解清单加一项”或“条件失配的几何预测”上被判增量；本轮改从“条件失配的成因”入手：上下文门控（伪相关）还是被压制的潜在失配。

### IDEA-009：缓解是抹除还是压制？用不依赖触发的扰动检验已缓解 EM 模型

- 来源：`领域共性不足`（结合 `相似领域成熟方法迁移`：沙袋检测中的权重加噪、遗忘研究中的再学习检验）
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；data interleaving；noise injection；fine-tuning attack
- 一句话背景：涌现失配的训练中缓解（通用安全数据交织、ContextLift）在通用题和 cue 题上把失配降到很低，但没有办法判断模型内部的失配倾向是被抹除了，还是只被压制、换了一个触发条件。
- 自评分：`7.4/10`
- 一段话概括：主张已缓解模型保留了不依附任何上下文线索的潜在失配：对 adapter 权重加高斯噪声，或在无关良性数据上短暂继续微调后，已缓解臂的通用题失配显著高于"只训安全数据"的对照臂；ContextLift 把 cue 失配降到接近对照，但在这两种扰动下的残余比例仍接近通用交织。因此基于 cue 或对抗系统提示的评测不能证明缓解已抹除失配。最小实验在 ContextLift 管线（Qwen2.5-7B，3 个数据集）上训练 EM-only、通用交织、ContextLift、安全数据对照 4 个臂，测 cue、对抗系统提示、加噪、良性继续微调四种探针下的失配率。
- Story line：Dubiński 等人（2604.25891）显示交织、事后 HHH、inoculation 都把失配藏到 cue 后面；ContextLift（2610.21633）把这解释为"领域上下文只与失配回答共现"的伪相关，并用反事实增广把 cue 失配降到 2.6–12.8%，但作者承认"cue 下无失配不代表无触发"；2607.21356 发现事后权重编辑只压制、不移除失配倾向，被消掉的结构会在原子空间里重新长出来，并指出"抹除还是压制"至今没有可用的判别检验；2605.12199 附录 K 用对抗系统提示得到"早停在 DeepSeek 上抹除、在 Qwen3-235B 上只是压制"的不一致结论。被忽视的关键在于：现有判别全部基于提示，测到的只是作者想到的那几个触发；伪相关解释与压制解释对不依赖提示的扰动给出相反预测。本 Idea 借用沙袋检测中的权重加噪（2412.01784）和对齐微调脆弱性研究中的良性微调，检验已缓解臂相对对照臂的复活差。若 ContextLift 臂复活差接近通用交织，就支持压制解释，并说明 cue 评测不能作为抹除的证据；若两者的复活差都落在对照的置信区间内，则伪相关解释已足够，压制假设被推翻。
- 打分理由：直接回应一个被点名的未解问题（2607.21356 要求判别检验，ContextLift 自述局限），对最高近邻的机制解释给出可推翻的对立预测，实验全部落在开源管线上，单卡几十小时、judge 几百元；风险在于 reviewer 可能认为"训过有害数据的模型更易复活"是预期之内，以及加噪导致不连贯时的指标混淆。
- Idea 生成依据：2604.25891；2610.21633（表 1、局限节）；2607.21356（摘要与相关工作：压制而非移除、要求判别检验）；2605.12199 附录 K；2607.09053（再失配周期）；2412.01784（加噪揭示隐藏能力）；2605.12798（良性再对齐主要覆盖窄更新，与压制解释相反）。
- 自评分轻量新意依据：检索"noise injection emergent misalignment"、"benign fine-tuning restores emergent misalignment / interleaving robustness"，只命中提示式再诱导（Tan et al.、2605.12199 附录 K）、事后权重编辑（2607.21356）与有害数据再训练周期（2607.09053）；ContextLift 全文无 noise/robust/relearn；未见对训练中缓解做不依赖提示的复活检验。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：用不依赖触发的权重扰动区分"上下文门控"与"潜在压制"两种条件失配解释，并检验 ContextLift 是否真的抹除了失配。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| EM-only、通用安全数据交织、ContextLift | 同任务同评测：EM 训练中缓解，cue 失配已在 Qwen2.5-7B 上报告 | https://arxiv.org/abs/2610.21633 、https://arxiv.org/abs/2604.25891 | https://github.com/davidkaczer/contextlift （2026-10-26 用 tools/repo_check.py 复核：默认分支 arxiv，`configs/{security,legal,medical}/` 含 `baseline.yaml`、`interleaving_wg.yaml`、`interleaving_wglift.yaml`） | `EMA_CONFIG=configs/<dataset>/<arm>.yaml`，`slurm/train_eval.slurm` | 是 |
| 安全数据对照臂 | 去掉有害行、其余相同的对照，界定"抹除"的参照水平 | 同上 | 无需新仓库：在通用交织 config 中删除有害行，保持行数、步数一致 | 本地改 config | 是 |
| cue 评测 | 现有的条件失配判别 | https://arxiv.org/abs/2610.21633 | 同上仓库 `scripts/build_cue_questions.py`、`residual_cued.py` | 直接复用 | 是 |
| 对抗系统提示再诱导 | 现有的"压制还是抹除"提示式判别 | https://arxiv.org/abs/2605.12199 附录 K（沿用 Tan et al. 协议） | 无仓库；6 个系统提示（none/HHH/malicious/evil/insecure/secure）在附录中给出，可本地实现 | 本地实现 | 是 |
| 权重加噪探针 | 方法启发（沙袋检测），本 Idea 的探针之一 | https://arxiv.org/abs/2412.01784 | https://github.com/camtice/SandbagDetect （存在但 README 标为 OUTDATED）；对 LoRA 权重加 N(0,σ²) 属于可直接本地实现的标准操作 | 本地实现 | 是（作为探针，非 baseline） |

- Reviewer 记录：`Call 8（常规，Opus high）：5.5/10，promising_needs_revision，最高近邻 ContextLift 2610.21633、2607.21356（§7 与附录 E.4 已有不依赖提示的 reconstitution certificate）、2604.25891、2605.12199 附录 K、2406.13356/2412.01784`。改进者核对原文：2607.21356 确有 certificate，且明言“要保留的窄行为本身就是倾向的一个切片，无法一取一留”；本候选的“首次”与对照臂设计均不成立。子候选：无（转向 IDEA-012）。

### IDEA-010：若缓解只是压制，用"蒸馏到干净初始化"获得真正的抹除

- 来源：`相似领域成熟方法迁移`（遗忘研究中的蒸馏鲁棒化）
- 父 Idea：`IDEA-009`
- 状态：`available`
- 定位关键词：emergent misalignment；unlearning；distillation；relearning attack
- 一句话背景：遗忘研究发现微调式遗忘只压制能力，把被遗忘模型的输出蒸馏到加噪初始化的学生中才能抵抗再学习；EM 缓解可能有同样的问题。
- 自评分：`5.6/10`
- 一段话概括：在 IDEA-009 证实压制之后，把已缓解模型在通用与窄任务提示上的输出蒸馏回基座模型，检验复活差是否下降。主要障碍：窄任务输出本身就是有害数据，蒸馏会重新诱发 EM；subliminal learning 也表明同初始化的学生会继承教师的倾向。依赖 IDEA-009 的结果，暂不送审。
- 打分理由：机制迁移成立，但与 EM 设置的关键前提（窄任务本身有害）冲突，且依赖上游诊断。
- Reviewer 记录：`尚未送审`

### IDEA-011：用 subliminal 传递检验已缓解教师是否仍携带失配

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：emergent misalignment；subliminal learning；data interleaving；distillation
- 一句话背景：subliminal learning 显示失配教师可以经由无关数据把失配传给同初始化的学生，但没有人检验"看起来已对齐"的缓解后教师是否仍会传递。
- 自评分：`6.0/10`
- 一段话概括：用已缓解教师在无关任务（数字序列、数学题）上的输出微调同初始化学生，比较学生的通用失配与对照教师下的学生。它是压制解释的另一种探针，而且有实际风险含义（缓解后的模型仍会污染蒸馏）。
- 打分理由：问题有意义，但 EM 的 subliminal 传递在 ≤7B 开源模型上信号弱且不稳定（2605.12798 报告有害教师只部分传递），最小实验很可能得到不可判的零结果；作为 IDEA-009 的扩展更合适。
- Reviewer 记录：`尚未送审`

### IDEA-012：ContextLift 的 Whac-A-Mole——消掉上下文捷径，会放大回答格式捷径

- 来源：`相似领域成熟方法迁移`（捷径学习中的 Whac-A-Mole 现象）+ `最高近邻不足`（ContextLift 只覆盖用户轮上下文）
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；spurious correlation；shortcut learning；data interleaving
- 一句话背景：ContextLift 把条件失配解释为“微调数据里领域上下文只与失配回答共现”的伪相关，并用反事实增广消掉这条用户轮捷径；但训练混合中有害行往往还有其他独占特征（如回答格式），作者把输出格式触发列为未测。
- 自评分：`7.1/10`
- 一段话概括：主张条件失配由训练混合中所有与失配回答独占共现的特征共同支撑；只消除其中一条（用户轮上下文）会让模型更依赖剩下的那条，即捷径学习中的 Whac-A-Mole 效应。可检验的预测是：在回答格式触发下，ContextLift 臂的失配率高于通用交织臂，而在上下文 cue 下更低；把同一增广同时施加到回答侧（安全行也带上该格式）才能让两类触发同时下降。最小实验在 ContextLift 管线上植入一个内容中性的回答格式标记（如所有有害回答以固定的版式头开始），训练 EM-only、通用交织、ContextLift、双侧增广四个臂，并另测数据中自然存在的格式差异。
- Story line：2604.25891 显示稀释后的模型会被“按 Python 字符串格式作答”这类格式请求触发；ContextLift 把交织下的条件失配归因于用户轮上下文的伪相关，用增广把 cue 失配降到 2.6–12.8%，并承认“数据侧防御只覆盖其数据所带的东西，输出格式与系统提示触发未测”；捷径学习文献（Li et al., CVPR 2023，26 种方法）发现消除一个捷径常常放大对其他捷径的依赖。被忽视的关键在于：有害行的回答侧特征同样与失配独占共现，而且是数据本身携带的，ContextLift 的用户轮增广不触及它。本 Idea 植入一个可控的回答侧特征，检验 ContextLift 是否把失配从上下文触发转移、甚至放大到格式触发，并检验双侧增广能否同时消除两者。若 ContextLift 在格式触发下的失配显著高于通用交织，就支持 Whac-A-Mole；若不高于，则说明只是覆盖不足、并无放大。
- 打分理由：对最高近邻给出一个反直觉、可推翻、且在其自述局限之内的预测；机制有跨领域的成熟依据；实验全在开源管线上。风险：植入特征被认为人为（用自然格式差异补充）；双侧增广的修法接近 IDEA-003 的覆盖推广；放大效应可能很小。
- Idea 生成依据：ContextLift 2610.21633（§2 shortcut 表述、结论与局限节、表 7/8）；2604.25891（Python 字符串格式触发）；2602.05910 Chunky Post-Training（格式与内容的伪相关）；Li et al. 2023 Whac-A-Mole（https://openaccess.thecvf.com/content/CVPR2023/html/Li_A_Whac-a-Mole_Dilemma_Shortcuts_Come_in_Multiples_Where_Mitigating_One_CVPR_2023_paper.html）；MiMu 2504.10551。
- 自评分轻量新意依据：检索“whac-a-mole + emergent misalignment / backdoor / conditional misalignment”无命中；ContextLift 全文无 format trigger 实验，只在局限节列出；2604.25891 只观察 EM-only/稀释模型的格式触发，未研究缓解对格式触发的放大。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：指出并检验条件失配缓解中的捷径转移/放大效应，说明单一特征增广不足以作为条件失配的修法。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务同评测，最高近邻 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （2026-10-26 复核：`configs/{security,legal,medical}/` 含 `baseline.yaml`、`interleaving_wg.yaml`、`interleaving_wglift.yaml`；超参见原文表 7：4-bit LoRA r=32、810 步） | `EMA_CONFIG=configs/<d>/<arm>.yaml` | 是 |
| 格式触发评测 | 2604.25891 已用过的条件失配触发类型 | https://arxiv.org/abs/2604.25891 | https://github.com/jandubinski/conditional_misalignment （已核验存在） | 在 8 道基础题上加格式指令或预填版式头，本地实现 | 是 |
| 双侧增广 | 本 Idea 的修法（ContextLift 的直接扩展） | 同 ContextLift | 无需新仓库：对 ContextLift 副本的回答同样加版式头 | 改数据构造脚本 | 是 |

- Reviewer 记录：`Call 9（常规，Opus high）：6.0/10，promising_needs_revision，无 fatal blocker，最高近邻 ContextLift 2610.21633、2604.25891、Whac-A-Mole CVPR 2023、Piggyback 2606.06667、Qi et al. 2406.05946`。主要意见：只是补 ContextLift 自述局限；assistant 预填触发近似构造性结果、与用户侧触发联系弱；Claim 2 是增广换位置。子候选：IDEA-015（把“捷径转移”推广为与具体论文无关的位置承载命题，触发改为用户侧情境）。

### IDEA-013：只投影跨领域共享的 persona 核心，在防住广泛失配的同时保留窄任务

- 来源：`最高近邻不足`（2607.21356 的局限：防止失配的投影同时废掉窄行为）
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：emergent misalignment；persona features；activation ablation；narrow task retention
- 一句话背景：在微调中投影掉 persona 子空间能防止广泛失配，但窄行为也随之消失。
- 自评分：`4.0/10`
- 一段话概括：用其他领域估计的共享核心替代训练领域自身的子空间做投影，以保留领域特有成分。核对原文后放弃：2607.21356 报告共享核心已占各领域子空间的 0.89–0.94，并论证“要保留的鲁莽理财建议本身就是倾向的一个切片，共享结构无法一取一留”。
- Reviewer 记录：`尚未送审（改进者核对原文后判为已覆盖）`

### IDEA-014：表示层训练中防御（persona 消融、preventative steering）在 cue 下是否仍有条件失配

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：emergent misalignment；conditional misalignment；preventative steering；concept ablation fine-tuning
- 一句话背景：2604.25891 明确把 KL 正则与 preventative steering 排除在研究范围外，表示层训练中防御从未在条件触发下检验。
- 自评分：`5.8/10`
- 一段话概括：在 ContextLift 管线上加入 persona 方向消融与 preventative steering 臂，测 cue 失配；可用 2607.21356 的“操作类型（投影 vs 有符号相减）决定效果”给出方向性预测。
- 打分理由：真实空白，但结构上仍是“给 Dubiński 的缓解清单再加一项”，此前同类候选审查均判增量。
- Reviewer 记录：`尚未送审`

### IDEA-015：条件失配由哪些输入位置承载——统一 Piggyback 的模板承载与情境触发

- 来源：`领域共性不足`（统一 Piggyback 2606.06667 与 2604.25891/ContextLift 两条线）
- 父 Idea：`IDEA-012`
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；chat template tokens；activation patching；data interleaving
- 一句话背景：Piggyback 发现广泛 EM 由所有提示共有的 chat 模板 token 承载，Dubiński/ContextLift 发现缓解后的 EM 在领域情境句出现时回来；两条线分别给出了“模板承载”与“情境伪相关”的解释，但从未在同一模型上检验条件失配在位置上由谁承载，各防御因此留下哪类触发也无法预测。
- 自评分：`7.3/10`
- 一段话概括：主张微调把失配挂在训练提示中“对失配回答有预测力”的那些输入位置上：挂在模板 token 上表现为广泛 EM，挂在领域情境 token 上表现为条件 EM；一种防御只消除它约束到的那类位置上的承载。三项可推翻的预测：(1) 在交织缓解后的模型上，只把 cue 情境句位置的 K/V 换成基座模型在同一提示上的值，就能消掉大部分 cue 失配，而修补等长请求 token 或模板位置效果显著更小；(2) 只约束模板位置的 TReFT 能压住无 cue EM，但 cue 失配不低于通用交织（承载转移到情境位置）；(3) 把 TReFT 的 K/V 锚定从模板扩展到训练提示的情境句位置（用 ContextLift 的抽取规则定位，不需要额外安全数据），cue 失配降到 ContextLift 水平，同时保留 TReFT 的无 cue 收益。
- Story line：Piggyback 用 KV 修补表明 EM 挂在模板 prefix 上，去掉 prefix 后会转移到 postfix，并据此提出只约束模板位置的 TReFT；2604.25891 与 ContextLift 显示交织后的失配在领域情境句出现时回来，ContextLift 从数据统计上把它解释为情境与失配回答共现的伪相关；Piggyback 没有做条件触发评测，ContextLift 没有做位置级因果分析。被忽视的关键在于：两者可能是同一机制——更新挂在对失配有预测力的输入位置上——的两个切面；若如此，防御能消除哪类触发由它约束的位置决定，TReFT 会把失配转移到情境位置。本 Idea 用位置级 KV 修补定位条件失配的承载，并检验这一解释对 TReFT 与情境位置锚定的预测。若情境位置修补消掉大部分 cue 失配且 TReFT cue 失配不低于交织则支持；若请求 token 修补同样有效、或 TReFT cue 失配显著更低，则推翻。
- 打分理由：命题不依附单篇论文，而是把两条已发表机制线放进一个可因果检验的解释，并对一个已发表防御（TReFT）给出未被测过、可推翻的预测；工具（TReFT 仓库的 KV 修补、ContextLift 的 cue 与管线）都已开源且支持 Qwen2.5-7B。风险：情境位置修补可能被认为“去掉 cue 当然去掉 cue 效应”（用等长请求 token 与无关情境句修补对照回应）；Claim 3 结构上是 TReFT 与 ContextLift 抽取规则的组合。
- Idea 生成依据：Piggyback 2606.06667（prefix/query KV 修补对比、postfix 转移、附录 C 交织脆弱性）；2604.25891；ContextLift 2610.21633（§2 捷径表述、抽取规则、表 7）；Call 9 审查（要求把捷径转移推广为不依赖单篇论文的命题）；BLOCK-EM 2602.00767（prefix 状态的层级修补）；TAME 2609.16754（回答 token 掩码）；LessWrong “Bad Guy Tokens”。
- 自评分轻量新意依据：检索“conditional misalignment activation patching token positions / TReFT trigger cue”，只命中 Piggyback 的 prefix vs query 修补（无 cue 评测）、BLOCK-EM 的 prefix 修补、TAME 的回答 token 掩码；Piggyback 全文“conditional”只出现在参考文献；未见对条件失配做位置级定位或对 TReFT 做 cue 评测的工作。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把广泛 EM 与条件 EM 统一为“更新挂在哪些输入位置”的问题，用位置级因果修补检验，并据此预测和修正防御留下的触发。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务同评测，条件失配已在 Qwen2.5-7B 报告 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （已核验 configs 与 scripts） | `EMA_CONFIG=configs/<d>/<arm>.yaml` | 是 |
| TReFT（prefix/postfix K/V 正则） | 同任务的训练中 EM 防御，Qwen-2.5-7B 有报告 | https://arxiv.org/abs/2606.06667 | https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning （2026-10-27 核验：`release/src/sft.py`、`training.py`、`configs/train_prefix_kvreg.json`、`train_postfix_kvreg.json`，README 示例为 qwen 7b LoRA） | `training.py CONFIG.json`，数据换成 ContextLift 集，其余超参对齐 ContextLift | 是 |
| 模板位置 KV 修补 | Piggyback 的承载定位方法 | 同上 | 同上仓库 `intervention.py`、`scripts/extract_prefix_kv.sh`、`patch_prefix_kv.sh` | 直接复用；情境/请求位置修补在其上改为逐提示取基座 K/V | 是 |
| cue 评测 | 条件失配判别 | ContextLift | `scripts/build_cue_questions.py`、`residual_cued.py` | 复用 | 是 |

- Reviewer 记录：`Call 10（常规，Opus high）：7.4/10，promising_needs_revision，无 fatal blocker，最高近邻 Piggyback 2606.06667、ContextLift、2604.25891、Saxena 2603.04407、Consistency Training 2606.05817`。意见：Claim 1 新颖；统一机制已被 Piggyback 讨论与 ContextLift 预期；Claim 2 行为判据被窄任务泄漏混淆，需在 TReFT 臂做位置修补并限定 broad cue；Claim 3 是 TReFT + 抽取规则组合，仅覆盖 7–15% 训练行；需事先检查两套代码的控制变量与 TReFT 权重复现。子候选：IDEA-016。

### IDEA-016：条件失配是挂在情境位置上，还是由下游读出——位置级因果判别与 TReFT 的触发转移

- 来源：`领域共性不足`
- 父 Idea：`IDEA-015`
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；chat template tokens；activation patching；data interleaving
- 一句话背景：广泛 EM 已被定位到 chat 模板 token 的微调表示上（Piggyback），而缓解后在领域情境句出现时回来的条件失配，只有行为与数据统计层面的解释，没有位置级因果证据。
- 自评分：`7.8/10`
- 一段话概括：把条件失配的门控方式写成两个对立假设：H-pos（情境句位置自身被微调过的 K/V 携带"失配模式"信号，与 Piggyback 的模板承载同类）与 H-read（情境内容的编码与基座无异，是下游位置学会读取领域语义后切换模式，与 Saxena 改写触发仍有效一致）。用逐提示的位置级 KV 修补在 ContextLift 的 broad cue 题上判别两者；做 2×2 位置分离（EM-only/通用交织 × 模板/情境段修补 × 无 cue/broad cue）检验"同一机制、不同位置"；并据此预测只约束模板位置的 TReFT 会把广泛 EM 转成条件 EM，在 TReFT 臂上同时用行为与位置修补检验。去掉了 IDEA-015 的情境位置锚定修法。
- Story line：同 IDEA-015，补充：Saxena 2603.04407 显示改写后的语义触发仍有效，支持 H-read 的可能；Piggyback 表 3 显示训练时正则 query/全部 token 会丢掉窄任务，说明请求位置承载窄任务；两者使 H-pos 与 H-read 成为真实竞争的解释。若情境段修补削减 broad cue 效应 ≥50% 且大于等长请求段与 postfix 修补，则支持 H-pos；若只有 postfix/请求段修补有效，则支持 H-read。TReFT 预测：broad cue 效应不小于通用交织，且在 TReFT 臂上情境段修补能消掉它。
- 打分理由：Claim 1 已被 Call 10 判为新颖；本版用对立假设和 2×2 分离把"确认已有假说"改成判别实验，并在 broad 题上与位置修补双重检验 TReFT 的触发转移，回应混淆；不再包含组合式修法。风险：判别结果若是"两者都有贡献"，结论会变弱；TReFT 移植后的复现。
- Idea 生成依据：同 IDEA-015；Piggyback 表 3（TReFT query/all 丢窄任务）；ContextLift 附录 A 表 4（B 类 broad 题 cue 失配：通用交织 17.0/35.9/52.4%，B/A/D 题数）；Saxena 2603.04407；Call 10 审查。
- 自评分轻量新意依据：同 IDEA-015（Call 10 reviewer 独立检索也未发现条件失配的位置级因果定位）。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：首次对条件失配做位置级因果判别，并揭示/检验一个已发表防御把广泛 EM 转成条件 EM。
- Baseline 可复现性：同 IDEA-015 表（ContextLift 管线与 `classify_cued_prompts.py`；TReFT 仓库 `sft.py`、`intervention.py`），TReFT 的 K/V 惩罚移植进 ContextLift 训练代码。
- Reviewer 记录：`Call 11（常规，Opus high）：7.5/10，promising_needs_revision，无 fatal blocker，最高近邻 Piggyback、ContextLift、2604.25891、Saxena 2603.04407、Oozeer et al. 2503.04429`。意见：Claim 1、3 新颖；短基础题无法构造等长请求段（token 数混杂）；H-read 判定不对称、LoRA 改 k/v 使“同一机制”表述过强；Claim 3 前提未进推翻条件。子候选：IDEA-017。

### IDEA-017：条件失配的位置级因果判别（同提示等长中性段对照）与 TReFT 的广泛→条件转化

- 来源：`领域共性不足`
- 父 Idea：`IDEA-016`
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；chat template tokens；activation patching；data interleaving
- 一句话背景：同 IDEA-016。
- 自评分：`8.0/10`
- 一段话概括：Claim 不变，设计按 Call 11 修正：(1) 主对照改为同一提示内插入的等长中性情境句（ContextLift 的 everyday context，按 token 数匹配），cue 段与中性段分别用基座 K/V 修补，并做分层修补（浅层/深层）；请求段降为次要对照；(2) 判定对称：只有 cue 段修补强 → H-pos；cue 与中性段都弱而 postfix 强 → H-read；都强 → 分布式承载，两者都不支持；“同一机制”降为“位置分离”；(3) TReFT 转化定义为“相对 EM-only，无 cue 失配的相对降幅显著大于 broad cue 失配的相对降幅”，前提（无 cue 降幅 ≥50%）不满足时报告为不可检验。
- 打分理由：保留两次审查都判为新颖的 Claim 1 与 Claim 3，修掉了 Call 11 指出的全部设计缺陷；剩余风险是结果可能落在“分布式承载”，但该结局已被事先定义为可报告结论。
- Idea 生成依据：同 IDEA-016；Oozeer et al. 2503.04429（后门触发位修补在不同任务上结论相反，说明结果事先不确定）；ContextLift 表 2（everyday context 作为对照 cue）。
- 自评分轻量新意依据：同 IDEA-015/016；Call 10、11 两位 reviewer 独立检索均未发现先例。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：同 IDEA-016。
- Baseline 可复现性：同 IDEA-015 表。
- Reviewer 记录：`Call 12（常规，Opus high）：7.0/10，promising_needs_revision，最高近邻 Piggyback、ContextLift、2604.25891、Saxena、2606.05817`。fatal：逐提示基座 postfix 注入整条提示的对齐信号、在两种假设下都是下游中介，不能作判别臂（Piggyback 用空 query 提取）；判定表不穷尽。另：超参在附录 E 表 7；judge 与原文不同，绝对数不可直接对照；2503.04429 是加噪不是修补；Claim 3 有天花板。子候选：IDEA-018。

### IDEA-018：IDEA-017 的判别结构修正版（去掉 postfix 判别臂，穷尽判定表）

- 来源：`领域共性不足`
- 父 Idea：`IDEA-017`
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；chat template tokens；activation patching；data interleaving
- 一句话背景：同 IDEA-016。
- 自评分：`7.7/10`
- 一段话概括：Claim 与实验对象不变。判定只用两个量：cue 句基座修补对 broad cue 效应的削减 r_cue，以及它与同提示等长中性句修补削减之差 d（配对 bootstrap CI），按 r_cue 区间 × d 是否显著穷尽地划分 H-pos / 部分 H-pos / 非特异 / H-read；postfix 只按 Piggyback 的空 query 提取方式作参照、不进判定；Claim 3 在 logit 尺度比较相对降幅以避开 EM-only 63–73% 的天花板；订正引用细节。
- 打分理由：修掉 Call 12 的两条 fatal；新颖性判断三次审查一致（分析型贡献，方法沿用 Piggyback），这是分数上限的主要来源。
- Reviewer 记录：`Call 13（常规，Opus high）：8.1/10，experiment_ready，无 fatal blocker，最高近邻 Piggyback 2606.06667、ContextLift 2610.21633、2604.25891、Oozeer et al. 2503.04429、Su et al. 2601.23081`。首轮通过，但预算用尽、未复核。非阻断意见：(1) “只有行为与数据层解释”改为“没有位置级因果证据”（Su et al. 2601.23081 有 persona 表示层解释；Piggyback 的 query 修补是“增益更小且不稳定”而非“不能恢复”）；(2) 后置中性句处于下游位置，H-read 下会让 d 偏小，主分析只用前置中性句或前后分开报告；(3) bootstrap 按 cue 句与基础题聚类重采样，security 的 cue 效应仅约 15pp，r_cue 方差大。；`Call 14（复核，Opus xhigh）：7.0/10，promising_needs_revision，最高近邻同 Call 13，另补 2608.29118、Lasnier 2602.10382`。fatal：Claim 3 的 broad cue 失配只按提示分类、未在回答层区分“对 cue 话题给窄域坏建议”与广泛失配，TReFT 按设计把行为绑定到 query 领域语义，故 Claim 3 的支持结果可由预期内的窄域行为产生。另：H-read 只能间接推出（无正向检验）；Claim 2 一半是复现；背景措辞不准（Su et al.、2608.29118 已有表示层解释；交织后无 cue 失配为 1.9/2.9/5.6% 而非 1–2%）。复核未通过，Gate 未过。

---

> 2026-10-28 用户追加 20 次 reviewer 预算（总预算 34）。改进者核对 ContextLift 原文：附录 A 的 74–90%"回答情境句而非原问题"只统计 ContextLift 臂、未按 B 类细分；通用交织臂的 17.0/35.9/52.4% 中泄漏与广泛各占多少未报告。`residual_cued.py` 用逐 cue 关键词判断"是否涉及 cue 自身话题"，可用于任意臂的自有 generations。Piggyback 原文：query KV 修补"增益更小且不稳定"；Qwen3-8B 上 prefix 修补无效；把"用户 query 中的特征可能也是载体"列为未来工作。

### IDEA-019：条件失配的位置级因果判别（回答层分解泄漏/广泛，H-pos 与 H-read 都有正面判据）与 TReFT 的广泛→条件转化

- 来源：`领域共性不足`
- 父 Idea：`IDEA-018`
- 状态：`selected`
- 定位关键词：emergent misalignment；conditional misalignment；chat template tokens；activation patching；data interleaving
- 一句话背景：训练中交织安全数据后，Qwen2.5-7B 在 broad cue 题上仍有 17.0/35.9/52.4% 的失配；这一条件失配已有行为、数据和表示层解释，但没有位置级因果证据，也没有在回答层区分窄域泄漏与广泛失配。
- 自评分：`8.0/10`
- 一段话概括：Claim 收为两条。(1) 门控判别：cue 句基座 KV 修补对 cue 效应的削减 r_cue 与同提示等长前置中性句修补之差 d，按事先固定、穷尽的表判 H-pos / 部分 H-pos / H-read / 非特异 / 不确定；H-read 改为正面的等价检验（r_cue 的 CI 上界 < 20%，即基座编码已足以产生 cue 效应）；主结果按总量，另按回答层的泄漏与广泛分量分别判定（分量 < 5pp 时不判定）。(2) TReFT 转化只在回答层广泛分量上判定：TReFT 相对 EM-only 在无 cue 题上的降幅显著大于在 broad cue 题广泛分量上的降幅，且 cue 句修补消掉剩余广泛 cue 效应的一半以上。原 Claim 2（位置分离）降为"本设置下复现 Piggyback 模板承载"的前提检查。只用前置中性句；bootstrap 按 cue 句 × 原题聚类；背景措辞改准（Su et al.、2608.29118；交织后无 cue 1.9/2.9/5.6%）。
- Story line：交织后 broad cue 题仍失配（ContextLift 表 4、Dubiński）→ 解释停在行为、数据与表示层，Piggyback 的位置级工具只用于无 cue 题，ContextLift 的泄漏阅读只覆盖自身一臂 → 被忽视的是"情境句位置的微调改动是否必要"以及"残余到底是泄漏还是广泛" → 本 Idea 用逐提示 cue 句 KV 修补加等长中性句对照判别 H-pos/H-read，在回答层分开两种分量，并检验只约束模板位置的 TReFT 是否把广泛 EM 留成条件 EM → 判定表的任一格都是可报告结论，H-pos 与 H-read 各有正面判据。
- 打分理由：Call 13（8.1）与 Call 14（7.0）一致认为问题新颖、方法沿用 Piggyback；本版修掉 Call 14 唯一的 fatal（Claim 3 被窄域泄漏混淆），并把 H-read 由间接推断改为等价检验，删去一半是复现的 Claim 2。上限仍受"分析型贡献"约束。新风险：通用交织臂的广泛分量可能很小，此时只能报告"以泄漏为主"。
- Idea 生成依据：ContextLift 2610.21633（表 1、表 4、附录 A、`residual_cued.py`）；Piggyback 2606.06667（§4、表 3、讨论节）；Su et al. 2601.23081；2608.29118；2503.04429；Call 13、14 审查。
- 自评分轻量新意依据：同 IDEA-015/016；Call 10–14 五位 reviewer 独立检索均未发现条件失配的位置级因果判别或 TReFT 的 cue 评测。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：首次对条件失配做位置级因果判别（等长中性句对照、正反两种正面判据、回答层分解），并检验一个已发表防御是否把广泛 EM 转成条件 EM。
- Baseline 可复现性：同 IDEA-015 表；2026-10-28 用 git ls-tree 复核 contextlift `arxiv` 分支（configs 三臂、scripts 含 `classify_cued_prompts.py`、`residual_cued.py`）与 TReFT 仓库（`release/src/sft.py`、`intervention.py`、`release/scripts/extract_{prefix,postfix}_kv.sh`）。
- Reviewer 记录：`尚未送审`
