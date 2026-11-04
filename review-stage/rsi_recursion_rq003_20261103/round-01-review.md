## 结论
2026-11-03，总体 score 5.0，verdict：promising_needs_revision。主贡献是一项测量研究：把冻结的各代改进者交叉作用于各代目标，估计“改进者增益 × 目标成熟度”的交互，并检验现有协议能否预测后期改进量。这个经验对象确实还没人测过，但分量不够。一是概念框架已被 2610.27610 提前给出，包括对角不可识别、“目标逼近天花板时收益收缩、改进者却在变好”的混淆，以及“在一组声明的起点上做 swap test、复合主张要重复 swap test”。二是按当前设计，在 paper_review 上交互为负几乎是量表和天花板直接决定的，无法判别“低垂果实”与测量伪影。三是“递归增益比”无法对应到 R_AI。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | RSI 过程级证据确实稀缺。2610.27610 的普查显示，26 篇声称改进了改进程序的研究中只有 4 篇做了同起点、同预算的比较。AIDE² 的点火测试也自认结论不确定。“改进者增益是否随目标成熟度衰减”会影响 imp@k 和点火测试该怎么解读，有明确价值。但主证据只来自 paper_review（主观二分类标签，测试分约 0.6，天花板低）和 STOP，外推到“当前 RSI 系统处于放大区还是衰减区”跨度很大。 |
| 新颖度 | 5.5 | 2610.27610 §4.3 的 Proposition 3 已形式化对角不可识别，并明确写出“gains can shrink as the solver approaches its performance ceiling even while the improver gets better / can grow when a fixed improver reaches states that are easier to improve”。它还要求做离对角观测、把估计量定义在单一状态或一组状态的平均上，复合主张要做重复 swap test。Wu et al. 的综述提出了 paired probe，2610.35193 提出了 paired continuations。brief 宣称“首次完整析因矩阵”，在框架层面只是这些设计的直接网格化。真正剩下的新意是：首次实际测出整个矩阵，量化交互，并检验各协议的预测效度。这一点可辨认，属于增量。brief 没有引用这些最近邻，“与最高近邻的差别”一节因此不成立。 |
| 有效性 | 4.5 | 现有依据：Hyperagents 中元 agent 迁移后 imp@50=0.63，初始元 agent 约为 0。但这个 j=0 的目标是因输出格式失败而得 0.0 分的 agent，改进主要来自修好格式，是“低垂果实”的极端形态。AIDE² 在后期目标上 3 个种子无法区分两个改进者（0.780 vs 0.782）。这些证据只说明“起点有增益、后期噪声大”，并不支持矩阵能读出可解释的交互。它们迁移到本设置还缺几步。(1) 原始准确率是有界量表，后期目标余量约 0.05 左右，与 100 篇测试集的单次标准误（约 0.05）同量级；按原始增益做加性交互，负号几乎是必然的，且换一种单调变换（如“关闭剩余差距的比例”或 logit）符号就可能变。(2) 能抗量表变换的只有排序交叉，但 5 个改进者的排序相关几乎没有统计功效。(3) 每格 3 次重复、k=10 小于 Hyperagents 的 50，后期列很可能全部接近 0。(4) 开源模型驱动下，谱系里的改进者可能根本没有变强（STOP 在 GPT-3.5/Mixtral 下退化），门控只查初始元 agent 在 j=0 的表现，没查谱系里后代改进者是否变强。 |

- **与起点问题的关系：** 仍属原问题，处理的是“改进者变强 vs 目标变难”这一可识别性子问题。“收益是否跨轮累积”和“历史变长”的分离仍未回答，原因见下文的记忆回放混淆。
- **实验能否判别主张：** 目前不能。
  - 第一，“交互显著为负 + 起点 imp@k 排序相关弱”这个支持条件，在 paper_review 上由余量压缩和格式修复效应就足以产生，无法与“改进者优势只在不成熟目标上”区分。推翻条件需要后期列有可测的正增益，而功效不足。
  - 第二，DGM-H 的元 agent 会演化出持久记忆，里面存着谱系专属的洞见，原文的记忆样例直接写了 Gen55/Gen64 的 paper review 准确率和修正方向。后代改进者 i 作用于同谱系的早期目标 j<i 时，可以直接回放已知修法。这也会产生负交互，而“完整历史 vs 截断历史”对照没有说明是否覆盖改进者代码里自带的记忆文件。
  - 第三，“递归增益比”是两条原始量表斜率之比，取值依赖代次间隔和量表选择，没有给出与 2609.00137 中 R_AI 的反馈强度和难度增长参数的映射，不能据此判定处在放大区还是衰减区。
- **可行性：pass。**
  - 已核实：Hyperagents 官方仓库含 domains、generate_loop.py、run_meta_agent.py、analysis/。论文 Appendix D.5 已做过只迁移元 agent、目标换成别的 task agent 的组合，所以 (i, j) 重组有现成路径。README 还公开了实验日志（Google Drive）。STOP 和 HGM 代码已由 brief 核实，点火测试的规范在 AIDE² §3.6 中足以独立实现。
  - 预算偏低估：Hyperagents 报告每 100 次迭代自修改约 33M token，即每次约 33 万，不是 15 万；100 篇论文的评测约 0.5M。按约 810 个子代计，总量约 6.5 亿 token。走 API 时元 agent 部分约 2.7 亿 token，不是 1.2 亿。本地 MoE 模型以 prefill 为主，在 8×A100 上数天内仍可完成；API 路线大概率仍在 1000 元附近，但余量很小。
  - 无人工标注，标签就是 accept/reject 准确率，与主张口径一致。
  - 风险在于效果，不在能否实现：开源模型下谱系里的改进者可能不变强。若要沿用公开的 Claude 谱系，又会换掉驱动模型。

## 最高近邻
1. **Auditing the Product, Not the Recursion**（Chen, Zhu, Zheng，2026-10）https://arxiv.org/abs/2610.27610
   - 重叠：对角不可识别命题、天花板收缩混淆、离对角 swap test、在一组声明状态上平均、复合主张要重复 swap test。
   - 差别：只做普查和理论，没跑任何矩阵实验。
2. **Hyperagents / DGM-H**（Zhang et al.，2026）https://arxiv.org/abs/2603.19461
   - 重叠：定义 imp@k、冻结元 agent、只迁移元 agent 的组合、paper_review 领域。
   - 差别：只在格式失败、得 0 分的起点上测，没有跨目标成熟度的比较。
3. **Recursive self-improvement of AI research agents（AIDE²）**（Srikanth et al.，2026）https://arxiv.org/abs/2609.26457
   - 重叠：点火测试，即同一后期起点、换外环 agent。
   - 差别：只有一个后期状态、两个改进者、3 个种子，结论不确定；也指出噪声让决定性比较代价极高。
4. **Recursive Criticality of AI Self-Improvement**（Burtsev，2026）https://arxiv.org/abs/2609.00137
   - 重叠：给出反馈强度相对难度增长的 R_AI 阈值，并呼吁测量。
   - 差别：纯理论，没有从有界基准增益到其参数的操作化。
5. **Huxley-Gödel Machine（CMP）**（Wang et al.，2025）https://arxiv.org/abs/2510.21614
   - 重叠：元生产力与当前表现不匹配，用后代表现估计改进潜力。
   - 差别：在同一棵树里估计，不是固定目标上的受控交叉。
- 另见 Wu et al. 的 RSI 综述（Preprints.org 2026，提出 paired probe，需要检索原文核实）和 2610.35193（paired continuations 与三级比较设计，https://arxiv.org/abs/2610.35193）。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.5, "novelty": 5.5, "effectiveness": 4.5},
  "contribution_assessment": "主贡献是改进者×目标成熟度的离对角交叉测量，以及对现有协议预测效度的检验。重要性有限但明确：过程级证据稀缺，点火测试结论不确定。新颖度受 2610.27610 压制：对角不可识别、天花板收缩混淆、多状态 swap test 与重复 swap test 均已提出，剩下的是首次实测与量化交互。有效性不足：paper_review 的有界准确率、格式失败的 j=0 起点、后期余量与评测噪声同量级，使原始量表上的负交互几乎必然出现且依赖量表；5 个改进者的排序相关缺乏功效；DGM-H 的持久记忆会让后代改进者在同谱系早期目标上回放已知修法；递归增益比与 R_AI 没有可识别的映射；开源模型下谱系里的改进者可能并未变强。",
  "feasibility": "pass",
  "feasibility_reason": "Hyperagents 官方代码含元 agent 与 task agent 分离迁移的路径（Appendix D.5），并公开了实验日志；STOP、HGM 代码可得，AIDE² 点火测试规范足以独立实现。按论文报告的每次迭代约 33 万 token 自修改加 0.5M 评测，总量约 6.5 亿 token，本地 8×A100 可在数天内完成；API 路线约 2.7 亿 token，大概率仍在 1000 元附近。无需人工标注。主要风险是效果，不是能否实现。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "新颖度：析因测量框架与“目标逼近天花板导致收益收缩”的混淆已由 2610.27610（对角不可识别命题、多状态 swap test、复合主张需重复 swap test）及 Wu et al. 的 paired probe 提出；brief 未引用，“首次完整析因矩阵”的定位不成立，剩余新意仅为实测。",
    "Claim 判别：在 paper_review 上，j=0 是格式失败、0 分的目标，后期目标余量约 0.05、与 100 篇评测的标准误同量级；原始增益上的负交互可由余量压缩与量表直接产生，换一种单调变换符号就可能改变，无法区分“低垂果实”与测量伪影；能抗量表的排序检验只有 5 个改进者，缺乏功效。",
    "Claim 判别：DGM-H 元 agent 的持久记忆含谱系专属修法，后代改进者作用于同谱系早期目标时可直接回放，同样产生负交互；历史长度对照未说明是否覆盖改进者自带的记忆文件。",
    "Claim 判别：递归增益比是依赖代次间隔与量表的原始斜率之比，未给出与 R_AI 参数的映射，不能据此判定放大区还是衰减区。",
    "有效性：门控只检查初始元 agent 在 j=0 的 imp@10，未检查开源模型驱动的谱系里后代改进者是否变强；若没有变强，矩阵没有可分解的改进者增益。"
  ],
  "novelty_conclusion": "框架层面已被 2610.27610、Wu et al. 的 paired probe 与 2610.35193 的 paired continuations 覆盖；尚无工作实测完整的改进者×目标矩阵并估计交互与协议预测效度，这是可辨认的经验增量，但不足以支撑 8 分新颖度。",
  "closest_neighbors": [
    "Auditing the Product, Not the Recursion: The Evaluation Evidence Behind Recursive Self-Improvement Claims (arXiv:2610.27610)",
    "Hyperagents (arXiv:2603.19461)",
    "Recursive self-improvement of AI research agents / AIDE² (arXiv:2609.26457)",
    "Recursive Criticality of AI Self-Improvement (arXiv:2609.00137)",
    "Huxley-Gödel Machine (arXiv:2510.21614)"
  ]
}
```
