> 使用说明：本模板只用于贡献门槛和可行性审查通过后的 `FINAL_IDEA.md`（以及最终展开后的 `CURRENT_IDEA.md`）。遵循 `references/贡献评判标准.md`，保留审查通过的主贡献与待验证条件。由主执行器直接展开，不调用 improver 子 agent。循环中的 brief 只写“背景 / 核心 Claim / 方法设计的核心思想 / 最小实验”四部分，不套用本模板。

# Improved Idea Template

Write the improved idea in the user's language when clear from the request. Assume the reader knows the broad field but is new to this narrow research direction. The proposal must be readable to a researcher who has not seen the raw brainstorming notes. Do not write a loose bullet dump; make the idea understandable like the introduction and experiment-plan sections of a paper.

The contribution may be a method, an important new phenomenon or perspective, or a coherent combination. Improvements on existing problems are valid; discovery-led work need not add a new fix. Adapt method-oriented section labels to the investigation when appropriate. Do not invent an unsolved problem, inflate a local assertion into a major discovery, or turn planned outcomes into established findings. Explain the importance, novelty, effectiveness, and feasible validation of the same main contribution.

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

**主贡献及其价值：** <成功后新增什么值得知道或使用的东西；说明三项的当前依据与未知部分。有效性依据须区别于未来成功阈值和验证设计，不把计划当结果。>

## 1. Introduction-Style Summary

### 1.1 Task Anchor and Minimal Scope
<State the exact task the paper is anchored on, the smallest focused domain/setting, and what is out of scope. Avoid broad area names without a concrete task.>

### 1.2 How Existing Methods Handle This Task
<Explain the most relevant existing method family or closest competitors. Describe their normal pipeline and assumptions. Name concrete papers/systems/benchmarks when known; mark unknown prior work as needs search. When a paper was supplied as the starting point, place it here as related work, task origin, method inspiration, or one example of a broader limitation; do not organize the proposal as a completion of that paper.>

### 1.3 Bottleneck in Existing Methods
<Identify the real bottleneck targeted by a method, or the important phenomenon and gap in understanding targeted by a discovery. Existing problems need not be unsolved. Claiming a newly discovered shared unsolved problem requires checking prior recognition and fixes. Explain the consequence for the field, not merely that an experiment has not been done.>

### 1.4 Our Improvement
<State what we build, change, train, or investigate. For a method, explain the meaningful improvement over strong baselines and why the mechanism should cause it. For a phenomenon or perspective, explain what new understanding follows and how the investigation distinguishes competing accounts. A diagnostic assertion alone is not automatically the main contribution.>

### 1.5 Experiment Setup at a Glance
<Summarize the planned benchmark(s), dataset(s), verified reproducible baselines, metrics, and success criterion in one compact paragraph. Keep every baseline in the same target domain, task, and evaluation setting.>

### 1.6 Contributions / Novelty
State the main contribution first and add only substantive supporting contributions; no fixed count. Explain what changes if it succeeds. For paper input, each must belong to the new idea rather than filling an omission in the supplied paper. Method, phenomenon, perspective, task, or theory contributions may be used as appropriate; an artifact or extra ablation does not automatically add contribution weight.

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
<State the smallest experiment that demonstrates or falsifies the value of the main contribution. A method must test meaningful improvement on the actual problem, not only an intermediate statistic; a discovery must establish reliable evidence and distinguish important alternatives. Explain why the critical operations can be implemented within the user's resources.>

### 3.2 Dataset / Benchmark
<Name the dataset(s), benchmark(s), task split, environment, or synthetic setup. If uncertain, list the best current candidate and mark what needs checking.>

### 3.3 Baselines
<Use this section as the single baseline source of truth. Follow references/基线复现依据.md. Minimum strong comparisons must match the task and evaluation. Give either verified public code and an entry/configuration, or sufficiently specified primary algorithm/prompt/tool sources and a faithful independent implementation plan, its unresolved choices, and required artifacts. Standard algorithms may be specified directly. Distinguish planned reproduction from completed results and official implementation. If a necessary competitor cannot be reproduced, retain its novelty and Claim implications; do not silently replace it with weaker work. Cross-domain inspiration is not a same-task performance baseline. State how model, data, budget, observation permissions, and evaluation are held equal.>

### 3.4 Metrics
<List the primary metric and secondary metrics. Explain what outcome would count as a meaningful improvement.>

### 3.5 Expected Result and Failure Condition
<State what result would make the main contribution worth pursuing, what would refute it, and what would leave only a low-value diagnostic assertion. Tie continuation to the shared contribution standard, not only statistical significance.>

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
