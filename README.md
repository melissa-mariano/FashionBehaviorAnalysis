# FashionBehaviorAnalysis
## Quand le bleu céruléen devient une donnée

---

## Contexte

Ce projet est inspiré du célèbre monologue du *bleu céruléen* dans **Le Diable s’habille en Prada**, qui illustre comment les tendances de la mode — souvent perçues comme des choix personnels — sont en réalité façonnées par une industrie complexe.

L’objectif est d’explorer une question centrale :

**Comment l’industrie de la mode influence-t-elle les comportements et les décisions individuelles dans notre société ?**

À partir d’une enquête quantitative menée auprès de 428 répondants, ce projet combine data science, sociologie de la mode et storytelling visuel pour analyser les paradoxes entre discours éthique, pression sociale et pratiques réelles.

---

## Problématique

Comment l’industrie de la mode impacte-t-elle le comportement et les choix vestimentaires ?

Plus précisément :
- Existe-t-il un décalage entre valeurs déclarées et comportements réels ?
- Quel rôle jouent les réseaux sociaux et les tendances ?
- Peut-on identifier des profils psychologiques de consommateurs ?

---

## Structure du projet

FashionBehaviorAnalysis/
│
├── data/
│   └── La mode - LaMode.csv
│
├── notebooks/
│   └── notebook_visualisations.py
│
├── reports/
│   ├── figures/
│   ├── personas_clusters.csv
│   ├── personas_moyennes_par_cluster.csv
│   └── kmeans_elbow_silhouette.csv
│
├── requirements.txt
└── README.md

---

## Installation

### Cloner le projet

git clone https://github.com/melissa-mariano/FashionBehaviorAnalysis.git
cd FashionBehaviorAnalysis

### Créer un environnement virtuel (recommandé)

python -m venv venv
venv\Scripts\Activate.ps1

### Installer les dépendances

pip install -r requirements.txt

---

## Utilisation

python notebooks/notebook_visualisations.py

Ce script :
- nettoie et standardise les données de l’enquête
- génère l’ensemble des visualisations
- segmente les répondants en personas via clustering
- exporte les résultats dans le dossier reports/

---

## Visualisations principales

- Le Grand Paradoxe : discours éthique vs consommation réelle de fast fashion
- Spirale de culpabilité : influence des réseaux sociaux et culpabilité post-achat
- Personas consommateurs (K-Means)
- Carte des renoncements
- Arbre décisionnel
- Sankey narratif du parcours d’achat

---

## Méthodologie

- Nettoyage et normalisation des données
- Transformation des échelles de type Likert
- Feature engineering sociologique
- Clustering K-Means
- Arbre de décision
- Visualisations narratives

---

## Objectifs du projet

- Comprendre les dynamiques sociales derrière les choix vestimentaires
- Mettre en évidence l’influence structurelle de l’industrie de la mode
- Transformer un phénomène culturel en analyse data-driven
- Construire un storytelling visuel basé sur des données réelles

---

## Dépendances principales

- pandas
- numpy
- matplotlib
- plotly
- scikit-learn

---

## Auteur

Melissa Albuquerque
