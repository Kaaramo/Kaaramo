"""Portrait ASCII animé : chaque ligne se tape de gauche à droite, avec un curseur, puis l'image reste figée."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "portrait-detoure.png"
OUT = ROOT / "karamo-ascii.svg"

RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 66, 46          # cases de 1 car. ; une case de police mono fait ~0,6 de large pour 1 de haut
CW, LH = 6.0, 9.0            # largeur d'un caractère et hauteur de ligne, en px
PAD = 14
LINE_DUR = 0.09              # durée de frappe d'une ligne, en s


def load_grid():
    rgba = Image.open(SRC).convert("RGBA")
    # recadrage tête et épaules, comme sur le CV
    rgba = rgba.crop((101, 100, 521, 560))
    # luminance du sujet seul, contraste local renforcé (CLAHE) pour faire ressortir les traits du visage
    rgb = np.asarray(rgba.convert("RGB"))
    lum = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    lum = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6, 6)).apply(lum)
    gray = Image.fromarray(lum).resize((COLS, ROWS), Image.LANCZOS)
    a = np.asarray(gray, dtype=float) / 255.0
    alpha = np.asarray(rgba.split()[-1].resize((COLS, ROWS), Image.LANCZOS), dtype=float) / 255.0
    subj = a[alpha >= 0.25]
    lo, hi = np.percentile(subj, 2), np.percentile(subj, 98)
    a = np.clip((a - lo) / (hi - lo + 1e-6), 0, 1) ** 0.8
    return a, alpha


def to_lines(a, alpha):
    lines = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            if alpha[y, x] < 0.25:
                row.append(" ")
                continue
            # fond sombre : les zones claires reçoivent les caractères les plus denses
            idx = int(round(a[y, x] * (len(RAMP) - 1)))
            row.append(RAMP[max(1, idx)])
        lines.append("".join(row).rstrip())
    return lines


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    lines = to_lines(*load_grid())
    w = PAD * 2 + COLS * CW
    h = PAD * 2 + ROWS * LH + 18
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="Portrait ASCII de Karamo Sylla">',
        "<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:9.6px;fill:#c9e8d4;white-space:pre}"
        ".cap{fill:#5b7a68;font-size:10px}</style>",
        f'<rect width="{w:.0f}" height="{h:.0f}" rx="10" fill="#0d1117"/>',
    ]
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        y = PAD + (i + 1) * LH
        begin = i * LINE_DUR
        lw = len(line) * CW
        cid = f"c{i}"
        parts.append(
            f'<clipPath id="{cid}"><rect x="{PAD}" y="{y - LH + 1:.1f}" width="0" height="{LH}">'
            f'<animate attributeName="width" from="0" to="{lw:.1f}" begin="{begin:.2f}s" dur="{LINE_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        parts.append(f'<text x="{PAD}" y="{y:.1f}" clip-path="url(#{cid})">{esc(line)}</text>')
    total = len(lines) * LINE_DUR
    # curseur bloc qui descend avec la frappe puis clignote en bas
    parts.append(
        f'<rect x="{PAD}" y="{PAD + 1}" width="{CW:.0f}" height="{LH - 1:.0f}" fill="#39d353">'
        f'<animate attributeName="y" from="{PAD + 1}" to="{PAD + ROWS * LH - LH + 1:.0f}" dur="{total:.2f}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" begin="{total:.2f}s" repeatCount="indefinite"/></rect>'
    )
    parts.append(f'<text class="cap" x="{PAD}" y="{h - 10:.0f}">karamo@github ~ $ cat portrait.txt</text>')
    parts.append("</svg>")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"{OUT.name} : {len([l for l in lines if l.strip()])} lignes, {w:.0f}x{h:.0f}")


if __name__ == "__main__":
    build()
