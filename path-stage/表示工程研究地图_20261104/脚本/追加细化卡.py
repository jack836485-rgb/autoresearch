# -*- coding: utf-8 -*-
"""第二轮细化：在拥挤簇内部，用近邻论文的失败条件与矛盾提炼更细的问题卡，追加到 研究问题.json。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ev(i, t, org, loc, role, setup, var, ctrl, obs, bound):
    return {"作品ID": i, "标题": t, "机构": org, "原文链接": f"https://arxiv.org/abs/{i}", "位置": loc, "阅读版本": "v1",
            "证据角色": role, "实验设置": setup, "变化变量": var, "对照与保持条件": ctrl, "具体观察": obs,
            "成本口径": None, "证据边界": bound}


NEW = [
{"id": "Q005", "细化自": ["Q003", "Q001"],
 "具体问题": "推理模型中，在 steering 下生成的思维链会放大被 steer 的决定（思考模式比不思考更容易被 steer），而 steering 之前已写好的思维链会锁住原决定；放大与锁定各由什么决定？放大是剂量效应、文本正反馈，还是答案在审议前已预先确定？",
 "宏观标签": ["推理模型", "审议放大", "合理化", "CoT 监控"],
 "线索类型": ["受控实验中的反常结果", "跨论文矛盾"],
 "证据": [
  ev("2604.01202", "Therefore I am. I Think.", [], "§3.1、§3.4、Table 1", "原始实验（窗口外、白名单外）",
     "Qwen3-4B 与 GLM-Z1-9B；When2Call（NVIDIA）与 BFCL 的工具调用决策；从生成前激活提取决策方向；n=100／方向", "steering 强度 α、注入／抑制、思考／不思考", "同一决策方向与样本",
     "Qwen3-4B When2Call α=12：抑制翻转 思考 49% vs 不思考 18%，注入 62% vs 29%；BFCL α=12：抑制 26 vs 20，注入 53 vs 27；GLM-Z1-9B 注入在 BFCL α=30 达 79%；作者称思考模式一致更易被 steer，且 CoT 常为被翻转的决定找理由",
     "单次运行、n=100；是否有范数匹配随机方向对照未核实；思考模式下被 steer 的 token 数是否更多未核实（剂量混淆）；GPT-OSS-20B 因 MoE 被排除"),
  ev("2605.26772", "Beyond a Single Direction: Chain-of-Thought Disrupts Simple Steering of Refusal", [], "摘要", "原始实验（白名单外，仅摘要）",
     "DeepSeek-R1-Distill-Llama-8B 拒答", "CoT 固定／去除／在 steering 下重新生成", None,
     "CoT 固定 39%，去除 CoT 70%，在 steering 下重新生成 CoT 94%；移除 steering 后仅凭重新生成的 CoT 保留 48% 效果", "仅摘要"),
  ev("2603.01437", "Post-Hoc Reasoning in Chain of Thought: Decoding and Steering Pre-Committed Answers", [], "§3.4、§4.2、附录 F", "原始实验（窗口外、白名单外）",
     "指令模型（含 Qwen2.5-7B、Gemma-2-9B）与一个推理模型（GPT-OSS-20B）；二选一任务的答案 steering，范数匹配正交对照", "steering 方向与强度", "范数匹配正交方向",
     "指令模型中探针方向翻转率显著高于正交对照，较大模型对任意方向更鲁棒；推理模型上探针能解码答案，但探针方向与正交方向的翻转率都很低",
     "推理模型只有 GPT-OSS-20B，为 MoE，结论可能与路由混淆（见 Q004）"),
  ev("2603.05488", "Reasoning Theater: Disentangling Model Beliefs from Chain-of-Thought", ["Harvard"], "摘要", "原始实验（窗口外，仅摘要）",
     "DeepSeek-R1 671B、GPT-OSS 120B；MMLU 与 GPQA-Diamond；注意力探针、强制提前作答、CoT 监控", "题目难度", None,
     "简单回忆题的最终答案远早于 CoT 监控就可从激活解码；难题更接近真实推理；回溯／顿悟几乎只出现在探针显示大幅信念变化的回答中", "仅摘要")],
 "已有解决方法": [],
 "已支持的解释": ["决定可在推理 token 之前从激活解码（2604.01202、2603.01437、2603.05488）"],
 "待验证解释": ["思考模式更易被 steer，是因为 CoT 为被改的决定找理由并自我强化（2604.01202 作者描述，未与剂量对照分离）",
                "已写好的 CoT 文本携带原决定、抵消 steering（2605.26772 的固定 CoT 结果）",
                "推理模型难以 steer（2603.01437）可能由 MoE 路由造成，而非审议本身"],
 "尚未解决": "两篇独立工作都出现'在 steering 下审议会放大决定'，但没有工作把它当作现象分离：剂量（被 steer 的 token 数）、文本正反馈、预先确定程度三者未被拆开；放大何时转为锁定也不清楚。本轮检索未检出专门研究。",
 "可检验切口": "在稠密推理模型上，对同一决策方向比较：只在生成前位置注入后关闭 vs 全程注入；思考 vs 不思考在相同被 steer 的 token 数下比较；用 steering 前的 CoT 文本强制续写 vs 自由重新生成；按预先确定程度（探针置信度或题目难度）分层。观察翻转率、CoT 长度与合理化比例。",
 "已知边界": ["证据多在 4–9B 稠密模型与工具调用／拒答／二选一任务", "多数证据在窗口外且非白名单"],
 "解决状态": "机制未定",
 "查新状态": "做了定向网页检索（思考模式更易 steer、CoT 放大／合理化），只找到 2604.01202 报告该现象而未分离；未进行完整查新。",
 "与其他问题的关系": ["Q003：已生成文本通路", "Q004：GPT-OSS 的 MoE 混淆", "Q006：决定类变量的 steering"]},
{"id": "Q006", "细化自": ["Q001"],
 "具体问题": "答案级 steering 在'信息来源选择'类失败（受线索诱导的偏差、上下文与参数知识冲突）上能恢复正确答案，但在'推理过程'类失败（矛盾盲视、过度思考、工具调用决策）上只注入全局标签偏置，纠正错误的同时破坏原本正确的决定；这条分界由什么决定？",
 "宏观标签": ["答案级 steering", "全局先验偏移", "修复 vs 移动"],
 "线索类型": ["跨论文矛盾", "受控失败实验"],
 "证据": [
  ev("2607.18114", "How Does Alignment Tuning Shape Representations of Sycophancy and Related Cue-Induced Biases in LLMs?", ["University of Toronto"], "摘要", "原始实验（仅摘要）",
     "5 个模型家族、7 种线索诱导偏差", "沿偏差方向 steering", None,
     "每种偏差都有可解码、可 steer 的线性方向，steering 在所有家族上恢复无偏答案，并保留大多数原本正确的答案", "仅摘要"),
  ev("2610.20067", "Which Knowledge Should LLMs Trust? Uncovering a Generalizable Steering Direction Across Knowledge Conflicts", ["Peking University"], "摘要", "原始实验（仅摘要）",
     "4 个模型家族；事实冲突、RAG、记忆、规则遵循", "上下文／参数知识偏好方向", None,
     "单一方向可在上下文与参数答案之间切换，并迁移到 RAG、记忆与规则遵循", "仅摘要"),
  ev("2608.29431", "Evaluating the Semantic Specificity of Representation Steering in Language Models", ["University of Cambridge"], "§5.1–5.3", "原始实验",
     "矛盾盲视的后层局部 steering；4 个模型家族", "α、是否 oracle 门控", "同一 steering vector",
     "oracle 门控下 100% 恢复；无门控时原本答对的规则准确率随 α 单调下降，错误集中在目标标签", "具体数值未取到"),
  ev("2605.05715", "Decodable but Not Corrected by Fixed Residual-Stream Linear Steering", ["Amazon"], "贡献节、§4.1", "原始实验",
     "Llama-3.1-8B-Instruct（主）、Qwen2.5-7B；MedQA 过度思考", "steering 方法族与配置（29 种）", "同一失败样本集",
     "可解码 71.6%，steering Δ≈0", "失败模式标签由判分器标注"),
  ev("2609.36138", "When Does Correction Become Repair? Mechanistic Auditing of Internal Interventions in Tool-Using LLMs", [], "摘要", "原始实验（白名单外，仅摘要）",
     "7 个 LLM；When2Call 与 MetaTool 的 K 路工具决策", "方向与路由条件", "59 个预算匹配随机方向",
     "5 个模型有方向特异的净增益；但净增益 +55 的干预破坏了它触及的基线正确决策中的一半以上", "仅摘要；代码已公开")],
 "已有解决方法": ["oracle／条件门控（2608.29431 的 oracle 门控；CAST 类条件 steering）只在已知目标子集时有效"],
 "已支持的解释": ["推理类失败上的 steering 表现为全局标签偏置（2608.29431）", "行为移动不等于修复（2609.36138）"],
 "待验证解释": ["steering 只提供全局先验偏移：正确行为在实例间一致时（总是忽略线索、总是信上下文）它就是修复；正确行为依实例而定时，它只能在纠错与破坏之间交换（本地图推测）"],
 "尚未解决": "成功与失败案例来自不同任务、模型和指标，没有在同一模型上同时测纠正率与破坏率；'正确行为是否实例一致'能否预测修复比例未检验。",
 "可检验切口": "在同一模型上构造成对任务：同一能力的'实例一致'版本（如总是该忽略的线索）与'实例相关'版本（如部分样本该信线索），分别测纠正率与对原本正确样本的破坏率；对照全局 steering、条件门控、逐样本检索目标（2611.04757）。",
 "已知边界": ["成功证据多为摘要级", "推理类失败的数值部分未取到"],
 "解决状态": "机制未定",
 "查新状态": "做了定向网页检索（steering 只做全局偏移、不能修复推理错误），未检出直接研究；2611.04757（逐样本 steering 何时需要）与之相邻。",
 "与其他问题的关系": ["Q001", "Q005"]},
{"id": "Q007", "细化自": ["Q003"],
 "具体问题": "在需要多个阶段持续控制的任务（多轮中不断有新用户回合、agent 循环中有工具返回）里，短暂前缀 steering 何时足够、何时必须持续干预；持续干预又为何在多轮中累积损伤，或效果衰减、反转？",
 "宏观标签": ["前缀 steering", "多轮", "持续性"],
 "线索类型": ["作者明确的未解决问题", "跨论文矛盾"],
 "证据": [
  ev("2610.04967", "One Token Can Be Enough: Bridging Prompting and Activation Steering with Prefix Steering", [], "§6 Conclusion", "作者局限（白名单外）",
     "4 个模型、5 个任务", "干预时长与强度", None,
     "作者写明：行为实验无法区分被改的表示与生成的上下文两种机制；合适的时长与强度依任务而定，需要在更长生成和多阶段控制任务上弄清何时前缀足够、何时需持续干预", "作者局限"),
  ev("2605.10664", "Prompt-Activation Duality", ["MIT"], "§3.2、摘要", "原始实验",
     "persona vector 多轮逐 token steering", "控制方式", "相同对话",
     "标准 steering 连贯性急剧下降；GCAD 漂移 −18.6→−1.9，第 10 轮特质表达 78.0→93.1", "KV 污染为推测"),
  ev("2610.19817", "Model vs. User: Whose Values Prevail? Inference-Time Value Alignment in Multi-Turn Conversations", [], "摘要", "原始实验（机构未核实）",
     "3 个模型、2 组价值权衡", "用户与助手方向是否相反", None,
     "早期成功的 steering 几轮后衰减或反转；与基线偏向一致的一方常占上风", "仅摘要"),
  ev("2604.08169", "Activation Steering for Aligned Open-ended Generation without Sacrificing Coherence", [], "§6 Discussion", "原始实验（窗口外）",
     "Llama-3.3-70B、Qwen3.6-27B；恶意 system prompt；2 种特质；多轮", "固定系数 vs 投影目标选择性干预", None,
     "固定系数在最佳点可比，但对层与系数极脆弱；重复放大与干预选择性成反比", "作者称只测了一种失对齐来源、两种特质、两种架构")],
 "已有解决方法": ["GCAD（2605.10664）", "StTP／StMP 选择性干预（2604.08169）", "前缀 steering（2610.04967）", "DAC 随生成衰减强度（2406.17563）"],
 "已支持的解释": [],
 "待验证解释": ["KV 污染（2605.10664）", "新回合的用户内容会重新锚定模型的基线偏向（2610.19817 的观察）"],
 "尚未解决": "各方法只在单一设定下评测；新回合输入如何削弱前缀效果、持续干预的损伤是否随回合数累积，均未在同一设置下测量。",
 "可检验切口": "在同一多轮协议下，比较前缀、每回合起点注入、全程注入、选择性注入；分别测特质保持与连贯性随回合的曲线，并改变新回合内容与目标特质的冲突程度。",
 "已知边界": ["证据分散于 persona、价值与恶意 system prompt 三类"],
 "解决状态": "机制未定",
 "查新状态": "前缀 steering 作者明确列为未来工作；未进行完整查新。",
 "与其他问题的关系": ["Q003", "Q002"]},
]

p = ROOT / "研究问题.json"
d = json.loads(p.read_text(encoding="utf-8"))
ids = {x["id"] for x in NEW}
d["研究问题"] = [q for q in d["研究问题"] if q["id"] not in ids] + NEW
for q in d["研究问题"]:
    if q["id"] == "Q003":
        q["打磨状态"] = "2026-11-04 未送审：查新显示通路级问题已被 SKOP、GCAD、Memory Inception、DAC、Prefix Steering、StTP 覆盖；已细化为 Q005（推理模型审议放大 vs 锁定）与 Q007（多阶段控制下的持续性）。见 idea-stage/repe_steer_pathway_q003_20261104/"
d["推荐顺序"] = ["Q005", "Q006", "Q007", "Q002", "Q004"]
d["细化说明"] = "2026-11-04 第二轮：Q001／Q003 查新拥挤后，用最强近邻的失败条件与矛盾细化出 Q005–Q007；Q001 与 Q003 保留为上位标签。"
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", [q["id"] for q in d["研究问题"]])
