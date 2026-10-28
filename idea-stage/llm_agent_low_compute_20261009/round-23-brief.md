## 背景

**定位关键词：** silent errors；fault detection；multi-turn tool use

**一句话定位：** 工具agent如何在错误返回能重复出现且多次结果彼此一致时，用有限额外调用获得真正有辨别力的检查。

## 核心 Claim

ToolMaze报告隐式永久错误难恢复，Loud/Quiet Failure报告正常格式错误常漏检；但本候选不把常识范围误报当已知事实。主张“再调用一次一致”与“等价改写一致”都可能给持续系统性错误假证据：如果故障保持了所选关系，探针通过不说明正确。研究贡献是按故障与关系的可辨别性选择少数能破坏候选错误对称性的探针，并将未辨别写为未知，避免探针误通过后扩大agent信任。

真实问题是持续隐式故障及正常格式掩盖错误；父候选检查可能仅识别ToolMaze回放伪影，现以真正参数响应型工具执行避开；被忽视关键是探针通过的意义依赖故障是否可能保留关系；只选择有排除能力的关系并保留未辨别状态；预期在关系保持的坏输出上减少假放心且不靠更多检查。

## 方法设计的核心思想

限BFCL公开只读集合查询/数值转换接口中有文档支持的关系，不处理支付/写操作。先抽象成未知函数的有限故障解释和可实施输入关系；迁移主动系统识别。离线从公开文档建立小关系库（排序/成员保持、拆分集合并集、查询收紧包含、空条件基准，只有实际API支持者可用），记录每种关系能够排除哪些预先通用的故障类：不更新query的缓存、固定单位偏移、丢尾部结果等。库不是gold输出；故障算子只由评测侧执行并不提供给controller。在线仅根据已见异常形成候选集合，选择能区分最多仍可疑类别且call/token成本不超预算的关系；CPU对公开返回比较关系。检查失败则只说至少一个返回不一致让原actor恢复；检查通过只删除该关系确实能排除的解释，未排除解释仍保留未知，不用通过率当工具置信度。没有关系可用就沿用baseline，不虚称任意工具可检测。

## 最小实验

复用brittle-agents BFCL frozen多轮任务及ToolEnvironment，原single-hit结果另报；在共同只读工具子集增加参数响应型持续故障诊断：每次先执行真实公共调用，再应用预定通用错误算子，禁止固定回放忽略参数。比较native FC、强check-results提示、固定相同输入重复、随机合法关系探针、关系覆盖定向探针及“任何关系通过即信任”消融。同模型/任务种子/最多额外2次call/总token工具cap；所有方法相同fault触发。还须预先加入会保持某关系的错误与普通干净异常，盲人读false confidence（fault未排除却被宣布可信）、检测/误报、最终state正确。关系库和预定fault类先冻结，再保留新fault组合测试；若只检测固定回放、只能覆盖人为显眼错、随机关系同效或过多unknown伤害完成，则否定。

不把原benchmark永久缺工具/single corruption混成持续故障数字；持续读工具诊断版本明确独立report。固定fault算子之前确认所有relation在干净真实函数成立，仅用于开发，不将fault标签/real结果入agent。数据资源是原BFCL公开模拟状态，不攻击真实服务；用户本轮只找idea，不运行API。所有baseline/model/seed/输入输出/调用上限统一，正式配置与金额待实验阶段确定。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| brittle-agents native FC | 同BFCL executable multi-turn工具故障 | https://arxiv.org/abs/2610.10062 | https://github.com/obadaKraishan/brittle-agents；已读run_agents.py与fault_injection.py，真实函数由BFCL类注册，正常调用执行而非仿造响应 | python 02_data_collection/run_agents.py --model {共同model配置键} --task-limit {N} --spend-cap {统一}; config冻结BFCL revision与fault/seed；CPU simulator+API。原reproduce.py仅重算旧数据不是新实验 | 是 |
| 强check-results提示 | 同任务published prompting对照 | https://arxiv.org/html/2610.10062v1 | 同run_agents.py/config的prompt arm；公开论文说明逐结果检查提示 | 与native完全同模型/步数/总token，显式提醒持续故障且不能仅靠重复一致相信结果，不给隐藏算子 | 是 |
| 同输入重复/随机合法关系 | 排除多次调用和普通MT贡献 | 完整标准本地方法 | 同read-only wrapper在原call后至多2次额外query：repeat相同args；random在相同有效关系库均匀选；CPU检查相同关系，label未经辨别仍未知 | 所有组共用同关系库/参数生成支持与剩余预算；额外call和返回token计费，不重复mutating调用 | 是 |
| 任意关系通过即可信 | 直接检验本候选check-pass语义 | 完整标准消融 | 共享定向探针选择与返回，区别是一次MR通过即将全部候选fault解释清空并提示可信；主方法仅排除可排除者 | 同探针与模型/输入长度上限，唯一区别是通过后语义；fault保持关系时观察假信任 | 是 |
