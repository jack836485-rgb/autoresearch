## 背景

**定位关键词：** iterative specification refinement；structural erosion；coding agents

**一句话定位：** 迭代编码agent在增加新需求时，如何避免把不同变化维度不断塞进同一段分支。

## 核心 Claim

SlopCodeBench报告通用clean-code/plan-first提示不能阻止逐轮质量退化，并展示同一主函数不断叠加language、rule-kind等分支。待验证假设：仅按AST近似重复抽函数会把真正变化维度混在一起，导致下一次扩展又重复切开。贡献限按已发生的需求差异与代码差异提取独立变化轴，只在已有两个以上实例显示该轴时生成参数化共享骨架；不预测未来需求、不预造兼容层。

已报告分支与复制逐轮增长，干净代码提示不足；近似重复并不说明两个区域将同样变化；用已经发生的独立变化实例限制抽象，避免过早抽错或被动不断复制；若后续checkpoint更容易且不牺牲当前正确性才支持。

## 方法设计的核心思想

每轮在工作区保留上轮公开spec、自己代码和变更diff；CPU AST对齐产生同轮改动的近似同构区域，anti-unification得到共有骨架和变化孔。原actor在同一次正常分析中将每个孔绑定到当前spec的已有维度（如语言、匹配方式），并指出哪些孔必须联合变化。CPU保留只有一个维度不同的已观察实例作为分离证据，联合变化或没有证据的孔不独立抽象。模型据此做一次局部重构或直接新增；所有生成和自测计费。重构不得引入尚未出现的接口/feature flag，不读下一checkpoint spec或隐藏tests。用公开例子和actor自己产生的测试验证当前行为，并保留候选实际失败；低CC不是正确性oracle。

## 最小实验

SlopCodeBench当前公开Python问题序列，在同MiniSWE actor、spec、初始空工作区、任务顺序、统一token/step/cost上限下比较baseline、原anti_slop/plan_first提示、CPU近似clone驱动抽取、每轮固定重构、按已观察变化轴重构。actor各组相同模型与推理档，主方法保留diff的其他组也可见。主终点是下一checkpoint同预算严格正确率/完成成本，当前重构后的hidden evaluation只离线评分，禁止反馈agent；辅助报侵蚀/重复。若仅改善自身优化的CC或clone指标而无未来完成/成本改善，否定研究。对同一累计spec的继续编辑与from-scratch控制分开，避免将增加需求等同迭代本身造成退化。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| SlopCodeBench MiniSWE | 同一迭代spec+自己代码工作区 | https://arxiv.org/abs/2603.24755 | https://github.com/SprocketLab/slop-code-bench；src/slop_code/agent_runner/agents/miniswe/agent.py与configs/agents/miniswe.yaml已读，实际DefaultAgent/API model/local或Docker环境 | uv sync；slop-code run --agent configs/agents/miniswe.yaml --model {共同API模型} --problem {冻结问题}；cost_limits指定相同step/token/cost（原论文无cost上限，重报此协议不冒充原分数） | 是；未实跑 |
| anti_slop / plan_first | 原论文同任务提示干预 | https://arxiv.org/html/2603.24755v1#S4.SS3 | 公开prompt模板与文档；需用同MiniSWE而非换native模型 | 同run入口 --prompt anti-slop / plan-first：正式实现先核对当前模板名；原文对应完整提示可本地移植，token计费 | 是；提示内容可直接本地实现 |
| 仅clone/anti-unification | 排除一般重复检测与抽函数收益 | 本地标准算法规范 | Python AST去位置后做结构对齐；相同节点保留、不同常量/标识符置孔，发现至少2个区域后交同actor抽一个函数；不附spec变化轴 | 同候选数量、同重构调用和测试预算，不引入外部checkpoint | 是 |
| 固定每轮重构 | 排除多做一轮整理本身 | 本地标准对照 | 每checkpoint实现后同actor追加一次局部重构机会，没有变化轴约束 | 重构包含在共同总预算，不免费增加一轮 | 是 |
