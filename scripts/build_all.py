"""Génère tous les panneaux, dans les deux thèmes. Les données GitHub privées (projets, langages)
se rafraîchissent à part, en local : python scripts/collect_repos.py"""
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
for script in ["fetch_contributions.py", "render_hero_svg.py", "render_heatmap_svg.py", "render_stats_svg.py",
               "make_ascii_svg.py", "make_info_card.py", "render_projects_svg.py", "render_stack_svg.py"]:
    print(f"--- {script}")
    runpy.run_path(str(HERE / script), run_name="__main__")
