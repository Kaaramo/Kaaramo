"""Panneau ./contributions.sh : grille 53 x 7 révélée en diagonale, total et légende, en deux thèmes."""
import json
from datetime import date
from pathlib import Path

from theme import THEMES, finalize, frame

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "contributions.json"

W = 860
CELL, GAP = 12, 3
LEFT, TOP = 48, 100
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def level(count):
    for lvl, cap in enumerate((0, 2, 5, 9, 19)):
        if count <= cap:
            return lvl
    return 5


def build(theme_name, data):
    t = THEMES[theme_name]
    days, st = data["days"], data["stats"]
    offset = (date.fromisoformat(days[0]["date"]).weekday() + 1) % 7
    h = TOP + 7 * (CELL + GAP) + 50
    css = (".c{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.2,.8,.2,1) forwards}"
           "@keyframes pop{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:none}}")
    p = frame(W, h, "./contributions.sh", t, css, meta=f'updated {data["generated"]}')
    p.append(f'<text x="{LEFT}" y="72" font-size="26" class="b tx">{st["total"]:,}'
             f'<tspan font-size="13" class="mu" font-weight="400" dx="10">contributions in the last year</tspan></text>')
    for i, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(f'<text x="14" y="{TOP + i * (CELL + GAP) + 10}" font-size="10" class="mu">{lab}</text>')
    seen = set()
    for idx, d in enumerate(days):
        wk, dow = divmod(idx + offset, 7)
        x, y = LEFT + wk * (CELL + GAP), TOP + dow * (CELL + GAP)
        dt = date.fromisoformat(d["date"])
        if dow == 0 and dt.day <= 7 and dt.month not in seen and wk < 52:
            seen.add(dt.month)
            p.append(f'<text x="{x}" y="{TOP - 9}" font-size="10" class="mu">{MONTHS[dt.month - 1]}</text>')
        tip = f'{d["count"]} contribution{"s" if d["count"] != 1 else ""} on {d["date"]}'
        p.append(f'<rect class="c" style="animation-delay:{(wk + dow * 1.5) * 0.011:.3f}s" x="{x}" y="{y}" width="{CELL}" '
                 f'height="{CELL}" rx="3" fill="{t["heat"][level(d["count"])]}"><title>{tip}</title></rect>')
    yb = TOP + 7 * (CELL + GAP) + 28
    p.append(f'<text x="{LEFT}" y="{yb}" font-size="11.5" class="mu">longest streak <tspan class="ac b">{st["longest_streak"]}</tspan> days'
             f'  ·  best day <tspan class="ac b">{st["best_day"]["count"]}</tspan> on {st["best_day"]["date"]}'
             f'  ·  <tspan class="ac b">{st["active_days"]}</tspan> active days</text>')
    lx = W - 22 - 5 * (CELL + 3) - 64
    p.append(f'<text x="{lx}" y="{yb}" font-size="10.5" class="mu">Less</text>')
    for j in range(5):
        p.append(f'<rect x="{lx + 31 + j * (CELL + 3)}" y="{yb - 10}" width="{CELL}" height="{CELL}" rx="3" fill="{t["heat"][j]}"/>')
    p.append(f'<text x="{lx + 35 + 5 * (CELL + 3)}" y="{yb}" font-size="10.5" class="mu">More</text>')
    return finalize(p, "contributions", theme_name)


if __name__ == "__main__":
    data = json.loads(SRC.read_text(encoding="utf-8"))
    for th in THEMES:
        out, size = build(th, data)
        print(f"{out.name} : {size // 1024} Ko")
