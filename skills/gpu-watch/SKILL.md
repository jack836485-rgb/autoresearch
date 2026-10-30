---
name: gpu-watch
description: 查看 A100、L40、4090-225、4090-226 服务器的 GPU 占用（ssh + nvidia-smi），或在后台等到某台服务器有满足条件的空卡后自动唤醒当前会话。适用于“看看哪台服务器有卡”“等卡空了叫我”“没卡了等一等”“gpu watch”，以及要跑实验却发现卡被占满的情况。
argument-hint: "[需要几张卡、每卡多少显存、限定哪些服务器]"
allowed-tools: Bash(python *), Read, Edit
---

# GPU 空卡监视

需求：**$ARGUMENTS**

脚本：`C:/Users/30473/Desktop/研一/autoresearch/skills/gpu-watch/gpu_watch.py`（下文记作 `$W`）
配置：同目录 `servers.json`（服务器启用状态、可用卡、排除卡、占卡进程、备注）

脚本从本机并发 ssh 到各服务器跑 nvidia-smi。满足条件时打印状态表和一行 `GPU_READY {"server": ..., "gpus": [...]}`，退出码 0。

## 什么算可用的卡

一张卡同时满足下面各项才算可用：

- 在该服务器的 `gpus` 里（`"all"` 或卡号列表），且不在 `exclude_gpus` 里；服务器 `enabled` 不为 false
- 卡上没有别人的进程（加 `--allow-shared` 后允许共用，只看显存和利用率）
- 空闲显存 ≥ `--min-free-gb`（默认为该卡总显存的 90%）
- 利用率 ≤ `--max-util`（默认 10%）
- 连续 `--stable` 次检查都满足（默认 2 次，间隔 `--interval` 120 秒），以免把别人两次任务之间的空档当成空卡

自己的占卡进程（命令行匹配 `own_placeholder`，且属主是 ssh 用户）占用的显存算作可回收。这类卡被选中时，输出里会提示先停占卡程序。

## 步骤

1. **先看一眼**：`python $W --once`，若只关心部分服务器就加 `--servers A100,4090-226`。退出码 0 说明现在就有卡，直接用 `GPU_READY` 给出的服务器和卡号；退出码 3 说明当前没有。
2. **定条件**：按任务需要设置 `--gpus`（同一台服务器上的卡数）、`--min-free-gb`，必要时加 `--servers`（按偏好排序，几台同时满足时选靠前的那台）。条件要照任务的实际需求定，不要为了早点等到卡而放宽；拿不准时问用户。
3. **等待**：
   - **Claude Code**：用 Bash 的 `run_in_background: true` 运行 `python $W --gpus 2 --min-free-gb 40`。不要轮询，也不要读中途输出。脚本退出时会话会被自动唤醒，这时再读输出。
   - **Codex**：没有后台唤醒，前台运行并加 `--timeout`，取值略小于 shell 工具允许的最长执行时间，例如 `python $W --gpus 2 --min-free-gb 40 --timeout 3000`。退出码 2（`GPU_TIMEOUT`）表示这一轮没等到，用同样的命令再跑一次。
4. **拿到卡后**：尽快在对应服务器用 `CUDA_VISIBLE_DEVICES=<卡号>` 启动任务，避免卡又被别人占走；如有占卡提示，先停占卡程序。启动前先看一下服务器备注（如 L40 禁止 vLLM 多卡）。

默认只在结束时打印一次状态表，节省 token；排查问题时可加 `-v`，每轮打印一行摘要。

## 修改配置

用户说明服务器或卡的可用情况时，修改 `servers.json`：

- “L40 被某项目征用了”：`"enabled": false, "reason": "被 XX 项目征用，到 11 月"`
- “A100 只能用 6、7 号卡”：`"gpus": [6, 7]`（nvidia-smi 的 index，从 0 起）
- “4090-226 的 3 号卡别碰”：`"exclude_gpus": [3]`
- 需要提醒以后的会话的限制，写进 `"note"`，状态表里会显示

只按用户的说明修改。不要为了拿到更多卡，自行启用服务器或放开卡号。新增服务器时，需要先在 `~/.ssh/config` 里配置好、能免密 ssh，再把 Host 名加到 `servers`。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 条件满足，见 `GPU_READY` 行 |
| 2 | `--timeout` 到期仍未满足（`GPU_TIMEOUT`） |
| 3 | `--once` 且当前不满足 |
| 1 | 参数或配置错误，或指定的服务器全部停用 |

单台服务器 ssh 失败不会让脚本退出，状态表里会标“连接失败”，脚本继续等其他服务器。
