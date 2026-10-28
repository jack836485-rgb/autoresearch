---
name: idea-paper-draft
description: "Generate an honest Markdown paper/presentation draft directly from an idea-discovery report, selected idea, refined proposal, or experiment plan. Use when the user says \"根据 idea 写论文初稿\", \"idea to paper draft\", \"写汇报文稿\", \"给不懂的人汇报\", \"从 IDEA_REPORT 生成初稿\", or wants a non-specialist Markdown narrative with figures before running the full /paper-writing pipeline."
---

# Idea Paper Draft

Turn a selected research idea into a readable Markdown draft for human reporting and a bridge artifact for `/paper-writing`.

This skill is for the moment between `/idea-discovery` and full experiments: the user wants to see what the idea would look like as a story, what evidence exists, what figures would explain it, and what is still missing.

## Default Output

Write:

- `paper-draft/IDEA_PITCH_DRAFT_<timestamp>.md`
- `paper-draft/IDEA_PITCH_DRAFT.md`
- `paper-draft/NARRATIVE_REPORT_<timestamp>.md`
- `paper-draft/NARRATIVE_REPORT.md`
- `paper-draft/MANIFEST.md`
- `paper-draft/figures/` for generated or copied figures

The pitch draft is the primary user-facing artifact. The narrative report is a structured handoff to `/paper-writing`.

## Input Resolution

Use the user's explicit file or topic first. If missing, search in this order:

1. `idea-stage/IDEA_CANDIDATES.md`
2. `idea-stage/IDEA_REPORT.md`
3. `refine-logs/FINAL_PROPOSAL.md`
4. `refine-logs/EXPERIMENT_PLAN.md`
5. `refine-logs/REVIEW_SUMMARY.md`
6. `review-stage/AUTO_REVIEW.md`
7. `results/`, `outputs/`, `figures/`, `experiments/`

If the user says "第一个 idea" or "top idea", select the first recommended/surviving idea. If multiple plausible ideas remain and no ranking exists, ask one concise clarification question.

## Evidence Discipline

Never invent experiment results.

Classify every claim and figure as one of:

- `OBSERVED`: backed by an actual result file, log, table, or generated artifact
- `PRELIMINARY`: backed by a small sanity check or pilot with visible evidence
- `PLANNED`: described in an experiment plan but not run
- `DATA_NEEDED`: required for the story but not yet available
- `UNVERIFIED`: literature or result claim mentioned in an upstream report but not independently checked in this run

Use these labels in the text when the distinction matters. If no experiment has run, say "预研方案" or "待跑 benchmark", not "预研结果".

## Draft Shape

Write the pitch draft in Chinese by default unless the user asks otherwise. Target non-specialists: explain jargon once, prefer concrete examples, and keep paragraphs short.

Required sections:

1. `# 标题`
2. `## 一句话结论`
3. `## 这件事为什么值得做`
4. `## 现在别人做到哪了`
5. `## 我们的想法`
6. `## 系统怎么工作`
7. `## Benchmark 怎么设计`
8. `## 预研实验/当前证据`
9. `## 现在还缺什么`
10. `## 汇报时可以怎么讲`

When writing for a presentation, include speaker-ready paragraphs under each section. The user should be able to read them aloud or paste them into slides.

## Figure Policy

The draft must contain figures unless the user explicitly says text-only. A useful draft should usually have 3-5 figures.

Prefer these figure types:

- **Figure 1: Motivation / problem contrast** — why the task matters and what prior setups miss
- **Figure 2: Method pipeline** — input, compiler/planner, controller, monitor, output
- **Figure 3: Benchmark design** — tasks, environments, tolerances, metrics, baselines
- **Figure 4: Preliminary result** — only if actual result data exists
- **Figure 5: Evidence gap / next experiment map** — when results are missing

Rules:

- Every figure must make one message obvious without reading a long caption.
- If a figure is schematic, label it `示意图` or `conceptual`.
- If a result figure lacks data, do not fake it. Replace it with a benchmark design figure or a `DATA_NEEDED` placeholder table.
- Insert figures in Markdown with relative paths, for example `![方法流程](figures/method_pipeline.svg)`.
- For simple diagrams, create lightweight SVG or Mermaid-derived images in `paper-draft/figures/`.
- For data plots, use existing result files when available; otherwise describe the intended plot and mark it `DATA_NEEDED`.

## Workflow

### 1. Gather Context

Read the selected idea report and related refinement/experiment files. Extract:

- problem and target audience
- selected idea name
- closest prior work and difference
- method components
- benchmark plan
- existing evidence
- missing evidence
- risks and next steps

### 2. Build an Evidence Ledger

Before drafting, make a short internal ledger:

```markdown
| Claim | Status | Evidence file | Use in draft |
|---|---|---|---|
| ... | OBSERVED/PRELIMINARY/PLANNED/DATA_NEEDED/UNVERIFIED | path or none | section/figure |
```

Use this ledger to avoid overclaiming.

### 3. Generate Figures

Create or collect figures before finalizing the Markdown. Minimum acceptable set when no experiment results exist:

1. problem contrast diagram
2. method pipeline diagram
3. benchmark design diagram/table

When results exist, include at least one real plot or table and cite the data source in the caption.

### 4. Write the Pitch Draft

Use the user's reporting style when provided. For non-specialist reporting, include:

- selection background
- research status
- what we do differently
- how the system works
- what the current pre-study shows
- what the benchmark will measure
- why the next experiment is decisive

Do not write like a grant or paper abstract unless asked. The tone should be clear, confident, and honest.

### 5. Write the Narrative Report

Write `paper-draft/NARRATIVE_REPORT.md` as the bridge to `/paper-writing`. It should contain:

- working title
- problem statement
- contribution claims with evidence status
- method details
- benchmark and experiment plan
- result summary if real results exist
- figure inventory
- limitations
- `DATA_NEEDED` list

This file may be more technical than the pitch draft, but it must preserve the same evidence labels.

### 6. Self-Check

Before finishing, verify:

- no fake numbers or fake completed experiments
- every "result" sentence has evidence or is explicitly marked preliminary/planned
- every inserted image path exists
- the first figure appears before the reader reaches the method details
- benchmark metrics and baselines are concrete
- `NARRATIVE_REPORT.md` can be used as input to `/paper-writing`

## Output Summary

End with a short report listing:

- pitch draft path
- narrative report path
- generated figure paths
- evidence gaps still blocking a real paper
- suggested next command, usually `/experiment-plan`, `/experiment-bridge`, or `/paper-writing "paper-draft/NARRATIVE_REPORT.md"`
