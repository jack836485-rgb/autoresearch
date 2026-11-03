# 审查记录

- Call 1（常规，effort high）：IDEA-002，6.5/10，promising_needs_revision，贡献三项 {'importance': 7.0, 'novelty': 7.0, 'effectiveness': 5.5}，可行性 fail，Gate 结果 failed。主贡献是以隔离影子中的同任务阳性对照选择分块或全文重读。若同预算同整轨迹FPR下胜过最强固定策略则值得使用，但当前重要性和新意均未达到8分；已有长上下文漏检及缓解证据尚未连接到对照对另一攻击的预测，更未连接到两条重读路径的条件收益差异。
- Call 2（常规，effort high）：IDEA-005，6.8/10，promising_needs_revision，贡献三项 {'importance': 7.0, 'novelty': 7.0, 'effectiveness': 6.0}，可行性 pass，Gate 结果 failed。若关键结果成立，将新增外部违规阳性探针对监控重读动作收益的诊断用途。长日志漏检及计算选择具有适用的邻近依据，但具体探针能否预测分块与全文的收益差仍未知。相较已有金丝雀和监督动作路由有可辨认增量，目前独立机制与作用范围尚不足以达到两个8分。
- Call 3（常规，effort high）：IDEA-006，7.5/10，promising_needs_revision，贡献三项 {'importance': 8.0, 'novelty': 8.0, 'effectiveness': 6.0}，可行性 pass，Gate 结果 failed。主贡献是通过当前日志内的局部与跨步正负对照，实测读取干预的相对收益并选择原日志读取动作。针对重要的监控计算分配问题，区别于单一canary难度信号、元信息路由和离线合成能力选择；现有监控退化与依赖结构证据支持6分的有效性预期，但程序测试收益向原攻击收益的迁移及额外读取成本回报仍未知。贡献三维达到数值门槛，当前强对照缺口独立阻断主Claim。
