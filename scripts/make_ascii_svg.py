"""Panneau ASCII : portrait en traits tiré de l'avatar illustré. Chaque ligne se tape de gauche à droite,
avec un curseur, puis l'image reste figée."""
from pathlib import Path

import cv2
import numpy as np

from theme import GREEN, esc, frame

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "avatar" / "avatar.png"
OUT = ROOT / "karamo-ascii.svg"

W, H = 370, 470
COLS, ROWS = 60, 46
CW, LH = 5.65, 8.7
FS = 9.4
X0, Y0 = 16, 50
RAMP = " .`':-=+*%#@"
LINE_DUR = 0.07


def grid():
    img = cv2.imread(str(SRC))
    h, w = img.shape[:2]
    target = (COLS * CW) / (ROWS * LH)
    cw = int(h * target)
    x0 = (w - cw) // 2
    img = img[:, x0:x0 + cw]
    # fond crème uni : masque par distance à la couleur des coins
    corners = np.concatenate([img[:40, :40].reshape(-1, 3), img[:40, -40:].reshape(-1, 3)])
    bg = corners.mean(axis=0)
    dist = np.linalg.norm(img.astype(float) - bg, axis=2)
    mask = (dist > 28).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # traits : contours de l'illustration, épaissis pour survivre à la réduction
    edges = cv2.Canny(cv2.GaussianBlur(gray, (7, 7), 0), 55, 140)
    edges = cv2.dilate(edges, np.ones((7, 7), np.uint8))
    size = (COLS, ROWS)
    e = cv2.resize(edges, size, interpolation=cv2.INTER_AREA) / 255.0
    g = cv2.resize(gray, size, interpolation=cv2.INTER_AREA) / 255.0
    m = cv2.resize(mask, size, interpolation=cv2.INTER_AREA) / 255.0
    # intensité : le trait domine, un léger modelé vient des zones claires
    v = np.clip(e * 1.9 + np.clip(g - 0.55, 0, 1) * 0.9, 0, 1)
    return v, m


def lines():
    v, m = grid()
    out = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            if m[y, x] < 0.35:
                row += " "
                continue
            idx = int(round(v[y, x] * (len(RAMP) - 1)))
            row += RAMP[idx] if v[y, x] >= 0.12 else " "
        out.append(row.rstrip())
    return out


def build():
    ls = lines()
    css = ".a{font-size:%.1fpx;white-space:pre;fill:#d6dde5}" % FS
    p = frame(W, H, "cat portrait.txt", css)
    last = 0
    for i, line in enumerate(ls):
        if not line.strip():
            continue
        y = Y0 + (i + 1) * LH
        begin = i * LINE_DUR
        last = i
        p.append(f'<clipPath id="c{i}"><rect x="{X0}" y="{y - LH + 1:.1f}" width="0" height="{LH + 1:.1f}">'
                 f'<animate attributeName="width" from="0" to="{len(line) * CW + 2:.1f}" begin="{begin:.2f}s" dur="{LINE_DUR:.2f}s" fill="freeze"/></rect></clipPath>')
        p.append(f'<text class="a" x="{X0}" y="{y:.1f}" clip-path="url(#c{i})">{esc(line)}</text>')
    total = (last + 1) * LINE_DUR
    p.append(f'<rect x="{X0}" y="{Y0 + 2}" width="{CW:.1f}" height="{LH - 1:.1f}" fill="{GREEN}">'
             f'<animate attributeName="y" from="{Y0 + 2}" to="{Y0 + last * LH + 2:.1f}" dur="{total:.2f}s" fill="freeze"/>'
             f'<animate attributeName="opacity" values="1;0;1" dur="1.1s" begin="{total:.2f}s" repeatCount="indefinite"/></rect>')
    p.append("</svg>")
    OUT.write_text("\n".join(p), encoding="utf-8")
    print(f"{OUT.name} : {sum(1 for l in ls if l.strip())} lignes, {W}x{H}")


if __name__ == "__main__":
    build()
