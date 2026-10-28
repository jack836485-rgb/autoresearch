## 背景

**定位关键词：** reinforcement learning with verifiable rewards；compositional generalization；counterfactual evaluation；distributionally robust optimization

**一句话定位：** 这是在程序可验证的数学与符号推理中，用结构保持的问题变换判断 RLVR 是否获得可复用能力的问题。

## 核心 Claim

1. 单题 `pass@k`、Cover@τ 或轨迹表征多样性都不能区分“罕见命中”与“可复用的新能力”；一个更严格但仍可计算的经验判据是：在未见底层实例的多个结构等价变体上，RL 模型都达到预先固定的可靠性阈值，并超过给 base 更大采样预算得到的 decoding envelope。
2. 在相同训练 rollout token 下，vanilla GRPO、RepExp 和 DIVER 的 IID 增益不一定转化为上述跨变体能力增益；若它们只改变已有轨迹的概率或表面多样性，这个差距会在 held-out 变换族上暴露。
3. 不引入 teacher，只把一个训练 group 分配给同一底层问题的多个结构保持变体，并最大化变体成功率的 lower-tail/CVaR，可以比这些 baseline 获得更多通过该经验判据的 held-out 问题族；若它只提高平均正确率而不提高 family-level lower-tail 或不能超过 base envelope，则 Claim 被推翻。

## 方法设计的核心思想

输入是 Reasoning Gym 中一个可程序验证的底层实例，以及由实体重命名、输入顺序置换或图节点重标号生成的等价变体。每次更新在固定总 rollout 数和总 token 下，为同族多个变体各生成少量回答；verifier 先给每个回答二元正确性，再用该族各变体成功率的下尾均值形成一个 family reward，并与原始 outcome reward 相加后计算 GRPO advantage。输出仍是普通解答，不要求额外 CoT 标注。与 RepExp、DIVER 和低似然奖励的关键差别是：本方法不把“距离远”当新颖，而只奖励同一底层能力在结构保持干预下的最差端可复用性。

## 最小实验

固定 `Qwen2.5-Math-7B`、3 个 seed、同一批 Reasoning Gym 底层实例、相同训练 prompt 数、总 rollout token、更新步数、最大响应长度和评测 token。选择 3--4 个能精确生成等价变体且 verifier 不变的任务族，例如 Countdown 输入置换、图任务节点重标号、逻辑任务实体重命名；底层实例在 train/test 间完全隔离。比较：(a) base decoding envelope，冻结 base checkpoint，在每个 held-out family 上使用温度/采样网格，给它 8 倍评测 token，依据 https://arxiv.org/abs/2609.01274 的预算化搜索思想直接实现；(b) vanilla GRPO，使用已核验的 Reasoning Gym `training/train_grpo.py` 和 `training/rewards/reward.py`（https://github.com/open-thought/reasoning-gym）；(c) RepExp，使用已核验的 `rep_exp/train_elliptical.sh`、`main_rep_exp.py` 和 elliptical reward manager（https://github.com/verl-project/verl-recipe/tree/main/rep_exp，论文 https://arxiv.org/abs/2510.11686）；(d) DIVER，使用已核验的 `scripts/train/baseline.sh` 与 `verl/div_src/reward_fn.py`（https://github.com/NJU-RL/DIVER，论文 https://arxiv.org/abs/2509.26209）；(e) 本方法，只在 vanilla 脚本中改变 group 构造和 reward 聚合。主指标是 held-out family 中所有变体均达到 `τ=0.2` 的 family coverage、最差变体 pass@1，以及超过 base 8× decoding envelope 的 family 数；普通 pass@1/pass@k 为次指标。支持 Claim 的结果是本方法在 3 个 seed 上提高 family coverage 且产生非零、可复现的 envelope-exceeding families，而 IID pass@1 相近；若优势只出现在普通 pass@1、对变体下尾无提升，或 base 的扩大搜索能恢复这些 family，则推翻 Claim。
