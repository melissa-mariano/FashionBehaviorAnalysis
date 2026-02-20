# Analyse de l’Industrie de la Mode

## Problématique
Comment l’industrie de la mode impacte-t-elle le comportement et les choix de notre société ?

---

## Structure du projet

```
project_root/
│
├── data/                 # Contient le fichier CSV avec les données
│   └── La mode - LaMode.csv
│
├── notebooks/            # Contient les notebooks Jupyter
│   └── analyse_mode.ipynb
│
├── requirements.txt      # Dépendances Python nécessaires
│
└── README.md             # Documentation du projet
```

---

## Installation

1. **Cloner le projet**

```bash
git clone <URL_DU_PROJET>
cd project_root
```

2. **Créer un environnement virtuel** (optionnel mais recommandé)

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Windows (cmd)
venv\Scripts\activate.bat
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

---

## Contenu du projet

- **data/**  
  Contient le fichier CSV issu de l’enquête sur les comportements liés à la mode (`La mode - LaMode.csv`).

- **notebooks/**  
  Contient le notebook `analyse_mode.ipynb` avec l’ensemble des analyses, visualisations et calculs.

- **requirements.txt**  
  Liste des bibliothèques Python nécessaires à l’exécution du notebook.

---

## Utilisation

1. Lancer Jupyter Notebook :

```bash
jupyter notebook notebooks/analyse_mode.ipynb
```

2. Exécuter les cellules dans l’ordre pour :

- Nettoyer et standardiser les données (par ex. `df_clean`)  
- Créer des visualisations :
  - Diagrammes de Sankey
  - Graphiques en barres
  - Graphiques radar
  - Scatter plots
  - Heatmaps
- Calculer l’indice **« Fashion Victim »**  
- Identifier des **personas** de consommateurs

---

## Dépendances principales

- pandas  
- numpy  
- matplotlib  
- seaborn  
- plotly  
- scikit-learn  
- networkx

> Ajoutez d’autres packages dans `requirements.txt` si le notebook les utilise (ex. `pdfplumber`, `langdetect`, `spacy`, etc.).

---

## Objectifs du projet

- Explorer le comportement des consommateurs dans l’industrie de la mode  
- Identifier les contradictions entre intentions éthiques et comportements réels  
- Visualiser les habitudes d’achat et les influences sociales  
- Construire des personas et des indices pour analyser les tendances

---

## Structure du notebook (résumé des étapes)

1. Chargement des données (`data/La mode - LaMode.csv`)  
2. Inspection initiale et traitement des valeurs manquantes  
3. Nettoyage et standardisation (normalisation des colonnes, unification des langues, conversion de formats)  
4. Feature engineering (calcul de l’indice « Fashion Victim », création de variables catégorielles)  
5. Visualisations exploratoires et storytelling (Sankey, barres, radars, scatter, heatmaps)  
6. Clustering / segmentation pour créer des personas  
7. Synthèse et recommandations

---

## Auteur

Melissa Albuquerque