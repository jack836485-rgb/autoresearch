---
name: idea-drawback-discovery
description: 一个slot中的完整Idea改进循环，接收相关Problems、drawbacks和可选初始假设，维护候选池并有据演化目标，通过全新独立Reviewer后输出Idea与实验交接。默认只留必要Idea文档，机器记录集中json目录；不运行正式实验。
---

# 研究不足驱动的 Idea 改进执行器

当前 Agent 自己检索、生成、评分、选择、改进和写作；只有独立 Reviewer 可再委托。总控通过 Subagent 调用本 skill，也可按同一接口单独运行。不依赖旧 `idea-improvement-loop`，不修改其他 skill。

## 输入与初始记录

读取 [执行接口](references/执行接口.md)。输入 `slot_path`、相关 `problems`、`drawbacks`、`problem_map_context`、`constraints`、可选 `pre_solution_idea`，`problem_id` 为路由标识。一个 Slot 是完整循环，不固定对应一个问题。

将最初交给执行器的 Problems、drawbacks、假设、硬约束和来源记录在 `RAW_IDEA.md`，初始化后不改写。初始不足不是必须全部覆盖；用户明确硬约束才是。复用 Map 与原文链接，仅补查必要文献。允许有证据地调整 Claim、机制和目标，记录初始／实际不足、新相关不足、变化依据和约束符合性；完全偏题或违反硬约束不合格。

初始假设是普通候选，无来源加分，可修改、否定或放弃。未知参数留待确认；无法建立初始范围返回真实阻断，不猜内容。

## Discovery 与候选

读取 [发现与改进](references/发现与改进.md)，先尝试两个高优先级路线：相似领域成熟机制迁移；最高近邻的 `机制→假设→失效条件→领域不足→新机制`。不能用方法拼接、补模块或补实验冒充独立贡献。只有前两路线均无自评分 **>7** 的合格候选时，进入真实证据支持的未覆盖任务路线。

形成多个实质候选后再轻量查新、总体自评分；查新不限Map年份／机构。独立贡献、可证伪最小实验、同任务baseline复现、目标演化证据与硬约束成立且自评分>7、无阻断者为 `available`。无法复现的最高近邻仍用于创新边界判断。

按 [候选模板](templates/candidate.json) 和 [状态脚本](scripts/slot_state.py) 将完整候选登记到 `json/REVIEW_STATE.json`；自动生成的 `IDEA_CANDIDATES.md` 只供人类阅读。版本有稳定ID及父子关系，旧Claim、评分与Review不覆盖。先选尚未完成预算的Problem，再选择该范围最高分合格者；无合格者时选择最高分待改进候选作探索性审查，真实保留阻断及低分，不伪装为available。同分直接判断并记理由；已覆盖、纯补丁或已有效审过的同一版本不重复送审凑数。

每个候选以ID和标题区分，正文只展示**处理的不足、背景、核心 Claim、方法、最小实验、Storyline**。处理的不足按当前addressed_drawback_ids解析为完整中文描述，初始与新发现的不足都要展开，不让人类另查编号。评分、排名／选择、路线、父候选、证据、基线复现、目标演化及Review历史等完整记录只在json，不在候选Markdown展开。发现依据、未成熟方向和放弃理由用discovery-note追加到状态中的discovery_notes，不另建人类笔记或报告；程序及总控从JSON读取这些信息。

## 独立审查与改进

按 [四节Brief](templates/round-brief.md) 写背景、核心Claim、方法核心思想、最小实验；说明当前目标及变化证据，不泄露候选ID、自评分、排名或历史。各轮保存在Slot根目录 `round-01-brief.md` 等，并同步 `CURRENT_IDEA.md`。

**每个目标Problem至少10个有效Idea/Review循环，完成当前预算前不许停止。** `review_problem_ids`指定目标问题，初始`review_budget`均为10；Brain可在轮次边界追加预算，执行器重新读取状态后完成新预算。联合Slot分别计数，仅候选实际处理的Problem计入该轮。有效独立审查要求真实新Reviewer、零上下文、完整检索/判断及符合初始范围与硬约束；错误、超时、格式失败只记真实调用，不计完成。prepare不计次，start紧邻真实spawn前持久化调用；恢复不清零。每次新 `spawn_agent`、`fork_turns:none`，不复用、不继续。仅传当前Brief、初始范围／drawbacks／硬约束和 [固定rubric](templates/reviewer-prompt.md)；Reviewer独立联网查近邻，不能看到池、排名、历史或未选种子。细节见 [独立审查](references/独立审查.md)。

**Gate：**本轮确为最高分合格候选，有效独立审查score **>7.5**，无fatal blocker；恰好7.5、自评分或肯定措辞不能通过。目标可合理聚焦，不因未覆盖全部初始不足拒绝。

未过时亲读Review原作，新增实质改进并全池重排；没有合格者继续生成或探索性送审，不因低分/近邻多早停。提前通过只保留已通过候选，继续其他实质分支，不能在预算未满时生成最终文档或finish。当前预算将满时向Brain报告候选进展、Review缺口和后续可检验目标，由Brain决定是否加预算；完成全部当前预算后才能选已通过候选或报告未通过。真实工具/输入阻断保存未完成状态和计数，恢复同一历史。原始审查Markdown保存在reviews，每轮一份；实际Improver与Reviewer提示另存prompt，解析及候选对应结果进入json，不再生成终审汇总Markdown。

## 最终写作与产物边界

只在全部目标Problem完成当前预算且候选Gate通过后扩展 [最终Idea](templates/final-idea.md) 和 [实验交接](templates/experiment-handoff.md)，不偷换通过的Claim。说明最初目标、演化、当前预计处理／未覆盖、新不足及验证；未运行结果写假设。实质变更需重新登记和审查，仍受本循环预算。

人类文档仅保留：

```text
<slot>/
├── RAW_IDEA.md
├── IDEA_CANDIDATES.md
├── CURRENT_IDEA.md
├── FINAL IDEA.md           # 仅Gate通过后
├── EXPERIMENT_HANDOFF.md   # 仅Gate通过后
├── round-01-brief.md       # 有几轮留几份
├── PIVOT_OR_STOP.md        # 失败可留
├── reviews/               # 每轮原始审查Markdown
├── prompt/                # 实际Improver输入及每轮Reviewer提示
└── json/                  # 机器输入、状态、结果、prompt与解析
```

prompt内保留 `improve-01-prompt.md` 和 `round-01-review-prompt.md` 等完整实际提示；恢复调用或实质追加指令使用新的improve序号，不覆盖历史。总控保存Improver提示，prepare-review自动保存Reviewer提示；独立使用时按实际收到的任务文本保存Improver提示。不能把模板或事后总结冒充实际输入；历史缺失据实说明。Reviewer仅接收本轮允许文本，不读取prompt目录。

不创建资料目录、临时代码、下载仓库、原文缓存、流程报告或重复摘要。在线读原文／代码核实即可，引用URL和关键证据留在json中的完整候选／最终Idea；缺少可读来源据实标注。此次不执行实验、不生成实验代码。

用finish或stop返回原结果对象，并写 `json/SLOT_RESULT.json`；字段含路由、状态、最佳候选、真实Review评分／verdict、Idea／Handoff路径、blockers及六个目标演化字段。addressed表示声称处理且设计了验证，不代表已解决。失败final／handoff路径null，不存在未通过的最终文档。所有机器JSON均放 `json/`，无需附加人类输出文件。
