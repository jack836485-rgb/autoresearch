---
name: idea-drawback-improve-brain
description: 从Problem Map规划多drawback独立研究方向，按One Loop One Slot调用idea-drawback-discovery Subagent；Group只生成一份输入与执行总结，机器记录放json。负责规划和收集，不代跑Improvement或正式实验。
---

# Idea 改进总控（Brain）

一个Slot是一次完整独立Loop，可含多个相关Problem／drawback，也可单个；默认Multi-Drawback First，优先自然协同，不机械拆分、不要求全覆盖。

总控负责读图、筛选、关系判断、开放目标、可选假设、调度和收集；每Slot由一个Subagent使用 `idea-drawback-discovery` 自行完成候选与全新独立Reviewer循环。总控不替孩子改候选、打分或绕Gate。

## 最低轮次与大脑加预算

每个选中的 Problem 至少完成 **10 个有效 Idea → 独立 Review → 改进循环**，小于十轮不许结束研究。一次完成是实质候选或实质改进版本获得全新零上下文Reviewer的有效审查；标题数、自评分、prepare、失败/超时调用和重复审同一版本不计有效轮次。

自然联合的多Problem Slot按当前候选实际处理的初始Problem分别计数；只在初始输入提到或作为背景不计完成。`review_problem_ids`指定本Slot目标问题，`review_budget`保存每个问题当前预算，初始均为10。自评分低、近邻多、暂时无合格候选不是早停理由；继续换机制、查原作并形成实质改进。没有合格者时，对最高分待改进候选作探索性独立审查，保持真实阻断，不重复已覆盖版本凑轮数。

前十轮出现通过候选时保留该分支，继续探索其他实质候选；完成全部目标Problem的当前预算后，再选择已过Gate的候选写最终Idea。Gate仍要求合格候选的独立score>7.5且无fatal blocker。真实输入/工具阻断或用户取消保留未完成状态和真实计数，不算完成研究。

**Brain可以自主给有潜力的Loop增加预算。** 依据具体剩余新意、有效Review中的非致命缺口、实质改进进展和可区分的最小实验直接判断，不建评分表，不因分数接近门槛自动续费。记录增加多少轮、涉及Problem、潜力证据及下一阶段要解决什么；不得降低十轮最低要求、改分或重置历史。执行器在当前预算将满时先向Brain汇报，Brain决定加预算或收集结果。

在执行器初始化后、没有准备中/运行中Review的轮次边界，协调其暂缓下一条状态命令，先保存新序号的实际追加指令，再用 `group_state.py extend-budget --group ... --slot-id ... --rounds 5 --reason "潜力依据" --objective "下一阶段目标" --prompt-file <slot>/prompt/improve-02-prompt.md`；可用 `--problem-ids`只增加部分问题。命令同步Group和执行器预算及历史，不改初始输入、候选或审查；将已保存的指令原样发给执行器续跑。具体轮数按研究判断，不固定每次加5。

## 执行

1. 输入具体 `path-stage` 地图、可选problems和constraints；读取 [Map接口](references/ProblemMap接口.md)，复用有据不足、已有处理、近邻和边界，用户范围优先。
2. 按 [Slot规划](references/Slot规划.md) 判断共同失效假设、因果／结构关系和冲突；自然联合或拆开，同目标不同Loop要有实质区别。共同原因未知时只作为假设。
3. 有证据的共同insight可给简短 `pre_solution_idea`，否则null。探索目标不锁方法，种子可被改进、否定或放弃；真实硬约束保持有效，目标可有据演化。
4. 用 [Group工具](scripts/group_state.py) 创建 `idea-stage/<group>/`，重名增序号。规划和比较可参考 [规划模板](templates/group-plan.json)、[比较模板](templates/group-comparison.json)，这些JSON若落盘都放Group的 `json/`。
5. 按 [Subagent协议](references/Subagent协议.md) 和 [调用模板](templates/slot-agent-prompt.md) 传完整允许上下文；调用前将实际完整提示保存到该Slot的 `prompt/improve-01-prompt.md`，原样作为Subagent消息，调度状态关联该路径。恢复或实质追加指令另存新序号；各轮Reviewer提示由孩子保存到同一prompt目录。只写自身Slot。给Reviewer留容量；可并行准备、串行审查，容量不足时先等空位，不用失败spawn试探。
6. 按 [收集规范](references/汇总与目标演化.md) 只读收集孩子 `json/` 的状态和结果及指定Idea文档，逐Problem核实当前预算、有效轮次及真实Gate／终态；不足预算不能作为完成收集。合理聚焦与新相关问题可接受，偏题／违规要标定位阻断。

## 唯一Group总结

Group根目录只留 `实验总结.md`：概括最初输入各Improver的Problems／drawbacks、探索目标及可选假设、候选数、真实Review调用数、各Problem有效轮次与当前预算、加预算依据、执行状态、目标演化、通过／失败和主要原因。只需简短说明重合或优先级，不复制候选池和全量文献。

```text
idea-stage/<group>/
├── 实验总结.md
├── json/                  # 总控状态、规划及比较等机器记录
├── slot-001/              # 孩子按自身简洁文件约定输出
└── slot-002/
```

不再生成独立manifest、ideas、ranking、流程／调度报告，也不创建资料、下载、临时代码等目录。程序需要的JSON只在相应 `json/`；提示正文只在相应Slot的 `prompt/`。孩子的IDEA_CANDIDATES只展示六项研究内容；完整候选、评分、选择、目标演化和Review历史从json机器记录读取，不从人类视图恢复执行状态。

最后报告唯一总结路径、真实通过／失败和限制。addressed仅表示方案预计处理并设计验证，未做实验不能称解决。只要求修改skill时完成必要验证，不启动真实研究循环。
