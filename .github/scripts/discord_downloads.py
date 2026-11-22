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


def diff(k):
    if prev is None:
        return ""
    v = last.get(k, 0) - prev.get(k, 0)
    return f" (+{v})" if v >= 0 else f" ({v})"


def versions_line(k):
    v = (last.get("versions") or {}).get(k)
    if not v:
        return None
    pv = ((prev or {}).get("versions") or {}).get(k)
    parts = []
    for ver, cnt in v.items():
        d = "" if pv is None else (f" (+{cnt - pv.get(ver, 0)})" if cnt - pv.get(ver, 0) > 0 else "")
        parts.append(f"{ver} {cnt:,}{d}")
    return "　└ " + " · ".join(parts)


lines = []
for k in names:
    lines.append(f"**{names[k]}** {last.get(k, 0):,}{diff(k)}")
    vl = versions_line(k)
    if vl:
        lines.append(vl)
total = sum(last.get(k, 0) for k in names)
ptotal = sum(prev.get(k, 0) for k in names) if prev else None
tdiff = "" if ptotal is None else f" (+{total - ptotal})" if total >= ptotal else f" ({total - ptotal})"

payload = {
    "username": "hyveo addons",
    "embeds": [{
        "title": f"📦 CurseForge 다운로드 · {last['at'][:10]}",
        "url": "https://hyveo.github.io/addons/#downloads",
        "description": "\n".join(lines) + f"\n\n합계 **{total:,}**{tdiff}",
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
