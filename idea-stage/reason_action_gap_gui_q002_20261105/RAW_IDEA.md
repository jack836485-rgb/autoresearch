# 输入问题卡

## 来源
- 地图：`path-stage/GUI_Agent研究地图_20261104/`（`研究地图.md` §Q002、`研究问题.json` 中 `Q002`）
- 检索日期 2026-11-04；近期窗口 2026-05-04 至 2026-11-04
- 机构口径：ai-frontier-search 白名单 + QS 前 50；非白名单关键诊断论文标注为补充证据
- 用户指令：用 `/idea-improvement-loop` 打磨 Q002，Reviewer 预算 15 次（2026-11-05）

## 具体问题
GUI 智能体在推理中已承认之前的动作无效或指令存在冲突，下一步动作仍重复或继续执行；这种推理–动作脱节在 GUI 策略中从何而来（仅成功轨迹 SFT 的动作先验、推理为事后叙述、动作解码对屏幕变化不敏感）？

## 关键证据
| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| Absorbed in Inertia: Activation Analysis for Computer-Use Agents（TU Delft） | https://arxiv.org/abs/2609.37176 | 重复集中于失败轨迹；4 个模型中 3 个有 55–89% 的屏幕–动作重复伴随失败承认；重复段动作前激活持续（吸收区域）；steering 使惯性变化从 −33.8% 到 +44.0%，不稳定 | 分母为检测到的屏幕–动作重复；承认判定依赖 LLM judge |
| Do GUI Agents Know When Not to Act?（ConflictGUI / ConflictGuard，Ant Group、SJTU） | https://arxiv.org/abs/2609.03438 | 两类失败：premise-blind execution 与 awareness-action mismatch（推理提及冲突仍输出可执行动作）；可行任务表现好的 agent 在冲突下倾向盲目执行 | 本轮未取到 mismatch 的定量比例 |
| CUA-Recovery（Univ. of Manchester 等） | https://arxiv.org/abs/2610.27645 | 完全恢复 Pass@3 最高 25.5%（GPT 5.5，d=20）；Claude Opus 4.8 最高 7.7%；开源均 ≤6.4%；恢复训练使 MyPCBench 9.2%→24.5%，Odysseys 24.1%→34.9% | 未区分恢复失败是不知错还是知错不改 |
| Reading Right, Acting Wrong（非白名单） | https://arxiv.org/abs/2610.18579 | 托管 API 的单次打分模型 70–73% 错误发生在事实探针答对之后 | 非 GUI 专属、非白名单补充证据 |

地图正文补充：AndroidFlux（arXiv:2610.34384，机构未核实）80 个人工核验任务上 Qwen3-VL-4B/8B 从首错步恢复平均约 26%。

## 已有解决方法与剩余边界
- 已有解决方法：激活 steering（Absorbed in Inertia 测试，效果不稳；ConflictGuard 条件 steering）；恢复轨迹合成训练（RoTS，arXiv:2605.29447，Alibaba；CUA-Recovery-Train）；教师蒸馏装入停止动作（arXiv:2607.17136，非白名单）。
- 已支持的解释：惯性与动作前激活的持续区域相关（相关性证据，干预不稳定）。
- 尚未解决：推理文本与动作的耦合在 GUI 策略里何处断开、训练侧来源是什么；通用 LLM 中 knowing-doing gap 已有研究（arXiv:2504.16078 Google DeepMind；arXiv:2607.13618），但未针对 GUI 截图–动作循环。

## 待验证解释与分歧
- 待验证解释：仅成功轨迹 SFT 导致动作先验压过推理（地图推断）；推理为事后叙述（待验证）。
- 地图列出的三个竞争解释：① 训练数据只含成功轨迹，动作先验压过推理；② 推理只是事后叙述；③ 动作解码对屏幕变化不敏感。
- 地图训练层线索：arXiv:2607.17136 说明 RL 奖励无法装入策略从不采样的动作（如停止），与解释①相容但未直接检验。

## 可检验切口与查新状态
- 可检验切口：相同屏幕与历史下只改推理中是否承认失败，观察下一动作分布是否改变；比较不同训练来源（仅成功 SFT / 含恢复数据 / RL）的开源 CUA 的条件依赖强度。
- 查新状态：反证检索发现通用 knowing-doing gap 研究，降级为“通用现象已有工作涉及”；GUI 设置的成因未检出直接研究。
- 已知边界：四个开源 CUA、两个基准；承认判定依赖 LLM judge；干预实验需在线环境。

## 问题锚点（Problem Anchor）
- **起点问题**：开源截图驱动 GUI/computer-use 智能体（UI-TARS、GUI-Owl、OpenCUA、EvoCUA 一类）在推理文本中已承认前一动作失败或指令存在冲突后，下一动作仍重复或照常执行；需要定位推理与动作的耦合在哪里断开、断开的训练侧来源是什么，以及能否据此改善恢复、终止与循环失败。
- **初始任务与评测**：屏幕–动作重复（惯性）检测、ConflictGUI 冲突指令终止、CUA-Recovery / AndroidFlux 类错误恢复成功率；在线桌面/移动环境（OSWorld、AndroidWorld 类）或离线轨迹。
- **瓶颈与证据边界**：现象与激活关联已测，成因未定；激活 steering 不稳定；恢复数据训练有效但不解释“知而不改”；通用 knowing-doing gap 已有非 GUI 研究；承认判定依赖 LLM judge。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 80GB / 4×L40 48GB / 8×4090 24GB；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺。在线 Android 模拟器或桌面虚拟机能否在服务器上运行尚待确认，离线轨迹诊断不受此限。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 high + 复核 xhigh）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
