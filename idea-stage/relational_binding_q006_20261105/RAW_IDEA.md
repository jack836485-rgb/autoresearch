# 输入问题卡

## 来源
- 地图：`path-stage/GUI_Agent研究地图_20261104/`（§Q006、`研究问题.json` 中 `Q006`）；检索 2026-11-04，窗口 2026-05-04 至 2026-11-04
- 用户指令（2026-11-05 晚）：按推荐顺序把其余卡各打磨多轮

## 具体问题
GUI grounding 在标准基准上高分，但遇到关系型空间指令（左右、包含、列表序号、遮挡等）时大幅崩溃；崩溃发生在关系解析、锚点定位还是坐标解码，什么训练信号能教会关系绑定？

## 关键证据
| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| GUI-Primitives: Diagnosing Spatial Reasoning Failures in Vision-Language GUI Grounding（非白名单/未核实） | https://arxiv.org/abs/2608.21832 | 最强 Claude Opus 4.7 清洗核心集 32.4%，人类 96.9%；Qwen2.5-VL-7B 24.9%；OS-Atlas-Base-7B 10.8% 高于同底座 Qwen2-VL-7B 4.9%；空白画布使 Qwen2.5-VL-7B 22.0%→6.5% | 未覆盖 UI-TARS-1.5、GUI-Owl、GTA1 等新 GUI 专训模型；人机协议不完全匹配 |
| GUI-Perturbed: Domain Randomization Reveals Systematic Brittleness in GUI Grounding Models（非白名单/未核实） | https://arxiv.org/abs/2604.14262 | 关系型指令使准确率降 27–56 pp；rank-8 LoRA 加增广数据反而退化 | 窗口外（2026-04）；仅摘要 |
| How Many Pixels Is a Digit Worth? Place-Aware Coordinate Entropy for GUI Agent Confidence Estimation（CUHK） | https://arxiv.org/abs/2609.24277 | 单数位熵 AUROC：个位 0.65、十位 0.77、百位 0.82 | 置信度估计，不直接解释关系崩溃 |

打磨阶段补读：GUI-Primitives 代码与数据公开（github.com/Abrar2652/gui-primitives，HF kagnlp/gui-primitives），994 个对比指令对、七种关系，每对固定截图与锚点、只改关系词，目标在两个指定候选间移动；GUI-Perturbed 代码与数据公开（github.com/ManifoldRG/GUI-DR，HF figai/GUI-Perturbed，含其 LoRA 微调的 UI-TARS-1.5-7B）。

## 已有解决方法与剩余边界
- 已有解决方法：交互式光标搜索 GUI-Cursor（arXiv:2509.21552，窗口外）；不确定性驱动 zoom（AutoFocus 等）；小目标 token 预算分析（arXiv:2610.09313）
- 尚未解决：崩溃层级未分离；新一代 GUI 专训模型未被这两份关系评测覆盖。

## 可检验切口与查新状态
- 可检验切口：固定截图与锚点，分别探测关系解析、锚点定位、坐标解码的正确性，定位崩溃层级。
- 查新状态：反证检索发现 GUI-Perturbed 与 GUI-Cursor，标为“现象已有两篇独立报告”

## 问题锚点（Problem Anchor）
- **起点问题**：GUI grounding 模型在标准基准上高分，遇到关系型空间指令时大幅崩溃；需要定位崩溃层级并找到能教会关系绑定的训练信号。
- **初始任务与评测**：GUI-Primitives（七种关系、对比对、点在框内准确率）；GUI-Perturbed；ScreenSpot 系列（检查常规精度不下降）。
- **瓶颈与证据边界**：两份报告都只到现象；GUI-Perturbed 中 rank-8 LoRA + 增广数据反而退化；新一代 GUI 专训模型覆盖不全。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；付费 API 1000 元以内；token 资源稀缺。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次判定三项都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断。
