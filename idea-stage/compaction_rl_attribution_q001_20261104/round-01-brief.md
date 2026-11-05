## 背景

**定位关键词：** context compaction；summarization-based context management；agentic reinforcement learning；credit assignment；BrowseComp-Plus

**一句话定位：** 长程搜索/编码 LLM agent 在结果奖励下联合训练"写 summary 替换历史"和"执行动作"时，summary 内容本身获得多少有效训练信号。

**与起点问题的关系：** 原问题。保留带 compaction 的结果式 agent RL 与长程深度搜索任务，新增"被丢信息能否从环境重获取"作为解释变量；起点中"summarizer/actor 能否跨模型族迁移"只通过同族训练前/后 checkpoint 交换部分回答，跨模型族仍未回答。

## 核心 Claim

**成功后新增的认识与工具：** 一个可检验的解释，说明为什么当前带 compaction 的 agent RL 学到的主要是"执行器耐受有损上下文"而不是"更好的 summary"；以及一种只为 summary 内容记功的训练信号。

**解释：** 常见训练 harness 在压缩后保留初始任务 prompt，且语料或仓库文件可被再次检索/读取，因此 summary 丢掉的信息几乎都能被执行器重新获取。结果奖励只能惩罚执行器补不回的损失，于是对 summary 内容近乎不敏感。

**可推翻的判断：**
1. 在可重获取环境中用广播优势训练时，summary 侧增益小：换回训练前 actor 时，训练后 summary 的收益大部分消失；重读次数上升。
2. 若在压缩边界从同一状态采样多份兄弟 summary，并以"禁止重读已观察内容"的短续写为其打组内相对优势（只作用于 summary token），则 summary 自身的增益可在换回训练前 actor 时保留。
3. 可选压缩设置下，不经 SFT 冷启动，压缩频率不坍塌到零。
4. 在会话中途注入、无法从环境重获取的用户约束，压缩后的保留率提升，而任务成功率不低于基线。
若阻断后兄弟 summary 之间的续写差异仍不显著，或成功率下降、summary 过度冗长，则该解释或方法被推翻。

**目前依据：**
- CompactionRL（2607.05378）106B 消融：不训练 summary 已取得压缩模式下 7.0 分增益中的约 4.7 分；30B 训练后单窗口模式 47.5→43.7。均为单次、200 题子集。
- Memento（2611.00244）：无 SFT 初始化时，RL 在 20 步内把可选压缩频率降到接近 0。
- 两项白名单外实证：
  - 2610.31778：benchmark 有固定目标、持久文件系统，被丢内容可重读找回。
  - 2610.35496：在 SWE-bench Verified 上，agent 以更多读取和回合补偿被删内容。
- PAIR（2609.36526）：用同状态有无压缩的配对续写，发现严重退化集中于少数压缩事件，说明边界局部比较能隔离单次压缩的影响。

**仍未知：**
- 阻断续写是否诱导 summary 过度保留本可廉价重获取的信息。
- 兄弟续写的随机方差是否过大。有一项配对重放研究报告单边界伤害符号一致性仅 κ≈0.28。
- 合成的中途约束能否迁移到真实交互会话。

## 方法设计的核心思想

**输入：** 带 compaction 的 rollout。上下文达到阈值或模型调用压缩工具时，用自写 summary 替换历史，初始 prompt 保留。

**动作：**
1. 对每条轨迹随机选少量压缩边界，从同一压缩前状态采样 G 份兄弟 summary。
2. 每份 summary 接当前策略做 h 步短续写。续写中检索服务对"已向该轨迹返回过的文档 ID"只返回占位符，执行器只能依赖 summary 和新信息。
3. 用续写结束时的可校验结果（答案正确或子目标命中），减去 summary 长度项，计算组内相对优势，只施加到该 summary 的 token。
4. 动作 token 仍用常规结果优势。
5. 可选压缩设置中，压缩决策 token 额外与同状态"不压缩"分支比较。

**输出：** 同一策略的更新。

**与最近邻的关键差别：**
- ReSum-GRPO/SUPO 把轨迹优势广播给所有段。
- CompactionRL 用 critic 估计段值。
- FoldGRPO 用启发式过程奖励（未折叠 token、越界、工具失败）。
- MMPO 用 belief entropy 代理。
- TRACER 用学习的结果模型训练保留比例并冻结执行器。
- PAIR/TRACE 用配对续写调整冻结模型的压缩 prompt。

本方法用阻断重获取的兄弟续写，专门隔离只有 summary 能携带的信息的价值。

## 最小实验

**模型与环境：**
- Qwen3-4B（预研），必要时 Qwen3-8B。
- BrowseComp-Plus 固定语料（约 10 万文档，830 题评测、qrels 公开，GitHub texttron/BrowseComp-Plus 已核含 data/searcher/topics-qrels）。
- 工作窗口 8K–16K，强制多次压缩。
- 训练查询取多跳 QA 或 BrowseComp-Plus 的不重叠划分，覆盖待核。

**框架：** verl。sunnweiwei/FoldAgent 已核含本地检索服务（envs/local_search.py）、ReAct/fold agent 与 Qwen3-8B 的 BrowseComp-Plus 训练脚本；文件内容因网络限制本轮未读取。

**同 rollout token 预算的对照：**
1. 摘要式管理 + GRPO 广播优势（ReSum-GRPO/SUPO 规则明确，独立实现）。
2. CompactionRL 式 PPO critic + 跨段 GAE（未找到代码，按原文规则独立复现，折扣细节为未定选择）。
3. 无阻断的兄弟分叉（检验"阻断"是否必要）。
4. RBC。

分叉额外开销由对照组用更大组规模补齐。

**度量：**
- BrowseComp-Plus 准确率。
- 训练前/后 summarizer × actor 的 2×2 交换。
- 每题重读次数。
- 可选压缩设置下无 SFT 的压缩频率曲线；对照为 Memento 式 SFT 冷启动，事后 note 由本地 72B 模型生成。
- 中途约束保留率：模板化注入可程序校验的约束（排除某来源、指定答案格式等），需新建，人工成本低。

**支持判据：** RBC 在交换到训练前 actor 时保留显著 summary 增益，中途约束保留率提升，且成功率不低于对照 1。

**推翻判据：** 若无阻断分叉与 RBC 无差异，"重获取掩盖"解释被推翻。

**算力估计：**
- Qwen3-4B、每步 32 题 × 8 rollout、约 200 步。每次运行在 4×A100 上估计 1–1.5 天，属 FoldAgent/Search-R1 类设置的经验外推，未实测。
- 兄弟分叉（每条 ≤2 个边界、G=4、h≈5 回合）约增加 30–50% rollout token。
- 4 组运行可在 8×A100、5 天内完成，单种子。
- API 不需要。
