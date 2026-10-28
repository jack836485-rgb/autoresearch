# Mini Experiment 项目与证据契约

初始化、恢复或评审实验前必须先读本契约。

## 1. 文件为什么这样分

实验目录只有一份面向人的入口：`PROJECT.md`。它负责用人话说明项目目标、架构、真实
文件映射、运行时序、命令、证据边界和下一步。机器事实各自只有一个权威来源：

| 事实 | 唯一来源 |
|---|---|
| 冻结范围、架构接口、资源版本、命令、科学门槛 | `EXPERIMENT_CONTRACT.yaml` |
| 当前阶段、资源缺口、active job、选中的 run/review | `EXPERIMENT_STATE.json` |
| 原子需求及其实现和证据映射 | `REQUIREMENTS.jsonl` |
| 每次终态运行的命令、范围、产物和哈希 | `runs/RUNS.jsonl` |
| 给人看的架构、复现入口、证据摘要与下一步 | `PROJECT.md` |
| 独立评审结论 | `reviews/round-NNN/REVIEW.{md,json}` |

不要再生成 `RESOURCE_REPORT.md`、`REQUIREMENTS.md`、`IMPLEMENTATION_PLAN.md`、
`RESULTS.md` 或 `HANDOFF.md`。它们过去只是重复上述事实，容易互相矛盾。恢复旧实验时
应保留已有文件，不要擅自删除；把仍有用的信息迁入当前权威文件后，旧文件不再参与校验
或交接。

标准布局如下：

```text
experiments/<slot>/
  PROJECT.md
  EXPERIMENT_CONTRACT.yaml
  EXPERIMENT_STATE.json
  REQUIREMENTS.jsonl
  configs/                         # 新实现推荐；现成框架可用等价目录
  src/                             # 数据、方法、评测和编排的真实实现
  tests/
  schemas/
    CONTENT_MANIFEST.example.json
    REQUIREMENT_RECORD.example.json
    RUN_RECORD.example.json
    GATE_REPORT.example.json
  runs/
    RUNS.jsonl
    <run-id>/
      stdout.log
      stderr.log
      raw/
      metrics.json
  reviews/
    round-NNN/
      REVIEW.md
      REVIEW.json
```

执行者是实现文件、契约、状态、需求、运行证据和 `PROJECT.md` 的唯一写入者。Reviewer
只能写自己的 `reviews/round-NNN/`。外部数据、权重和框架只能作为只读输入；缓存和输出
必须指向实验目录内部。

## 2. Mini Experiment 确定的长期架构

项目从第一版就固定六个职责边界：

1. **契约与配置**：定义范围、版本、seed、smoke/full 差异、命令和门槛。
2. **数据**：只负责生成、加载、切分和规范化，不偷偷做评分。
3. **方法**：通过公共协议接收数据并产生原始预测、轨迹或 checkpoint。
4. **评测**：独立消费原始输出，执行资格过滤、指标计算、聚合和 gate 判断。
5. **运行编排**：串起预检、数据、方法、评测、失败处理和状态更新。
6. **证据**：保存日志、raw、metrics、manifest 和 append-only run receipt。

在 `EXPERIMENT_CONTRACT.yaml.architecture` 冻结组件、公共接口和入口，在 `PROJECT.md`
把这些职责映射到真实 `.py::函数或类`。工程流程图的箭头必须对应真实调用或数据传递，
不能只画“数据层/方法层/评测层”这种概念盒子。若接入成熟框架，保留其原生目录，但仍要
逐文件说明等价映射。
后续增量默认只能扩展数据适配器、方法、指标、配置和测试；不得复制 runner 或 scorer
形成旁路。smoke 与 full 必须走相同的算法、评测器和证据路径，只允许缩减规模。

## 3. 需求可追溯性

每条原子需求必须形成以下链路：

```text
claim -> observable contrast -> implementation -> test/oracle -> metric -> threshold -> failure action
```

`REQUIREMENTS.jsonl` 每行恰好一个对象，是唯一需求真相。必需字段包括：

- 稳定 ID 与强度 `MUST`、`SHOULD` 或 `MAY`；
- idea 文件、章节/行号和源文本哈希；
- 规范化需求、claim ID、实现路径和符号；
- 验证命令、oracle、metric/gate、阈值及阈值口径；
- 状态 `unmapped`、`implemented`、`verified`、`blocked` 或 `deferred`；
- 证据路径、失败动作和未解决原因。

`source.text_sha256` 是对应 idea 行按 `\n` 拼接且末尾无换行的 UTF-8 SHA-256。
`EXPERIMENT_STATE.json.requirements` 的计数必须由 JSONL 推导，不能手填。`PROJECT.md`
可以按组件概括需求，但不要抄出另一张逐行需求表。

不得默默替用户决定会改变科学结论的欠规格选择。普通工程选择可以采用最小惯例做法，但
必须写入契约；会改变 claim 或 pass/fail 解释的选择进入 `unresolved_decisions` 和状态的
`pending_actions`。

## 4. 资源和环境

框架候选及取舍写入 `workspace.framework_candidates`，最终框架的来源、revision、license
写入 `workspace`。环境、数据、权重、只读路径和预检命令写入 `resources`。需要用户补齐
的事项写入 `EXPERIMENT_STATE.json.resource_gate.missing` 与 `pending_actions`；
`PROJECT.md` 只给出人能执行的摘要和检查命令。

永远不要保存凭据值，只记录环境变量名。命令、日志、raw、metrics、manifest、项目说明
和 review 中出现的值都必须替换成环境变量引用或 `<REDACTED>`。

## 5. 运行证据

`runs/RUNS.jsonl` 只追加不改写。失败后重跑要使用新 run ID，不能把失败记录改成成功。
每条记录至少包含：

```text
schema_version, run_id, purpose, status
command_argv, cwd, started_at, ended_at, exit_code
environment, provenance, config, seeds, scope
stdout_path, stderr_path, raw_artifacts, metrics_path
artifact_hashes, requirement_ids, claim_ids, limitations, redactions
```

`purpose` 只能是 `test`、`smoke`、`full`、`analysis` 或 `dry_run`；终态只能是
`passed`、`failed`、`cancelled` 或 `unknown`。正在运行的本地进程或远程任务只记录在
`EXPERIMENT_STATE.json.active_jobs`，结束后再向 JSONL 追加一条终态记录。

每个 passed run 都要对 stdout、stderr、raw 和 metrics 建立完整 SHA-256 映射，并记录
覆盖实际实现/配置输入的排序 content manifest 及其摘要。长任务还要记录 backend、job ID、
预计成本、持久输出路径、清理责任人和状态检查方式。

原始输出不可变，指标必须由代码派生。每个数字要能回到 run、raw 和 metrics，并说明单位、
分母、聚合、随机性和不确定性。mock 只能证明测试行为，dry run 只能证明入口和配置有效，
smoke 只能说明缩减范围内的真实观察。

## 6. `PROJECT.md` 的交接职责

`PROJECT.md` 是导航，不是第二份证据。它必须持续维护以下内容：

- 当前目标、状态、已验证事实和不能下的结论；
- 六个架构职责及其真实路径、公共接口和目录所有权；
- 精确到真实 `.py::symbol` 的 Mermaid 工程架构图和一次运行的 Mermaid 时序图；
- 精确环境、资源、测试、canonical smoke 和 full 命令；
- run ID、raw/metrics 路径、科学 gate、限制和未执行工作；
- 后续增量规则、最短下一步和 reviewer 优先入口。

每轮实现或修复后只更新变化的部分。架构边界没有变化时，不重写整篇；发生架构变更时，
同时更新契约、图、真实文件映射和相关测试。Reviewer 仍须直接检查代码和机器证据，不能把
`PROJECT.md` 的陈述当成证明。

## 7. 状态和评审门槛

状态值：

```text
in_progress | awaiting_resources | blocked | passed
```

阶段值：

```text
initialized | discovering | awaiting_resources | planning | implementing
testing | reviewing | fixing | passed | blocked
```

资源门状态只能是 `unknown`、`awaiting`、`satisfied` 或 `blocked`。进入 scored review 前
必须是 `satisfied` 且 missing 为空。每次阶段变化、长任务开始前和结束后都要原子更新状态。

最终通过条件固定为：

```text
score > 8.0
AND mode == "postrun"
AND verdict == "pass"
AND blocking_findings == []
AND all MUST requirements are verified
AND evidence integrity passes
AND required tests pass
AND canonical smoke passes
```

`acceptance.required_test_commands` 必须是非空且唯一的 argv 列表；canonical smoke receipt
必须与 `acceptance.smoke_command` 完全一致。8.0 分不算通过。
