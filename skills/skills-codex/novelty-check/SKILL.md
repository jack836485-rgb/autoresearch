---
name: "novelty-check"
description: "Verify research idea novelty against recent literature. Use when user says \"\u67e5\u65b0\", \"novelty check\", \"\u6709\u6ca1\u6709\u4eba\u505a\u8fc7\", \"check novelty\", or wants to verify a research idea is novel before implementing."
---

# Novelty Check Skill

Check whether a proposed method/idea has already been done in the literature: **$ARGUMENTS**

## Constants

- REVIEWER_MODEL = `gpt-5.6-sol` — Model used via a secondary Codex agent. Must be an OpenAI model (e.g., `gpt-5.6-sol`, `o3`, `gpt-4o`)
- **REVIEWER_BACKEND = `codex`** — Default: Codex xhigh reviewer. Use `--reviewer: oracle-pro` only when explicitly requested; if Oracle is unavailable, warn and fall back to Codex xhigh.

## Instructions

Given a method description, systematically verify its novelty:

### Phase 0: Prepare the Idea-Stage Output Directory
When the user asks to check the novelty of an idea under a user-provided `idea-stage/<slot>/` directory (the directory containing `FINAL_IDEA.md`):

1. Reuse or create `idea-stage/<slot>/novelty-check/` alongside `FINAL_IDEA.md`.
2. At the start of each novelty-check run, create a child directory named with a timestamp precise to seconds: `idea-stage/<slot>/novelty-check/<YYYYMMDD_HHMMSS>/` (for example, `20260910_143025/`).
3. Save the literature excerpts and the final novelty-check report in that timestamped directory. Use Chinese filenames by default; name the final report `新意查证报告.md`.
4. Do not move search logs, reviewer prompts/raw responses, or review traces into this directory. Continue to handle review traces according to the **Review Tracing** section below.

This directory rule applies only when the user identifies an idea under `idea-stage/<slot>/`; otherwise, keep the existing output behavior.

### Phase A: Extract Key Claims
1. Read the user's method description
2. Identify 3-5 core technical claims that would need to be novel:
   - What is the method?
   - What problem does it solve?
   - What is the mechanism?
   - What makes it different from obvious baselines?

### Phase B: Multi-Source Literature Search
For EACH core claim, search using ALL available sources:

1. **Web Search** (via `WebSearch`):
   - Search arXiv, Google Scholar, Semantic Scholar
   - Use specific technical terms from the claim
   - Try at least 3 different query formulations per claim
   - Include year filters for 2024-2026

2. **Known paper databases**: Check against:
   - ICLR 2025/2026, NeurIPS 2025, ICML 2025/2026
   - Recent arXiv preprints (2025-2026)

3. **Read abstracts**: For each potentially overlapping paper, WebFetch its abstract and related work section

### Phase C: Fresh-Agent Verification (same-family provisional by default)
Call REVIEWER_MODEL via `spawn_agent` (`spawn_agent`) with xhigh reasoning:
```
reasoning_effort: xhigh
```
Prompt should include:
- The proposed method description
- All papers found in Phase B
- Ask: "Is this method novel? What is the closest prior work? What is the delta?"

### Phase D: Novelty Report
Output a structured report:

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Claims
1. [Claim 1] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
2. [Claim 2] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
...

### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
|-------|------|-------|---------|----------------|

### Overall Novelty Assessment
- Score: X/10
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON
- Key differentiator: [what makes this unique, if anything]
- Risk: [what a reviewer would cite as prior work]

### Suggested Positioning
[How to frame the contribution to maximize novelty perception]
```

### Important Rules
- Be BRUTALLY honest — false novelty claims waste months of research time
- "Applying X to Y" is NOT novel unless the application reveals surprising insights
- Check both the method AND the experimental setting for novelty
- If the method is not novel but the FINDING would be, say so explicitly
- Always check the most recent 6 months of arXiv — the field moves fast

## Review Tracing

After each `spawn_agent` or optional `oracle-pro` reviewer call, save the trace following `../shared-references/review-tracing.md`. Write files directly to `.aris/traces/novelty-check/<date>_run<NN>/` and record searched claims, closest papers, reviewer route, raw response, and final novelty decision. Respect the `--- trace:` parameter when present (default: `full`).
