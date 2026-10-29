export type FileTail = { path: string; lines: number; last: string; error?: string }
export type BgTask = {
  id: string
  description: string
  command: string
  startedAt: number
  endedAt?: number
  status: string
  files: string[]
  tails: FileTail[]
}

declare module 'claude-code' {
  interface PluginState {
    'bg-tasks': { tasks: Shaped<BgTask[]>; now: Shaped<number> }
  }
}
