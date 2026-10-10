"""Panneau ./contributions.sh : grille 53 x 7 révélée en diagonale, total et légende."""
import json
from datetime import date
from pathlib import Path

from theme import GREEN, MUTED, PALETTE, frame

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

W = 860
CELL, GAP = 12, 3
LEFT, TOP = 46, 92
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def level(count):
    if count == 0:
        return 0
    if count < 3:
        return 1
    if count < 6:
        return 2
    if count < 10:
        return 3
    if count < 20:
        return 4
    return 5


def build():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    days, st = data["days"], data["stats"]
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # semaine commençant le dimanche, comme GitHub
    h = TOP + 7 * (CELL + GAP) + 48
    css = (".c{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s cubic-bezier(.2,.8,.2,1) forwards}"
           "@keyframes pop{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:none}}")
    p = frame(W, h, "./contributions.sh", css)
    p.append(f'<text x="{LEFT}" y="66" font-size="22" class="tx b">{st["total"]:,}<tspan font-size="13" class="mu" font-weight="400">  contributions in the last year</tspan></text>')
    p.append(f'<text x="{W - 24}" y="66" font-size="11.5" class="mu" text-anchor="end">updated {data["generated"]}</text>')
    for i, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(f'<text x="14" y="{TOP + i * (CELL + GAP) + 10}" font-size="10" class="mu">{lab}</text>')
    seen = set()
    for idx, d in enumerate(days):
        wk, dow = divmod(idx + offset, 7)
        x, y = LEFT + wk * (CELL + GAP), TOP + dow * (CELL + GAP)
        dt = date.fromisoformat(d["date"])
        if dow == 0 and dt.day <= 7 and dt.month not in seen and wk < 52:
            seen.add(dt.month)
            p.append(f'<text x="{x}" y="{TOP - 8}" font-size="10" class="mu">{MONTHS[dt.month - 1]}</text>')
        delay = (wk + dow * 1.5) * 0.011
        tip = f'{d["count"]} contribution{"s" if d["count"] != 1 else ""} on {d["date"]}'
        p.append(f'<rect class="c" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[level(d["count"])]}"><title>{tip}</title></rect>')
    yb = TOP + 7 * (CELL + GAP) + 26
    p.append(f'<text x="{LEFT}" y="{yb}" font-size="11.5" class="mu">longest streak <tspan class="gr b">{st["longest_streak"]}</tspan> days  ·  best day <tspan class="gr b">{st["best_day"]["count"]}</tspan> on {st["best_day"]["date"]}</text>')
    lx = W - 24 - 5 * (CELL + 3) - 62
    p.append(f'<text x="{lx}" y="{yb}" font-size="10.5" class="mu">Less</text>')
    for j, c in enumerate(PALETTE[:5]):
        p.append(f'<rect x="{lx + 30 + j * (CELL + 3)}" y="{yb - 10}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>')
    p.append(f'<text x="{lx + 34 + 5 * (CELL + 3)}" y="{yb}" font-size="10.5" class="mu">More</text>')
    p.append("</svg>")
    OUT.write_text("\n".join(p), encoding="utf-8")
    print(f"{OUT.name} : {W}x{h}")


if __name__ == "__main__":
    build()
