"""Carte d'infos façon neofetch : barre de titre, puis lignes clé/valeur qui apparaissent en fondu décalé.
STATIC=1 produit une version figée (aperçus locaux)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

W = 490
PAD = 20
LH = 19
KEY_W = 92

# Chaque entrée : (clé, valeur). Une clé vide prolonge la ligne précédente.
ROWS = [
    ("Now", "Big Data & AI engineering student, ENSA Tétouan"),
    ("", "Founder, AI5D: AI consulting and development"),
    ("Prev", "AI consultant & developer (freelance), AI Crafters"),
    ("", "Trainer, AI4Leaders program, AI4X Academy"),
    ("Focus", "AI agents, RAG, NLP, automation for business"),
    ("Stack", "Python · PyTorch · Hugging Face · LangChain"),
    ("", "LangGraph · CrewAI · MCP · FastAPI · n8n"),
    ("", "PostgreSQL · Qdrant · Next.js · AWS"),
    ("Projects", "SKILLNAV · RADAR · Azimut"),
    ("Award", "Winner, AI Prompt Challenge Bank-e"),
    ("", "Crédit Agricole du Maroc · GITEX Africa 2026"),
    ("Impact", "400+ people trained in AI"),
    ("Links", "karamosylla.com · linkedin.com/in/syllakaramo"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    top = 46
    h = top + PAD + len(ROWS) * LH + 34
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="Karamo Sylla : informations de profil">',
        "<style>"
        "text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px}"
        ".k{fill:#39d353;font-weight:700}.v{fill:#c9d1d9}.t{fill:#e6edf3;font-weight:700;font-size:13px}"
        ".m{fill:#7d8590}"
        + ("" if STATIC else
           ".r{opacity:0;animation:in .45s ease-out forwards}"
           "@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}")
        + "</style>",
        f'<rect width="{W}" height="{h}" rx="10" fill="#0d1117" stroke="#30363d"/>',
        f'<path d="M0 10a10 10 0 0 1 10-10h{W - 20}a10 10 0 0 1 10 10v20H0z" fill="#161b22"/>',
        '<circle cx="18" cy="15" r="5" fill="#ff5f56"/><circle cx="34" cy="15" r="5" fill="#ffbd2e"/><circle cx="50" cy="15" r="5" fill="#27c93f"/>',
        f'<text class="m" x="{W / 2:.0f}" y="19" text-anchor="middle">karamo@github: ~</text>',
        f'<text class="t" x="{PAD}" y="{top + 4}">karamo<tspan class="m">@</tspan>sylla</text>',
        f'<text class="m" x="{PAD}" y="{top + 18}">{"-" * 13}</text>',
    ]
    y0 = top + 24 + LH
    for i, (k, v) in enumerate(ROWS):
        y = y0 + i * LH
        delay = 0.15 + i * 0.12
        style = "" if STATIC else f' style="animation-delay:{delay:.2f}s"'
        p.append(
            f'<g class="r"{style}>'
            + (f'<text class="k" x="{PAD}" y="{y}">{esc(k)}</text>' if k else "")
            + f'<text class="v" x="{PAD + KEY_W}" y="{y}">{esc(v)}</text></g>'
        )
    # palette de couleurs, signature neofetch
    yb = y0 + len(ROWS) * LH - 4
    colors = ["#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0", "#e6edf3"]
    for j, c in enumerate(colors):
        p.append(f'<rect x="{PAD + KEY_W + j * 22}" y="{yb}" width="18" height="10" rx="2" fill="{c}"/>')
    p.append("</svg>")
    OUT.write_text("\n".join(p), encoding="utf-8")
    print(f"{OUT.name} : {len(ROWS)} lignes, {W}x{h}{' (statique)' if STATIC else ''}")


if __name__ == "__main__":
    build()
