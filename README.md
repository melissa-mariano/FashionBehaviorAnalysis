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

## Galerie des visualisations

### 1) Parcours & structure des comportements

#### Sankey — parcours (3 étapes)
👉 [Ouvrir la visualisation](reports/sankey_parcours_3_etapes.html)

#### Sankey — cycle complet (4 étapes)
👉 [Ouvrir la visualisation](reports/sankey_cycle_complet_4_etapes.html)


### 2) Segmentation (K-means) & personas

#### Typologie des consommateurs (waffle)
<p align="center">
  <img src="reports/figures/waffle_clusters_typologie.png" width="900" alt="Waffle - typologie par cluster">
</p>

#### Personas — projection PCA 2D
<p align="center">
  <img src="reports/figures/personas_pca_2d.png" width="900" alt="PCA 2D - personas par cluster">
</p>

#### Heatmap — items / variables par cluster
<p align="center">
  <img src="reports/figures/heatmap_items_par_cluster.png" width="900" alt="Heatmap - variables par cluster">
</p>

#### Obsolescence psychologique — rejet du “démodé” (moyenne)
<p align="center">
  <img src="reports/figures/obsolescence_psy_par_cluster.png" width="900" alt="Obsolescence psychologique - par cluster">
</p>


### 3) Fast fashion & éthique (cohérence / paradoxe)

#### Fast fashion (en %) par cluster
<p align="center">
  <img src="reports/figures/fastfashion_pct_par_cluster.png" width="900" alt="Fast fashion - pourcentage par cluster">
</p>

#### Carte des renoncements — arbitrages moyens par cluster
<p align="center">
  <img src="reports/figures/carte_renoncements_par_cluster.png" width="900" alt="Carte des renoncements - par cluster">
</p>

#### Règles pour payer 20% plus cher (produit éthique) — arbre de décision
<p align="center">
  <img src="reports/figures/arbre_decision_payer_plus.png" width="900" alt="Arbre de décision - payer 20% plus cher">
</p>

#### Le “Grand Paradoxe” — discours vs réalité
<p align="center">
  <img src="reports/figures/grand_paradoxe.png" width="900" alt="Grand paradoxe - discours vs réalité">
</p>

#### Culpabilité : paradoxe vs non-paradoxe
<p align="center">
  <img src="reports/figures/boxplot_culpabilite_par_paradoxe.png" width="900" alt="Boxplot - culpabilité paradoxe vs non-paradoxe">
</p>

#### Densité — éthique × culpabilité
<p align="center">
  <img src="reports/figures/heatmap_densite_ethique_culpabilite.png" width="900" alt="Heatmap densité - éthique x culpabilité">
</p>

#### Taux de paradoxe par âge
<p align="center">
  <img src="reports/figures/paradoxe_par_age.png" width="900" alt="Paradoxe - taux par âge">
</p>

#### Paradoxe éthique par canal d'achat
<p align="center">
  <img src="reports/figures/paradoxe_par_canal.png" width="900" alt="Paradoxe - par canal d'achat">
</p>


### 4) Achat & fin de vie (descriptif)

#### Canaux d’achat (multi-choix)
<p align="center">
  <img src="reports/figures/dist_canaux_achat.png" width="900" alt="Canaux d'achat - distribution">
</p>

#### Fréquence d’achat (top)
<p align="center">
  <img src="reports/figures/dist_frequence_achat.png" width="900" alt="Fréquence d'achat - top réponses">
</p>

#### Destination fin de vie (multi-choix)
<p align="center">
  <img src="reports/figures/dist_destination_fin_vie.png" width="900" alt="Destination fin de vie - distribution">
</p>

#### Fin de vie par fréquence d’achat
<p align="center">
  <img src="reports/figures/fin_de_vie_par_frequence.png" width="900" alt="Fin de vie - selon fréquence d'achat">
</p>


### 5) Tendances : adoption & “packs”

#### Uniformisation — articles tendance par cluster (% adoption)
<p align="center">
  <img src="reports/figures/heatmap_items_par_cluster.png" width="900" alt="Uniformisation - adoption des items par cluster">
</p>

#### Packs de tendances (corrélation > 0.15)
<p align="center">
  <img src="reports/figures/reseau_items_tendance.png" width="900" alt="Réseau - packs de tendances">
</p>


### 6) Réseaux sociaux

#### Réseaux sociaux — distribution de l’influence déclarée (1–10)
<p align="center">
  <img src="reports/figures/reseaux_dist_influence.png" width="900" alt="Réseaux sociaux - distribution influence 1-10">
</p>

#### Réseaux sociaux vs tendances — densité des réponses
<p align="center">
  <img src="reports/figures/reseaux_influence_vs_tendances.png" width="900" alt="Réseaux vs tendances - densité">
</p>

#### Réseaux sociaux — probabilité de fast fashion selon l’influence
<p align="center">
  <img src="reports/figures/reseaux_fastfashion_selon_influence.png" width="900" alt="Probabilité fast fashion - selon influence réseaux">
</p>

#### Culpabilité selon la consommation de fast fashion
<p align="center">
  <img src="reports/figures/reseaux_culpabilite_fastfashion_boxplot.png" width="900" alt="Boxplot - culpabilité selon fast fashion">
</p>

#### Réseaux sociaux — corrélations des variables psycho-sociales
<p align="center">
  <img src="reports/figures/reseaux_heatmap_correlations.png" width="900" alt="Heatmap - corrélations psycho-sociales">
</p>

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
