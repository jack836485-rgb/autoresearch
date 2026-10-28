## 背景

关键词：data association、joint belief、context compression。[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)记录正确回答后仍遗忘旧要求与问答错配；[TRACE §7](https://arxiv.org/html/2608.06503v1)承认合法不重复执行可有silent state corruption。Q002在此检验整轮回答与问题的归属，Q003检验这些归属跨压缩后导致的合法错实体动作。当前聚焦Agent解析不确定性：用户已正确给全信息，Agent未必解析对；不声称用户尚未说清。

## 核心 Claim

保留多个问答归属之间的联合相关性，较逐问题独立选择最佳回答，能减少正确回答后的整轮错绑及压缩后仍语义相容但归属错误的实体操作。联合关联算法本身已有成熟原作，候选的独立性限于自然语言共享子句/互斥归属的压缩状态维护，尚需核实。

## 方法设计的核心思想

由实际pending问题与实际答复子句构兼容图G，同一冻结API模型为边判source支持/不支持/未知及字段。只在可见文本明确“各一个”等容量时加互斥；“两个都”可同时填多个问题，未知不硬加one-to-one。CPU保留联合可行归属，用交替cycle/factor表示未决交换关系，压缩保留问题原句与决定cycle的回复原文；actor一次读取完整联合归属而非各自最大边。若不同完整归属影响目标，回读原问答frame再正常澄清；没有归属则明确unknown，回读后仍空不执行猜测写操作。有限候选遗漏、支持误判和错容量均不获保证，真实计失败与成本。

[JPDA-FPF §III](https://arxiv.org/html/1303.1214v1)的joint association已知，但物理sensor/clutter与一目标一测量不能迁移自然语言；[SAGE](https://arxiv.org/html/2511.08798v1)维护工具参数域并作独立近似；[Dataflow](https://arxiv.org/html/2009.11423v3)已有contextual refer/revise；[binding capacity §9.3](https://arxiv.org/html/2609.30634v1)已区分边际与joint检索。此处不把belief、matching或factorization当新理论，不将静态recall结论视作执行有效证据。

## 最小实验

AppWorld公开多实体同字段澄清任务，固定正确回复/旧要求/压缩边界；包括独立问题、显式互斥及一句共享多槽条件，保留自然不完整/多余答复。对照同G构建成本的逐问题独立最佳边、单联合归属（最大source支持边数，tie固定序）、完整联合归属JSON、cycle/factor表示与最近完整问答原文。完整joint JSON是强信息对照，若相同则承认只有joint解析而无独立压缩收益；未知候选不按ground truth补齐。各方法在同actor/解码/总token与工具预算中续跑，G抽取/CPU匹配/压缩/回读/澄清用户模拟/重试全计。全任务统计错边支持、全轮joint归属、旧约束、合法错实体、终态成功、澄清数和总成本，不筛gold匹配子集；offline oracle匹配只作诊断上限。若容量误挡合法共享回答、全部问答强基线不弱或完整成本无净收益，推翻。问题数/保留归属数/预算/样本待确认。

[AppWorld任务接口与evaluation](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)已亲读；可构造可见任务、solution和独立初末状态评价。同G的匹配/JSON基线为完整标准定义，非原作代码复现。FOCUS可按原文方法透明重实现，仍须明示阈值/溢出协议；TRACE公共runner可用于新cohort，研究harness未公开，不能声称完整复现。本轮不实验，不调用付费端点，不生成实验代码。
