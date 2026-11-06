## 结论
2026-11-05，总体 score 4.5，verdict：needs_rethink。主贡献是用"同一模型看 clean 渲染"当教师，对引导页面上的在线轨迹做门控自蒸馏，让 7–8B CUA 不加推理调用也能抵抗引导。贡献不足，原因有三：
- **新颖度受限。** 机制上 SecOPD（2608.21500）已经做了几乎相同的事：初始模型看干净输入，对被注入输入上的 rollout 打分做在线蒸馏。一致性训练（BCT/ACT）也是同类做法。
- **教师信息不对等。** 官方 CAVEAT 代码显示，clean 渲染不是"信息等价、只去掉引导"的视图：最优商品（hero）在 clean 下排在自然结果第 1 位，storefront 上还带唯一的诚实价值徽章；steered 下 hero 被埋到深处。教师因此拿到的是近似答案位置的特权信息，学生在引导页面上拿不到。
- **门控方向反了。** 在引导页面上必需的动作（翻页、排序或筛选、多开商品页），clean 教师都会给低概率。门控恰好会挑出这些步骤，并把它们压低。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 小模型在激励错配环境中的鲁棒性有实际价值，测试时零额外调用也有用。但证据只来自一个基准：9 个环境，每个 storefront 只有 1 个场景、4–5 个变体，留出的 caveat_shop 只有 5 个场景 × 4 个变体。影响面有限。 |
| 新颖度 | 6.0 | CUA 暗模式这个目标领域里，没检索到"clean 视角自教师"训练，迁移本身有新意。但同为 agent 鲁棒性的 SecOPD 已是同一算法：冻结初始模型看干净输入当教师，学生看被操纵输入做在线蒸馏。BCT 与一致性训练也是"被操纵输入对齐干净输入的自身响应"。本方法的结构性适配只有按 URL 与商品 ID 对齐状态，没有针对 CAVEAT 中 clean 与 steered 信息不对等做适配。这是可辨认的增量，不到 7–8。brief 的近邻对比也漏了 SecOPD 和一致性训练。 |
| 有效性（先验） | 4.5 | **支持依据：** SecOPD 在注入场景、BCT 在谄媚与越狱场景、GHD 在 GUI 特权蒸馏上有效，说明"同模型 + 干净上下文教师"在信息等价的扰动下可行。**直接反证一（环境结构，代码已核验）：** storefront 的 `steering.py` 注明 clean 下 hero 保持第 1 个最佳匹配位并带诚实徽章；steered 下徽章全部剥除，hero 被移到合规块末尾往前数 2–5 位，并配合限速门让"挖掘者到不了"。CAVEAT-Shop 的 `experiment_laptops.py` 注明 clean 下 hero 在自然排序第 1 位。教师的高置信来自答案位置，不是来自"忽略引导"。按 SKU 映射后，教师偏好的动作在学生当前页上往往不可见。它对翻页、排序、多开商品页、核对结账总价这些引导下必需的探索动作给低概率，门控会选中这些步骤并压低。预勾选附加项在 clean 下没有对应元素，教师无法评分"取消勾选"。**直接反证二：** 2609.29051（PSP）在多轮 agent 上报告，以不可观测特权信息为教师的 OPSD 会让学生"装作拥有特权信息"，表现低于 GRPO，最差低于基座。本设定的 hero 位置、徽章和滴漏前的含费价正属于这类不可观测信息。此外，教师输入的"相同历史"里含有学生此前看到的引导观测，会污染教师。 |
| 待预研 | — | 7–8B 模型在 clean 下的最优购买率（因为 clean 下 hero 排第 1，可能靠"点第一个"就过了 30% 的 no-go 门槛，这个门槛不能说明教师质量）；留出环境上的增益幅度；1.2 倍调用约束与"引导下必须深挖"是否兼容。 |

**与原问题的关系：** 回答的是原问题中"能否不靠更多调用修复"一半，明确不回答"哪种机制主导失败"。这次转向本身不构成阻断。

**实验能否判别主张：否。**
- 离线行为克隆对照不成立：clean 成功轨迹点的是排第 1 的 hero，按 URL 映射到引导页面后，该元素多在后页、并不可见，这个对照按构造就偏弱，是稻草人。
- 缺少同任务最直接的竞争者：用环境自带的最优选择判定做结果奖励的 GRPO 或 RL，同样本、同步数。GHD 与 PSP 的主要对照都是它。没有这个对照，无法把收益归因到"在线、按状态对齐的教师信号"。
- 缺少零额外调用的引导感知提示基线。
- 留出集只有 20 个强相关任务 × 3 次，统计功效有限。

**可行性：pass。** 实现路径可信：CAVEAT 本地开源，接受 OpenAI 兼容接口，vLLM 可部署；clean 与 steered 由环境变量切换，两个实例可以并行。预检、训练（8×A100 约 2–3 天）和评测都在用户的算力与 5 天约束内，不需要付费 API。需要补实现的有三处：
- 购物车与结账状态需要在 clean 实例里回放动作才能对齐，只打开 URL 不够；
- 规格预算与限速门的会话状态也要同步；
- 训练用的 storefront 只有 clean 与 steered 两种条件（置顶、徽章、社会证明、预勾选附加项），没有 8 类单机制，所以留出集上的多数机制是零样本泛化。

## 最高近邻
1. **SecOPD: Mitigating Adaptive Prompt Injections by On-Policy Distillation**（https://arxiv.org/abs/2608.21500）
   - 重叠：学生在被注入输入上 rollout，由初始模型看对应干净输入打分，做在线蒸馏。核心机制几乎相同。
   - 差别：针对指令注入和工具调用 agent，不涉及多步 GUI 的呈现引导与状态对齐。
2. **CAVEAT**（https://arxiv.org/abs/2609.27273；https://github.com/microsoft/CAVEAT）
   - 重叠：同一基准；CAVEAT-27B 经 SFT、迭代 SFT 与在线蒸馏训练。
   - 差别：用外部强教师加 harness，不用匹配对照；权重未发布。
3. **Consistency Training Helps Stop Sycophancy and Jailbreaks**（https://arxiv.org/abs/2510.27062），及其来源 BCT（Chua et al.）
   - 重叠：让被操纵输入下的行为对齐无操纵输入下的自身响应。
   - 差别：单轮 LLM，离线自生成目标，不是在线多步 agent。
4. **From Self-Distillation to Self-Practice: Privileged Information for Multi-Turn Agents**（https://arxiv.org/abs/2609.29051）
   - 重叠：多轮 agent 上以同模型加特权信息为教师的 OPSD。
   - 差别：给出反证：不可观测特权信息让学生"装作知道"，不如 GRPO。
5. **The Next Screenshot Knows: Gated Hindsight Distillation**（https://arxiv.org/abs/2608.06065）
   - 重叠：GUI 上同参数教师、门控在线蒸馏。
   - 差别：特权信息是下一张截图，门控要求教师能恢复示范动作；不处理呈现操纵。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 4.5},
  "contribution_assessment": "主贡献：以同模型看 clean 渲染为教师、对引导页面在线轨迹做门控自蒸馏，使 7-8B CUA 零额外调用抵抗激励引导。重要性有但范围有限：单基准，留出 20 个任务。新颖度：目标领域无直接先例，但 SecOPD 已是同一机制（初始模型看干净输入为教师做在线蒸馏），BCT/一致性训练同类，仅增加 URL/SKU 状态对齐，属可辨认增量。有效性：CAVEAT 代码显示 clean 下 hero 位于自然排序第 1（storefront 还带唯一诚实徽章），steered 下 hero 被深埋并有限速门，教师信息不对等、近似答案键；按 SKU 映射后，教师会给翻页、排序、多开商品页等引导下必需的探索动作低概率，门控会选中并压低这些动作；预勾选附加项在 clean 下无对应元素；PSP 报告多轮 agent 上不可观测特权信息的 OPSD 劣于 GRPO 甚至低于基座。待预研：clean 下起点模型表现（可能靠点第一个通过 no-go 门槛）、增益幅度、1.2 倍调用约束与深挖需求是否兼容。",
  "feasibility": "pass",
  "feasibility_reason": "CAVEAT 本地开源，clean/steered 由环境变量切换，可并行部署；vLLM 部署 8B 模型，8xA100 约 2-3 天训练，在约束内，无需付费 API。需补实现：购物车与结账状态及规格预算、限速会话状态要在 clean 实例中回放动作对齐；训练 storefront 只有 clean/steered 一种组合引导，共约 40 个任务。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "有效性直接反证：CAVEAT 的 clean 渲染让 hero 位于自然排序第 1（storefront 另有唯一诚实价值徽章），steered 下 hero 深埋；教师所持是学生不可观测的答案位置信息，不是信息等价的去引导视图，且门控会压低引导下必需的探索动作（翻页、排序、多开商品页、核对总价、取消附加项）；PSP（2609.29051）在多轮 agent 上报告此类 OPSD 劣于 GRPO 甚至低于基座",
    "贡献不足：SecOPD（2608.21500）已实现以初始模型看干净输入为教师、对被操纵输入的在线 rollout 蒸馏，BCT/一致性训练同类；本方案只增加 URL/SKU 状态对齐，三项分数无一达到 8，不满足 8/7/6 门槛",
    "Claim 阻断：缺少同任务、同样本预算、以环境最优选择判定为奖励的 GRPO/RL 对照，无法把收益归因到状态对齐的教师信号；离线行为克隆对照因 clean 成功轨迹点的是第 1 位 hero、映射到引导页后多不可见而按构造偏弱",
    "定位缺失：brief 未与 SecOPD、一致性训练（BCT/ACT）比较"
  ],
  "novelty_conclusion": "目标领域（CUA 暗模式/激励引导）未见 clean 视角自教师训练，但相邻的 agent 鲁棒性领域中，SecOPD 已用同一机制（干净输入教师 + 在线蒸馏），一致性训练同类；跨领域增量仅为多步 GUI 状态对齐，且未针对 CAVEAT clean 与 steered 信息不对等做结构性适配，新颖度约 6。",
  "closest_neighbors": [
    "SecOPD: Mitigating Adaptive Prompt Injections by On-Policy Distillation (arXiv:2608.21500)",
    "CAVEAT: Towards Robust Computer-Use Agents in Incentive-Misaligned Environments (arXiv:2609.27273)",
    "Consistency Training Helps Stop Sycophancy and Jailbreaks (arXiv:2510.27062)",
    "From Self-Distillation to Self-Practice: Privileged Information for Multi-Turn Agents (arXiv:2609.29051)",
    "The Next Screenshot Knows: Gated Hindsight Distillation for Mobile GUI Agents (arXiv:2608.06065)"
  ]
}
```
