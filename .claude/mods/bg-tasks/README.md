# bg-tasks：后台任务面板

在聊天旁的面板里显示本会话中以后台方式启动的 Bash 任务：状态（运行中 / 已完成 / 失败）、已运行时长，以及命令写入的日志文件的行数和最后一行，每 5 秒刷新。命令 `/bgtasks` 重新打开面板。

## 在新会话里启用

mod 放在会话所在的云端容器里，会话结束就消失，所以每个新会话要装一次：

1. 让 Claude 加载 `plugin-authoring` skill；
2. 让 Claude 把本目录复制到 `/root/.claude/dev-mods/<当前会话ID>/bg-tasks/`；
3. 界面弹出 "Turn on the mods Claude writes in this session?" 时选 Turn them on。

## 限制

- 只记录启用之后启动的后台任务。
- 面板由客户端绘制；不是所有客户端都会画 mod 面板。诊断结果写在 `/tmp/claude-0/bg-tasks-诊断.json`。
