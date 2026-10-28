恢复同一Improver /root/deep_tools，继续本Slot，不新建Loop或重置历史。

使用更新后的 idea-drawback-discovery，重新加载本Slot json/REVIEW_STATE.json 和初始SLOT_INPUT，读取本Slot候选发现段和真实审查检查点。Slot路径：C:/Users/30473/Desktop/研一/autoresearch/idea-stage/低显卡Agent深度打磨_20261010/slot-001。

已真实record第5轮，状态in_progress、active_call=None、reviewer_calls_used=5，Q001=5/10、Q005=5/10，无passing_candidate。原分数6.6、6.8、7.3、7.2、6.2与阻断不改；下一新候选ID008、下一真实Review第6轮。按原实际执行器提示和项目规则继续独立搜索与实质改进；不重复有效审过的版本凑轮数，不因为分数低或近邻覆盖而研究stop。没有合格候选时审最高待改进者，资格与分数如实。

只委托逐轮全新Reviewer。容量当前属于slot-002第6轮；你prepare第6轮后请求总控容量，明确授予前不start/spawn。仍最多两个Improver、一个串行Reviewer，真实结束立即释放通知；正文逐字用prepare生成内容、fork_turns:none、真实bind与完整record。

第8轮有效record后、prepare第9轮前先在active_call=None边界汇报Brain：每Problem真实计数、具体剩余新意、审查的非致命缺口、下一阶段能区分什么假设、追加几轮是否值得。原每Problem10预算不变；Brain依据具体证据决定追加或按原预算继续。所有当前预算完成且真实Gate通过后才写FINAL/Handoff和finish；否则依规则真实结束，预算没满不能研究stop。

原input、RAW、旧Review、分数和通过资格均只读历史；只写本Slot。原AGENTS约束持续有效，checksum只有替代实质更贵操作且改变下一步时可用，完整成本要计。不开正式实验、不写实验代码、不调用户付费模型端点、不发通知。正常上下文压缩可继续；若turn资源确实用尽，再保存干净检查点并返回同Agent续跑标记，不能伪装成研究终态。
