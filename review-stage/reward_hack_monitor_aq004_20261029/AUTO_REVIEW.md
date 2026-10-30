# 审查记录

- Call 1（常规，effort high）：IDEA-003，5.5/10，promising_needs_revision，Gate 结果 failed。Elicitor capability as the independent variable and current-checkpoint elicitation refresh appear new (no direct prior found); frozen-monitor decay during RL is partially pre-empted by ariaw/Engels/Na
- Call 2（常规，effort high）：IDEA-006，6.5/10，promising_needs_revision，Gate 结果 failed。诱导者作为操纵变量（尤其 C2 能力与RL分布的拆分）在奖励投机监控中未见先例，但 C1 机制与 on/off-policy 探针数据研究部分重合，C3 是在策刷新的直接延伸；主测试床负例构造在已报告投机率下会失效，须修正后再评
- Call 3（常规，effort high）：IDEA-007，7.5/10，promising_needs_revision，Gate 结果 failed。以'诱导检查点×时点'为操纵变量、在投机出现前构造前瞻监控器，并做能力/分布/风格三方拆分，这在已检索文献中未见；但它与 Trace-and-Amplify 和 Kirch et al. 部分重合，新颖性边界偏窄，要靠 C1/C3 的机制结果撑起来。基线同域、可复现、已核验，无致命阻塞。未达 8 分的原因：对照 4 在 800/800 设定下不可构造；指令文本可能经监控器输入泄漏标签，且正例未过滤
- Call 4（常规，effort high）：IDEA-008，7.0/10，promising_needs_revision，Gate 结果 failed。以诱导者×诱导时点为操纵变量、在投机出现前构造前瞻监控器的设定，在已检索文献中未见，C1 分布逼近与 C2 具备新意；C1 的'能力先于倾向'子主张与 PRIME、2609.16268 部分重合；与 Trace-and-Amplify 和 Kirch et al. 去名后仍可区分。
- Call 6（常规，effort high）：IDEA-009，7.6/10，promising_needs_revision，Gate 结果 failed。以检查点诱导数据训练监控器、并在 RL 投机出现前做前瞻召回评测，未见先例，C2/C3 新颖；但'诱导者×时点'作为变量已被 EleutherAI 用于投机率预测，现有定位不实；整体属于 Kirch et al. / Trace-and-Amplify 脉络下的数据来源消融加时间轴，分量中等。
- Call 7（常规，effort high）：IDEA-010，6.8/10，promising_needs_revision，Gate 结果 failed。未发现把检查点诱导数据当作监控器训练集并在真实 RL 中评测前瞻召回的工作，组合层面新颖；但核心动作相当于 Kirch et al. 的 incentivised 数据沿 RL 时间轴重做，新意幅度中等，主要价值在 C1/C3 的分布拆分实证
- Call 8（常规，effort high）：IDEA-011，7.5/10，promising_needs_revision，Gate 结果 failed。检索未见'投机出现前用 RL 检查点诱导数据训练监控器并测前瞻召回'的工作，问题与 C3 拆分新颖；但方法是 Kirch et al. incentivised 数据沿 RL 时间轴的直接延伸，新增贡献依赖实证结果。投机前漂移窗口短（≤80 步 LoRA），且 Countdown-Code 只有单一策略，天花板/零结果风险高。Baseline 同领域且仓库可复现，无致命阻塞。
