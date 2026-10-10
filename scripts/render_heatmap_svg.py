"""Grille de contributions 53 x 7 en SVG, révélée en diagonale au chargement."""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP = 12, 3
LEFT, TOP = 34, 30
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def build():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    days = data["days"]
    st = data["stats"]
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # GitHub commence la semaine le dimanche

    weeks = (offset + len(days) + 6) // 7
    w = LEFT + weeks * (CELL + GAP) + 16
    h = TOP + 7 * (CELL + GAP) + 64
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Contributions GitHub de Karamo Sylla sur un an">',
        "<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:10px;fill:#7d8590}"
        ".s{fill:#c9d1d9;font-size:11.5px}.n{fill:#39d353;font-weight:700}"
        ".c{opacity:0;animation:pop .35s ease-out forwards}"
        "@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:none}}"
        ".c{transform-box:fill-box;transform-origin:center}</style>",
        f'<rect width="{w}" height="{h}" rx="10" fill="#0d1117" stroke="#30363d"/>',
    ]
    for i, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(f'<text x="8" y="{TOP + i * (CELL + GAP) + 10}">{lab}</text>')
    seen = set()
    for idx, d in enumerate(days):
        pos = idx + offset
        wk, dow = divmod(pos, 7)
        x = LEFT + wk * (CELL + GAP)
        y = TOP + dow * (CELL + GAP)
        dt = date.fromisoformat(d["date"])
        if dt.day <= 7 and dow == 0 and dt.month not in seen and wk < weeks - 1:
            seen.add(dt.month)
            p.append(f'<text x="{x}" y="{TOP - 9}">{MONTHS[dt.month - 1]}</text>')
        lvl = min(d["level"], 4) if d["count"] < 20 else 5
        delay = (wk + dow) * 0.012
        title = f'{d["count"]} contribution{"s" if d["count"] != 1 else ""} on {d["date"]}'
        p.append(
            f'<rect class="c" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[lvl]}"><title>{title}</title></rect>'
        )
    yb = TOP + 7 * (CELL + GAP) + 22
    best = st["best_day"]
    p.append(
        f'<text class="s" x="{LEFT}" y="{yb}"><tspan class="n">{st["total"]}</tspan> contributions in the last year'
        f'  ·  longest streak <tspan class="n">{st["longest_streak"]}</tspan> days'
        f'  ·  current streak <tspan class="n">{st["current_streak"]}</tspan> days</text>'
    )
    if best and best["count"]:
        p.append(f'<text x="{LEFT}" y="{yb + 18}">best day: {best["date"]} ({best["count"]})  ·  updated {data["generated"]}</text>')
    lx = w - 16 - 6 * (CELL + 2) - 70
    p.append(f'<text x="{lx}" y="{yb + 18}">Less</text>')
    for j, c in enumerate(PALETTE[:5]):
        p.append(f'<rect x="{lx + 28 + j * (CELL + 2)}" y="{yb + 9}" width="{CELL - 2}" height="{CELL - 2}" rx="2" fill="{c}"/>')
    p.append(f'<text x="{lx + 28 + 5 * (CELL + 2) + 4}" y="{yb + 18}">More</text>')
    p.append("</svg>")
    OUT.write_text("\n".join(p), encoding="utf-8")
    print(f"{OUT.name} : {weeks} semaines, {w}x{h}")


if __name__ == "__main__":
    build()
