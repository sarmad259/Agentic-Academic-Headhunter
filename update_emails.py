#!/usr/bin/env python3
"""Update targets.json with real emails and flag non-professors."""

import json

EMAIL_DATA = {
    "Zhuosheng Zhang": {"email": "zhangzs@sjtu.edu.cn", "status": "Pending"},
    "Devamanyu Hazarika": {"email": "[SKIP - now at Meta AI, not faculty]", "status": "Skip"},
    "Saining Xie": {"email": "saining.xie@nyu.edu", "status": "Pending"},
    "Dian Yu": {"email": "[SKIP - at Google Brain, not faculty]", "status": "Skip"},
    "Junyi Li": {"email": "junyili@cityu.edu.hk", "institution": "City University of Hong Kong", "country": "Hong Kong", "status": "Pending"},
    "Yijun Tian": {"email": "[SKIP - PhD student, not professor]", "status": "Skip"},
    "Jiaao Chen": {"email": "jiaaochen@gatech.edu", "status": "Pending"},
    "Md. Alamin Talukder": {"email": "alamin.cse@iubat.edu", "status": "Pending"},
    "Aditi Singh": {"email": "a.singh22@csuohio.edu", "status": "Pending"},
    "Shijie Wang": {"email": "[SKIP - PhD student, not professor]", "status": "Skip"},
    "Sinno Jialin Pan": {"email": "sinnopan@cse.cuhk.edu.hk", "institution": "Chinese University of Hong Kong", "country": "Hong Kong", "status": "Pending"},
    "Ioannis D. Apostolopoulos": {"email": "[SKIP - postdoc, not professor]", "status": "Skip"},
    "Mingchen Gao": {"email": "mgao8@buffalo.edu", "status": "Pending"},
    "Christopher D. Manning": {"email": "manning@cs.stanford.edu", "status": "Pending"},
    "Steven Bethard": {"email": "bethard@arizona.edu", "status": "Pending"},
    "Minsu Cho": {"email": "mscho@postech.ac.kr", "status": "Pending"},
    "Xuezhe Ma": {"email": "xuezhema@usc.edu", "status": "Pending"},
    "Bo Han": {"email": "bohan@riken.jp", "institution": "RIKEN AIP", "country": "Japan", "status": "Pending"},
    "Federico Bianchi": {"email": "[SKIP - postdoc, now at TogetherAI]", "status": "Skip"},
    "Patrick Lewis": {"email": "[SKIP - PhD alumni, now at Cohere]", "status": "Skip"},
    "Jialang Xu": {"email": "jialang.xu@ucl.ac.uk", "status": "Pending"},
    "Hiroaki Hayashi": {"email": "[SKIP - PhD alumni, now at Salesforce]", "status": "Skip"},
    "Chunting Zhou": {"email": "[SKIP - PhD alumni, now at Meta]", "status": "Skip"},
    "Ethan Perez": {"email": "[SKIP - PhD student, now at Anthropic]", "status": "Skip"},
    "Yuhao Zhang": {"email": "yuhao@cs.stanford.edu", "status": "Pending"},
    "Yuhui Zhang": {"email": "yuhuiz@stanford.edu", "status": "Pending"},
    "Mert Yuksekgonul": {"email": "mertyg@stanford.edu", "status": "Pending"},
    "Tegan Maharaj": {"email": "tegan.maharaj@hec.ca", "institution": "HEC Montreal", "country": "Canada", "status": "Pending"},
    "Xingyi Yang": {"email": "x3yang@eng.ucsd.edu", "status": "Pending"},
    "Jun Yu": {"email": "harryjun@ustc.edu.cn", "institution": "University of Science and Technology of China", "country": "China", "status": "Pending"},
    "Stanislaw Jastrzebski": {"email": "s.jastrzebski@uj.edu.pl", "status": "Pending"},
    "Seyed-Ahmad Ahmadi": {"email": "[SKIP - now at NVIDIA, not faculty]", "status": "Skip"},
    "Xiaolei Wang": {"email": "wangxiaolei@ruc.edu.cn", "status": "Pending"},
    "Yuan Wu": {"email": "[LOOKUP - not found publicly]", "status": "Pending"},
    "Richard Ren": {"email": "richard@safe.ai", "status": "Pending"},
    "Balint Gyevnar": {"email": "b.gyevnar@ed.ac.uk", "status": "Pending"},
    "Ze Liu": {"email": "zeliu@mail.ustc.edu.cn", "status": "Pending"},
    "Steven Basart": {"email": "sbasart@ttic.edu", "status": "Pending"},
}

with open("targets.json") as f:
    data = json.load(f)

updated = 0
skipped = 0
for prof in data["professors"]:
    name = prof["name"]
    if name in EMAIL_DATA:
        info = EMAIL_DATA[name]
        prof["email"] = info["email"]
        prof["status"] = info.get("status", "Pending")
        if "institution" in info:
            prof["institution"] = info["institution"]
            prof["university"] = info["institution"]
        if "country" in info:
            prof["country"] = info["country"]
        if info["status"] == "Skip":
            skipped += 1
        else:
            updated += 1

with open("targets.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"✓ {updated} professors updated with real emails")
print(f"✓ {skipped} flagged as Skip (PhD students / moved to industry)")
print(f"\nReady to email professors:")
for prof in data["professors"]:
    if prof.get("status") == "Pending" and prof.get("email") and "[" not in prof["email"]:
        print(f"  {prof['name']:<30} {prof['email']}")
