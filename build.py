"""
Génère le site statique du club de tennis à partir des fichiers
YAML dans content/ et des templates dans templates/.

Usage :
    python build.py

Résultat : le dossier site/ contient le HTML/CSS prêt à héberger.
"""

import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

import json
import re

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "site"

# Mettez ici le nom de votre dépôt GitHub si vous utilisez GitHub Pages
# en mode "projet" (ex: "https://<user>.github.io/<repo>/").
# Laissez "" si vous utilisez un domaine personnalisé ou Netlify.
BASE_URL = "/tennis-club-chusclan/"
#BASE_URL = ""

COULEURS_PALETTE = ["#c81d25", "#2f7d4f", "#3498db", "#e67e22", "#8e44ad", "#d4547e", "#16a085", "#b8860b"]

def slugify(texte):
    return re.sub(r'[^a-z0-9]+', '-', texte.lower()).strip('-')


def load_yaml(filename):
    with open(CONTENT_DIR / filename, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build():
    config = load_yaml("config.yaml")
    tournois = load_yaml("tournois.yaml")
    evenements = load_yaml("evenements.yaml")
    equipes = load_yaml("equipes.yaml")
    adhesions = load_yaml("adhesions.yaml")

    competitions = load_yaml("competitions.yaml")

    # Liste des compétitions distinctes, dans l'ordre où elles apparaissent
    noms_competitions = []
    for c in competitions:
        if c["competition"] not in noms_competitions:
            noms_competitions.append(c["competition"])

    couleur_par_competition = {
        nom: COULEURS_PALETTE[i % len(COULEURS_PALETTE)]
        for i, nom in enumerate(noms_competitions)
    }

    timeline_groups = [
        {"id": slugify(nom), "content": nom}
        for nom in noms_competitions
    ]

    timeline_items = []
    for i, c in enumerate(competitions):
        nom = c["competition"]
        couleur = couleur_par_competition[nom]
        tooltip = (
            f"<span class='tooltip-titre'>"
            f"<span class='tooltip-pastille' style='background:{couleur};'></span>"
            f"{nom}</span>"
            f"<strong>vs {c['adversaire']}</strong><br>"
            f"{c.get('domicile_exterieur', '')}"
        )
        if c.get("score"):
            tooltip += f"<br>Score : {c['score']}"
        timeline_items.append({
            "id": i,
            "group": slugify(nom),
            "start": c["date"],
            "content": f"vs {c['adversaire']}",
            "title": tooltip,
            "style": f"background-color:{couleur}; border-color:{couleur}; color:white;",
        })

    partenaires = load_yaml("partenaires.yaml")
    
    # Nettoyage du dossier de sortie
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Copie des fichiers statiques (CSS, images)
    shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    nb_enfants = config["statistiques"]["adherents"]["enfants"]
    nb_adultes = config["statistiques"]["adherents"]["adultes_femmes"] + config["statistiques"]["adherents"]["adultes_hommes"]
    total_adherents = nb_enfants + nb_adultes
    pct_enfants = round((nb_enfants / total_adherents) * 100, 1) if total_adherents else 0

    context = {
        "config": config,
        "adhesions": adhesions,
        "tournois": tournois,
        "evenements": evenements,
        "equipes": equipes,
        "partenaires": partenaires,
        "legende_competitions": [{"nom": n, "couleur": c} for n, c in couleur_par_competition.items()],
        "timeline_groups_json": json.dumps(timeline_groups, ensure_ascii=False),
        "timeline_items_json": json.dumps(timeline_items, ensure_ascii=False),
        "total_adherents": total_adherents,
        "pct_enfants": pct_enfants,
        "nb_adultes": nb_adultes,
        "base_url": BASE_URL,
    }

    pages = {
        "index.html": "index.html",
        "adhesions.html": "adhesions.html",
        "actualites.html": "actualites.html",
        "competitions.html": "competitions.html",
        "partenaires.html": "partenaires.html",
    }

    for template_name, output_name in pages.items():
        template = env.get_template(template_name)
        html = template.render(**context)
        (OUTPUT_DIR / output_name).write_text(html, encoding="utf-8")
        print(f"✓ Généré : site/{output_name}")

    print(f"\nSite généré dans {OUTPUT_DIR}/")
    print("Ouvrez site/index.html dans votre navigateur pour prévisualiser.")


if __name__ == "__main__":
    build()
