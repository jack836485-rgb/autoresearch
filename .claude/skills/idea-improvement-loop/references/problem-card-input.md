# Problem Card Input Mode (`problem_card`)

Read this file only when the user points to a path-stage research map (for example one produced by `ai-research-landscape`) or a problem ID in it.

## What to read

A map directory usually contains `研究地图.md`, `研究问题.json`, and `文献笔记/`. Read only:

1. The selected card(s) in `研究问题.json`, all fields. If the user named a map but no problem ID, ask once which card(s) to use.
2. The matching `### Qxxx` section of `研究地图.md`.
3. For each card listed in `与其他问题的关系`, only its `具体问题` line.
4. Lines about the selected card in `文献笔记/反证检索.txt`, if the file exists.

Do not read other notes, scripts, or downloaded material unless a specific candidate needs them. If the map's layout differs, read the equivalent pieces and record what was used.

## RAW_IDEA.md

```markdown
# 输入问题卡

## 来源
<地图路径、问题 ID、地图检索日期与近期窗口、机构口径。>

## 具体问题
<照录卡片的具体问题。>

## 关键证据
| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
<每条证据一行，照录卡片内容，不改写数字。>

## 已有解决方法与剩余边界
<卡片的已有解决方法、已支持的解释、尚未解决。>

## 待验证解释与分歧
<卡片的待验证解释，以及地图正文中的跨论文分歧。>

## 可检验切口与查新状态
<照录卡片；查新状态原样保留。>

## 问题锚点（Problem Anchor）
<记录起点问题的对象、条件、初始任务/评测、瓶颈与证据边界，以及用户资源、时间、非目标约束和进入实验规划的成功条件。起点记录保持稳定；候选可以研究子问题或邻近新问题，其实际对象与转向理由写在 brief 中。不要写候选偏好或自评分数。>
```

## Reuse rules

- **Card evidence is already-read evidence.** Use the card's papers as idea-generation sources at the reading depth the map recorded. Do not search again for papers the card already lists.
- **Read to the depth needed for the decision.** Reuse ordinary background evidence at the card's recorded depth. Open the primary source when the Claim depends on an unverified or omitted detail, a card paper becomes the highest neighbor or a necessary baseline, or a reviewer cites it. Read the method, experiment, appendix or implementation section that determines the assumed flaw, mechanism difference or reproduction route; an abstract alone does not establish those details. Record what was verified without rereading every card paper.
- **The map's coverage is limited.** A map covers a recent window and an institution whitelist. Prior work outside the window or the whitelist is unknown to it, so the lightweight novelty check must search beyond the map. A card whose `查新状态` says no targeted novelty search was done gives no novelty assurance at all.
- **Route inputs.** The card's `已有解决方法` are the highest-neighbor candidates for route 2. Its evidence, `待验证解释`, `尚未解决`, and the map's cross-paper disagreements are the inputs for route 3.
- **The card's `可检验切口` is a seed, not a plan.** Register it as a `问题卡切口` candidate. It is usually a diagnostic experiment without a method, so it typically needs routes 1–3 to become a full idea. It may be revised, narrowed, or abandoned.
- **A diagnostic seed is not automatically a contribution.** Apply `贡献评判标准.md`: an important new phenomenon or perspective can stand without a fix when its value and evidence meet the gate; otherwise use the seed to develop a method or stronger discovery. Merely testing a card's conjecture does not qualify it for finalization.
- **Problem Anchor.** The starting problem comes from `具体问题`, its initial setting from the evidence, and its remaining bottleneck from `尚未解决`; constraints come from the user. A valuable subproblem or adjacent new problem may be retained and selected. State its own contribution and evidence, which original conditions it keeps or changes, and what the original question still needs. Scope change alone is not a reason to reject it.
- **Nothing from the map goes to the reviewer** beyond what the four-part brief needs. The reviewer searches independently.

## Source-card writeback at finalization

When the project requires it, update the selected source card's existing status/notes structure with the run's outcome, idea/review paths and remaining original question; keep any corresponding status in the map text consistent. Record a successful handoff as completed idea development, not an experimentally solved problem. If a subproblem or adjacent new problem was retained, record that relation and its own outcome. Stopping one route does not mean abandoning the entire source question; mark that only when it is actually the decision.
