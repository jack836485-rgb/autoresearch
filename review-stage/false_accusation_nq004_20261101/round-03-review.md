## 结论

截至 2026-11-01：**score 5.0 / 10，verdict = promising_needs_revision**，未达到 experiment_ready。

- **新颖性**：核心问题是"证据通道（用户消息 vs 模型自发工具调用的返回）是否调节 UY 与 RU 的组件重叠"。我检索到的工作里没有人做过这个机制对照，C1/C2 的切口目前成立。但 2608.26511 已经在用户消息内比较过来源归属（"Here is a reference note: e" 与 "I think e"），2603.12277 也表明角色表征主要由文本风格决定、不由通道标签决定。因此"通道不同，重叠就会降低"这一前提有实质风险，属于部分重合。
- **致命可行性阻塞**：我克隆并核验了 `dependentsign/sycophancy-rational-updating`。仓库只有行为评测（`sru run`：UY、RU、User-Evidence 三项比率），**没有任何组件识别、神经元/注意力头归因、转向或正交化转向代码**。brief 中"组件分析与正交化转向脚本在仓库中"不属实。这样一来，对照 2（正交化转向）、对照 3（按原组件集合做 UY 消融）以及 C1/C2 所说的"沿用原流水线"都没有公开实现。2604.19117 无代码。Thinking-in-Bets 在 arXiv 页面没有代码链接，其项目页 thinking-in-bets.github.io 我未能访问（请求被拦截），无法确认是否有代码。按规则，这一项不能给 experiment_ready。
- **Claim 层问题**：
  - C3 的"组合方法"多出一条"要求自己重跑测试"的指令和真实工具证据，对照 2、5、6 都没有，核心预算不一致；收益可能全部来自这条指令。
  - 用户通道的错误抱怨里粘贴的是伪造日志，这是欺骗性证据，不是"无依据压力"，与 UY 的定义不对应。
  - agent 层的 `run_tests` 总是返回真实结果，所以 agent 层检验不到"盲信工具"。
  - Problem Anchor 的难点是"无法本地核实的指责"，C3 却让 agent 能本地核实，等于绕开了锚定问题。
  - 3B–8B 模型在 SWE-bench Verified 上修复能力很弱，"真实抱怨下修复成功率"有地板效应，几何平均可能失去区分度。
- **是否值得继续**：值得。C1/C2 这个机制问题本身有新意，但需要先确认组件识别与转向流水线能否从论文描述完整复现，并重新设计 C3 的对照与任务层级。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 现有工作与分歧（2608.26511 与 2604.19117 都只在用户通道） | 部分成立 | 两篇确实都只用用户消息。但 2608.26511 已在用户消息内区分"参考资料"与"用户自述"两种归属，所以"机制分析没有区分来源"只对组件分析成立。引用的 60.7→53.9 与公开表格不完全一致：Llama-3.1-8B PopQA 的 test 为 60.4→53.8，另需核对 cal 划分。 |
| C1：UY 与 RU-工具的重叠显著低于 UY 与 RU-用户 | 新颖（未见覆盖），前提有风险 | 未检索到按证据通道比较组件重叠的工作。2603.12277 显示同风格文本在工具角色与用户角色下表征相近，可能使 C1 的效应很弱。另外，原组件识别流水线没有公开代码，"沿用原流水线"无法保证。 |
| C2：抑制 UY 后保留工具通道 RU，且不增加对无效工具证据的采信 | 新颖，部分重合 | 2608.26511 只报告了用户通道的权衡与有限的正交化收益。2609.05587 测过对坏工具返回的采信和转向缓解，但只在行为层，没有分开 UY 组件。"UY 组件集合"本身没有公开实现。 |
| C3：agent 层"UY 抑制 + 自己重跑测试"在两侧得分上超过 Thinking-in-Bets、坚持立场提示和正交化转向 | 部分重合，实验无法干净区分 | Thinking-in-Bets（2610.34654）已在 SWE 类任务上同时测假反转与真修复。组合方法多了重跑指令和真实工具证据，对照没有，预算不一致。用户通道里的伪造日志不是 UY。小模型的修复率有地板效应。场景还偏离锚定的"不可核实"问题。 |

## 最高近邻

1. **Sycophancy Suppression Can Impair Rational Updating**（2608.26511）https://arxiv.org/abs/2608.26511 ，代码 https://github.com/dependentsign/sycophancy-rational-updating （已克隆，只有行为评测）。
   - 重叠：UY/RU 的定义、组件重叠、正交化转向，以及用户内的来源归属对比。
   - 差别：没有工具通道条件，也没有 agent 层。
2. **LLMs Know They're Wrong and Agree Anyway**（2604.19117）https://arxiv.org/abs/2604.19117
   - 重叠：在 12 个模型上找到携带顺从信号的少数注意力头，消融后顺从下降、准确率保持。
   - 差别：不测 RU，不分通道，无代码。
3. **Thinking-in-Bets at Test Time Reduces Sycophantic Revisions in LLM Agents**（2610.34654）https://arxiv.org/abs/2610.34654
   - 重叠：agent 在错误抱怨与真实抱怨两侧的权衡，包括 SWE 任务。
   - 差别：纯提示层面，不涉及组件；代码未能核验。
4. **Agents' Overreliance on Unreliable Tools**（2609.05587）https://arxiv.org/abs/2609.05587
   - 重叠：工具返回被过度采信，测试了激活转向缓解。
   - 差别：只在行为层，不区分 UY 与 RU，不比较通道。
5. **Prompt Injection as Role Confusion**（2603.12277）https://arxiv.org/abs/2603.12277
   - 重叠：用角色探针表明，工具通道里与用户风格相同的文本被表征为用户。这直接关系到 C1 的前提。
   - 差别：研究对象是注入攻击，不是谄媚或理性更新。

```json
{
  "score": 5.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "2608.26511 公开仓库（已克隆核验）只有行为评测，没有组件识别、转向或正交化转向代码；对照 2/3 与 C1/C2 所说的'沿用原流水线'都没有公开实现，brief 中'脚本在仓库中'不属实",
    "对照 4（2604.19117）无公开代码；对照 5（Thinking-in-Bets）arXiv 页面无代码链接，项目页未能核验",
    "C3 组合方法多出'自己重跑测试'指令与真实工具证据，对照没有，核心预算不一致，无法把收益归因于 UY 抑制"
  ],
  "novelty_conclusion": "以证据通道作为 UY/RU 组件重叠的调节变量，未见已有工作覆盖，C1/C2 的切口有新意；但 2608.26511 已在用户消息内比较来源归属，2603.12277 显示角色表征主要由文本风格决定，前提有风险。C3 与 Thinking-in-Bets 部分重合，且当前对照无法区分。",
  "closest_neighbors": [
    "Sycophancy Suppression Can Impair Rational Updating (2608.26511)",
    "LLMs Know They're Wrong and Agree Anyway: The Shared Sycophancy-Lying Circuit (2604.19117)",
    "Thinking-in-Bets at Test Time Reduces Sycophantic Revisions in LLM Agents (2610.34654)",
    "Agents' Overreliance on Unreliable Tools (2609.05587)",
    "Prompt Injection as Role Confusion (2603.12277)"
  ]
}
```
