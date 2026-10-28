## 背景

**定位关键词：** reinforcement learning with verifiable rewards；counterfactual generalization；rule following；algorithmic generalization

**一句话定位：** 这是在程序化符号推理中，区分模型只是提高固定任务解法概率，还是学会按题面给出的新规则改变推理轨迹的问题。

## 核心 Claim

1. “新能力”在有限实验中不能被证明为 base 分布的理论零支持，但可以形成更强的、可证伪的**规则条件化获得证书**：在训练未见的随机运算规则和更深表达式上，RL 模型对成对规则干预的联合成功率之单侧 95% 置信下界高于预注册阈值 `τ_RL=0.20`，而冻结 base 在预注册 8 倍采样预算内的对应单侧 95% 置信上界低于 `τ_base=0.05`；同时两个规则世界的正确答案被 generator 保证不同。
2. 在随机规则每个实例都重新采样、固定表达式表面模板的设置中，singleton GRPO 或仅增加规则对暴露的 outcome-only GRPO 仍可能学到局部频率捷径；若真正缺的是“规则变化应导致轨迹变化”的条件响应，二者不会稳定通过上述联合证书。
3. 对真实规则下 verifier-valid 的轨迹，联合优化其在真实 prompt 与反事实规则 prompt 下的对数似然差，再叠加普通 outcome GRPO，可以在相同训练 prompts、rollout token、反事实重算 token 和更新步数下，比 paired-exposure GRPO 获得更多通过证书的 held-out 规则族。若提升被 paired-exposure GRPO 解释、只出现在见过的规则或浅层表达式，或者 base 的预注册搜索包络恢复，则 Claim 被推翻。

## 方法设计的核心思想

使用 Algebrarium 的 `random_latin_square` 与表达式树生成器构造任务。每个训练单元共享同一载体集合、表达式树和表面模板，但含两个独立运算表 `R` 与 `R'`；只保留执行结果不同的规则对。模型分别在两条 prompt 上采样，程序 verifier 检查最终答案和逐步状态。普通 outcome reward 仍按 prompt 内独立组计算。对于在 `R` 下完全验证通过、且同一轨迹按 `R'` 执行失败的 rollout `y`，增加反事实轨迹对比项 `log π(y|x_R)-log π(y|x_R')`；对 `R'` 下的正确轨迹对称处理。它把 verifier-valid 轨迹自动变成另一个规则世界的 hard negative，不依赖 teacher 或人工过程标注。该项不是组内公共常数：真实和反事实 prompt 上的 token log-ratio 直接对参数求导，因此不会被 GRPO 的 reward centering 消除。与 PIRL/同构扰动要求同义输入保持输出不变不同，这里改变任务定义并要求轨迹随干预改变；与 ACRE 的选项重排一致性不同，这里训练的是未见形式系统上的规则条件化，而不是答案位置不变性。

## 最小实验

固定 `Qwen2.5-Math-7B`、3 个 seed、一个 `8x80GB` 节点量级；各方法使用相同训练底层表达式、prompt 数、采样响应 token、更新步数、最大响应长度和评测 token。主任务用公开 Algebrarium（https://github.com/Linzwcs/Algebrarium）：已核验 `python -m algebrarium.cli`、`src/algebrarium/generators.py::generate_random_latin_square`、表达式 generator、确定答案与 CoT 输出；训练接入 Reasoning Gym 已核验的 `training/train_grpo.py` 和 `training/rewards/reward.py`（https://github.com/open-thought/reasoning-gym）。训练使用载体大小 4--5、表达式深度 2--4 的随机规则，测试底层 seeds、规则表完全隔离，并分成同深度 held-out 与深度 5--6 外推两层。比较：(a) 冻结 base 的预注册 8 倍搜索包络，温度固定为 `{0.6,0.8,1.0}`，不按 test 表现挑 decoder；(b) singleton outcome GRPO；(c) paired-exposure outcome GRPO，看到与本方法完全相同的规则对、各 prompt 独立计算 reward，并执行相同的跨 prompt teacher-forced 前向但将对比项系数设为零；(d) DIVER，使用已核验的真正入口 `scripts/train/train_diver.sh`（`div_coeff=0.1`）和 `verl/div_src/reward_fn.py::RewardManager`（https://github.com/NJU-RL/DIVER），把同一 Algebrarium parquet/scorer 接入后保持模型、8 rollouts 与核心预算一致；(e) generator-trace SFT，使用同一公开 generator 的确定性轨迹、匹配优化 token，不使用外部 teacher；(f) 本方法，在 (c) 上加入对称反事实轨迹似然比。主指标是在至少 500 个 held-out 规则对上“两个世界均正确且答案按规则改变”的 pair success，以及其 across-seed hierarchical bootstrap 区间；证书判定额外用预注册的单侧 Clopper--Pearson 界，且只报告有限预算可达性。次指标为单世界 pass@1、规则交换后沿用旧答案率及深度外推曲线。关键机制对比只看 (c) 对 (f)，两者的生成和前向计算图完全相同，只差对比项是否反向传播：若 (f) 的 pair success 区间不高于 (c)，则反事实对比机制失败；若 SFT 达到同等或更好结果，则结论应写成“显式规则轨迹监督更有效”，不能宣称 RL 特有的能力获得。
