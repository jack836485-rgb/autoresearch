# 最终评审：N-Q004（用户决定换卡）

- 状态：`rejected_no_viable_candidate`（20 次额度用 3 次；剩余额度转给 A-Q002）

| 调用 | 候选 | 分数 | 主要阻塞 |
|---|---|---|---|
| 1 | IDEA-004 措辞 vs 证据来源因子诊断 | 5.5 | EO 在 8B 模型上稀少；效应大小比较不能识别成因；真 / 假两侧不对称 |
| 2 | IDEA-005 对称两轮协议 + 核实 SFT | 5.5 | Thinking-in-Bets、Correction or Manipulation? 已覆盖行为层两侧评测 |
| 3 | IDEA-006 证据通道调节组件重叠 | 5.0 | 2608.26511 仓库无组件 / 转向代码（improver 误写）；C3 预算不一致、偏离锚点；Role Confusion 前提风险 |

最高近邻：CAVE-Bench (https://arxiv.org/abs/2609.32616)、Thinking-in-Bets (https://arxiv.org/abs/2610.34654)、Correction or Manipulation? (https://arxiv.org/abs/2610.36453)、2608.26511、2604.19117、Prompt Injection as Role Confusion (https://arxiv.org/abs/2603.12277)。
