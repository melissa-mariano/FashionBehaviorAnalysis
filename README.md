# Analyse des comportements de consommation de mode

Explorer la mode comme un système de données : comportements d’achat, tensions éthiques, pression sociale et segmentation des profils consommateurs.

---

## Contexte

Ce projet est inspiré du célèbre monologue du *bleu céruléen* dans **Le Diable s’habille en Prada**, qui illustre comment les tendances — souvent perçues comme des choix individuels — sont en réalité façonnées par un système industriel structuré.

À partir d’une enquête quantitative menée auprès de **428 répondants**, le pipeline propose une analyse orientée **data storytelling**, traduisant des comportements sociaux (achat, influence, culpabilité, arbitrages, fin de vie) en structures analytiques lisibles à l’aide de visualisations avancées et d’exports automatisés.

---

## Problématique

Comment l’industrie de la mode impacte-t-elle le comportement et les choix vestimentaires ?

Questions principales :
- Existe-t-il un décalage entre valeurs déclarées et comportements réels (fast fashion) ?
- Quel rôle jouent les réseaux sociaux, la tendance et la pression sociale ?
- Peut-on identifier des profils (personas) via une segmentation exploratoire ?
- Quels arbitrages structurent les décisions (prix, qualité, confort, éthique, tendance) ?
- Comment la fréquence d’achat est-elle liée à la fin de vie des vêtements ?

---

## Structure du projet

```
FashionBehaviorAnalysis/
│
├── data/
│   └── La mode - LaMode.csv
│
├── notebooks/
│   └── pipeline_visualisations.py
│
├── reports/
│
├── requirements.txt
└── README.md
```

---

## Installation

### Cloner le projet

git clone https://github.com/melissa-mariano/FashionBehaviorAnalysis.git  
cd FashionBehaviorAnalysis

### Créer un environnement virtuel (recommandé)

Windows (PowerShell) :
python -m venv venv  
venv\Scripts\Activate.ps1

macOS / Linux :
python3 -m venv venv  
source venv/bin/activate

### Installer les dépendances

pip install -r requirements.txt

---

## Utilisation

python notebooks/pipeline_visualisations.py

Ce script exécute un **pipeline analytique complet** :

- normalisation robuste des échelles Likert (détection automatique)
- design system visuel inspiré du bleu céruléen
- construction d’indicateurs sociologiques (paradoxe éthique, obsolescence psychologique)
- visualisations narratives (hexbin, Sankey, réseaux, heatmaps)
- clustering exploratoire K-Means + projection PCA
- arbre de décision interprétable (XAI léger)
- génération automatique des exports (figures, diagnostics, tableaux)

---

## Logique analytique (chapitres)

- Chapitre 1 — Discours vs réalité : le Grand Paradoxe
- Chapitre 2 — Spirale des réseaux sociaux et culpabilité
- Chapitre 3 — Machine à tendances (co-adoption d’items)
- Chapitre 4 — Personas et segmentation
- Chapitre 5 — Uniformisation et pression sociale
- Chapitre 6 — Arbitrages structurés
- Chapitre 7 — Décision explicable (payer plus pour l’éthique)
- Chapitre 8 — Conséquences : fréquence d’achat et fin de vie

---

## Méthodologie

- Nettoyage et normalisation des données (formats FR, Likert)
- Renommage robuste et détection automatique des variables
- Feature engineering sociologique
- Analyse de densité (hexbin)
- Clustering K-Means + PCA
- Réseaux de corrélation (packs de tendances)
- Arbre de décision interprétable
- Data storytelling visuel

---

## Objectifs du projet

- Comprendre les dynamiques sociales derrière les choix vestimentaires
- Mettre en évidence l’influence structurelle de l’industrie de la mode
- Transformer un phénomène culturel en analyse data-driven

---

## Dépendances principales

- pandas
- numpy
- matplotlib
- seaborn
- plotly
- scikit-learn

---

## Auteur

Melissa Albuquerque
