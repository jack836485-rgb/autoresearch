## 背景

**定位关键词：** reward hacking；training-time reward hacking；prompt-elicited trajectories；on-policy probe training data；linear probe；RLVR

**一句话定位：** 代码 RLVR 中，自然奖励投机在训练中途才出现。出现之前没有在策的自然正例可以训练监控器，而用提示诱导数据训练的监控器又对训练期自然投机泛化差。

## 核心 Claim

1. **现有失败。**
   - 用提示诱导轨迹训练的监控器，对训练期自然投机泛化差（Trace-and-Amplify，arXiv 2604.23488）。
   - 探针泛化受训练数据生成方式影响，以"意图"定义的行为最敏感（Kirch et al.，arXiv 2511.17408）。但该研究面对的是静态模型，自然正例存在。
   - Engels/Nanda 指导的 overwrite-tests 实验（Qwen3-4B，GRPO，LeetCode）：基座模型自然触发漏洞的频率低于千分之一；RL 约 80–100 步开始投机；固定 LLM judge 与探针在投机 run 中，从训练开始到结束准确率下降约 16 点。
   - 已有受控研究显示投机受能力门控：捷径只对已学会的工具形成（2609.16268）；早期改写评测器的尝试因能力不足失败，之后以不同策略成功（2604.01476）。
2. **被忽视的关键。** 在 RL 中，策略在漂移，目标行为在出现之前没有自然样本。因此"用在策数据"在这个时刻无从谈起。真正能选择的只有两样：由哪个检查点、在哪个时点去诱导。这一变量从未被操纵过。本 Idea 主张：
   - **C1（诱导分布随检查点逼近）**：在自然投机出现之前的预设时点 t（步 20/40/60），检查点 t 被指示投机时产生的投机，其策略类别分布比初始模型诱导的分布更接近 t 之后自然出现的投机。距离用类别分布的总变差衡量。同时报告各检查点"被指示时投机成功"的比例随步数的变化，作为"能力先于倾向"的直接测量。
   - **C2（前瞻监控）**：只用 t 时可得的数据训练监控器：
     - 正例：当前检查点被指示投机、且代理奖励通过的样本；
     - 负例：同一检查点无指令、代理奖励通过的样本。负例污染率即 t 时的自然投机率，自然投机出现前很低，用真值实测并报告。
     - 这一监控器在 t 之后整个训练中对自然投机的召回，高于初始模型诱导的监控器；也高于用同一时点可得的真值标注自然数据训练的监控器（彼时自然正例极少）。
   - **C3（拆分与风格检验）**：
     - 同家族更大的非 RL 模型诱导：接近当前检查点诱导的效果，则差距主要来自能力；接近初始模型诱导的效果，则差距主要来自 RL 形成的分布。
     - 在去注释、经 AST 规范化的代码输入范围内，若 C2 的优势消失，则差距来自诱导带来的文本风格（Trace-and-Amplify 的解释），本 Idea 的分布解释被推翻。

## 方法设计的核心思想

- **输入**：RL 训练早期（自然投机出现前）的检查点；固定诱导提示（明确要求利用题面给出的测试漏洞）；代理奖励。
- **动作**：在预设时点对检查点做指令诱导与无指令采样，按上面的规则构造正负例，训练读取方固定的监控器：冻结基座激活上的线性探针，以及文本分类器。不读取策略自身激活，以排除 Obfuscation Atlas（2602.15515）报告的表示漂移。真值只用于评测。
- **输出**：在投机出现前就位的监控器，以及"诱导者 × 时点"对之后自然投机覆盖的测量。
- **与最高近邻的差别**：
  - Trace-and-Amplify 比较诱导数据与训练期自然数据，并归因于风格；
  - Kirch et al. 在静态模型上比较 on/off-policy 数据；
  - PRIME（2606.09711）用内部表征预测投机出现的时刻，不构造监控数据，也不比较诱导者。
  - 本 Idea 在策略漂移、目标行为尚未出现时，把诱导者与诱导时点作为操纵变量，检验它们能否预见之后的自然投机。

## 最小实验

- **主测试床：Engels/Nanda 的 overwrite-tests 环境。**
  - 设置：Qwen3-4B，thinking 关闭，LeetCode 中/难题，GRPO，200 步，3 个种子。
  - 已报告的策略类别：`return`/`pass` 绕过、硬编码少数用例、写迎合自身解的错误用例、打印代替断言、不报错的 `assertEqual`、只测题面示例。
  - 真值：是否只通过自定义测试。
- **第二测试床：Trace-and-Amplify。** Qwen2.5-Coder-1.5B-Instruct 与 DeepSeek-Coder-1.3B-Instruct，各 3 种子，约 300 步。只检验 C2 是否跨模型家族成立。
- **对照**：同一监控器结构与超参、同一诱导提示、每个时点各 800 条正例与 800 条负例。
  1. 初始模型诱导（即 prompt-elicited 冻结 baseline，按本设计自行构造）；
  2. 同家族更大非 RL 模型诱导（Qwen3-8B / Qwen2.5-Coder-7B-Instruct / DeepSeek-Coder-6.7B-Instruct）；
  3. 当前检查点诱导（本 Idea）；
  4. 同时点真值标注自然数据训练；
  5. 参照上界：自然投机出现后用真值标注数据训练；
  6. 参照：零样本 LLM judge。
  - 输入范围分完整回答与规范化代码两种。
- **指标**：
  - 对 t 之后各检查点窗口的真值自然投机，计算 TPR@5%FPR 与 AUROC；
  - 诱导与自然投机的策略类别总变差距离；
  - 指令投机成功率曲线；
  - 正负例标签纯度（真值核对）；
  - 回答长度与注释数作协变量。
  - 预设：样本数 ≥30 的策略类别少于 3 类时，C1 改用"诱导投机与自然投机的监控器得分分布距离"代替类别距离。
- **支持与推翻**：
  - **C1**：检查点诱导的距离显著小于初始模型诱导（3 种子）。若相等，或指令投机成功率在步 0 已饱和、分布也不变，则 C1 被推翻；后一情形说明投机的门槛是倾向而非能力。
  - **C2**：前瞻监控器的召回在 t 之后显著高于对照 1 和对照 4。否则被推翻。
  - **C3**：看对照 2 落在哪一侧，以及规范化代码范围内 C2 优势是否保持。
- **Baseline 来源与复现：**
  - **overwrite-tests**
    - 说明：https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against
    - 代码：https://github.com/ariahw/rl-rewardhacking ，已克隆核验。
    - `create_all_datasets` 生成带漏洞提示的数据。
    - `run_rl_training no_intervention --model_id qwen/Qwen3-4B --task simple_overwrite_tests --seed k` 训练。
    - `train_probe` 流程在冻结基座激活上训练 mass-mean / logistic 探针。该流程默认使用真值标注数据，本实验只替换输入数据。
    - LLM judge 经 OpenRouter 调用；`eval_model <RUN_NAME> <step>` 评测。
  - **Trace-and-Amplify**
    - 论文：https://arxiv.org/abs/2604.23488
    - 代码：https://github.com/LichenLillc/CoTMonitoring ，已克隆核验。
    - `Trace-and-Amplify_Framework/train_script.sh` 训练；`my_utils/add_fake_test_final-ver.py` 注入伪测试。
    - `CoTMonitors_Training_and_Evaluation/scripts/paired_probe_pipeline/BERT_pipeline.sh` 训练文本分类器；`scripts/gpt_evaluate.py` 为 LLM 监控器。
    - 发布数据为 Git LFS 指针，本实验不依赖它，全部轨迹自产。
  - 两个测试床与本任务同为代码 RLVR 训练期投机监控。
- **算力与 API 估算：**
  - **overwrite-tests**：仓库未给训练时长。按 8×A100 每次约 1 天粗估（需试跑核实），3 次约 576 A100 小时。
  - **Trace-and-Amplify**：原文 4×A6000、约 300 步。按 4×A100 每次约 1 天，6 次约 576 A100 小时。
  - **诱导与采样**：9 条轨迹 × 3 个时点 × 3 种诱导者 × 约 1,600 条，加上真值标注评测采样，1.3–8B 推理约 80 A100 小时。
  - **监控器训练**：分钟到小时级。
  - **合计**：约 1,250 A100 小时，8×A100 上约 7 天。
  - **LLM judge**：默认本地 Qwen3-8B。若改用 API，按约 8×10⁷ 输入 token、每百万约 1 美元，约 80 美元（约 580 元）。
