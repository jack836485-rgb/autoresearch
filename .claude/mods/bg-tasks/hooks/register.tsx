import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { BgTask, FileTail } from '../types'

const PANE = 'bg-tasks'
const TITLE = '后台任务'
const TICK_MS = 5000
const DIAG = '/tmp/claude-0/bg-tasks-诊断.json'

// 字段变了就改 shape 标签，旧版本存下的值会被丢弃
const tasks = atom({ plugin: 'bg-tasks', key: 'tasks' } as const, [] as BgTask[], { shape: 'tasks-1' })
const now = atom({ plugin: 'bg-tasks', key: 'now' } as const, 0, { shape: 'now-1' })

// 从命令里找出写入的日志文件：`> 文件`、`>> 文件`、`tee 文件`，跳过 /dev/null 与 2>&1
function redirectTargets(command: string): string[] {
  const out: string[] = []
  const re = /(?:^|[^0-9&>])>>?\s*("[^"]+"|'[^']+'|[^\s;&|()]+)|\btee\s+(?:-a\s+)?("[^"]+"|'[^']+'|[^\s;&|()]+)/g
  let m: RegExpExecArray | null
  while ((m = re.exec(command))) {
    const raw = (m[1] ?? m[2] ?? '').replace(/^["']|["']$/g, '')
    if (!raw || raw === '/dev/null' || raw.startsWith('&')) continue
    out.push(raw)
  }
  return out
}

// 命令以 `cd 目录 &&` 开头时，把相对路径接到该目录下
function resolveFrom(command: string, cwd: string | undefined, p: string): string {
  if (p.startsWith('/')) return p
  const cd = /^\s*cd\s+("[^"]+"|'[^']+'|[^\s;&|]+)\s*&&/.exec(command)
  let base = cd?.[1] ? cd[1].replace(/^["']|["']$/g, '') : cwd
  if (base && !base.startsWith('/') && cwd) base = `${cwd}/${base}`
  return base ? `${base}/${p}` : p
}

function fmtElapsed(ms: number): string {
  const s = Math.max(0, Math.floor(ms / 1000))
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  return h > 0 ? `${h}时${m}分` : m > 0 ? `${m}分${sec}秒` : `${sec}秒`
}

function shortName(p: string): string {
  const parts = p.split('/')
  return parts.slice(-2).join('/')
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'bgtasks', description: '打开后台任务面板' })
    const opened = await $.ui.open({ id: PANE, title: TITLE })
    try {
      await $.fs.write(DIAG, JSON.stringify({ at: new Date().toISOString(), opened, panes: await $.ui.panes() }, null, 1))
    } catch {}

    const tick = async () => {
      const list = await read($, tasks)
      const running = list.filter(t => t.status === 'running')
      const fresh = new Map<string, FileTail[]>()
      for (const t of running) {
        const tails: FileTail[] = []
        for (const path of t.files) {
          try {
            const text = await $.fs.read(path)
            const lines = text.split('\n').filter(l => l.trim() !== '')
            const last = (lines[lines.length - 1] ?? '').replace(/\s+/g, ' ').slice(0, 160)
            tails.push({ path, lines: lines.length, last })
          } catch {
            tails.push({ path, lines: 0, last: '', error: '暂无内容或无法读取' })
          }
        }
        fresh.set(t.id, tails)
      }
      if (fresh.size > 0) {
        await update($, tasks, l => l.map(t => (fresh.has(t.id) ? { ...t, tails: fresh.get(t.id)! } : t)))
      }
      await update($, now, () => Date.now())
    }
    void tick()
    $.clock.every(TICK_MS, () => void tick())

    return next(e)
  })

  on('command.run', { command: 'bgtasks' }, async $ => {
    await $.ui.open({ id: PANE, title: TITLE })
    return { text: '后台任务面板已打开。' }
  })

  // 记录每个以后台方式启动的 Bash 命令
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const ran = await next(e)
    if (!e.run_in_background) return ran
    const res = 'result' in ran ? (ran.result as { backgroundTaskId?: string; stdout?: string } | undefined) : undefined
    const id = res?.backgroundTaskId
    if (!id) return ran

    const command = e.command ?? ''
    const cwd = (e as unknown as { cwd?: string }).cwd
    const files: string[] = []
    const outMatch = /Output is being written to:\s*(\S+?)\.?(?:\s|$)/.exec(res?.stdout ?? '')
    if (outMatch?.[1]) files.push(outMatch[1])
    for (const p of redirectTargets(command)) {
      const abs = resolveFrom(command, cwd, p)
      if (!files.includes(abs)) files.push(abs)
    }
    const task: BgTask = {
      id,
      description: e.description ?? command.slice(0, 80),
      command: command.slice(0, 300),
      startedAt: Date.now(),
      status: 'running',
      files,
      tails: [],
    }
    await update($, tasks, l => [...l.filter(t => t.id !== id), task].slice(-30))
    return ran
  })

  // 后台任务结束时，引擎以 task-notification 的来源提交通知
  on('prompt.submit', async ($, e, next) => {
    if (e.origin?.kind === 'task-notification') {
      const done = new Map<string, string>()
      const re = /<task-id>([^<]+)<\/task-id>[\s\S]*?<status>([^<]+)<\/status>/g
      let m: RegExpExecArray | null
      while ((m = re.exec(e.text))) if (m[1] && m[2]) done.set(m[1].trim(), m[2].trim())
      if (done.size > 0) {
        const t = Date.now()
        await update($, tasks, l =>
          l.map(x => (done.has(x.id) ? { ...x, status: done.get(x.id)!, endedAt: x.endedAt ?? t } : x)),
        )
      }
    }
    return next(e)
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const list = await read($, tasks)
    const t = (await read($, now)) || Date.now()
    const ordered = [...list].sort((a, b) => {
      if ((a.status === 'running') !== (b.status === 'running')) return a.status === 'running' ? -1 : 1
      return b.startedAt - a.startedAt
    })
    const color = (s: string) => (s === 'running' ? 'yellow' : s === 'completed' ? 'green' : 'red')
    const label = (s: string) =>
      s === 'running' ? '运行中' : s === 'completed' ? '已完成' : s === 'failed' ? '失败' : s === 'killed' ? '已停止' : s

    return (
      <Box flexDirection="column">
        {ordered.length === 0 && <Text dimColor>本会话还没有后台任务。</Text>}
        {ordered.map(task => (
          <Box flexDirection="column" marginBottom={1}>
            <Text>
              <Text color={color(task.status)} bold>
                {label(task.status)}
              </Text>{' '}
              {task.description}
            </Text>
            <Text dimColor>
              {task.id} · {fmtElapsed((task.endedAt ?? t) - task.startedAt)}
              {task.status === 'running' ? '' : '（用时）'}
            </Text>
            {task.tails.map(f => (
              <Text dimColor wrap="truncate-end">
                {shortName(f.path)}：{f.error ?? `${f.lines} 行 · ${f.last || '（空）'}`}
              </Text>
            ))}
          </Box>
        ))}
      </Box>
    )
  })
}
