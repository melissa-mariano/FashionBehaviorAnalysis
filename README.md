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

> **Note :** certaines visualisations (Sankey) sont interactives et sont donc accessibles via un **lien** (fichier `.html`).  
> Les autres graphiques sont affichés directement en image.

---

### 1) Parcours & structure des comportements

#### 1.1 Sankey — parcours (3 étapes)
**Objectif :** visualiser le chemin le plus fréquent entre **achat → usage → fin de vie**.  
**Lecture :** plus le flux est épais, plus le parcours est courant.  
👉 [Ouvrir la visualisation Sankey — parcours (3 étapes)](reports/sankey_parcours_3_etapes.html)

#### 1.2 Sankey — cycle complet (4 étapes)
**Objectif :** représenter un cycle plus détaillé (4 étapes) pour observer les **enchaînements dominants**.  
**Lecture :** permet d’identifier des “autoroutes” comportementales et des parcours minoritaires.  
👉 [Ouvrir la visualisation Sankey — cycle complet (4 étapes)](reports/sankey_cycle_complet_4_etapes.html)

---

### 2) Segmentation (K-means) & personas

#### 2.1 Typologie des consommateurs (waffle chart)
**Objectif :** montrer la taille de chaque cluster de manière visuelle.  
**Lecture :** chaque carré = 1 répondant ; plus une couleur occupe d’espace, plus le cluster est représenté.  
![Typologie des consommateurs (waffle)](reports/waffle_clusters_typologie.png)

#### 2.2 Personas en 2D (PCA)
**Objectif :** projeter les individus sur un plan 2D pour voir si les clusters sont **distincts ou chevauchants**.  
**Lecture :** des groupes séparés indiquent une segmentation plus “nette”.  
![Personas PCA 2D](reports/personas_pca_2d.png)

#### 2.3 Heatmap — items par cluster
**Objectif :** comparer rapidement les clusters sur plusieurs variables clés (intensités/valeurs moyennes).  
**Lecture :** plus la case est marquée, plus la variable est élevée dans le cluster.  
![Heatmap items par cluster](reports/heatmap_items_par_cluster.png)

---

### 3) Réseaux sociaux, tendances & fast fashion

#### 3.1 Réseaux sociaux vs tendances — densité des réponses
**Objectif :** observer la relation entre **influence des réseaux** et **influence des tendances**.  
**Lecture :** les zones foncées indiquent les couples de réponses les plus fréquents.  
![Réseaux sociaux vs tendances](reports/reseaux_influence_vs_tendances.png)

#### 3.2 Distribution — influence des réseaux
**Objectif :** voir la répartition des notes d’influence des réseaux (1–10).  
**Lecture :** permet d’identifier si la population est plutôt “peu influencée” ou “très influencée”.  
![Distribution influence réseaux](reports/reseaux_dist_influence.png)

#### 3.3 Fast fashion selon l’influence des réseaux
**Objectif :** mesurer si une influence réseaux plus forte est associée à une pratique plus élevée de fast fashion.  
**Lecture :** comparer les niveaux/variations selon les groupes de score.  
![Fast fashion selon influence réseaux](reports/reseaux_fastfashion_selon_influence.png)

#### 3.4 Heatmap — corrélations (réseaux, tendances, fast fashion, etc.)
**Objectif :** synthétiser les liens entre variables (corrélations positives/négatives).  
**Lecture :** utile pour repérer des associations fortes à investiguer.  
![Heatmap corrélations réseaux](reports/reseaux_heatmap_correlations.png)

---

### 4) Culpabilité, éthique & paradoxe

#### 4.1 Heatmap — densité éthique vs culpabilité
**Objectif :** voir comment se répartissent les réponses entre **sensibilité éthique** et **culpabilité**.  
**Lecture :** les zones denses montrent les profils majoritaires.  
![Densité éthique vs culpabilité](reports/heatmap_densite_ethique_culpabilite.png)

#### 4.2 Boxplot — culpabilité par paradoxe
**Objectif :** comparer la culpabilité selon un indicateur de “paradoxe” (ex : conscience vs comportement).  
**Lecture :** médiane et dispersion : qui ressent le plus de culpabilité ?  
![Boxplot culpabilité par paradoxe](reports/boxplot_culpabilite_par_paradoxe.png)

#### 4.3 Le “grand paradoxe”
**Objectif :** mettre en évidence un profil type : **forte conscience / forte culpabilité** mais comportements qui ne suivent pas toujours.  
**Lecture :** visuel de synthèse pour appuyer l’argument du paradoxe.  
![Grand paradoxe](reports/grand_paradoxe.png)

#### 4.4 Paradoxe par âge
**Objectif :** voir si le paradoxe varie selon les tranches d’âge.  
**Lecture :** comparer les niveaux entre groupes d’âge.  
![Paradoxe par âge](reports/paradoxe_par_age.png)

#### 4.5 Paradoxe par canal d’achat
**Objectif :** tester si certains canaux (en ligne / boutique / seconde main…) sont associés à plus de paradoxe.  
**Lecture :** utile pour relier comportements et contexte d’achat.  
![Paradoxe par canal](reports/paradoxe_par_canal.png)

---

### 5) Obsolescence psychologique & dynamique d’achat

#### 5.1 Obsolescence psychologique par cluster
**Objectif :** comparer les clusters sur l’obsolescence psychologique (lassitude, envie de renouveler, etc.).  
**Lecture :** identifie les segments les plus exposés à l’achat impulsif / renouvellement rapide.  
![Obsolescence psychologique par cluster](reports/obsolescence_psy_par_cluster.png)

#### 5.2 Fast fashion — part par cluster
**Objectif :** visualiser quels clusters consomment le plus “fast fashion”.  
**Lecture :** repérer les segments prioritaires pour actions de sensibilisation.  
![Fast fashion % par cluster](reports/fastfashion_pct_par_cluster.png)

---

### 6) Fin de vie des vêtements & fréquence d’achat

#### 6.1 Distribution — fréquence d’achat
**Objectif :** comprendre le rythme d’achat dominant dans l’échantillon.  
**Lecture :** met en évidence les profils “achats fréquents” vs “achats occasionnels”.  
![Distribution fréquence achat](reports/dist_frequence_achat.png)

#### 6.2 Distribution — destination de fin de vie
**Objectif :** voir ce que deviennent majoritairement les vêtements (don, recyclage, poubelle, revente…).  
**Lecture :** indique les pratiques de fin de vie les plus courantes.  
![Distribution destination fin de vie](reports/dist_destination_fin_vie.png)

#### 6.3 Fin de vie selon la fréquence d’achat
**Objectif :** relier rythme d’achat et comportement de fin de vie.  
**Lecture :** utile pour identifier si l’achat fréquent est associé à plus de renoncements/déchets.  
![Fin de vie par fréquence](reports/fin_de_vie_par_frequence.png)

---

### 7) Canaux d’achat

#### 7.1 Distribution — canaux d’achat
**Objectif :** identifier les canaux dominants (sites, magasins, seconde main, etc.).  
**Lecture :** aide à contextualiser les comportements observés (ex : influence réseaux vs e-commerce).  
![Distribution canaux d’achat](reports/dist_canaux_achat.png)

---

### 8) Renoncements & arbitrages

#### 8.1 Carte — renoncements par cluster
**Objectif :** montrer les renoncements (ex : acheter moins, éviter certaines marques, etc.) selon les segments.  
**Lecture :** met en évidence les clusters les plus enclins à changer de comportement.  
![Renoncements par cluster](reports/carte_renoncements_par_cluster.png)

---

### 9) Modélisation explicative (arbre de décision)

#### 9.1 Arbre de décision — “payer plus” (exemple)
**Objectif :** expliquer les facteurs associés à la probabilité de “payer plus” (variable cible).  
**Lecture :** chaque nœud = une règle ; les branches montrent les combinaisons de facteurs qui mènent au résultat.  
![Arbre de décision — payer plus](reports/arbre_decision_payer_plus.png)

---

### 10) Focus “spirale” (si utilisée)

#### 10.1 Réseaux sociaux vs culpabilité (couleur = FF)
**Objectif :** explorer la co-variation entre influence des réseaux et culpabilité, avec indication fast fashion (FF).  
**Lecture :** utile pour illustrer un continuum, mais moins lisible qu’une densité/boxplot si trop de points.  
![Spirale culpabilité](reports/spirale_culpabilite_reseaux.png)

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
