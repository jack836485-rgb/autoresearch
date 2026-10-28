# 调度与实际下游协议

创建／恢复前读取当前 `idea-drawback-discovery/SKILL.md`、`references/执行接口.md` 和 `templates/input.json`，优先会话提供的 skill 路径，然后当前已安装目录。依赖缺失先查找，不转用旧 Improver 或把总控变成执行器。无法调用 Subagent 时交付 Group 规划并标调度阻断，不能声称循环已完成。

## 首次创建和输入映射

Group 为本次用户输入／筛选的一组问题，保存在 `idea-stage/<group>/`。Group根目录只留一份 `实验总结.md`，机器记录在json。`group_state.py init` 检查规划、创建新目录并给每个 Slot 写 `json/SLOT_INPUT.json`，填下游实际字段：

```json
{
  "slot_path": "当前slot绝对路径",
  "problem_id": "slot_id，作为本次调用路由标识",
  "review_problem_ids": ["Q002"],
  "minimum_reviews_per_problem": 10,
  "problems": [{"problem_id": "Q002", "problem": "已有问题内容"}],
  "drawbacks": [{"id": "Q002-D01", "description": "初始不足", "problem_ids": ["Q002"], "evidence": []}],
  "pre_solution_idea": null,
  "problem_map_context": {
    "problem_records": [],
    "literature": [],
    "closest_neighbors": [],
    "limitations": [],
    "background": [],
    "source_paths": [],
    "exploration_goal": "开放研究目标",
    "initial_motivation": "初始动机",
    "initial_validation_goal": "初始预期观察",
    "planning_rationale": "共同瓶颈及边界的判断"
  },
  "constraints": {"hard": [], "preferences": []}
}
```

完整证据应填而非照抄空示例；保留成本、版本和来源位置。下游 `init --input <slot>/json/SLOT_INPUT.json` 建立RAW_IDEA和候选状态，父Agent不代跑循环。

## Agent 边界与容量

首次用新 `spawn_agent`，推荐 `fork_turns: none`，通过 [slot-agent-prompt.md](../templates/slot-agent-prompt.md) 传本Slot允许上下文。给定下游skill实际路径，将填好路径、任务和额外约束的完整实际消息，在调用前以UTF-8保存为 `<slot>/prompt/improve-01-prompt.md`，再读取同一正文作为spawn消息。不能只存未填模板、任务摘要或JSON路径。只读相关原地图和自身输入；原文／代码在线阅读，不下载整库、缓存资料或生成临时代码。

恢复、替代Improver或实质追加研究指令分别保存improve-02-prompt.md等新序号，保留之前的文本；容量通知和纯状态问询无需另存。Improver提示序号独立于Reviewer轮次，不计审查预算。孩子的prepare-review将实际Reviewer正文保存为 `prompt/round-NN-review-prompt.md`，Reviewer仅收到本轮正文，不能读取整个prompt目录。历史补记优先从实际调用记录或原JSON恢复，并在json标明恢复来源；找不到的文本不得伪造。

一个 Slot 同时只有一个 Improver；它自行维护 Candidate Pool、三路线、Goal Evolution、Fresh Reviewer、每Problem至少十轮及Brain追加后的预算和 Finalization。父 Agent 不为每个 drawback 另开子 Slot，不代审／改分，也不启动其他 Improver 在同目录竞争。Reviewer 是下游唯一可再委托的 Agent。

并发按实际容量留Reviewer位；可以两个Improver并行准备、Reviewer串行通知，容量许可后才start/spawn，不能用失败调用探测空位。四位容量至少留一空位；若不做容量协调则一次只跑一个Improver。等待完成信号或估计耗时，不反复轮询文件。调度信息放Group/json状态，不另写调度报告。

`group_state.py dispatch --prompt-file ...` 仅记录成功创建后的 Agent ID与已保存的实际提示路径，不实际 spawn，避免隐藏调用与重试。提示必须位于该Slot的prompt目录；不同调用不得复用同一提示文件。实质追加指令的路径和来源在Group/json的dispatch_history对应条目记录，不另写调度报告。工具调用失败用 `execution-failed` 记录 Group 层原因，不构造孩子的结果。正常工作状态变化以完成／失败信号和真实文件为准。

## 恢复与失败

工具中断时若原 Improver 还在运行，先检查实际状态，不能重复 spawn。原 Agent 可恢复时继续同一任务；需要替代时顺序启动一个新的执行器，明确只恢复同 Slot 已有状态、Anchor 与审查预算，记录替代原因及前 Agent ID。不得同时跑两个写同 Slot 的 Agent。

恢复保留初始输入、真实审查与有效轮数，不重开同一方案清零。未完成当前预算不得研究早停；预算将满先向Brain汇报。真实工具阻断保持未完成状态，可恢复同一Slot。缺少结果则等真实状态或记录实际执行失败，父Agent不写伪子结果。

## Brain 追加预算

Brain可自主给有潜力的Loop增加有效审查轮数。依据应指出剩余机制差别、非致命Review缺口、改进进展和下一阶段可检验目标，不按分数接近门槛机械追加。仅在执行器初始化后、无prepared/started调用的轮次边界操作，先协调执行器暂缓状态命令，再执行extend-budget；只更新Group和执行器的review_budget与预算历史，不改初始输入、候选、分数或Review。追加指令保存为新improve-NN-prompt.md并记录实际消息，执行器重新加载状态续跑，不覆盖原提示。

## 收集与只读 Gate 验证

读子目录的 `json/SLOT_RESULT.json`、`json/REVIEW_STATE.json`、候选文档及实际最终文件。接口保留原结果与六个演化字段，并包含review_budget、problem_review_counts、minimum_reviews_per_problem、review_budget_complete、reviewer_calls_used；不额外生成终审报告。

标为可进入排名的结果需：每个目标Problem完成当前预算（初始各10轮，含Brain追加），下游 status/verdict 为 experiment_ready、对应当前 Slot／路由、分数 >7.5、文件存在，且原下游状态中相同 best_candidate_id 有有效 `gate_passed` 调用、无 fatal blocker、分数一致。**这只是读已有 Gate 的完整性，不重新实现候选选择／Reviewer 或修改门槛。**子目录没过 Gate、格式错误、分数错配、路径指向其他 Slot、假最终文件、完全脱离来源均不能由父 Agent升级。

原 `SLOT_RESULT`、候选、分数和来源均保持不变；Group 另记录 `collection_status`／收集阻断，不把 Group 判断写回孩子。没有合法结果的执行失败只出现在 Group 状态及文档。

## 总控状态命令

规划／比较需要落盘时放本次Group的json目录。命令维护Group、唯一总结及首次输入；extend-budget另同步执行器的预算与预算历史，不改候选或审查：

```text
python -X utf8 <skill>/scripts/group_state.py init --plan <规划.json> --idea-root <工作区>/idea-stage
python -X utf8 <skill>/scripts/group_state.py dispatch --group <group绝对路径> --slot-id slot-001 --agent-id <实际spawn返回ID> --prompt-file <slot>/prompt/improve-01-prompt.md
python -X utf8 <skill>/scripts/group_state.py extend-budget --group <group绝对路径> --slot-id slot-001 --rounds 5 --reason "具体潜力证据" --objective "追加轮次要解决的问题" --prompt-file <slot>/prompt/improve-02-prompt.md
python -X utf8 <skill>/scripts/group_state.py collect --group <group绝对路径> --slot-id slot-001
python -X utf8 <skill>/scripts/group_state.py execution-failed --group <group绝对路径> --slot-id slot-002 --reason "实际工具或执行错误"
python -X utf8 <skill>/scripts/group_state.py compare --group <group绝对路径> --comparison <group>/json/比较判断.json
```

新运行每次init创建新Group，重名增序号；恢复直接用旧Group，不再init。状态源为 `json/GROUP_STATE.json`；不生成其他Group人类文档。
