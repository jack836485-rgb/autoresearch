# OPD 检索

检索大语言模型 on-policy distillation 方向时读取本文件。默认时间和机构条件仍由 `SKILL.md` 决定。

## 主题判定

核心对象是：学生生成当前策略的轨迹或访问状态，教师在这些状态上提供蒸馏监督，学生据此更新。教师可以是外部模型、自身快照、EMA 或获得特权上下文的自身；监督可以涉及 token 分布、教师续写或与该训练过程直接相关的表示。

纳入 OPD 方法、机制分析、训练系统和直接使用 OPD 的语言模型应用。明确主要研究贡献与 OPD 的关系，不能因为摘要、相关工作或实验基线中出现 OPD 就计入。混合／离策略变体如果直接研究 OPD 的采样与监督问题，应标注实际策略形式；不能把纯离线教师数据 SFT 写成 OPD。

研究 OPD 教师反馈替代形式的论文，例如黑盒 rubric-based OPD，可以作为该方向的直接扩展收录，但标明其监督方式，不能写成与 token 级 KL 蒸馏相同的机制。

仍以语言模型为训练对象。视觉语言、语音语言、扩散语言模型和语言智能体可以纳入并标明类型；纯图像、视频或 3D 生成网络的同名 OPD 不自动属于大语言模型方向。

## 查询展开

- 主词：`on-policy distillation`、`on policy distillation`、`on-policy self-distillation`、`OPD`、`OPSD`、`multi-teacher on-policy distillation`、`MOPD`。
- 补漏词：`student-generated trajectories`、`student-induced states`、`teacher continuations`、`privileged context`、`self-distillation`、`reverse KL`、`generalized knowledge distillation`。与 `language model`／`LLM`／`VLM`／`language agent` 组合；这些词只用于发现，最终读方法确认采样和监督关系。
- 子问题：教师信号与选择、多教师合并、自蒸馏与特权信息、散度／熵／长度偏差、数据与课程、跨 tokenizer、rollout 复用与系统效率、与 RLVR 的组合。

先使用完整术语，再用实际发现的方法名和论文引用补漏。OPD 缩写在不同领域会有其他含义；标题相符也需要核实训练对象。

## 数量与复用

用户要求 N 篇时，N 指去重后已核实符合条件的作品数。原始命中、待核实、仅引用 OPD 的邻近工作不占名额。候选总数通常大于 N，按核实进展继续扩大候选，不为凑数放宽主题或机构。

同一会话中已经读取并核实的记录可以复用；时间窗口或白名单修改后重新应用这些条件，不重复下载同一原作。元数据与原文标题不同，优先采用原文标题，以 arXiv ID 识别作品；变体或版本不另算一篇。同样的 MOPD、COPSD 等简称可能分别代表不同工作，保留完整标题与 ID 后再判断是否为同一篇。
