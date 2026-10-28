# -*- coding: utf-8 -*-
"""对 批量读取论文.py 落盘的正文 JSON 作者区做白名单／QS 前 50 关键词初筛，结果写文件，作者区不进上下文。

这是初筛不是资格判定：命中条目在被正式引用前仍需核对作者–机构对应；未命中或缺作者区的条目单独列出供人工检查。
用法：python -X utf8 机构初筛.py <正文目录> <输出.json>
核实被引论文：python -X utf8 机构初筛.py <正文目录> --show <arXiv ID> ...（只打印命中机构名前后的短片段）
"""
import json, re, sys
from pathlib import Path
WL = {
 "Google": r"Google|DeepMind", "Microsoft": r"Microsoft|MSRA", "Meta": r"\bMeta\b|FAIR|Facebook",
 "Amazon": r"Amazon|\bAWS\b", "Apple": r"\bApple\b", "NVIDIA": r"NVIDIA|Nvidia", "IBM": r"\bIBM\b",
 "Adobe": r"Adobe", "OpenAI": r"OpenAI", "Anthropic": r"Anthropic",
 "Alibaba": r"Alibaba|Qwen|Tongyi|DAMO|Amap|AMAP|Taobao|Alimama|Ant Token Hub|Token Hub",
 "ByteDance": r"ByteDance|Bytedance|Seed\b|TikTok|Douyin", "Tencent": r"Tencent|Hunyuan|WeChat",
 "Baidu": r"Baidu", "Huawei": r"Huawei|Noah", "Ant Group": r"Ant Group|Ant Research|AntGroup|inclusionAI|Ant International",
 "Kuaishou": r"Kuaishou|Kwai", "SenseTime": r"SenseTime", "DeepSeek": r"DeepSeek",
 "Moonshot": r"Moonshot|Kimi", "Zhipu": r"Zhipu|Z\.ai|\bZ\.AI", "MiniMax": r"MiniMax",
 "xAI": r"\bxAI\b", "Mistral": r"Mistral", "Cohere": r"Cohere", "Sakana": r"Sakana",
 "Thinking Machines": r"Thinking Machines", "Liquid AI": r"Liquid AI", "Reka": r"\bReka\b",
 "Nous": r"Nous Research", "World Labs": r"World Labs", "Physical Intelligence": r"Physical Intelligence",
 "Black Forest Labs": r"Black Forest", "Runway": r"\bRunway\b", "Databricks": r"Databricks|Mosaic",
 "Salesforce": r"Salesforce", "Ai2": r"Allen Institute|\bAI2\b|\bAi2\b", "BAAI": r"\bBAAI\b|Beijing Academy of Artificial",
 "上海AI实验室": r"Shanghai Artificial Intelligence Lab|Shanghai AI Lab|Shanghai AI Laboratory",
 "StepFun": r"StepFun", "ModelBest": r"ModelBest|OpenBMB",
}
QS = {
 "MIT": r"Massachusetts Institute of Technology|\bMIT\b", "Imperial": r"Imperial College", "Stanford": r"Stanford",
 "Oxford": r"Oxford", "Harvard": r"Harvard", "Cambridge(Univ)": r"University of Cambridge", "Caltech": r"Caltech|California Institute of Technology",
 "ETH": r"ETH Z", "UCL": r"University College London|\bUCL\b", "NUS": r"National University of Singapore|\bNUS\b",
 "HKU": r"(?<!Chinese )University of Hong Kong|\bHKU\b", "NTU(SG)": r"Nanyang", "PKU": r"Peking University|\bPKU\b", "Tsinghua": r"Tsinghua",
 "UPenn": r"University of Pennsylvania|UPenn", "Cornell": r"Cornell", "Yale": r"\bYale\b", "CUHK": r"Chinese University of Hong Kong|CUHK",
 "UNSW": r"UNSW|New South Wales", "JHU": r"Johns Hopkins", "Berkeley": r"Berkeley", "EPFL": r"EPFL|Polytechnique F", "Melbourne": r"University of Melbourne",
 "UChicago": r"University of Chicago", "TUM": r"Technical University of Munich|Technische Universit.t M", "Fudan": r"Fudan", "Princeton": r"Princeton",
 "Sydney": r"University of Sydney", "ANU": r"Australian National University", "McGill": r"McGill", "Monash": r"Monash", "Toronto": r"University of Toronto",
 "HKUST": r"HKUST|Hong Kong University of Science and Technology", "PSL": r"PSL|Paris Sciences", "Edinburgh": r"Edinburgh", "SJTU": r"Shanghai Jiao Tong|SJTU",
 "KCL": r"King's College London|King’s College London", "SNU": r"Seoul National", "UTokyo": r"University of Tokyo|The University of Tokyo", "Manchester": r"University of Manchester",
 "UQ": r"University of Queensland", "Yonsei": r"Yonsei", "Columbia": r"Columbia University", "IP Paris": r"Polytechnique de Paris",
 "Northwestern": r"Northwestern University", "UBC": r"University of British Columbia", "ZJU": r"Zhejiang University", "Delft": r"Delft", "UCLA": r"UCLA|Los Angeles", "PolyU": r"Polytechnic University|PolyU",
}
d = Path(sys.argv[1])
if len(sys.argv) > 2 and sys.argv[2] == "--show":
    for aid in sys.argv[3:]:
        files = sorted(d.glob(f"{aid}v*正文.json"))
        if not files:
            print(aid, "未找到正文"); continue
        j = json.loads(files[0].read_text(encoding="utf-8")); p = j.get("paper") or {}
        blk = p.get("author_block") or j.get("text", "")[:4000]
        found = []
        for name, rx in {**WL, **QS}.items():
            spans = [blk[max(0, m.start() - 30):m.end() + 30].strip() for m in list(re.finditer(rx, blk))[:3]]
            if spans:
                found.append(f"{name}「" + "」「".join(spans) + "」")
        # "internship""work done while" 之类弱关联需人工判断，不算署名。
        print(aid, p.get("arxiv_version_date"), "；".join(found) or "未命中")
    sys.exit(0)
res = []
for f in sorted(d.glob("*正文.json")):
    j = json.loads(f.read_text(encoding="utf-8"))
    p = j.get("paper") or {}
    # 作者区缺失时退回正文前部，覆盖机构写在脚注里的情况。
    blk = (p.get("author_block") or "") + " " + (j.get("text", "")[:4000] if not p.get("author_block") else "")
    res.append({"file": f.name, "title": p.get("title"), "date": p.get("arxiv_version_date"),
                "hits": [k for k, rx in WL.items() if re.search(rx, blk)],
                "qs": [k for k, rx in QS.items() if re.search(rx, blk)],
                "author_block_len": len(p.get("author_block") or ""), "error": j.get("error")})
Path(sys.argv[2]).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
unmatched = [r["file"] for r in res if not r["hits"] and not r["qs"]]
print(len(res), "篇；白名单命中", sum(1 for r in res if r["hits"]), "；仅 QS", sum(1 for r in res if r["qs"] and not r["hits"]),
      "；读取错误", sum(1 for r in res if r["error"]), "；无作者区", sum(1 for r in res if not r["author_block_len"]))
print("未命中（需人工看作者区或 PDF 首页）：", " ".join(unmatched[:40]) + (" …" if len(unmatched) > 40 else ""))
