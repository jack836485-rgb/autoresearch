---
name: idea-improvement
description: "将用户提供的研究想法直接改进为一份完整、聚焦、可实施的 proposal，并且只输出一个 improved_idea.md 文件。适用于用户说‘改进 idea’、‘打磨想法’、‘把这个想法变成可做实验的方案’或 ‘improve this idea’。"
---

# Idea Improvement

## Purpose

把一个原始研究想法直接整理成一份完整的、面向实验规划的 proposal。整个流程由主执行器完成一次，不启动其他执行单元，不做独立评审，不评分，不设置通过门槛，也不重复迭代。

## Input

接受以下任一种输入：

- 用户在 prompt 中直接给出的原始研究想法；
- 用户提供的想法文件路径；
- 用户明确指定的已有 proposal。

只读取与当前想法明确相关的上下文，不默认复用其他 idea 的结论。先在当前上下文中确定 Problem Anchor：

- bottom-line problem：要解决的具体技术问题；
- target domain / benchmark / setting：最小任务和应用设置；
- must-solve bottleneck：现有方法的关键瓶颈；
- constraints：算力、数据、时间、代码库、投稿场景和 non-goals；
- success condition：什么证据足以开始实验。

想法过于模糊时最多提出一个简短澄清问题；否则明确必要假设后继续。

## Template

唯一模板是：

`/data/raid5/wangchenyang/Auto-claude-code-research-in-sleep/skills/skills-codex/idea-improvement/templates/improved-idea-template.md`

完整读取该模板，并逐节填写。模板中的章节、术语表位置和 `## References Used` 结尾不可省略、改名或重排。

## Direct Improvement

直接根据原始想法、Problem Anchor 和模板生成 proposal：

1. 保持问题边界和约束；如果某个假设不成立，明确写出原因。
2. 聚焦一个主贡献和支撑它的最小机制，不靠堆叠模块扩大 idea。
3. 在标题前提供术语/缩写表，假设读者熟悉大领域但不了解该窄方向。
4. 先解释具体的输入、动作和输出流程，再引入抽象概念或公式。
5. 首次出现公式时定义每个符号，并紧接着解释公式的实际含义。
6. 不编造引用、实验结果或新颖性结论；未知的现有工作标记为 `needs search`。
7. 使用中文写作，引用、方法名、数据集名和 benchmark 名保留标准英文名称，除非用户明确要求其他语言。
8. 不写 review、score、verdict、评审意见或后续多轮改进方案。

## Output

只生成一个文件：

`idea-stage/<slug>/improved_idea.md`

其中 `<slug>` 从想法标题或 prompt 短语生成，只使用小写字母、数字和下划线；不添加时间戳或随机后缀。若用户指定了输出目录，则在该目录下写入同名 `improved_idea.md`。

文件内容必须完整遵循模板，至少满足：

- 术语/缩写表位于标题之前；
- 任务、瓶颈、改进机制和最小验证实验具体明确；
- 方法先给出输入到动作到输出的流程；
- 所有公式符号在首次使用时定义并解释；
- 末尾为 `## References Used`，列出实际使用的来源，未使用外部来源时明确说明。

写入前在内存中完成一次完整性检查并修正明显遗漏。不要为了记录过程生成任何其他文件，包括原始输入副本、状态文件、演化摘要、评审文件、最终副本、实验交接文件、日志或 trace。

## Mathematical Formatting

Markdown 数学符号使用通用渲染器支持的 LaTeX 分隔符：行内公式使用 `$...$`，独立公式使用 `$$...$$`。首次出现公式时定义所有符号，并用普通语言解释其在方法中的作用。

## Final Response

完成后只向用户报告 `improved_idea.md` 的实际路径和一句话状态说明，不粘贴完整 proposal，不额外生成摘要文件或交接文件。不要在此 skill 中启动实验；生成的唯一文件是供后续 `/experiment-plan` 使用的 proposal。
