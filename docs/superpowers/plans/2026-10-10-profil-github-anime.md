# Plan : README de profil GitHub animé

**Spec :** demande de Karamo du 2026-10-10, méthode de l'article « Build an animated GitHub profile README »
(avivashishta.com, lu le 2026-10-10). Faits du profil : dossier « Avenir et Orientations » (`00-profil/`, `data/04-experiences.md`).

## Global Constraints

- Aucun service tiers, aucun token : seules les images SVG du dépôt et l'endpoint public `github.com/users/Kaaramo/contributions`.
- GitHub retire JavaScript et style en ligne : animations en SMIL ou CSS interne au SVG, mise en page en `<table>` et `<br>`.
- Aucun fait inventé : tout ce qui figure sur la carte vient du dossier de Karamo. Pas d'adresse e-mail publique.
- Rien n'est poussé sur GitHub sans l'accord explicite de Karamo ; aucune mention d'assistant dans les commits.

## Tâches

- [x] `scripts/make_ascii_svg.py` : portrait ASCII animé (balayage ligne par ligne, curseur), depuis le portrait détouré du CV.
- [x] `scripts/make_info_card.py` : carte façon neofetch, lignes en fondu décalé ; `STATIC=1` pour un rendu figé.
- [x] `scripts/fetch_contributions.py` : données publiques vers `data/contributions.json` (jours, série, meilleur jour, total).
- [x] `scripts/render_heatmap_svg.py` : grille 53 × 7, révélation diagonale.
- [x] `README.md` : portrait et carte côte à côte, grille dessous, liens.
- [x] `.github/workflows/update-profile-art.yml` : rafraîchissement quotidien de la grille.
- [x] Vérification d'un bloc (2026-10-10) : quatre scripts exécutés sans erreur (371 jours, 328 contributions), trois SVG valides en XML, rendu final regardé à l'image ; portrait retravaillé (rampe inversée, CLAHE, recadrage).
- [ ] Publication : création du dépôt public `Kaaramo/Kaaramo` par Karamo, poussée après son accord.
