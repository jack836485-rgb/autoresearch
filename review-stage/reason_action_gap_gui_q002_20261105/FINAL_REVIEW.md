# 评审小结：GUI_Agent研究地图_20261104 Q002（未通过，用户决定标记拥挤并换卡）

| 调用 | 候选 | 总分 | 重要性 / 新颖度 / 有效性 | verdict | 主要阻断 |
|---|---|---|---|---|---|
| 1 | IDEA-003 失败条件化去似然训练 | 5.0 | 6.0 / 5.5 / 4.5 | promising_needs_revision | 推理时等价于解码屏蔽，而屏蔽与 R³ 都"降重复不提成功"；新意是 2608.23651 开放问题的补完，训练侧与 SEAgent、CPL 重叠；缺 CPL / 训练 vs 屏蔽主对照 |
| 2 | IDEA-006 复读 / 知而不改 / 假换法三分与修法交互 | 6.0 | 6.5 / 6.5 / 5.5 | promising_needs_revision | 三类各自已有近邻（CPL、Say One Thing、CUADebug R5）；部分交互预测由定义推出；缺"去历史不给推理"对照与"按类型路由 vs 最强统一策略"比较；UI-TARS-0717 可能非公开权重 |
| 3 | IDEA-007 同底座 RL 前后检查点（GUI-Owl-7B → Desktop-RL）离线归因 | 4.5 | 6.0 / 7.0 / 4.5 | needs_rethink | 公开 gui-owl-7b 轨迹出自 TRPO RL 运行；GUI-Owl 通用版已含 RL 阶段；第二对无环境；判据过宽 |
| 4 | IDEA-008 同初始化 4 个公开 RL 配方（ARPO、DART-GUI、SEAgent、ZeroGUI）的惯性对照 | 5.0 | 6.0 / 6.5 / 5.5 | needs_rethink | 描述性方向判断、n=4；主指标是重复∧承认的合取；SEAgent 含 SFT 且奖励惩罚冗余；步数配置偏移 |

用户 2026-11-05 晚要求继续打磨，预算由 15 扩至 30，第 3、4 次为重开后的调用。

两次评审均为 opus 子代理（harness 无法设 reasoning effort），fresh zero-context，未复用。

最高近邻：Feedback That Backfires（2608.23651）、Absorbed in Inertia（2609.37176）、Mitigating Conversational Inertia / CPL（2602.03664）、SEAgent（2508.04700）、VeriGUI（2604.05477）、Say One Thing（2510.02204）、CUADebug（2608.02643）、VLAA-GUI（2604.21375）；第 2 次评审后本人检出 StepWise（2604.27151，stuck 触发的小→大模型升级，已追回大部分强模型成功率）。

未通过原因：惯性/循环框架下，机制（表面形式复制、自我模仿、执行落差）、推理时修法（屏蔽、改写、R³、Loop Breaker）、训练修法（负向模仿、CPL、恢复数据）与升级级联都已有近邻；且多项结果显示压低重复本身不提升成功率。剩余可做的切口（升级时交接上下文）预计 6–6.5 分，用户决定不再投入。
