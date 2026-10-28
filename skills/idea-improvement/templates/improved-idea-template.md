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

## 1. Introduction-Style Summary

### 1.1 Task Anchor and Minimal Scope
<State the exact task the paper is anchored on, the smallest focused domain/setting, and what is out of scope. Avoid broad area names without a concrete task.>

### 1.2 How Existing Methods Handle This Task
<Explain the most relevant existing method family or closest competitors. Describe their normal pipeline and assumptions. Name concrete papers/systems/benchmarks when known; mark unknown prior work as needs search.>

### 1.3 Bottleneck in Existing Methods
<Identify the specific bottleneck, failure mode, cost, data dependence, evaluation blind spot, or modeling assumption that prevents existing methods from solving the task well. This should be narrow enough that one paper can attack it.>

### 1.4 Our Improvement
<Explain the proposed improvement directly against the bottleneck. Begin with one plain-language sentence saying what we actually build, change, train, or run. Then state what changes relative to existing methods, why that change should help, and what is deliberately kept simple.>

### 1.5 Experiment Setup at a Glance
<Summarize the planned benchmark(s), dataset(s), baselines, metrics, and success criterion in one compact paragraph.>

### 1.6 Contributions / Novelty
List the paper's concrete contributions:
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
<State the smallest experiment that can falsify or support the core idea.>

### 3.2 Dataset / Benchmark
<Name the dataset(s), benchmark(s), task split, environment, or synthetic setup. If uncertain, list the best current candidate and mark what needs checking.>

### 3.3 Baselines
<List the minimum baselines needed for the first validation. Include simple baselines as well as closest-method baselines when known.>

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
   - Role in this proposal: <closest prior work / baseline / benchmark / method inspiration / limitation being addressed / evaluation source>
   - Confidence: <verified / user-provided / reviewer-invoked / uncertain-needs-search>
