# 离线预检（2026-11-05）

数据：HF `xlangai/ubuntu_osworld_verified_trajs` 中 EvoCUA-8B（`evocua_8b_20260105.zip`）、UI-TARS（`UI-TARS-0717-100step.zip`，Reviewer 指出可能不是公开权重模型）、OpenCUA-7B（`...opencua_7b-cot_l2-action_history-3image-Ubuntu-50steps.zip`）的 traj.jsonl 与按需下载的截图（HTTP 区间读取 zip，未整包下载）。截图"未变"：480×270 灰度、像素差 >12 的比例 <0.2%。

| 检查 | EvoCUA-8B | UI-TARS | OpenCUA-7B |
|---|---|---|---|
| 抽样的"动作与前 3 步内相同"步 | 400 | 300 | 300 |
| 其中决策截图未变 | 155 | 161 | 172 |
| 未变步出现在失败轨迹的比例 | 89% | 95% | 90% |
| 推理复读（与前 6 步某次相似度 >0.9） | 44% | 24% | 13% |
| 非重复步的推理复读基线 | 10.1% | 4.7% | 0.3% |
| 新鲜承认失败（正则粗标） | 19% | 31% | 20% |
| 紧接重复且首次无效：重试使屏幕改变 | 6/230（3%） | — | 5/193（3%） |

OSWorld 不可行任务（26 个）：UI-TARS 失败 23 个，其中 12 个在某步推理中写出不可行却从未输出 FAIL；EvoCUA-8B 成功 22/26；OpenCUA-7B（三次运行共 78 条）失败 72 条，其中 16 条有同类表述。正则粗标，未复核。

AgentNet Ubuntu 5k（OpenCUA 训练数据公开部分）：82,448 步中 3,832 步紧随 `last_step_correct=false` 的步，其中 15 步（0.4%）重复错误动作；45% 轨迹含错误步。

脚本在 `脚本/`，抽样结果在 `结果/`。
