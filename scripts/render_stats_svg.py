"""Panneau whoami --stats : six tuiles chiffrées et histogramme mensuel, en deux thèmes."""
import json
from collections import OrderedDict
from pathlib import Path

from theme import THEMES, finalize, frame

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "contributions.json"

W, H = 490, 480
PAD = 22
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def monthly(days):
    m = OrderedDict()
    for d in days:
        m[d["date"][:7]] = m.get(d["date"][:7], 0) + d["count"]
    return list(m.items())[-12:]


def build(theme_name, data):
    t = THEMES[theme_name]
    days, st = data["days"], data["stats"]
    active = st["active_days"]
    tiles = [
        (f'{st["total"]:,}', "contributions, last 12 months"),
        (f"{active}", "active days"),
        (f'{st["longest_streak"]}', "longest streak (days)"),
        (f'{st["current_streak"]}', "current streak (days)"),
        (f'{st["best_day"]["count"]}', "best day"),
        (f'{st["total"] / active if active else 0:.1f}', "per active day"),
    ]
    css = (".bar{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .8s cubic-bezier(.2,.8,.2,1) forwards}"
           "@keyframes grow{to{transform:scaleY(1)}}")
    p = frame(W, H, "whoami --stats", t, css)
    p.append(f'<linearGradient id="bg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["accent"]}"/>'
             f'<stop offset="1" stop-color="{t["accent2"]}" stop-opacity=".75"/></linearGradient>')
    tw = (W - 2 * PAD - 12) / 2
    for i, (val, lab) in enumerate(tiles):
        x, y = PAD + (i % 2) * (tw + 12), 54 + (i // 2) * 82
        p.append(f'<g class="fade" style="animation-delay:{0.1 + i * 0.08:.2f}s">'
                 f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="70" rx="10" fill="{t["tile"]}" stroke="{t["border"]}"/>'
                 f'<rect x="{x:.1f}" y="{y + 18}" width="3" height="34" rx="1.5" fill="url(#bg1)"/>'
                 f'<text x="{x + 18:.1f}" y="{y + 37}" font-size="25" class="b tx">{val}</text>'
                 f'<text x="{x + 18:.1f}" y="{y + 57}" font-size="11" class="mu">{lab}</text></g>')
    months = monthly(days)
    top, base = 334, 440
    p.append(f'<text x="{PAD}" y="{top - 14}" font-size="11.5" class="mu">contributions per month</text>')
    mx = max((v for _, v in months), default=1) or 1
    slot = (W - 2 * PAD) / len(months)
    bw = slot * 0.62
    for i, (k, v) in enumerate(months):
        bh = max(2, (base - top) * v / mx)
        x = PAD + i * slot + (slot - bw) / 2
        fill = "url(#bg1)" if v else t["heat"][0]
        p.append(f'<rect class="bar" style="animation-delay:{0.6 + i * 0.05:.2f}s" x="{x:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" '
                 f'height="{bh:.1f}" rx="3" fill="{fill}" opacity="{1 if v == mx else .78}"><title>{k}: {v}</title></rect>')
        if v == mx:
            p.append(f'<text x="{x + bw / 2:.1f}" y="{base - bh - 6:.1f}" font-size="10.5" text-anchor="middle" class="ac b">{v}</text>')
        p.append(f'<text x="{x + bw / 2:.1f}" y="{base + 17}" font-size="9.5" text-anchor="middle" class="mu">{MONTHS[int(k[5:]) - 1][0]}</text>')
    p.append(f'<line x1="{PAD}" y1="{base + .5}" x2="{W - PAD}" y2="{base + .5}" stroke="{t["border"]}"/>')
    return finalize(p, "stats", theme_name)


if __name__ == "__main__":
    data = json.loads(SRC.read_text(encoding="utf-8"))
    for th in THEMES:
        out, size = build(th, data)
        print(f"{out.name} : {size // 1024} Ko")
