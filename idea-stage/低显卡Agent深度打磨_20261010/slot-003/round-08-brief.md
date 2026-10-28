## 背景

**定位关键词：** LLM software agents, procedural memory, verification allocation, program repair

相同经验可能使多个代码候选共享错误。一个公共检查即使让所有候选同向失败、不能改变现有排序，仍可能给修复器提供能生成新正确候选的证据。排序价值与修复价值不同；共享错误的自然发生率及净收益尚未验证。

当前目标及演化依据：聚焦经验引发共同错误时检查预算如何分配，把高一致省验证的目标改为可改变代码池的验证价值。不是给固定池选择器补一个repair模块：核心比较是共同公共检查虽无排序增益却可能有修复增益时，是否应改变获取检查的准则。保持软件agent/冻结actor/全成本，不扩成医疗VQA。

https://arxiv.org/html/2608.11888v1：§IV-C自然相关技能可能使实现沿错误默认/模板执行；这支持共同错误假设的来源，但没有证明多个候选共享同一错误。
https://arxiv.org/html/2607.20950：§2.1固定代码集合；§2.2/4.1明确同方向共享检查不能改变winner，EVSI按最终选择价值评价；§5.2无correct候选时selector无法创造答案。固定池前提成立时不是缺陷，本方向改变terminal动作允许repair。
https://arxiv.org/html/2609.19515：VRR已经Verify-Repair-Reselect、保留winner并条件生成三种修复/新方法；§3.3额外验证分配仍优先可改变排序的entries，§3.4再根据低score/Unknown触发repair。共同错误修复、反复验证不是空白。

## 核心 Claim

待验证：在自然程序经验造成候选共同错误的冻结软件agent中，公共检查对现有候选排序的价值可以接近零，而对生成可修复新候选的价值非零。以检查反馈后允许的最优“保留原候选或修复”行为估计检查价值，可比仅按改变排序分配同一预算减少共同错误；若完整VRR或普通公共test-and-repair已等效，则独立机制不成立。

## 方法设计的核心思想

固定同一次初始代码集合和当前经验库。检查菜单仅来自当前公开仓库已有测试及公开接口/编译检查，隐藏SWE-bench test_patch/FAIL_TO_PASS及oracle终态不在运行时菜单。每个公共检查都保留真实输出，候选共同失败不视为排序无用而自动跳过。训练/dev在同失败类记录“该检查产生的可见反馈→冻结actor修复→公开复查→仅离线终态”的真实结果与费用，估计检查后最佳可达保留/修复价值；不把LLM预测值称真实posterior。不加因果graph、hash/新flag。运行时用公开错误类、候选对同public检查的行为预测和剩余预算，比较立即交付、为排序购买检查、为修复购买检查；修复分支允许只挑一个候选进行一次定额修复并保留原winner重新选。两种检查选择器都获得相同repair器、公共菜单与修复次数上限，因此差异是买哪条证据，而非一方没有修复。输入/检查无支持时按同普通公开测试顺序，不赋予oracle预测。任何检查不能保证整个任务正确；只用公开回执推动生成，hidden outcome仅开发估计器/离线评价。

最高近邻及差别：BoE已budgeted signed shared evidence及EVSI；VRR已公共检查、unknown、repair与reselection；Self-Debugging/Reflexion已有执行反馈修复，MBR-EXEC/MPSC已有执行共识。当前剩余差别是获取检查时直接计入其对共同错误修复的可达价值，而不是事后给排序证据加修复；该准则仍可能是终端action含repair的标准value-of-information直接适配。未充分排除，不标available。

## 最小实验

首先在SWE-bench公开train/dev的共同issue/base_commit上用同一冻结actor和自然失败经验生成固定N候选，诊断共同错误是否出现且需要公共测试才发现；不人工制造恶意skills或修改官方test任务。运行时只issue、base repo及真实可见执行日志；hidden test_patch和终态只official harness离线评价。公共test菜单由base repo实际tests/文档运行命令确定，不从target补丁或FAIL_TO_PASS选择，未来逐repo安装与测试菜单合法性待核实，不能称已可运行完成。比较不追加检查、公共固定顺序test-and-repair、排序EVSI+同repair、修复价值+同repair、VRR完整标准适配；另统一随机检查+repair。共享初始pool、actor/decoder、经验body、修复次数/单次tokens、check菜单和可见feedback、总API+CPU预算；估计数据、库构建、baselinecriteria/judge、check执行、错误解析、修复/复查/重新选择全部计。报告最终resolved/全部任务、全部费用、公共检查率、共同检查失败/全部检查、共同失败后新增正确候选/有共同失败任务（仅offline定义）、选择已正确winner后误改坏比例及无支持率。强控制将同实际check ledger给两种acquisition控制器，展示差异来自公共检查选取，不能让提案有更多信息；完整VRR按相同总预算而非无额外模型账。若自然共同经验错不存在、普通test-and-repair/完整VRR等效、修复成功率不足、或估计/检测成本抵掉收益，则推翻。N、repo子集、publicmenu与budget、model、globalrepair价值估计参数留实验阶段待确认。当前不运行。

基线定义/复现：[{"name": "SWE-bench基础环境及隐藏评价分离", "paper_url": "https://github.com/SWE-bench/SWE-bench", "code_url": "https://raw.githubusercontent.com/SWE-bench/SWE-bench/main/swebench/harness/run_evaluation.py", "reproduction": "已亲读official harness读test_patch进行offline验证；runtime不输入test_patch/FAIL_TO_PASS。未来CPU docker repo环境和公共base tests需按repo官方安装；无下载/执行，入口可核验不等于所有任务可运行。", "controlled_parameters": "相同issue/base commit、actor/decoder/CPU和总费用", "extra_costs": "镜像/安装/CPU测试及API全部计"}, {"name": "BoE式排序价值公共测试选择+同修复器", "paper_url": "https://arxiv.org/html/2607.20950", "code_url": null, "reproduction": "完整标准适配：固定pool、公共检查菜单、dev估计其对winner变化及最后交付正确率的收益/成本，依此选检查；所有观察交同修复器。原VQA大模型和设计cost不当软件baseline官方分数。", "controlled_parameters": "公共menu/估计数据、同repair次数/actor、总预算", "extra_costs": "训练估计与全部检查/repair/reselect"}, {"name": "VRR和普通公开test-and-repair参考实现", "paper_url": "https://arxiv.org/html/2609.19515", "code_url": null, "reproduction": "原文§3 Algorithm1、§3.3–3.7有完整生成criteria、初判、additionalranking checks、低score/Unknown触发winner/runner/new approach修复、公开screen并同criteriareselect定义；本地按完整标准定义同API实现，尚未找到/核实作者官方code，不称官方复现。普通test-and-repair固定公开测试顺序，将首个真实失败反馈给actor一次定额修复，保留原候选复查后唯一提交。", "controlled_parameters": "同pool/模型/解码/总预算、同repair上限", "extra_costs": "criteria/评审/全部三种proposal/复查和重选，普通基线同计"}]
