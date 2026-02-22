# Analyse des comportements de consommation de mode

Explorer la mode comme un système de données :
comportements d’achat, tensions éthiques et segmentation des profils consommateurs.

---

## Contexte

Ce projet est inspiré du célèbre monologue du *bleu céruléen* dans **Le Diable s’habille en Prada**, qui illustre comment les tendances de la mode — souvent perçues comme des choix personnels — sont en réalité façonnées par une industrie complexe.

L’objectif est d’explorer une question centrale :

**Comment l’industrie de la mode influence-t-elle les comportements et les décisions individuelles dans notre société ?**

À partir d’une enquête quantitative menée auprès de 428 répondants, ce projet combine science des données et sociologie de la mode pour analyser les paradoxes entre discours éthique, pression sociale et pratiques réelles.

---

## Problématique

Comment l’industrie de la mode impacte-t-elle le comportement et les choix vestimentaires ?

Plus précisément :
- Existe-t-il un décalage entre valeurs déclarées et comportements réels ?
- Quel rôle jouent les réseaux sociaux et les tendances ?
- Peut-on identifier des profils psychologiques de consommateurs ?

---

## Structure du projet

```
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
```

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

Cette section présente un ensemble de figures produites par le pipeline d’analyse.  
Elles synthétisent (i) les comportements d’achat, (ii) les tensions entre attitudes éthiques et pratiques de consommation, et (iii) une segmentation exploratoire (K-means) permettant de caractériser des profils de répondants.

> **Note** : les figures ci-dessous sont générées dans `reports/figures/`.  
> Si tu changes ton dossier de sortie, adapte simplement les chemins.

---

### 1) Le “Grand Paradoxe” : discours vs réalité
Cette visualisation met en évidence l’écart entre **déclarations éthiques** (score élevé de souci éthique) et **usage effectif** de la fast fashion. Elle permet d’identifier la part de répondants relevant d’un paradoxe (valeurs déclarées vs comportements observés) et de comparer ce phénomène aux autres groupes.

![Le Grand Paradoxe](reports/figures/grand_paradoxe.png)

---

### 2) Taux de paradoxe par âge
Le paradoxe (déclarer un fort souci éthique tout en consommant de la fast fashion) est ici analysé **par tranches d’âge**. L’objectif est de tester l’hypothèse d’un effet générationnel sur la dissonance entre valeurs et comportements.

![Paradoxe par âge](reports/figures/paradoxe_par_age.png)

---

### 3) Paradoxe éthique par canal d’achat
Cette figure compare le taux de paradoxe selon le **canal d’achat**. Elle éclaire le rôle possible des environnements de consommation (online/offline, seconde main, etc.) dans l’alignement – ou non – entre attitudes éthiques et pratiques.

![Paradoxe par canal](reports/figures/paradoxe_par_canal.png)

---

### 4) Fréquence d’achat (distribution)
Distribution descriptive des modalités de **fréquence d’achat**. Cette vue sert de base de contexte pour interpréter les analyses plus “comportementales” (fin de vie, fast fashion, clusters).

![Fréquence d’achat](reports/figures/dist_frequence_achat.png)

---

### 5) Canaux d’achat (multi-choix)
Comme la question est en **choix multiples**, la figure est construite après “explosion” des réponses (split sur `;`). Elle permet d’observer la hiérarchie des canaux (internet, magasin physique, seconde main, etc.).

![Canaux d’achat](reports/figures/dist_canaux_achat.png)

---

### 6) Destination de fin de vie (multi-choix)
Analyse de la **fin de vie des vêtements** (don, vente, stockage, recyclage, jet). Cette visualisation offre une lecture des pratiques de circularité (revente/don) vs pratiques de sortie (jet) au niveau global.

![Destination fin de vie](reports/figures/dist_destination_fin_vie.png)

---

### 7) Fin de vie par fréquence d’achat (comparaison en %)
Cette figure compare les options de fin de vie **en pourcentage, à l’intérieur de chaque groupe de fréquence d’achat**. Elle répond à une question analytique : les acheteurs fréquents ont-ils des comportements de fin de vie différents (don/vente/stockage/recyclage/jet) ?

![Fin de vie par fréquence](reports/figures/fin_de_vie_par_frequence.png)

---

### 8) Clustering : carte des renoncements (arbitrages par cluster)
À partir d’un clustering (K-means) sur des variables d’attitudes et préférences, cette figure compare les **moyennes** par cluster sur des dimensions clés (prix, qualité, confort, éthique, tendance). Elle aide à interpréter les clusters comme des **profils** d’arbitrage.

![Carte des renoncements](reports/figures/carte_renoncements_par_cluster.png)

---

### 9) Arbre de décision : règles associées au fait de payer +20% (éthique)
Un arbre de décision (profondeur limitée) fournit une lecture interprétable des **règles** associées à une disposition à payer davantage pour un produit éthique. L’objectif est exploratoire : identifier les variables (et seuils) les plus discriminants.

![Arbre de décision](reports/figures/arbre_decision_payer_plus.png)

---

### 10) Uniformisation des items “tendance” par cluster (heatmap)
Cette heatmap présente, par cluster, le **taux d’adoption (%)** d’items tendance (variables multi-choix transformées en dummies). Elle permet de visualiser la structure “style/produit” associée à chaque profil.

![Heatmap items par cluster](reports/figures/heatmap_items_par_cluster.png)

---

### 11) Obsolescence psychologique par cluster
Mesure synthétique du rejet du “démodé” (moyenne par cluster). Elle vise à relier la segmentation à une dimension psycho-sociale : la sensibilité à l’obsolescence symbolique.

![Obsolescence psychologique](reports/figures/obsolescence_psy_par_cluster.png)

---

### 12) Packs de tendances (réseau de co-achat)
Réseau construit à partir des corrélations entre items tendance (dummies). Les liens représentent des associations au-dessus d’un seuil, suggérant des **co-adoptions** récurrentes (“packs”) dans les réponses.

![Réseau items tendance](reports/figures/reseau_items_tendance.png)

---

### 13) Typologie des consommateurs (waffle chart)
Représentation en grille des clusters (1 carré ≈ 1 répondant). L’objectif est de donner une lecture immédiate de la **répartition** des profils dans l’échantillon.

![Waffle clusters](reports/figures/waffle_clusters_typologie.png)
---

### Lecture finale

Entre aspiration éthique et plaisir esthétique, la mode apparaît comme un espace de tension permanente.  
Ces visualisations proposent une approche analytique — mais assumée, sensible et contemporaine — de ce que signifie consommer la mode aujourd’hui.

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
