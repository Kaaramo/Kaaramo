"""Panneau cat about.md : identité et repères, en deux colonnes clé/valeur, en deux thèmes."""
from theme import SANS, THEMES, esc, finalize, frame

W = 860
PAD = 26
LH = 24
KEY_W = 88
COL2 = 440

LEFT = [
    ("role", "Big Data & AI engineering student"),
    ("school", "ENSA Tétouan, graduating 2027"),
    ("now", "Founder, AI5D: AI consulting & engineering"),
    ("prev", "AI consultant & developer, AI Crafters"),
    ("trainer", "AI4Leaders program, AI4X Academy"),
]
RIGHT = [
    ("focus", "GenAI in production: RAG, agents, MLOps"),
    ("award", "Winner, AI Prompt Challenge Bank-e"),
    ("", "GITEX Africa 2026, Crédit Agricole"),
    ("impact", "400+ professionals trained in AI"),
    ("research", "web mining, NLP, agentic systems"),
]


def rows(col, x0, start, shift):
    out = []
    for i, (k, v) in enumerate(col):
        y = start + i * LH
        out.append(f'<g class="fade" style="animation-delay:{0.25 + (i + shift) * 0.11:.2f}s">'
                   + (f'<text x="{x0}" y="{y}" font-size="12.5" class="ac b">{esc(k)}</text>' if k else "")
                   + f'<text x="{x0 + KEY_W}" y="{y}" font-size="12.5">{esc(v)}</text></g>')
    return out


def build(theme_name):
    t = THEMES[theme_name]
    start = 120
    h = start + len(LEFT) * LH + 18
    p = frame(W, h, "cat about.md", t)
    p.append(f'<text x="{PAD}" y="76" font-size="22" class="sans xb tx" style="font-family:{SANS};letter-spacing:-.4px">Karamo Sylla</text>')
    p.append(f'<text x="{PAD + 158}" y="75" font-size="13.5" class="sans mu" style="font-family:{SANS}">'
             "I turn business use cases into AI systems that ship, and teach teams to use them.</text>")
    p.append(f'<line x1="{PAD}" y1="92" x2="{W - PAD}" y2="92" stroke="{t["hair"]}"/>')
    p += rows(LEFT, PAD, start, 0)
    p += rows(RIGHT, COL2, start, 0.5)
    return finalize(p, "about", theme_name, faces=("mono-400", "mono-700", "inter-400", "inter-800"))


if __name__ == "__main__":
    for th in THEMES:
        out, size = build(th)
        print(f"{out.name} : {size // 1024} Ko")
