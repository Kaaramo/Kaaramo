"""Panneau cat about.md : identité et repères, en deux colonnes clé/valeur qui apparaissent en fondu.
STATIC=1 produit une version figée (aperçus locaux)."""
import os
from pathlib import Path

from theme import esc, frame

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

W = 860
PAD = 26
LH = 23
KEY_W = 86
COL2 = 448

LEFT = [
    ("Role", "Big Data & AI engineering student"),
    ("School", "ENSA Tétouan, graduating 2027"),
    ("Now", "Founder, AI5D: AI consulting & engineering"),
    ("Prev", "AI consultant & developer, AI Crafters"),
    ("Trainer", "AI4Leaders program, AI4X Academy"),
]
RIGHT = [
    ("Focus", "GenAI in production: RAG, agents, MLOps"),
    ("Award", "Winner, AI Prompt Challenge Bank-e"),
    ("", "Crédit Agricole du Maroc, GITEX Africa 2026"),
    ("Impact", "400+ professionals trained in AI"),
    ("Projects", "SKILLNAV · RADAR · Azimut"),
]


def rows(col, x0, start):
    out = []
    for i, (k, v) in enumerate(col):
        y = start + i * LH
        delay = 0.25 + (i + (0 if x0 == PAD else 0.5)) * 0.12
        cls = "" if STATIC else ' class="fade"'
        style = "" if STATIC else f' style="animation-delay:{delay:.2f}s"'
        out.append(f'<g{cls}{style}>'
                   + (f'<text x="{x0}" y="{y}" font-size="12.5" class="gr b">{esc(k)}</text>' if k else "")
                   + f'<text x="{x0 + KEY_W}" y="{y}" font-size="12.5">{esc(v)}</text></g>')
    return out


def build():
    start = 112
    h = start + len(LEFT) * LH + 20
    p = frame(W, h, "cat about.md")
    p.append(f'<text x="{PAD}" y="70" font-size="21" class="tx b">Karamo Sylla</text>')
    p.append(f'<text x="{PAD + 152}" y="70" font-size="13" class="mu">AI engineer &amp; consultant · I turn business use cases into AI systems that ship</text>')
    p.append(f'<line x1="{PAD}" y1="84" x2="{W - PAD}" y2="84" stroke="#21262d"/>')
    p += rows(LEFT, PAD, start)
    p += rows(RIGHT, COL2, start)
    p.append("</svg>")
    OUT.write_text("\n".join(p), encoding="utf-8")
    print(f"{OUT.name} : {W}x{h}{' (statique)' if STATIC else ''}")


if __name__ == "__main__":
    build()
