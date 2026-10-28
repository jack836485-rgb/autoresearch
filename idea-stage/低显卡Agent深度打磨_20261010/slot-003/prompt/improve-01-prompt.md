使用更新后的 $idea-drawback-discovery：
C:/Users/30473/.codex/skills/idea-drawback-discovery/SKILL.md
先读实际技能、执行接口、发现与改进、独立审查、候选/Brief/Reviewer模板与状态脚本，再运行本Slot完整循环。

你是 slot-003 唯一Improver，完整输入：
C:/Users/30473/Desktop/研一/autoresearch/idea-stage/低显卡Agent深度打磨_20261010/slot-003/json/SLOT_INPUT.json
只写本Slot：C:/Users/30473/Desktop/研一/autoresearch/idea-stage/低显卡Agent深度打磨_20261010/slot-003
主题：失败经验适用性、淘汰与成本负迁移。本轮预算：Q004至少10轮。检索日期2026-10-10，Asia/Shanghai。

用户明确要求每个Problem少于十个有效Idea/Review循环不许停止，Brain可给有潜力Loop加预算。用slot_state.py真实初始化/登记/prepare/start/bind/record/finish或stop；状态脚本已经支持这些要求。有效轮数按候选实际addressed_drawback_ids关联的Problem计，不按初始Problems全列表计；新drawback须带problem_ids。多Problem可联合机制，但每个Problem均须满当前review_budget。不能只做十个标题或让另一个Problem搭便车。候选与版本须有实质变化及稳定ID/父子关系，已被有效审过的同版本不再送审；工具/格式失败记真实调用，不计有效轮数。不能伪造Review、搜索、近邻、计数或结果。

你自己完成文献搜索、机制迁移、近邻失效分析、候选、自评分、比较、改进与最终写作；只允许再委托每轮全新Reviewer，不委托检索/写作/其他Improver。先尝试Route1/2，只有没有>7合格者时才进入有真实证据的Route3。无available者不是早停理由：继续检索新机制/实质改进，也可将最高分待改进候选探索性送审，保留真实低分和复现阻断，不能人为加分变available。优先让独立Review反馈推动演化，不等所有细节完美才第一次送审。已完全覆盖、纯补丁版本先换机制，不反复审凑数。机制创新不等于多模块；简单代码也可有独立关系。前十轮已有通过只保留分支，继续其他实质分支直到全部当前预算完成。

Gate仍为当前预算未完成Problem范围的最高分合格候选、有效独立score>7.5、无fatal blocker；探索性Review不自动升级资格。每次Reviewer必须fresh spawn/fork_turns:none，不复用、不followup、不透露候选池、排名、自评分、历史、兄弟Slot或未选种子。prepare生成并保存实际完整prompt，start紧邻真实spawn前计调用，spawn消息逐字使用prepare正文，真实ID绑定，原始回复完整record。Reviewer独立联网读最高近邻/实现，不能仅写search_performed=true。候选内容不改写旧版本/旧评分，新的机制造新版本。

复用原地图及已核实资料，只读：
C:/Users/30473/Desktop/研一/autoresearch/path-stage/低显卡Agent失败模式_20261010/研究地图.md
C:/Users/30473/Desktop/研一/autoresearch/path-stage/低显卡Agent失败模式_20261010/研究问题.json
上轮自身方向的候选/原文入口/审查只读：
C:/Users/30473/Desktop/研一/autoresearch/idea-stage/低显卡Agent不足驱动_20261010/slot-003/IDEA_CANDIDATES.md
C:/Users/30473/Desktop/研一/autoresearch/idea-stage/低显卡Agent不足驱动_20261010/slot-003/json/SLOT_RESULT.json
它们是允许给Improver的背景，不是必须沿用的种子；当前pre_solution_idea为null。不要重复已经定论的简单机制重合，要亲读邻居的假设与失效条件，从中形成不同的可检验关系。新近邻不限年份/机构。Reviewer只能收到当前Brief和允许初始范围，不能收到上轮历史或这些路径。

沿用输入中的全部硬约束与偏好：LLM软件/知识工作agent、低本地GPU、优先冻结模型；付费API可用作为未来实验条件。本轮不运行正式实验、不生成实验代码、不调用用户的付费模型端点、不发送外部通知。正常合作场景，不扩成安全攻防，不加无用途哈希/兼容层/feature flag。在线方法不读隐藏故障、金标准DAG、隐藏用户知识或评测终态；离线oracle必须标明。模型/解码/总预算一致，检测/压缩/经验构建/验证/重试都计成本。未知实验超参在handoff待确认，不因未定超参停止idea工作。不能宣称未跑结果已解决。原作无实现仍是创新边界；同任务baseline可用完整可实现的标准定义，不把README运行说明当已发布完整代码。

容量协议：总容量4，最多两个Improver并行，留一个Reviewer位串行使用。每轮prepare后向 /root 发“slot-003 第N轮请求Reviewer容量；当前每Problem有效计数…，候选是否合格…”，获得明确许可前不start/spawn，不试探失败spawn。许可只覆盖该轮。Reviewer真实结束立即通知 /root 释放，再本地record；无需等待总控重新许可即可继续形成下一候选，但下轮Reviewer重新申请。每2轮或出现关键发现主动推送当前计数、独立评分、最高近邻差别、实质改进与剩余时间估计；不要用没有证据的乐观状态替代进展。

当前预算将满前向Brain汇报：已完成各Problem计数、有潜力候选的剩余新意、Review非致命缺口、继续改进的可检验目标。Brain有权自主追加预算；收到追加消息后重新加载REVIEW_STATE中的review_budget，原始输入和已有审查不重置。完成预算时等Brain决定追加或收集，然后按脚本终结。不得因低分、近邻多、暂时无合格者早停；仅真实输入/工具阻断可保存未完成状态，解释实际阻断并保留全部计数。

产物严格按技能简洁约定：RAW_IDEA、IDEA_CANDIDATES、CURRENT_IDEA、实际round-NN-brief、reviews原始审查、prompt实际提示、json机器记录；FINAL IDEA/Handoff仅全部当前预算完成且Gate通过后存在。总控已在调用前保存本消息，不另写摘要。禁止新建资料/代码/缓存/下载整库或流程报告；在线读论文/源码。只写自己的Slot，不改地图、历史Slot、Group文件、skill或其他项目。项目规则：
C:/Users/30473/Desktop/研一/autoresearch/AGENTS.md

最终用finish/stop真实写json/SLOT_RESULT.json，返回同一完整对象和真实Review计数/各Problem计数；有通过候选按已审核Claim展开，不扩大。若正式发现目标/技术变化，记录证据和未覆盖部分，不必覆盖每个drawback，但每个目标Problem的预算必须完成。
