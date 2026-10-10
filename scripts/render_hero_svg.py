"""Bannière d'accueil : avatar illustré, nom, rôles qui s'écrivent en alternance, repères."""
import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw

from theme import SANS, THEMES, esc, finalize, frame

ROOT = Path(__file__).resolve().parent.parent
AVATAR = ROOT / "assets" / "avatar" / "avatar.png"

W, H = 860, 250
AV = 168                 # diamètre de l'avatar
AX, AY = 38, (H - AV) // 2
TX = AX + AV + 40        # début du texte
ROLES = ["AI engineer & consultant", "Founder of AI5D", "AI engineering student",
         "Trainer: 400+ people trained"]
SLOT = 3.4               # secondes par rôle
CHIPS = ["Rabat, Morocco", "ENSA Tetouan '27", "GITEX Africa 2026 winner"]
NOW = ["building the AI5D platform", "shipping GenAI to production", "training leaders in AI"]
MONO_W = 0.6             # largeur d'un caractère mono, en em


def avatar_b64():
    im = Image.open(AVATAR).convert("RGB").resize((AV * 2, AV * 2), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode()


def roles_svg(t, x, y, fs):
    total = SLOT * len(ROLES)
    out = []
    for i, role in enumerate(ROLES):
        width = len(role) * fs * MONO_W + 2
        a, b, c, d = i * SLOT, i * SLOT + 1.0, i * SLOT + SLOT - 0.7, i * SLOT + SLOT - 0.25
        kt = [0, a / total, b / total, c / total, d / total, 1]
        vals = [0, 0, width, width, 0, 0]
        # supprime les doublons de keyTimes (premier rôle)
        pts = []
        for k, v in zip(kt, vals):
            if pts and abs(pts[-1][0] - k) < 1e-9:
                pts[-1] = (k, v)
            else:
                pts.append((k, v))
        ks = ";".join(f"{k:.4f}" for k, _ in pts)
        vs = ";".join(f"{v:.1f}" for _, v in pts)
        cx = ";".join(f"{x + v + 2:.1f}" for _, v in pts)
        out.append(
            f'<clipPath id="r{i}"><rect x="{x}" y="{y - fs}" height="{fs * 1.4:.1f}" width="0">'
            f'<animate attributeName="width" dur="{total}s" repeatCount="indefinite" keyTimes="{ks}" values="{vs}"/></rect></clipPath>'
            f'<text x="{x}" y="{y}" font-size="{fs}" class="ac" clip-path="url(#r{i})">{esc(role)}</text>'
            f'<rect y="{y - fs + 2}" width="{fs * 0.55:.1f}" height="{fs * 1.1:.1f}" fill="{t["accent"]}" opacity="0">'
            f'<animate attributeName="x" dur="{total}s" repeatCount="indefinite" keyTimes="{ks}" values="{cx}"/>'
            f'<animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" keyTimes="{ks}" '
            f'values="{";".join(".85" if v > 0 else "0" for _, v in pts)}"/></rect>'
        )
    return out


def build(theme_name, b64):
    t = THEMES[theme_name]
    css = (".grid{opacity:.5}"
           ".ring{transform-origin:%dpx %dpx;animation:spin 18s linear infinite}"
           "@keyframes spin{to{transform:rotate(360deg)}}" % (AX + AV // 2, AY + AV // 2))
    p = frame(W, H, "Karamo Sylla", t, css, bar=False)
    # trame de points discrète, plus dense à droite
    p.append(f'<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="{t["border"]}"/></pattern>'
             f'<linearGradient id="fadeR" x1="0" x2="1"><stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>'
             f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#fadeR)"/></mask>'
             f'<rect class="grid" x="2" y="2" width="{W - 4}" height="{H - 4}" rx="13" fill="url(#dots)" mask="url(#m)"/>')
    # avatar avec anneau en dégradé qui tourne lentement
    cx, cy, r = AX + AV // 2, AY + AV // 2, AV // 2
    p.append(f'<linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["accent"]}"/>'
             f'<stop offset=".5" stop-color="{t["accent2"]}" stop-opacity=".2"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient>'
             f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r + 7}" fill="none" stroke="url(#rg)" stroke-width="2.5" stroke-dasharray="6 5"/>'
             f'<clipPath id="av"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
             f'<image x="{AX}" y="{AY}" width="{AV}" height="{AV}" clip-path="url(#av)" href="data:image/jpeg;base64,{b64}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["border"]}"/>')
    # texte
    p.append(f'<text x="{TX}" y="70" font-size="13" class="mu">karamo@github ~ $ <tspan class="tx">whoami</tspan></text>')
    p.append(f'<text x="{TX - 2}" y="118" font-size="44" class="sans xb tx" style="font-family:{SANS};letter-spacing:-1.2px">Karamo Sylla</text>')
    p.append(f'<text x="{TX}" y="153" font-size="17" class="mu">&gt;</text>')
    p += roles_svg(t, TX + 20, 153, 17)
    # repères
    x = TX
    for i, chip in enumerate(CHIPS):
        w = len(chip) * 6.9 + 34
        p.append(f'<g class="fade" style="animation-delay:{0.3 + i * 0.12:.2f}s">'
                 f'<rect x="{x:.1f}" y="180" width="{w:.1f}" height="28" rx="14" fill="{t["tile"]}" stroke="{t["border"]}"/>'
                 f'<circle cx="{x + 15:.1f}" cy="194" r="3.2" fill="{t["accent"] if i != 2 else t["accent2"]}"/>'
                 f'<text x="{x + 25:.1f}" y="198.5" font-size="12" class="sans" style="font-family:{SANS}">{esc(chip)}</text></g>')
        x += w + 10
    # encart « currently » à droite
    bx, by, bw, bh = W - 254, 38, 218, 116
    p.append(f'<g class="fade" style="animation-delay:.5s"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" '
             f'fill="{t["tile"]}" stroke="{t["border"]}"/>'
             f'<text x="{bx + 18}" y="{by + 26}" font-size="11.5" class="mu">~/currently</text>')
    for i, line in enumerate(NOW):
        yy = by + 54 + i * 24
        p.append(f'<text x="{bx + 18}" y="{yy}" font-size="12.5"><tspan class="ac">&#9656;</tspan>'
                 f'<tspan class="sans tx" style="font-family:{SANS}" dx="8">{esc(line)}</tspan></text>')
    p.append("</g>")
    return finalize(p, "hero", theme_name, faces=("mono-400", "inter-400", "inter-800"))


if __name__ == "__main__":
    b64 = avatar_b64()
    for th in THEMES:
        out, size = build(th, b64)
        print(f"{out.name} : {size // 1024} Ko")
