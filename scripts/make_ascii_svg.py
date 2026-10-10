"""Panneau cat portrait.txt : portrait en traits tiré de l'avatar illustré. Chaque ligne se tape de gauche
à droite, avec un curseur, puis l'image reste figée. Deux thèmes."""
from pathlib import Path

import cv2
import numpy as np

from theme import THEMES, esc, finalize, frame

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "avatar" / "avatar.png"

W, H = 370, 480
COLS, ROWS = 60, 47
CW, LH = 5.65, 8.7
FS = 9.4
X0, Y0 = 16, 52
RAMP = " .`':-=+*%#@"
LINE_DUR = 0.07


def lines():
    img = cv2.imread(str(SRC))
    h, w = img.shape[:2]
    cw = int(h * (COLS * CW) / (ROWS * LH))
    img = img[:, (w - cw) // 2:(w - cw) // 2 + cw]
    corners = np.concatenate([img[:40, :40].reshape(-1, 3), img[:40, -40:].reshape(-1, 3)])
    mask = (np.linalg.norm(img.astype(float) - corners.mean(axis=0), axis=2) > 28).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.dilate(cv2.Canny(cv2.GaussianBlur(gray, (7, 7), 0), 55, 140), np.ones((7, 7), np.uint8))
    size = (COLS, ROWS)
    e = cv2.resize(edges, size, interpolation=cv2.INTER_AREA) / 255.0
    g = cv2.resize(gray, size, interpolation=cv2.INTER_AREA) / 255.0
    m = cv2.resize(mask, size, interpolation=cv2.INTER_AREA) / 255.0
    v = np.clip(e * 1.9 + np.clip(g - 0.55, 0, 1) * 0.9, 0, 1)
    out = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            row += RAMP[int(round(v[y, x] * (len(RAMP) - 1)))] if m[y, x] >= 0.35 and v[y, x] >= 0.12 else " "
        out.append(row.rstrip())
    return out


def build(theme_name, ls):
    t = THEMES[theme_name]
    p = frame(W, H, "cat portrait.txt", t, ".a{font-size:%.1fpx;white-space:pre;fill:%s}" % (FS, t["ascii"]))
    last = 0
    for i, line in enumerate(ls):
        if not line.strip():
            continue
        y, last = Y0 + (i + 1) * LH, i
        p.append(f'<clipPath id="c{i}"><rect x="{X0}" y="{y - LH + 1:.1f}" width="0" height="{LH + 1:.1f}">'
                 f'<animate attributeName="width" from="0" to="{len(line) * CW + 2:.1f}" begin="{i * LINE_DUR:.2f}s" '
                 f'dur="{LINE_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
                 f'<text class="a" x="{X0}" y="{y:.1f}" clip-path="url(#c{i})">{esc(line)}</text>')
    total = (last + 1) * LINE_DUR
    p.append(f'<rect x="{X0}" y="{Y0 + 2}" width="{CW:.1f}" height="{LH - 1:.1f}" fill="{t["accent"]}">'
             f'<animate attributeName="y" from="{Y0 + 2}" to="{Y0 + last * LH + 2:.1f}" dur="{total:.2f}s" fill="freeze"/>'
             f'<animate attributeName="opacity" values="1;0;1" dur="1.1s" begin="{total:.2f}s" repeatCount="indefinite"/></rect>')
    return finalize(p, "portrait", theme_name)


if __name__ == "__main__":
    ls = lines()
    for th in THEMES:
        out, size = build(th, ls)
        print(f"{out.name} : {size // 1024} Ko")
