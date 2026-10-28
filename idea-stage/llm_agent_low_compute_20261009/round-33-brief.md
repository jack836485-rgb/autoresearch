## 背景

**定位关键词：** data wrangling；execution feedback；data provenance

**一句话定位：** 数据分析agent排序或重设索引后复用旧布尔mask时，怎样发现合法标签对齐实际筛选了另一批数据行。

## 核心 Claim

DA-Code报告代码可执行但任务语境误解，RADAR已检查schema/row count/绑定列/显式join，并保留操作与输入表记录；这些证据不直接证明Python布尔mask与目标数据行仍对应。待诊断窄失效：mask在原df计算，df经sort/filter/reset_index后原整数标签被重新使用，旧mask依然合法、长度/类型可一致，却落到另一批行。贡献只限由公开执行构建的行身份对应，诊断mask来源与当前行身份的分离；不发明pandas对齐或一般血缘。

公共pandas语义会按label对齐，实际schema和行数正确不说明mask的业务行身份正确；记录行变换前后对应而非只存表metadata；让actor看到具体错配并重算或重附mask；只有同预算修复自然错误且超过简单重算/强验证才值得做。

## 方法设计的核心思想

首版只支持一个Python action内部read_csv、纯行变换sort_values/drop行/reset_index和由列比较形成的Boolean Series，再用[]/.loc选行；不处理join/groupby或改列值后的谓词时效。CPU为自己读取的表分配顺序行ID（普通元数据，无hash/指纹），跟随上述变换传播对应表；mask保留每个bool的来源行ID。当pandas按标签对齐时，比较实际目标行ID与该bool原来源，返回首个不一致的可见行/谓词例子。默认只给原actor修正提示，不能仅凭标签不同判错；公开源码显式按位置的mask不纳入。纯行重排可按ID重附旧bool作单独消融；如果谓词值被改或行出处未知保持unknown，不自动修。

## 最小实验

DA-Code公开CSV的DW/DM/EDA，排除ML与GPU任务，先独立盲标自然mask复用错误；CPU行绑定机制比较DA-Agent、DS-STAR完整原生验证、同shape/index唯一性反馈、通用总是重算mask强策略、行来源诊断（另测纯行变换重附）。所有组同公开原始文件/任务、同actor和各辅助模型、总token/API/执行预算；同Python操作观察，只改变反馈。RADAR完整代码未在一级论文给出仓库，若无法核验不冒充可运行baseline；将其明确公开的schema/rowcount/列绑定/显式join规则完整实现为本地简单runtime-check控制，不标RADAR原作者分数。评价官方table match/成功与误筛行、误报、无法覆盖及CPU成本；若重算mask已等效、自然错误罕见、来源记录开销更大或主要操作不支持就停止。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| DA-Agent on DA-Code | 同CSV数据分析与表输出 | https://arxiv.org/abs/2410.07331 | https://github.com/yiyihum/da-code；run.py、PromptAgent、PythonController已读 | python run.py --model {共同actor} --task_config da_code/configs/task/dm.jsonl --source_dir da_code/source --max_steps {共同} --max_memory_length {共同} --max_tokens {共同} --example_index {固定} --output_dir {slot}；CPU Docker | 是；未实跑 |
| DS-STAR原生 | 同DA-Code已发表强验证基线 | https://arxiv.org/abs/2509.21825 | https://github.com/google-research/ds-star；run_ds_star.py真实parser、agents/ds_star.py coder/debug/verify/router、tools/llm.py已直接读 | 每公开任务复制instruction到tasks/{id}/question.txt，guidelines.txt提供同格式说明（实际无论是否optional均会读取），source文件到data；python run_ds_star.py --task {id} --llm {共同支持gpt/Gemini快照} --debug_round {cap} --max_round {cap} --max_workers 1；原LLM helper未强制total token，统一补调用边界预算与输出上限/共同采样配置；所有file分析/verify/router计费，不改算法 | 是；源码核验未实跑 |
| 通用mask重算 | 强便宜对照 | 本地标准规范 | 每次sort/filter/reset_index后，用实际支持且保存的原列比较表达式在当前df重算mask；不支持则unknown，不能自动猜predicate | 同采集/表达式与actor，CPU耗时完整记账 | 是 |
| schema/index与runtime checks | 一般可见检查，隔离row identity增量 | pandas规范＋RADAR公开规则，不称复现RADAR | 记录dtype/shape/len、index唯一性，执行SQL时按已见schema验列、要求多行隐式join有显式键；所有规则CPU可直接实现，Python不追加行身份追踪 | 同可见数据、反馈额度与执行预算；RADAR全文无可核验官方代码，不列其原作者算法基线 | 是；标准本地控制 |
