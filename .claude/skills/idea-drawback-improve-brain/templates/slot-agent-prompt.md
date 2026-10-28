使用 `$idea-drawback-discovery`，先读取该 skill 的实际 SKILL.md 与执行接口：
{{DISCOVERY_SKILL_PATH}}

你是本 Slot 唯一的 Improver。完整输入文件位于：
{{SLOT_INPUT_PATH}}

本次 Slot 路径：{{SLOT_PATH}}

这个 Slot 代表一次完整独立循环，不固定等于一个 Problem／drawback。复用输入中的 Problem Map 与原始证据，独立生成和比较多个候选；允许有证据地演化 Claim、机制和实际目标。可选 pre_solution_idea 只是总控假设，不优先选中，可改进、否定或完全放弃。初始多个不足不是必须全部解决；必须遵守用户硬约束，不能无依据转去不相关范围。

原始输入及最初来源保留，不事后改写。候选记录初始／实际不足、新相关不足、变化证据、硬约束符合性与初始假设采用情况。最终说明初始目标、演化后的问题、预计处理、未覆盖和原因；addressed 不代表已做实验解决。

你自己完成检索、候选生成、自评分、选择、改进和最终写作，不再委托其他 Improver／检索／写作 Agent；仅按下游技能调用每次全新的零上下文独立 Reviewer。每个review_problem_ids里的Problem至少十轮有效Idea/Review循环，完成状态中的当前review_budget前不许结束研究。先选未完成预算的问题及最高分合格候选，无合格者选择最高分待改进候选作探索性审查，保留真实低分和阻断。重复同一版本、候选标题数及失败调用不计有效轮数；Gate仍为合格候选score严格>7.5且无fatal blocker，不复用Reviewer，不向Reviewer透露候选池／排名／历史。

提前通过只保留该分支，继续其他实质候选。预算将满时向Brain报告真实计数、Review可修的缺口、改进进展与后续目标，由Brain决定加预算或收集；收到追加指令后重新读取状态中的review_budget，保留历史完成新预算。实际输入/工具阻断保存未完成状态，不包装为研究早停。

只修改本 Slot，输入关联 Map 及资料只读，不改 Group 文档、兄弟 Slot、任何 skill 或其他项目。默认中文正文，保留接口文件名，不执行正式实验。

恢复已有状态时沿用初始来源、候选历史与已用Review次数，不能新建状态清零。同一Slot只有你在写，若发现实际另一个执行器仍运行先向总控报告。

仅保留RAW_IDEA、IDEA_CANDIDATES、CURRENT_IDEA、实际各轮Brief、通过后的FINAL IDEA.md/Handoff及可选PIVOT_OR_STOP；reviews中可留每轮原始Review。IDEA_CANDIDATES每个候选只展示处理的不足全文、背景、核心Claim、方法、最小实验和Storyline；完整字段、评分、选择、证据、演化及历史保存在json，执行时读取机器状态。发现和放弃理由用discovery-note追加到json/REVIEW_STATE.json，不写进人类候选文档。prompt目录保存实际Improver输入与每轮Reviewer提示；总控已在调用前保存本消息，你无需重复另写。prepare-review保存Reviewer提示后，只将其正文原样发给全新Reviewer，不向它提供prompt目录。机器输入、状态、结果和解析进入json，不另建资料、代码、缓存或流程笔记。

最终保存json/SLOT_RESULT.json并返回完整对象和重要阻断；最终Idea只在Gate通过后存在，不将失败标成experiment-ready。总控只留唯一实验总结，勿要求为同一结果再写摘要。
