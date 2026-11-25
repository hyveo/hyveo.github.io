"""downloads.json의 마지막 두 기록을 비교해서 디스코드 웹훅으로 알린다."""
import json
import os
import sys
import urllib.request

hook = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
if not hook:
    print("DISCORD_WEBHOOK_URL 시크릿이 없어서 건너뜀")
    sys.exit(0)

d = json.load(open("public/addons/downloads.json", encoding="utf-8"))
names = d["addons"]
h = d["history"]
last = h[-1]
prev = h[-2] if len(h) > 1 else None
today = last["at"][:10]
day0 = next((r for r in reversed(h) if r["at"][:10] < today), None)


def change(now, before):
    if before is None:
        return ""
    v = now - before
    return f"  (+{v})" if v > 0 else ("" if v == 0 else f"  ({v})")


def total(r):
    return sum(r.get(k, 0) for k in names)


fields = []
for k, name in names.items():
    cnt = last.get(k, 0)
    head = f"{name} — {cnt:,}회" + change(cnt, prev.get(k) if prev else None)
    v = (last.get("versions") or {}).get(k)
    pv = ((prev or {}).get("versions") or {}).get(k)
    if v:
        dv = None if day0 is None else (day0.get("versions") or {}).get(k, {})
        rows = []
        for ver, n in v.items():
            bits = []
            if pv is not None and prev is not day0 and n - pv.get(ver, 0) > 0:
                bits.append(f"+{n - pv.get(ver, 0)}")
            if dv is not None and n - dv.get(ver, 0) > 0:
                bits.append(f"오늘 +{n - dv.get(ver, 0)}")
            rows.append(f"`v{ver}`  **{n:,}**회" + (f"  ({' · '.join(bits)})" if bits else ""))
        value = "\n".join(rows)
    else:
        value = "버전별 기록 없음"
    fields.append({"name": head, "value": value, "inline": True})

t = total(last)
desc = f"전체 **{t:,}회**" + change(t, total(prev) if prev else None)
if day0 is not None:
    parts = " · ".join(f"{names[k]} +{last.get(k, 0) - day0.get(k, 0)}" for k in names)
    desc += f"\n📅 오늘({today[5:7]}/{today[8:10]}) 누적: {parts} · 합계 **+{t - total(day0)}**"
payload = {
    "username": "hyveo addons",
    "embeds": [{
        "title": f"📦 CurseForge 다운로드 · {last['at'][:10]}",
        "url": "https://hyveo.github.io/addons/",
        "description": desc,
        "fields": fields,
        "color": 0x3FB950,
    }],
}
req = urllib.request.Request(
    hook,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json", "User-Agent": "hyveo-addons-bot (https://hyveo.github.io, 1.0)"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=20) as r:
    print("디스코드 전송:", r.status)
