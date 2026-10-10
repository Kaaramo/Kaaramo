"""Cartes des projets épinglés : une carte par projet (cliquable depuis le README), en deux thèmes."""
import json
import textwrap
from pathlib import Path

from theme import SANS, THEMES, esc, finalize, frame

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "projects.json"

W, H = 425, 178
PAD = 22
LANG_COLORS = {"TypeScript": "#3178c6", "HTML": "#e34c26", "Python": "#3572A5", "JavaScript": "#f1e05a",
               "CSS": "#663399", "Jupyter Notebook": "#DA5B0B", "Shell": "#89e051"}


def slug(name):
    return "project-" + name.lower()


def build(theme_name, pr, idx):
    t = THEMES[theme_name]
    p = frame(W, H, pr["name"], t, bar=False)
    # pictogramme dépôt + nom
    p.append(f'<g class="fade" style="animation-delay:{0.05 + idx * 0.06:.2f}s">'
             f'<rect x="{PAD}" y="{PAD}" width="30" height="30" rx="8" fill="{t["tile"]}" stroke="{t["border"]}"/>'
             f'<path d="M{PAD + 9} {PAD + 8}h10a2 2 0 0 1 2 2v12h-10a2 2 0 0 0-2 2z M{PAD + 9} {PAD + 24}a2 2 0 0 1 2-2" '
             f'fill="none" stroke="{t["accent"]}" stroke-width="1.6" stroke-linejoin="round"/>'
             f'<text x="{PAD + 42}" y="{PAD + 14}" font-size="16.5" class="sans sb tx" style="font-family:{SANS}">{esc(pr["name"])}</text>'
             f'<text x="{PAD + 42}" y="{PAD + 30}" font-size="11" class="mu">Kaaramo/{esc(pr["name"])}</text>'
             f'<text x="{W - PAD}" y="{PAD + 14}" font-size="16" class="ac" text-anchor="end">&#8599;</text></g>')
    # accroche puis description
    p.append(f'<text x="{PAD}" y="{PAD + 60}" font-size="13.5" class="sans sb tx" style="font-family:{SANS}">{esc(pr["tagline"])}</text>')
    for i, line in enumerate(textwrap.wrap(pr["description"], 62)[:2]):
        p.append(f'<text x="{PAD}" y="{PAD + 80 + i * 17}" font-size="12" class="sans mu" style="font-family:{SANS}">{esc(line)}</text>')
    # pied : langage, commits, topics
    y = H - 22
    lang = pr["language"] or "-"
    p.append(f'<circle cx="{PAD + 5}" cy="{y - 4}" r="5" fill="{LANG_COLORS.get(lang, t["muted"])}"/>'
             f'<text x="{PAD + 15}" y="{y}" font-size="11.5">{esc(lang)}</text>')
    x = PAD + 15 + len(lang) * 7.2 + 16
    p.append(f'<text x="{x:.1f}" y="{y}" font-size="11.5" class="mu"><tspan class="ac b">{pr["commits"]}</tspan> commits</text>')
    x += (len(str(pr["commits"])) + 8) * 7.2 + 16
    for tp in pr["topics"][:3]:
        w = len(tp) * 6.6 + 16
        if x + w > W - PAD:
            break
        p.append(f'<rect x="{x:.1f}" y="{y - 14}" width="{w:.1f}" height="20" rx="10" fill="none" stroke="{t["border"]}"/>'
                 f'<text x="{x + 8:.1f}" y="{y}" font-size="10.5" class="ac2">{esc(tp)}</text>')
        x += w + 6
    return finalize(p, slug(pr["name"]), theme_name, faces=("mono-400", "mono-700", "inter-400", "inter-600"))


if __name__ == "__main__":
    projects = json.loads(SRC.read_text(encoding="utf-8"))
    for th in THEMES:
        for i, pr in enumerate(projects):
            out, size = build(th, pr, i)
            print(f"{out.name} : {size // 1024} Ko")
