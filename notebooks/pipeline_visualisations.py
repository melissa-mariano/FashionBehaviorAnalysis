# -*- coding: utf-8 -*-
"""
notebook_visualisations.py  (mode notebook VS Code avec cellules #%%)

But :
- Reprendre le pipeline robuste (détection colonnes) + ajouter TOUTES les visualisations “valeur”
- À exécuter en mode notebook (VS Code : Python: Run Cell / Run All)

Sorties :
- reports/figures/*.png
- reports/*.html
- reports/*.csv
"""

#%% =========================
# 0) IMPORTS & CONFIG (clean)
# =========================
from __future__ import annotations

from pathlib import Path
import re
import unicodedata
import warnings

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from cycler import cycler

import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier, plot_tree

#%% =========================
# 0B) PALETTE (UNIQUE) : Cerulean
# =========================
PALETTE = {
    "CERULEAN_DARK":  "#005B82",  # cerulean foncé
    "CERULEAN":       "#007BA7",  # cerulean classic
    "CERULEAN_LIGHT": "#4FB6E1",  # clair
    "CERULEAN_SOFT":  "#A7D8F0",  # très clair
    "NAVY":           "#083D5B",  # contraste bleu nuit
    "GRID":           "#D6EAF5",  # grid léger bleu
    "GRIS_CLAIR":     "#E9ECEF",
    "NOIR":           "#0B1D26",
}


#%% =========================
# 0C) COLORMAP (UNIQUE) : Heatmaps cerulean
# =========================
CERULEAN_CMAP = mcolors.LinearSegmentedColormap.from_list(
    "cerulean_cmap",
    ["#F3FBFF", PALETTE["CERULEAN_SOFT"], PALETTE["CERULEAN_LIGHT"], PALETTE["CERULEAN"], PALETTE["CERULEAN_DARK"]],
    N=256
)

#%% =========================
# 0D) DESIGN SYSTEM (premium look)
#     -> objectif: mêmes marges, même typo, même grille, même lisibilité
# =========================
def apply_design_system() -> None:
    """Applique un thème global Matplotlib cohérent (à appeler une seule fois au début)."""
    plt.rcParams.update({
        # canvas
        "figure.facecolor": "white",
        "axes.facecolor": "white",

        # contours & texte
        "axes.edgecolor": PALETTE["CERULEAN_DARK"],
        "axes.labelcolor": PALETTE["CERULEAN_DARK"],
        "text.color": PALETTE["CERULEAN_DARK"],
        "xtick.color": PALETTE["CERULEAN_DARK"],
        "ytick.color": PALETTE["CERULEAN_DARK"],

        # grid “soft”
        "axes.grid": True,
        "grid.color": PALETTE["GRID"],
        "grid.linestyle": "-",
        "grid.linewidth": 0.8,

        # typographie (simple mais propre)
        "axes.titlesize": 18,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,

        # légende
        "legend.frameon": True,
        "legend.framealpha": 0.95,
        "legend.edgecolor": PALETTE["GRID"],
    })

    # cycle de couleurs (évite couleurs random)
    plt.rcParams["axes.prop_cycle"] = cycler(color=[
        PALETTE["CERULEAN_DARK"],
        PALETTE["CERULEAN"],
        PALETTE["CERULEAN_LIGHT"],
        PALETTE["NAVY"],
    ])

def set_editorial_axes(ax: plt.Axes, title: str | None = None, xlabel: str | None = None, ylabel: str | None = None) -> None:
    """Uniformise un axe (respiration + style)."""
    if title:
        ax.set_title(title, pad=18, fontweight="bold")
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # enlève le “cadre” trop lourd en haut/droite
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # grid légère uniquement en y (souvent plus chic)
    ax.grid(True, axis="y", alpha=0.35)
    ax.grid(False, axis="x")

    # marge interne (évite éléments collés)
    ax.margins(x=0.05, y=0.08)


def export_png(path: Path) -> None:
    """Export propre: marges + bbox pour éviter titres collés."""
    # IMPORTANT: tight_layout AVANT savefig
    plt.tight_layout(pad=1.6)
    plt.savefig(path, dpi=240, bbox_inches="tight")
    plt.close()


# applique le design system une fois
apply_design_system()

#%% =========================
# 0E) PATHS / OUTPUTS
# =========================
DATA_PATH = Path("data") / "La mode - LaMode.csv"

OUT_DIR = Path("reports")
FIG_DIR = OUT_DIR / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

#%% =========================
# 0F) TEXT / NUM HELPERS (tes fonctions)
# =========================
def norm_text(s: str) -> str:
    s = str(s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def safe_to_numeric(series: pd.Series) -> pd.Series:
    # gère virgules FR "7,5"
    s = series.astype(str).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


from pandas.api.types import is_string_dtype
def map_likert_fr_to_num(series: pd.Series) -> pd.Series:
    if not is_string_dtype(series):
        return series

    m = {
        "jamais": 1,
        "rarement": 2,
        "parfois": 3,
        "souvent": 4,
        "toujours": 5,
        "pas du tout": 1,
        "peu": 2,
        "assez": 3,
        "beaucoup": 4,
        "enormement": 5,
        "énormément": 5,
    }

    def conv(x):
        if pd.isna(x):
            return np.nan
        t = norm_text(x)
        try:
            return float(t)
        except ValueError:
            pass
        for k, v in m.items():
            if k in t:
                return float(v)
        return np.nan
    return series.apply(conv)

#%% =========================
# DÉTECTION / RENOMMAGE ROBUSTE
# =========================
def rename_robuste(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    mapping: dict[str, str] = {}
    cols_norm = {c: norm_text(c) for c in df.columns}

    def pick_col(predicate) -> str | None:
        for c, nc in cols_norm.items():
            if predicate(nc):
                return c
        return None

    # --- profil
    c = pick_col(lambda nc: "quel est votre age" in nc or nc == "age" or "age ?" in nc)
    if c: mapping[c] = "Age"

    c = pick_col(lambda nc: "etes-vous" in nc or "êtes-vous" in nc)
    if c: mapping[c] = "Genre"

    c = pick_col(lambda nc: "situation professionnelle" in nc and "precisez" not in nc)
    if c: mapping[c] = "Situation_Pro"

    # --- parcours d'achat
    c = pick_col(lambda nc: "tous les combien de temps achetez" in nc or ("frequence" in nc and "achetez" in nc))
    if c: mapping[c] = "Frequence_Achat"

    c = pick_col(lambda nc: "ou achetez-vous" in nc or "où achetez-vous" in nc)
    if c: mapping[c] = "Canal_Achat"

    c = pick_col(lambda nc: ("cycle de vie moyen" in nc and "garde-robe" in nc) or ("cycle de vie moyen" in nc))
    if c: mapping[c] = "Duree_Vie_GardeRobe"

    c = pick_col(lambda nc: ("que faites-vous le plus souvent" in nc and "vous separer" in nc) or ("recycle" in nc and "jette" in nc))
    if c: mapping[c] = "Destination_Fin_Vie"

    c = pick_col(lambda nc: "apres avoir achete" in nc and "jamais portes" in nc or "jamais etre portes" in nc)
    if c: mapping[c] = "Vetements_Jamais_Portes"

    # --- matrice importance
    def pick_importance(keyword: str) -> str | None:
        return pick_col(lambda nc: "caracteristiques suivantes" in nc and keyword in nc)

    c = pick_importance("prix")
    if c: mapping[c] = "Importance_Prix"
    c = pick_importance("qualite")
    if c: mapping[c] = "Importance_Qualite"
    c = pick_importance("marque")
    if c: mapping[c] = "Importance_Marque"
    c = pick_importance("confort")
    if c: mapping[c] = "Importance_Confort"
    c = pick_importance("mode")
    if c: mapping[c] = "Importance_Tendance"
    if not any(v == "Importance_Tendance" for v in mapping.values()):
        c = pick_importance("tendance")
        if c: mapping[c] = "Importance_Tendance"

    # --- influence & psycho
    c = pick_col(lambda nc: "tendances actuelles" in nc and "influenc" in nc)
    if c: mapping[c] = "Influence_Tendances"

    c = pick_col(lambda nc: "reseaux sociaux" in nc and ("dict" in nc or "influenc" in nc))
    if c: mapping[c] = "Influence_Reseaux"

    c = pick_col(lambda nc: "pression sociale" in nc)
    if c: mapping[c] = "Pression_Sociale"

    c = pick_col(lambda nc: ("evite" in nc and "plus a la mode" in nc) or ("evité" in nc and "plus a la mode" in nc))
    if c: mapping[c] = "Peur_Etre_Demode"

    c = pick_col(lambda nc: "confiance en vous" in nc or ("vetements" in nc and "confiance" in nc))
    if c: mapping[c] = "Impact_Confiance"

    c = pick_col(lambda nc: "culpabil" in nc)
    if c: mapping[c] = "Sentiment_Culpabilite"

    # --- fast fashion
    c = pick_col(lambda nc: "concept de" in nc and "fast fashion" in nc)
    if c: mapping[c] = "Connaissance_FastFashion"

    c = pick_col(lambda nc: ("avez-vous deja consomme" in nc or "avez-vous déjà consommé" in nc)
                          and ("fast fashion" in nc)
                          and ("shein" in nc or "temu" in nc or "plateforme" in nc))
    if c: mapping[c] = "Utilise_FastFashion"

    c = pick_col(lambda nc: "raisons achetez-vous" in nc and "fast fashion" in nc)
    if c: mapping[c] = "Motivations_FastFashion"

    # --- articles achetés (choix multiples)
    c = pick_col(lambda nc:
        ("acheté certains de ces articles" in nc)
        or ("achete certains de ces articles" in nc)
        or ("certains de ces articles" in nc and "choix" in nc)
    )
    if c:
        mapping[c] = "Type_Articles_Achetes"


    # --- éthique / prix
    c = pick_col(lambda nc: "considerations ethique" in nc or ("ethique" in nc and "environnement" in nc))
    if c: mapping[c] = "Souci_Ethique"

    c = pick_col(lambda nc: "20 %" in nc and ("pret" in nc or "prêt" in nc))
    if c: mapping[c] = "Pret_A_Payer_Plus"

    df2 = df.rename(columns=mapping)
    return df2, mapping


#%% =========================
# CHARGEMENT
# =========================
if not DATA_PATH.exists():
    raise FileNotFoundError(f"CSV introuvable : {DATA_PATH.resolve()}")

df_raw = pd.read_csv(DATA_PATH)
df, mapping = rename_robuste(df_raw)

# corrige colunas duplicadas (ex: Canal_Achat que virou DataFrame)
df = df.loc[:, ~df.columns.duplicated()].copy()


print("OK - Données chargées.")
print(f"Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")

# Diagnostic exporté
diag_lines = ["=== DIAGNOSTIC COLONNES (original -> standard) ==="]
for k, v in mapping.items():
    diag_lines.append(f"- {k}  -->  {v}")
(OUT_DIR / "diagnostic_colonnes.txt").write_text("\n".join(diag_lines), encoding="utf-8")
print("OK - Diagnostic exporté : reports/diagnostic_colonnes.txt")


#%% =========================
# PRÉPARATION NUMÉRIQUE (colonnes clés)
# =========================
# conversions robustes (si présentes)
num_10 = [
    "Souci_Ethique", "Pret_A_Payer_Plus",
    "Influence_Tendances", "Influence_Reseaux",
    "Impact_Confiance",
    "Importance_Prix", "Importance_Qualite", "Importance_Marque", "Importance_Tendance", "Importance_Confort",
    "Sentiment_Culpabilite",
]

for c in num_10:
    if c in df.columns:
        df[c] = safe_to_numeric(df[c])

likert_5 = ["Pression_Sociale", "Peur_Etre_Demode", "Vetements_Jamais_Portes"]
for c in likert_5:
    if c in df.columns:
        df[c] = map_likert_fr_to_num(df[c])


#%% =========================
# 1) GRAND PARADOXE (global)
# =========================
req = ["Souci_Ethique", "Utilise_FastFashion"]
if all(c in df.columns for c in req):
    d = df.copy()

    # 1) FastFashion: on force une lecture Oui/Non, sinon NaN -> "Autres"
    ff_txt = d["Utilise_FastFashion"].astype(str).str.strip().str.lower()

    d["FF"] = np.select(
        [
            ff_txt.str.contains(r"\boui\b", na=False),
            ff_txt.str.contains(r"\bnon\b", na=False),
        ],
        [1, 0],
        default=np.nan
    )

    # 2) Souci éthique: numeric + seuil
    d["Souci_Ethique_num"] = pd.to_numeric(d["Souci_Ethique"], errors="coerce")
    d["Ethique_Haute"] = d["Souci_Ethique_num"] >= 7

    # 3) Groupes (4 cas) + Autres = seulement si on ne peut pas classer
    d["Comportement"] = "Autres (données manquantes / non interprétables)"

    d.loc[d["Ethique_Haute"] & (d["FF"] == 1), "Comportement"] = (
        "Souci éthique élevé, mais achat de fast fashion"
    )
    d.loc[(~d["Ethique_Haute"]) & (d["FF"] == 1), "Comportement"] = (
        "Souci éthique faible, et achat de fast fashion"
    )
    d.loc[d["Ethique_Haute"] & (d["FF"] == 0), "Comportement"] = (
        "Souci éthique élevé, et pas de fast fashion (cohérent)"
    )
    d.loc[(~d["Ethique_Haute"]) & (d["FF"] == 0), "Comportement"] = (
        "Souci éthique faible, et pas de fast fashion"
    )

    # 4) Pourcentages + ordre (labels non abrégés)
    counts = d["Comportement"].value_counts(normalize=True) * 100

    order = [
        "Souci éthique élevé, mais achat de fast fashion",
        "Souci éthique faible, et achat de fast fashion",
        "Souci éthique élevé, et pas de fast fashion (cohérent)",
        "Souci éthique faible, et pas de fast fashion",
        "Autres (données manquantes / non interprétables)",
    ]
    counts = counts.reindex(order).fillna(0)

    # 5) Plot
    plt.figure(figsize=(12, 6))
    plt.barh(counts.index, counts.values, edgecolor="black")
    plt.gca().invert_yaxis()
    plt.title("Le Grand Paradoxe : discours vs réalité", fontweight="bold")
    plt.xlabel("%")
    plt.ylabel("")
    export_png(FIG_DIR / "grand_paradoxe.png")

    # (Optionnel) debug: voir ce que contient "Autres"
    # print(d.loc[d["Comportement"].str.startswith("Autres"), "Utilise_FastFashion"].value_counts(dropna=False).head(20))

else:
    warnings.warn("Grand paradoxe ignoré (colonnes manquantes).")


#%% =========================
# 1B) GRAND PARADOXE PAR ÂGE (buckets)
# =========================
req = ["Age", "Souci_Ethique", "Utilise_FastFashion"]
if all(c in df.columns for c in req):
    d = df.dropna(subset=["Age", "Souci_Ethique", "Utilise_FastFashion"]).copy()
    d["FF_Oui"] = d["Utilise_FastFashion"].astype(str).str.contains("oui", case=False, na=False)
    d["Ethique_Haute"] = d["Souci_Ethique"] >= 7
    d["Paradoxe"] = (d["Ethique_Haute"] & d["FF_Oui"]).astype(int)

    # buckets simples
    bins = [0, 18, 24, 34, 44, 54, 64, 120]
    labels = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    d["Age_Groupe"] = pd.cut(d["Age"], bins=bins, labels=labels, include_lowest=True)

    grp = d.groupby("Age_Groupe", observed=False)["Paradoxe"].mean() * 100
    plt.figure(figsize=(10, 5))
    plt.plot(grp.index.astype(str), grp.values, marker="o")
    plt.title("Taux de paradoxe (DIT éthique MAIS FF) par âge", fontweight="bold")
    plt.ylabel("% du groupe")
    plt.xlabel("Groupe d'âge")
    plt.grid(True, linestyle="--", alpha=0.4)
    export_png(FIG_DIR / "paradoxe_par_age.png")
else:
    warnings.warn("Paradoxe par âge ignoré.")


#%% =========================
# 1C) GRAND PARADOXE PAR CANAL
# =========================
req = ["Canal_Achat", "Souci_Ethique", "Utilise_FastFashion"]
if all(c in df.columns for c in req):
    d = df.dropna(subset=req).copy()
    d["FF_Oui"] = d["Utilise_FastFashion"].astype(str).str.contains("oui", case=False, na=False)
    d["Ethique_Haute"] = d["Souci_Ethique"] >= 7
    d["Paradoxe"] = (d["Ethique_Haute"] & d["FF_Oui"]).astype(int)

    grp = d.groupby("Canal_Achat")["Paradoxe"].mean().sort_values(ascending=False) * 100
    plt.figure(figsize=(10, 5))
    plt.bar(grp.index.astype(str), grp.values, edgecolor="black")
    plt.title("Paradoxe éthique par canal d'achat", fontweight="bold")
    plt.ylabel("% (DIT éthique MAIS FF)")
    plt.xticks(rotation=20, ha="right")
    export_png(FIG_DIR / "paradoxe_par_canal.png")
else:
    warnings.warn("Paradoxe par canal ignoré.")


def split_multi(series: pd.Series, sep=";") -> pd.Series:
    # retorna lista de escolhas por linha
    return series.fillna("Non spécifié").astype(str).apply(
        lambda x: [t.strip() for t in x.split(sep) if t.strip()] if sep in x else [x.strip()]
    )

def top_n_with_other(series: pd.Series, n=6, other="Autres") -> pd.Series:
    vc = series.value_counts()
    top = set(vc.head(n).index)
    return series.apply(lambda x: x if x in top else other)

#%% =========================
# 2) SANKEY ÉTENDU (cycle complet si possible)
# =========================
# Variante courte : 3 étapes (toujours)
if all(c in df.columns for c in ["Frequence_Achat", "Canal_Achat", "Utilise_FastFashion"]):
    d0 = df[["Frequence_Achat", "Canal_Achat", "Utilise_FastFashion"]].copy()

    # explode Canal_Achat (multi-choix)
    d0["Canal_Achat_list"] = split_multi(d0["Canal_Achat"], sep=";")
    d = (
        d0
        .explode("Canal_Achat_list")
        .drop(columns=["Canal_Achat"])   # <- remove a coluna original
        .rename(columns={"Canal_Achat_list": "Canal_Achat"})
    )
    # nettoyer labels + réduire cardinalité
    d["Frequence_Achat"] = d["Frequence_Achat"].fillna("Non spécifié").astype(str).str.strip()
    ca = d["Canal_Achat"]
    if isinstance(ca, pd.DataFrame):
        ca = ca.bfill(axis=1).iloc[:, 0]
    d["Canal_Achat"] = ca
    d["Canal_Achat"] = d["Canal_Achat"].fillna("Non spécifié").astype(str).str.strip()
    d["Utilise_FastFashion"] = d["Utilise_FastFashion"].fillna("Non spécifié").astype(str).str.strip()

    d["Canal_Achat"] = top_n_with_other(d["Canal_Achat"], n=6, other="Autres canaux")
    d["Frequence_Achat"] = top_n_with_other(d["Frequence_Achat"], n=6, other="Autres fréquences")

    cols = ["Frequence_Achat", "Canal_Achat", "Utilise_FastFashion"]
    grouped = d.groupby(cols).size().reset_index(name="count")

    labels_list, sources, targets, values = [], [], [], []

    def idx(x: str) -> int:
        if x not in labels_list:
            labels_list.append(x)
        return labels_list.index(x)

    for _, r in grouped.iterrows():
        s = idx(str(r[cols[0]])); t = idx(str(r[cols[1]]))
        sources.append(s); targets.append(t); values.append(int(r["count"]))
        s = t; t = idx(str(r[cols[2]]))
        sources.append(s); targets.append(t); values.append(int(r["count"]))

    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=18, label=labels_list, color=PALETTE["CERULEAN"]),
        link=dict(source=sources, target=targets, value=values)
    )])
    fig.update_layout(title_text="Parcours consommateur (Sankey nettoyé)", font_size=10)
    fig.write_html(OUT_DIR / "sankey_parcours_3_etapes.html", include_plotlyjs="cdn")
    print("OK - Sankey nettoyé : reports/sankey_parcours_3_etapes.html")

# Variante longue : 4 étapes (si Destination_Fin_Vie existe)
if all(c in df.columns for c in ["Frequence_Achat", "Canal_Achat", "Utilise_FastFashion", "Destination_Fin_Vie"]):
    d0 = df[["Frequence_Achat", "Canal_Achat", "Utilise_FastFashion", "Destination_Fin_Vie"]].copy()

    # explode multi-choix
    d0["Canal_Achat_list"] = split_multi(d0["Canal_Achat"], sep=";")
    d0["FinVie_list"] = split_multi(d0["Destination_Fin_Vie"], sep=";")

    d = (
        d0
        .explode("Canal_Achat_list")
        .explode("FinVie_list")
        .drop(columns=["Canal_Achat", "Destination_Fin_Vie"])  # <- remove as originais
        .rename(columns={"Canal_Achat_list": "Canal_Achat", "FinVie_list": "Destination_Fin_Vie"})
    )

    # nettoyage + réduction cardinalité
    d["Frequence_Achat"] = d["Frequence_Achat"].fillna("Non spécifié").astype(str).str.strip()
    ca = d["Canal_Achat"]
    if isinstance(ca, pd.DataFrame):
        ca = ca.bfill(axis=1).iloc[:, 0]
    d["Canal_Achat"] = ca
    d["Canal_Achat"] = d["Canal_Achat"].fillna("Non spécifié").astype(str).str.strip()
    d["Utilise_FastFashion"] = d["Utilise_FastFashion"].fillna("Non spécifié").astype(str).str.strip()
    d["Destination_Fin_Vie"] = d["Destination_Fin_Vie"].fillna("Non spécifié").astype(str).str.strip()

    d["Canal_Achat"] = top_n_with_other(d["Canal_Achat"], n=6, other="Autres canaux")
    d["Frequence_Achat"] = top_n_with_other(d["Frequence_Achat"], n=6, other="Autres fréquences")
    d["Destination_Fin_Vie"] = top_n_with_other(d["Destination_Fin_Vie"], n=6, other="Autres destinations")

    cols = ["Frequence_Achat", "Canal_Achat", "Utilise_FastFashion", "Destination_Fin_Vie"]
    grouped = d.groupby(cols).size().reset_index(name="count")

    labels_list, sources, targets, values = [], [], [], []
    def idx(x: str) -> int:
        if x not in labels_list:
            labels_list.append(x)
        return labels_list.index(x)

    for _, r in grouped.iterrows():
        s = idx(str(r[cols[0]])); t = idx(str(r[cols[1]]))
        sources.append(s); targets.append(t); values.append(int(r["count"]))
        s = t; t = idx(str(r[cols[2]]))
        sources.append(s); targets.append(t); values.append(int(r["count"]))
        s = t; t = idx(str(r[cols[3]]))
        sources.append(s); targets.append(t); values.append(int(r["count"]))

    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=18, label=labels_list, color=PALETTE["CERULEAN"]),
        link=dict(source=sources, target=targets, value=values)
    )])
    fig.update_layout(title_text="Cycle complet (Sankey - 4 étapes, nettoyé)", font_size=10)
    fig.write_html(OUT_DIR / "sankey_cycle_complet_4_etapes.html", include_plotlyjs="cdn")
    print("OK - Sankey 4 étapes nettoyé : reports/sankey_cycle_complet_4_etapes.html")


#%% =========================
# 3) CARTE DU MENSONGE CONFORTABLE : Éthique vs FF, couleur = culpabilité
# =========================
req = ["Souci_Ethique", "Utilise_FastFashion", "Sentiment_Culpabilite"]
if all(c in df.columns for c in req):
    d = df.dropna(subset=req).copy()
    d["FF_Oui"] = d["Utilise_FastFashion"].astype(str).str.contains("oui", case=False, na=False).astype(int)

    # scatter : éthique (x), culpabilité (y), taille/couleur selon FF
    plt.figure(figsize=(10, 6))
    x = d["Souci_Ethique"].values
    y = d["Sentiment_Culpabilite"].values
    c = d["FF_Oui"].values
    plt.scatter(x, y, c=c, cmap="coolwarm", alpha=0.6)
    plt.title("Éthique vs Culpabilité (couleur = Fast Fashion)", fontweight="bold")
    plt.xlabel("Souci éthique (1–10)")
    plt.ylabel("Culpabilité (1–10)")
    plt.grid(True, linestyle="--", alpha=0.3)
    export_png(FIG_DIR / "ethique_vs_culpabilite_couleur_ff.png")
else:
    warnings.warn("Éthique vs culpabilité ignoré.")


#%% =========================
# 4) RÉSEAU / PACKS DE TENDANCES : co-achat des items tendance
# =========================
if "Type_Articles_Achetes" in df.columns:
    items = df["Type_Articles_Achetes"].dropna().astype(str)
    dummies = items.str.get_dummies(sep=";")
    if dummies.shape[1] >= 2:
        corr = dummies.corr()

        # Construire une liste d'arêtes fortes
        threshold = 0.15
        edges = []
        cols = corr.columns.tolist()
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                w = corr.iloc[i, j]
                if w > threshold:
                    edges.append((cols[i], cols[j], float(w)))

        # Visualisation "réseau" simple sans networkx :
        # on place les noeuds sur un cercle, et on trace les liens.
        nodes = cols
        n = len(nodes)
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        pos = {nodes[i]: (np.cos(angles[i]), np.sin(angles[i])) for i in range(n)}

        plt.figure(figsize=(11, 11))
        # liens
        for a, b, w in edges:
            xa, ya = pos[a]
            xb, yb = pos[b]
            link_color = PALETTE["CERULEEN"] if w >= 0.30 else PALETTE["CERULEAN"]
            plt.plot(
                [xa, xb],
                [ya, yb],
                linewidth=1 + 4*w,
                 alpha=0.65,
                color=link_color,
                zorder=1
            )
        # noeuds
        sizes = (dummies.sum().reindex(nodes).fillna(0).values + 1) * 30
        xs = [pos[k][0] for k in nodes]
        ys = [pos[k][1] for k in nodes]
        plt.scatter(xs, ys, s=sizes, color=PALETTE["CERULEAN"], alpha=0.95, edgecolor="black", linewidth=0.8, zorder=3)

        # labels
        for k in nodes:
            x, y = pos[k]
            plt.text(x*1.18, y*1.18, k.strip(), ha="center", va="center", color= "black", fontsize=12, zorder=4)

        plt.title(f"Packs de tendances (corrélation > {threshold})", fontsize=24, fontweight="bold", pad=22)
        plt.xlim(-1.35, 1.35)
        plt.ylim(-1.35, 1.35)
        plt.axis("off")
        export_png(FIG_DIR / "reseau_items_tendance.png")
    else:
        warnings.warn("Réseau items ignoré (pas assez d'items).")
else:
    warnings.warn("Réseau items ignoré (colonne manquante).")


#%% =========================
# 5) CLUSTERING (Personas) + exports + visus
# =========================
features = [
    "Age",
    "Influence_Tendances",
    "Influence_Reseaux",
    "Impact_Confiance",
    "Importance_Prix",
    "Importance_Qualite",
    "Importance_Marque",
    "Importance_Tendance",
    "Importance_Confort",
]
available = [c for c in features if c in df.columns]
if len(available) >= 4:
    d = df[available].copy()

    # conversions numeric déjà faites, mais on sécurise
    for c in available:
        d[c] = safe_to_numeric(d[c])

    # imputation simple
    d = d.fillna(d.median(numeric_only=True)).dropna()
    if len(d) >= 30:
        scaler = StandardScaler()
        X = scaler.fit_transform(d[available])

        # === ÉVALUATION DU NOMBRE DE CLUSTERS ===
        from sklearn.metrics import silhouette_score
        inertias = []
        silhouettes = []
        K = range(2, 9)

        for k in K:
            km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
            labels = km.fit_predict(X)
            inertias.append(km.inertia_)
            silhouettes.append(silhouette_score(X, labels))
        
        df_kmeans_eval = pd.DataFrame({
            "k": list(K),
            "inertia": inertias,
            "silhouette": silhouettes
        })

        df_kmeans_eval.to_csv(OUT_DIR / "kmeans_elbow_silhouette.csv", index=False)
        print("OK - Export : reports/kmeans_elbow_silhouette.csv")

        kmeans = KMeans(n_clusters=4, random_state=RANDOM_STATE, n_init=10)
        d["Cluster"] = kmeans.fit_predict(X)

        # join contexte utile
        ctx_cols = [c for c in ["Utilise_FastFashion", "Souci_Ethique", "Pression_Sociale", "Sentiment_Culpabilite", "Peur_Etre_Demode", "Type_Articles_Achetes", "Canal_Achat"] if c in df.columns]
        d_ctx = df.loc[d.index, ctx_cols].copy() if ctx_cols else pd.DataFrame(index=d.index)
        df_cluster = pd.concat([d, d_ctx], axis=1)

        df_cluster.to_csv(OUT_DIR / "personas_clusters.csv", index=False)
        print("OK - Export : reports/personas_clusters.csv")

        # scatter matplotlib pur (âge vs réseaux)
        if "Age" in df_cluster.columns and "Influence_Reseaux" in df_cluster.columns:
            plt.figure(figsize=(10, 6))
            plt.scatter(df_cluster["Age"], df_cluster["Influence_Reseaux"], c=df_cluster["Cluster"], cmap="tab10", alpha=0.75)
            plt.title("Clusters (K-Means) : Âge vs Influence réseaux", fontweight="bold")
            plt.xlabel("Âge"); plt.ylabel("Influence réseaux")
            export_png(FIG_DIR / "personas_scatter.png")

        # moyennes par cluster (table)
        means = df_cluster.groupby("Cluster")[available].mean().round(2)
        means.to_csv(OUT_DIR / "personas_moyennes_par_cluster.csv")
        print("OK - Export : reports/personas_moyennes_par_cluster.csv")

    else:
        warnings.warn("Clustering ignoré (pas assez de lignes après nettoyage).")
        df_cluster = None
else:
    warnings.warn("Clustering ignoré (pas assez de variables).")
    df_cluster = None


#%% =========================
# 6) HEATMAP UNIFORMISATION : % adoption items par cluster
# =========================
import seaborn as sns
import matplotlib.colors as mcolors

CERULEAN_CMAP = mcolors.LinearSegmentedColormap.from_list(
    "cerulean",
    ["#F3FBFF", "#A9D6E5", "#61A5C2", "#2A6F97", "#0047AB"],
    N=256
)

if df_cluster is not None and "Type_Articles_Achetes" in df_cluster.columns:
    items = df_cluster["Type_Articles_Achetes"].dropna().astype(str)
    dummies = items.str.get_dummies(sep=";")

    if dummies.shape[1] >= 1:
        temp = pd.concat([df_cluster["Cluster"], dummies], axis=1).fillna(0)
        pct = temp.groupby("Cluster").mean() * 100

        plt.figure(figsize=(14, 6))
        ax = sns.heatmap(
            pct,
            cmap=CERULEAN_CMAP,
            vmin=0, vmax=100,
            linewidths=0.5,
            linecolor="white",
            cbar_kws={"label": "% d'adoption"}
        )

        ax.set_title("Uniformisation : articles tendance par cluster (% adoption)", fontweight="bold")
        ax.set_xlabel("")
        ax.set_ylabel("")
        plt.xticks(rotation=30, ha="right")
        plt.yticks(rotation=0)

        export_png(FIG_DIR / "heatmap_items_par_cluster.png")
    else:
        warnings.warn("Heatmap items ignorée (pas d'items).")
else:
    warnings.warn("Heatmap items ignorée.")


#%% =========================
# 7) OBSOLESCENCE PSYCHOLOGIQUE : peur d'être démodé par cluster
# =========================
if df_cluster is not None and "Peur_Etre_Demode" in df_cluster.columns:
    d = df_cluster.dropna(subset=["Peur_Etre_Demode"]).copy()
    grp = d.groupby("Cluster")["Peur_Etre_Demode"].mean().sort_index()
    plt.figure(figsize=(8, 5))
    plt.bar([f"Cluster {i}" for i in grp.index], grp.values, edgecolor="black")
    plt.ylim(1, 5)
    plt.title("Obsolescence psychologique : rejet du 'démodé' (moyenne)", fontweight="bold")
    plt.ylabel("Niveau (1=Jamais, 5=Toujours)")
    export_png(FIG_DIR / "obsolescence_psy_par_cluster.png")
else:
    warnings.warn("Obsolescence psycho ignorée.")


#%% =========================
# 8) SPIRALE CULPABILITÉ : influence réseaux vs culpabilité, couleur FF
# =========================
req = ["Influence_Reseaux", "Sentiment_Culpabilite", "Utilise_FastFashion"]
if all(c in df.columns for c in req):
    d = df.dropna(subset=req).copy()
    d["FF_Oui"] = d["Utilise_FastFashion"].astype(str).str.contains("oui", case=False, na=False).astype(int)

    plt.figure(figsize=(10, 6))
    plt.scatter(d["Influence_Reseaux"], d["Sentiment_Culpabilite"], c=d["FF_Oui"], cmap="coolwarm", alpha=0.55)
    plt.title("Spirale de la culpabilité : Réseaux sociaux vs Culpabilité (couleur = FF)", fontweight="bold")
    plt.xlabel("Influence réseaux (1–10)")
    plt.ylabel("Culpabilité (1–10)")
    plt.grid(True, linestyle="--", alpha=0.3)
    export_png(FIG_DIR / "spirale_culpabilite_reseaux.png")
else:
    warnings.warn("Spirale culpabilité ignorée.")


#%% =========================
# 9) CARTE DES RENONCEMENTS : prix/qualité/confort/éthique/tendance par cluster
# =========================
if df_cluster is not None:
    cols = [c for c in ["Importance_Prix", "Importance_Qualite", "Importance_Confort", "Souci_Ethique", "Importance_Tendance"] if c in df_cluster.columns]
    if len(cols) >= 3:
        grp = df_cluster.groupby("Cluster")[cols].mean().round(2)

        x = np.arange(len(cols))
        width = 0.18
        plt.figure(figsize=(12, 5))
        for i, cl in enumerate(grp.index):
            plt.bar(x + (i - len(grp.index)/2)*width + width/2, grp.loc[cl].values, width=width, edgecolor="black", label=f"Cluster {cl}")

        plt.xticks(x, cols, rotation=15, ha="right")
        plt.ylim(0, 10.5)
        plt.title("Carte des renoncements : arbitrages moyens par cluster", fontweight="bold")
        plt.ylabel("Niveau moyen (1–10)")
        plt.legend()
        export_png(FIG_DIR / "carte_renoncements_par_cluster.png")
    else:
        warnings.warn("Carte des renoncements ignorée (colonnes insuffisantes).")


#%% =========================
# 10) ARBRE DE DÉCISION : Qui paie +20% pour l'éthique ?
def _recolor_tree_fills(ann_list, class_names=("Ne paie pas", "Paie")):
    C_LIGHT = PALETTE["CERULEAN_LIGHT"]
    C_DARK = PALETTE["CERULEAN_DARK"]
    for o in ann_list:
        txt_obj = o
        txt_content = txt_obj.get_text()
        bbox = txt_obj.get_bbox_patch()
        
        if "class =" in txt_content:
            cls = txt_content.split("class =")[-1].strip()
            
            if cls == class_names[1]:  # "Paie"
                bbox.set_facecolor(C_DARK)
                bbox.set_edgecolor("white")
                txt_obj.set_color("white") 
            else:                    
                bbox.set_facecolor(C_LIGHT)
                bbox.set_edgecolor(C_DARK)
                txt_obj.set_color("black")
req = ["Pret_A_Payer_Plus", "Age", "Souci_Ethique", "Importance_Prix", "Importance_Qualite"]

if all(c in df.columns for c in req):
    d = df.dropna(subset=req).copy()
    y = (d["Pret_A_Payer_Plus"] >= 7).astype(int)
    feats = ["Age", "Souci_Ethique", "Importance_Prix", "Importance_Qualite"]
    X = d[feats].copy()

    tree_model = DecisionTreeClassifier(
        max_depth=3,
        min_samples_leaf=20,
        class_weight="balanced",
        random_state=RANDOM_STATE
    )
    tree_model.fit(X, y)
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='white')
    
    ann = plot_tree(
        tree_model,
        feature_names=feats,
        class_names=["Ne paie pas", "Paie"],
        filled=True,
        rounded=True,
        fontsize=11,
        ax=ax,
        precision=2 # Limita casas decimais para evitar poluição visual
    )
    _recolor_tree_fills(ann, class_names=("Ne paie pas", "Paie"))

    plt.title("Règles pour payer 20% plus cher (produit éthique)", fontsize=22, fontweight="bold", pad=20)
    export_png(FIG_DIR / "arbre_decision_payer_plus.png")
    plt.show()

else:
    warnings.warn("Arbre de décision ignoré (colonnes manquantes).")

#%% =========================
# 11) DESTINATION FIN DE VIE par fréquence d'achat (barres empilées)
# =========================
req = ["Frequence_Achat", "Destination_Fin_Vie"]
if all(c in df.columns for c in req):
    d = df.dropna(subset=req).copy()

    dum = d["Destination_Fin_Vie"].astype(str).str.get_dummies(sep=";")
    dum.columns = [c.strip() for c in dum.columns]
    temp = pd.concat([d["Frequence_Achat"], dum], axis=1)

    pct = temp.groupby("Frequence_Achat").mean() * 100

    # garder top options pour lisibilité
    top_cols = dum.sum().sort_values(ascending=False).head(6).index
    pct = pct[top_cols]

    x = np.arange(len(pct.index))
    n = len(pct.columns)
    width = min(0.8 / max(n, 1), 0.18)

    plt.figure(figsize=(12, 6))
    for i, col in enumerate(pct.columns):
        plt.bar(x + (i - (n-1)/2)*width, pct[col].values, width=width,
                edgecolor="black", label=col)

    plt.xticks(x, pct.index.astype(str), rotation=20, ha="right")
    plt.ylabel("% des répondants (dans le groupe)")
    plt.title("Fin de vie : % des répondants par option (multi-choix)", fontweight="bold")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    export_png(FIG_DIR / "fin_de_vie_par_frequence.png")
else:
    warnings.warn("Fin de vie par fréquence ignorée.")


#%% =========================
# 12) RAPPORT COURT (Markdown) : fichiers générés
# =========================
generated = [
    "reports/diagnostic_colonnes.txt",
    "reports/figures/grand_paradoxe.png",
    "reports/figures/paradoxe_par_age.png",
    "reports/figures/paradoxe_par_canal.png",
    "reports/figures/ethique_vs_culpabilite_couleur_ff.png",
    "reports/figures/reseau_items_tendance.png",
    "reports/figures/personas_scatter.png",
    "reports/personas_clusters.csv",
    "reports/personas_moyennes_par_cluster.csv",
    "reports/figures/heatmap_items_par_cluster.png",
    "reports/figures/obsolescence_psy_par_cluster.png",
    "reports/figures/spirale_culpabilite_reseaux.png",
    "reports/figures/carte_renoncements_par_cluster.png",
    "reports/figures/arbre_decision_payer_plus.png",
    "reports/figures/fin_de_vie_par_frequence.png",
    "reports/sankey_parcours_3_etapes.html",
    "reports/sankey_cycle_complet_4_etapes.html",
]

md = ["# Résumé des exports\n", "Fichiers potentiellement générés :\n"]
for p in generated:
    md.append(f"- {p}")
(OUT_DIR / "resume_exports.md").write_text("\n".join(md), encoding="utf-8")
print("OK - Résumé : reports/resume_exports.md")

#%% =========================
# 12) VISUALISATIONS COMPLÉMENTAIRES
# =========================

# Dossiers 
try:
    OUT_DIR
except NameError:
    OUT_DIR = Path("reports")
try:
    FIG_DIR
except NameError:
    FIG_DIR = OUT_DIR / "figures"

OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


def _savefig(path: Path):
    try:
        export_png(path)  
    except Exception:
        plt.tight_layout()
        plt.savefig(path, dpi=200, bbox_inches="tight")
        plt.close()

# -------- helpers --------
def col_like(df: pd.DataFrame, must_contain: list[str]):
    """Retourne la 1ère colonne dont le nom contient tous les fragments donnés."""
    cols = []
    for c in df.columns:
        ok = True
        cl = str(c).lower()
        for frag in must_contain:
            if frag.lower() not in cl:
                ok = False
                break
        if ok:
            cols.append(c)
    return cols[0] if cols else None

def split_multi(s: pd.Series, sep=";"):
    """Gère multi-choix: split sur ';' et nettoyage."""
    return (
        s.fillna("")
         .astype(str)
         .str.split(sep)
         .apply(lambda lst: [x.strip() for x in lst if x and x.strip()])
    )

def value_counts_pct(s: pd.Series, dropna=False):
    vc = s.value_counts(dropna=dropna)
    pct = (vc / vc.sum() * 100).round(1)
    return pd.DataFrame({"count": vc, "pct": pct})

def barh_counts(s: pd.Series, title: str, filename: str, top_n=12):
    d = s.fillna("Non spécifié").astype(str).str.strip()
    vc = d.value_counts().head(top_n)[::-1]
    plt.figure(figsize=(10, 5))
    plt.barh(vc.index, vc.values)
    plt.title(title, fontweight="bold")
    plt.xlabel("Nombre de réponses")
    _savefig(FIG_DIR / filename)

# -------- 1) créer des alias courts (si pas déjà présents) --------
# IMPORTANT: on ne détruit rien, on crée juste des colonnes "propres" en plus

ALIASES = {
    "Frequence_Achat": ["fréquence", "achetez-vous", "vêtements"],
    "Canal_Achat": ["où achetez-vous", "choix multiples"],
    "Cycle_Vie": ["cycle de vie moyen"],
    "Destination_Fin_Vie": ["que faites-vous", "séparer", "choix multiples"],
    "Obsolescence_Apres_Achat": ["finissent-ils", "jamais être portés"],
    "Influence_Tendances": ["tendances actuelles", "influencent"],
    "Achat_Parce_Tendance": ["uniquement parce qu'il est tendance"],
    "Pression_Sociale": ["pression sociale"],
    "Evite_Plus_Mode": ["évité de porter", "plus à la mode"],
    "Confiance": ["confiance en vous"],
    "Bien_Shabiller_Social": ["bien s’habiller", "vie sociale"],
    "Influence_Reseaux": ["réseaux sociaux", "dictent"],
    "Publie_Photos_Tendance": ["publie", "photos", "achats"],
    "Culpabilite_RS": ["culpabilité", "réseaux sociaux"],
    "Perception_Sans_Tendance": ["différence", "perçu", "tendance"],
    "Items_Achetes": ["acheté certains de ces articles", "choix multiples"],
    "Connaissance_FF": ["connaissez-vous le concept", "fast fashion"],
    "Utilise_FastFashion": ["avez-vous déjà consommé", "fast fashion"],
    "Souci_Ethique": ["considérations éthiques", "environnementales"],
    "Pret_A_Payer_Plus": ["coûtait 20 % plus cher", "prêt"],
    "Raisons_FF": ["raisons achetez-vous", "fast fashion", "choix multiples"],
    "Age": ["quel est votre âge"],
    "Genre": ["êtes-vous :"],
    "Expression_vs_Conformite": ["outil d'expression", "conformer"],
    "Situation_Pro": ["situation professionnelle ?"],
    "Importance_Prix": ["caractéristiques", "prix"],
    "Importance_Qualite": ["caractéristiques", "qualité"],
    "Importance_Marque": ["caractéristiques", "marque"],
    "Importance_Mode": ["caractéristiques", "mode / tendances"],
    "Importance_Confort": ["caractéristiques", "confort"],
}

for short, frags in ALIASES.items():
    if short not in df.columns:
        original = col_like(df, frags)
        if original is not None:
            df[short] = df[original]
        else:
            # pas grave: on laisse absent
            pass

# Nettoyage minimal sur les alias clés (évite erreurs .str sur DataFrame)
for c in ["Frequence_Achat", "Canal_Achat", "Cycle_Vie", "Destination_Fin_Vie",
          "Utilise_FastFashion", "Connaissance_FF", "Raisons_FF", "Items_Achetes", "Genre"]:
    if c in df.columns:
        df[c] = df[c].fillna("Non spécifié").astype(str).str.strip()

# -------- 2) visus “classiques” (distributions) --------
if "Frequence_Achat" in df.columns:
    barh_counts(df["Frequence_Achat"], "Fréquence d’achat (top)", "dist_frequence_achat.png", top_n=12)

if "Canal_Achat" in df.columns:
    # multi-choix => explode
    tmp = df[["Canal_Achat"]].copy()
    tmp["Canal_Achat"] = split_multi(tmp["Canal_Achat"])
    tmp = tmp.explode("Canal_Achat")
    if tmp["Canal_Achat"].notna().any():
        barh_counts(tmp["Canal_Achat"], "Canaux d’achat (multi-choix)", "dist_canaux_achat.png", top_n=15)

if "Cycle_Vie" in df.columns:
    barh_counts(df["Cycle_Vie"], "Cycle de vie moyen d’un vêtement", "dist_cycle_vie.png", top_n=12)

if "Destination_Fin_Vie" in df.columns:
    tmp = df[["Destination_Fin_Vie"]].copy()
    tmp["Destination_Fin_Vie"] = split_multi(tmp["Destination_Fin_Vie"])
    tmp = tmp.explode("Destination_Fin_Vie")
    if tmp["Destination_Fin_Vie"].notna().any():
        barh_counts(tmp["Destination_Fin_Vie"], "Destination fin de vie (multi-choix)", "dist_destination_fin_vie.png", top_n=15)

if "Raisons_FF" in df.columns:
    tmp = df[["Raisons_FF"]].copy()
    tmp["Raisons_FF"] = split_multi(tmp["Raisons_FF"])
    tmp = tmp.explode("Raisons_FF")
    if tmp["Raisons_FF"].notna().any():
        barh_counts(tmp["Raisons_FF"], "Raisons d’achat fast fashion (multi-choix)", "dist_raisons_fastfashion.png", top_n=15)

# -------- 3) profils par cluster (si colonne Cluster existe) --------
if "Cluster" in df.columns:
    # Age par cluster (si numérique)
    if "Age" in df.columns:
        age_num = pd.to_numeric(df["Age"], errors="coerce")
        if age_num.notna().any():
            plt.figure(figsize=(10, 5))
            for cl in sorted(df["Cluster"].dropna().unique()):
                plt.hist(age_num[df["Cluster"] == cl].dropna(), bins=15, alpha=0.6, label=f"Cluster {cl}")
            plt.title("Distribution de l’âge par cluster", fontweight="bold")
            plt.xlabel("Âge")
            plt.ylabel("Nombre")
            plt.legend()
            _savefig(FIG_DIR / "age_par_cluster_hist.png")

    # Boxplots des scores (éthique / prix / qualité) par cluster
    score_cols = [c for c in ["Souci_Ethique", "Importance_Prix", "Importance_Qualite", "Pret_A_Payer_Plus"] if c in df.columns]
    for sc in score_cols:
        s = pd.to_numeric(df[sc], errors="coerce")
        if s.notna().any():
            data = []
            labels = []
            for cl in sorted(df["Cluster"].dropna().unique()):
                data.append(s[df["Cluster"] == cl].dropna().values)
                labels.append(f"C{cl}")
            if sum(len(x) for x in data) > 0:
                plt.figure(figsize=(10, 5))
                plt.boxplot(data, labels=labels, showfliers=False)
                plt.title(f"{sc} par cluster (boxplot)", fontweight="bold")
                plt.ylabel("Score")
                _savefig(FIG_DIR / f"box_{sc.lower()}_par_cluster.png")

    # Utilise_FastFashion (% oui/non) par cluster
    if "Utilise_FastFashion" in df.columns:
        t = (
            df[["Cluster", "Utilise_FastFashion"]]
            .dropna(subset=["Cluster"])
            .copy()
        )
        t["Utilise_FastFashion"] = t["Utilise_FastFashion"].fillna("Non spécifié").astype(str).str.strip()
        pivot = pd.crosstab(t["Cluster"], t["Utilise_FastFashion"], normalize="index") * 100
        pivot = pivot.round(1)
        pivot.to_csv(OUT_DIR / "utilise_fastfashion_pct_par_cluster.csv", index=True)

        plt.figure(figsize=(10, 5))
        bottom = np.zeros(len(pivot.index))
        for col in pivot.columns:
            plt.bar(pivot.index.astype(str), pivot[col].values, bottom=bottom, label=col)
            bottom += pivot[col].values
        plt.title("Fast fashion (en %) par cluster", fontweight="bold")
        plt.xlabel("Cluster")
        plt.ylabel("%")
        plt.legend(loc="upper right")
        _savefig(FIG_DIR / "fastfashion_pct_par_cluster.png")

# -------- 4) exports “storytelling” en tables --------
# Un mini résumé chiffré global (simple, utile pour l’article)
summary_lines = []
summary_lines.append(f"- N réponses: {len(df)}")
if "Souci_Ethique" in df.columns:
    s = pd.to_numeric(df["Souci_Ethique"], errors="coerce")
    if s.notna().any():
        summary_lines.append(f"- Souci éthique (moyenne): {s.mean():.2f} / 10")
if "Pret_A_Payer_Plus" in df.columns:
    s = pd.to_numeric(df["Pret_A_Payer_Plus"], errors="coerce")
    if s.notna().any():
        summary_lines.append(f"- Prêt à payer +20% (moyenne): {s.mean():.2f} / 10")
if "Influence_Reseaux" in df.columns:
    s = pd.to_numeric(df["Influence_Reseaux"], errors="coerce")
    if s.notna().any():
        summary_lines.append(f"- Influence réseaux (moyenne): {s.mean():.2f} / 10")

(Path(OUT_DIR) / "resume_storytelling.md").write_text("\n".join(summary_lines), encoding="utf-8")
print("OK - Visus complémentaires + exports storytelling générés.")

#%% =========================
# 13) WAFFLE CHART : Typologie des consommateurs (clusters)
# =========================
from matplotlib.patches import Rectangle

# 1) Choisir la bonne table : df_cluster (prioritaire), sinon df si Cluster existe
df_waffle = None
if "df_cluster" in globals() and df_cluster is not None and "Cluster" in df_cluster.columns:
    df_waffle = df_cluster.copy()
elif "Cluster" in df.columns:
    df_waffle = df.copy()

if df_waffle is None:
    warnings.warn("Waffle chart ignoré (colonne Cluster manquante).")
else:
    d = df_waffle.dropna(subset=["Cluster"]).copy()

    # 2) Sécuriser : Cluster en int
    d["Cluster"] = pd.to_numeric(d["Cluster"], errors="coerce")
    d = d.dropna(subset=["Cluster"])
    d["Cluster"] = d["Cluster"].astype(int)

    counts = d["Cluster"].value_counts().sort_index()
    labels = [f"Cluster {c}" for c in counts.index]
    values = counts.values

    # 3) Couleurs (TA palette existante)
    base_colors = [
        PALETTE["CERULEAN_DARK"],
        PALETTE["CERULEAN"],
        PALETTE["CERULEAN_LIGHT"],
        PALETTE["CERULEAN_SOFT"],
        PALETTE["NAVY"],
    ]
    colors = [base_colors[i % len(base_colors)] for i in range(len(values))]

    # 4) Grille waffle (50x50 = 2500)
    n_cols = 50
    n_rows = 50
    n_total = n_cols * n_rows

    proportions = values / values.sum()
    squares = np.floor(proportions * n_total).astype(int)

    # Ajustement pour atteindre exactement 2500 cases
    remainder = n_total - squares.sum()
    if remainder > 0:
        order = np.argsort(-(proportions * n_total - squares))  # plus grands restes
        for i in order[:remainder]:
            squares[i] += 1

    # 5) Construire la grille (liste de catégories)
    grid = []
    for i, c in enumerate(squares):
        grid += [i] * int(c)

    # (sécurité)
    grid = grid[:n_total]
    if len(grid) < n_total:
        grid += [len(values) - 1] * (n_total - len(grid))

    # 6) Plot
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="white")
    ax.set_facecolor("white")

    # dessin des carrés (avec marges propres)
    cell = 0.92  # espace entre carrés (plus premium)
    for i, cat in enumerate(grid):
        row = i // n_cols
        col = i % n_cols

        # origine en bas à gauche
        x = col
        y = (n_rows - 1 - row)

        rect = Rectangle((x, y), cell, cell, facecolor=colors[cat], edgecolor="white", linewidth=0.4)
        ax.add_patch(rect)

    # marges visuelles (respiration)
    ax.set_xlim(-1.5, n_cols + 1.5)
    ax.set_ylim(-8, n_rows + 3.5)
    ax.axis("off")

    # titre
    ax.text(
        0, n_rows + 2.2,
        "Typologie des consommateurs de mode (Waffle chart)",
        fontsize=16, fontweight="bold", color=PALETTE["CERULEAN_DARK"]
    )

    # sous-titre (optionnel mais “académique”)
    ax.text(
        0, n_rows + 1.2,
        f"{len(d)} répondants — 1 carré ≈ {max(1, int(round(len(d) / n_total)))} répondant(s)",
        fontsize=10, color=PALETTE["NAVY"]
    )

    # légende éditoriale (une ligne par cluster)
    y0 = -2.5
    for i, (lab, val) in enumerate(zip(labels, values)):
        ax.add_patch(Rectangle((0, y0 - i*1.2), 1.2, 0.7, facecolor=colors[i], edgecolor="none"))
        ax.text(
            1.5, y0 - i*1.2 + 0.35,
            f"{lab} — {val} ({val/values.sum()*100:.1f}%)",
            va="center", fontsize=10, color=PALETTE["NOIR"]
        )

    export_png(FIG_DIR / "waffle_clusters_typologie.png")
    print("OK - Waffle exporté : reports/figures/waffle_clusters_typologie.png")