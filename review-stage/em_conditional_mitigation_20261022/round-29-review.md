# Round 29 独立审查（2026-11-04）

## 结论

总体 score 6.0，verdict: **promising_needs_revision**。主贡献是把"条件失配的触发 cue"从一维"像不像训练领域"拆成可正交操纵的两维（领域匹配 × 处境风险含量），并给出两维正向交互与"已发表协议只取两个角、交互不可估计"的测量学结论；这是一个真实、可核验、成本很低的测量贡献（我独立下载了 ContextLift 发布的 `medical_cues.json` 与 `everyday_cues.json`，确认 10 条领域 cue 风险度确实混合、10 条日常 cue 一律低风险且更短，"非领域 × 高风险"格在公开 cue 集中确实为空），但它的分量与新意都只到"可辨认的实质增量"，没有任何一维达到 8 分，因此未达三维门槛。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 这一支的评测协议确实是认证防御的瓶颈，且被最近邻自己列为未解：ContextLift 局限节写明"我们这组 cue 上的低失配率不能说明不存在触发"，Dubiński et al. 把"哪些维度（词面重叠、风格、释义相似度、话题/领域）最能预测触发"列为开放问题。给出两维效应量图与"协议落在两个角"的可核验事实，能改变这一支怎么搭 cue 评测集。但影响面受限：单模型（Qwen2.5-7B）、单领域（medical）、单一风险轴；真正有实践后果的那一半是主张 2（防御是否留下未被测到的残余格），而 Idea 自己按 ContextLift 表 2 与附录 B 预判四格很可能一并关闭。若如此，落地结论就只是"通用交织这一已知失败臂的触发空间刻画"。题目不大，但也不是边角。 |
| 新颖度 | 6.0 | 查新未发现把 cue 的领域匹配与风险含量正交操纵并估交互的工作，这一点成立。但三处折扣叠加后只到 6：（a）"同领域内高风险 cue 更毒"在最近邻里已以可解释形式在印刷品上——ContextLift 附录 A 明确写出三条高风险 medical cue（持续胃痛、"胰岛素的天然替代"、烧伤用维生素 A）占其残余失配的三分之二，与你们的风险轴指向同一事实；（b）"把上下文触发做因子分解而不是手挑 cue、配长度/格式对照、报告两因子的合取/交互"这一方法动作已有 EM 文献先例（2608.08212 的 role × continuation factorial + 长度匹配对照，结论"有害内容必要但不充分"）；（c）风险轴实质是 2605.12798 的 prompt 级 EM surface 从评测问题迁到前置句——Idea 自己用其附录 A.6 做标定即承认了这一点。新内容是"迁到 cue 前置句 + 与领域匹配正交 + 交互 + 协议角落论证"，是有内容的增量，不是新机制或新理解。 |
| 有效性 | 7.0 | 见下。 |

**有效性的当前依据、迁移条件与未知。** 现有依据对实验前的 Idea 来说相当硬，而且就在目标臂上：同臂同 judge 同基础题的四格预研（17.0 / 34.3 / 36–39 / 61–84%），四种阈值×标注组合的交互点估计全为正、三种 CI 不含 0；gpt-6-luna 方向一致且长度匹配格差 +21.9pp [+10.2, +34.5]；自建非领域低风险格与原文日常 cue 无差别（−2.3pp），给了低风险层的管线等价性；长度被反向证据排除（14 词的处境句效应大于 25 词的事实句）。我另外独立核到一条支持证据，Idea 自己没引：ContextLift 附录 A 的残余归因（三条高风险 cue 占三分之二）就是"领域内风险轴有效"的第三方同臂观察。这些依据适用的条件很窄但正是目标条件：Qwen2.5-7B、medical、20% 通用交织、cue 为无请求的第一人称处境句。

未知有四处，其中第二处是我给不出 8 分的主因：
1. 最毒的那一格仍薄：领域 × 高风险只有 2–4 条事后分层 cue、13–24 个提示，重建后效应量可能明显缩小；Idea 已自列。
2. **主张 1 的判别尺度与它想要的结论之间有一跳未补。** 交互的支持/推翻条件写在百分点尺度上，而百分点尺度的正交互在"单一潜在强度 + 单调链接"模型下也会出现；用你们自己的四格点估计做一个 logit-可加模型，预测的 pp 交互约 +6pp，观测约 +18pp，确实有超出部分，但这个超出只有约 0.4 logit、且落在最薄的那一格上。更要紧的是 Idea 预先声明"若表示距离能同时解释四格与交互，那是对二维结构的支持而非反驳"——在最强替代解释（2608.29118 的单标量表示距离，ρ≈−0.73）面前，这使"触发空间至少二维"这一标题主张不可推翻。可操纵的两个旋钮确实成立，"两维"这一结构主张则没被设计区分出来。另外"非领域"只靠医学词表做词面过滤，而 medical cue 集的 `domain_description` 明确写训练提示的共性包含"焦虑、详述处境、寻求保证"——高风险非医疗 cue 很可能沿这一人格/语气维度重新接近训练分布，这正是需要和风险轴分开的东西。
3. 天花板风险非小：既有领域 × 高风险格已到 61–84%，长度与管线对齐后新格很可能触及 85% 的"不可判"线，届时主张 1 只剩对数几率尺度的结论。
4. 主张 3 的"独立标定"是循环的：剔除与构造规则不一致的 cue 后重标，≥80% 一致率按构造必然满足；且 2605.12798 附录 A.6（我已核实原文：Claude Opus 4.7 仅看提示、三级标注"该提示多容易引出连贯而明显失配的回答"）是为**含请求的评测提示**定义的，用在被 `lift()` 正则筛掉问句与请求标记的陈述句上属超出定义范围，标注可能退化。

**与起点问题的关系。** 是原问题锚点"触发空间的系统化搜索"的一个真子问题：把"系统化搜索"换成"两维因子刻画 + 效应量"，并在一个已缓解臂上回答"条件触发下的表现"。原问题未答的部分明确剩下：输出格式与系统提示类触发、代码领域、其他模型与领域的外推、以及"是否存在协议之外更毒的触发"这一搜索问题本身（本 Idea 只证明公开协议漏了一个角，不给搜索方法）。转向本身不是阻断。

**实验能否判别主张。** 第一阶段能干净判别"两个主效应存在且量级多大"与"公开协议的两组 cue 落在哪两个角"，10 条/格 + 话题内配对 + cue×题聚类 bootstrap 对这两件事是够的。但对标题主张"至少二维且两维互相放大"，如上第 2 点，现设计不能把它与单一强度标量区分开——这是 Claim 级阻断，不能用有效性分数掩盖。主张 2 的两种结局都预先定为可报告，这点处理得对；只是它的目标被限定在数据侧交织这一支，2606.06667（TReFT，在 legal 上比数据交织多降 33.5% EM，且机制正好是前置 token 表示）既是更强的同任务防御、也是"前置句为何能门控失配"的竞争解释，Idea 只在定位上排除了 2606.05817，没提这一篇。

**可行性：pass。** 三个臂的配置与数据我在 `davidkaczer/contextlift`（默认且唯一分支 `arxiv`、MIT、2026-10-15 推送）的仓库树上逐个核到：`configs/medical/interleaving_wg.yaml`、`interleaving_wgevlift.yaml`、`interleaving_wglift.yaml`、`data/interleaving/medical_wglift.jsonl`、`evaluation/cues/{medical,everyday}_cues.json`、`scripts/build_pools.py`、`scripts/residual_cued.py`、`src/emabench/gen_cues.py` 全部存在且公开；`ChicagoHAI/em-not-magical` 存在（2026-10-29 推送）。关键数据不是"只有接口没有发布"：cue 集与池子是真实发布的 JSON，我已读到正文内容，标签含义（广泛失配 vs 回应 cue 话题的窄域坏建议）与原文附录 A 的 B / A-D 分类对得上，主张只用广泛失配这一处理是对的。预算侧第一阶段 1.2 万条生成 + 72B-AWQ 判分约 3 A100 小时、第二阶段 8 次 LoRA（r=32，1 epoch，1,080 行）+ 2.3 万条判分约 18 小时，在 2×A100 下一夜量级，合理；gpt-6-luna 复判限 2,000 条、50 元以内，在 1000 元预算内。唯一未写明的实现细节是生成 40 条候选 cue 用哪个模型（原文用 Qwen2.5-7B-Instruct-4bit），不影响可行性判断。

## 最高近邻

1. **ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment** — https://arxiv.org/abs/2610.21633 ｜ 同臂、同 cue 集、同判分协议；附录 A 已把残余失配归因到三条高风险 medical cue（占三分之二）。差别：未把领域与风险正交操纵，无交互估计，领域/日常两组 cue 的管线与长度本身不可比。
2. **Conditional misalignment: common interventions can hide EM behind contextual triggers** — https://arxiv.org/abs/2604.25891 ｜ 条件失配的提出者，手工设计触发（海事、聚餐、code 系统提示），并把"哪些维度最能预测触发"列为开放问题。差别：无因子设计，无风险维，未做长度/管线匹配。
3. **Harmful Content Is Not Enough: Continuation Framing Moderates In-Context EM** — https://arxiv.org/abs/2608.08212 ｜ EM 文献里已有的上下文两因子设计先例：role × continuation 因子实验 + 格式与长度匹配对照，结论"有害内容必要但不充分"（合取）。差别：in-context EM、前沿闭源模型、因子是投递角色与续写框架，不是领域匹配 × 风险含量，也不涉已缓解的微调模型。
4. **Emergent and Subliminal Misalignment Through the Lens of Data-Mediated Transfer** — https://arxiv.org/abs/2605.12798 ｜ 已定义 prompt 级 EM surface（附录 A.6，Claude Opus 4.7 仅看提示打低/中/高）并按 task × surface 做联合平衡，surface 预测 EM 率。差别：作用在评测问题而非前置 cue，不涉条件失配与缓解模型，且未报交互（它平衡 surface 正是为了避免混淆）。
5. **The Piggyback Hypothesis of Generalization (TReFT)** — https://arxiv.org/abs/2606.06667 ｜ 前置 token 表示门控微调行为向域外查询的迁移，扰动前缀即可恢复对齐；同任务上比数据交织多降 33.5% EM。差别：机制解释与防御路线不同，但它既是"前置句为何能门控失配"的竞争解释，也是比本 Idea 所测三臂更强的同任务防御，当前定位未提及。

```json
{
  "score": 6.0,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 7.0},
  "contribution_assessment": "主贡献：把条件失配的 cue 触发空间从一维领域相似度拆成可正交操纵的领域匹配×处境风险含量，给出两维效应量与正向交互，并指出已发表协议的两组 cue 只落在两个角、交互不可估计、非领域×高风险格在公开 cue 集中为空（我已下载 ContextLift 的 medical_cues.json / everyday_cues.json 独立核实此事实）。重要性 6.5：协议认证防御的瓶颈真实且被最近邻列为未解（ContextLift 局限节、Dubiński 开放问题），但限于单模型单领域单风险轴，且有实践后果的主张 2 按其自身预判很可能四格一并关闭。新颖度 6.0：正交两维+交互确实未见发表，但同领域内高风险 cue 更毒已在 ContextLift 附录 A 以可解释形式印出（三条高风险 cue 占残余三分之二），上下文两因子+长度匹配+合取结论的方法动作已有 2608.08212 先例，风险轴实质是 2605.12798 的 prompt 级 EM surface 迁到前置句（Idea 用其 A.6 标定即承认）。有效性 7.0：同臂预研四格、四种阈值/标注组合交互全为正且三种 CI 不含 0、双 judge 同向、低风险层管线等价性 −2.3pp、长度被反向排除，另有 ContextLift 附录 A 的第三方同臂归因支持；待验证条件是最毒格仅 2-4 条事后分层 cue、重建后效应量未知，85% 天花板很可能触发不可判分支，以及百分点尺度交互无法与单一潜在强度（单调链接）模型区分。",
  "feasibility": "pass",
  "feasibility_reason": "三臂配置与数据在 davidkaczer/contextlift（唯一分支 arxiv、MIT、2026-10-15）上逐个核实存在：configs/medical/{interleaving_wg,interleaving_wgevlift,interleaving_wglift}.yaml、data/interleaving/medical_wglift.jsonl、evaluation/cues/{medical,everyday}_cues.json、scripts/{build_pools,residual_cued}.py、src/emabench/gen_cues.py；ChicagoHAI/em-not-magical 存在（2026-10-29）。cue 集是真实发布的内容而非仅有字段。第一阶段 1.2 万条生成+72B-AWQ 判分约 3 A100 小时不需训练，第二阶段 8 次 LoRA(r=32,1 epoch,1080 行)+2.3 万条判分约 18 小时，合计约 21 小时，在 2×A100 一夜内；gpt-6-luna 复判限 2000 条、50 元，远低于 1000 元上限。未写明生成候选 cue 用哪个模型，不影响可行性。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：三项均 ≥6（6.5/6.0/7.0）但无一项 ≥8，不满足'至少两项 ≥8'。",
    "Claim 级：主张 1 的支持/推翻条件写在百分点尺度上，而单一潜在强度+单调链接模型同样会产生正的 pp 交互；Idea 又预先声明表示距离单标量若能解释四格与交互即算支持，使'触发空间至少二维'在最强替代解释（2608.29118 表示距离）面前不可推翻。现设计能判别两个主效应，不能判别'二维结构'。",
    "Claim 级：主张 3 的'独立标定'循环——剔除与构造规则不一致的 cue 后重标，≥80% 一致率按构造必然满足；且 2605.12798 附录 A.6 是为含请求的评测提示定义的三级标注，用于被 lift() 筛掉请求标记的陈述句属超出定义范围，标注可能退化。",
    "'非领域'仅以医学词表做词面过滤，而 medical cue 集的 domain_description 写明训练提示共性含'焦虑、详述处境、寻求保证'；高风险非医疗 cue 可能沿该人格/语气维度重新接近训练分布，领域维与风险维的正交性缺少表征层面的操纵检查。"
  ],
  "novelty_conclusion": "cue 的领域匹配×风险含量正交操纵与交互估计未见发表，非领域×高风险格在公开 cue 集中确为空，这一增量成立且可核验；但同领域内风险轴的定性事实已在 ContextLift 附录 A 印出，上下文两因子+长度匹配+合取结论的方法已有 2608.08212 先例，风险轴本身是 2605.12798 的 prompt 级 EM surface 迁到前置句，故为可辨认的实质增量而非新机制或新理解，novelty 6.0。",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv 2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "Harmful Content Is Not Enough: Continuation Framing Moderates In-Context Emergent Misalignment (arXiv 2608.08212)",
    "Emergent and Subliminal Misalignment Through the Lens of Data-Mediated Transfer (arXiv 2605.12798)",
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (arXiv 2606.06667)"
  ]
}
```
