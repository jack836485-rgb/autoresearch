## 结论
2026-11-04，总体 score 4.5，verdict：needs_rethink。主贡献是"ContextLift 的残余条件失配集中在请求侧立场 cue 上，用 LLM 把立场改写成处境句即可补上"。这个贡献不够，原因有三：第一，缺口本身已由 ContextLift 原文附录 A 报告；第二，主张 1 的度量混淆了"回答 cue 的窄域坏建议"和"条件触发的广义失配"；第三，修补只是对一篇三周前论文抽取规则的增量改动，作者自己也试过"生成式 context 池"。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 5 | 对象是当前最强的条件 EM 防御，审计它有价值。但实质残余只在 medical 上：ContextLift 的 cued 失配为 12.8%，broad 子集 10.6%；security 和 legal 仅 2.6% 和 6.1%，留给新发现的余量很小。补上一类 cue 不改变"数据侧防御只覆盖数据所带内容"这一判断，这个判断 ContextLift 的结论一节已经写明。 |
| 新颖度 | 4.5 | 一是 ContextLift 自己的 medical cue 集（仓库 `evaluation/cues/medical_cues.json`，由 Qwen2.5-7B 从训练提示生成）本来就含"natural alternatives to insulin"和"Vitamin A supplements for a burn"。附录 A 明确写到：有三条"描述用户正在设法治疗的健康问题"的 cue（胃痛、胰岛素替代、维生素 A）占 medical 残余的三分之二，且 74–90% 的残余答案是在"回答 cue 而不是问题"。brief 里 87%/81% 的最强 cue 正是这两条，所以"立场 cue 残留触发"不是新发现，"ContextLift 只用处境句 cue 评测"的说法也不准确。二是"lift 规则只覆盖 7–15% 的行，没有前导处境句的提示什么也抽不到"已写在原文第 2 节和局限一节；788/5,400 的计数与原文的 783 个唯一 context 一致。三是用模型生成 context 来扩展覆盖，原文附录 F 提到早期用过"generated context pool"，最后为了"无模型、无标注"才改用正则。剩下的新意是"把请求侧立场改写成陈述句放进副本"这一具体变体，属于可辨认的小增量。 |
| 有效性 | 5.5 | 当前依据：ContextLift 附录 A 和表 4 支持立场类 cue 上确有残余（medical 的 A/D 类为 25.8%）；表 2 支持"副本内容越贴近 cue，压得越低"，所以 ContextLift+ 降低 R 族 cue 效应有合理机制；2608.29118 的距离解释也支持这一方向。未知部分：原文把这类残余归因于 cue 本身可被读成领域请求，即模型给出的是窄任务坏建议，而不是广义失配。R 族按构造（"I want to treat X with essential oils instead of antibiotics"）几乎都会落入 A/D 类。因此 ContextLift+ 把它压下去，可能本身就是在抑制窄任务对近似请求的响应；它与"域内失配不降 3pp"能否同时成立，没有任何依据。 |

- **与起点问题的关系：** 回答的是原问题的子问题，即最强防御在一类结构化触发下的覆盖。原问题里"触发空间的系统化搜索"只推进到一个族（请求侧立场），格式和系统提示类触发仍未回答。
- **实验能否判别主张：** 不能充分判别。
  - 主张 1 没有按 broad 与 ambiguous/domain 拆分 R 族 prompt，也没有判断答案是否在"回答 cue"，所以测到的"缺口"可能只是原文已承认、并定性为窄域行为的那部分残余（claim 阻断）。
  - 主张 2 的修补与"副本覆盖了更多唯一且经 LLM 生成的句子"混在一起：ContextLift+ 的唯一句子数和来源都变了，而 brief 没有同预算、同数量的 LLM 改写 S 型句对照，因此无法归因到"按同一原因修补"。
  - 72B-AWQ judge 的阈值定在分数聚集的 30 附近，对差值的 5pp 和 3pp 门槛很敏感。gpt-6-luna 复判只做一致性检查，不作为主判，所以与原文数字的可比性有限。
- **可行性：pass。** 实现与资源依据如下：
  - 仓库 `davidkaczer/contextlift` 的 arxiv 分支公开，已确认有 `configs/medical/interleaving_wglift.yaml`、`data/interleaving/medical_wglift.jsonl`、`medical_cues.json`、`medical_prompt_classes.json`；
  - 新训两个 7B 4-bit LoRA 臂约 2.4 A100 小时，生成加 72B 打分约 4 小时，在 2×A100 内；
  - R 型改写只需固定 prompt 加人工抽查 50 句，API 成本可忽略；
  - 标签含义需注意："misaligned"沿用 Betley judge，会把窄域坏建议也计为失配，原文 Appendix A 正因此另做 prompt 分类，本方案需同样可得，仓库已有分类文件和判别 prompt 路线。

## 最高近邻
- **ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment**（Mai & Kaczér, 2026）https://arxiv.org/abs/2610.21633
  - 重叠：同一方法、数据和评测；附录 A 已定位 medical 残余在"正在治疗的健康问题"立场 cue 上，第 2 节和局限一节已披露 lift 覆盖率与"无触发不代表安全"。
  - 差别：没有专门构造立场族，没有改写式副本。
- **Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers**（Dubiński et al., 2026）https://arxiv.org/abs/2604.25891
  - 重叠：条件 EM 的定义与"缓解后 cue 下复现"的审计范式。
  - 差别：触发是手工设计的，没有测 ContextLift。
- **Emergent Misalignment Is Not Magical**（Li et al., 2026）https://arxiv.org/abs/2608.29118
  - 重叠：表示距离预测 EM 诱发程度，可直接预言"离训练近、离副本远"的 cue 残留。
  - 差别：没有涉及防御的覆盖范围。
- **Aligned Data Can Induce Misalignment via Context Confusion**（Bakman et al., 2026）https://arxiv.org/abs/2609.38379
  - 重叠：定向对齐数据优于通用数据，可作为"按领域定制副本"的近邻修法。
  - 差别：研究对象是由对齐数据诱发的语境混淆，不是 EM 交织防御。
- **Correct, Don't Delete: Mitigating Emergent Misalignment with Corrective Supervision**（Epifano, 2026）arXiv:2609.37624（来自 ContextLift 引用，未单独核验正文）
  - 重叠：定向纠正数据。
  - 差别：需要知道有害样本，没有在 cue 下评测（据 ContextLift 转述）。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 5.0, "novelty": 4.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是审计并修补 ContextLift 的请求侧立场触发缺口。缺口本身已在 ContextLift 附录 A 报告：medical 残余的三分之二来自胰岛素替代、维生素 A、胃痛三条立场 cue，且主要是在回答 cue；lift 覆盖率限制也已在正文和局限一节披露，生成式 context 池作者早期试过。剩余新意是把请求侧立场改写成陈述句放进副本，属于小增量。有效性方面，原文表 2 和表 4 支持副本内容越匹配越有效、立场 cue 确有残余；但 R 族按构造属于 ambiguous/domain 类，压低其 cue 效应与保持窄任务之间的冲突没有依据，度量也没有区分窄域坏建议与广义失配。",
  "feasibility": "pass",
  "feasibility_reason": "公开仓库 arxiv 分支已含 wglift 配置、数据、medical cue 与 prompt 分类文件；新训两个 7B QLoRA 臂加 2.2 万条生成和 72B 打分约 10 A100 小时，改写与复判 API 成本很低，均在 2×A100 和 1000 元约束内。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "新颖度阻断：请求侧立场 cue 上的残余已由 ContextLift 附录 A 定位并归因（三条立场 cue 占 medical 残余三分之二，多为回答 cue），brief 关于 ContextLift 只用处境句 cue 评测的定位与其公开 cue 集不符",
    "Claim 阻断：主张 1 没有区分 broad 与 ambiguous/domain prompt，也没有区分回答 cue 的窄域坏建议与广义失配；R 族按构造偏向领域请求，测到的缺口可能就是原文已定性的窄域残余",
    "Claim 阻断：主张 2 缺少同预算、同唯一句数的 LLM 改写处境句对照，无法把改善归因于立场内容而非副本多样性或覆盖量",
    "贡献分量不足：三维为 5/4.5/5.5，没有任何一项达到 8"
  ],
  "novelty_conclusion": "相对 ContextLift 原文，缺口发现基本已被其附录 A 和局限覆盖；修补是对抽取规则的 LLM 改写扩展，作者早期尝试过生成式 context 池，只算小增量。",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv 2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "Emergent Misalignment Is Not Magical (arXiv 2608.29118)",
    "Aligned Data Can Induce Misalignment via Context Confusion (arXiv 2609.38379)",
    "Correct, Don't Delete: Mitigating Emergent Misalignment with Corrective Supervision (arXiv 2609.37624, needs_search for full text)"
  ]
}
```
