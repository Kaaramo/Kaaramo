"""Collecte locale (GitHub CLI connecté) : fiches des projets épinglés et langages agrégés de tous les dépôts.
Écrit data/projects.json et data/languages.json. Aucun nom de dépôt privé n'est conservé."""
import json
import re
import subprocess
from pathlib import Path

GH = r"C:\Program Files\GitHub CLI\gh.exe"
ROOT = Path(__file__).resolve().parent.parent

PINNED = ["SKILLNAV", "Radar", "Finance-CyberAttack-Analytics",
          "ai5d-digital-design-system", "ai5d-auth", "Vehicle-Damage-Detection"]
# libellé court affiché sur la carte, tiré du README de chaque projet
TAGLINE = {
    "SKILLNAV": "Job-market observatory for AI & data skills",
    "Radar": "Competitive intelligence run by an AI agent",
    "Finance-CyberAttack-Analytics": "Cyberattacks on the financial sector, 2015-2025",
    "ai5d-digital-design-system": "Design system of the AI5D products",
    "ai5d-auth": "Identity SDK of the AI5D ecosystem",
    "Vehicle-Damage-Detection": "Damage detection with convolutional networks",
}
EXCLUDED_LANGS = {"Jupyter Notebook"}  # le poids des sorties de notebooks fausserait la répartition


def gh_json(*a):
    return json.loads(subprocess.run([GH, *a], capture_output=True, text=True, encoding="utf-8").stdout or "null")


def commits(full):
    r = subprocess.run([GH, "api", "-i", f"repos/{full}/commits?per_page=1"], capture_output=True, text=True, encoding="utf-8")
    m = re.search(r'page=(\d+)>; rel="last"', r.stdout)
    return int(m.group(1)) if m else (1 if '"sha"' in r.stdout else 0)


def main():
    projects = []
    for name in PINNED:
        full = f"Kaaramo/{name}"
        r = gh_json("repo", "view", full, "--json", "name,description,primaryLanguage,repositoryTopics,url")
        langs = gh_json("api", f"repos/{full}/languages") or {}
        projects.append({
            "name": r["name"], "url": r["url"], "tagline": TAGLINE[name],
            "description": r["description"] or "",
            "language": (r["primaryLanguage"] or {}).get("name", ""),
            "languages": langs,
            "topics": [t["name"] for t in (r["repositoryTopics"] or [])][:4],
            "commits": commits(full),
        })
    (ROOT / "data" / "projects.json").write_text(json.dumps(projects, indent=1, ensure_ascii=False), encoding="utf-8")

    totals, count = {}, 0
    for owner in ["Kaaramo", "ia5d", "aseguim-org", "mimbao-hq"]:
        for r in gh_json("repo", "list", owner, "--limit", "300", "--json", "nameWithOwner,isFork,isArchived"):
            if r["isFork"] or r["isArchived"]:
                continue
            count += 1
            for lang, size in (gh_json("api", f"repos/{r['nameWithOwner']}/languages") or {}).items():
                if lang not in EXCLUDED_LANGS:
                    totals[lang] = totals.get(lang, 0) + size
    data = {"repositories": count, "excluded": sorted(EXCLUDED_LANGS),
            "bytes": dict(sorted(totals.items(), key=lambda x: -x[1]))}
    (ROOT / "data" / "languages.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"{len(projects)} projets, langages sur {count} dépôts")


if __name__ == "__main__":
    main()
