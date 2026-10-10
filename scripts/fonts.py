"""Polices embarquées dans les SVG : Inter (titres, texte) et JetBrains Mono (terminal), licence OFL.

Les TTF sont téléchargés une fois depuis Google Fonts dans assets/fonts/ et versionnés ; chaque SVG
n'embarque ensuite que le sous-ensemble des glyphes qu'il affiche, en WOFF2 base64."""
import base64
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "assets" / "fonts"

# clé : (famille Google Fonts, graisse, nom CSS utilisé dans les SVG)
FACES = {
    "inter-400": ("Inter", 400, "KInter"),
    "inter-600": ("Inter", 600, "KInter"),
    "inter-800": ("Inter", 800, "KInter"),
    "mono-400": ("JetBrains Mono", 400, "KMono"),
    "mono-700": ("JetBrains Mono", 700, "KMono"),
}


def ensure():
    """Télécharge les TTF manquants (une seule fois, en local)."""
    import requests
    DIR.mkdir(parents=True, exist_ok=True)
    for key, (family, weight, _) in FACES.items():
        path = DIR / f"{key}.ttf"
        if path.exists():
            continue
        css = requests.get(
            f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}:wght@{weight}",
            headers={"User-Agent": "Mozilla/4.0"}, timeout=30).text
        url = re.search(r"url\((https://[^)]+\.ttf)\)", css).group(1)
        path.write_bytes(requests.get(url, timeout=60).content)
        print("police téléchargée :", path.name)


def face_css(text, keys):
    """@font-face pour les clés demandées, réduites aux caractères de `text`."""
    from fontTools import subset
    chars = "".join(sorted(set(text + " ")))
    out = []
    for key in keys:
        family, weight, css_name = FACES[key]
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt"]
        opts.name_IDs = []
        opts.notdef_outline = True
        font = subset.load_font(str(DIR / f"{key}.ttf"), opts)
        sub = subset.Subsetter(opts)
        sub.populate(text=chars)
        sub.subset(font)
        buf = io.BytesIO()
        subset.save_font(font, buf, opts)
        b64 = base64.b64encode(buf.getvalue()).decode()
        out.append(f"@font-face{{font-family:'{css_name}';font-weight:{weight};"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(out)


if __name__ == "__main__":
    ensure()
