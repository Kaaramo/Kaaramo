"""Charte commune des panneaux SVG : deux thèmes (sombre, clair), cadre à bordure en dégradé,
polices embarquées. Chaque script appelle frame() pour ouvrir un panneau et finalize() pour l'écrire."""
import re
from pathlib import Path

from fonts import face_css

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "assets" / "svg"

THEMES = {
    "dark": {
        "bg": "#0d1117", "panel_top": "#0f141b", "panel_bot": "#0b0f14", "bar": "#11161d",
        "tile": "#131922", "border": "#262c36", "hair": "#1c222b",
        "text": "#e6edf3", "soft": "#c9d1d9", "muted": "#7d8590",
        "accent": "#3fdc6c", "accent2": "#2ec5b6", "accent_dim": "#26a641",
        "heat": ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#7ef0a5"],
        "ascii": "#d6dde5",
    },
    "light": {
        "bg": "#ffffff", "panel_top": "#ffffff", "panel_bot": "#f6f8fa", "bar": "#f6f8fa",
        "tile": "#ffffff", "border": "#d0d7de", "hair": "#e6eaef",
        "text": "#1f2328", "soft": "#24292f", "muted": "#59636e",
        "accent": "#1a7f37", "accent2": "#0f7f73", "accent_dim": "#2da44e",
        "heat": ["#ebedf0", "#aceebb", "#4ac26b", "#2da44e", "#116329", "#0a3d1a"],
        "ascii": "#2f363d",
    },
}

MONO = "'KMono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "'KInter',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def base_css(t):
    return (
        f"text{{font-family:{MONO};fill:{t['soft']}}}"
        f".sans{{font-family:{SANS}}}"
        f".mu{{fill:{t['muted']}}}.ac{{fill:{t['accent']}}}.tx{{fill:{t['text']}}}.ac2{{fill:{t['accent2']}}}"
        ".b{font-weight:700}.sb{font-weight:600}.xb{font-weight:800}"
        ".fade{opacity:0;animation:fade .55s cubic-bezier(.2,.8,.2,1) forwards}"
        "@keyframes fade{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important;transform:none!important}}"
    )


def defs(t, w, h):
    return (
        "<defs>"
        f'<linearGradient id="bd" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{t["accent"]}" stop-opacity=".55"/>'
        f'<stop offset=".35" stop-color="{t["border"]}"/>'
        f'<stop offset=".7" stop-color="{t["border"]}"/>'
        f'<stop offset="1" stop-color="{t["accent2"]}" stop-opacity=".45"/></linearGradient>'
        f'<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["panel_top"]}"/>'
        f'<stop offset="1" stop-color="{t["panel_bot"]}"/></linearGradient>'
        "</defs>"
    )


def frame(w, h, title, t, extra_css="", meta="", bar=True):
    """Ouvre un panneau. bar=False donne une carte sans barre de terminal (bannière, cartes projets)."""
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">',
        "<style>" + base_css(t) + extra_css + "</style>",
        defs(t, w, h),
        f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="14" fill="url(#pn)" stroke="url(#bd)" stroke-width="1.5"/>',
    ]
    if bar:
        p += [
            f'<path d="M1.5 14.5a13 13 0 0 1 13-13h{w - 29}a13 13 0 0 1 13 13V36H1.5z" fill="{t["bar"]}"/>',
            f'<line x1="1.5" y1="36.5" x2="{w - 1.5}" y2="36.5" stroke="{t["hair"]}"/>',
            '<circle cx="21" cy="18.5" r="5.5" fill="#ff5f57"/><circle cx="39" cy="18.5" r="5.5" fill="#febc2e"/><circle cx="57" cy="18.5" r="5.5" fill="#28c840"/>',
            f'<text x="80" y="23" font-size="12.5"><tspan class="ac">karamo</tspan><tspan class="mu">@github</tspan>'
            f'<tspan class="mu"> ~ $ </tspan><tspan class="tx">{esc(title)}</tspan></text>',
        ]
        if meta:
            p.append(f'<text x="{w - 20}" y="23" font-size="11" class="mu" text-anchor="end">{esc(meta)}</text>')
    return p


def finalize(parts, name, theme_name, faces=("mono-400", "mono-700")):
    """Ajoute les polices réduites aux glyphes affichés, ferme le SVG et l'écrit."""
    body = "\n".join(parts) + "\n</svg>"
    texts = " ".join(re.findall(r">([^<>]+)<", body))
    texts = texts.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    font = "<style>" + face_css(texts, list(faces)) + "</style>"
    body = body.replace("<style>", font + "<style>", 1)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    out = SVG_DIR / (f"{name}.svg" if theme_name == "dark" else f"{name}-light.svg")
    out.write_text(body, encoding="utf-8")
    return out, len(body.encode("utf-8"))
