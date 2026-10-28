# 实验交接：IDEA-032

Call24独立7.7/10，experiment_ready，无fatal。完整方案见[FINAL_IDEA.md](FINAL_IDEA.md)。

## 定位与Claim

API tools、pagination、stateful execution。对正在分页的集合，自身成功写可能改变成员/筛选/排序，使旧页边界失效。研究是这类agent自致silent omission的诊断与范围更新，不发明offset、cursor或先枚举后写。

## 首版实现

公开AppWorld ReAct/FullCode、environment.py和pagination.py已读。CPU读agent AST、公开参数/返回、原actor的文档影响说明；同集合成功写触发范围失效，提供已处理ID和剩余范围，由原actor选标准恢复。全部组共用观察记录，controller不读DB/gold/evaluator。未知影响不能当无影响；复杂语法覆盖不足另报。

## 唯一baseline与预算

正式规范见全文§3.3：官方ReAct、FullCode、先收集ID再执行、写后重查当前前缀、本方法。官方ReAct本来有分页提醒，不再设重复“通用提醒”臂。入口appworld run auto --agent-name simplified_react_code_agent --model-name {共同actor} --dataset-name dev，FullCode换agent名。

相同actor/任务/seed/文档/API、LLM调用、完整token和API上限；初始探索、解释、重查、失败、CPU耗时均记录。不能让批量代码的内部API免费。

## 首个诊断及停止

自然bulk任务先检查扫描中删除/改变筛选成员后是否漏项，区分普通未翻页。独立标注，不用controller自身标签作真值。不存在足够自然失败、先收集ID已等效、影响识别低覆盖或重查成循环时停止。人工配对前缀诊断与自然任务分开。

主指标task成功与剩余目标；次指标误重开、漏失效、重复操作、token/调用/CPU。正式模型、金额、样本和seed待用户决定。本轮未跑实验，无GPU训练。
