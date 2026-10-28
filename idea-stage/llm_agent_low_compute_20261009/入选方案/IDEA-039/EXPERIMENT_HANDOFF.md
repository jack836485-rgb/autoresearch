# 实验交接：IDEA-039

Call22独立8.1/10，experiment_ready，fatal为空；完整方案见[FINAL_IDEA.md](FINAL_IDEA.md)，未运行实验。

## 任务和Claim

ALFWorld文字环境、episodic memory、credit assignment。MemRL对最终注入ID统一负更新；待验证未采用经验是否因此误弃。创新限：memory/template变量绑定、真实env.step动作匹配及回执，构成无需训练/反事实的负Q资格，不是边际因果归因。

## 最小实现

[MemRL](https://github.com/MemTensor/MemRL) runner输出最终ID与每轮动作；原actor正常JSON附memory_id/template_id/bindings，CPU实例化后对照真实动作/回执。失败时仅过滤有执行支持的负更新ID，成功更新原样。原经验文本/检索不变，可绑定模板作侧表；无模板者覆盖缺口另报，不能认为未使用。

## 公平实验与baseline

唯一定义见FINAL_IDEA §3.3：MemRL、self-report、同次数random、EmbodiSkill、MemP、无memory。固定库Q消融与强方法保留编辑的原生模式分开；同初始信息、actor/embedding、task/seed、few-shot、k=3、memory token和总预算。所有构建、反思、修订、embedding和actor成本计入；不给某组免费元数据。

入口：MemRL python run/run_alfworld.py --config configs/rl_alf_config.yaml。EmbodiSkill python tasks/run_epochs.py --task alfworld --skill_module embodiskill --agent_model {共同actor} --agent_api_type openai --skill_model {共同反思模型} --skill_api_type openai --max_trials {cap} --num_epochs {共同} --train_shuffle_seed 42 --output_dir {slot}。

MemP已读Memory/build/retrieve/update及llm_api；原online actor没有传args.model且覆盖凭据/例子路径有错，不能原样运行。用共同TextWorld runner接公开Memory组件、显式传共同actor、按API_KEY/API_BASE_URL/MODEL_NAME设构建模型和embedding，修正路径；保持原方法，不引入额外策略。

## 最早止损

先独立盲标是否实际落实建议，模型自报不是真值。没有明显未采用误负、模板覆盖低、绑定漏掉泛化使用、random或self-report同效，则停止。真正做过的正确指导仍可能被全局失败误罚，本门不解决所有信用分配。

主指标held-out成功/后续误弃；次指标采用识别精确率/召回、未采用负更新率及完整token/调用/费用。所有任务在成功率分母，不只挑可绑定者。

## 实验前待用户定

actor/embedding/反思模型快照、API金额、task数、重复seed与action cap。本轮无训练、未启动API实验、未租GPU。API actor+CPU TextWorld与绑定验证可使本地GPU需求为零；复现adapter尚未实跑。