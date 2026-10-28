## 背景

**定位关键词：** reinforcement learning with verifiable rewards；counterfactual generalization；rule-conditioned reasoning；unlikelihood training

**一句话定位：** 这是在可执行规则世界中，让 RLVR 不只奖励答对，还在规则被干预时准确撤销已经失效的第一步状态转移的问题。

## 核心 Claim

1. 有限实验不能证明 base 理论零支持；本文只定义**规则条件化获得证书**：对预注册的每个 held-out 规则族，RL 模型在成对规则世界中生成两条均可被 interpreter 完整重放、且在正确首分歧点产生不同状态的轨迹，其 pair-success 单侧 95% 下界高于 `0.20`；冻结 base 在预注册 8 倍响应 token 包络下的上界低于 `0.05`。该证书比普通 pass@k 强，但只陈述给定预算和任务分布上的经验获得。
2. Outcome-only GRPO、DIVER 或按正确状态比例给部分 reward 都没有明确告诉策略：当某条规则改变时，原轨迹从哪一步开始必须停止沿用。它们可以提高单世界正确率或轨迹多样性，却仍在 held-out 规则下复制来自另一世界的首个失效状态。
3. 在普通 paired outcome GRPO 上，仅加入由 interpreter 自动定位的**首分歧状态排斥**，即在反事实 prompt 与仍然共同有效的轨迹前缀下，对旧世界首个错误 next-state token span 作 unlikelihood，可比等数据等前向的 outcome-only、在线正向自模仿和 state-reward GRPO 获得更多通过证书的规则对。若优势可由任一控制解释，或只改善单世界准确率而不降低首分歧复制率，则 Claim 被推翻。

## 方法设计的核心思想

每个任务输出 canonical trace：`STEP i | rule_id | input_state | next_state`，以及最终答案。任务 interpreter 逐行重算 `next_state`；格式可解析、每一步等于 interpreter 结果且终态正确时，rollout 才获得普通 outcome reward。对一个在规则 `R` 下通过的 rollout，保持其 token 序列不变，在配对规则 `R'` 下重放：从第 1 步开始找出 interpreter 期望状态与 rollout 声明状态首次不同的位置 `j`。由于 `j` 之前的前缀在两个世界都有效，只在 `R'`、该共同前缀条件下，对 rollout 的第 `j` 个 `next_state` token span 最小化 `-sum log(1-p(token))`；反向配对对称处理。没有额外正向 MLE，正向学习仍完全来自两边共有的 outcome GRPO。对照 `outcome-only` 执行相同 replay 和额外 teacher-forced forward 但 stop-gradient；`positive-only` 使用相同 mask 与系数、把第 `j` 个 span 换成真实世界中的正向 NLL；`state-reward` 只按 interpreter 判对的状态比例塑形。这样负向反事实排斥、额外 token-level 梯度和结构 reward 三种解释可以分开。

## 最小实验

固定 `Qwen2.5-Math-7B`、3 seeds、一个 `8x80GB` 节点量级，以及相同的训练 prompt、采样 rollout token、更新步数、最大响应和评测 token。训练/测试包含三个规则机制独立且都有公开实现的族：(A) Algebrarium 随机 quasigroup/Latin-table 表达式，使用 https://github.com/Linzwcs/Algebrarium 的 `src/algebrarium/generators.py::generate_random_latin_square`、`factory.py` 表达式树和 `substeps`，本方法仅新增逐节点 canonical trace parser；(B) 反事实进位制加法，使用 https://github.com/ZhaofengWu/counterfactual-evaluation 的 `arithmetic/sample_ccc.py`、`eval_ccc.py`，canonical state 是每一位的和、输出位与 carry；(C) 非标准程序语义，使用 ICML 2026 PLSemanticsBench 的公开 `predtrace` 数据、`exec-trace` 与 `src/plsemanticsbench/core/evaluator.py`（https://github.com/EngineeringSoftware/PLSemanticsBench）。三族分别冻结可实现的分布外轴：A 以 Latin-table seed 与表达式树同时隔离，B 训练 base 5--8、测试未见 base 9--12 且数字串隔离，C 按 PLSemanticsBench 的 nonstandard `mutation-pattern` 分组留出并同时隔离程序；训练轨迹深度 2--4，测试另含深度 5--6。开发集只用于选择一个所有方法共用、base 单次成功率在 0.1--0.4 的难度带，阈值与 test seeds 先冻结。比较 base 8 倍包络、paired outcome GRPO、positive-only、state-reward GRPO、DIVER、generator-trace SFT 和首分歧排斥；DIVER 使用已核验的 https://github.com/NJU-RL/DIVER `scripts/train/train_diver.sh`（`div_coeff=0.1`）与 `verl/div_src/reward_fn.py::RewardManager`，接同一 parquet/interpreter scorer。每族至少 500 个 held-out rule pairs；主指标为 pair success、首分歧旧状态复制率和每族单侧 Clopper--Pearson 证书，跨 seed 差异用以 rule-pair 为 cluster 的 hierarchical bootstrap。支持 Claim 3 必须在至少两个族显著优于所有三项机制控制、第三族不劣；否则只报告边界或负结果。SFT 若相当或更强，则明确结论为程序轨迹监督优于该 RL 机制。
