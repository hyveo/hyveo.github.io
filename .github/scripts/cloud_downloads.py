"""매일 아침 CurseForge 공식 API로 다운로드 수를 읽어 downloads.json에 기록하고,
디스코드 Dashboard 채널로 리포트를 보낸다. (GitHub Actions에서 실행)

필요한 시크릿
- CF_CORE_API_KEY: CurseForge Core API 키 (console.curseforge.com)
- DISCORD_DASHBOARD_WEBHOOK_URL: 디스코드 'CurseForge > Dashboard' 채널 웹훅 (없으면 전송만 건너뜀)
"""
import datetime as dt
import json
import os
import sys
import urllib.request

PROJECTS = {"centerbar": 1814948, "levelpace": 1814884, "hyveo-center": 1814965}
PATH = "public/addons/downloads.json"
KST = dt.timezone(dt.timedelta(hours=9))


def api(path):
    key = os.environ.get("CF_CORE_API_KEY", "").strip()
    if not key:
        sys.exit("CF_CORE_API_KEY 시크릿이 없어요")
    req = urllib.request.Request("https://api.curseforge.com" + path,
                                 headers={"x-api-key": key, "Accept": "application/json",
                                          "User-Agent": "hyveo-addons-bot (https://hyveo.github.io)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]


def read_counts():
    entry, betas = {}, set()
    versions = {}
    for slug, pid in PROJECTS.items():
        entry[slug] = int(api(f"/v1/mods/{pid}")["downloadCount"])
        files = api(f"/v1/mods/{pid}/files?pageSize=50")
        files.sort(key=lambda f: f.get("fileDate", ""), reverse=True)
        v = {}
        for f in files:
            ver = (f.get("displayName") or f.get("fileName", "")).replace(".zip", "").split()[-1].split("-")[-1]
            v[ver] = v.get(ver, 0) + int(f.get("downloadCount", 0))
            if f.get("releaseType") == 2:
                betas.add((slug, ver))
        versions[slug] = v
    entry["versions"] = versions
    return entry, betas


def append(entry):
    s = open(PATH, encoding="utf-8").read().rstrip()
    assert s.endswith("]\n}") or s.endswith("]}") or s.endswith("]\n}".strip()), "unexpected json tail"
    i = s.rstrip("}").rstrip().rstrip("]").rstrip()
    new = i + ",\n    " + json.dumps(entry, ensure_ascii=False) + "\n  ]\n}\n"
    json.loads(new)
    open(PATH, "w", encoding="utf-8").write(new)


def base_for(h, start):
    for r in reversed(h):
        if r["at"][:10] < start:
            return r, False
    return {}, True


def dashboard(h, betas):
    hook = os.environ.get("DISCORD_DASHBOARD_WEBHOOK_URL", "").strip()
    if not hook:
        print("DISCORD_DASHBOARD_WEBHOOK_URL 없음: Dashboard 전송 건너뜀")
        return
    d = json.load(open(PATH, encoding="utf-8"))
    names = {"centerbar": "센터바", "levelpace": "레벨페이스", "hyveo-center": "애드온 센터"}
    h = d["history"]
    last, prev = h[-1], h[-2]
    tot = lambda r: sum(r.get(k, 0) for k in names)
    sign = lambda n: f"+{n}" if n >= 0 else str(n)
    head = " · ".join(f"{names[k]} {last[k]} ({sign(last[k] - prev.get(k, 0))})" for k in names)
    desc = f"**{head} · 합계 {tot(last)} ({sign(tot(last) - tot(prev))})**\n(비교 기준: {prev['at'][:10]} {prev['at'][11:16]} 기록)\n"
    today = last["at"][:10]
    d0 = dt.date.fromisoformat(today)
    mon = (d0 - dt.timedelta(days=d0.weekday())).isoformat()
    day0, _ = base_for(h, today)
    for label, start in ((f"📅 오늘({today[5:7]}/{today[8:10]})", today),
                         (f"📆 이번 주({mon[5:7]}/{mon[8:10]}~)", mon),
                         (f"🗓 이번 달({int(today[5:7])}월)", today[:8] + "01")):
        b, partial = base_for(h, start)
        parts = " · ".join(f"{names[k]} +{last[k] - b.get(k, 0)}" for k in names)
        desc += f"\n{label}: {parts} · 합계 **+{tot(last) - tot(b)}**" + (" _(첫 배포부터)_" if partial else "")
    pv_all = prev.get("versions") or {}
    dv_all = day0.get("versions") or {}
    fields = []
    for k, name in names.items():
        v = last["versions"][k]
        pv, dv = pv_all.get(k), dv_all.get(k, {})
        rows = []
        for ver, n in v.items():
            bits = []
            if pv is not None and prev is not day0:
                if ver not in pv:
                    bits.append("새 버전")
                elif n - pv[ver] > 0:
                    bits.append(f"+{n - pv[ver]}")
            if n - dv.get(ver, 0) > 0:
                bits.append(f"오늘 +{n - dv.get(ver, 0)}")
            beta = " β" if (k, ver) in betas else ""
            rows.append(f"`v{ver}{beta}`  **{n}**회" + (f"  ({' · '.join(bits)})" if bits else ""))
        s = sum(v.values())
        if s != last[k]:
            rows.append(f"_버전별 합 {s} (전체와 {abs(last[k] - s)} 차이)_")
        fields.append({"name": f"{name} — {last[k]}회 ({sign(last[k] - prev.get(k, 0))})",
                       "value": "\n".join(rows)[:1024], "inline": True})
    payload = {"username": "CurseForge Dashboard", "embeds": [{
        "title": f"📦 CurseForge 다운로드 · {last['at'][:10]} {last['at'][11:16]}",
        "url": "https://hyveo.github.io/addons/", "color": 0x3FB950,
        "description": desc, "fields": fields,
        "footer": {"text": "아침 자동 리포트 · 리워드 포인트는 채팅에서 조회할 때만 확인돼요"}}]}
    req = urllib.request.Request(hook + ("&" if "?" in hook else "?") + "wait=true",
                                 data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "hyveo-addons-bot (https://hyveo.github.io, 1.0)"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=20) as r:
        print("Dashboard 전송:", r.status)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "record"
    if cmd == "record":
        entry, betas = read_counts()
        entry = {"at": dt.datetime.now(KST).strftime("%Y-%m-%dT%H:%M+09:00"), **entry}
        append(entry)
        json.dump(sorted(map(list, betas)), open("/tmp/betas.json", "w"))
        print(json.dumps(entry, ensure_ascii=False))
    elif cmd == "dashboard":
        betas = {tuple(x) for x in json.load(open("/tmp/betas.json"))} if os.path.exists("/tmp/betas.json") else set()
        dashboard(None, betas)


if __name__ == "__main__":
    main()
