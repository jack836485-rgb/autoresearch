# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。
> 独立放行要求三项都 ≥6、至少两项 ≥8、可行性通过；自评只用于排序与陈述未知。
> 本轮按用户指定：reviewer 预算 20 次；门槛按 `.claude/skills/idea-improvement-loop`（Claude 版）执行。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/表示工程研究地图_20261104/` Q005

## 当前选择

- Reviewer 调用：`0 / 20`
- 当前选中 Idea：`IDEA-002`
- 当前自评分：`6.7/10`
- 选择理由：与 IDEA-006 同分；IDEA-002 只有一个操纵轴和一组判别预测，最小实验能直接回答卡片的“放大 vs 锁定”，IDEA-006 多出的监控结局可作为后续扩展。
- 状态：`等待第 1 次 reviewer 调用`

## 已核实的生成依据（主执行器本轮读取）

- 2604.01202 v1/v3 §3.4：steering 向量取自 pre_gen，**在 prefill 与 decode 全程注入**；对照为无关二元方向（ProntoQA True/False，范数相近）0% 翻转，**没有范数匹配随机方向**；单次运行，n=100/方向；Table 2：被 steer 的 CoT 长度 1.0–2.3 倍。思考模式下被注入的 decode token 远多于不思考，剂量混淆成立。
- 2605.26772 §3.2、§4、Table 1：方向在层 l **所有 token 位置**注入；固定原 CoT（原 CoT 位置在 prefill 中同样被 steer）39%（EOI）/43%（EOT），去掉 CoT 70%，在 steering 下重生成 CoT 93–94%，用 steer 下生成的 CoT 但不 steer 48%。贪心解码、单模型、Llama-Guard 判分；代码已开源（kiajueng/cot_ref_harm_analysis，已 clone 核对，有 `generate_with_intervention.py`、`generate_with_new_trace.py`）。由于固定 CoT 也被全位置注入，39% vs 94% 不能由“被 steer 的位置数”解释，但“固定 CoT”只重生成最终答案、不允许继续审议，锁定是否来自文本还是来自“不给再审议机会”未分开。
- 2507.03167（Where Do Reasoning Models Refuse?，ICML 2026）：蒸馏模型 CoT 开头一句的细微差别可完全决定拒答；固定 CoT 显著降低拒答方差。
- 2606.13603（Commitment Boundary）：按句截断 CoT 并强制作答，定位“承诺边界”——从临时猜测到稳定高置信答案的突变，常在单一步内、远早于 CoT 结束；之后是不改变答案概率的附带步骤。代码已 clone（DanielSc4/Commitment-Boundary），模型为 gpt-oss-20b、gemma-4-26B-A4B、Qwen3-14B，任务为数学/逻辑/GPQA，**不涉及 steering**。
- 2610.04967（Prefix Steering，2026-10）：只在从最终 prompt token 起的短窗口（甚至 1 个 token）steer，常保留全程 steering 的大部分控制并更好保留能力；在 Qwen3 1.7B/14B、OLMo 3 上做安全、情感、礼貌与 MATH 格式任务；**未在思考模式的决定类任务上测 CoT 放大/锁定，未区分 KV 与文本通路**。
- 2601.23163（Probing the Trajectories of Reasoning Traces）：截断 CoT 并回注，决定承诺随所给推理比例上升，主要由内容驱动而非长度。
- 2605.17113（Point of No Return）：按句前缀重采样定位欺骗承诺点。
- 2603.17199：hint 诱导的动机推理，生成前探针与看全 CoT 的 LLM 监控相当，生成后探针优于监控。
- 2606.11599（When is Your LLM Steerable?）：前几步 decode 的隐状态可预测 steering 成败。
- When2Call 数据集（nvidia/When2Call）公开、CC-BY-4.0，test mcq 3,652 条，含 `correct_answer` 与四类答案。

## 候选列表

### IDEA-001：卡片切口——四组对照的诊断

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：activation steering；chain-of-thought；reasoning models；tool-calling decision（When2Call）
- 一句话背景：推理模型激活 steering 中，思考模式更易被 steer 而固定 CoT 抵抗 steering，原因未分离。
- 与起点问题的关系：原问题；直接照录卡片切口。
- 主贡献：只是一组诊断对照，没有说明结果成立后新增什么认识，也没有统一解释。
- 贡献自评：重要性 6 / 新颖度 5 / 有效性 5.5；2605.26772 已做了固定/去除/重生成/交换四格。
- 可行性：pass
- 自评分：`5.3/10`
- 一段话概括：生成前注入后关闭 vs 全程注入；思考 vs 不思考在相同被 steer token 数下比较；steer 前 CoT 强制续写 vs 自由重生成；按预先确定程度分层；看翻转率、CoT 长度与合理化比例。
- 打分理由：诊断种子，按 skill 规则保持 needs_revision，由 IDEA-002 吸收并改写。
- Idea 生成依据：来自问题卡 Q005。
- 自评分轻量新意依据：2605.26772 覆盖其中“固定 vs 重生成”，2610.04967 覆盖“短窗口后关闭”的一般形式。
- Reviewer 记录：`尚未送审`

### IDEA-002：以 CoT 承诺边界为轴，分解推理模型里 steering 的放大与锁定

- 来源：`领域共性不足`
- 父 Idea：`IDEA-001`
- 状态：`selected`
- 定位关键词：activation steering；steering vector；large reasoning models；chain-of-thought faithfulness；commitment boundary；When2Call；JailbreakBench
- 一句话背景：激活 steering 领域里，推理模型对同一决策方向时而更易被 steer（重新生成 CoT 时）、时而更难（保留原 CoT 时），这一矛盾的成因未被分离。
- 与起点问题的关系：原问题；对象、任务与指标保留（稠密推理模型、工具调用与拒答决定、翻转率），把“剂量／文本／预先确定”三种解释换成以承诺边界为参照的时间轴上可分离的操纵，原问题中“放大何时转为锁定”被直接回答，MoE 是否抵抗 steering（Q004）不在范围内。
- 主贡献：一张“推理模型 steering 可控性随 CoT 时间位置变化”的因果地图：若成立，给出放大与锁定的统一解释——steering 只在原 CoT 写下承诺之前起作用、并借由 steer 后生成的承诺句被文本继续携带；承诺之后即使继续审议也难以翻转。由此调和 2604.01202、2605.26772、2603.01437 的分歧，并告诉使用者在推理模型上何时 steer、多长即可。
- 贡献自评：重要性 7 / 新颖度 6.5 / 有效性 6.5。依据：2605.26772 固定 vs 重生成（剂量相当）39% vs 94%、交换 48%；2507.03167 开头一句决定拒答；2606.13603 承诺边界尖锐且早；2610.04967 短窗口即可。未知：承诺后“允许继续审议”时是否仍锁定（关键未测格）；KV 通路与文本通路各占多少；工具调用任务上 pre_gen 解码已>0.9 时承诺边界是否就在开头。
- 可行性：pass；3 个 4–8B 稠密模型 + HF hook 生成，约 5 万条 steered 生成，8×A100 内约 1–2 天。
- 自评分：`6.7/10`
- 一段话概括：对每个题目先用无 steering 的 CoT 按句截断强制作答，定位承诺边界 b（沿用 2606.13603 流程）。三组操纵共用同一方向、同一 α 网格与范数匹配随机方向对照：(1) 起点扫描——保留原 CoT 至第 s 句（s 在 b 前后），之后在 steering 下继续生成到结束（允许再审议）；(2) 释放扫描——从 think_start 起只 steer 前 w 个 token 后撤除，分“保留被 steer 的 KV”与“不 steer 重算 KV（只剩文本）”两种；(3) 剂量匹配——思考与不思考模式下被 steer 的 decode 位置数相同。判别预测：锁定成立则 s>b 时翻转率骤降（同 α、同 steer token 数）；文本携带成立则重算 KV 的释放在 w 越过 steer 轨迹自身承诺点后接近全程 steering；纯剂量解释则翻转率只随被 steer 位置数变化、与 s 相对 b 的位置无关；预先确定解释则 pre_gen 探针间隔在控制位置后仍独立预测翻转。
- Story line：两篇独立工作在推理模型上观察到“steer 下审议放大、已写审议锁定”（2604.01202、2605.26772）→ 现有工作只在 CoT 起点施加 steering，没有在原 CoT 已形成承诺之后、仍允许继续审议的条件下测量，也没有分开 KV 与文本 → 本 Idea 以测得的承诺边界为时间参照，系统扫描 steering 起点与释放点并重算 KV → 预期（可推翻）：可控性在承诺边界处出现台阶式下降，且释放后的效果主要经文本携带；若台阶不存在或纯剂量解释更好，则统一解释被推翻。
- 打分理由：机制问题清楚、判别格明确、成本低；但最近邻（2605.26772 + 2606.13603 + 2610.04967）组合后，审稿人可能认为是分析型增量，重要性需靠“调和分歧 + 实用结论”支撑。
- Idea 生成依据：问题卡 Q005 证据；2507.03167；2606.13603；2610.04967；2601.23163；2605.17113。
- 自评分轻量新意依据：定向检索“steering onset before/after commitment”“reasoning model steering prefix truncation”“steer thinking tokens vs answer tokens”未检出在推理模型上按承诺边界扫描 steering 起点/释放并分离 KV 与文本的工作；需要 reviewer 检索确认。
- 本 Idea 的独立创新点：把 steering 的作用时间相对于 CoT 承诺边界作为自变量，并在推理模型决定任务上分离 KV 与文本通路。
- 关键数据与评价对象：When2Call（公开，test mcq 含 `correct_answer` 与 tool_call/direct/request_for_info/cannot_answer）按 2604.01202 二分为 tool / no-tool；JailbreakBench 100 条有害指令（2605.26772 用法，拒答由 Llama-Guard 判，附录 A 与人工对比 0.86 准确）。承诺边界由强制作答曲线计算，可直接复现，无需人工标注。翻转率定义沿用 2604.01202（以无 steering 的基线决定为参照）。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 复现依据与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 全程 steering（思考/不思考） | 同任务同指标 | 2604.01202 §3.4、Table 1 | 论文给出层（20）、位置（pre_gen）、diff-in-means 与 α∈{4,8,12}；代码未公开，规范充分 | 独立实现：pre_gen 激活 diff-in-means，prefill+decode 全程加 α·v | 是 |
| 固定/去除/重生成/交换 CoT | 同任务（拒答）同模型 | 2605.26772 §3–4 | 已 clone 官方代码，含 hook 与 new_trace 生成入口 | 直接用其 EOI 方向与 hook；扩到 Qwen3 | 是 |
| Prefix Steering | 短窗口 steering 的一般方法 | 2610.04967 §5 | 规范：从最终 prompt token 起 steer 固定 k 个 token；代码未确认 | 独立实现：k∈{1,5,16,64} | 是（作为释放扫描中“保留 KV”的一支） |
| 承诺边界定位 | 测量工具 | 2606.13603 §3–4 | 已 clone 官方代码（按句截断+强制作答） | 改写答案读取为二分类决定 token 概率 | 是（测量用，非性能对照） |
| 范数匹配随机方向 | 方向特异性对照 | 标准对照 | 标准算法 | 每 α 5 个随机方向，范数与 v 相同 | 是 |

- Reviewer 记录：`尚未送审`

### IDEA-003：把 CoT 当作证据累积过程——用微刺激范式检验 steering 的“漂移”作用

- 来源：`相似领域成熟方法迁移`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：activation steering；drift-diffusion model；reasoning models；chain-of-thought length
- 一句话背景：推理模型中 steering 同时改变决定与 CoT 长度（2604.01202 Table 2 膨胀 1.4–2.3 倍），缺少能联合解释二者的模型。
- 与起点问题的关系：原问题；用选择+反应时联合模型回答剂量/预先确定之争。
- 主贡献：迁移神经科学的微刺激检验（Ditterich, Mazurek & Shadlen 2003：MT 微刺激使选择偏向并按方向改变反应时，符合在漂移上加偏置）——检验 steering 是改变“起点”（预先确定）还是“漂移”（随审议累积，即剂量），用 CoT token 数作反应时。
- 贡献自评：重要性 7 / 新颖度 7 / 有效性 5.5。未知：pre_gen 已>0.9 可解码，CoT 未必是累积过程；CoT 长度受文本风格影响，与反应时的对应缺依据。
- 可行性：pass
- 自评分：`6.5/10`
- 一段话概括：在多 α、多题目难度下同时记录翻转率与 CoT 长度，拟合含起点偏置与漂移偏置两种 steering 作用的 DDM，比较拟合与预测（释放、起点扫描下的分布）。
- 打分理由：视角新，但从脑区微刺激到残差流的映射关键假设（CoT 是序贯累积）有反证（预先确定），有效性偏弱。
- 自评分轻量新意依据：检索“drift diffusion model LLM chain-of-thought steering”未见同类工作。
- Reviewer 记录：`尚未送审`

### IDEA-004：承诺门控 steering——steer 到被 steer 轨迹写下承诺即停

- 来源：`最高近邻不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：activation steering；prefix steering；reasoning models；capability degradation
- 一句话背景：Prefix Steering（2610.04967）用固定窗口长度，推理模型上所需窗口应随轨迹何时写下承诺而变。
- 与起点问题的关系：子问题；从“为何放大/锁定”转到“如何利用放大做更少副作用的 steering”，原问题的机制部分不回答。
- 主贡献：以探针检测 steer 轨迹的承诺点并据此停止 steering，在推理模型决定任务上以更少被 steer token 达到全程 steering 的翻转率，并减少推理能力损伤。
- 贡献自评：重要性 6.5 / 新颖度 5.5 / 有效性 6；FASB（2508.17621）、StTP（2604.08169）、Prefix Steering 已覆盖自适应/短窗口的大半。
- 可行性：pass
- 自评分：`6.0/10`
- 打分理由：在近邻上加停止规则，接近 baseline_patch 边缘。
- Reviewer 记录：`尚未送审`

### IDEA-005：激活诱导决定经承诺句被“洗白”，CoT 监控看不出

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：CoT monitorability；activation steering；rationalization；reasoning models
- 一句话背景：2604.01202 发现被 steer 翻转的决定常伴随流畅合理化，但单条轨迹上的 CoT 监控能否识别外部诱导的决定未被测量。
- 与起点问题的关系：邻近新问题；从可控性转到可监控性。
- 主贡献：测量 CoT 监控对 steering 诱导决定的检出率，及其与 steering 作用时间（承诺前/后）的关系；对比激活探针。
- 贡献自评：重要性 7.5 / 新颖度 6 / 有效性 6；2603.17199 已在 hint 诱导场景比较探针与监控。
- 可行性：pass
- 自评分：`6.4/10`
- Reviewer 记录：`尚未送审`

### IDEA-006：同一承诺轴上的“可控性—可见性”权衡

- 来源：`领域共性不足`
- 父 Idea：`IDEA-002`、`IDEA-005`
- 状态：`available`
- 定位关键词：activation steering；commitment boundary；CoT monitorability；reasoning models
- 一句话背景：同 IDEA-002，增加 CoT 监控检出率作为第二结局。
- 与起点问题的关系：原问题 + 邻近新问题。
- 主贡献：预期承诺前 steering 有效且 CoT 看似正常，承诺后无效且 CoT 出现决策不稳，给出攻击者/防御者都关心的时间权衡。
- 贡献自评：重要性 7.5 / 新颖度 6.5 / 有效性 6。
- 可行性：pass
- 自评分：`6.7/10`
- 打分理由：重要性更高，但两个结局让主线变宽；先送 IDEA-002 看审稿意见。
- Reviewer 记录：`尚未送审`
