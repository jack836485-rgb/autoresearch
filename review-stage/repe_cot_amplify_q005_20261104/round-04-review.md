## 结论
2026-11-04｜总体 score 5.0｜verdict: promising_needs_revision。主贡献是“在承诺之后用接收端注意力阻断切断少数承诺片段，再施加 steering/纠正前缀，不回滚即可逆转决定”，外加“锁定集中于少数承诺片段”的机制结论。目前还不够：所用阻断原语（Thought Anchors 的注意力抑制、DRTC 的接收端阻断）已经存在，Thought Anchors 还明确指出它近似于删除该句，所以方法的实际增量接近“定位并删掉少数句子再纠正”。效果证据只覆盖“整段去除 CoT”这一端，“只去掉少数片段”这一关键一步缺少直接依据。此外，方案只从 t 起阻断，S 的信息已写进 S 与 t 之间各 token 的 KV，这一点削弱了机制主张，也削弱了方法本身。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 承诺后纠正失效是真实且有用的问题：2605.26772 中固定 CoT 时 steering 翻转 39%，去掉 CoT 后升到 70%。如果能做到“不回滚即恢复”，就能给只负责检测和熔断的守卫（PROACT-Agent 明确写了它只能终止）提供处置手段。但安全设置下回滚只需重生成本轮推理，代价并不高；智能体中“保留工具进度”的优势只在 S 跨越之前已完成工具调用的步骤时才存在，覆盖比例未知。机制结论的分量取决于集中性是否成立。 |
| 新颖度 | 6.0 | 只比较“保留/整段去除”两极的是 2605.26772，本方案取的是两极之间的自然中间点。阻断原语与“从后续所有 token 阻断某句”的做法来自 Thought Anchors 和 DRTC。在推理期改注意力或 KV 来纠正、并让智能体继续任务，ICON（攻击场景下的注意力 steering）和 CachePrune（KV 剪枝）已有先例。可辨认的增量在于：用于推理模型承诺之后的解锁，并和决策方向 steering 组合。由于掩码约等于删句，它与“删除 S 文本后重新 prefill 再纠正”难以区分，而方案没有设这个对照。 |
| 有效性 | 5.0 | 现有依据：(i) 整段去除 CoT 能解锁（70%），但该数据针对“只重生成答案”；(ii) 2507.03167 显示蒸馏模型中开头一句可决定拒答，但那是在自然生成中，不是在已写出长篇服从型 CoT 之后；(iii) DRTC 的 Gini 0.50–0.58、top-5% 质量仅 0.23–0.28，属于中等集中，在 15% token 上限内能否接近整段去除的幅度没有依据；(iv) 2606.13603 的 72%/27% 来自 gpt-oss-20b 的 AIME 数字扰动，与拒答或工具决定不同类。关键未知有两点。其一，只从 t 起阻断时，S 与 t 之间的句子 KV 已经吸收了 S，服从型轨迹中计划内容通常冗余分布，间接通路很可能保住锁定。其二，在智能体中工具返回（注入）不可屏蔽，承诺可以从注入处被重新读出。 |

与起点的关系：这是起点“锁定由什么决定”的子问题方法化；“放大”一侧以及剂量、文本、预先确定三者的分离仍未回答，转向本身不构成阻断。

实验能否判别：目前不能充分判别。
- **S 的选择用到了结局读数。** S 由贪心搜索选出，标准正是“使强制作答决定越过中点”，所以“屏蔽 S 有效”部分由构造保证。同 token 数的随机句对照无法排除另一种解释：任何经结局搜索选出的小掩码都可能因分布外扰动而翻转决定。需要不经结局选择的同预算定位方式作对照，例如 Thought Anchors 重要度、t 前最后 k 句、含决定词的句子。
- **缺少两个对照。** 一是“删除 S 文本并重新 prefill 后纠正”，它同样保留工具调用，能检验 KV 掩码是否必要。二是 AgentDojo 上不回滚的同任务防御：ICON 式注意力 steering 或对注入段的屏蔽，以及 CachePrune 一类方法。
- **“更低代价”的主张缺少统计口径。** 需要报告 S 落在已完成工具调用之前的轨迹占比。DeepSeek-R1-Distill-Llama-8B 的模板会剥离历史 think，也没有原生工具调用；如果 S 落在当前步的 CoT 中，回滚并不需要重做工具调用。

可行性：pass。Qwen3-8B 与 R1-Distill-8B 在 HF eager/SDPA 下可以用自定义 4D 掩码，定位为每条 20–60 次带缓存前向，约 700 万生成 token，在 2×A100 两天内可完成；JailbreakBench、XSTest、When2Call 和 AgentDojo 都公开可得，判官为本地 Llama-Guard 加规则函数，API 预算可忽略。2605.26772 的代码有公开链接，SafeThink 与 FASB 的规范足以独立实现。需要注意两点：XSTest 只有 250 条安全提示，8B 模型的过度拒绝率较低，要收集 100–200 条“已承诺拒绝”轨迹需多次采样，可得数量应先核实；R1-Distill 在 AgentDojo 上缺少原生工具调用格式，智能体设置实际上可能只有 Qwen3-8B 一个模型。

## 最高近邻
1. Thought Anchors（2506.19143）https://arxiv.org/abs/2506.19143 ——对后续所有 token 做按句注意力抑制以衡量句子影响，作者明确说明这近似删除该句；只做归因和调试，不做纠正。
2. DRTC（2602.15332）https://arxiv.org/abs/2602.15332 ——在 pivot 处做接收端分块阻断，影响中等集中（Gini 0.50–0.58）；只做归因，不做纠正。
3. Beyond a Single Direction（2605.26772）https://arxiv.org/abs/2605.26772 ——同模型：固定 CoT 时 steering 翻转 39%，去掉 CoT 后 70%，重生成时 94%；局限部分明确说未测去除特定步骤，本方案正好填补这一点。
4. ICON（2602.20708）https://arxiv.org/abs/2602.20708 ——检测注入后在推理期做注意力 steering，以“恢复轨迹、继续任务”而非中止为目标，AgentDojo 上有评测；是智能体设置下“不回滚即恢复”的同任务强对照。
5. CachePrune（2504.21228）https://arxiv.org/abs/2504.21228 ——通过编辑或剪枝 KV 缓存来防间接注入，属于在 KV 层切断特定片段影响的近邻；SafeThink（2602.11096）与 FASB（2508.17621）分别对应早期前缀和回滚两类对照。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是在推理模型承诺后，用接收端注意力阻断切断少数承诺片段，再配合 steering 或纠正前缀，不回滚即可逆转决定，同时给出“锁定集中于少数片段”的机制结论。重要性中上：真实问题，有可服务的检测守卫，但安全设置下回滚代价本就不高，智能体中的代价优势覆盖未知。新颖度为增量：阻断原语来自 Thought Anchors 和 DRTC，且约等于删句，在推理期改注意力或 KV 做纠正有 ICON 和 CachePrune 先例，本工作是 2605.26772 两极之间的自然中间点。有效性依据间接：只有整段去除 CoT 的 70%，DRTC 的集中度仅中等；只从 t 起阻断时，S 的信息已写入中间 token 的 KV；智能体中注入段不可屏蔽，承诺可被重新读出。未达到三项≥6且至少两项≥8的门槛。",
  "feasibility": "pass",
  "feasibility_reason": "8B 稠密模型在 HF eager/SDPA 下可用 4D 掩码，定位与约 700 万 token 生成在 2×A100 两天内可完成，四个数据集公开，判官本地运行；需核实 XSTest 已承诺拒绝轨迹的数量，R1-Distill 缺少原生工具调用，智能体设置可能只有 Qwen3-8B 一个模型。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：重要性6.5、新颖度6.0、有效性5.0，没有任何两项达到8。",
    "方法与机制设计漏洞：只从 t 起阻断，未处理 S 经 S 与 t 之间 token 的 KV 传递的间接影响，“锁定=少数片段可读性”无法由此检验；同时缺少“删除 S 文本并重新 prefill 后纠正”对照，而掩码近似删句，KV 掩码的必要性和新意无法确立。",
    "机制 Claim 判别不足：S 由强制作答结局贪心选出，同 token 数随机句对照无法排除“经结局搜索的小掩码造成分布外扰动”的解释，需要不经结局选择的同预算定位对照。",
    "智能体 Claim 缺少同任务强对照与代价口径：AgentDojo 上未对比 ICON、CachePrune 等不回滚即可继续任务的防御；注入段不可屏蔽；“保留工具进度”只在 S 先于已完成工具调用时成立，覆盖比例未定义，R1-Distill 的模板剥离历史 think 且无原生工具调用。"
  ],
  "novelty_conclusion": "阻断原语（Thought Anchors、DRTC）与推理期注意力或 KV 纠正（ICON、CachePrune）都已存在；新意在于把它用于推理模型承诺后的解锁并与决策 steering 组合，属可辨认但有限的增量，且与简单删句难以区分。",
  "closest_neighbors": [
    "Thought Anchors: Which LLM Reasoning Steps Matter? (arXiv:2506.19143)",
    "Directional Reasoning Trajectory Change (DRTC) (arXiv:2602.15332)",
    "Beyond a Single Direction: Chain-of-Thought Disrupts Simple Steering of Refusal (arXiv:2605.26772)",
    "ICON: Indirect Prompt Injection Defense for Agents based on Inference-Time Correction (arXiv:2602.20708)",
    "CachePrune: Neural-Based Attribution Defense Against Indirect Prompt Injection Attacks (arXiv:2504.21228)"
  ]
}
```
