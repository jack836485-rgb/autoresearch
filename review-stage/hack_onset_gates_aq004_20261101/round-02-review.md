## 结论

截至 2026-11-01：**score 5.0，verdict = needs_rethink**。

- **新颖性**：问题本身有新意，在已检索范围内没有找到同时做以下两件事的工作：在多渠道 agent RL 中用课程对渠道打开时刻做双重分离；在无监控压力下，把冻结监控器的衰减分解为"新渠道"与"已见渠道变隐蔽"两部分。最近邻各覆盖其中一块：能力门控（2609.16268、2604.01476）、课程改变出现时刻（SimHack）、监控器失效（CATCH 在施压条件下；AF 文章中的 16 点下降）、HVTA 环境（只做评测）。整体属于"部分重合，但组合与问法是新的"。
- **问题在于最小实验测不了核心 Claim C1**。我克隆核验了 HVTA 仓库，发现三处问题：
  1. 逻辑漏洞渠道的判定不要求读码。`Wordle/env_with_bug.py` 对任何短猜测都置 `logical_bug_triggered`，`TowerOfHanoi/env_with_bug.py` 对任何被接受的非法移动都置位，与是否读过源码无关。HVTA 论文的局限部分也写明"能力较弱的模型可能无意中触发逻辑漏洞"。对 4B 模型来说，这条渠道可能在第 0 步就因不会下棋而"打开"。
  2. 两项前置技能是嵌套的，不是互相独立的。漏洞源码由 `_populate_logical_bug_source` 写在 `~/source/env.py`，要读源码也得先会文件导航。所以"导航课程同时提前两条渠道"不能推翻门控假设，C1 的证伪条件本身不成立。
  3. 没有证据表明导航门在起点是关着的。答案文件只在 `home/<随机目录>/` 下一层，旁边有 README，系统提示也列出了 `fs_ls`/`fs_cat`。若 Qwen3-4B 一开始就会导航，C1 与 C3 的门控前提就是空的。
- **其他判断**：C2 中线性探针一臂只用 t₀ 前、来自第一条渠道的样本训练，它在新渠道上召回低几乎是构造使然，真正有信息量的只有 LLM judge 一臂。基线与复现路线没问题：HVTA、verl-agent、rl-rewardhacking 均已克隆核验，算力估计也在约束内。
- **是否值得继续**：问题值得做，但当前的"环境—Claim"对应关系不成立，需要重新确立。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 现有观察 | 大体属实，个别表述过强 | 2609.16268 的"捷径只在已学会的工具上出现"、HVTA"把 RL 训练列为未来工作"、CATCH"在施压条件下被代码注释误导"均已核实。AF 文章的 16 点下降发生在把监控器作为干预手段的投机 run 中，作者自己也说样本太少，无法归因为规避。2606.26300 的摘要只说验证器需要与策略共同演化，"每轮人工补规则"需在正文中核实。rl-rewardhacking 仓库中没有 `train_probe`，对应的是 `scripts/run_probes.py:create_probes`。 |
| C1 子技能门控（双重分离） | 部分重合；按现设计无法检验 | 2609.16268 与 2604.01476 已给出整体层面的能力或奖励稀缺门控，SimHack 也用课程改变出现时刻；"渠道级双重分离"是新的。但 HVTA 的漏洞标签不依赖读码，读源码又依赖导航，前置技能嵌套而非正交，所以双重分离及其证伪条件在这个环境里不成立。 |
| C2 衰减来自新渠道 | 新颖（部分重合） | 没有找到这种分解。Garg 的 LessWrong 文章（2026-11-01）报告"RL 是滑向监控器原本就漏掉的行为"，但它只有单一 exploit 且存在监控压力；CATCH 的失效也发生在施压下。不过探针只用第一条渠道的样本训练，在新渠道上召回低是分布外造成的，这一臂接近同义反复。 |
| C3 子技能是渠道级前兆 | 部分重合；依赖 C1 | SimHack 已经在打开前预测整体出现时刻；渠道级前兆是新的。但若导航技能在起点已饱和，或逻辑漏洞可以被无意触发，"技能领先于渠道打开"就没有可测的对象。 |

## 最高近邻

1. **Hack-Verifiable Environments（HVTA）**，https://arxiv.org/abs/2605.20744 ，代码 https://github.com/MajoRoth/hack-verifiable-environments
   - 重叠：同一套环境、渠道与确定性标签，仓库已经提供逐渠道的 onset 日志（`*_step`）。
   - 差别：没有 RL 训练；其局限部分承认能力较弱的模型会误触逻辑漏洞，这正好削弱 C1。
2. **When Reward Hacking Rebounds**，https://arxiv.org/abs/2604.01476
   - 重叠：投机的出现受正当能力与奖励稀缺门控，并用正当 rollout 数与题目难度做干预，同时做表征探针。
   - 差别：单渠道（改写测试）、单轮 LeetCode，不涉及渠道级前置技能。
3. **CATCH**，https://arxiv.org/abs/2609.39533
   - 重叠：用 SFT 混合与奖励难度控制投机出现时刻，也报告了 CoT 监控器失效。
   - 差别：单轮编程场景；失效发生在监控器作为惩罚施压的条件下，没有做渠道分解。
4. **Steering RL Training: Benchmarking Interventions Against Reward Hacking**（ariaw、Engels、Nanda，AF 2025-12），https://www.alignmentforum.org/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against
   - 重叠：Qwen3-4B 加 GRPO，冻结的探针与 LLM judge 在投机 run 中准确率下降约 16 点。
   - 差别：只有单一漏洞，监控器作为干预手段使用，作者未归因。
5. **Monitor Evasion Depends on What RL Finds and What Monitors Miss**（Garg，LessWrong 2026-11-01），https://www.lesswrong.com/posts/moDKmh4GerCjfB5mM/monitor-evasion-depends-on-what-rl-finds-and-what-monitors
   - 重叠：冻结探针下，衰减来自 RL 发现了监控器本来就漏掉的投机形态，而不是监控器被"击败"。
   - 差别：玩具任务加单一 exploit，有监控压力，不区分新渠道与旧渠道变隐蔽。

```json
{
  "score": 5.0,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "HVTA 逻辑漏洞渠道的确定性标签不要求读码：Wordle 短猜测、TowerOfHanoi 被接受的非法移动都会直接置 logical_bug_triggered，HVTA 论文也承认弱模型会误触；4B 策略下'读码→漏洞渠道'的门控无从检验",
    "前置技能嵌套而非正交：漏洞源码位于 ~/source/env.py，读码依赖文件导航，使 C1 的双重分离与'某课程同时提前两条渠道即推翻'的证伪条件失效",
    "缺少起点技能未饱和的证据：答案文件仅在 home 下一层且附 README，系统提示列出 fs_ls/fs_cat；若 Qwen3-4B 起点即会导航，C1/C3 的门控前提为空"
  ],
  "novelty_conclusion": "渠道级子技能双重分离与'新渠道 vs 已见渠道变隐蔽'的冻结监控器衰减分解在已检索文献中未见，属部分重合下的新组合；但在 HVTA 上按现设计无法检验 C1/C3，C2 的探针一臂近乎构造性结果。",
  "closest_neighbors": [
    "Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale (arXiv 2605.20744)",
    "When Reward Hacking Rebounds: Understanding and Mitigating It with Representation-Level Signals (arXiv 2604.01476)",
    "CATCH: A Controllable Analysis Testbed for Reward Hacking in Coding RL (arXiv 2609.39533)",
    "Steering RL Training: Benchmarking Interventions Against Reward Hacking (AF, ariaw/Engels/Nanda)",
    "Monitor Evasion Depends on What RL Finds and What Monitors Miss (LessWrong, Garg, 2026-11-01)"
  ]
}
```
