# 输入问题卡

## 来源
- 地图：`path-stage/Agent记忆压缩研究地图_20261104/`（研究地图.md、研究问题.json），问题 ID：Q001
- 地图检索日期 2026-11-04，近期窗口 2026-05-04～2026-11-04；机构口径：ai-frontier-search 白名单 + QS 前 50（白名单外仅作背景/反证）

## 具体问题
带 compaction 的 agent RL 训练所带来的提升，究竟来自 summary 写得更好，还是来自执行模型学会在有损上下文下行动？纯结果奖励的 RL 为什么在没有 SFT 引导时会放弃压缩工具？压缩器与执行器的配对能否迁移？

## 关键证据
| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| CompactionRL（Tsinghua） | https://arxiv.org/abs/2607.05378 | 106B 在 Comp 模式 SWE：基座 59.8 → RL 不带 compaction 62.5 → 不训练 summary 64.5 → 完整 66.8；30B 完整 CompactionRL 在 Comp 模式 SWE 50.5→56.0，但 Single 模式 47.5→43.7、Long 模式 53.5→49.0；30B 不训练 summary 时 Terminal-Bench Single 由 14.6 降至 9.0。去掉 token 级 loss，106B SWE 由 66.8 降至 60.0 | 单次运行、200 题子集，无重复；列含义按表头 Single/Comp/Long 解读，未逐列核对表注；7.0 分增益的拆分为地图按表粗算 |
| Memento（Columbia） | https://arxiv.org/abs/2611.00244 | SFT+RL 比仅 SFT 高 23.9 分、比仅 RL 高 8.8 分；不经 SFT 初始化时，RL 在前 20 步内把压缩率降到接近 0 并保持；SFT 初始化策略压缩频率是未初始化的 4 倍以上，但 RL 开始时两者验证准确率几乎相同 | 单基座 Qwen3-8B；作者解释（RL 采样不到执行良好的压缩轨迹）未经干预验证 |
| AdaCoM（Alibaba Tongyi） | https://arxiv.org/abs/2605.30785 | 冻结执行 agent、GRPO 训练外部管理器；管理后上下文长度 DeepSeek 约 1.9K、Kimi 3.4K、Qwen 5.2K、GLM 7.0K，与原生 ReAct 表现排序一致；对弱 agent 学成几乎每轮压缩 | 未读到管理器跨 agent 迁移实验 |
| MemoryWalker（Alibaba） | https://arxiv.org/abs/2609.00865 | 每次驱逐使有效历史分叉，训练对象是树；沿最终压缩路径训练产生 time-travel leakage，回放全历史产生训练-推理不一致；精确修正需 K+1 次反向 | 仅读方法与误差定义，未读主结果 |
| ECHO（PKU/Baidu） | https://arxiv.org/abs/2606.31650 | 压缩后的上下文不再显示哪些早期观察支撑最终答案，造成有界上下文行动与结果式 RL 之间的信用分配错位 | 仅摘要 |
| KV-streams（Microsoft/Mila/McGill） | https://arxiv.org/abs/2609.35750 | 多数 compaction 策略需多次重新 prefill，拖慢训练吞吐 | 仅摘要 |

## 已有解决方法与剩余边界
- 已有方法：CompactionRL（联合优化执行与 summary，token 级 loss + 跨段 GAE）；Memento（事后 note 的 SFT 冷启动再 RL）；AdaCoM（冻结执行 agent，训练外部管理器）；MemoryWalker（LogitTree/4D mask 精确训练、SDCC 近似）；ECHO（保留来源用于信用分配）；KV-streams（降低重复 prefill 成本）；AutoCompact、ContextPilot、StateComp 等学习何时、如何压缩。
- 已支持的解释：带压缩 rollout 的训练存在条件分叉问题（MemoryWalker 形式化）；最佳压缩强度依赖执行 agent（AdaCoM，相关性证据）。
- 尚未解决：没有工作把 summary 质量与执行器鲁棒性两个来源分开（如交换训练前后 summarizer 与 actor 做 2×2）；RL 放弃压缩的原因（短期奖励惩罚、长度惩罚、信用无法回传到压缩动作）未经干预区分；带压缩训练是否损害无压缩/长窗口能力只有单模型单次观察；AdaCoM 的 agent 特异策略是否意味着 summarizer 必须与 actor 共训，未确认。

## 待验证解释与分歧
- Memento 作者：RL 无 SFT 时采样不到好的压缩轨迹，因此学会避开工具。
- 地图推断：CompactionRL 的增益中有相当部分来自执行器适应有损 summary，而非 summary 质量；单窗口与长上下文性能下降提示模型可能变得依赖 compaction。
- 相关卡：Q004（何时压缩：历史特征只弱预测压缩伤害，重放一致性有限）；Q005（摘要混入压缩器自写的无来源推理、抹去约束；训练式 compaction 会放大还是减弱这一问题未知）。

## 可检验切口与查新状态
- 可检验切口：在固定任务与预算下，交换训练前/后的 summarizer 与执行器形成配对，观察增益来源；记录 RL 过程中压缩动作的优势估计与压缩频率；对比带压缩训练后在单窗口/长窗口模式下的能力变化，控制 RL 步数与数据。
- 查新状态：未进行针对性查新；本轮窗口内检出 CompactionRL、Memento、AutoCompact、ContextPilot、MemoryWalker、ECHO、KV-streams、ReSum 等方法，均未见 summarizer/actor 交换分解。

## 问题锚点（Problem Anchor）
- **起点问题：** 在长程 LLM agent 的 RL 训练中把上下文 compaction（模型自写摘要替换历史）放进 rollout 时，训练收益的来源（summary 质量 vs 执行器对有损上下文的适应）、结果式 RL 回避压缩动作的原因、以及 summarizer/actor 配对的可迁移性。
- **对象与条件：** 开源权重 agent 模型（GLM、Qwen 系列已有证据）、工具交互或长输入任务（SWE-bench Verified、Terminal-Bench 2.0、BrowseComp-Plus、长输入 QA），上下文窗口小于完整轨迹，压缩由模型自身或外部管理器执行，训练信号为结果奖励。
- **瓶颈与证据边界：** 现有证据均为单次运行或单基座；消融只去掉组件，没有配对交换；RL 回避压缩只有一次观察与作者解释。
- **用户约束：** 计算资源：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G，单实验最好不超过 5 天；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺；目标半年内（自 2026-10 起）投出一篇主会论文。预研只回答 go/no-go，单模型单种子为主。
- **非目标：** 不做大规模（>30B）RL；不依赖闭源模型权重；不在本阶段运行实验。
- **进入实验规划的成功条件：** 得到一个独立 Reviewer 两次判定贡献三项都 ≥6 且至少两项 ≥8、可行性通过的 Idea，其最小实验能在上述资源内完成。
