## 背景

**定位关键词：** long-term interactive memory；multi-session reasoning；reading

**一句话定位：** 长期记忆助手如何正确合并已经召回的跨会话证据。

## 核心 Claim

LongMemEval E.5 报告正确检索但错误生成占相当比例。主张不继续提高相似度，而把召回的证据转成回答所需的最小事件连接，减少多个会话中实体/时间混配。

论文直接诊断召回正确仍回答错；关键可能是拼接证据形成答案而非检索；原句索引连接约束生成；在正确召回组没有收益就推翻主要 Claim。

## 方法设计的核心思想

固定同一检索列表，使用同一 reader 在一轮输出中先绑定问题实体、事件与原句索引，再生成答案；不新增模型调用、不读取 has_answer。仅在跨会话问题使用必要连接，原文仍可追溯。

## 最小实验

固定 LongMemEval retrieval cache，比较 direct、CoN、同 token 事件连接；分别报告 recall-correct 与 recall-wrong 组 QA，并盲查是否索引来源支持输出。若只 CoT 格式改变无稳定收益则否定。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| BM25 + direct reading | long-term interactive memory、retrieval、同一 LongMemEval 问答 | https://arxiv.org/abs/2410.10813 | https://github.com/xiaowu0162/LongMemEval；已读取 src/retrieval/run_retrieval.py 与 src/generation/run_generation.py；flat-bm25 分支使用 rank_bm25.BM25Okapi(doc.split(" "))，CPU 可运行，不使用 dense CUDA checkpoint | python src/retrieval/run_retrieval.py --in_file {S_cleaned} --out_dir {dir} --retriever flat-bm25 --granularity session；generation 使用 --retriever_type flat-bm25 --topk_context {k} --history_format json --useronly false --cot false，并提供 --in_file/--out_dir/--model_name/--model_alias/--openai_key；环境依赖需安装 CPU 版本 PyTorch | 是 |
| 相同检索 + Chain-of-Note | long-term memory 的 reading 阶段，避免用换 reader 掩盖检索或整理收益 | https://arxiv.org/html/2410.10813v2#S5.SS5 | 同上 run_generation.py；已读取 --con 选项及 prepare_prompt | 锁定相同检索列表与 reader；仅 --con true；计入额外 CoN token/调用，整体预算统一 | 是 |
