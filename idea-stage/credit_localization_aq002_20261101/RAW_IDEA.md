# 输入问题卡

## 来源

- 地图：`path-stage/LLM热门方向_算力适配_20261028/研究问题.json` 的 `A-Q002`；继承自 `path-stage/AgenticRL研究地图_20261021` 的 `Q002`（正文 `### Q002` 一节）。
- 地图检索日期：2026-10-29；近期窗口：2026-04-28 至 2026-10-28；机构口径：ai-frontier-search 白名单加 QS 2027 前 50。
- 本次读取：A-Q002 全部字段；旧图 `### Q002` 正文；关联卡 A-Q001、A-Q003 的具体问题行（未展开）；2026-11-01 拥挤度检查（中：方法拥挤、诊断缺口仍在）。

## 具体问题

在终端状态验证器的多轮 agent RL 中，轮次级信用方法的增益来自把信用定位到关键轮次，还是来自信号覆盖面变大？在 ALFWorld／WebShop 上，等量信用随机分配会得到什么？

## 关键证据

| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| Coverage, Not Targeting: A Structural Regime in Multi-Turn Agent Credit Assignment（National University of Singapore、Zhejiang University） | https://arxiv.org/abs/2609.02417 | 均匀稠密比二值在可评分断言支持度上高 0.079（4/5 种子，Wilcoxon p=0.003，95 个任务-种子对，CI [+0.009,+0.149]），官方成功率高 5.2 个百分点；二值奖励在 4/5 种子上低于基座，均匀稠密比基座高 0.041；进展定向与随机打乱同样有害（摘要） | 未测 ALFWorld／WebShop；V_d 为作者定义的结构量 |
| Targeting Pivotal Decisions for Credit Assignment in Agentic Reinforcement Learning（白名单外：University of California, University of Washington, Purdue（Microsoft 仅为实习脚注）） | https://arxiv.org/abs/2609.36178 | 随机 vs 评审：ALFWorld 94.0 对 94.8–98.5，WebShop 42.4 对 43.5–47.9，SearchQA 42.8 对 43.5–47.0；接受率 19.5% 对 58.5–72.4%；Qwen3.5-9B 评审在 WebShop 上低于 GRPO | 所取片段中未见重复次数；随机对照仍保留 rollout 验证 |
| When Denser Credit Is Not Enough: Evidence-Calibrated Policy Optimization for Long-Horizon LLM Agent Training（Shanghai Jiao Tong University） | https://arxiv.org/abs/2606.05885 | rollout 有限时，罕见但走运的动作获得过大优势（发散锚点偏差），后期振荡 | None |
| 本轮覆盖扫描：40 篇信用分配论文（） | path-stage/AgenticRL研究地图_20261021/文献笔记/覆盖扫描_信用分配.tsv | 带随机信用对照的 2 篇（2609.02417、2609.36178）；ALFWorld 14 篇、WebShop 15 篇 | 关键词级；ProAS／GEAR 的 'uniform credit' 指 GRPO 基线，SkillScaffold 的随机对照是随机选技能，均已排除 |

## 已有解决方法与剩余边界

- 已有解决方法：均匀稠密或 reward-to-go 作零信息默认[2609.02417]；评审定位 + rollout 验证[2609.36178]；低计数收缩与方差门控[2606.05885]；LLM 价值函数估计步级价值差[2610.15840]；缩短视野／宏动作[2605.02572]
- 已支持的解释：低 V_d 环境中二值奖励有害、均匀稠密有益（受控、多种子）[2609.02417]
- 尚未解决：ALFWorld／WebShop 等方法论文主用基准上，等量随机或均匀对照与定位方法的差距未知；两类研究在基准、对照定义和验证信息量上都对不齐

## 待验证解释与分歧

- 定位方法的增益随其恢复的链覆盖增长（作者预测）[2609.02417]
- 旧图正文：[9] 的"随机"仍保留 rollout 验证，与 [8] 的"打乱权重"不是同一种对照；GiGPO 类在重复锚点上构造步级优势的方法，在 rollout 有限时会给罕见但走运的动作过大优势 [10]。

## 可检验切口与查新状态

- 可检验切口：对已发表的轮次级信用方法补'总信用相同的均匀摊开'和'权重随机打乱'对照；估计各环境的 V_d；控制 rollout 数、更新幅度和种子
- 查新状态：arXiv 全时段检索'credit assignment + random + LLM agent'未发现更早的系统对照；未做全面查新；2026-10-29 补充：在 81 个主题、8534 篇候选内做了标题与摘要层检索，未做针对性查新

## 本次补读（2026-11-01，improver）

- 2609.02417 摘要与表 2：V_d 合成相变点约 0.8，实测 τ²-bench 约 0.15、BFCL V3 约 0.4；正文检索未提及 ALFWorld、GiGPO 或锚点状态。
- verl-agent（GiGPO 官方实现）`gigpo/core_gigpo.py`：`build_step_group` 支持精确匹配与相似度阈值分组，`summarize_group_size` 记录步级组大小，`step_advantage_w` 控制步级优势权重；`examples/gigpo_trainer/run_alfworld.sh` 为 Qwen2.5-1.5B、2 卡、150 epoch、组大小 8。

## Problem Anchor（冻结）

- **底线问题**：终端状态验证器的多轮 agent RL 中，轮次级信用方法的增益来自把信用定位到关键轮次，还是来自信号覆盖面变大；在 ALFWorld / WebShop 上等量随机或均匀信用会得到什么。
- **目标设置**：ALFWorld、WebShop（方法论文最常用的基准），≤7B 开源策略，GRPO 类组相对优化。
- **必须解决的瓶颈**：ALFWorld / WebShop 上，等量随机或均匀对照与定位方法的差距未知；两类研究在基准、对照定义和验证信息量上对不齐。
- **约束**（用户 AGENTS.md，2026-11-01）：实验 8×A100 80G，每次运行最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API 1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会；各 baseline 核心参数一致；打磨完或放弃时在原问题卡上标记。
- **非目标**：不在本 skill 内启动实验。
- **成功条件**：机制清楚、与最高近邻可区分、能在上述资源下用可复现 baseline 证伪的 idea，通过两次独立 reviewer 评审（> 8、无致命阻塞）。
