## 背景

**定位关键词：** constraint-aware planning；plan repair；TravelPlanner

**一句话定位：** 规划agent修复一个预算或住宿错误时，怎样避免破坏先前已经满足的饮食、住宿和路线约束。

## 核心 Claim

TravelPlanner原文报告同时跟踪全局多约束困难。公开CORAL在补齐cuisine后为降预算删travel-day meals并替换酒店，这些实际操作可能移除某个cuisine的唯一见证或改变最低住宿要求；只证明失败可达，不证明发生率。主张一种局部修补单独看似合理，却必须和另一个槽位的支持转移一起才合法：CPU记录已满足约束的可见支持，找出候选编辑所移除的最后见证，并围绕它构建小型联合修补，再验整个候选，而不是每次都接受单编辑或每步要求永不暂时违反。

同时多约束失败已有证据，代码显示局部降价可删除既有支持；逐项修补可能产生来回摆动，强拒绝又可能堵住需要两步联合修改的路径；用被删最后见证引出相关候选槽位，将联合变更整体提交；若同预算比随机同大小邻域更少摆动且最终成功更高才支持。

## 方法设计的核心思想

首版用官方sole-planning可见reference_information，不做额外城市检索；共享同一原actor从raw query提取的约束和候选表，不读取隐藏local_constraint/参考完整plan。输入初始结构化行程与当前违约；CPU为cuisine、restaurant distinctness、hotel属性/连续住宿、预算等已支持约束计算见证或数值依赖。原actor提出局部修改；若它删除最后一个required-cuisine见证或影响已满足住宿条件，就把相关可替代槽位加入小邻域，固定其它slots，在最多3个slot的联合候选中求低改动可行修补。允许联合候选构造的中间状态暂时违约，只在最终whole-plan公开规则检查后提交；找不到则扩大下一actor回合或返回未解决，不宣称无解。CPU不更改用户硬要求，不私下松budget，不预测不可见记录。SAT/CSP与neighborhood search是成熟原语，增量限agent提出的单修补与被破坏支持之间的转换和同预算诊断。

## 最小实验

TravelPlanner原始sole-planning train/dev诊断真实修复序列：某约束通过→修另一项→原约束再次失败。统一候选池/原始query解析、actor/validator、CPU限时/总token/调用预算；比较官方ReAct/Reflexion、已核验CORAL、单编辑修补＋全局验后反馈、拒绝任何破坏已满足约束的单编辑、同3-slot随机邻域、支持见证定向联合邻域。保留CORAL原策略与原全局评分，不给主方法隐藏oracle；原CORAL无actor，不人为塞强模型，零模型成本照实报告。主指标最终all-constraints pass、修复摆动次数与完整成本；支持指标定向邻域相对随机同大小/单编辑的差别。若全局验单编辑已足够、单编辑拒绝不陷入僵局、自然repair regressions少、或全池标准CSP重建更便宜，则停止。主结论不外推到two-stage检索或真实旅行建议。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| TravelPlanner ReAct/Reflexion sole-planning | 同原始规划任务、同可见候选池 | https://arxiv.org/abs/2402.01622 | https://github.com/OSU-NLP-Group/TravelPlanner；sole_planning.py parser与Planner/ReactPlanner/Reflect入口已读，reference_information是此模式合法输入 | cd tools/planner；python sole_planning.py --set_type validation --output_dir {slot} --model_name {共同API支持模型} --strategy react（或reflexion）；统一总预算，原脚本重试/后处理费用也计入 | 是；未实跑 |
| CORAL局部repair | 同TravelPlanner已公开CPU局部修复强baseline | https://github.com/ChouYuanjue/coral-travel-planner | 已打开真实TravelPlannerGreedySolver.plan_query/_repair_plan和run_travelplanner_planner.py；repo以原raw query解析，oracle-fields默认为false | pip install -e .；python scripts/run_travelplanner_planner.py --split validation --method coral --repo-root {TravelPlanner} --output-dir {slot}；禁用--oracle-fields，先确认提供候选与主方法同sole reference scope；官方evaluator只离线评分 | 是；源码核验未实跑 |
| 单编辑＋全局反馈 | 强便宜既有范式 | 完整本地标准规范 | 同actor每轮只提交一个slot修改，CPU按全部共同显式约束检查并反馈，允许后续修复刚破坏约束 | 同候选/约束/预算，不提供hidden evaluator信息 | 是 |
| 严格单编辑保持 | 排除只保护已满足约束 | 完整本地标准规范 | 任何单编辑导致原已满足显式约束失败便不提交，actor另选单编辑；不可借此降低任务成功分母 | 同规则/信息/调用预算 | 是 |
| 随机同大小联合邻域 | 排除多改几个slot即可 | 完整本地标准规范 | 与主方法同最多3个slots、相同有限候选与CPU search cap，均匀选同数量slot而非按见证；同whole-plan检查 | 同actor proposals/种子/预算；未找到保持未解决 | 是 |
