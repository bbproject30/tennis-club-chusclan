# Site du Tennis Club Chusclan

Site statique généré en Python (Jinja2 + YAML), hébergé gratuitement sur GitHub Pages.

## Pages

- `index.html` — Accueil
- `adhesions.html` — Adhésions & Tarifs
- `actualites.html` — Actualités
- `competitions.html` — Compétitions
- `partenaires.html` — Nos partenaires

## Utilisation en local
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python build.py

Ouvrez `site/index.html` dans un navigateur pour prévisualiser.

## Modifier le contenu

Tout se trouve dans `content/` (fichiers `.yaml`, sans code à toucher) :
`config.yaml`, `adhesions.yaml`, `competitions.yaml`, `partenaires.yaml`.

Photos → `static/images/` · Documents PDF → `static/documents/`

Après modification : `python build.py`, puis publier (voir ci-dessous).

## Publier une mise à jour
git add .
git commit -m "Description du changement"
git push

Le site se régénère et se republie automatiquement en 1-2 minutes.