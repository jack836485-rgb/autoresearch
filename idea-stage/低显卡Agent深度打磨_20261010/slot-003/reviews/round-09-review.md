## 结论

实际检索日期：**2026-10-10**。**score：6.0 / 10；verdict：needs_rethink**。

存在 **fatal novelty blocker**：当前接口已经明确任务输入、片段局部变量和允许输出；在普通函数封装获得相同角色信息后，形参、局部作用域、保留函数体常量及显式返回值已覆盖主要能力。Brief 没有指出一个受支持、自然可达且普通函数无法保持的行为，来证明来源绑定展开具有独立机制新意。重命名稳定和避免捕获本身也已有完整卫生宏研究。这个判断针对当前明确接口，不断言所有 Python 片段都能等价封装。[Python 名称绑定规则](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)、[Towards the Essence of Hygiene](https://michaeldadams.org/papers/hygiene/hygiene-2015-popl-authors-copy.pdf)

研究价值仍在：真实经验片段是否产生实例复制或变量覆盖，以及这些错误是否增加总费用，可以形成有意义的经验诊断。当前尚没有发生率证据，因此不能把其价值直接兑换为方法创新或已解决问题。

目标演化成立。它仍研究软件／知识工作 agent 的经验适用性，并从“相关样例被过信”聚焦到可执行代码复用；原研究支持这个聚焦，但不支持 name capture 已经常见。未处理淘汰和反馈混杂不构成拒绝理由。当前设计遵守冻结模型、低本地算力、运行时不读隐藏标签、完整成本核算和仅做研究交接等硬约束。[Agent Skills Can Be Harmful，§IV-C](https://arxiv.org/html/2608.11888v1)

## Claim 判断

| 当前 Claim | 判断 | 最关键依据及可验证性 |
|---|---|---|
| 相同词面任务参数不等于相同绑定角色 | **已覆盖其程序语义核心** | 卫生宏明确区分引入的 binder、reference 与调用侧绑定；词面名称不足以决定绑定关系。这不是新的绑定原理。[Adams 2015，§2、§4](https://michaeldadams.org/papers/hygiene/hygiene-2015-popl-authors-copy.pdf) |
| 区分任务输入、内部绑定与程序常量，防止实例复制 | **部分重合** | AWM 已抽象实例值；CRAFT 已把内部文本输入提升为函数参数；ReGAL 已从程序提取通用 helper，并修正硬编码值。当前尚未给出超出这些抽象的独立角色识别机制。任务替换诊断可以验证结果，但不能单独证明机制新颖。[AWM，§2.3](https://arxiv.org/html/2409.07429)、[CRAFT，§2.1](https://arxiv.org/html/2309.17428)、[ReGAL，§3.2](https://arxiv.org/html/2401.16467) |
| 展开后的局部绑定只影响同片段引用，且对无关变量重命名稳定 | **已覆盖** | 这是 introduced-binder hygiene 与 alpha 等价的既有目标；在当前显式输入／输出接口内，普通函数局部作用域也提供关键隔离。可机械验证，但通过只能证明正确实现既有性质。[卫生性原作](https://michaeldadams.org/papers/hygiene/hygiene-2015-popl-authors-copy.pdf)、[Python 作用域](https://docs.python.org/3/reference/executionmodel.html#resolution-of-names) |
| 因而降低真实任务错误、重试和完整费用 | **部分重合，场景效应待验证** | 原失败研究支持样例过信会造成错误，未证明代码捕获是主要原因。AppWorld 确有持久交互 shell，说明共享变量场景可达，不能据此推断发生率或收益。成功率与完整费用均可证伪。[失败研究](https://arxiv.org/html/2608.11888v1)、[AppWorld environment.py](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/environment.py) |
| 来源绑定展开区别于普通 function／SkillSmith typed operator | **部分重合，独立差别未成立** | SkillSmith 已允许选择和动态实例化部分操作；当前普通函数又获得同样的输入角色和输出范围。Brief 已诚实设置等效即否定的条件，但尚未提出剩余可区分能力。[SkillSmith，§3.1–3.5](https://arxiv.org/html/2605.15215) |

最小实验具备证伪能力：相同角色信息的普通函数是有力对照，且没有人为削弱它；自然发生门槛也避免了仅靠人为冲突制造收益。AppWorld 的 [`react_code_agent.py`](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py) 和 [`environment.py`](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/src/appworld/environment.py) 已核验为模型生成与代码执行入口。核心预算原则可以对齐，具体参数留待确认符合约束。

“AWM式”和“SkillSmith式”目前属于在同任务上的移植对照定义，不能称官方复现。SkillSmith 论文所指 [Aeloon 仓库](https://github.com/AetherHeart-AI/Aeloon) 可访问，但本轮未确认其编译器与运行时入口；这项限制不降低它作为新颖性近邻的权重。

## 最高近邻

1. **[Towards the Essence of Hygiene — Adams，POPL 2015](https://michaeldadams.org/papers/hygiene/hygiene-2015-popl-authors-copy.pdf)**  
   已核验可读原文。§2、§4、§5覆盖引入绑定／引用的捕获、绑定信息和 alpha 等价判据。当前差别是由任务轨迹判断哪些值应该替换；这个语义识别问题没有被卫生宏解决，但 Brief 尚未为它定义新的机制。它是机制近邻，不是 AppWorld 同任务 baseline。

2. **[CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets](https://arxiv.org/html/2309.17428)**  
   已核验原文，2023 预印本／ICLR 2024。§2.1明确泛化具体变量名，把代码内部文本输入改成调用参数，并验证抽象函数能解决原任务。当前差别是 AST 绑定检查及来源分类。其视觉、表格、数学任务成绩不能直接作为 AppWorld baseline；论文给出[官方实现](https://github.com/lifan-yuan/CRAFT)。

3. **[ReGAL: Refactoring Programs to Discover Generalizable Abstractions](https://arxiv.org/html/2401.16467)**  
   已核验原文与[官方仓库](https://github.com/esteng/regal_program_learning)。§3将原程序重构为 helper 和调用程序，执行验证；§3.2及附录明确用参数替换过度具体的硬编码值。当前差别是保持来源绑定，而非通过 LLM 重构与结果验证；函数复用和常量／参数抽象并非新增贡献。其原任务不是 AppWorld。

4. **[SkillSmith: Compiling Agent Skills into Boundary-Guided Runtime Interfaces](https://arxiv.org/html/2605.15215)**  
   已核验原文。§3.1–3.5覆盖离线编译、部分能力接口、输入／输出 contract、typed operators，以及当前任务输入的动态实例化。当前聚焦较窄的 Python 片段绑定，并未被原作明确形式化；但“部分复用”本身不是差别。论文所指仓库可访问，具体复现入口尚未核验。

5. **[Agent Workflow Memory](https://arxiv.org/html/2409.07429)**  
   已核验原文及[官方仓库](https://github.com/zorazrw/agent-workflow-memory)。§2.3、A.1已有细粒度子程序抽取、实例上下文抽象和非固定输入变量化。当前差别是机械绑定保持；原作没有卫生性保证。WebArena／Mind2Web 的原成绩不能冒充当前 AppWorld 对照成绩。

```json
{
  "score": 6.0,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "在已声明的显式任务输入、片段局部绑定和显式输出接口内，获得相同角色信息的普通函数封装已覆盖主要能力；当前未指出来源绑定展开独有的受支持行为。剩余机械性质属于成熟卫生宏机制的迁移，独立机制新意未成立。"
  ],
  "novelty_conclusion": "真实代码经验复用中的实例复制、变量覆盖及完整成本具有经验研究价值，但发生率和收益尚未验证。当前方法由已有实例参数化、函数抽象及卫生绑定机制组成，未建立区别于公平普通函数对照的独立贡献。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Towards the Essence of Hygiene",
      "url": "https://michaeldadams.org/papers/hygiene/hygiene-2015-popl-authors-copy.pdf",
      "overlap": "引入绑定和引用的捕获避免、绑定信息及alpha等价判据。",
      "difference": "不判断LLM任务轨迹中的值是否属于应替换的任务输入；当前尚未给这个识别问题定义独立机制。",
      "verified": true
    },
    {
      "title": "CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets",
      "url": "https://arxiv.org/html/2309.17428",
      "overlap": "把具体代码解抽象成可复用函数，泛化变量名，将内部文本输入改成调用参数并验证。",
      "difference": "当前增加AST绑定检查和来源分类；原作任务不能直接充当AppWorld同任务baseline。",
      "verified": true
    },
    {
      "title": "ReGAL: Refactoring Programs to Discover Generalizable Abstractions",
      "url": "https://arxiv.org/html/2401.16467",
      "overlap": "从程序提取通用helper及调用示例，通过验证、编辑和参数化处理过度具体的硬编码值。",
      "difference": "当前声称保持来源绑定而非通过LLM重构和执行结果验证；独立收益尚未成立。",
      "verified": true
    },
    {
      "title": "SkillSmith: Compiling Agent Skills into Boundary-Guided Runtime Interfaces",
      "url": "https://arxiv.org/html/2605.15215",
      "overlap": "离线编译部分能力、输入输出contract、typed operators及当前任务输入的动态实例化。",
      "difference": "未明确提供Python片段的形式化卫生绑定保证；论文已核验，所指仓库的具体编译运行入口尚未确认。",
      "verified": true
    },
    {
      "title": "Agent Workflow Memory",
      "url": "https://arxiv.org/html/2409.07429",
      "overlap": "从经验提取细粒度子程序，抽象实例上下文并变量化非固定输入。",
      "difference": "没有机械卫生绑定保证；当前AWM式对照是AppWorld移植定义而非原官方复现。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "当前仍研究软件和知识工作agent中的经验适用性。样例过信的原文证据支持聚焦可执行代码复用，但不证明name capture发生率；淘汰和反馈混杂是明确未覆盖部分。冻结模型、低本地算力、无运行时隐藏标签、完整成本计入、核心参数待确认及仅做研究交接均符合约束。"
  }
}
```