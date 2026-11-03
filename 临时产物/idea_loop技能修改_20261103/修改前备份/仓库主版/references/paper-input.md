# Paper Input Mode (`baseline_paper`)

Read this file only when the user supplies a paper as the starting point.

## Reading and RAW_IDEA.md

Read the actual paper before searching for ideas. Prefer the full primary text; inspect the appendix and official repository when needed to understand the method or experiments. Do not infer the paper from its title, abstract alone, or a secondary summary when the full text is available.

Write `RAW_IDEA.md` with this template. State whether the paper mainly introduces a new task, a new method, or both, but do not use that classification to pick a separate ideation route. Separate the authors' claims and reported results from the improver's interpretation.

```markdown
# 输入论文分析

## 论文信息
<标题、作者、年份、论文链接、官方代码链接或“未找到官方代码”。>

## 核心创新点
<用说人话的方式说明论文提出的是新任务、新方法还是两者都有，以及作者声称的新意。>

## 主要方法
<说明输入是什么、方法实际做了什么、输出是什么；只保留理解后续创新所需的结构。>

## 实验设计与主要结论
<说明数据或 benchmark、主要 baseline、指标、关键对照和论文实际报告的结论；将作者报告与 improver 判断分开。>
```

## Role of the supplied paper

- It is the user-designated highest neighbor for route 2 and the ground-truth starting point, not a candidate. Never register it as `IDEA-001`.
- It enters the minimal experiment only if it matches the new idea's task and evaluation setting and passes the same reproducibility check. Otherwise cite it as task origin, method inspiration, or an example of a broader limitation.
- Broader search during generation serves only to find transferable mechanisms, understand the method family, and locate real task evidence.

## Paper-removal test

For every candidate and every revision, record `与输入论文的关系` and `本 Idea 的独立创新点`. After removing the supplied paper's title and method name, the candidate must still state a standalone research problem, its own Claim or mechanism, and a falsifiable experiment. This is a structural independence check, not a novelty audit.

A candidate whose contribution is “add a missing component”, “complete an omitted experiment”, “extend the paper to one more setting”, or otherwise repair the paper is a `baseline_patch`: record it, never select or review it. A limitation of the paper may motivate an idea only when the improver turns it into a broader problem (routes 2 or 3) with an independently stated contribution.
