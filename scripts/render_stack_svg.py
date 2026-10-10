"""Panneau ./stack.sh : répartition des langages sur tous les dépôts, puis la stack du portfolio en pastilles."""
import json
from pathlib import Path

from theme import THEMES, esc, finalize, frame

ROOT = Path(__file__).resolve().parent.parent
LANGS = ROOT / "data" / "languages.json"

W = 860
PAD = 26
LABEL_W = 168
CHIP_H = 25
CW = 7.25

# couleurs de langages reprises de GitHub Linguist
LANG_COLORS = {"TypeScript": "#3178c6", "HTML": "#e34c26", "Python": "#3572A5", "JavaScript": "#f1e05a",
               "CSS": "#663399", "Shell": "#89e051", "PLpgSQL": "#336790"}

GROUPS = [
    ("generative_ai/", ["Python", "PyTorch", "Hugging Face", "OpenAI", "Anthropic", "Gemini", "LangChain",
                        "LangGraph", "CrewAI", "MCP", "Pinecone", "Weaviate", "Qdrant", "pgvector"]),
    ("production/", ["AWS", "Bedrock", "Lambda", "SageMaker", "Docker", "Kubernetes", "Terraform",
                     "GitHub Actions", "FastAPI", "PostgreSQL", "Redis", "LangSmith", "MLflow", "Grafana"]),
    ("data_fullstack/", ["TypeScript", "React", "Next.js", "Snowflake", "Databricks", "Azure", "GCP",
                         "n8n", "Make", "Apify"]),
]


def build(theme_name, langs):
    t = THEMES[theme_name]
    css = (".seg{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:sx .9s cubic-bezier(.2,.8,.2,1) forwards}"
           "@keyframes sx{to{transform:scaleX(1)}}")
    body = []
    # barre des langages
    total = sum(langs["bytes"].values())
    items = list(langs["bytes"].items())
    top = [(k, v) for k, v in items if v / total >= 0.01][:6]
    other = total - sum(v for _, v in top)
    if other > 0:
        top.append(("Other", other))
    y = 62
    body.append(f'<text x="{PAD}" y="{y}" font-size="12.5" class="ac b">languages/</text>')
    body.append(f'<text x="{W - PAD}" y="{y}" font-size="11" class="mu" text-anchor="end">'
                f'by code size across {langs["repositories"]} repositories, notebooks excluded</text>')
    bx, bw, by = PAD, W - 2 * PAD, y + 14
    body.append(f'<clipPath id="lb"><rect x="{bx}" y="{by}" width="{bw}" height="10" rx="5"/></clipPath><g clip-path="url(#lb)">')
    x = bx
    for i, (k, v) in enumerate(top):
        w = bw * v / total
        body.append(f'<rect class="seg" style="animation-delay:{0.1 + i * 0.08:.2f}s" x="{x:.1f}" y="{by}" width="{w + .6:.1f}" '
                    f'height="10" fill="{LANG_COLORS.get(k, t["muted"])}"/>')
        x += w
    body.append("</g>")
    lx, ly = PAD, by + 32
    for k, v in top:
        label = f"{k} {v * 100 / total:.1f}%"
        body.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="4.5" fill="{LANG_COLORS.get(k, t["muted"])}"/>'
                    f'<text x="{lx + 15}" y="{ly}" font-size="11.5">{esc(k)} <tspan class="mu">{v * 100 / total:.1f}%</tspan></text>')
        lx += len(label) * 7 + 34
    y = ly + 26
    body.append(f'<line x1="{PAD}" y1="{y - 6}" x2="{W - PAD}" y2="{y - 6}" stroke="{t["hair"]}"/>')
    # pastilles
    n = 0
    y += 10
    for gi, (label, tools) in enumerate(GROUPS):
        body.append(f'<text x="{PAD}" y="{y + 17}" font-size="12.5" class="ac b">{esc(label)}</text>')
        x = PAD + LABEL_W
        for it in tools:
            w = len(it) * CW + 24
            if x + w > W - PAD:
                x = PAD + LABEL_W
                y += CHIP_H + 9
            body.append(f'<g class="fade" style="animation-delay:{0.4 + n * 0.03:.2f}s">'
                        f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{CHIP_H}" rx="12.5" fill="{t["tile"]}" stroke="{t["border"]}"/>'
                        f'<circle cx="{x + 12:.1f}" cy="{y + CHIP_H / 2}" r="2.7" fill="{t["accent"]}"/>'
                        f'<text x="{x + 20:.1f}" y="{y + 16.5}" font-size="12">{esc(it)}</text></g>')
            x += w + 8
            n += 1
        y += CHIP_H + 22
        if gi < len(GROUPS) - 1:
            body.append(f'<line x1="{PAD}" y1="{y - 11}" x2="{W - PAD}" y2="{y - 11}" stroke="{t["hair"]}"/>')
    h = y + 6
    return finalize(frame(W, h, "./stack.sh", t, css) + body, "stack", theme_name)


if __name__ == "__main__":
    langs = json.loads(LANGS.read_text(encoding="utf-8"))
    for th in THEMES:
        out, size = build(th, langs)
        print(f"{out.name} : {size // 1024} Ko")
