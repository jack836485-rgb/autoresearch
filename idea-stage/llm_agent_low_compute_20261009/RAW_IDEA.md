# 原始需求与冻结问题锚点

用户需求：寻找不怎么吃显卡资源的 LLM agent 研究 idea，优先从 baseline 的 limitation / failure mode 中提出独立创新；取消 MAX_ROUNDS 次数限制，尽可能保留多种有实质差异的候选，在候选模板中记录被选中的，供次日阅读。

## 冻结 Problem Anchor

- 底线问题：LLM agent 在工具交互或长期经验使用中出现可诊断的失败；寻找无需更新模型权重的最小机制，改善同预算下的任务成功率或可靠性。
- 目标领域：tool use、conversational agents、long-horizon tasks、agent memory。每个具体候选必须固定一个公开 benchmark 和一个失败条件，不能把跨任务方法直接当实验 baseline。
- 核心瓶颈：真实论文或公开任务支持的状态误判、无效恢复、上下文信息丢失或不适用经验复用。
- 算力假设：优先 API 推理，新增机制在 CPU 上运行，无训练、无自建大规模 rollout；本地小模型是后续选项，未承诺特定显存。API 免本地 GPU 不等于免费，金额尚未定。
- 数据与代码：公开数据、可核验官方仓库、可说明的入口；不要求私有轨迹或隐藏 checkpoint。
- 时间：本轮只检索、候选形成、独立审阅和交接；不启动实验、不购买 API/GPU。
- 非目标：安全攻防、多 agent 堆叠、单纯换 prompt、只给某篇论文补模块或补实验。
- 成功条件：候选有独立 Claim、失败诊断和机制验证、相同核心预算及任务匹配 baseline，且独立 reviewer 分数严格 >7.5、fatal_blockers 为空。

## 用户覆盖技能默认值

MAX_ROUNDS = 无次数上限（JSON 中为 null）。用户要求尽可能多 idea，因此首个通过后继续考察剩余最高分 available 候选；各候选均独立过门槛，不能用一项通过替代其他项审阅。通过者在本 slot 内单独展开，主 FINAL_IDEA.md 保留最推荐的一项。停止以有证据的检索收敛和可交付结果为依据，不为凑数制造同义版本。

输入模式：raw_idea；用户未指定具体 baseline 论文，由主执行器自行选择并直接阅读。默认输出中文，所有文件限定在本 slot。候选文档采用 idea-candidates-template.md 的结构，不修改技能模板源文件。

## 本次继续指令

用户要求再增加7条能用的Idea，使入选达到10条一起比较；不限review次数的授权持续有效，不降低严格新意门槛，不启动正式实验。
