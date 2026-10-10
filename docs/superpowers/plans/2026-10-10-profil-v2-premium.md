# Plan : profil GitHub, version premium (V3 technique, « V2 » pour Karamo)

**Date :** 2026-10-10
**Spec :** demande de Karamo du 2026-10-10 (« encore plus moderne et premium ») ; référence visuelle fournie le même jour ;
cartographie `.prive/cartographie-depots.md` (projets épinglés, contributions privées activées).

## Global Constraints

- Aucun JavaScript, aucune ressource externe dans les SVG (GitHub les bloque) : polices et avatar embarqués en base64.
- Polices sous licence libre (OFL) : Inter (titres) et JetBrains Mono (terminal), sous-ensemble des seuls glyphes utilisés.
- Deux thèmes : chaque panneau existe en sombre et en clair ; le README choisit avec `<picture>` et `prefers-color-scheme`.
- Aucun fait inventé ; aucun nom de dépôt privé. Les chiffres viennent de GitHub (grille publique, API via GitHub CLI).
- Animations sobres, jouées une fois, désactivées par `prefers-reduced-motion`.
- Rien n'est poussé sans relecture du rendu ; aucune mention d'assistant dans les commits.

## Tâches

- [x] `theme.py` : deux palettes, cadre à bordure en dégradé, polices embarquées (`fonts.py` : téléchargement, sous-ensemble, base64).
- [x] `render_hero_svg.py` : bannière (avatar illustré, nom, rôles qui s'écrivent en alternance, repères).
- [x] Panneaux existants portés sur la nouvelle charte, en deux thèmes : contributions, stats, portrait, about, stack.
- [x] `collect_repos.py` (local, GitHub CLI) : métadonnées des 6 projets épinglés et langages agrégés de tous les dépôts.
- [x] `render_projects_svg.py` : une carte cliquable par projet épinglé ; barre des langages dans `./stack.sh`.
- [x] `build_all.py` : génère tout ; le robot quotidien ne refait que contributions et stats, dans les deux thèmes.
- [x] README recomposé.
- [x] Vérification d'un bloc : scripts, XML, poids des SVG, rendu sombre et clair regardé à l'image ; puis publication.

Vérification (2026-10-10) : build_all sans erreur, 24 SVG (25 à 80 Ko), rendu sombre et clair regardé à l'image ; débordements corrigés (pastilles de la bannière, ligne « award »).
