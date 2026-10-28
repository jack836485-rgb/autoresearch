## 背景

**定位关键词：** abstention；retrieval；long-term interactive memory

**一句话定位：** 长期记忆助手如何在未检索到答案时判断是否应继续查找。

## 核心 Claim

无相关context不等于历史没有答案；主张以检索过程的独立覆盖信号决定一次额外检索，而不是凭reader对答案的confidence。

论文把retrieval和reading错误分开；reader无法凭空知道遗漏；用检索覆盖而非答案自信决策；如果覆盖信号不辨别漏检或有信息样本误弃增加则停止。

## 方法设计的核心思想

CPU追踪问题实体是否命中、检索词是否覆盖显式属性和会话时间；若关键实体未命中，原模型在同总预算内改写一次检索，再挤占一次reader调用；信号与答案标签分离，未知仍可弃答。

## 最小实验

LongMemEval k固定与总两次调用上限，对照一次CoN、始终二检索、自置信再检索、覆盖触发；offline分类answer存在/不存在和retrieval成功/失败。若自置信或始终二查等效则无独立创新。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| BM25 + direct reading | long-term interactive memory、retrieval、同一 LongMemEval 问答 | https://arxiv.org/abs/2410.10813 | https://github.com/xiaowu0162/LongMemEval；已读取 retrieval/generation.py 及 run_generation.sh；flat-bm25 分支使用 rank_bm25.BM25Okapi(doc.split(" "))，CPU 可运行，不使用 dense CUDA checkpoint | python src/retrieval/run_retrieval.py --in_file {S_cleaned} --out_dir {dir} --retriever flat-bm25 --granularity session；generation 必须 --retriever_type flat-session（若turn则flat-turn） --topk_context {k} --history_format json --useronly false --cot false --con false，并提供 --in_file/--out_dir/--model_name/--model_alias/--openai_key；不是flat-bm25。环境用CPU版PyTorch | 是；Call14后纠正旧命令，不代表已运行 |
| 相同检索 + Chain-of-Note | long-term memory 的 reading 阶段，避免用换 reader 掩盖检索或整理收益 | https://arxiv.org/html/2410.10813v2#S5.SS5 | 同上 run_generation.py + run_generation.sh；已核验 con/con-separate 映射 | 锁定相同检索列表/reader；官方 con = --cot true --con false（单次输出先提证据），con-separate = --cot true --con true（每项先独立提notes再回答）；最小实验用单次con，同retriever_type flat-session/flat-turn；所有额外token/调用计费 | 是；Call14后纠正旧映射 |
