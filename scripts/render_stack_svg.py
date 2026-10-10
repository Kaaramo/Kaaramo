"""Panneau ./stack.sh : la stack du portfolio (karamosylla.com), en trois groupes de pastilles."""
from pathlib import Path

from theme import BORDER, GREEN, esc, frame

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "stack.svg"

W = 860
PAD = 26
LABEL_W = 170
CHIP_H = 24
CW = 7.4  # largeur moyenne d'un caractère mono à 12px

GROUPS = [
    ("generative_ai/", ["Python", "PyTorch", "Hugging Face", "OpenAI", "Anthropic", "Gemini", "LangChain",
                        "LangGraph", "CrewAI", "MCP", "Pinecone", "Weaviate", "Qdrant", "pgvector"]),
    ("production/", ["AWS", "Bedrock", "Lambda", "SageMaker", "Docker", "Kubernetes", "Terraform",
                     "GitHub Actions", "FastAPI", "PostgreSQL", "Redis", "LangSmith", "MLflow", "Grafana"]),
    ("data_fullstack/", ["TypeScript", "React", "Next.js", "Snowflake", "Databricks", "Azure", "GCP",
                         "n8n", "Make", "Apify"]),
]


def build():
    body = []
    y = 64
    n = 0
    for gi, (label, items) in enumerate(GROUPS):
        body.append(f'<text x="{PAD}" y="{y + 16}" font-size="12.5" class="gr b">{esc(label)}</text>')
        x = PAD + LABEL_W
        for it in items:
            w = len(it) * CW + 22
            if x + w > W - PAD:
                x = PAD + LABEL_W
                y += CHIP_H + 9
            body.append(f'<g class="fade" style="animation-delay:{0.15 + n * 0.035:.3f}s">'
                        f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{CHIP_H}" rx="12" fill="#11161d" stroke="{BORDER}"/>'
                        f'<circle cx="{x + 11:.1f}" cy="{y + CHIP_H / 2}" r="2.6" fill="{GREEN}"/>'
                        f'<text x="{x + 19:.1f}" y="{y + 16}" font-size="12">{esc(it)}</text></g>')
            x += w + 8
            n += 1
        y += CHIP_H + 22
        if gi < len(GROUPS) - 1:
            body.append(f'<line x1="{PAD}" y1="{y - 11}" x2="{W - PAD}" y2="{y - 11}" stroke="#21262d"/>')
    h = y + 6
    p = frame(W, h, "./stack.sh") + body + ["</svg>"]
    OUT.write_text("\n".join(p), encoding="utf-8")
    print(f"{OUT.name} : {W}x{h}, {n} technologies")


if __name__ == "__main__":
    build()
