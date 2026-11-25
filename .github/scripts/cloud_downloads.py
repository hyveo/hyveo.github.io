"""매일 아침 CurseForge 공식 API와 공개 파일 목록으로 다운로드 수를 읽어 downloads.json에 기록하고,
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
FILES_PATH = "public/addons/files.json"
TYPE_KO = {"R": "R", "B": "B", "A": "A"}
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


def version_fields(h, names):
    last = h[-1]
    vers = last.get("versions")
    latest = json.load(open("/tmp/latest.json")) if os.path.exists("/tmp/latest.json") else {}
    pv = next((r["versions"] for r in reversed(h[:-1]) if r.get("versions")), {})
    meta = json.load(open(FILES_PATH, encoding="utf-8")).get("files", {}) if os.path.exists(FILES_PATH) else {}
    fields = []
    for k, name in names.items():
        rows = []
        f0 = latest.get(k)
        if f0:
            when = dt.datetime.fromisoformat(f0["at"].replace("Z", "+00:00")).astimezone(KST).strftime("%m/%d %H:%M")
            rows.append(f"최신: **{f0['name']}** ({'B' if f0['beta'] else 'R'}, {when})")
        if vers and k in vers:
            for v, n in vers[k].items():
                diff = n - pv.get(k, {}).get(v, 0)
                m = meta.get(k, {}).get(v, {})
                tag = f" {TYPE_KO.get(m.get('type'), '')} · {m['uploaded'][5:10].replace('-', '/')}" if m else ""
                rows.append(f"`v{v}`{tag}  **{n}**회" + (f"  (+{diff})" if diff else ""))
        else:
            rows.append("버전별 숫자를 읽지 못했어요")
        fields.append({"name": name, "value": "\n".join(rows)[:1024], "inline": True})
    return fields


def site_files(pid):
    """curseforge.com 공개 파일 목록(로그인 불필요)이 쓰는 JSON. 버전별 totalDownloads가 Author Console과 같다."""
    out, page = [], 0
    while True:
        req = urllib.request.Request(
            f"https://www.curseforge.com/api/v1/mods/{pid}/files?pageIndex={page}&pageSize=50&removeAlphas=false",
            headers={"Accept": "application/json", "User-Agent": "hyveo-addons-bot (https://hyveo.github.io)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        out += d.get("data", [])
        total = d.get("pagination", {}).get("totalCount", len(out))
        if len(out) >= total or not d.get("data"):
            return out
        page += 1


def read_counts():
    # 합계는 Core API, 버전별 숫자는 curseforge.com 공개 파일 목록에서 읽는다.
    # (Core API·CFWidget의 파일별 숫자는 갱신이 며칠씩 늦어 쓰지 않는다)
    entry = {slug: int(api(f"/v1/mods/{pid}")["downloadCount"]) for slug, pid in PROJECTS.items()}
    versions, latest, meta = {}, {}, {}
    try:
        for slug, pid in PROJECTS.items():
            files = sorted(site_files(pid), key=lambda f: f["dateCreated"], reverse=True)
            versions[slug] = {f["displayName"].split()[-1]: int(f["totalDownloads"]) for f in files}
            meta[slug] = {f["displayName"].split()[-1]: {
                "type": {1: "R", 2: "B", 3: "A"}.get(f["releaseType"], "?"),
                "uploaded": dt.datetime.fromisoformat(f["dateCreated"].replace("Z", "+00:00")).astimezone(KST).strftime("%Y-%m-%d %H:%M"),
                "size": int(f.get("fileLength", 0)), "file": f.get("fileName", "")} for f in files}
            if files:
                latest[slug] = {"name": files[0]["displayName"], "beta": files[0]["releaseType"] != 1,
                                "at": files[0]["dateCreated"]}
        entry["versions"] = versions
        json.dump({"updated": dt.datetime.now(KST).strftime("%Y-%m-%dT%H:%M+09:00"), "files": meta},
                  open(FILES_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    except Exception as e:  # noqa: BLE001  사이트가 막히면 합계만 기록
        print("버전별 숫자 읽기 실패, 합계만 기록:", e)
        latest = {}
    json.dump(latest, open("/tmp/latest.json", "w"), ensure_ascii=False)
    return entry, set()


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
    payload = {"username": "CurseForge Dashboard", "embeds": [{
        "title": f"📦 CurseForge 다운로드 · {last['at'][:10]} {last['at'][11:16]}",
        "url": "https://hyveo.github.io/addons/", "color": 0x3FB950,
        "description": desc,
        "fields": version_fields(h, names),
        "footer": {"text": "참조 API: 합계 = CurseForge Core API (GET https://api.curseforge.com/v1/mods/{id}) · 버전별 = curseforge.com 공개 파일 목록 (GET https://www.curseforge.com/api/v1/mods/{id}/files)\n(+n)은 이전 버전별 기록과 비교 · 리워드 포인트는 채팅에서 조회할 때 확인돼요"}}]}
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
