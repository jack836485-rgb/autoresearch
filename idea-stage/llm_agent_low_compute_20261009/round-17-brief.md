## 背景

**定位关键词：** long-term interactive memory；temporal reasoning；retrieval

**一句话定位：** 长期记忆助手如何避免错误时间范围导致相关证据被不可逆过滤。

## 核心 Claim

LongMemEval E.4 报告小模型给无时间问题编造时间范围。主张将不可靠时间预测变成可恢复的检索分配，保留一定原始语义候选，改善误筛而不增加 reader 上下文。

小模型误编时间已被论文分析；被忽视关键是错误筛选不可恢复；固定预算保留全局候选形成纠错机会；若误筛很少或简单不筛等效，则放弃。

## 方法设计的核心思想

在同一 CPU BM25 排名中分配固定 k 个位置：有显式日期且可确定范围时按规则筛选；范围无法由文本锚定时不硬删，保留范围内与全局候选并按确定证据去重；reader 的 k 和 token不变。

## 最小实验

LongMemEval 的 temporal 与非 temporal 子集，诊断假时间范围排除 gold evidence（gold仅离线）；同 BM25、reader和 k 比较不筛选、预测硬筛、规则筛、保留全局候选。主指标 evidence recall、QA 与误筛；若收益来自更强 reader 或多看文档则否定。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| BM25 + direct reading | long-term interactive memory、retrieval、同一 LongMemEval 问答 | https://arxiv.org/abs/2410.10813 | https://github.com/xiaowu0162/LongMemEval；已读取 retrieval/generation.py 及 run_generation.sh；flat-bm25 分支使用 rank_bm25.BM25Okapi(doc.split(" "))，CPU 可运行，不使用 dense CUDA checkpoint | python src/retrieval/run_retrieval.py --in_file {S_cleaned} --out_dir {dir} --retriever flat-bm25 --granularity session；generation 必须 --retriever_type flat-session（若turn则flat-turn） --topk_context {k} --history_format json --useronly false --cot false --con false，并提供 --in_file/--out_dir/--model_name/--model_alias/--openai_key；不是flat-bm25。环境用CPU版PyTorch | 是；Call14后纠正旧命令，不代表已运行 |
| 相同检索 + Chain-of-Note | long-term memory 的 reading 阶段，避免用换 reader 掩盖检索或整理收益 | https://arxiv.org/html/2410.10813v2#S5.SS5 | 同上 run_generation.py + run_generation.sh；已核验 con/con-separate 映射 | 锁定相同检索列表/reader；官方 con = --cot true --con false（单次输出先提证据），con-separate = --cot true --con true（每项先独立提notes再回答）；最小实验用单次con，同retriever_type flat-session/flat-turn；所有额外token/调用计费 | 是；Call14后纠正旧映射 |
