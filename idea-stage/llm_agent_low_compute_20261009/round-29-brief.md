## 背景

**定位关键词：** data wrangling；exploratory data analysis；execution feedback

**一句话定位：** 数据分析agent执行无异常的join/groupby后，怎样发现目标统计单元已经被悄悄重复或改成了另一种加权。

## 核心 Claim

DA-Code报告任务误解与持续错误，并公开dm-csv-010要求先求每月销量总和、再按月取均值的任务和多表orders/order_items数据。待诊断的具体失败是每步Python与join合法，最终却按交易行平均而非按月平均，或把合法一对多join造成的重复实体当成多个统计单元。主张执行反馈需说明目标单元在变换中的权重，而非只有shape/dtype/代码是否跑通；CPU追踪明确单元键和聚合层级，向原actor返回导致加权改变的最小可见例子。

公开任务确实要求多层聚合而baseline有任务误解入口；正常shape和合法join不足以说明一月一票还是一行一票；把实际执行的单元重复次数与归约层级暴露出来；若原actor同预算能修好自然统计权重错误才有价值。

## 方法设计的核心思想

原actor在正常计划中从明确任务文字声明聚合单元键、分组、sum/mean/count层级以及所需总体范围；各组共用同一声明，不给主方法人工正确plan。CPU在Python action内记录支持的read_csv/merge/filter/groupby/aggregate操作的实际关系，使用已有公开实体键或行序号，不用hash。对目标单元保留进入聚合前的重复次数与已经完成的归约层级；只有任务要求一单元一票、而实际mean/count使用行权重或SUM重复了单元级常量时返回反例，允许合法交易级sum和有意一对多。不能自动drop_duplicates，因为那可能删掉真实交易。原actor据证据修改代码；模糊单元或无法跟踪操作为unknown，不能伪造正确聚合。它不解决所有语义错误、不读gold输出。

## 最小实验

DA-Code公开data-wrangling/EDA任务，首版不用ML训练；先诊断自然错误轨迹中的聚合层级/权重错配，再做相同前缀配对恢复。比较DA-Agent、同声明+反思、shape/dtype/row-count profiling、pandas merge validate+indicator、目标单元/聚合层级执行反馈。所有组同actor/数据/任务/步数/历史窗口/输入输出token与总调用预算；CPU算力计时。评价原任务table match和完整成功，另报错权重修复/误报。若目标声明常错、只是多给一个反思轮已等效、merge validate已够或只在人工错误有效则停止。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| DA-Agent on DA-Code DW/EDA | 同数据分析任务、公开真实数据 | https://arxiv.org/abs/2410.07331 | https://github.com/yiyihum/da-code；PromptAgent、run.py parser、PythonController和README已读，Docker CPU+API | python run.py --model {共同actor} --max_steps {cap} --max_memory_length {共同} --max_tokens {共同} --task_config da_code/configs/task/dm.jsonl --source_dir da_code/source --example_index {固定} --output_dir {slot}；实际eval config名eval_all.jsonl而README例子旧名，正式脚本用parser核对值 | 是；源码核验未运行 |
| 同聚合声明+反思 | 排除自然语言任务拆解/额外反馈已足够 | 本地完整标准控制 | 所有方法共用初始目标单元声明；每次代码后同actor依据原输出反思一次，计入总预算 | 同一PromptAgent，不给额外正确plan | 是 |
| shape/type/row count profiling | 一般数据质量检查 | 本地标准对照 | 在支持的变换前后记录shape、dtype、null计数、行数和关联键唯一性；摘要同token cap | 和主方法同CPU采样及反馈机会，不追踪目标单元权重 | 是 |
| pandas validate+indicator | 强现有join基数检查 | https://pandas.pydata.org/docs/reference/api/pandas.merge.html | 实际merge(validate=原actor所声明的1:1/1:m/m:1,indicator=True)并反馈异常/left_only/right_only；原actor选合法m:m时不强报错 | 同声明/表/代码，不训练、无需隐藏checkpoint | 是 |
