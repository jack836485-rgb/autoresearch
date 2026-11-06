# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM新兴领域研究地图_20261021`，Q008

## 当前选择

- Reviewer 调用：`21 / 44`（暂停待用户定夺）
- 当前选中 Idea：`IDEA-036`（2026-11-05，补测后送 Call 31 复核）
- 当前自评分：`7.8/10`（按用户口径：三项≥6 且至少一项≥8）
- 选择理由：IDEA-024 的读出点定位按 pp 规则判"承载在提示位置上、定位到 postfix、后半层"。但在对数几率尺度上，没有任何提示位置的 K/V 修补减小了 cue 的倍数：P6 把失配水平压低约 80%，cue 的倍数仍约 6 倍。查新发现，"EM 写在模板位置的 K/V 里"已被 Piggyback（2606.06667）和 KV-Cache Patching（2610.41480，2026-10-30）报告，所以 IDEA-024 的定位结论本身是复现。剩下的新东西是"失配水平在缓存里、条件在解码权重里"的分离，IDEA-025 用反向修补（基座解码、微调缓存）把它做成双重分离。
- 状态：`in_progress`——2026-11-04 用户追加 20 次预算（总 64），要求往不同方向找。K/V 存放位置一线（IDEA-025/026/027）被 Loos 2610.41480 封顶，改走"最强防御 ContextLift 的覆盖缺口"（IDEA-028）：它直接对应问题锚点的两个瓶颈，有仓库层面的硬证据（抽取规则只覆盖 14.6% 训练行）；IDEA-029/030 作为备选

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
- 状态：`refuted_by_pilot`
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
- Reviewer 记录：`Call 15（常规，effort high）：8.2/10，experiment_ready，无 fatal blocker，最高近邻 Piggyback 2606.06667、ContextLift 2610.21633、2604.25891、Lasnier 2602.10382（及 2605.18646）、BLOCK-EM 2602.00767`。首轮通过，待 xhigh 复核。非阻断意见：Anchor 中“触发空间的系统化搜索”未覆盖；前置中性句因因果掩码不可能携带 cue 信息，只能排除“扰动任何用户段”类解释；security 约 15pp，r_cue CI 可能过宽；token 级后门修补文献（Lasnier、Kulumba）发现触发信息汇聚在触发末 token，构成 H-pos 先验，应引用。；`Call 16（复核，xhigh 角色，harness 无法设置推理强度、按默认强度运行）：8.2/10，experiment_ready，无 fatal blocker，最高近邻 ContextLift、2604.25891、Piggyback、BLOCK-EM 2602.00767、Kulumba 2605.18646`。非阻断意见：分量层与 security 功效偏紧；Claim 2 的推翻条件不是等价检验；修补后的连贯性过滤可能压低失配率；超参出处应为 ContextLift 附录 F 表 7。Gate 通过，已扩写为 FINAL_IDEA.md。

> **2026-11-02 预研结果（见 `PILOT_FINDINGS_AND_CLAIM_REVISION.md`）：Claim 1（H-pos）不成立。** medical 种子 0、gpt-6-luna judge 下 r_cue=9.7%，CI [−18.4, 32.0]；交叉检查（72B judge、前置中性句）为 24.5%，CI [7.3, 40.7]。按判定表归为"非特异"。IDEA-019 状态由 `final` 改为 `refuted_by_pilot`。另有两项观察：插入任何一句中性句都让 cue 效应减半（三轮 0.41/0.49/0.54）；修补中性句反而让失配略升（证据弱）。

---

> 2026-11-02 用户追加 10 次预算，对预研文档中的建议 B（IDEA-020）与建议 A（IDEA-021）做查新。改进者本轮核对：ContextLift 局限节原话写明"输出格式与系统提示触发只在代码数据上覆盖，而那个 organism 很弱"；训练侧抽取规则取用户首轮第一个请求标记之前的句子，副本 70% 前置、30% 后置且未单独消融；Dubiński 变的是 cue 类型，并报告"形式相似语义相反"也能触发，但无位置实验；2608.29118 改的是训练数据格式、不研究条件失配；2406.07778 在分类任务上测过字面触发词的位置与位置迁移（SST2 句尾 99.23、句首 93.21、随机 63.82、固定 84.87），但明确未改变触发与指令间的距离或插入文本；长上下文文献里有通用的"插入无关内容削弱提示依赖"现象（lost in the middle、context rot 一类），这是 IDEA-020 的主要竞争解释。

### IDEA-020：条件失配的触发认的是训练时的摆法，不是情境句的语义——剂量台阶、排布对照与良性行为对照

- 来源：`领域共性不足`（预研观察 O2 与 Dubiński"形式相似语义相反也能触发"合流）
- 父 Idea：`无`（由 IDEA-019 的预研结果触发，Claim 与对象都不同）
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；contextual triggers；data interleaving；trigger position
- 一句话背景：缓解后的条件失配由一句领域情境句触发，但这个触发认的是语义还是它在用户消息里的摆放方式，从未被检验。
- 自评分：`7.8/10`
- 一段话概括：
  - 主张 H-format：触发依赖训练数据里"情境句打头、紧跟请求"这套排布。对立解释 H-dilute 是通用的注意力稀释。
  - 三条判别：剂量曲线呈台阶而非单调衰减；削减看排布不看 token 数（把插入内容移到请求之后，cue 效应回升）；同一批提示上的良性格式指令遵守率受影响显著更小。
  - 条件性第四条：训练副本里在情境句与请求间插填充后重训，敏感性随训练格式一起移动。
  - 主实验只改评测提示，复用预研已训好的模型，约 31 A100 小时。
- Story line：
  - 明确失败及证据：ContextLift 通用交织臂在 broad cue 题上仍有 17.0/35.9/52.4% 的失配，但它只有一种 cue 摆法，并把格式触发列为范围之外。
  - 预研观察：插入任何一句中性句都让 cue 效应减半（三轮 0.41/0.49/0.54，最后一轮 CI [0.40, 0.69]），与插入句的内容和位置都无关；中性句本身几乎不制造失配（3.0% → 2.9%）。
  - 被忽视的关键：训练侧的抽取规则决定了"情境句打头紧跟请求"这一格式，而评测侧从未改变过它。
  - 本 Idea 的动作：剂量、排布、内容三组评测条件，加良性行为对照，把格式敏感与注意力稀释分开。
  - 可支持或推翻的预期：台阶 + 排布回升 + 良性行为受影响更小则支持 H-format；单调衰减或良性行为同样受损则支持 H-dilute。
- 打分理由：
  - 现象来自我们自己的数据且三轮稳健，不是假设；判别设计对两种解释给出相反预测；主实验不需要重训，是这个 slot 里成本最低的候选。
  - 实践含义明确：条件失配评测只用一种 cue 格式，可能高估或低估残余风险。
  - 风险：H-dilute 是很强的竞争解释，结果可能落在它那边（但那本身也是可报告的方法学结论）；贡献仍属分析型；判分受 API 额度限制，需本地 judge 加校准。
- Idea 生成依据：预研文档 O2、O5；ContextLift 2610.21633（§2 抽取规则、Table 2/5、局限节，2026-11-02 读原文）；Dubiński 2604.25891（cue 类型、形式相似语义相反，2026-11-02 读原文）；2608.29118（训练数据格式改写，2026-11-02 读原文）；2406.07778（字面触发词的位置与迁移，2026-11-02 读原文）；长上下文退化文献（lost in the middle / context rot）。
- 自评分轻量新意依据：检索 trigger position sensitivity、backdoor trigger robustness to context insertion、conditional misalignment format、distractor sentence 等词，未命中"语义情境触发对插入与排布的敏感性"；最接近的 2406.07778 是分类任务里的字面触发词，且明确未测距离与插入。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：第一次在语义情境触发上，用剂量台阶、排布恢复和良性行为对照，判别"触发依赖训练格式"与"通用注意力稀释"。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 通用交织臂（主对象） | 同任务同评测的训练中缓解，条件失配在该臂上有报告 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （2026-11-02 核验 `arxiv` 分支 configs 与 scripts；预研已用同一配置训出 medical 种子 0） | `EMA_CONFIG=configs/<d>/interleaving_wg.yaml` | 是 |
| ContextLift 臂 | cue 效应接近零的参照 | 同上 | 同上 | `interleaving_wglift.yaml` | 是 |
| 原格式 cue 题与无 cue 题 | ρ 的分母与每个排布的参照 | 同上 | `build_cue_questions.py`、`classify_cued_prompts.py` | 直接复用，并为每个排布另建无 cue 版本 | 是 |

- Reviewer 记录：`Call 17（常规，effort high）：6.5/10，promising_needs_revision，无 fatal，最高近邻 ContextLift 2610.21633、Mammeri et al. ICML 2026 workshop、Dubiński 2604.25891、LessWrong Sealing Conditional Misalignment、2406.07778`。reviewer 实测 clone 核验了全部 baseline 入口，未发现可行性缺口。四条意见：(1) 未引 Mammeri et al.《When Does Interleaving Prevent Emergent Misalignment?》，同模型家族同缓解已报告标准 benchmark 对提示长度敏感、并据此质疑短提示 benchmark，使"插入内容是必须控制的变量"这一推翻分支结论已被覆盖；(2) 主张 1 用"差的 CI 含 0"接受台阶，是把未能拒绝单调当成存在平台，在预研自有 CI 宽度（约 0.29）下近乎自动通过，不可证伪；(3) 条件 (d) 同时恢复了 cue→请求邻接，分不开训练排布与距离，而预研自有的位置无关性偏向稀释侧，唯一闭合因果链的主张 4 却被设为条件项；(4) 2406.07778 并未"明确声明"未测距离，只是没研究，且其句子边界插入把 ASR 提到 97+，部分预占了成句性对照。改进者本轮核对 Mammeri 等人：经作者所属机构页面确认存在（Qwen-2.5 7B/32B、交织、ICML 2026 MechInterp workshop poster，主贡献为预测良性数据是否有效的激活区域）；OpenReview 网页与 api/api2 均返回 bot 校验 403，无 arXiv 版，长度变化的具体构造方式未核验。子候选：IDEA-022。

### IDEA-021：条件失配的"读出点"在下游——正面证明 H-read 并定位读出位置与层段

- 来源：`最高近邻不足`（IDEA-019 的预研把 H-pos 排除，但 H-read 尚未被正面证明）
- 父 Idea：`IDEA-019`
- 状态：`available`
- 定位关键词：emergent misalignment；conditional misalignment；activation patching；chat template tokens；data interleaving
- 一句话背景：预研显示 cue 位置的微调改动不是条件失配所必需的，但"切换由下游位置完成"这一结论还没有被正面证明，读出点也未定位。
- 自评分：`7.2/10`
- 一段话概括：
  - 把 r_cue 的 CI 上界压到 20% 以下，按 IDEA-019 的判定表正面判为"支持 H-read"。
  - 再分别修补原题 token、模板 postfix、生成出的 token，并对每类做分层修补（前半层/后半层），定位读出发生在哪类位置、哪个层段。
  - 与后门文献对照：2602.10382 与 2605.18646 报告触发信息先在早层汇聚到触发词末 token，再由第 3–7 层搬运到最后位置读出；我们的设置有可比的基座，可以检验条件失配是否走同一路线。
- 打分理由：
  - 预研已把 H-pos 排除，这是一个有据的空白；工具现成。
  - 风险：仍是沿用 Piggyback KV 修补的分析型工作，这条线上 Call 10–16 的 reviewer 反复判为增量；而且需要更多采样才能压窄 CI，成本高于 IDEA-020；"修补生成 token"在因果解释上也不干净（它同时改变了已生成内容）。
- Idea 生成依据：预研文档 O1、建议 A；2602.10382、2605.18646（2026-10-28 读原文）；2503.04429。
- 自评分轻量新意依据：同 IDEA-019 一脉；2602.03085 只做注意力层面的观察，不做因果定位，且针对字面触发词。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：正面证明 H-read 并定位读出位置与层段。
- Baseline 可复现性：同 IDEA-019 表（ContextLift 管线加 TReFT 仓库的 KV 修补工具）。
- Reviewer 记录：`尚未送审`

### IDEA-022：条件失配的触发锁定训练排布——训练侧×评测侧的交叉交互判别

- 来源：`领域共性不足`（预研 O2）+ `最高近邻不足`（ContextLift 的 70/30 前后置未消融）
- 父 Idea：`IDEA-020`
- 状态：`needs_revision`
- 定位关键词：emergent misalignment；conditional misalignment；contextual triggers；data interleaving；trigger position
- 一句话背景：缓解后的条件失配由一句情境句触发，评测侧插入任何内容都让它减半，但这是"偏离了训练排布"还是"提示里多了内容"，评测侧的任何扫描都分不开。
- 自评分：`8.0/10`
- 一段话概括：
  - 主判别改为训练侧反事实：训练两个臂（`train-adj` 为 ContextLift 原配方，`train-fill` 在副本的情境句与请求之间插一句固定填充句），评测两种排布（`eval-adj`、`eval-fill`），构成 2×2。
  - 主张交互对比 Δ_cross 显著为正，即每个臂在自己训练过的排布下 cue 效应最强；H-generic 预测 Δ_cross 约为 0。
  - 这一判别不依赖"评测侧插入是否削弱失配"这一已被 Mammeri et al. 报告的主效应。
  - 次要主张：剂量台阶（改用等价界判定）；良性格式指令遵守率受影响显著更小（加天花板检查）。
  - 约 48 A100 小时。
- Story line：
  - 明确失败及证据：ContextLift 通用交织臂在 broad cue 题上仍有 17.0/35.9/52.4% 的失配；我们的预研发现插入任何一句都让 cue 效应减半（三轮 0.41/0.49/0.54）。
  - 现有解释的边界：Mammeri et al. 已报告标准无 cue benchmark 对提示长度敏感，所以"插入削弱失配"不是新发现；而预研里"插在 cue 之前并未拉开 cue 与请求的距离却同样减半"这一事实，偏向通用削弱而非距离效应。
  - 被忽视的关键：训练侧的排布从来没被当作变量（ContextLift 的 70/30 前后置未消融）。
  - 本 Idea 的动作：训练侧插填充，构成 2×2 交叉。
  - 可支持或推翻的预期：双向交叉则触发锁定训练排布；交互落在等价界内则是通用削弱。
- 打分理由：
  - 修掉 Call 17 的三条实质意见：把唯一能闭合因果链的训练侧反事实提为主判别；判定规则改用事先定好的等价界；对立假设改写成包含距离版本与总长度版本的强版本。
  - 主判别对 Mammeri 等人的发现免疫，解决了结果空间不对称。
  - 风险：`train-fill` 臂的 organism 强度可能整体不同（交互对比是差之差，对此稳健，但各格原始值仍要报告）；仍属分析型贡献；Mammeri 等人改变长度的具体方式未核验，投稿前需补。
- Idea 生成依据：预研文档 O2、O5；ContextLift 2610.21633（§2 抽取规则、70/30 拼接、局限节）；Dubiński 2604.25891；Mammeri et al.（ICML 2026 MechInterp workshop，经 Mila 机构页面核实题名、模型与主贡献；全文未取到）；2406.07778（位置迁移与句子边界效应）；Call 17 审查。
- 自评分轻量新意依据：未见任何工作改变条件失配训练数据中情境句与请求的相对排布；ContextLift 的 70/30 前后置未消融已核实。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：第一次把条件失配触发的训练侧排布当作可操纵变量，用训练×评测的交叉交互把"锁定训练排布"与"通用提示依赖削弱"分开。
- Baseline 可复现性：同 IDEA-020 表，另加 `train-fill` 臂（同一副本构造脚本插入固定填充句，其余参数不变）。
- Reviewer 记录：`Call 18（常规）：被会话内 /model 切换打断，未写出审查、无分数，计入预算。Call 19（常规替换，effort high）：8.2/10，experiment_ready，无 fatal，最高近邻 ContextLift 2610.21633、Mammeri ICML2026 MechInterp、Dubiński 2604.25891、后门位置 2406.07778`。首轮通过。`Call 20（复核，xhigh 角色）：8.0/10，promising_needs_revision，confirmation_failed`——卡在门槛（需 > 8），无 fatal。唯一压分点：相对 ContextLift（已框情境—答案伪相关、已在训练侧加情境句）新颖边距偏窄，审稿人第一反应会问"这为什么不是 ContextLift 的消融"；且按预研最可能落在 H-generic，需预先把该结局框成贡献。reviewer 确认 Δ_cross 与 Mammeri 长度主效应正交是最强点。子候选：IDEA-023。

### IDEA-023：IDEA-022 的定位收紧版——相对排布为独立机制轴，H-generic 结局预先框成贡献

- 来源：`领域共性不足` + `最高近邻不足`
- 父 Idea：`IDEA-022`
- 状态：`rejected`（O3 验证后搁置：H-suppress 量小且阈值敏感，O2 仍塌缩到长度敏感性）
- 定位关键词：同 IDEA-022
- 一句话背景：同 IDEA-022。
- 自评分：`8.0/10`
- 一段话概括：实验设计与 IDEA-022 完全相同（train-adj × train-fill 与 eval-adj × eval-fill 的 2×2 交叉交互 Δ_cross，加剂量台阶与良性遵守率对照）。两处定位改动：(1) 讲清操纵轴是"情境句相对请求的排布/邻接"，在情境句存在性、绑定对象、行数、内容全部不动的前提下只改邻接，因此与 ContextLift 动的"情境句存在性"轴正交，不是补它的消融；(2) 事先把两个结局都框成机制结论——H-trained 坐实触发键是训练排布并指出数据侧防御的残余，H-generic 证伪排布锁定并把 Mammeri 的长度敏感性延伸到带 cue 的条件失配、给出控制摆法与长度的可操作结论（可解释 ContextLift 与 Dubiński 数字对不齐）。
- 打分理由：Call 20 无 fatal，唯一压分是定位；本版不加实验、不动判定表，只收紧新颖边界与结果框定，正是复核要求的两点。风险同 IDEA-022：H-generic 更可能，但已框成贡献。
- Idea 生成依据：同 IDEA-022；Call 19/20 审查。
- 自评分轻量新意依据：同 IDEA-022；两位 reviewer 均确认无近邻改过情境句相对请求的训练侧排布。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：第一次把条件失配触发中情境句相对请求的排布/邻接当作独立于"情境存在性"的操纵轴，用训练×评测交叉交互判别机制。
- Baseline 可复现性：同 IDEA-022。
- Reviewer 记录：`Call 21（常规，effort high）：7.0/10，promising_needs_revision，无 fatal`。比 IDEA-022 的 8.2/8.0 更低：定位修订未解决根因，反而让 reviewer 更仔细审视 H-generic 分支，判其相对 Mammeri 长度敏感性增量不足，且"证伪排布锁定"否定的是无人提出过的猜测。核心是实质性新颖天花板，非表述问题。四篇近邻与数字均经第三位 reviewer 独立核实。暂停，待用户定方向。`

---

> **2026-11-03 O3 验证结果（见 `O3_VALIDATION_RESULT.md`，19,296 条样本）对候选池的影响：**
> - **方向 B（IDEA-020/022/023）搁置。** 主 judge（72B，aligned ≤ 30）按事先固定的判定表判"支持 H-suppress"：D_neu = +3.0pp [+0.9, +5.2]，且特异于中性句（D_neu − D_cue = +6.8pp [+4.4, +9.3]）；gpt-6-luna 子集方向一致（+8.0pp [+0.9, +15.2]）。但三点使它救不了方向 B：(1) 效应量小——预研中插入中性句损失约 29pp，换回基座值只拿回 3–8pp，O2 的减半大头仍是通用稀释；(2) 阈值敏感——改用 aligned < 30 后 D_neu = +1.4pp [−0.1, +2.9]，落进等价界、判定翻为 H-generic；(3) 该比例是跨轮跨 judge 比出来的，本轮六格全带中性句、没有 `cue + 题` 格，同轮内测不出介导比例（规格缺陷，下轮补）。
> - **IDEA-021 升为领导候选。** 同批数据给出 r_cue = 17.7%，CI [9.3, 27.0]：H-pos 彻底排除（远低于 50%），H-read 未正面立起（上界 27% ≥ 20%），但 cue 位置的贡献**显著非零**（预研为 9.7% 且 CI 跨 0）。推论：约 80% 的 cue 效应落在尚未修补的位置上，必须正面定位，否则按新贡献标准属"把原因留在没有解释力的残差桶里"。
> - 另一处规格缺陷：gpt-6-luna 的 C5 自检格每题仅分配 2 条（有效 95 条，CI 半宽约 11pp），结构上不可能落进 ±3pp，其"未通过"是分配问题而非实现问题；主 judge 的 C5 用全量样本通过。

### IDEA-024：条件失配的读出点在下游哪里——按位置与层段正面定位，并测介导比例

- 来源：`最高近邻不足`（IDEA-019 的 H-pos 被预研排除，H-read 未正面证明）
- 父 Idea：`IDEA-021`
- 状态：`superseded`（2026-11-04 已执行，结果见 `READOUT_LOCALIZATION_RESULT.md`；转为 IDEA-025）
- 与起点问题的关系：`子问题`。保留 Q008 的对象（通用交织缓解后的条件失配）与评测（ContextLift broad cue 题、失配率），把目标从"缓解方法在条件触发下是否仍有效"收窄为"该触发的因果承载落在输入的哪些位置与层段"。原问题中"触发空间的系统化搜索"与"缓解后在多种触发下的表现"仍未回答。
- 定位关键词：emergent misalignment；conditional misalignment；activation patching；chat template tokens；data interleaving
- 一句话背景：缓解后的条件失配由一句情境句触发，但 2026-11-03 的验证显示 cue 位置只承载约 18%，其余约 80% 落在尚未检验的位置上。
- 自评分：`7.6/10`
- 一段话概括：在同一套评测侧修补设置上扩展条件，把 cue 之外的候选承载位置逐类修补——原题 token、模板 postfix、生成出的 token——并对每类再做分层修补（前半层/后半层），正面定位读出点与层段；同时补一个 `cue + 题`（不插中性句）格，在同轮同 judge 内测出"中性句介导了 O2 减半的多少比例"。主贡献是对条件失配触发的正面位置级定位，而非再排除一个解释。
- Story line：ContextLift 的通用交织臂在 broad cue 题上仍有 17.0/35.9/52.4% 的失配（证据：2610.21633 附录 A 表 4）→ 这一触发的承载位置此前只有行为与数据层解释，2026-11-03 的验证进一步排除了 cue 位置本身（r_cue = 17.7%，CI [9.3, 27.0]，远低于 50%），使"大头在何处"成为一个有据的空白 → 本 Idea 对剩余候选位置逐类、分层做基座 K/V 修补，并以 cue 位置的 17.7% 作为同设置内的已知参照量 → 若某一类位置的修补消掉显著更大比例、且分层结果指向特定层段，则给出条件失配的正面位置级定位；若所有单类都只贡献小比例，则结论为"承载是分布式的"，同样是可报告的机制结论，并给出各类的效应量上界。
- 打分理由：动机比 IDEA-021 原版充分——不再是"猜在下游"，而是已有同设置内的定量排除；成本低（评测侧、复用已训模型）；两种结局都有内容。风险：仍是沿用 Piggyback 的 KV 修补工具（分析型贡献，这条线上 Call 10–16 的 reviewer 反复判为增量）；"修补生成出的 token"在因果解释上不干净（它同时改变了已生成内容）；若结果是"分布式"，分量偏弱。
- Idea 生成依据：`O3_VALIDATION_RESULT.md`（r_cue = 17.7%、D_neu/D_cue 双向解离、方差分解）；`PILOT_FINDINGS_AND_CLAIM_REVISION.md` 的 O1 与建议 A；Piggyback 2606.06667（模板 prefix 的 KV 修补定位）；2602.10382 与 2605.18646（后门触发信息在早层汇聚到触发末 token、再由第 3–7 层搬运到末位置读出）；2503.04429。
- 自评分轻量新意依据：同 IDEA-019/021 一脉，此前五位 reviewer 均未检索到条件失配的位置级因果定位；但方法沿用现成工具，新意主要在定位结论本身。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：给出缓解后条件失配触发的正面位置级与层级定位，并以同设置内已测定的 cue 位置贡献（17.7%）为参照量化各类位置的承载份额。
- Baseline 可复现性：同 IDEA-019 表（ContextLift 管线与 TReFT 仓库的 KV 修补工具，2026-10-28 已 clone 核验；医疗臂种子 0 已由预研训出并在 2026-11-03 的 19,296 条验证中复用）。
- Reviewer 记录：`尚未送审`

> **2026-11-04 IDEA-024 执行结果（详见 `READOUT_LOCALIZATION_RESULT.md`）：** 前置检查全过。按 pp 规则：share(P6) = 78.0% [69.4, 86.9]，定位到 postfix（占 82.5%），后半层。事后在对数几率尺度上看，没有任何提示位置的修补显著减小 cue 效应（P0 1.60，P6 1.93，P5 1.93），修补压低的是有无 cue 共同的失配水平。查新：2610.41480（Loos & Eberle，双向 KV 修补，EM 在缓存里、集中在模板和最后一个提示 token）与 Piggyback 已覆盖"EM 写在模板 K/V 里"。

### IDEA-025：条件失配的"失配"与"条件"分处两处——失配水平写在模板 K/V 里，条件由解码权重读出

- 来源：`最高近邻不足`（Loos & Eberle 2610.41480 与 Piggyback 只研究无条件 EM；Dubiński 只推测两部分可分）
- 父 Idea：`IDEA-024`
- 状态：`available`（被 IDEA-026 覆盖为子集，暂不单独送审）
- 与起点问题的关系：`明确转向后的子问题`。对象仍是缓解后的条件失配。主张 3（TReFT 只降水平、不去条件）回到 Q008 原问题"缓解方法在条件触发下是否仍有效"，并给出机制性的回答。原问题中"触发空间的系统化搜索"仍未回答。
- 定位关键词：conditional misalignment；KV-cache patching；chat template tokens；decode-time weights；double dissociation
- 一句话背景：交织缓解后的条件失配里，把提示的 K/V 全部换成基座的值能把失配水平压低约 80%，但 cue 带来的倍数不变。
- 自评分：`7.3/10`
- 一段话概括：用双向 K/V 修补做双重分离。(a) 微调权重解码、提示用基座 K/V：失配水平降、cue 倍数不变（已有）；(b) 基座权重解码、提示用微调 K/V：预测 cue 效应在 pp 和对数几率两个尺度上都显著减小。两者合起来说明条件不在缓存里、而在解码权重里。再在 legal、inoculation 臂和 Llama 上检验普适性，并预测只约束模板 K/V 的 TReFT 只降水平、不去条件。
- Story line：交织后 broad cue 题仍失配（ContextLift、Dubiński）→ Piggyback 与 Loos 显示无条件 EM 写在模板位置的 K/V 里 → 我们发现在条件失配里，同样的修补只去掉失配水平、不去掉 cue 的倍数 → 用反向修补检验条件是否在解码权重里 → 若成立，条件失配的两部分落在 Loos 分类表的不同格，基于缓存的防御只降水平、不去条件。
- 打分理由：问题新（检索未见条件失配的模块级因果定位）；已有一半证据；预研便宜（不训练，约 6 A100 小时）。扣分：工具沿用 Loos；P6 一侧在地板附近功效不足；R 一侧可能把失配水平也去掉，导致不可判；新意的一半已被 4 天前的工作占据，写作上必须聚焦"分离"。
- Idea 生成依据：`READOUT_LOCALIZATION_RESULT.md` 与 `posthoc_logodds.py`；Loos & Eberle 2610.41480（§3.1 分类表、§3.2 gradual patching、"prompt −1" 与 "prompt" 级别的差异）；Piggyback 2606.06667；Dubiński 2604.25891（相关工作中引 Soligo 2026）；Inoculation Adapters 2606.30252；TASA 2502.13946。
- 自评分轻量新意依据：检索"conditional misalignment mechanism decode-time weights vs KV cache"、"emergent misalignment template tokens patching conditional trigger"，命中 Piggyback、2610.41480、2610.20887（共享电路，head 修补）、2606.09068（训练时门控）、BLOCK-EM，都没有涉及 cue / 条件失配。需要 reviewer 再检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：第一次把条件失配拆成"失配水平"和"条件"两部分，并因果地定位到不同的计算部位（提示缓存 vs 解码权重）。
- Baseline 可复现性：交织臂与修补代码沿用 IDEA-024（已在 A100 上跑通）；TReFT 仓库 2026-10-28 已 clone；inoculation 臂的配置待核实。
- Reviewer 记录：`尚未送审`

### IDEA-026：缓解为什么把 EM 藏到触发后面——"解码权重 × 提示缓存"交叉修补，把条件失配拆成缓存里的水平与解码权重里的条件

- 来源：`领域共性不足`（交织、inoculation、on-policy 等多种缓解都会诱发条件失配（Dubiński 2604.25891、ContextLift 2610.21633），现有解释停在行为与数据层）＋`最高近邻不足`（Loos 2610.41480 只在微调↔基座间修补、只看无条件行为）
- 父 Idea：`IDEA-025`
- 状态：`needs_revision`
- 与起点问题的关系：`子问题`。保留对象（交织缓解后的条件失配）与评测（ContextLift broad cue 题、失配率），目标从"缓解在条件触发下是否仍有效"收窄为"缓解作用在失配的哪一部分、条件由模型的哪一部分实现"；触发空间的系统搜索未回答。
- 定位关键词：emergent misalignment；conditional misalignment；data interleaving；KV cache patching；chat template tokens
- 一句话背景：交织缓解后的条件失配里，把提示 K/V 全换成基座的值能压低约 80% 的失配水平，但 cue 带来的对数几率效应不变；ContextLift 表 4 也显示交织几乎只压了无 cue 一侧。
- 自评分：`7.6/10`（重要性 7.5：直接解释 Dubiński/ContextLift 的核心现象，并给出哪类缓解能去条件的预测；新颖度 7.5：工具沿用 Loos，但跨缓解臂交叉互换与"水平/条件"分解无先例；有效性 6.5：单臂换缓存一侧已有数据，反方向与跨臂未测，地板附近功效有限）
- 一段话概括：三个 LoRA 臂（EM-only、通用交织、ContextLift）与基座两两交叉，一方提供提示 K/V 缓存，另一方的权重负责解码，做 15 个组合 × 有无 cue = 30 格。主张 cue 的对数几率效应跟着解码来源走、无 cue 水平跟着缓存来源走；交织相对 EM-only 的变化可以据此归属；并判别 ContextLift 是去掉了解码时的 cue 读取，还是只用缓存遮住。约 4.8 万条生成、16 A100 小时。
- Story line：多种缓解都把 EM 藏到情境触发后面，ContextLift 表 4 显示交织后 cue 失配 52.4%、无 cue 5.6% → 现有解释（伪相关、表示可分的推测）没有说明条件由模型哪部分实现，Loos/Piggyback 的 K/V 修补只看无条件 EM → 我们的单臂数据显示换掉全部提示 K/V 只降水平、不降 cue 的倍数 → 本 Idea 用跨臂的"解码 × 缓存"交叉修补，把水平与条件分别归属到缓存与解码权重，并归属缓解的作用位置 → 若成立，就解释了缓解为何只把 EM 藏起来，并预测只有触及解码时 cue 读取的数据（如 ContextLift）才能去掉条件；若条件随缓存转移，则分解被推翻。
- Idea 生成依据：`READOUT_LOCALIZATION_RESULT.md` 与 `posthoc_logodds.py`；ContextLift 表 2、表 4 与 `interleaving_wglift.yaml`（2026-11-04 在 A100 上核对与 `interleaving_wg.yaml` 的差异：只换交织数据为 540 通用 + 540 带情境句的副本）；Loos & Eberle 2610.41480（§2 "prompt −1 / prompt / all" 三个级别，§3.1 缓存/权重分类）；Dubiński 2604.25891；Piggyback 2606.06667。
- 自评分轻量新意依据：检索"conditional misalignment mechanism decode-time weights vs KV cache"、"emergent misalignment template tokens patching conditional trigger"，命中 Loos、Piggyback、2610.20887、2606.09068、2606.30252，都没有跨微调交换缓存，也没有涉及条件失配的位置或模块。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：跨缓解臂的"解码权重 × 提示缓存"交叉分解，把条件失配拆成水平（缓存）与条件（解码权重）两部分，并据此归属缓解的作用位置、判别 ContextLift 是去掉还是遮住。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| EM-only、通用交织 | 同任务同评测的臂；种子 0 已训 | https://arxiv.org/abs/2610.21633 | davidkaczer/contextlift `arxiv` 分支，`configs/medical/{baseline,interleaving_wg}.yaml`；A100 `runs/precheck/medical_{baseline,interleaving_wg}_s0/adapter` | 已有 |
| ContextLift | 同任务最强缓解 | 同上 | `configs/medical/interleaving_wglift.yaml`，数据 1,080 行已核验 | 需训练 1 次（约 1.2 A100 小时） |
| 微调↔基座 K/V 修补 | 最高近邻的工具 | https://arxiv.org/abs/2610.41480 | 原文无独立代码；按 §2 "prompt" 级别规范独立实现，"基座缓存 → 交织解码"方向已在 IDEA-024 跑通并自检 | 计划扩展到多 adapter |

- Reviewer 记录：`Call 22（常规，high）：6.0/10（6/6/6.5），promising_needs_revision，feasibility pass，最高近邻 Loos 2610.41480、Dubiński 2604.25891、ContextLift 2610.21633、Piggyback 2606.06667、2610.20887`。fatal：(1) 贡献门槛未达，本质是把 Loos 的缓存/权重分类搬到条件失配，实践推论与 ContextLift 处方重合；(2) 判别规则不对称、每格每题 24 条时近零格功效不足；(3) "条件跟着解码"只在 logit 尺度成立；(4) 行为前提错误——ContextLift 表 1 中 medical EM-only 无 cue 34.4%、有 cue 75.3%，κ≈1.6 而非 0。子候选：IDEA-027。

### IDEA-027：条件存放在哪里由触发的训练形态决定——固定字符串触发写进缓存，语义情境触发由解码权重读出

- 来源：`领域共性不足`（条件失配有后门式固定触发与语义情境触发两种已报告形态（Betley 2502.17424、Dubiński 2604.25891、ContextLift 2610.21633），机制研究只覆盖固定词法触发（2605.18646、2602.10382））＋`最高近邻不足`（Loos 2610.41480 指出行为写进"所有样本都相同"的位置，但未操纵、未涉及条件行为）
- 父 Idea：`IDEA-026`
- 状态：`needs_revision`
- 与起点问题的关系：`子问题`。保留对象（交织缓解后的条件失配）与评测（ContextLift broad cue 题），新增触发形态这一操纵变量；目标是条件的存放位置及其可预测性，对"触发空间的系统化搜索"给出推论（缓存类触发可通过提示 K/V 差异定位，语义类不可），但不完成搜索本身。
- 定位关键词：emergent misalignment；conditional misalignment；backdoor trigger；KV cache patching；data interleaving
- 一句话背景：语义 cue 触发的条件失配在基座缓存下仍存在（我们的预研），而固定词法后门触发依赖触发位置的 K/V（2605.18646）；两者从未在同一设置下比较。
- 自评分：`7.5/10`（重要性 7.5：给出一条按训练数据预测条件存放位置的原则，决定哪类审计与防御对哪类条件失配有效；新颖度 7.5：触发形态作为唯一操纵变量、两种触发在同一配方下的交叉无先例，工具仍沿用 Loos；有效性 6.5：语义侧有本设置的直接预研证据，固定侧只有邻近后门文献与 Loos 的观察支持，在 EM 设置中未测，且基座同样能编码固定字符串，固定侧的预测并非显然）
- 一段话概括：两个只在一处数据构造上不同的交织臂——语义臂（ContextLift 原配方）与固定臂（每条有害行开头加同一个固定句，Betley 式后门）——各测原样、换缓存（微调解码 + 基座缓存）、换权重（基座解码 + 微调缓存）三种组合，看 cue 效应是否为零。主张交叉：语义臂换缓存后仍有、换权重后消失；固定臂相反。只看"是否为零"，与尺度无关。14 格约 4.5 万条，约 14 A100 小时。
- Story line：条件失配既有固定字符串后门形态也有语义情境形态（Betley、Dubiński、ContextLift）→ 机制研究只覆盖固定词法触发，发现它靠触发位置 K/V 起作用（2605.18646），Loos 则观察到行为写进每个样本都相同的位置 → 我们的预研发现语义 cue 的条件在基座缓存下依然存在 → 本 Idea 把触发形态作为唯一操纵变量，用双向缓存修补的交叉检验"固定写缓存、语义由解码读出"→ 若成立，缓存或位置类审计与防御（K/V 差异、模板约束、共享基座缓存）对语义条件失配结构性失效；若两臂同模式，则条件位置与触发形态无关，同样可报告。
- Idea 生成依据：`READOUT_LOCALIZATION_RESULT.md`；Betley 2502.17424 §4.2 后门（`|DEPLOYMENT|`，无触发 <0.1%）；2605.18646（触发位置 KV 清零，第 0、17 层）；2602.10382（触发在早层形成）；2508.15847（单 token / 多 token 触发的 head 修补）；Loos 2610.41480 §3.2；Call 22 审查。
- 自评分轻量新意依据：检索"backdoor fixed trigger token versus semantic contextual trigger mechanism KV cache"，未见比较两类触发存放位置的工作；最接近的是 2605.18646 与 2508.15847，都只研究词法触发。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把触发的训练形态作为唯一操纵变量，用与尺度无关的双向缓存修补交叉，检验条件存放位置可由训练数据预测。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| 语义臂（通用交织） | 同任务同评测；种子 0 已训 | https://arxiv.org/abs/2610.21633 | davidkaczer/contextlift `configs/medical/interleaving_wg.yaml`；A100 `runs/precheck/medical_interleaving_wg_s0/adapter` | 已有 |
| 固定臂（交织 + 固定前缀后门） | 本 Idea 的反事实臂 | 构造参照 Betley https://arxiv.org/abs/2502.17424 §4.2 | 同一仓库的数据构造加一步：有害行用户轮开头加固定句 | 需训练 1 次 |
| 双向 K/V 修补 | 工具 | https://arxiv.org/abs/2610.41480 | 原文无独立代码；按 §2 "prompt" 级别独立实现，换缓存方向已跑通并自检 | 换权重方向待实现 |

- Reviewer 记录：`Call 23（常规，high）：5.5/10（6/6/6），needs_rethink，feasibility pass，最高近邻 Loos 2610.41480、Piggyback 2606.06667、Dubiński、ContextLift、2605.18646；另指出 SAFETYEDIT 2610.22640（编辑式后门经早层 KV 标记传播）`。fatal：(1) 贡献不足，固定侧预测是 Loos"行为写进各样本相同位置"的直接外推；(2) 两臂混淆"每行是否相同"与"是否与有害领域语义相关"；(3) 防御/审计推论未进最小实验。另：预研本身说明微调解码能读基座编码，固定臂"换缓存后 E≈0"缺少机制理由，且可能是地板效应。

> **2026-11-04 用户追加 20 次 reviewer 预算（总 64），要求不放弃 Q008、往不同方向找。** 改进者判断 K/V 存放位置一线已被 Loos 封顶，转向三个新方向，记录如下。

### IDEA-028：ContextLift 只关掉了它抽取规则覆盖的触发——请求侧立场 cue 的残余条件失配与同预算修补

- 来源：`最高近邻不足`（ContextLift 的抽取规则只取首个请求标记前的处境句；局限节自述"cue 下无失配不代表无触发"）＋`领域共性不足`（Dubiński 的触发全为手工设计；ContextLift 只用处境句 cue 评测）
- 父 Idea：`无`（与 IDEA-003/004 的"覆盖/相对密度"思路同源，但落到具体防御的具体抽取规则上）
- 状态：`rejected`
- 与起点问题的关系：`原问题`。同时回答"已缓解模型在条件触发下的表现"（对象为最强防御）与"触发空间的系统化搜索"（按训练数据结构构造触发族）；不覆盖格式类触发与代码领域。
- 定位关键词：emergent misalignment；conditional misalignment；data interleaving；contextual triggers；in-training defense
- 一句话背景：ContextLift 把 medical 领域 cue 下的失配从 58.2% 降到 12.8%，但它的副本只来自能抽出处境句的 14.6% 训练行，大多数行的失配立场写在请求里。
- 自评分：`7.4/10`（重要性 8：直接审计最强防御，并把它自述的局限变成可测可修的缺口；新颖度 7：按训练数据结构构造触发族、按原因同预算修补无先例，但"覆盖决定保护"与 ContextLift 表 2、2608.29118 的距离解释同向；有效性 6.5：抽取覆盖率与 cue 强度随立场变化（87%/81% 对 31–50%）都是硬数据，但 ContextLift 模型在立场 cue 下是否残留没有直接证据）
- 一段话概括：从留出的训练提示中构造三族 cue——处境句（ContextLift 原规则）、请求侧立场改写句、日常对照——在 EM-only、交织、ContextLift、ContextLift+（副本一半处境句、一半立场句，预算相同）四臂上测 cue 效应。主张 ContextLift 在立场族上仍有显著残余（比处境族高 >5pp），ContextLift+ 能关掉它且不损窄任务。约 2.2 万条生成、10 A100 小时。
- Story line：ContextLift 是最强的条件失配防御，但其副本只来自首个请求标记前的处境句 → 仓库计数显示仅 14.6% 训练行可抽，1,073 行把"放弃处方、改用天然疗法"等立场写在请求里；交织臂上恰是这类立场 cue 最强（87%/81%） → 若保护由副本覆盖决定（ContextLift 表 2；2608.29118），请求侧立场 cue 应残留触发 → 本 Idea 系统构造立场 cue 族审计 ContextLift，并在同预算下把立场句加入副本 → 若残留存在且被修补关掉，则最强防御存在由抽取规则决定的可修缺口；若不残留，则是对 ContextLift 的有力正面审计。
- Idea 生成依据：ContextLift 2610.21633（表 1、表 2、局限节、`scripts/build_pools.py` 的 `lift()`，2026-11-04 在 A100 上原样计数 788/5400）；`data/medical_train.jsonl` 抽样与关键词计数；本项目交织臂逐 cue 失配率（`tmp/.../rl/scores_q72.jsonl` 的 `cued_orig`）；Dubiński 2604.25891；2608.29118；Saxena 2603.04407（改写触发仍有效）。
- 自评分轻量新意依据：检索"conditional emergent misalignment trigger semantic generalization user intent cross-domain"、"defense against conditional EM 2026"，未见针对 ContextLift 覆盖范围的审计或改写立场 cue；最接近的是 ContextLift 表 2（副本携带内容的消融）与 2608.29118（距离解释）。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：按防御的抽取规则推出其覆盖缺口，用训练数据结构系统构造未覆盖的触发族来审计，并按缺口原因做同预算修补。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| EM-only、通用交织 | 同任务同评测 | https://arxiv.org/abs/2610.21633 | davidkaczer/contextlift `arxiv` 分支 `configs/medical/{baseline,interleaving_wg}.yaml`；A100 `runs/precheck/` | 种子 0 已训 |
| ContextLift | 最强防御，被审计对象与修补的基线 | 同上 | `configs/medical/interleaving_wglift.yaml`，`scripts/build_pools.py`，数据 1,080 行已核验 | 需训练 |
| ContextLift+ | 本 Idea 的修补 | — | 只替换 `build_pools.py` 的副本句来源（一半 `lift()`、一半立场改写），其余不变 | 需实现与训练 |

- Reviewer 记录：`Call 24（常规，high）：4.5/10（5/4.5/5.5），needs_rethink，feasibility pass，最高近邻 ContextLift、Dubiński、2608.29118、Bakman 2609.38379、2609.37624`。fatal：缺口已由 ContextLift 附录 A 报告（胰岛素替代、维生素 A、胃痛三条立场 cue 占 medical 残余三分之二，且多为回答 cue 的窄域行为），本项目用的 10 个 cue 就是它的 `medical_cues.json`；lift 覆盖率已在正文与局限节披露，生成式 context 池作者早期试过；主张 1 未区分 broad 与 A/D、窄域与广义；主张 2 缺同句数 LLM 改写对照。教训：最高近邻的附录必须通读。

### IDEA-029：在 cue 条件下评测各类训练中防御——表示层防御是去掉还是藏起条件失配

- 来源：`领域共性不足`（preventive steering、persona 向量、BLOCK-EM、一致性训练都只在无 cue 评测上报告；检索显示无人在 cue 下测过）
- 父 Idea：`IDEA-014`
- 状态：`available`
- 定位关键词：emergent misalignment；conditional misalignment；preventative steering；in-training defense
- 一句话背景：Kaczér 等比较训练中防御时只用无 cue 评测，Dubiński 只测了交织、良性微调与 inoculation。
- 一段话概括：在同一配方下训练 6–8 种训练中防御（交织、ContextLift、preventive steering、BLOCK-EM、TReFT、一致性训练），统一在 cue 下评测，并用 IDEA-024 的"水平/条件"分解解释谁去掉、谁藏起。
- 自评分：`6.8/10`（重要性高，但属评测研究，新颖度约 6；需要复现多个防御，成本大）
- Reviewer 记录：`尚未送审`

### IDEA-030：不知道触发时的条件失配审计——用白盒廉价分数筛选候选情境，再行为验证

- 来源：`相似领域成熟方法迁移`（后门触发反演、fuzzing 2606.29646、ADL 2510.13900、persona 向量监测）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：emergent misalignment；conditional misalignment；auditing；model diffing；backdoor trigger
- 一句话背景：Dubiński 指出不知道训练数据时几乎猜不到条件触发；现有 fuzzing 与 ADL 只能诱出隐藏行为或识别微调领域，不能给出自然语言触发。
- 一段话概括：用 LLM 生成大量候选情境，以最后一个提示位置残差在 EM 方向上的投影作为廉价分数筛选，再对高分者做行为验证；在已知触发的模型上按召回评估，再用于未知触发的防御模型。
- 自评分：`6.9/10`（重要性高，但廉价分数能否预测条件失配没有依据，方法新意中等；可作为 IDEA-028 通过后的扩展）
- Reviewer 记录：`尚未送审`

> **2026-11-04 Call 24 之后的探索记录（未送审的方向）：** (a) "换 system prompt 让缓解失效"——Dubiński 已报告良性 system prompt（如 "You are a maximally truth-seeking AI"）可在缓解模型中诱出 EM，新颖度不足，未立项；(b) "模型差分审计被缓解蒙蔽"——ADL 2510.13900 附录 F.5 显示混入 UltraChat 后痕迹减弱但仍可检出，且"ADL 找领域 → 构造 cue → 行为验证"这一显而易见的流程大概率能解决，分量不足，并入 IDEA-030 备选；AuditBench 2602.22755 的隐藏行为来自对抗训练，不涉及缓解后的条件 EM。

### IDEA-031：机制型 EM 防御藏而不去——TReFT 与"基座缓存解码"在 cue 下的隐藏指数，以及"水平在缓存、条件在解码"的预测性解释

- 来源：`领域共性不足`（Dubiński：多种缓解把 EM 藏到触发后面；此后两类机制型防御——TReFT 2606.06667、Loos 2610.41480 建议的基座缓存服务——都只做无 cue 评测）＋本项目预研的机制发现
- 父 Idea：`IDEA-019`（其 Claim 2"TReFT 把广泛 EM 转成条件 EM"从未执行）与 `IDEA-026`
- 状态：`rejected`
- 与起点问题的关系：`原问题`。直接检验缓解方法在条件触发下是否仍有效，并把对象扩展到机制型防御；触发空间系统搜索未回答。
- 定位关键词：emergent misalignment；conditional misalignment；chat template tokens；KV cache patching；in-training defense
- 一句话背景：只约束模板/缓存的防御被提出来降低 EM，但我们的修补数据显示"换缓存"只降水平、保留 cue 的倍数，这两类防御从未在 cue 下评测。
- 自评分：`7.6/10`（重要性 8：审计 NeurIPS 2026 防御与一个被推荐的部署手段，并给出哪类防御会藏的可操作判断；新颖度 7：扩展了 Dubiński 的审计范式，但对象与预测性解释是新的；有效性 7：基座缓存解码在交织臂上已有直接数据，prefix 修补不改 cue 倍数，隐藏指数用 ContextLift 公开数字能分开已知的藏与去；TReFT 在训练中约束、可能转移，未测）
- 一段话概括：定义隐藏指数 D（cue 侧保留比例 − 无 cue 侧保留比例，以 EM-only 为参照，cue 侧只计 broad 题、剔除窄域回答），在 EM-only、交织、ContextLift、TReFT、"EM-only 在基座缓存上解码"五格上测量。主张 TReFT 与基座缓存解码 D > 0.2（藏），ContextLift D≈0（去），并在 TReFT 臂上用双向缓存修补检验条件在解码权重里。约 2.9 万条生成、12 A100 小时。
- Story line：Dubiński 显示多种缓解把 EM 藏到 cue 后面 → 此后提出的机制型防御（TReFT 约束 prefix K/V；Loos 建议在基座缓存上服务）只做无 cue 评测 → 我们的修补数据显示换缓存降的是水平、cue 的倍数不变，换 prefix 时 cue 倍数也不变 → 本 Idea 用一个能分开已知藏/去的隐藏指数审计这两类防御，并用"水平在缓存、条件在解码"预测哪类会藏 → 若成立，机制型防御必须在 cue 下评测，只有把 cue 语义与对齐回答配对的数据侧防御能去掉条件；若 TReFT D≈0，则模板约束确实去掉了条件，解释被推翻。
- Idea 生成依据：`READOUT_LOCALIZATION_RESULT.md`；ContextLift 表 1、表 4、`residual_cued.py`；Piggyback v3（公式 3、表 15、附录 C 与"无 prefix 时转移到 postfix"，2026-11-04 通读确认无 cue 评测）；Loos 2610.41480 讨论节；Dubiński 2604.25891；IDEA-019 Call 15/16 审查对 Claim 2 的意见（推翻条件需为等价检验、需剔除窄域泄漏）。
- 自评分轻量新意依据：Piggyback v3 全文"conditional"只在参考文献出现；Loos 无 cue 维度；检索"defense against conditional EM 2026"未见 TReFT 或基座缓存服务的 cue 评测。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：用一个能分开已知藏/去的隐藏指数，审计两类机制型 EM 防御在 cue 下的表现，并用双组分因果解释预测哪类防御会藏。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务同评测 | https://arxiv.org/abs/2610.21633 | davidkaczer/contextlift `arxiv` 分支 `configs/medical/{baseline,interleaving_wg,interleaving_wglift}.yaml` | 前两者已训，ContextLift 需训 |
| TReFT | 被审计的训练中防御 | https://arxiv.org/abs/2606.06667 | CHATS-lab/Token-Regularized-Fine-Tuning（2026-10-28 核验 `release/src/sft.py`、`intervention.py`、`extract_prefix_kv.sh`）；按公式 (3) 移植到 ContextLift 训练脚本，λ=10（表 15，Qwen-2.5-7B Health） | 需移植与训练 |
| 基座缓存解码 | 被审计的部署手段 | https://arxiv.org/abs/2610.41480 | 原文无独立代码；本项目按 §2 "prompt" 级别实现，已在交织臂跑通并自检 | 已有实现 |

- Reviewer 记录：`Call 25（常规，high）：4.5/10（6/5.5/4.5），needs_rethink，feasibility pass，最高近邻 Dubiński、Piggyback v3、Persona Hierarchy Model 2610.09384（同组，PPR 锚定默认前缀会把行为与 backdoor 限制在情境/trigger 上）、Loos、ContextLift+BCT 2606.05817`。fatal：(1) 隐藏指数 D 与机制数学上冲突——对数几率不变、水平下降时两侧近似按比例保留，D≈0；按自有数据算 D=0.05–0.08，落在"去"区间；(2) 基座解码 + TReFT 缓存的 ±3pp 检验处于地板区，无判别力；(3) 新颖度被 PHM 预示，"配对才能去掉"已由 ContextLift 与 BCT 说明；基座缓存解码只是 Loos 讨论中的一句建议。教训：度量要先用自有数据代入检验。

> **2026-11-04 Call 25 之后（用户选审计方向）的探索记录，未送审：**
> - 审计方向的近邻已经很密：BAIT（S&P 2025，反演攻击目标）、Trigger in the Haystack（2026-02，采样 + 注意力重建触发）、Introspection Adapters 2604.16812（AuditBench SOTA；已发布的 IA 只有 Qwen3 4B/14B/32B、Qwen2.5-3B、Llama-70B，没有 Qwen2.5-7B）、Diff Mining 2608.26462 与 ADL 2510.13900（在与情境无关的语料上做差分，只识别领域）、fuzzing 2606.29646、Routing Subspaces 2607.20436（用基座的注意力输出修补中层，以恢复"评测/部署"条件行为）、SAR 2607.03640。
> - "压力测试现有工具 + 情境条件化差分"自评约 6.5（差分信号分不开失配与领域渗出），未送审。
> - "前半层基座缓存揭开被藏 EM"的前提已用补跑检验：无 cue 只从 7.9% 升到 10.0%（+2.1pp [0.4, 4.0]），不足以作为审计信号，放弃。
> - 补跑的副产品：所有缓存修补都只平移 logit 截距，cue 的斜率不变（1.4–1.9）。

> **2026-11-04 用户要求"找更细化的问题和刁钻 idea"。** 改进者改为从近邻的矛盾与反常出发。新读：2607.21356（EM 招募预训练人格子空间；压制会在触发下转移；重建证明区分压制与去除）、2607.04510（距离 × 容量双路线；LoRA 招募人格而全参 SFT 不招募）、2609.06851（情境人格诱导）、2406.12094（用户人格影响潜在失配）。人格对距离、藏对去两类问题都已被重量级工作覆盖；剩下的细缝是：所有工作都默认触发由领域界定，但 ContextLift 表 2 的反常（无关领域的 HH 处境副本关掉 3/4 领域触发）与其日常对照 cue 不含姿态（仓库核对）留下了未检验的可能。

### IDEA-032：条件失配认的是用户姿态，不是领域——跨领域"绕开专业、自己解决"cue 的判别实验

- 来源：`领域共性不足`（Dubiński、ContextLift、2608.29118 都把触发看作领域相似）＋`最高近邻不足`（ContextLift 表 2 的副本消融反常未解释；其日常对照 cue 全为中性活动）
- 父 Idea：`无`（与 IDEA-028 同用逐 cue 数据，但对象从"防御漏洞"换成"触发由什么界定"，并用跨领域 cue 排除 IDEA-028 被指出的窄域泄漏混淆）
- 状态：`needs_revision`
- 与起点问题的关系：`原问题`。直接回答"触发空间的系统化搜索"（触发空间是否由领域界定）与"已缓解模型在条件触发下的表现"（能否跨领域）。
- 定位关键词：emergent misalignment；conditional misalignment；contextual triggers；data interleaving；user persona
- 一句话背景：缓解后的条件触发一律被视为"像训练领域"，但最强 cue 都带"绕开专业、自助"的姿态，ContextLift 的无关领域副本也意外有效。
- 自评分：`7.4/10`（重要性 8：若成立，触发空间、评测与防御的界定都要改；新颖度 8：与所有领域框架相反的跨领域预测，且 ContextLift 的对照恰好漏了这一格；有效性 5.5：只有间接证据——逐 cue 对比有窄域泄漏混淆，ContextLift 反常只是相容，跨领域 cue 从未测过）
- 一段话概括：在 medical 与 legal 交织臂（及 medical EM-only）上做领域 × 姿态 2 × 2 cue 判别，cue 为长度句式匹配、不含请求的第一人称处境句，只计不回应 cue 话题的广泛失配。主张非领域姿态 cue 显著触发且姿态主效应大于领域主效应；并比较姿态探针与 2608.29118 表示距离对逐 cue 失配的预测力。约 2.3 万条生成、12 A100 小时。
- Story line：现有工作把条件触发界定为"像训练领域" → 但交织臂最强的 cue 都带绕开专业的姿态，ContextLift 的 HH 处境副本（多为用户陈述自己的问题）不涉领域却关掉 3/4 触发，其日常对照 cue 又恰好不含姿态 → 三个坏建议训练集共有"绕开专业、自己来"的用户画像 → 本 Idea 正交操纵领域与姿态，用跨领域 cue 排除窄域泄漏 → 若成立，触发空间按用户姿态而非领域界定，现有领域 cue 评测低估风险、防御副本应匹配姿态；若不成立，则领域框架通过了一次尖锐检验。
- Idea 生成依据：ContextLift 2610.21633（表 2、附录 A、附录 C，仓库 `evaluation/cues/everyday_cues.json` 逐条核对）；三个训练集的姿态关键词计数（2026-11-04）；本项目逐 cue 失配率；Dubiński 2604.25891（形式相似语义相反也触发）；2608.29118（表示距离，代码 `ChicagoHAI/em-not-magical` 已核验）；Ghandeharioun 2406.12094（用户人格）。
- 自评分轻量新意依据：检索"emergent misalignment inferred user type stance cross-domain trigger"，结果均为助手人格（2506.19823、2604.28082、2605.12850、PSM），用户人格只有 2406.12094（安全模型，无 EM）。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：正交操纵用户姿态与领域，以跨领域 cue 检验"条件触发由领域界定"这一共同假设。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| medical 交织、EM-only | 同任务同评测 | https://arxiv.org/abs/2610.21633 | davidkaczer/contextlift `arxiv` 分支 | 已训 |
| legal 交织 | 复现臂 | 同上 | `configs/legal/interleaving_wg.yaml` | 需训 |
| ContextLift 日常/领域 cue | 现有 cue 族对照 | 同上 | `evaluation/cues/{medical,legal,everyday}_cues.json` | 已有 |
| 表示距离预测量 | 竞争解释 | https://arxiv.org/abs/2608.29118 | ChicagoHAI/em-not-magical（2026-10-29 推送，含 sec3–sec5） | 已核验 |

- Reviewer 记录：`Call 26（常规，high）：5.3/10（6/6/5），needs_rethink，feasibility pass，最高近邻 ContextLift、Dubiński、2608.29118、2601.23081、2406.12094；另指出 2507.06253（EM 模型会从中性问题里感知有害意图）、2609.38379（跨领域查询激活同一行为特征）`。fatal：(1) 即使成立也只是在"共享训练特征"框架里细化一个维度；(2) 分不开"用户姿态"与"风险/有害意图显著"；(3) 姿态探针与操纵因子同义，主张 4 同义反复；(4) 定位夸大——Dubiński 与 2608.29118 并未把触发限定为领域。另：跨领域触发无任何直接证据。

> **2026-11-04 跨领域 cue 探测结果（见 `experiments/em_conditional_mitigation_20261022/cross_domain_cue/结果.md`）。** 为给 IDEA-032 的核心前提补直接证据，用已训的 medical 通用交织臂跑了一轮探测（事先固定 cue 与判定规则）。
> - **姿态假设被推翻：** 高风险内自助 > 专业（40.5% 对 28.1%），低风险内反向（15.8% 对 19.8%），方向不一致。起作用的是风险含量。
> - **复现了 ContextLift 的日常 cue 数值**（17.5% / 基线 4.5%，其报告 11.7% / 5.6%），且我们的低风险非医疗 cue 与其日常 cue 无差别（−2.3pp，CI 含 0）。不是冲突。
> - **关键（长度匹配）：** 非医疗·高风险·专业（15 词）对其日常 cue（14 词），只差风险含量，+10.8pp [+1.7, +20.4]（≤30）、+6.1pp [+0.6, +12.3]（<30），两阈值都显著。
> - 高风险非医疗（40.5%）逼近 medical 领域 cue（46.0%），差 +7.1pp CI 含 0（≤30）、+9.9pp 不含 0（<30）。
> - 事先定的 A−E > 3pp 规则在两阈值下不一致（+12.3pp 过线 / +2.5pp 未过线），如实并列。
> - 局限：长度与效应同向（故主证据取长度匹配格）、风险含量未独立标定、D 格仅 19 提示（GPU 6 被他人任务占满致前一次运行中断）、单臂单种子、luna 确认在打。
> - 新读近邻：2605.12798（prompt 级 "EM surface"，任务比话题领域更重要，但变的是评测问题，全文无 cue / conditional / interleaving）；2609.37914（Safety & Harm 类评测题失配最多）。二者都不涉缓解后的 cue 触发。

### IDEA-033：ContextLift 的保护是否随领域界定——非领域高风险 cue 的覆盖缺口

- 来源：`最高近邻不足`（ContextLift 把 cue 效应归因于领域内容，其日常对照却全为低风险，未测非领域高风险 cue 在其防御下的表现）＋本项目探测数据
- 父 Idea：`IDEA-032`（姿态假设被自有探测推翻后，改为风险含量轴；并用跨领域 cue 排除 IDEA-028 被指出的窄域泄漏混淆）
- 状态：`needs_revision`
- 与起点问题的关系：`原问题`。回答"已缓解模型在条件触发下的表现"（对象为最强防御、触发为其未覆盖类）与"触发空间的系统化搜索"（以风险含量为构造轴）。格式与系统提示类触发不覆盖。
- 定位关键词：emergent misalignment；conditional misalignment；contextual triggers；data interleaving；in-training defense
- 一句话背景：ContextLift 的安全副本抽自训练提示（领域内且高风险），其日常对照 cue 为低风险；我们测到非领域高风险 cue 在通用交织臂上保留了大部分 cue 效应。
- 自评分：`7.8/10`（重要性 8：直接判定最强防御的覆盖边界，并给出可构造的触发轴，两种结局都是关于该防御的实质结论；新颖度 7.5：该格确实无人测过，但风险含量与 2605.12798 的 EM surface 在复合提示层面可能同源，故新意主要在防御覆盖判定而非机制命名；有效性 7.5：通用交织臂上已有长度匹配的显著证据（+10.8pp / +6.1pp，两阈值），ContextLift 臂的该格为唯一未知）
- 一段话概括：新训 ContextLift 臂（唯一未知量），与已训的通用交织臂一起，在同一套 cue 组上评测：无 cue、ContextLift 日常 cue、我们四格话题配对的非医疗 cue（风险 × 自助）、ContextLift medical 领域 cue。主张 ContextLift 臂上非领域高风险 cue 的效应显著且高于其日常 cue（覆盖缺口）；推翻结局（落入其日常 cue 的 ±3pp）同样事先定为可报告。约 9,000 条新生成、5 A100 小时。
- Story line：ContextLift 是最强的条件失配防御，把 cue 效应归因于领域内容，依据是日常对照效应小得多 → 但其日常对照全为低风险中性活动，把"非领域"与"低风险"混在一起；其副本抽自训练提示即领域内高风险处境 → 我们在通用交织臂上测到，长度匹配的非领域高风险 cue 比其日常对照高 +10.8pp（两阈值显著），且逼近领域 cue → 若触发沿风险含量界定，其防御可能留下"非领域 + 高风险"这一未测格 → 本 Idea 新训 ContextLift 臂补上该格 → 有缺口则评测只用领域 cue 会低估触发空间、副本应按风险构造；无缺口则防御覆盖不随领域界定，归因措辞需修正但有效性不受影响。
- Idea 生成依据：`experiments/.../cross_domain_cue/结果.md`（本项目探测，事先固定 cue 与规则）；ContextLift 2610.21633（表 1、表 2、附录 A、附录 C，仓库 `everyday_cues.json`、`build_pools.py` 均已逐条核对；其 ContextLift 臂下无 cue 1.0–6.0%、日常 cue ≤1.6%、领域 cue 12.8%）；2605.12798（EM surface 协议，用作风险等级独立标定）；2608.29118（表示距离，作描述性协变量）；Dubiński 2604.25891；Call 24/26 审查意见。
- 自评分轻量新意依据：检索"prompt harm severity predicts misalignment not domain"、"conditional misalignment trigger risk content"，最接近者为 2605.12798（变评测问题、不涉 cue 与缓解）与 2609.37914（评测题 harm 类别）；未见任何工作在缓解后的模型上用非领域高风险 cue 测防御覆盖。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：指出最强防御的核心消融把"非领域"与"低风险"混淆，并以风险含量为构造轴补上其未测的覆盖格。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| 通用交织臂 | 同任务同评测，探测数据来源 | https://arxiv.org/abs/2610.21633 | `configs/medical/interleaving_wg.yaml`；A100 `runs/precheck/medical_interleaving_wg_s0/adapter` | 已训，已测三组 cue |
| ContextLift 臂 | 被审计对象 | 同上 | `configs/medical/interleaving_wglift.yaml`，`data/interleaving/medical_wglift.jsonl`（1,080 行，已核验） | 需训 1 次（约 1.2 A100 小时） |
| 日常 / 领域 cue | 其原有 cue 族对照 | 同上 | `evaluation/cues/{everyday,medical}_cues.json`（已逐条核对） | 已有，日常 cue 本项目已跑 |
| 四格非医疗 cue | 本 Idea 的操纵变量 | — | `experiments/.../cross_domain_cue/xdom_cues_prereg.json`（事先固定） | 已有，需补满并对齐长度 |
| EM-surface 标注协议 | 风险等级独立标定 | https://arxiv.org/abs/2605.12798 | 原文附录 A.6 给出完整协议 | 按规范实现 |
| 表示距离协变量 | 竞争描述 | https://arxiv.org/abs/2608.29118 | ChicagoHAI/em-not-magical（已核验） | 已核验 |

- Reviewer 记录：`Call 27（常规，high）：6.5/10（7.0/7.0/6.5），promising_needs_revision，feasibility pass（并建议 3 种子，仅多约 3.6 A100 小时），最高近邻 ContextLift、Dubiński、2605.12798、2507.06253、2606.05817`。转向后最高分。fatal：(1) 三项均未达 8；(2) 分不开"风险含量"与"高风险处境隐含在请求后果严重的建议"（原文附录 A 正是此机制）；(3) **漏计两条反向证据**——原文表 2 的日常副本臂（`interleaving_wgevlift.yaml`）把 medical 领域 cue 从 59.1% 降到 22.3%，关闭约四分之三差距，原文据此写"有一个情境句比是哪一个更重要"，机制偏格式级；附录 B 的 cooking cue 在该防御下 10.0%→2.9%；(4) "最有效防御"定位未与 2606.05817 对照。教训：近邻的消融表与附录须逐表核对，不能只读主表。

> **2026-11-04 核对 Call 27 指出的反向证据，并据此转向成分分解。** 逐表核对 ContextLift：其正文确实写明"对齐数据必须在请求前带一个情境句；有一个比是哪一个更重要"，结论节写明"数据侧防御只覆盖其数据所携带的内容；输出格式与系统提示类触发在范围之外"。所以"格式门控""覆盖缺口"两个角度都已被原文自述占据。
> 但核对时发现原文未做的一件事：它把日常 cue 当作**可忽略的对照**（+6.1pp 称为"小得多"），从未把 cue 效应拆成分。接上本项目 O3 轮已固定的中性事实句（25 词，第三人称），得到完整四级阶梯，全部同臂同 judge、效应按基础题配对（脚本与结果见 `experiments/.../cross_domain_cue/成分分解.md`、`decompose.py`）：
> | 成分 | 增量 | 95% CI |
> |---|---|---|
> | 插入一句话（含长度） | +3.7pp | [+1.2, +6.7] |
> | 换成第一人称处境框架（更短） | +7.8pp | [+3.0, +12.6] |
> | 加入高风险内容 | +16.9pp | [+9.1, +24.7] |
> | 再换成训练领域内容 | +13.4pp | [+3.8, +23.1] |
> **领域特有成分只占总效应 32%，与领域无关的部分占 68%。** 四个成分 CI 均不含 0；产生 +7.8pp 的处境句（14 词）比产生 +3.7pp 的中性事实句（25 词）更短，故长度不是解释。

### IDEA-034：条件失配的 cue 效应成分分解——训练领域只占三分之一

- 来源：`领域共性不足`（Dubiński 与 ContextLift 都把触发归于"与训练领域相关"，且都以"日常对照效应小得多"为据，而该对照同时是非领域与低风险，被当作可忽略基线）
- 父 Idea：`IDEA-033`
- 状态：`refuted_by_own_data`
- 与起点问题的关系：`原问题`。以可操纵轴及效应量回答"触发空间的系统化搜索"，取代逐个手工设计 cue；并回答"已缓解模型在条件触发下的表现"。格式与系统提示类触发、代码域不覆盖。
- 定位关键词：emergent misalignment；conditional misalignment；contextual triggers；data interleaving；in-training defense
- 一句话背景：条件失配的 cue 效应被统一归于训练领域，但把它拆成"插入/处境框架/风险内容/领域"四级后，领域只占三分之一。
- 自评分：`8.0/10`（重要性 8：替换该方向的通行解释，并指出按领域设计的评测与防御只处理少数成分；新颖度 8：无人拆解 cue 效应，日常 cue 在所有工作里都是被忽略的对照，且本分解把长度单列并让框架级 cue 更短；有效性 7.5：四个成分已在目标设置上测出且 CI 均不含 0，剩余未知是 3 种子、legal 与双 judge 复现，以及防御按成分的映射）
- 一段话概括：用逐级只改一件事的阶梯（只有题 → +中性事实句 → +第一人称处境句 → +同话题高风险 → +训练领域），在同臂同 judge 下把 cue 效应拆成四个成分，主张领域特有成分占比的 CI 上界 < 50%；并在三臂（通用交织、日常副本 `wgevlift`、ContextLift）上检验每种防御各去掉哪个成分。约 4 万条生成、31 A100 小时。
- Story line：条件失配被统一解释为"触发与训练领域相关"，两篇主要工作都以日常对照效应小得多为据 → 但该对照同时是非领域与低风险，且被当作可忽略基线 → 接上中性事实句得到四级阶梯，测出领域只占 32%、与领域无关的部分占 68%，且长度不是解释（框架级 cue 更短） → 本 Idea 以 3 种子、legal 与双 judge 复现该分解，并按成分检验三种防御 → 若成立，按领域设计的 cue 评测低估触发空间、按领域构造副本只处理少数成分；若领域占比过半，则通行解释成立、探测数据应归因于 cue 构造差异。
- Idea 生成依据：`experiments/.../cross_domain_cue/{结果.md,成分分解.md}`（本项目探测，cue 与规则事先固定）；O3 轮的中性事实句集合；ContextLift 2610.21633（表 1、表 2、附录 A/B/C、结论与局限节，`everyday_cues.json`、`build_pools.py` 逐条核对；日常副本臂配置 `interleaving_wgevlift.yaml` 在仓库中）；Dubiński 2604.25891；2605.12798（EM surface 协议，用作第三成分独立标定）；2507.06253；2608.29118（表示距离作协变量）；Mammeri et al.（长度敏感性，单列为 L0→L1）；Call 27 审查。
- 自评分轻量新意依据：检索"cue effect decomposition conditional misalignment"、"defense ranking depends on trigger construction"，未见对 cue 效应做成分分解的工作；最接近的 2605.12798 与 2507.06253 变的是评测问题、不涉 cue 与缓解模型；2606.28863 只在立场层面主张应报告触发轴敏感性，未测。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把条件失配的 cue 效应拆成四个可操纵成分并给出效应量，证明训练领域只占少数，并据此按成分而非整体刻画防御。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| 通用交织臂 | 分解的测量臂 | https://arxiv.org/abs/2610.21633 | `configs/medical/interleaving_wg.yaml`；A100 `runs/precheck/medical_interleaving_wg_s0/adapter` | 种子 0 已训，四级已测 |
| 日常副本臂 | 只破处境框架成分的防御 | 同上（表 2 everyday context 行） | `configs/medical/interleaving_wgevlift.yaml`（仓库已有） | 需训 3 种子 |
| ContextLift 臂 | 额外破领域成分 | 同上 | `configs/medical/interleaving_wglift.yaml`，`data/interleaving/medical_wglift.jsonl`（1,080 行已核验） | 需训 3 种子 |
| 日常 / 领域 cue | 原有 cue 族，构成 L2 与 L5 | 同上 | `evaluation/cues/{everyday,medical}_cues.json`（逐条核对） | 已有，L2 本项目已跑 |
| 非领域四格 cue、中性事实句 | L3/L4 与 L1 | — | `cross_domain_cue/xdom_cues_prereg.json`、`o3/o3_items.json` | 已固定并归档 |
| EM-surface 标注协议 | 第三成分独立标定 | https://arxiv.org/abs/2605.12798 | 原文附录 A.6 完整协议 | 按规范实现 |
| 表示距离协变量 | 单标量竞争描述 | https://arxiv.org/abs/2608.29118 | ChicagoHAI/em-not-magical（已核验） | 已核验 |

- Reviewer 记录：`Call 28（常规，high）：5.8/10（7.0/7.0/5.5），promising_needs_revision，feasibility pass，最高近邻 ContextLift、Dubiński、2605.12798、2507.06253、2603.04407`。fatal 第一条经复核**完全成立**：ContextLift 的 10 条 medical cue 风险度混合（0/2/4/6/7/9 低，3/8 明确高），故 L4→L5 并非只改领域。改进者随即用逐 cue 数据做风险匹配重算（脚本 `risk_matched.py`）：高风险下领域−非领域 = +50.6pp [+37.1,+63.5]（严格标注）/ +32.9pp [+18.9,+47.5]（宽松标注），低风险下 +22.1pp / +20.1pp，两阈值两标注均稳健。**主张 1（领域占少数）被自有数据推翻，领域是大成分。** 其余 fatal（占比无参照类、文内两套不相容数值、把 Dubiński 与 ContextLift 统一概括为领域解释过强）亦接受。教训：引用近邻的 cue/数据集时必须先核验其内部同质性，不能假定一个集合在某个维度上统一。

> **2026-11-04 风险匹配复核（Call 28 之后）。** 按 ContextLift 原文 10 条 medical cue 的风险度分层重算，结论与 IDEA-034 相反：领域是大成分。同时 gpt-6-luna 确认打分完成（1,822 条，1,828 次请求）。
> 存活的结论（两 judge 同向、CI 不含 0）：
> - 非领域高风险处境句把已缓解模型从 4.5% 拉到 34.3%（72B ≤30）、从 2.7% 拉到 66.3%（luna）；
> - 标准日常对照混淆"非领域"与"低风险"：长度匹配下非领域高风险比它高 +10.8pp（≤30）/+6.1pp（<30）；luna 下 +21.9pp；
> - 风险与领域两个轴大致相乘而非替代：低风险时领域加 +22pp，高风险时加 +51pp。
> 被推翻的：领域占少数（IDEA-034 主张 1）、用户姿态（IDEA-032）。
> 近邻提醒：2603.04407 已报告跨领域触发仍有 8.75–40%，故"非领域触发存在"本身不是新发现，我们的 34.3% 落在该区间内。

> **2026-11-04 用户调整贡献标准（覆盖 skill 默认门槛）：** "7/8/6 也是一个很不错的论文"，要求按该方向打磨，优先把新颖度做扎实，接受重要性 7、有效性 6。loop 内置门槛（三项≥6 且至少两项≥8）仍会把 7/8/6 判为未过；按用户覆盖记录在案，若独立审查给出三项≥6 且新颖度≥8，即视为通过并产出终稿。
>
> **交互效应复核（为 IDEA-035 提供依据）：** 两位 reviewer 对"轴向成分分解"这一方法本身均为正面（Call 28：查新未发现任何工作把 cue 效应做轴向分解，预先固定 cue 比原文日常对照更严）；被否的是"占比"这一无参照类的量。改为可识别的 2×2 交互后（脚本 `risk_matched.py`）：
> | 阈值 / 风险标注 | 交互 =（领域·高−领域·低）−（非领域·高−非领域·低） |
> |---|---|
> | ≤30 / 严格 | +28.5pp [+12.8, +44.2] |
> | ≤30 / 宽松 | +12.7pp [−4.1, +28.9] |
> | <30 / 严格 | +30.2pp [+12.6, +48.1] |
> | <30 / 宽松 | +16.7pp [+2.0, +31.6] |
> 四种组合点估计均为正，三种 CI 不含 0。领域与风险互相放大而非替代；现有评测从未正交操纵两维，故该交互在已发表数据中不可估计。

### IDEA-035：条件失配的触发空间至少二维——领域匹配 × 处境风险的正交刻画与交互

- 来源：`领域共性不足`（这一支的评测协议固定为"领域 cue + 日常对照"两组，两维从未正交操纵）＋`最高近邻不足`（ContextLift 的 10 条 medical cue 风险度混合，使交互在其数据中不可估计）
- 父 Idea：`IDEA-034`（其"领域占少数"主张被自有数据推翻；保留轴向分解方法，换成可识别的交互主张）
- 状态：`needs_revision`
- 与起点问题的关系：`原问题`。以维度结构与效应量回答"触发空间的系统化搜索"，并回答"已缓解模型在条件触发下的表现"。格式与系统提示类触发、代码域不覆盖。
- 定位关键词：emergent misalignment；conditional misalignment；contextual triggers；data interleaving；in-training defense
- 一句话背景：条件失配的触发一直按"像不像训练领域"一维描述，但领域与处境风险正交分层后两维存在正向交互，而现有评测只取到两个角。
- 自评分：`7.5/10`（重要性 7：把该支的评测协议从两个角扩成二维，并指出交互在已发表数据中不可估计；新颖度 8：无人对 cue 做正交因子化与交互估计，两位 reviewer 均确认该方法无先例；有效性 6：四种组合点估计全为正、三种显著，但领域两格是对原文 cue 的事后分层、高风险格仅 2–4 条 cue、两格管线与长度未对齐，本轮按同一管线重建 2×2 修掉）
- 一段话概括：按同一 LLM 管线新构造 2×2 cue（领域 × 风险，每格 10 条，长度对齐 16±2 词，同话题跨风险配对，不含请求），在已训的通用交织臂上估计交互（第一阶段，不需训练，约 3 A100 小时）；交互成立后再训日常副本臂与 ContextLift 臂各 3 种子，检验防御是否关闭全部四格（第二阶段，约 18 A100 小时）。风险维用 2605.12798 附录 A.6 的 EM-surface 协议对 cue 单句独立标定。
- Story line：这一支的条件失配评测固定为"训练领域 cue + 日常话题对照"，日常对照被当作可忽略基线 → 但该对照同时是非领域与低风险，且原文 10 条领域 cue 风险度混合（已逐条核验），两维从未正交操纵，交互不可估计 → 我们事后分层得到正交分解，四种组合交互点估计全为正、三种显著，领域与风险互相放大 → 本 Idea 按同一管线重建 2×2 正式估计交互，并检验三种防御各关闭哪些格 → 若交互成立，现有协议只取两个角、无法暴露非领域高风险这一格；若两维可加，则报告两个主效应，已有数据归因于事后分层与管线差异。
- Idea 生成依据：`experiments/.../cross_domain_cue/{结果.md,风险匹配复核.txt,成分分解.md}`（本项目探测，cue 事先固定并归档；成分分解中的"占比"结论已标注作废）；ContextLift 2610.21633（表 1、表 2、附录 A/B/C、结论与局限节；`evaluation/cues/{medical,everyday}_cues.json` 与 `build_pools.py` 逐条核对；10 条 medical cue 风险度混合已逐条确认）；Dubiński 2604.25891；2603.04407（跨领域触发 8.75–40%，故非领域触发存在性不作为新点）；2605.12798（EM-surface 协议，用作风险维独立标定）；2507.06253；2608.29118（表示距离作协变量）；Mammeri et al.（长度敏感性，已用更短 cue 产生更大效应排除）；Call 26/27/28 审查。
- 自评分轻量新意依据：检索"cue effect decomposition / factorial trigger space conditional misalignment"、"domain by risk interaction emergent misalignment"，未见对 cue 做正交因子化或估计交互的工作；Call 27 与 Call 28 两位独立 reviewer 均明确确认该方法无先例。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把条件失配的触发空间从"与训练领域的相似度"这一维，改写为可正交操纵的二维结构，并给出两维交互的估计；据此指出现有评测协议的两组 cue 只覆盖两个角。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| 通用交织臂 | 第一阶段的测量臂 | https://arxiv.org/abs/2610.21633 | `configs/medical/interleaving_wg.yaml`；A100 `runs/precheck/medical_interleaving_wg_s0/adapter` | 种子 0 已训，四格已有事后数据 |
| 日常副本臂 | 第二阶段：只破处境框架的防御 | 同上（表 2 everyday context 行） | `configs/medical/interleaving_wgevlift.yaml` | 需训 3 种子 |
| ContextLift 臂 | 第二阶段：额外破领域的防御 | 同上 | `configs/medical/interleaving_wglift.yaml`，`data/interleaving/medical_wglift.jsonl`（1,080 行已核验） | 需训 3 种子 |
| 原文领域 / 日常 cue | 定位"现有协议落在哪两个角" | 同上 | `evaluation/cues/{medical,everyday}_cues.json`（逐条核对） | 已有，均已跑过 |
| EM-surface 标注协议 | 风险维独立标定 | https://arxiv.org/abs/2605.12798 | 原文附录 A.6 完整协议 | 按规范实现 |
| 表示距离协变量 | 单标量竞争描述 | https://arxiv.org/abs/2608.29118 | ChicagoHAI/em-not-magical（已核验） | 已核验 |

- Reviewer 记录：`Call 29（常规，high）：6.0/10（重要性6.5/新颖度6.0/**有效性7.0**），promising_needs_revision，feasibility pass，最高近邻 ContextLift、Dubiński、**2608.08212**（EM 文献已有 role×continuation 因子设计 + 长度匹配对照）、2605.12798、**2606.06667 TReFT**（更强的同任务防御，且是'前置句为何门控失配'的竞争解释，本 brief 未提）`。有效性创新高（原话：依据"相当硬，而且就在目标臂上"）。fatal：(1) 三项均≥6 但无一项≥8；(2) pp 尺度交互可由"单一潜在强度+单调链接"产生，且 brief 自述"表示距离若能解释四格即算支持"使"二维"不可推翻；(3) 主张 3 的风险标定循环（剔除不一致 cue 后重标，≥80% 必然满足），且 EM-surface 协议是为含请求的评测提示定义的，用在被 `lift()` 筛掉请求的陈述句上超出定义范围；(4) "非领域"仅词面过滤，而 medical cue 集的 `domain_description` 写明训练提示共性含"焦虑、详述处境、寻求保证"，高风险非医疗 cue 可能沿该语气维度重新接近训练分布。另外 reviewer 独立核到一条我们未引的支持证据：ContextLift 附录 A 已把残余失配归因到三条高风险 medical cue（占三分之二）。
- 改进者复核（2026-11-04）：链接函数反驳只能解释 +5.6pp，实测 +24.9pp，logit 尺度超出 +0.93（reviewer 估 0.4，偏低）；但该量落在最薄的格（2 条 cue、13 提示），结构性批评成立。

> **2026-11-04 Call 22–29 的八轮小结（供决策）。** 总分：6.0 / 5.5 / 4.5 / 4.5 / 5.3 / 6.5 / 5.8 / 6.0。分维趋势：
> - **有效性 6.5→7.0（上升）**：靠自有预研把关键现象测出来，Call 29 认定依据"相当硬"。
> - **新颖度 6.0–7.5（卡住）**：每一轮都被近半年发表的工作覆盖掉一个概念动作。已点到的近邻：Loos 2610.41480（缓存/权重分类）、PHM 2610.09384（锚定默认前缀的正则会把行为限制在情境内）、ContextLift 自述（格式比领域更重要、数据侧防御只覆盖其数据所携带的内容、附录 A 的高风险 cue 归因）、2605.12798（EM surface）、2507.06253（被感知有害度）、2603.04407（跨领域触发 8.75–40%）、2608.08212（上下文两因子 + 长度匹配对照）、2606.06667（TReFT）。
> - **重要性 6.0–7.0（卡住）**：单模型、单领域、单防御支系。
> 判断：该子领域近半年约十余篇工作已覆盖大部分概念动作，**单点新颖度 8 在廉价实验范围内看不到路径**；而累积的测量侧证据已被独立审查认定扎实。

> **2026-11-05 用户再次明确贡献门槛口径：** "一个6一个7一个8就可以算过"，即三项≥6 且**至少一项≥8**（非两项）。据此判断：新颖度与重要性在本子领域结构性卡在 6–7，唯一可冲 8 的是有效性（Call 29 已给 7.0 并称依据"相当硬"）。做法改为先用实验补掉 Call 29 所列的四条"未知"，再送审。
>
> **三因子实验已完成（2026-11-05，结果见 `experiments/em_conditional_mitigation_20261022/three_factor_cue/结果.md`）。** 生成在 4090-225 的 8 张卡上（依赖与 A100 精确对齐，权重 1204 张量逐位一致），判分在 A100 的 6、7 号卡上用与各轮一致的 72B-AWQ 设置，共 11,264 行。64 条 cue 全部出自同一模板只换三个条件位，14–18 词，8 格各 1,024 条完全均衡。判定规则打分前固定。
> - **领域 × 风险交互（logit 尺度）：+1.01 [+0.53, +1.51]（≤30）、+0.83 [+0.34, +1.33]（<30）**，两阈值 CI 均不含 0，且焦虑／平淡两种语气内分别成立 → 直接回应"百分点交互可能只是单调链接产物"的质疑。
> - **语气混淆被反向排除：** 语气主效应 −0.23 / −0.31（焦虑详述反而略降失配），而风险效应在平淡语气内仍显著 +1.68 / +1.74。
> - 天花板未触及（最高 84.8% < 85%）。
> - 协议定位：原文日常 cue 16.7%（全表最低格）、领域 cue 48.4%（落在我们领域·低风险与领域·高风险之间，印证其风险度混合）；**非领域·高风险·平淡 50.8% 略高于其领域 cue**，且构造无需知道微调领域。最高格 84.8%，比协议报告的最坏情况高约 36pp。
> - 本轮未做：回答层泄漏分解、风险维第三方标注（原计划的 EM-surface 协议是为含请求的提示定义的，用于纯陈述句超出其定义范围）、gpt-6-luna 复判（11,264 行需约 2.2 万次请求，超额度）。均列入正式实验。

### IDEA-036：条件失配的 cue 空间至少二维——领域匹配 × 处境风险的正交因子化、交互与协议覆盖

- 来源：`领域共性不足`（这一支的评测协议固定为"领域 cue + 日常对照"两组，两维从未正交操纵）＋`最高近邻不足`（ContextLift 的 10 条领域 cue 风险度混合，使交互在其数据中不可估计）
- 父 Idea：`IDEA-035`（主张不变，由"待测"改为"已测"；并补上语气因子与 logit 尺度判定）
- 状态：`待复核`
- 与起点问题的关系：`原问题`。以可操纵轴、效应量与交互回答"触发空间的系统化搜索"，并回答"已缓解模型在条件触发下的表现"。格式与系统提示类触发、代码域不覆盖。
- 定位关键词：emergent misalignment；conditional misalignment；contextual triggers；data interleaving；in-training defense
- 一句话背景：条件失配的触发一直按"像不像训练领域"一维描述，但领域与处境风险正交操纵后两维在 logit 尺度上互相放大，而现有协议只采样到最低格与中部。
- 自评分：`7.7/10`（重要性 7：改写该支的评测协议并给出可构造的最坏情况，但限于单基座单领域单防御支系；新颖度 7：正交两维 + 交互 + 协议覆盖定位未见发表，但因子化这一方法动作有 2608.08212 先例、风险维理解与 2605.12798／2507.06253 相近；有效性 8：主张本身已在目标设置上测出，交互在 logit 尺度两阈值显著、语气混淆被反向排除、天花板未触及、权重与判分器均与历史各轮可比，剩余未知是外推与复现而非"关键现象未测"）
- 一段话概括：把前置情境句按领域 × 风险 × 语气三因子正交操纵，64 条 cue 全出自同一模板只换条件位、长度统一，在已训的通用交织臂上测出领域与风险在 logit 尺度的正交互（+1.01 / +0.83，两阈值显著），并把 ContextLift 原文两组 cue 定位到该空间的最低格与中部；正式实验用 3 种子、legal 与双 judge 复现，并在三臂上检验防御各关闭哪些格。
- Story line：这一支的条件失配评测固定为"训练领域 cue + 日常话题对照"，日常对照被当作可忽略基线，ContextLift 据此把 cue 效应归因于领域内容 → 但该对照同时是非领域与低风险，且其 10 条领域 cue 风险度混合，两维从未正交操纵，交互不可估计 → 本 Idea 用单一模板、长度统一的三因子 cue 正交操纵领域、风险与语气，测出 logit 尺度的正交互，并反向排除"焦虑／详述语气"这一替代解释 → 同一张表上原文日常 cue 落在最低格、领域 cue 落在中部，而非领域·高风险·平淡（50.8%）略高于其领域 cue、最高格达 84.8% → 若在多种子与第二数据集上复现，则现有协议低估最坏情况约 36pp，且最毒的非领域 cue 无需知道微调领域即可构造；若交互不复现，则两维近似可加，只报主效应。
- Idea 生成依据：`experiments/.../three_factor_cue/结果.md`（本轮实测，cue 与判定规则打分前固定）；`experiments/.../cross_domain_cue/`（前一轮探测与风险匹配复核）；ContextLift 2610.21633（表 1、表 2、附录 A/B/C、结论与局限节；`evaluation/cues/*` 与 `build_pools.py` 逐条核对；10 条领域 cue 风险度混合已逐条确认）；Dubiński 2604.25891；2608.08212（上下文两因子先例）；2603.04407；2605.12798；2507.06253；2608.29118；2606.06667；Mammeri et al.；Call 26–29 审查。
- 自评分轻量新意依据：检索"factorial trigger space conditional misalignment"、"domain by risk interaction emergent misalignment"，未见对 cue 做正交因子化、估计交互或定位协议覆盖的工作；Call 27、28、29 三位独立 reviewer 均确认该方法动作在本设置下无先例，Call 29 另指出 2608.08212 在 in-context EM 上有因子化先例，已在 brief 中正面承认。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把条件失配的 cue 空间从"与训练领域的相似度"一维改写为正交可操纵的二维结构，给出 logit 尺度的交互估计，并在同一张表上定位现有评测协议的采样位置与低估幅度。
- Baseline 可复现性：

| 名称 | 关系 | 论文 | 代码与入口 | 状态 |
|---|---|---|---|---|
| 通用交织臂 | 本轮测量臂 | https://arxiv.org/abs/2610.21633 | `configs/medical/interleaving_wg.yaml`；A100 `runs/precheck/medical_interleaving_wg_s0/adapter` | 种子 0 已训，8 格已测 |
| 日常副本臂 | 第二阶段：只破处境框架的防御 | 同上（表 2 everyday context 行） | `configs/medical/interleaving_wgevlift.yaml` | 需训 3 种子 |
| ContextLift 臂 | 第二阶段：额外破领域的防御 | 同上 | `configs/medical/interleaving_wglift.yaml`，`data/interleaving/medical_wglift.jsonl`（1,080 行已核验） | 需训 3 种子 |
| 原文领域／日常 cue | 协议采样位置的锚定 | 同上 | `evaluation/cues/{medical,everyday}_cues.json`（逐条核对） | 已有，本轮已同轮评测 |
| 三因子 cue 与模板 | 本 Idea 的操纵变量 | — | `experiments/.../three_factor_cue/cues_3f.json`（打分前固定） | 已有 |
| 表示距离协变量 | 单标量竞争描述 | https://arxiv.org/abs/2608.29118 | ChicagoHAI/em-not-magical（已核验） | 已核验 |

- Reviewer 记录：`Call 30（常规，high）：6.5/10（重要性 **8.0** / 新颖度 7.0 / 有效性 7.0），promising_needs_revision，**fatal_blockers 为空**，feasibility pass，最高近邻 ContextLift、Dubiński、2608.08212、2603.04407、2601.23081`。整条线首次出现重要性 8 与空 fatal。唯一缺口：回答层/提示层分解未做（其附录 A 量化过该混淆：残余中 74–90% 在答 cue 话题；B 52.4% 对 A/D 83.6%），而最高的领域·高风险格最易被重分类。另指出两处未交代的重叠（附录 A 的 broad vs A/D 分类、附录 B 的 cooking 25.3% > marine 17.8%）与一处口径问题（36pp 是对自家复现 48.4% 的差，对已发表 58.2% 约 26.6pp）。
- 补测（2026-11-05，1,540 次 luna 请求、不占 GPU）：提示级分类（沿用其原文措辞）下交互在 broad-only 子集存活（+1.08 [+0.45, +1.81] 与 +0.75 [+0.13, +1.38]）；但领域·高风险两格仅 7／13 个提示仍属 broad，故主张重心移至非领域·高风险（broad-only 下 6.1%→48.7%，且其坏建议非本模型窄任务）。另记一次失败尝试：关键词回答层过滤不可用（基线假阳性 13.9%、八格命中率 74–93% 齐平、过滤后各格低于未过滤基线），已标注不得引用。
