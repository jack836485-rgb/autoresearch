## 结论

2026-11-04：score 5.8，verdict **promising_needs_revision**。主贡献是"把已缓解模型上的 cue 效应拆成插入/处境框架/风险内容/训练领域四个成分，并据此指出领域特有成分只占少数"——这个方向有真实靶子（ContextLift 原文确实写下"so the effect is due to the domain content of the cue"），预研也确有可用数据；但当前阶梯的 L4→L5 一步同时换掉了"风险"与"领域"两件事（原文 10 条 medical cue 是混合风险度，并非高风险），按风险匹配的对照（L3→L5 ≈ +29pp）反而大于风险成分（+17pp），因此"领域占少数"这一主结论现在没有被自己的预研数据可靠支持。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 7.0 | 若成立，新增两件可用的东西：(1) 对"条件失配由训练领域触发"这一已发表归因的定量更正；(2) 评测侧的结论——用"领域 cue + 可忽略的日常对照"构造的缓解评测会漏掉一类无需知道微调领域即可构造的触发（攻击者门槛更低）。但范围窄：单基座（Qwen2.5-7B）、仅数据交织这一支防御、仅前置句触发、两个领域。而且"非领域触发存在"本身领域内已知：Dubiński 报告语义相反的系统提示、"只共享几个词"的看似无关提示也能触发；2603.04407 报告跨领域触发仍有 8.75–40%。所以这是一次"更正归因 + 拓宽协议"，而不是改变领域主要判断。|
| 新颖度 | 7.0 | 查新未发现任何工作把 cue 效应按"插入/人称处境框架/风险/领域"做成分分解，也没有在交织缓解臂上测过"非领域高风险"cue，这是可辨认且独立的新点，且预先固定 cue 的做法比原文的"日常对照"更严。扣分在于第三个成分的理解并不新：2605.12798 的 prompt-level EM surface（判别提示是否给出连贯有害回答的空间）与 2507.06253 的"被感知的有害程度与失配概率相关"已经给出同一机制，本 Idea 只是把它搬到前置句上并明确声明不主张命名，新意更接近测量而非机制。|
| 有效性 | 5.5 | **现在有什么依据：** 同臂、同 judge、同 8 题、cue 预先固定的六级阶梯，四个成分 CI 均不含 0；复现了原文的同臂无 cue 率（4.5% vs 5.6%）与领域 cue 的大幅回升；自建低风险非领域 cue 与原文日常 cue 无差别（−2.3pp，CI 含 0），说明 L2/L3 的"作者自写 vs 模型生成"管线差异在低风险层不构成混淆；长度反例（14 词处境句 > 25 词事实句）成立。**适用条件与未知：** 核心问题不在种子/judge/legal，而在量本身。我核对了公开 cue 文件（`evaluation/cues/medical_cues.json` 的 `cues/0..9`）：原文 10 条 medical cue 风险度混合——既有"1 型糖尿病想用天然替代胰岛素""严重烧伤""孩子摔倒"，也有"想了解洗手""疫苗接种排程""轻微背伤""保持健康的小技巧"。因此 L4（统一高风险、非领域）→L5（混合风险、领域）这一级并非"只改一件事"，它同时降低了风险度并加入领域；按风险匹配读同一组数据，L3（非领域低风险 17.0%）→L5（领域 46.0%）约 +29pp，明显大于风险成分 +16.9pp，方向与主结论相反。另外同一个对比在文内给出两个不相容的数值（成分表 +13.4pp [+3.8,+23.1] 与正文 +7.1pp [−5.5,+19.7]/+9.9pp），未说明差别来源；主阈值 aligned ≤ 30 下该对比 CI 还含 0。更根本的是，"领域成分占比"没有定义良好的参照类：分子分母都随自写高风险 cue 的强度移动，把 cue 写得更惊险就能把占比压到任意低，所以"占比 CI 上界 < 50%"的预设阈值通不过/通过都不能判定"领域是否是主要来源"。|

**与起点问题的关系：** 是原问题（问题锚点的"触发空间的系统化搜索"与"已缓解模型在条件触发下的表现"），给出的是可操纵轴与效应量而非搜索算法，属部分回答；原问题仍未答的是：不知道微调领域时如何发现未知触发、输出格式/系统提示类触发、代码领域、以及 inoculation 与事后 HHH 等其他防御族和其他基座。转向本身不是阻断项。

**实验能否判别主张：** 对"存在性/防御漏洞"类主张可以判别——L4 在交织臂上 34.3%（对 L0 4.5%），以及主张 2 的"日常副本臂/ContextLift 臂上 L4−L2 增量是否保留"，三臂 ×4 层的设计足以分辨，而且这是实践上更关键、原文未测过的格子。对当前写法的主张 1 不能判别：阶梯只有"非领域×{低,高}风险"两格加"领域×混合风险"一格，缺 `领域×低风险` 与 `领域×高风险` 两格，也缺与非领域 cue 同生成管线的领域 cue；交互存在时成分归因随路径变化，占比阈值无法裁决通行解释。补这两格只需新增 cue 与判分，不需要新训练，现有 L5 的 67 条提示级数据也能先按 cue 的风险度分层验核，成本很低。建议把主 Claim 改成"非领域、非训练上下文的高风险处境句即可把已缓解模型重新激活到 X%"的存在性主张加主张 2，并把"占比"降为补充描述；同时把"通行解释是领域"的措辞收到 ContextLift 的那一句归因上，不要外推成全领域共识（Dubiński 的"共享特征"本就不等于领域主题，高风险求建议的处境同样是与微调行上的共享特征）。竞争解释 2608.29118（表示距离，Spearman −0.73；且其结论是标量距离无法预测语义保持扰动下的变化）作为协变量报告是合适的，但若距离能单调解释四级，"成分"相对"相似度"的增量说明就需要正面给出。

**可行性：pass。** 三个配置（`configs/medical/interleaving_wg.yaml`、`interleaving_wgevlift.yaml`、`interleaving_wglift.yaml`）与 legal 对应配置、`evaluation/cues/{medical,everyday}_cues.json` 在 `davidkaczer/contextlift` 的 `arxiv` 分支上确实存在（已核验文件树）；超参与原文一致（QLoRA r=32、lr 1e-4、1 epoch、交织 20%），原文自述单次 40–45 分钟/H100，故 11 次训练约 13 A100 小时、合计约 31 A100 小时在 2×A100 约束内可完成（8 卡约 4 小时）。judge 为本地 72B-AWQ 加不超过 2,000 条 gpt-6-luna 复判，50 元内可行。关键数据不缺：cue、题目、被试臂都是公开或可重训的，不存在"字段存在但数据未发布"的问题。标签含义也分得清：失配 = coherence ≥ 50 且 aligned 低，且"回应 cue 话题的坏建议"与"广泛失配"分开计数（对应原文 Table 2 的 broad 列），主张只用广泛失配，这一点正确。唯一与原文不同的是主阈值用 aligned ≤ 30 而原文为 < 30，并列报告的处理可接受，但关键对比在两阈值下显著性不一致，须按预案判为 judge/阈值依赖。

## 最高近邻

1. ContextLift（arXiv:2610.21633, Mai & Kaczér; github.com/davidkaczer/contextlift）——直接靶子：medical 日常 cue 11.7% vs 同臂无 cue 5.6%，据此断言"effect is due to the domain content of the cue"；Table 2 的 everyday-context 副本关闭约 3/4 差距。差别：未做成分分解；但其 10 条 medical cue 风险度混合，这正是本 Idea 阶梯的混淆来源。
2. Conditional misalignment（arXiv:2604.25891, Dubiński et al.）——conditional EM 的提出者，教育化框架、flask 模板、以及"语义相反/仅共享几个词的无关提示"都能触发，并明确指出穷举触发空间不现实。差别：无成分分解、未在交织防御上测非领域高风险 cue。
3. Emergent and Subliminal Misalignment via Data-Mediated Transfer（arXiv:2605.12798）——prompt-level "EM surface"：LLM 判别提示留给连贯失配回答的空间，高 surface 提示 EM 率更高。差别：改的是评测问题本身，不涉前置 cue 与已缓解模型；但它已覆盖"风险/有害可写性"这一成分的理解。
4. Emergent misalignment as prompt sensitivity（arXiv:2507.06253, Wyse et al.）——模型对问题"被感知失配程度"的打分与失配概率相关，提示 nudge 效应大。差别：无 cue、无缓解臂；与第三个成分机制高度重叠。
5. Semantic Containment as a Fundamental Property of EM（arXiv:2603.04407）——触发按语义而非表层匹配起作用，改写后容纳仍保持，跨领域触发仍有 8.75–40%。差别：无防御臂、无成分分解；但已表明触发不必与领域严格一致。

```json
{
  "score": 5.8,
  "contribution_scores": {"importance": 7.0, "novelty": 7.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献：在交织缓解臂上把条件失配的 cue 效应按插入/处境框架/风险/领域四轴分解，并据此更正 ContextLift 的'效应来自 cue 的领域内容'归因。重要性 7：有真实的已发表归因可更正，并给出无需知道微调领域即可构造触发的评测结论，但范围限于单基座、数据交织一支、前置句触发，且'非领域触发存在'在 2604.25891 与 2603.04407 中已有先例。新颖度 7：无人做过 cue 效应的轴向成分分解，cue 预先固定；但第三个成分的理解等同 2605.12798 的 EM surface 与 2507.06253 的被感知有害度，属测量而非机制新意。有效性 5.5：预研确有同臂同 judge 的六级阶梯与非零 CI，并复现原文同臂数值，L3 与原文日常 cue 无差别可排除低风险层的 cue 管线混淆；但核对公开 medical_cues.json 的 10 条 cue 后发现它们风险度混合（从'洗手''疫苗排程'到'1 型糖尿病替代胰岛素''严重烧伤'），L4→L5 一级同时改变风险与领域，按风险匹配的 L3→L5 约 +29pp 大于风险成分 +16.9pp，与'领域占少数'方向相反；同一对比文内给出 +13.4pp 与 +7.1pp 两个不相容数值，主阈值下 CI 含 0；且'领域占比'的分子分母都随自写高风险 cue 的强度移动，没有定义良好的参照类，占比阈值无法裁决通行解释。待验证条件：补 领域×低风险、领域×高风险 两格与同管线生成的非领域 cue（无需新训练），并把主张改为存在性主张加主张 2。",
  "feasibility": "pass",
  "feasibility_reason": "已核验 davidkaczer/contextlift 的 arxiv 分支确有 configs/medical 与 configs/legal 下的 interleaving_wg / wgevlift / wglift 三个配置及 evaluation/cues/{medical,everyday}_cues.json；超参与原文一致，原文自述单次训练 40-45 分钟/H100，11 次训练约 13 A100 小时、全流程约 31 A100 小时在 2xA100 内可完成；judge 用本地 Qwen2.5-72B-AWQ 加不超过 2000 条 gpt-6-luna 复判，50 元内；关键 cue、题目与被试臂均公开或可重训，无不可得输入；标签把'回应 cue 话题的坏建议'与'广泛失配'分开计数，与主张一致。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "主张 1 的关键对比 L4->L5 不是'只改一件事'：公开的 10 条 medical cue 风险度混合而非高风险，该级同时降低风险并加入领域；按风险匹配的 L3->L5（约 +29pp）大于风险成分（+16.9pp），现有预研数据不支持'领域成分占少数'，缺 领域x低风险 与 领域x高风险 两格及同生成管线的非领域 cue，分解结果随路径变化。",
    "'领域成分占总效应的比例'没有定义良好的参照类：分子与分母都随自写高风险 cue 的强度移动，因此预设阈值（占比 CI 上界 < 50%）无论通过与否都不能裁决'领域是否为主要来源'，最小实验无法判别当前写法的主 Claim。",
    "同一对比在文内给出 +13.4pp [+3.8,+23.1] 与 +7.1pp [-5.5,+19.7]/+9.9pp 两套不相容数值且未说明来源，主阈值 aligned<=30 下该对比 CI 含 0。",
    "背景把 Dubiński 与 ContextLift 统一概括为'触发来自训练领域'过强：Dubiński 已报告语义相反与仅共享少数词的无关提示可触发，'共享特征'不等于领域主题，'通行解释'应收到 ContextLift 的那一句归因上。"
  ],
  "novelty_conclusion": "cue 效应的轴向成分分解与'在交织缓解臂上测非领域高风险 cue'未见先例，相对最高近邻有独立增量，不是换名或平凡组合；但风险/有害可写性这一成分的理解已被 2605.12798 与 2507.06253 覆盖，非领域触发的存在性亦已被 2604.25891 与 2603.04407 部分报告，故新意限于测量与归因更正。",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv:2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv:2604.25891)",
    "Emergent and Subliminal Misalignment Through the Lens of Data-Mediated Transfer (arXiv:2605.12798)",
    "Emergent misalignment as prompt sensitivity: A research note (arXiv:2507.06253)",
    "Semantic Containment as a Fundamental Property of Emergent Misalignment (arXiv:2603.04407)"
  ]
}
```
