## 结论

2026-11-05，总体 score 4.5/10，verdict：needs_rethink。主贡献是两件事：一是"关系指令上的错误主要是锚点捕获"这一诊断，二是"最小差异对比对 SFT 能教会关系绑定"这一训练信号。两者目前都不够。诊断与 GUI-Primitives 自己的分析冲突，也与它公开的预测数据冲突：失败主要发生在找不到候选（定位）这一步，锚点捕获只占少数。训练信号在普通交叉熵 SFT 下，与已有的关系型指称数据（UGround 等）差别很薄，"配对为什么有用"也缺少机制说明。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 关系型指令导致的崩溃确实存在：GUI-Perturbed 报告下降 27–56 个百分点，GUI-Primitives 上最高约 32%。但 GUI-Primitives 的结论是瓶颈主要在定位候选：60–92% 的预测落在两个候选之外；预测落进候选区域时，水平、垂直、邻近、序号四类关系的选对率为 0.82–0.90。只针对"关系绑定"的修法，覆盖的是失败中的一小部分。 |
| 新颖度 | 5 | 诊断部分：GUI-Primitives 已经按"目标/干扰项/都不是"分类，附录还有 "Anchor-collapse" 错误类型。用它公开的预测加元素框，几分钟就能算出锚点命中率（见下），作为新发现的分量很低。训练部分：UGround 的 Web-Hybrid 里约 23.5% 是相对位置指称，Jedi 有布局类合成数据，所以"关系型 SFT 数据"不新。剩下的新意是"同一截图、同一锚点、只换关系词"的配对结构。我在 GUI 领域没检索到这种最小差异对比训练，按迁移规则本可给到 7。但方案用的是普通 CE SFT，没有对比项或负例项，配对实际上只是数据怎么组织；与 UGround 在同一截图上给多个邻居生成关系指称相比，差别很小，所以压到 5。 |
| 有效性（先验合理性） | 4 | 已有直接反证。我用 GUI-Primitives 公开的预测（runs/diagnostic）和 mixed_corpus 的元素框做了核算。Qwen2.5-VL-7B 在 994 项上：落在锚点 11.8%，干扰项 1.9%，目标 22.0%，其余 64.3%。按最近元素细分：合成图上 48% 的预测离目标、干扰项、锚点都远（超过对角线的 3%），真实图上这一比例是 73%。OS-Atlas-7B、Claude Opus 4.7 的分布相近。因此"锚点多于干扰项"成立，但"锚点捕获占主导"被反驳。另外，Qwen2.5-VL-7B 的 497 个配对中有 319 个（64%）在换关系词后，预测点移动超过对角线的 2%，与"预测基本不动"也不符。训练机制方面：NegCLIP 的收益来自对比损失分母里的困难负例，这一迁移条件在生成式 CE SFT 里不存在；What's Up（Kamath et al. 2023）也报告，在空间关系语料上微调不足以解决问题。支持方向：GTA1-7B 在 GUI-Perturbed 关系指令上有 65.8%，说明训练能改善关系型定位，但这不能说明"配对"是原因。注意 UI-TARS-1.5 和 Qwen3-VL 级 GUI 模型的错误分布还没核实，定位能力更强的模型上锚点占比可能更高。 |
| 待预研（不计分） | — | 对比 SFT 相对强基线的增益幅度；合成配对能否迁移到真实截图上的关系指令；ScreenSpot-v2/Pro 是否下降；GUI 专训模型上锚点捕获的实际占比。 |

与起点问题的关系：这是对原问题的直接回答，"崩溃在哪一层"和"什么训练信号有用"都在原问题内，不存在转向。但现有证据指向的崩溃层是候选定位，不是关系绑定；原问题中"定位层为什么失败、怎么修"这一部分，本方案没有回答。

实验能否判别主张：目前不能。
- 点名式增广对照与 GUI-Perturbed 的设定不符。GUI-Perturbed 的 rank-8 LoRA 用的是 GUI-DR 视觉扰动增广数据，不是"只含直接点名指令"的数据。拿只有点名指令的数据当对照，它不提升关系子集几乎是必然的，所以这个对照过弱。
- 缺少已用关系型数据训练过的同任务强基线：UGround-V1-7B、Jedi-7B、GTA1-7B。
- 去配对对照把截图换成随机截图，会同时增加截图多样性，与"破坏最小差异"混在一起。
- 主指标用清洗核心集，只有 185 项（每种关系约 28 项），按关系分别报告的统计功效不足。真实截图上严格准确率接近 0，关系层的改善可能被定位误差掩盖。
- 训练数据计划用 Aguvis，它含 Mind2Web；GUI-Perturbed 也由 Mind2Web 构造，需要去重。

可行性：pass。GUI-Primitives 的数据、预测和代码已核实公开（HF 上的 kagnlp/gui-primitives，GitHub 上的 Abrar2652/gui-primitives）。条目里有 anchor_id，元素框在 ui_corpus/mixed_corpus 中，锚点分类可以直接做。GUI-Perturbed 的数据集（figai/GUI-Perturbed）和 GUI-DR 管线已公开。用 OS-Atlas 等的元素框按规则合成关系三元组有 UGround 的先例。7B 全参 SFT、约 10 万样本、9 个变体，在 8×A100 上约 2–3 天，符合不超过 5 天的约束。待定的是"Qwen3-VL-8B 级 GUI 模型"具体用哪个，以及 GUI-Perturbed 的 LoRA 权重链接，论文里没给。

## 最高近邻

1. GUI-Primitives（arXiv:2608.21832，https://arxiv.org/abs/2608.21832 ，EMNLP 2026）。重叠：数据集与评测对象相同，已做候选区域分类，并有 anchor-collapse 错误类型。差别：只做评测，没有训练修法；结论是瓶颈在定位候选，与本方案的诊断相反。
2. GUI-Perturbed / GUI-CP（arXiv:2604.14262，https://arxiv.org/abs/2604.14262 ）。重叠：关系型指令崩溃（模板为"在 X 上/下/左/右的按钮"），以及 UI-TARS-1.5-7B 的 LoRA 微调。差别：微调用的是视觉扰动增广数据，并非关系对比数据。
3. UGround（arXiv:2410.05243，https://arxiv.org/abs/2410.05243 ）。重叠：大规模合成相对位置和上下文关系指称（约 23.5%），用于 SFT。差别：没有最小差异配对结构，也没有针对锚点或配对做分析。
4. Jedi / OSWorld-G（arXiv:2505.13227，https://arxiv.org/abs/2505.13227 ）。重叠：合成布局与层级关系数据，有 Layout Understanding 评测，Jedi-7B 在该类上 57.7。差别：不是对比配对，也不专门针对关系词。
5. What's "up" with VLMs（arXiv:2310.19785，https://arxiv.org/abs/2310.19785 ）。重叠：最小差异的空间关系对照，以及"微调能否修好"。差别：对象是自然图像上的 CLIP 类模型；报告的是微调不足以解决问题。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 6.0, "novelty": 5.0, "effectiveness": 4.0},
  "contribution_assessment": "主贡献为'锚点捕获'诊断加'最小差异对比对SFT'训练信号。重要性6：关系指令崩溃真实，但GUI-Primitives显示主要瓶颈在候选定位，关系绑定只占少数失败。新颖度5：GUI-Primitives已有候选区域分类与anchor-collapse类型，锚点命中可由公开预测直接算出；UGround(约23.5%相对位置指称)与Jedi已有关系型SFT数据；普通CE SFT下配对只是数据组织，与已有数据差别薄。有效性4：公开预测核算显示Qwen2.5-VL-7B锚点命中11.8%、干扰项1.9%、其余64.3%，合成图48%、真实图73%的预测远离三者；64%的配对换关系词后预测移动，直接反驳'锚点捕获主导'和'对关系词不敏感'；NegCLIP式收益依赖对比损失，迁移条件在CE SFT中不存在。待预研：增益幅度、合成到真实的迁移、ScreenSpot是否下降、GUI专训模型上的锚点占比。",
  "feasibility": "pass",
  "feasibility_reason": "GUI-Primitives的数据、预测、代码与元素框，以及GUI-Perturbed的数据集与GUI-DR管线均已公开核实；按元素框合成关系三元组有UGround先例；9个7B SFT变体在8×A100上约2–3天，符合不超过5天的约束。Qwen3-VL-8B级GUI模型的具体选择与GUI-Perturbed LoRA权重链接待定。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "诊断主张被已有数据直接反驳：GUI-Primitives的分析与其公开预测都显示错误以远离候选的定位失败为主（Qwen2.5-VL-7B锚点11.8%、其余64.3%），且64%的配对换关系词后预测移动；'锚点捕获占主导、对关系词不敏感'不成立（UI-TARS-1.5与Qwen3-VL级模型尚未核实）。",
    "对照与依据误读：GUI-Perturbed的退化来自视觉扰动增广的rank-8 LoRA，并非点名式指令增广；点名式对照过弱，缺少UGround-V1-7B、Jedi-7B、GTA1-7B等已用关系型数据训练的同任务强基线，'普通增广做不到'的主张无法被检验。",
    "训练信号缺乏先验机制：普通CE SFT没有对比或负例项，'最小差异配对'为什么优于等量的非配对关系数据没有依据；去配对对照与截图多样性混淆，Claim 3无法干净判别；该信号与UGround式关系指称数据的差别过薄。"
  ],
  "novelty_conclusion": "在GUI领域未检索到最小差异关系对比训练；但关系型SFT数据已有（UGround、Jedi），诊断与GUI-Primitives的候选区域分析和anchor-collapse类型高度重叠，且在CE SFT下配对结构接近数据组织方式，实质新意有限。",
  "closest_neighbors": [
    "GUI-Primitives: Diagnosing Spatial Reasoning Failures in Vision-Language GUI Grounding (arXiv:2608.21832)",
    "GUI-Perturbed: Domain Randomization Reveals Systematic Brittleness in GUI Grounding Models (arXiv:2604.14262)",
    "Navigating the Digital World as Humans Do: Universal Visual Grounding for GUI Agents (UGround, arXiv:2410.05243)",
    "Scaling Computer-Use Grounding via User Interface Decomposition and Synthesis (Jedi/OSWorld-G, arXiv:2505.13227)",
    "What's \"up\" with vision-language models? (arXiv:2310.19785)"
  ]
}
```
