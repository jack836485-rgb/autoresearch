"""本项目候选与独立审阅的落盘工具；不执行实验。"""
import datetime
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
REVIEW = PROJECT / 'review-stage' / ROOT.name
DATA = ROOT / '候选数据.json'
STATE = REVIEW / 'REVIEW_STATE.json'
TZ = datetime.timezone(datetime.timedelta(hours=8))

BASELINES = {
 'memrl': [
  ['MemRL on ALFWorld','episodic memory、utility、runtime learning；同一文字交互 ALFWorld 任务','https://arxiv.org/abs/2601.03192','https://github.com/MemTensor/MemRL；已读取 run/run_alfworld.py、alfworld_rl_runner.py、memory_service.update_values、retrievers.py 与 rl_alf_config.yaml；API LLM/embedding，无模型训练','python run/run_alfworld.py --config configs/rl_alf_config.yaml；统一 text-only AlfredTWEnv、LLM/embedding、候选集合、k、max_steps和总调用；Linux/WSL2安装 ALFWorld/数据，CPU环境','是；源码核验，未运行'],
  ['相同 agent + semantic-only retrieval','同一记忆库与ALFWorld交互，排除模型或不同数据效果','https://arxiv.org/abs/2601.03192','同一官方 runner；已读 enable_value_driven 分支和 query retriever','相同 YAML 设 experiment.enable_value_driven=false；保留同一检索候选/k/token/轨迹获取预算','是'],
  ['相同 agent + 无记忆','ALFWorld任务的基础 ReAct；评估记忆开销是否值得','https://arxiv.org/abs/2210.03629','标准可直接本地实现：同 runner 生成调用不注入 retrieved memories；同原始few-shot、模型和工具','保留同actor输入/输出上限和工具上限；可用未花记忆构建token继续执行，但不能超过统一硬上限；无需隐藏数据/checkpoint','是'] ],
 'app': [
  ['AppWorld ReAct code agent','interactive coding agents、API tools、同一 AppWorld 任务','https://arxiv.org/abs/2407.18901','https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/react_code_agent.py，对应 SimplifiedReActCodeAgent','appworld run auto --agent-name simplified_react_code_agent --model-name {同一模型} --dataset-name dev；正式测试冻结后切 test_normal/test_challenge','是'],
  ['AppWorld full-code repair','同一环境中的整段代码生成与错误反馈修复','https://arxiv.org/abs/2407.18901','https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/full_code_agent.py，对应 SimplifiedFullCodeAgent','appworld run auto --agent-name simplified_full_code_agent --model-name {同一模型} --dataset-name dev；必须统一 API 发现与交互上限','是']],
 'maze': [
  ['ToolMaze native function calling','tool failures、dynamic replanning、相同 C/P 任务','https://arxiv.org/abs/2606.05806','https://github.com/Zhudongsheng75/ToolMaze；已读取 evaluation/scripts/run_eval.py 的 create_agent/evaluate_single_task/main 和 README','python evaluation/scripts/run_eval.py --task-category c3 --modes P0 P1 P2 P3 P4 --agent-type openai --model {同一模型} --limit {预先固定任务数}','是'],
  ['同预算 failure-aware prompting','相同工具失败设置，只提醒可能存在显式/隐式及暂时/永久失败','https://arxiv.org/html/2606.05806v1#S4','同上 runner；标准提示对照，可直接在相同 agent system prompt 写入完整提醒，不读取 perturbation 标签','复制同一配置，唯一变化为提示是否包含上述四类失败提醒；同模型、相同总调用/token/tool预算','是']],
 'tau': [
  ['官方 LLMAgent','conversational agents、dual-control、telecom','https://arxiv.org/abs/2506.07982','https://github.com/sierra-research/tau2-bench；已读取 src/tau2/agent/llm_agent.py 和 agent/README.md；当前仓库为 τ³，使用其修正后的文本 telecom，不混称原论文分数','uv sync；tau2 run --domain telecom --agent-llm {同一模型} --user-llm {固定模拟器} --num-trials {固定次数} --num-tasks {固定任务数}；自定义 agent 通过 HalfDuplexAgent.generate_next_message 注册','是'],
  ['结构化状态提示','相同对话和工具场景，排除仅增加提示格式的收益','https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/agent/README.md','标准本地对照：每轮用同一个 LLM 输出固定 JSON 的目标/已知事实/待办并作为下轮输入；不接入隐藏用户工具日志或评价','同一 LLMAgent 派生；同预算加入一份状态表，但没有本候选特有的更新机制','是']],
 'mem': [
  ['BM25 + direct reading','long-term interactive memory、retrieval、同一 LongMemEval 问答','https://arxiv.org/abs/2410.10813','https://github.com/xiaowu0162/LongMemEval；已读取 retrieval/generation.py 及 run_generation.sh；flat-bm25 分支使用 rank_bm25.BM25Okapi(doc.split(" "))，CPU 可运行，不使用 dense CUDA checkpoint','python src/retrieval/run_retrieval.py --in_file {S_cleaned} --out_dir {dir} --retriever flat-bm25 --granularity session；generation 必须 --retriever_type flat-session（若turn则flat-turn） --topk_context {k} --history_format json --useronly false --cot false --con false，并提供 --in_file/--out_dir/--model_name/--model_alias/--openai_key；不是flat-bm25。环境用CPU版PyTorch','是；Call14后纠正旧命令，不代表已运行'],
  ['相同检索 + Chain-of-Note','long-term memory 的 reading 阶段，避免用换 reader 掩盖检索或整理收益','https://arxiv.org/html/2410.10813v2#S5.SS5','同上 run_generation.py + run_generation.sh；已核验 con/con-separate 映射','锁定相同检索列表/reader；官方 con = --cot true --con false（单次输出先提证据），con-separate = --cot true --con true（每项先独立提notes再回答）；最小实验用单次con，同retriever_type flat-session/flat-turn；所有额外token/调用计费','是；Call14后纠正旧映射']],
 'ace': [
  ['官方 ACE on AppWorld','context adaptation、execution feedback、agent memory；同一 AppWorld 任务','https://arxiv.org/abs/2510.04618','https://github.com/ace-agent/ace + https://github.com/ace-agent/ace-appworld；已开主仓库和对应 AppWorld 子模块，入口仍需逐文件读后才可纳入','待核验 ace-appworld README 的实跑入口；仅有主包 ACE.run 不足以保证 AppWorld 复现','否']]
}

def now():
 return datetime.datetime.now(TZ).isoformat(timespec='seconds')

def write(path, text, description, stage='idea-discovery'):
 path.parent.mkdir(parents=True, exist_ok=True)
 path.write_text(text, encoding='utf-8')
 manifest = ROOT / 'MANIFEST.md'
 if not manifest.exists():
  manifest.write_text('# Research Output Manifest\n\n| Timestamp | Skill | File | Stage | Description |\n|-----------|-------|------|-------|-------------|\n', encoding='utf-8')
 with manifest.open('a', encoding='utf-8') as f:
  f.write(f'| {now()} | /idea-improvement-loop | {path.relative_to(PROJECT).as_posix()} | {stage} | {description} |\n')

def load():
 return json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else []

def state():
 return json.loads(STATE.read_text(encoding='utf-8'))

def save(items, s):
 s['timestamp'] = now()
 s['candidate_count'] = len(items)
 if 'target_total_passes' in s:
  prior = set(s.get('passes_at_resumption', []))
  s['new_passed_candidate_ids'] = [cid for cid in s['passed_candidate_ids'] if cid not in prior]
  s['new_passes_found'] = len(s['new_passed_candidate_ids'])
  s['requested_count_met'] = len(s['passed_candidate_ids']) >= s['target_total_passes']
 write(DATA, json.dumps(items,ensure_ascii=False,indent=2), '候选结构化数据；人读历史见候选池')
 write(STATE, json.dumps(s,ensure_ascii=False,indent=2), '当前状态与无限审阅预算', 'review')
 render(items,s)

def baseline_table(c):
 rows = c.get('baseline_rows', BASELINES.get(c['group'],[]))
 out='| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |\n|---|---|---|---|---|---|\n'
 return out + ''.join('| '+' | '.join(row)+' |\n' for row in rows)

def render(items,s):
 selected=s.get('selected_candidate_id') or '无'
 lines=['# Idea 候选池','', '> 采用 idea-candidates-template.md 结构；本文件是唯一人读候选历史。自评分是暂定排序，独立 reviewer 才能过新意门槛。未运行实验。','', '- 输入模式：`raw_idea`','- 输入论文：不适用；用户要求自行选择 baseline 的真实 failure mode。','- 时间：2026-10-09 起；所有资料限定本 slot。','- 算力约束：无训练；CPU 控制机制 + 相同模型 API 推理；金额、模型、正式样本数待实验前与用户确定。','', '## 当前选择','',f'- Reviewer 调用：`{s["reviewer_calls_used"]} / 无次数上限`',f'- 当前选中 Idea：`{selected}`',f'- 当前自评分：`{s.get("selected_self_score")}`',f'- 选择理由：{s.get("selection_reason","尚在候选生成阶段。")}',f'- 状态：`{s["status"]}`','', '### 阅读索引','', '| ID | 标题 | 自评 | 状态 | 独立审阅 |','|---|---|---|---|---|']
 for c in items:
  hist='；'.join(f'Call {r["call"]}: {r["score"]} / {r["verdict"]}' for r in c.get('reviews',[])) or '未审阅'
  lines.append(f'| {c["id"]} | [{c["title"]}](#{c["id"].lower()}) | {c["score"]} | {c["status"]} | {hist} |')
 lines += ['', '## 候选列表']
 for c in items:
  hist='；'.join(f'Call {r["call"]}：{r["score"]}/10，{r["verdict"]}，最高近邻 {", ".join(r["neighbors"])}；{r["conclusion"]}' for r in c.get('reviews',[])) or '尚未送审'
  lines += ['',f'<a id="{c["id"].lower()}"></a>',f'### {c["id"]}：{c["title"]}','',f'- 来源：`{c["route"]}`',f'- 父 Idea：`{c.get("parent","无")}`',f'- 状态：`{c["status"]}`',f'- 定位关键词：{c["keywords"]}',f'- 一句话背景：{c["background"]}',f'- 自评分：`{c["score"]}/10`',f'- 一段话概括：{c["claim"]} {c["method"]} {c["experiment"]}',f'- Story line：{c["story"]}',f'- 打分理由：{c["reason"]}',f'- Idea 生成依据：{c["sources"]}',f'- 自评分轻量新意依据：{c["novelty"]}','- 与输入论文的关系：不适用；论文是失败证据、相关工作或独立通过任务匹配要求的 baseline。',f'- 本 Idea 的独立创新点：{c["independent"]}','- Baseline 可复现性：','',baseline_table(c),f'- Reviewer 记录：{hist}',f'- 选择/修订记录：{c.get("selection_notes","未被选中；保留比较。")}',f'- 子候选：{", ".join(x["id"] for x in items if x.get("parent")==c["id"]) or "无"}']
 write(ROOT/'IDEA_CANDIDATES.md','\n'.join(lines)+'\n','完整候选池、被选中记录、审阅与血缘')

def add(candidates):
 items=load();s=state()
 for c in candidates:
  c['id']=f'IDEA-{len(items)+1:03d}'
  c.setdefault('status','available');c.setdefault('route','最高近邻不足')
  items.append(c)
 save(items,s)

def select(candidate_id=None):
 items=load();s=state();eligible=[c for c in items if c['status']=='available']
 leader=max(eligible,key=lambda c:c['score'])
 if candidate_id:
  chosen=next(c for c in eligible if c['id']==candidate_id)
  if chosen['score']!=leader['score']:
   raise ValueError('必须选择当前最高分 available 候选；同分可直接判断')
  leader=chosen
 n=s['reviewer_calls_used']+1
 leader['status']='selected';leader['selected_was_pool_leader']=True;leader['selection_notes']=f'Call {n} 选择时是 available 池最高分；同分优先证据更直接、任务更清楚的候选。'
 s.update(selected_candidate_id=leader['id'],selected_self_score=leader['score'],selected_was_pool_leader=True,selection_reason=leader['reason'],last_brief_path=str(ROOT/f'round-{n:02d}-brief.md'))
 brief=f'## 背景\n\n**定位关键词：** {leader["keywords"]}\n\n**一句话定位：** {leader["background"]}\n\n## 核心 Claim\n\n{leader["claim"]}\n\n{leader.get("evidence_detail",leader["story"])}\n\n## 方法设计的核心思想\n\n{leader["method"]}\n\n## 最小实验\n\n{leader["experiment"]}\n\n{leader.get("controls","同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。") }\n\n{baseline_table(leader)}'
 write(ROOT/f'round-{n:02d}-brief.md',brief,f'Call {n} 的四部分 brief')
 write(ROOT/'CURRENT_IDEA.md',brief,'当前候选 brief')
 # 紧接调用前持久化计数；任何失败调用也消费一次。
 s['reviewer_calls_used']=n
 save(items,s)
 return leader,brief,n

def record(n,response,agent_id):
 items=load();s=state();c=next(c for c in items if c.get('selection_notes','').startswith(f'Call {n} '))
 match=re.search(r'```json\s*(\{.*?\})\s*```',response,re.S)
 r=json.loads(match.group(1)) if match else None
 passed=bool(c.get('selected_was_pool_leader',False) and r and r['score']>7.5 and not r['fatal_blockers'])
 if r:
  c.setdefault('reviews',[]).append({'call':n,'score':r['score'],'verdict':r['verdict'],'neighbors':r['closest_neighbors'],'conclusion':r['novelty_conclusion'],'fatal_blockers':r['fatal_blockers']})
  c['status']='final' if passed else ('covered' if r['verdict']=='needs_rethink' else 'rejected' if r['verdict']=='reject' else 'needs_revision')
  s.update(last_reviewer_score=r['score'],last_verdict=r['verdict'],fatal_blockers=r['fatal_blockers'],closest_neighbors=r['closest_neighbors'],novelty_conclusion=r['novelty_conclusion'])
 else:
  c['status']='needs_revision';s['last_verdict']='malformed_response'
 if passed and c['id'] not in s['passed_candidate_ids']:s['passed_candidate_ids'].append(c['id'])
 s['reviewer_agent_ids'][f'call_{n}']=agent_id;s['last_review_path']=str(REVIEW/f'round-{n:02d}-review.md')
 write(REVIEW/f'round-{n:02d}-review.md',response,f'Call {n} reviewer 原始回复','review')
 with (REVIEW/'AUTO_REVIEW.md').open('a',encoding='utf-8') as f:
  f.write(f'\n- Call {n} / {c["id"]} / {agent_id}：'+(f'{r["score"]}，{r["verdict"]}，gate={passed}。' if r else 'JSON 无效，不能过门槛。')+'\n')
 trace=REVIEW/'.aris'/'traces'/'idea-improvement-loop'/'2026-10-09_run01'
 write(trace/f'{n:03d}-round-{n}-review.response.md',response,'完整原始 reviewer 回复','review')
 meta={'call_number':n,'purpose':f'round-{n}-review','timestamp':now(),'agent_id':agent_id,'model':'gpt-5.6-sol','reasoning_effort':'xhigh','context_policy':'fresh_zero_context','fork_turns':'none','continuation_allowed':False,'review_independence':'same-family','acceptance_status':'provisional','status':'ok' if r else 'malformed','parsed_response':r,'gate_passed':passed,'candidate_id':c['id'],'produced_artifacts':[s['last_review_path'],str(ROOT/'IDEA_CANDIDATES.md')]}
 write(trace/f'{n:03d}-round-{n}-review.meta.json',json.dumps(meta,ensure_ascii=False,indent=2),'审阅追踪元数据','review')
 events=REVIEW/'.aris'/'meta'/'events.jsonl';events.parent.mkdir(parents=True,exist_ok=True)
 with events.open('a',encoding='utf-8') as f:f.write(json.dumps({'event':'review_trace','skill':'idea-improvement-loop','purpose':f'round-{n}-review','agent_id':agent_id,'trace_path':str(trace),'status':meta['status']},ensure_ascii=False)+'\n')
 save(items,s)
 return r,passed

def prepare(candidate_id=None):
 c,b,n=select(candidate_id)
 trace=REVIEW/'.aris'/'traces'/'idea-improvement-loop'/'2026-10-09_run01'
 rubric=json.loads((trace/'001-round-1-review.request.json').read_text(encoding='utf-8'))['prompt'].split('Current four-part brief:')[0]
 anchor=(ROOT/'RAW_IDEA.md').read_text(encoding='utf-8').split('## 冻结 Problem Anchor')[1].split('## 用户覆盖技能默认值')[0]
 prompt=rubric+'\nCurrent four-part brief:\n'+b+'\nFrozen Problem Anchor and user constraints:\n'+anchor
 request={'call_number':n,'purpose':f'round-{n}-review','timestamp':now(),'tool':'spawn_agent','model':'gpt-5.6-sol','reasoning_effort':'xhigh','context_policy':'fresh_zero_context','fork_turns':'none','continuation_allowed':False,'files_referenced':[str(ROOT/f'round-{n:02d}-brief.md')],'prompt':prompt}
 write(trace/f'{n:03d}-round-{n}-review.request.json',json.dumps(request,ensure_ascii=False,indent=2),'完整 reviewer 提示','review')
 return n,c['id']
