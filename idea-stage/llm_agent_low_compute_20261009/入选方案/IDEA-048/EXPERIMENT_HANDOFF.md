# 实验交接：IDEA-048

独立8.0/10，无fatal；全文见[FINAL_IDEA.md](FINAL_IDEA.md)。

## 定位与主Claim

data wrangling；execution feedback；data provenance。

可能的自然错误：在原df算mask，排序并reset_index后旧整数标签被重新使用，再套旧mask。代码可跑、dtype/长度相同，却筛另一批行。这个pandas语义后果可推导；是否在DA-Code自然agent轨迹频繁出现仍需盲标，不能由RADAR总体静默错误率替代。

我们保留每个bool对应的来源行，跟随纯行变换维护对应关系。应用mask时比较该bool原来源和实际目标，给首个可见错配。默认原actor修代码；纯行重排时按ID重附可作单独消融，未知出处或值已改变不自动修。

## 最小实现

已读DA-Agent、PythonController、DS-STAR run/coder/debug/verify/router与LLM helper。新增仅支持操作的CPU追踪和反馈；API actor无需GPU。DS-STAR实际debug_round有正确拼写，guidelines.txt源码会无条件读取，需准备同格式说明；LLM helper未统一总token和采样，实验需调用边界统一计账与参数，不能原样声称公平。

## 实验与同预算baseline

先发现自然错误且能与合法alignment区别，再验证行来源证据能否比shape/index或简单重算更好。

冻结DA-Code公开CSV DW/DM/EDA子集，排除ML/重视觉任务。筛选依公开任务与框架支持，不按主方法结果挑任务。dev冻结支持操作，held-out盲标自然mask复用及误筛；所有不支持任务仍在整体成功分母。原始任务评分与配对错误前缀诊断分开。

唯一baseline规范见全文§3.3。

## 止损及待定参数

自然错配存在，身份检测准确且比廉价控制/DS-STAR改善同预算任务才继续。总是重算已等效、错误罕见、主要操作不支持、误报合法alignment或追踪比重算更贵则停止。

初版行变换覆盖很窄，自然频率可能低。追踪ID不能替代语义意图；位置选择/合法键对齐必须排除。改列值后旧谓词是否有效不在当前保证。简单重算可能始终更便宜，必须以它为硬停止对照。

actor快照、正式金额、task数、seed和cap在实验前确定。本轮没有跑模型实验。
