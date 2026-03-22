# Analyse Financière & Simulation Monte Carlo

> **Note** : On avait d'abord rédigé un README nous-mêmes, puis on a testé Claude.ai par curiosité. Le résultat étant bluffant, on s'en est servi comme base et on l'a adapté à notre projet. On ne peut donc pas s'en attribuer tout le mérite.

Outil d'analyse financière en Python permettant de récupérer des données boursières, calculer des indicateurs de performance et simuler des trajectoires de prix via Monte Carlo. Les résultats sont exportés dans un fichier Excel formaté.

---

## Fonctionnalités

- Récupération automatique des prix de clôture via **yfinance**
- Calcul des indicateurs financiers : rendement total, rendement annualisé, volatilité, ratio de Sharpe, max drawdown
- Ajout automatique d'un **ticker de référence** (S&P 500 par défaut)
- **Simulation Monte Carlo** sur un horizon et un nombre de simulations configurables
- Calcul de la **matrice de corrélation** entre les actifs
- Export d'un fichier **`resultats.xlsx`** formaté avec une feuille résumé et une feuille par ticker

---

## Installation

```bash
git clone https://github.com/Mathis-Mottet/Projet-Python-L3.git
cd Projet-Python-L3
```

### Étape 1 — Créer et activer le virtual environment

```bash
# Créer le venv
py -m venv .venv        # Windows
python -m venv .venv    # Mac/Linux

# L'activer
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate     # Mac/Linux
```

### Étape 2 — Installer les dépendances

```bash
pip install -r requirements.txt   # installe pandas, numpy, yfinance, xlsxwriter
pip install -e .                  # installe le projet en mode éditable (obligatoire pour les imports internes)
```

> Sans `pip install -e .`, Python ne reconnaît pas les imports internes du projet (`from projet.classes import ...`) car le dossier `src/` n'est pas dans le `PYTHONPATH` par défaut.

### requirements.txt

```
pandas
numpy
yfinance
xlsxwriter
```

---

## Structure du projet

```
Projet/                         ← dossier racine
├── main.py                     # Configuration et lancement
├── requirements.txt
├── README.md
└── src/
    └── projet/
        ├── __init__.py
        ├── pipeline.py                     # Fonction run() — point d'entrée du pipeline
        ├── classes/
        │   ├── __init__.py
        │   ├── asset.py                    # Classe Asset (composition avec PriceSeries)
        │   ├── priceseries.py              # Classe PriceSeries (calculs financiers)
        │   └── montecarlo.py               # Classes MonteCarloSimulator & MonteCarloResults
        └── fonctions/
            ├── __init__.py
            ├── extraction_yfinance.py      # Extraction et validation des données yfinance
            ├── ticker_de_reference.py      # Ajout du ticker de référence (S&P 500 par défaut)
            └── verif_param.py              # Validation des paramètres et des dates
```

---

## Utilisation

Configurer et lancer le pipeline depuis `main.py` :

```python
from projet.pipeline import run

run(
    all_tickers=["AAPL", "MSFT", "GOOGL"],
    choix_reference=False,      # True pour choisir manuellement le ticker de référence
    start_date_str="01/01/2022",
    end_date_str="31/12/2023",
    simulations=1000,
    horizon=252,                # En jours de trading (252 = 1 an)
    TSR=2                       # Taux sans risque sans pourcentage car converti par le code
)
```

### Paramètres

| Paramètre | Type | Description |
|---|---|---|
| `all_tickers` | `list[str]` | Liste des tickers boursiers (format yfinance) |
| `choix_reference` | `bool` | `True` pour saisir un ticker de référence manuellement, `False` pour utiliser `^GSPC` |
| `start_date_str` | `str` | Date de début au format `dd/mm/yyyy` |
| `end_date_str` | `str` | Date de fin au format `dd/mm/yyyy` |
| `simulations` | `int` | Nombre de simulations Monte Carlo (max : 100 000) |
| `horizon` | `int` | Horizon de simulation en jours (max : 2 520, soit 10 ans) |
| `TSR` | `float` | Taux sans risque sans pourcentage (entre -5 et 10, donc -5% et 10%) |

---

## Résultats — `resultats.xlsx`

Le fichier Excel généré contient :

**Feuille `Résumé`**
- Les paramètres de la simulation (dates, simulations, horizon, taux sans risque)
- Un tableau des métriques par ticker :
  - Prix initial et final
  - Rendement total, annualisé et journalier
  - Volatilité annualisée et journalière
  - Ratio de Sharpe
  - Max Drawdown
  - Résultats Monte Carlo : moyenne, percentiles 5% / 50% / 95%, probabilité de perte
- La matrice de corrélation entre les actifs

**Une feuille par ticker** avec les colonnes Date, Prix et Prix Base 100.

---

## Indicateurs calculés

| Indicateur | Description |
|---|---|
| Rendement total | `(P_fin - P_debut) / P_debut` |
| Rendement annualisé | Basé sur les log-rendements, annualisé sur 252 jours |
| Volatilité annualisée | Écart-type des log-rendements × √252 |
| Ratio de Sharpe | Rendement excédentaire / volatilité annualisée |
| Max Drawdown | Perte maximale depuis un pic |
| Monte Carlo | Simulation GBM (Geometric Brownian Motion) en base 100 |

> Les indicateurs nécessitant un minimum de données (21 jours de cotation) renvoient `N/A` si la condition n'est pas remplie.

---

## Gestion des erreurs

La robustesse du code était ce qu'on souhaitait développer et mettre en avant. Chaque étape est protégée contre les mauvaises entrées, avec des messages d'erreur explicites pour guider l'utilisateur.

**Validation des paramètres** (`TypeError`, `ValueError`)
- Types vérifiés strictement : `simulations` et `horizon` doivent être des `int`, `choix_reference` un `bool`, `TSR` un `float` ou `int`
- Valeurs hors limites refusées : simulations ≤ 0 ou > 100 000, horizon ≤ 0 ou > 2 520, TSR < -5 ou > 10
- Liste de tickers vide refusée, doublons détectés et supprimés automatiquement avec un message

**Validation des dates** (`ValueError`)
- Format `dd/mm/yyyy` obligatoire, toute autre syntaxe lève une erreur explicite
- Date de début doit être strictement inférieure à la date de fin
- Date de fin ne peut pas être égale ou supérieure à aujourd'hui (car prix de clôture)

**Validation des données yfinance** (`ValueError`)
- Tickers invalides ou sans données sur la période détectés et listés dans le message d'erreur
- Tickers trop récents ou trop anciens signalés avec les dates disponibles
- Décalage de dates de cotation entre tickers détecté avec proposition de continuer ou d'arrêter

**Gestion des indicateurs insuffisants**
- Si un ticker a moins de 21 jours de cotation, les indicateurs annualisés renvoient `N/A` dans l'Excel plutôt que de planter ou produire des valeurs absurdes
- La corrélation entre deux actifs aux dates de cotation différentes renvoie également `N/A`

---

## Limites

- **Equities uniquement** : des tickers Forex ou Commodities peuvent avoir des dates de cotation décalées et générer des avertissements. Ce projet ne les couvre donc pas
- **Hypothèse log-normale** : la simulation Monte Carlo suppose des rendements log-normaux (hypothèse GBM), ce qui ne capture pas les queues épaisses ni les chocs de marché
