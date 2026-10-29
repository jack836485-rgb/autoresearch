# -*- coding: utf-8 -*-
"""对已读取的 v1 正文 JSON 作者区做白名单关键词初筛；仅供人工核对，不是资格判定。"""
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
 "MIT": r"Massachusetts Institute of Technology|MIT", "Imperial": r"Imperial College", "Stanford": r"Stanford",
 "Oxford": r"Oxford", "Harvard": r"Harvard", "Cambridge(Univ)": r"University of Cambridge", "Caltech": r"Caltech|California Institute of Technology",
 "ETH": r"ETH Z", "UCL": r"University College London|UCL", "NUS": r"National University of Singapore|NUS",
 "HKU": r"University of Hong Kong|HKU", "NTU(SG)": r"Nanyang", "PKU": r"Peking University|PKU", "Tsinghua": r"Tsinghua",
 "UPenn": r"University of Pennsylvania|UPenn", "Cornell": r"Cornell", "Yale": r"Yale", "CUHK": r"Chinese University of Hong Kong|CUHK",
 "UNSW": r"UNSW|New South Wales", "JHU": r"Johns Hopkins", "Berkeley": r"Berkeley", "EPFL": r"EPFL|Polytechnique F", "Melbourne": r"University of Melbourne",
 "UChicago": r"University of Chicago", "TUM": r"Technical University of Munich|Technische Universit.t M", "Fudan": r"Fudan", "Princeton": r"Princeton",
 "Sydney": r"University of Sydney", "ANU": r"Australian National University", "McGill": r"McGill", "Monash": r"Monash", "Toronto": r"University of Toronto",
 "HKUST": r"HKUST|Hong Kong University of Science and Technology", "PSL": r"PSL|Paris Sciences", "Edinburgh": r"Edinburgh", "SJTU": r"Shanghai Jiao Tong|SJTU",
 "KCL": r"King's College London|King’s College London", "SNU": r"Seoul National", "UTokyo": r"University of Tokyo|The University of Tokyo", "Manchester": r"University of Manchester",
 "UQ": r"University of Queensland", "Yonsei": r"Yonsei", "Columbia": r"Columbia University", "IP Paris": r"Polytechnique de Paris",
 "Northwestern": r"Northwestern University", "UBC": r"University of British Columbia", "ZJU": r"Zhejiang University", "Delft": r"Delft", "UCLA": r"UCLA|Los Angeles", "PolyU": r"Polytechnic University|PolyU",
}
d = Path(sys.argv[1]); res = []
for f in sorted(d.glob("*v1正文.json")):
    j = json.loads(f.read_text(encoding="utf-8"))
    p = j.get("paper") or {}
    blk = (p.get("author_block") or "") + " " + (j.get("text", "")[:4000] if not p.get("author_block") else "")
    hits = [k for k, rx in WL.items() if re.search(rx, blk)]
    qs_hits = [k for k, rx in QS.items() if re.search(rx, blk)]
    res.append({"id": f.name.split("v1")[0], "title": p.get("title"), "date": p.get("arxiv_version_date"),
                "hits": hits, "qs": qs_hits, "author_block_len": len(p.get("author_block") or ""), "error": j.get("error")})
Path(sys.argv[2]).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(res), "with hits", sum(1 for r in res if r["hits"]), "qs only", sum(1 for r in res if r["qs"] and not r["hits"]), "no author block", sum(1 for r in res if not r["author_block_len"]))
