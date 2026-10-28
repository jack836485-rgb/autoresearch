# 最终审查结论

- 状态：`blocked_max_reviewer_calls`（试跑预算 3 次：2 次常规审查加 1 次调试强制复核）。
- 最佳送审候选：IDEA-004。首审 5.5/10（promising_needs_revision），复核 5.0/10（promising_needs_revision）。Gate 要求两次都 > 7.5，未满足。
- 两次审查一致的判断：
  - "缓解后逐提示残余失配能否被预测"是空白，可以证伪；
  - "有害数据覆盖、缓解数据未覆盖"的机制已由 ContextLift 陈述，本 Idea 的增量只是把它量化并做预测检验；
  - 阻断：inoculation 分支没有训练臂，D_m 也没有定义；EM-only 臂上的相对密度没有定义；
  - 首审另指出：漏了 2608.29118 的 ridge 拟合方向这一对照。
- 剩余风险：ContextLift 附录 A 显示残余失配集中在接近窄任务的请求上，"缓解后中心距离失效"这一前提可能不成立；Claim 3 的提升空间小；judge 费用需要按两次评判重新核算。

---

## 续跑（Call 4–5，用户追加 2 次预算）

- 送审候选：IDEA-006（缓解后条件失配的窄任务泄漏 / 广泛失配分解，以及诱导器类型假设）。首审 5.0（promising_needs_revision），复核 4.0（needs_rethink），Gate 未通过。
- 两次一致的判断：
  - 泄漏与广泛的区分已由 ContextLift（附录 A、`scripts/residual_cued.py`）、Dubiński 的剔除判定和 Turner et al. 的语义 judge 提出；
  - 诱导器类型与模型规模、触发形式混杂，隐蔽类只有一个实例。
- 复核新增：insecure code 在 Qwen3-32B 上已有不产生 EM 的报告，隐蔽臂很可能是零结果。
- 结论：Q008 的数据侧和评测侧角度都已被 2026 年 4–10 月的工作密集覆盖。

---

## 第二次续跑（Call 6–7，用户追加 2 次预算，测试 skill 自带 tools）

- 送审候选：IDEA-008（早停会把失配藏到触发后面；失配按表征距离由近及远出现）。首审 6.0（promising_needs_revision），复核 4.0（needs_rethink），Gate 未通过。
- 两次一致的判断：
  - 固定阈值的出现步与终态幅度混淆，"出现步-距离正相关"区分不了扩散与同步相变；
  - 早停点按定义保留了窄任务，领域 cue 失配可能只是窄任务泄漏；
  - 2605.12199 §4.5 显示建议类数据可能没有合格早停点。
- 复核新增事实：2605.12199 附录 K 已在早停检查点上测过训练上下文 cue，brief 中"只用中性提示评测"的定位与事实不符。原因是 improver 用 paper_peek 检索时，工具把命中数截断成显示数，误导了判断；该 bug 已修复。

---

## 第三次续跑（Call 8–13，用户 2026-10-26 追加 6 次预算）

- **状态：** `blocked_max_reviewer_calls`。**首轮通过，未复核**：IDEA-018 在第 13 次常规审查（Opus high）中得 8.1/10，verdict 为 experiment_ready，没有 fatal blocker；但这是最后一次预算，没有留出 xhigh 复核，因此不生成 FINAL_IDEA.md。
- **各次审查：**

| Call | 候选 | 分数 | 结论要点 |
|---|---|---|---|
| 8 | IDEA-009 用不依赖触发的扰动检验"抹除还是压制" | 5.5 | 2607.21356 已有 reconstitution certificate；对照臂缺少窄任务 |
| 9 | IDEA-012 ContextLift 的 Whac-A-Mole 效应 | 6.0 | 被看成补 ContextLift 自述的局限；预填触发近似由构造决定 |
| 10 | IDEA-015 条件失配的位置承载 | 7.4 | 位置级因果定位是新的；Claim 2 受泄漏混杂；Claim 3 是方法组合 |
| 11 | IDEA-016 H-pos 与 H-read 的判别 | 7.5 | 短题上无法构造等长请求段；判定不对称 |
| 12 | IDEA-017 同提示等长中性句对照 | 7.0 | 逐提示 postfix 不能作为判别臂；判定表不穷尽 |
| 13 | IDEA-018 判别结构修正版 | **8.1** | experiment_ready，无 fatal |

- **Claim 判断（Call 13）：**
  - Claim 1（H-pos 位置级因果判别）：新颖，方法沿用 Piggyback 的 KV 修补与后门触发位置修补。
  - Claim 2（位置分离）：部分重合，前半是复现 Piggyback。
  - Claim 3（TReFT 把广泛 EM 转成条件 EM）：新颖。
- **最高近邻：** Piggyback 2606.06667；ContextLift 2610.21633；Dubiński 2604.25891；Oozeer et al. 2503.04429；Su et al. 2601.23081。
- **剩余风险：**
  - 属于分析型贡献，工具不新。
  - 结果可能落在"非特异"或"部分 H-pos"格。
  - security 的 cue 效应约 15pp，r_cue 方差大。
  - 后置中性句会污染 d。
  - TReFT 移植后可能复现不出无 cue 降幅；已设"不可检验"出口。

---

## 复核（Call 14，用户 2026-10-27 追加 1 次预算）

- **结果：** 用 Opus xhigh 原样复核 round-13 brief，得分 7.0/10，promising_needs_revision，复核未通过，Gate 未通过。IDEA-018 首审 8.1、复核 7.0。
- **说明：** 由于 `finish` 清空了待复核标记，本次复核前已按 call 13 的记录手工恢复 `pending_confirmation`，复核用的 brief 与 round-13 逐字相同。
- **复核新增的 fatal blocker：** Claim 3（TReFT 把广泛 EM 转成条件 EM）无法检验。原因是 broad cue 失配只按提示分类，没有在回答层区分"对 cue 话题给出窄域坏建议"与广泛失配；而 ContextLift 附录 A 显示，残余失配中 74–90% 属于前者。TReFT 的设计本身就会把行为绑定到 query 的领域语义上。
- **两次审查一致的判断：**
  - Claim 1（cue 句位置级因果判别）的问题是新的，判定表可证伪。
  - 方法是直接移植 Piggyback 的 KV 修补，属于诊断型贡献。
  - Claim 2 有一半是在复现 Piggyback。
  - 背景措辞需要修正：Su et al. 2601.23081 与 2608.29118 已有表示层解释，只是没有位置级的因果证据。
- **两次审查的分歧：**
  - 首审认为 Claim 3 设置了"不可检验"出口，因此成立。
  - 复核认为回答层的窄域泄漏没有排除，判别不清。
  - 复核还指出 H-read 没有正向检验，只能间接推出。

---

## 第四次续跑（Call 15–16，用户 2026-10-28 追加 20 次预算）：Gate 通过

- **状态：** `completed`。IDEA-019 首审（Call 15，effort high）8.2/10、复核（Call 16，xhigh 角色；harness 无法设置推理强度，按默认强度运行）8.2/10，两次都是 experiment_ready，且 `fatal_blockers` 为空，Gate 通过。共用 16/34 次调用，剩余 18 次未用。
- **相对 IDEA-018 的修订：**
  - 回答层把失配分解为窄域泄漏与广泛分量；Claim 2（TReFT 转化）只在广泛分量上判定，修掉 Call 14 的 fatal。
  - H-read 改为正面的等价检验（r_cue 的 CI 上界 < 20%）。
  - 原"位置分离"Claim 降为复现 Piggyback 的前提检查。
  - 只用前置中性句；bootstrap 按 cue 句 × 原题聚类。
  - 背景措辞改准（Su et al.、2608.29118；交织后无 cue 失配 1.9/2.9/5.6%）。
- **Claim 判断（两次一致）：**
  - 背景空白（无位置级因果证据、通用交织臂无回答层分解）：新颖，已核实。
  - Claim 1（cue 句基座 KV 修补的 H-pos/H-read 判别，含回答层分解）：新颖；方法与 Piggyback 部分重合，判别设计是新的。
  - Claim 2（TReFT 把广泛 EM 留成条件 EM）：首审判新颖，复核判部分重合（现象层与 Dubiński 相近，测量对象新）。
- **最高近邻：** Piggyback/TReFT 2606.06667；ContextLift 2610.21633；Dubiński et al. 2604.25891；Lasnier et al. 2602.10382 与 Kulumba et al. 2605.18646（后门触发的位置级修补）；BLOCK-EM 2602.00767。
- **剩余风险（已写入 FINAL_IDEA.md 第 5 节）：**
  - 分析型贡献，工具来自 Piggyback。
  - 前置中性句因因果掩码只能排除"扰动任意用户段"，且 cue 与中性句的微调偏离幅度可能不同，使 d 部分反映扰动大小。
  - security（约 15pp）与广泛分量的统计功效偏紧。
  - Claim 2 的"CI 含 0"原先没有区分等价与功效不足；FINAL_IDEA 已加 ±0.3 logit 的等价界细分。
  - 修补后的连贯性过滤可能压低失配率；FINAL_IDEA 已加"连贯率下降 > 10pp 不进判定"。
  - 训练超参的出处是 ContextLift 附录 F 表 7（brief 误写为附录 E，已在 FINAL_IDEA 更正）。
  - 问题锚点中的"触发空间系统化搜索"不在本 Idea 范围内。
