> 使用说明：本模板只用于 novelty gate 通过后的 `FINAL_IDEA.md`（以及最终展开后的 `CURRENT_IDEA.md`）。由主执行器直接展开，不调用 improver 子 agent。循环中的候选保存在 `IDEA_CANDIDATES.md`，`round-N-brief.md` 只写“背景 / 核心 Claim / 方法设计的核心思想 / 最小实验”四部分，不要套用本模板，也不要把完整模板交给 reviewer。

# Improved Idea Template

Write the improved idea in the user's language when clear from the request. Assume the reader knows the broad field but is new to this narrow research direction. The proposal must be readable to a researcher who has not seen the raw brainstorming notes. Do not write a loose bullet dump; make the idea understandable like the introduction and experiment-plan sections of a paper.

Use direct, plain language throughout. Explain what the method concretely does before introducing abstractions or formal notation. Mathematical formulas are welcome when useful, but define every symbol at first use and immediately explain what the formula means in ordinary language. Once a specialized term has been explained in the glossary below, it may be used normally in later sections.

## Terminology and Acronym Glossary

Place this glossary before the title and all proposal sections. Include terms that a reader with general field knowledge may not know:

- terminology and abbreviations specific to the narrow research direction;
- terminology, abbreviations, module names, losses, metrics, or data structures defined by this proposal;
- uncommon benchmark, dataset, system, or method-family names needed to understand the proposal.

Do not pad the glossary with broad-field basics unless this proposal uses them in a nonstandard way. Expand every abbreviation, give a short translation when the user's language differs from the source term, and explain each entry in one plain-language sentence without using unexplained jargon. If the proposal introduces a term, clearly mark it as "defined in this proposal." If there are genuinely no specialized terms, say so explicitly rather than omitting the section.

| Term / acronym | Full name or translation | Plain-language meaning and role in this idea |
|---|---|---|
| <term> | <expanded form / translation; mark proposal-defined terms> | <concrete explanation> |

## Title
<A precise title that names the task/domain and the proposed mechanism.>

**定位关键词：** <List at least three established terms that appear in the cited literature, benchmark, or official task description. Do not coin terms here.>

**一句话背景：** <In one plain-language sentence, state the established field and the exact problem being studied.>

**输入论文及其角色（如适用）：** <Name and link the supplied paper. State whether it is task origin, method inspiration, a related-work example, or an experimental baseline that independently passed the same-task and reproducibility requirements.>

**本 Idea 的独立创新点：** <State the proposal's own novelty in one sentence. For paper input, it must remain a complete research contribution after removing the supplied paper's name and cannot be framed as repairing or completing that paper.>

## 1. Introduction-Style Summary

### 1.1 Task Anchor and Minimal Scope
<State the exact task the paper is anchored on, the smallest focused domain/setting, and what is out of scope. Avoid broad area names without a concrete task.>

### 1.2 How Existing Methods Handle This Task
<Explain the most relevant existing method family or closest competitors. Describe their normal pipeline and assumptions. Name concrete papers/systems/benchmarks when known; mark unknown prior work as needs search. When a paper was supplied as the starting point, place it here as related work, task origin, method inspiration, or one example of a broader limitation; do not organize the proposal as a completion of that paper.>

### 1.3 Bottleneck in Existing Methods
<Identify the specific bottleneck, failure mode, cost, data dependence, evaluation blind spot, or modeling assumption that prevents existing methods from solving the task well. This should be narrow enough that one paper can attack it.>

### 1.4 Our Improvement
<Explain the proposed improvement directly against the bottleneck. Begin with one plain-language sentence saying what we actually build, change, train, or run. Then state what changes relative to existing methods, why that change should help, and what is deliberately kept simple.>

### 1.5 Experiment Setup at a Glance
<Summarize the planned benchmark(s), dataset(s), verified reproducible baselines, metrics, and success criterion in one compact paragraph. Keep every baseline in the same target domain, task, and evaluation setting.>

### 1.6 Contributions / Novelty
List this proposal's concrete contributions. For paper input, every contribution must belong to the new idea rather than filling an omission in the supplied paper:
1. <Contribution 1: method/mechanism>
2. <Contribution 2: empirical finding/evaluation design>
3. <Contribution 3: artifact/analysis/theory if applicable>

## 2. Detailed Method Plan

### 2.1 Method Intuition
<Assume the reader has never seen this method family. Start with the core idea in one plain-language sentence, then explain the end-to-end workflow in 3-6 concrete steps: what goes in, what the method does or changes, and what comes out. Explain why each step helps with the bottleneck. Do not lead with a formula, component name, analogy, or abstract claim. Avoid unnecessary jargon and indirect phrasing.>

### 2.2 Inputs, Outputs, and Assumptions
- Inputs: <data, model states, prompts, trajectories, graphs, features, etc.>
- Outputs: <predictions, policies, rankings, generated artifacts, scores, etc.>
- Assumptions: <what must be true for the method to work>

### 2.3 Algorithm / System Design
<Describe the concrete modules and data flow. For each module, say what it receives, what operation it performs, and what it returns. Include training and inference paths when relevant. If useful, provide pseudocode or a numbered pipeline. When using an equation, define every symbol at first use and follow it immediately with one sentence explaining its operational meaning in plain language.>

### 2.4 Implementation Notes
<State the smallest practical implementation route, dependencies, compute expectations, and any codebase/data requirements.>

## 3. Minimal Validation Experiment

### 3.1 Purpose
<State the smallest experiment that can falsify or support the new idea's independent Claim. Reproducing a missing experiment from the supplied paper is not sufficient.>

### 3.2 Dataset / Benchmark
<Name the dataset(s), benchmark(s), task split, environment, or synthetic setup. If uncertain, list the best current candidate and mark what needs checking.>

### 3.3 Baselines
<Use this existing section as the single source of truth for experimental baselines; do not add a duplicate baseline section elsewhere. List only the minimum baselines needed for the first validation. Every baseline must directly match the positioning keywords, target domain, task, and evaluation setting. A supplied seed paper is not automatically an experimental baseline: include it here only when it satisfies those same requirements. A cross-domain method may be cited as inspiration but cannot be used here as an experimental baseline. For each nontrivial baseline, give the paper URL, a public code repository that the improver has opened and verified as the corresponding implementation, and the exact entry point/configuration/documented command to reproduce it. A simple standard baseline may omit a repository only when it can be implemented locally from a complete specification without unavailable data or checkpoints; explain that route. Exclude any baseline whose implementation or required artifacts cannot be verified. State how core model, data, training/inference budget, and evaluation parameters are held equal across baselines. Prefer a compact table with columns: Baseline, relevance to keywords/task, paper, verified code, reproduction route, controlled core parameters.>

### 3.4 Metrics
<List the primary metric and secondary metrics. Explain what outcome would count as a meaningful improvement.>

### 3.5 Expected Result and Failure Condition
<State what result would justify continuing, and what result would make the idea likely not worth further work.>

## 4. Follow-Up Experiment Plan

Assuming the minimal validation experiment passes, run the following experiments to support the paper claim:

1. Main benchmark comparison: <datasets/benchmarks, baselines, metrics>
2. Ablation study: <which module/design choice to remove or vary>
3. Robustness/generalization: <distribution shift, domains, seeds, model sizes, data scale, or stress tests>
4. Efficiency/cost analysis: <runtime, memory, annotation cost, token cost, sample efficiency, etc.>
5. Qualitative/error analysis: <case studies, failure taxonomy, visualization, or interpretability checks>

## 5. Risks and Open Questions

<List the key novelty, feasibility, data, evaluation, and paper-story risks. For each risk, state how to check it early.>

## References Used

List every paper, report, benchmark, or source actually relied on in this proposal. Do not invent citations. If no external paper was used, write: "No external papers were used in this round; closest prior work remains needs search."

1. <Title> - <authors if known>, <year if known>. <DOI/arXiv/URL if known>.
   - Role in this proposal: <supplied seed paper / closest prior work / experimental baseline / benchmark / method inspiration / limitation example / evaluation source>
   - Confidence: <verified / user-provided / reviewer-invoked / uncertain-needs-search>
