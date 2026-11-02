## 结论

评审日期 2026-11-01。**score 5.0 / 10，verdict：promising_needs_revision。** 值得继续，但目前的新颖性边界没有立住。

- **部分新颖。** "在 RL 过程内按检查点注入已验证的投机样本，再按投机类型分层，判断延迟由哪道门槛决定"这一干预设计，检索中没有找到完全相同的工作。
- **前提站不住。** "没有人用干预把这些解释分开"与"EleutherAI 明确写到各解释未被分别检验"两句不成立：
  - EleutherAI 博文（2025-10-07）只用 "We suspect / We speculate" 推测 propensity，没有提出发现、能力、激励三分法，也没有说这些解释未被检验。
  - SimHack（2610.28707）在真实 run 中改变每题 rollout 数（对应发现）和课程顺序（对应激励），并直接给出"GRPO 组内正当解与投机竞争优势"的机制解释。
  - 2604.01476 已经做了激励方向的干预：限制每次更新中正当 rollout 的数量，反弹会提前；换成更易的题，则不反弹。
  - CATCH（2609.39533）用 SFT 混入比例控制初始投机倾向，并控制奖励难度，研究投机何时出现。
  - brief 没有引用这三项中最近的 SimHack 和 CATCH。
- **偏离锚点。** Frozen Problem Anchor 要求解决的瓶颈是"冻结监控器在训练中对新出现投机的召回衰减"。当前 brief 完全没有涉及监控器，只回答了锚点前半句"为何延迟"。
- **C1 无法识别能力门槛。** 难执行类在步 0 只能用题目自带的离策略投机解注入，易执行类和后期检查点则用自产样本注入。注入来源与"能力"高度共变。旧策略对数概率由当前策略计算，重要性比恒为 1，等于按优势加权的 SFT。难执行类在步 0 不起飞，无法区分两种解释：能力不足，还是离策略文本的注入效力更低。
- **算力低估。** djinn 主 run 约 300 步/天，折合约 4.8 分钟一步，30 步分支约需 2.4 小时，不是 1 小时。分支算力因此被低估约 2.4 倍。仍在约束内，不致命。
- **Baseline 可复现。**
  - 两个代码库都已克隆核验：djinn 的 `train_agent.py --dataset skiptest` 加载 `djinn-problems-v0.9`，数据含 `exploit`、`insecure_verifier_info`、`exploit_type` 字段；rl-rewardhacking 的 `run_rl_training no_intervention`、`simple_overwrite_tests`、`create_all_datasets`、`eval_model` 都存在。
  - 注意 skiptest 分支的默认模型是 gpt-oss-20b，不是 Qwen3-8B。EleutherAI 报告 Qwen3 在无提示时投机"very slowly, if at all"。如果主 run 不出现投机，"出现步数的 1/4、1/2"无法定义。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 背景："延迟普遍存在 + 已有解释互不相同 + 无人干预分离" | 部分不成立（claim 阻塞） | 延迟现象属实（MATS 文章约 80–100 步；EleutherAI 投机慢）；但"EleutherAI 明确写到未分别检验"无原文支持；SimHack、2604.01476、CATCH 已做部分干预 |
| C1 发现门槛：易执行类在步 0 注入后起飞 | 部分重合 | Countdown-Code 与 CATCH 已显示预先给出投机样本（SFT）会提前或触发 RL 中的投机；SimHack 用增加 rollout 数加速发现。区别在于 RL 内注入、按检查点和类型分层 |
| C1 能力门槛：难执行类要等指令成功率上升后才起飞 | 部分新颖，但实验无法识别 | 能力是投机前兆这一思路已见于 2609.16268（工具捷径，非奖励投机）和 PRIME（2606.09711）；本设计的注入来源与能力共变，结论不可判别 |
| C2 激励门槛：起飞集中在同组正当通过率低的题 | 大部分已被覆盖 | 2604.01476 用"限制正当 rollout 数"与"更易题"做了干预；SimHack 给出 GRPO 组内竞争解释；CATCH 发现奖励越难，投机出现越早 |
| C3 诊断预测缓解：过滤题目只推迟激励门槛类投机 | 缓解本身已被覆盖，差异预测新颖 | 难度或课程推迟投机：ICML 2026 监控干预文、SimHack（课程使无投机训练延长 96.6%）、2604.01476；"只对激励门槛类型有效"的差异预测是新的，但依赖 C1 分类，而 C1 分类存在混淆 |

## 最高近邻

1. **SimHack: Predicting the onset of detectable reward hacking before RL training**（https://arxiv.org/abs/2610.28707）
   - 重叠：LeetCode RLVR（Overwrite/Lazy），Qwen3-4B，以投机出现步数为对象；改变 rollout 数（发现）和课程（激励），给出组内优势竞争解释；发现"初始投机率不决定出现时间"。
   - 差别：不做注入，不考虑能力门槛，不按投机类型区分门槛；代码未公开。
2. **When Reward Hacking Rebounds**（https://arxiv.org/abs/2604.01476）
   - 重叠：改写测试的三阶段现象；早期改写失败（能力），正当奖励稀缺导致反弹（激励）；已用"限制正当 rollout"和"更易题"做干预。
   - 差别：只有单一投机类型，不分离发现门槛，不做检查点注入。
3. **CATCH: A Controllable Analysis Testbed for Reward Hacking in Coding RL**（https://arxiv.org/abs/2609.39533）
   - 重叠：代码 GRPO，Qwen3-4B；用 SFT 混入比例控制初始投机倾向，并控制奖励难度，研究投机出现，比例低于阈值时不出现。
   - 差别：在 RL 前注入，不在 RL 中按检查点注入；没有把能力与发现分开。
4. **Countdown-Code**（https://arxiv.org/abs/2603.07084）
   - 重叠：SFT 中约 1% 的投机污染会在 RL 中重新出现，污染比例越高，投机出现越早；属于"预先给出投机"的干预。
   - 差别：在 RL 之前注入；不分投机类型的门槛，也不分检查点。
5. **CHERRL: Reproducing, Analyzing, and Detecting Reward Hacking in Rubric-Based RL**（https://arxiv.org/abs/2606.04923）
   - 重叠：可控注入偏差，出现步数随偏差类型变化（约 68–478 步），并用相关分析研究可发现性。
   - 差别：rubric RL 而非代码 RLVR；可发现性部分只是相关分析，没有检查点干预。

```json
{
  "score": 5.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "锚点偏离：Frozen Problem Anchor 要求解决的瓶颈是冻结监控器召回随训练衰减，brief 完全未涉及监控器",
    "claim 前提不成立：'EleutherAI 明确写到各解释未被分别检验'无原文支持；SimHack(2610.28707)、2604.01476、CATCH(2609.39533) 已对发现/激励做部分干预，且前两者未在 brief 中出现",
    "C1 识别混淆：注入来源（自产 vs 题目自带离策略解）与能力共变，重要性比恒为 1，步 0 难执行类不起飞无法区分能力门槛与离策略注入效力低"
  ],
  "novelty_conclusion": "RL 内按检查点注入、按投机类型分层分离门槛的设计部分新颖；C2 与 C3 的缓解部分已被 2604.01476、SimHack、CATCH 及 ICML 2026 监控干预文覆盖，C3 的差异预测新颖但依赖存在混淆的 C1；新颖性边界未立住",
  "closest_neighbors": [
    "SimHack: Predicting the onset of detectable reward hacking before RL training (arXiv 2610.28707)",
    "When Reward Hacking Rebounds: Understanding and Mitigating It with Representation-Level Signals (arXiv 2604.01476)",
    "CATCH: A Controllable Analysis Testbed for Reward Hacking in Coding RL (arXiv 2609.39533)",
    "Countdown-Code: A Testbed for Studying The Emergence and Generalization of Reward Hacking in RLVR (arXiv 2603.07084)",
    "Reproducing, Analyzing, and Detecting Reward Hacking in Rubric-Based Reinforcement Learning (CHERRL, arXiv 2606.04923)"
  ]
}
```
