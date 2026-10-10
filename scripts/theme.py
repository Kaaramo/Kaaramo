"""Charte commune des panneaux SVG : un seul cadre, une seule typo, une seule palette."""

BG = "#0d1117"
PANEL = "#0d1117"
BORDER = "#30363d"
BAR = "#161b22"
TEXT = "#e6edf3"
SOFT = "#c9d1d9"
MUTED = "#7d8590"
GREEN = "#39d353"
GREEN_DIM = "#26a641"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def frame(w, h, title, extra_css=""):
    """Ouvre un panneau : fond, bordure, barre de titre façon terminal avec la commande."""
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">',
        "<style>"
        f"text{{font-family:{MONO};fill:{SOFT}}}"
        f".mu{{fill:{MUTED}}}.gr{{fill:{GREEN}}}.tx{{fill:{TEXT}}}"
        ".b{font-weight:700}"
        ".fade{opacity:0;animation:fade .5s ease-out forwards}"
        "@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important}}"
        + extra_css
        + "</style>",
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>',
        f'<path d="M1 12.5a11.5 11.5 0 0 1 11.5-11.5h{w - 25}a11.5 11.5 0 0 1 11.5 11.5V34H1z" fill="{BAR}"/>',
        f'<line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{BORDER}"/>',
        '<circle cx="20" cy="17.5" r="5.5" fill="#ff5f57"/><circle cx="38" cy="17.5" r="5.5" fill="#febc2e"/><circle cx="56" cy="17.5" r="5.5" fill="#28c840"/>',
        f'<text x="{w / 2:.0f}" y="22" text-anchor="middle" font-size="12.5"><tspan class="gr">karamo@github</tspan><tspan class="mu"> ~ $ </tspan><tspan class="tx">{esc(title)}</tspan></text>',
    ]
