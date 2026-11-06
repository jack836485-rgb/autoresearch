# 审查记录

- Call 1（常规，effort high）：IDEA-002，4.5/10，needs_rethink，贡献三项 {'importance': 6.0, 'novelty': 5.5, 'effectiveness': 4.5}，可行性 pass，Gate 结果 failed。主贡献是'跨尺度扩散OPD伪影部分来自教师在学生状态上不可靠'的认识，加上用自适应重加噪保留双分支CFG的工具。重要性有限：GFD学生部署时仍带w=2的CFG并做了w扫描，w条件化折叠蒸馏可廉价保留可调引导，负提示价值未证。新颖度有限：重加噪到扩散边缘分布是DMD/VSD的核心思想，按状态选噪声级有Time-Shift Sampler先例，Any-OPD已有噪声-去噪投影，教师状态臂即离策略KD。
