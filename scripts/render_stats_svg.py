"""Panneau whoami --stats : six tuiles chiffrées et histogramme mensuel, depuis data/contributions.json."""
import json
from collections import OrderedDict
from datetime import date
from pathlib import Path

from theme import BORDER, GREEN, GREEN_DIM, PALETTE, frame

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "contributions.json"
OUT = ROOT / "stats.svg"

W, H = 490, 470
PAD = 22
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def monthly(days):
    m = OrderedDict()
    for d in days:
        k = d["date"][:7]
        m[k] = m.get(k, 0) + d["count"]
    return list(m.items())[-12:]


def build():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    days, st = data["days"], data["stats"]
    active = st["active_days"]
    avg = st["total"] / active if active else 0
    tiles = [
        (f'{st["current_streak"]}', "current streak (days)"),
        (f'{st["longest_streak"]}', "longest streak (days)"),
        (f'{st["total"]:,}', "contributions, last 12 months"),
        (f"{active}", "active days"),
        (f'{st["best_day"]["count"]}', "best day"),
        (f"{avg:.1f}", "per active day"),
    ]
    css = (".bar{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .7s cubic-bezier(.2,.8,.2,1) forwards}"
           "@keyframes grow{to{transform:scaleY(1)}}")
    p = frame(W, H, "whoami --stats", css)
    tw = (W - 2 * PAD - 12) / 2
    for i, (val, lab) in enumerate(tiles):
        col, row = i % 2, i // 2
        x, y = PAD + col * (tw + 12), 52 + row * 82
        p.append(f'<g class="fade" style="animation-delay:{0.1 + i * 0.08:.2f}s">'
                 f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="70" rx="9" fill="#11161d" stroke="{BORDER}"/>'
                 f'<text x="{x + 16:.1f}" y="{y + 36}" font-size="25" class="b" fill="{GREEN}" style="fill:{GREEN}">{val}</text>'
                 f'<text x="{x + 16:.1f}" y="{y + 56}" font-size="11" class="mu">{lab}</text></g>')
    months = monthly(days)
    top, base = 330, 432
    p.append(f'<text x="{PAD}" y="{top - 14}" font-size="11.5" class="mu">contributions per month</text>')
    mx = max((v for _, v in months), default=1) or 1
    slot = (W - 2 * PAD) / len(months)
    bw = slot * 0.62
    for i, (k, v) in enumerate(months):
        bh = max(2, (base - top) * v / mx)
        x = PAD + i * slot + (slot - bw) / 2
        fill = GREEN if v == mx else GREEN_DIM if v else PALETTE[0]
        p.append(f'<rect class="bar" style="animation-delay:{0.6 + i * 0.05:.2f}s" x="{x:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="{fill}"><title>{k}: {v}</title></rect>')
        if v == mx:
            p.append(f'<text x="{x + bw / 2:.1f}" y="{base - bh - 6:.1f}" font-size="10.5" text-anchor="middle" class="gr b">{v}</text>')
        m = int(k[5:]) - 1
        p.append(f'<text x="{x + bw / 2:.1f}" y="{base + 16}" font-size="9.5" text-anchor="middle" class="mu">{MONTHS[m][0]}</text>')
    p.append(f'<line x1="{PAD}" y1="{base + .5}" x2="{W - PAD}" y2="{base + .5}" stroke="{BORDER}"/>')
    p.append("</svg>")
    OUT.write_text("\n".join(p), encoding="utf-8")
    print(f"{OUT.name} : {W}x{H}")


if __name__ == "__main__":
    build()
