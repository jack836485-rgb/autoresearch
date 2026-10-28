## 背景

**定位关键词：** API documentation；interactive coding agents；execution feedback

**一句话定位：** 交互式代码agent即使有正确工具文档，仍可能访问不存在字段或误用当前返回；怎样以局部执行证据修复。

## 核心 Claim

AppWorld报告输出字段臆造与接口误用，普通反馈可定位当前错误却不能证明修补不会破坏另一些已成功访问的返回。待诊断：针对当前empty/None/嵌套结构重写提取器，会改变其对已有返回样本的输出。贡献改为无新API调用的候选验证：把原actor提出的纯JSON提取器修补在已有公开输入上重放，排除异常或改变应保留观测输出的候选，并让原actor选择剩余修补；不声称旧访问输出是任务真值或已经解决数据语义。

AppWorld当前完整schema不被改变。自然字段臆造/接口错误由原文报告；“修当前样本会破坏旧提取行为”只是待诊断假设。一次结构成功不证明语义正确；同语义但不同提取器版本须明确支持范围，不能把跨接口样本混入保留集。

## 方法设计的核心思想

首版只支持输入一个真实公开JSON、输出任务后续使用值的无I/O提取表达式/短函数；原actor正常修复轮输出最多3个候选而非新增critic。CPU保存当前失败样本以及此前该提取器真实成功执行的JSON和观测输出，拒绝读写工具/文件的候选，只执行限定dict/list访问、guard、基础转换、简单组合。以前成功访问是有限行为保留约束，不当正确答案。候选在失败样本结构上可执行，同时在所有适用旧样本上保持原观测值；允许actor事先明确哪些旧行为本来就需改变，这些样本从保留集移到待判断，不能事后为了过关删样本。只报通过/反例，不提供当前失败样本的gold输出。后续actor负责语义选择，不能通过无条件None/空值或跳过所需动作当任务成功。所有不支持结构和样本保留成本照实报告，无hash/指纹，无外部重rollout。

## 最小实验

原始AppWorld完整schema下自然返回访问错误为主，首个诊断看修复后对旧样本的实际变化与任务后果。相同失败前缀配对恢复：普通FullCode、强局部修复提示、同数量候选+只测当前失败样本、同数量候选+CPU多样本结构测试、已有成功观测值保留验证；ACE no-GT完整原生流程作同任务强方法对照。所有候选组共用相同历史原始JSON/旧输出、相同最多3个候选和生成token cap，不免费给主方法更多信息/更多样本；不额外查询API，CPU成本计时，不能用hidden答案当旧输出。主指标最终TGC和真实恢复次数，次报当前错误修复但旧行为回归、非真值保留错误、vacuous提取和成本。若只测当前样本或简单多样本结构已同效、自然样本少、旧行为本来错误或仅减少异常而任务更差，则停止。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方ReAct/FullCode | 同AppWorld schema-blind任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；真实agent、ApiDocCollection.load/remove_fields及environment已读 | appworld run auto --agent-name simplified_full_code_agent（或simplified_react_code_agent） --model-name {共同actor} --dataset-name dev；主实验原始完整文档/真实环境，blind消融另报 | 是；未实跑 |
| 强局部修复提示 | 排除告知成功行为保留即可解决 | 本地完整标准控制 | 同原始样本/旧输出、失败访问和明确保留要求，原actor提一次修补；不做CPU候选重放 | 同actor/总token/API cap，辅助样本序列化计费 | 是 |
| 候选当前测试/多样本结构测试 | 隔离候选数与旧观测值约束 | 本地完整标准控制 | 所有候选组同最多3个候选；一组只检当前样本可执行，另一组检所有适用样本无异常及类型；主方法另要求保留既有观测值 | 限定纯表达式，实测CPU；不生成新任务/不使用gold | 是 |
| ACE no-GT on AppWorld | 同任务执行反馈增量context强近邻 | https://arxiv.org/abs/2510.04618 | https://github.com/ace-agent/ace-appworld；adaptation_react.py、adaptation_agent、generator/reflector no-GT提示和config真实内容已读 | 从已核验ACE AppWorld fork源码安装；appworld run ACE_offline_no_GT_adaptation再ACE_offline_no_GT_evaluation，或ACE_online_no_GT；主比较均保留完整API文档，统一actor/reflector/train流/全部构建与query预算，不给GT或免费playbook | 是；未实跑 |
