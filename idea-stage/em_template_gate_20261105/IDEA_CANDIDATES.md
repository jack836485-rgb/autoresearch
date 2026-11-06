# Idea 候选池

- 输入模式：`raw_idea`
- 输入论文：不适用
- 输入问题卡：不适用（起点是用户自有的 EM 实验发现，见 RAW_IDEA.md）

## 当前选择

- Reviewer 调用：`1 / 6`
- 当前选中 Idea：暂无（IDEA-001 已审未过）
- 选择理由：唯一同时有一手效果依据（在已知存在条件失配的模型上，修补把有 cue 时的失配率从 29.9% 降到 4.0%）、已知领域失败（2604.25891）和方法空位的候选。
- 状态：`Call 1 为 4.0，needs_rethink；主要近邻 Piggyback/TReFT 未被 improver 读到（检索结果中出现过但没有打开），暂停送审，向用户汇报`

## 候选列表

### IDEA-001：条件失配经由模板位置的门表达——锚定 assistant 头后半层 K/V 的缓解在触发下仍然有效

- 来源：`原始想法`（用户的一手发现）结合 `相似领域成熟方法迁移`（流行病学加性对乘性交互的诊断；TASA 的模板锚定；ViT registers 的全局信息存放 token）
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：emergent misalignment、conditional misalignment、chat template、activation patching、KL regularization
- 一句话背景：数据层的 EM 缓解会把失配藏到上下文触发后面（2604.25891）；用户数据显示，残留失配的表达集中在 assistant 头位置的后半层 K/V，而 cue 在对数几率上做独立的乘性调制。
- 主贡献：
  1. 机制：条件失配不是"被缓解掉的失配被触发重新激活"，而是一个共享门（模板位置后半层 K/V）加上一个独立的触发增益；
  2. 诊断：用对数几率交互分析给缓解方法分类：作用在门上的方法在有无触发下产生平行的对数几率下移；上下文型方法只压无触发格，造成交互；
  3. 方法：训练时把模板位置后半层的 K/V 锚定到基座（位置特异的正则），预测它在触发下仍有效，并保留窄任务与通用能力。
- 贡献自评：
  - 重要性 7.5：直接针对 Evans 组报告的主流缓解失败模式；
  - 新颖度 7.5：位置特异的门和缓解分类没有检出先例；近邻是 TASA（安全拒答，不是 EM）、人格方向消融、全序列 KL 正则；
  - 有效性 7：在恰好存在条件失配的模型上，推理时修补后，有 cue 失配率从 29.9% 降到 4.0%，连贯性最多降 0.2pp；训练时正则是否同样有效未知。
  - 待预研：窄任务与通用能力的保留、训练时版本的效果、跨数据集与模型的普适性。
- 可行性：pass（7B LoRA、官方条件失配代码、本地 72B judge 或付费 judge）
- 自评分：`7.3/10`
- Reviewer 记录：`Call 1（常规，同模型 high）：4.0/10（重要性 5.5 / 新颖度 3.5 / 有效性 6.0），needs_rethink`。
  - 最高近邻：Piggyback/TReFT 2606.06667（模板 K/V 修补恢复对齐；训练时正则模板位置 K/V；优于 KL 与交织；含 Qwen-2.5-7B；代码 CHATS-lab/Token-Regularized-Fine-Tuning）；ContextLift 2610.21633；2604.25891；BLOCK-EM 2602.00767；2607.21356。
  - 阻断：方法与机制已被 TReFT 覆盖；没有与 ContextLift、TReFT 原版对比；剩余增量只有条件触发下的评测和一个标准的 logistic 交互读法。

### IDEA-002：只做诊断——用对数几率交互分析给 EM 缓解方法分类

- 来源：`相似领域成熟方法迁移`（流行病学效应修饰）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：emergent misalignment、conditional misalignment、mitigation evaluation
- 一句话背景：2604.25891 已用绝对失配率报告条件失配。
- 主贡献：只给出评估框架，没有方法。
- 自评分：`5.5/10`
- Reviewer 记录：`尚未送审`

### IDEA-003：模板 register 隔离——窄微调时加入可学习的模板 token 吸收全局倾向漂移，推理时移除

- 来源：`相似领域成熟方法迁移`（ViT registers）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：emergent misalignment、inoculation prompting、soft prompt
- 一句话背景：Inoculation Adapters（2606.30252）与 inoculation prompting 已是同类思路，后者在 2604.25891 中会变成触发。
- 自评分：`5.8/10`
- Reviewer 记录：`尚未送审`
