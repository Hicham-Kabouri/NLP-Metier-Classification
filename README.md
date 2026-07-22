# Classification Sémantique de Métiers (NAP)

Outil de recherche sémantique permettant d'associer une profession, saisie en langage libre (français ou arabe), aux codes de la **Nomenclature Analytique des Professions (NAP)**. Le projet a été réalisé dans le cadre d'un stage au **Haut-Commissariat au Plan (HCP) — Direction des systèmes d'informations statistiques**.

**Démo en ligne :** [https://nlp-metier-classification-aedasudzs46qdvjvvvack2.streamlit.app/](https://nlp-metier-classification-aedasudzs46qdvjvvvack2.streamlit.app/)

---

## Contexte et objectif

Dans le cadre des enquêtes et recensements menés par le HCP, chaque profession déclarée par un individu doit être rattachée à un code NAP officiel. Cette opération, traditionnellement manuelle, est chronophage et sujette à des incohérences entre agents.

Ce projet propose une solution automatisée : à partir d'une profession saisie librement (ex: *"infirmier en pédiatrie"*), l'outil retourne les codes NAP les plus proches sémantiquement, accompagnés d'un score de confiance.

## Fonctionnement

Le projet repose sur un pipeline en deux phases : la **construction du corpus de référence** (réalisée une fois, en amont) et la **recherche sémantique** (exécutée à chaque requête utilisateur).

### Phase 1 — Construction du corpus de référence

1. **Extraction des données** — la nomenclature officielle **NAP 2014** (Nomenclature Analytique des Professions), disponible au format PDF en français et en arabe, est extraite et structurée
2. **Construction de la base de données** — les intitulés de métiers sont organisés selon la structure hiérarchique de la nomenclature (Grand Groupe > Sous-Grand Groupe > Sous-Groupe > Code métier), pour les deux langues, puis consolidés dans un référentiel unique (`reference_corpus_final`, `data_mapping`)
3. **Génération des embeddings** — chaque intitulé de métier du corpus de référence est encodé en vecteur numérique via le modèle multilingue, puis sauvegardé (`src/embedding/`) pour éviter de recalculer ces vecteurs à chaque recherche

### Phase 2 — Recherche sémantique (à chaque requête)

4. **Prétraitement** — nettoyage du texte saisi par l'utilisateur (normalisation, gestion des diacritiques arabes, mise en minuscule pour le français)
5. **Embedding de la requête** — la requête est transformée en vecteur numérique via le même modèle de langue multilingue (`paraphrase-multilingual-mpnet-base-v2`)
6. **Recherche par similarité** — comparaison (similarité cosinus) entre le vecteur de la requête et les embeddings pré-calculés du corpus de référence
7. **Filtrage et classement** — sélection du top 20, suppression des doublons de code, application d'un seuil de confiance, puis affichage des 5 meilleurs résultats

## Stack technique

| Composant | Technologie |
|---|---|
| Modèle d'embedding | `sentence-transformers` (paraphrase-multilingual-mpnet-base-v2) |
| Traitement des données | `pandas`, `numpy` |
| Interface web | `Streamlit` |
| Conteneurisation | `Docker` |
| Hébergement | Streamlit Community Cloud |

## Structure du projet

```
NLP-Metier-Classification/
├── src/
│   ├── search_engine/
│   │   └── search_engine.py     # Nettoyage + moteur de recherche sémantique
│   └── embedding/                # Corpus de référence et embeddings pré-calculés
├── app.py                        # Interface web Streamlit
├── requirements.txt              # Dépendances Python
├── Dockerfile                    # Image de déploiement conteneurisé
└── README.md
```

## Installation et lancement en local

### Prérequis
- Python 3.10+
- Git

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/Hicham-Kabouri/NLP-Metier-Classification.git
cd NLP-Metier-Classification

# 2. Créer et activer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`.

### Alternative avec Docker

```bash
docker build -t nlp-metier-classification .
docker run -p 8501:8501 nlp-metier-classification
```

## Licence

Le code de ce projet est distribué sous licence MIT (voir le fichier `LICENSE`).

Les données de référence utilisées (nomenclature NAP 2014) proviennent du Haut-Commissariat au Plan et restent la propriété de cette institution.

## Auteur

**Hicham Kabouri**
Projet réalisé dans le cadre d'un stage au Haut-Commissariat au Plan (HCP) — Direction des systèmes d'informations statistiques