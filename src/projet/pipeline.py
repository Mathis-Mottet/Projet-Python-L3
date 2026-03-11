
from .verif_param import Param_Valides, Dates_Valides, NA
from .ticker_de_reference import Ticker_de_Reference
from .extraction_yfinance import Extraction_yfinance
from .asset import Asset
from .priceseries import PriceSeries 
from .monte_carlo import MonteCarloSimulator
import pandas as pd
import numpy as np


def run(
        all_tickers: list[str],
        choix_reference: bool, 
        start_date_str: str, 
        end_date_str: str, 
        simulations: int, 
        horizon: int
        ) -> None:
    
    """
    Lance le pipeline qui va s'occuper d'appeler toutes les fonctions et classes

    Args:
        all_tickers (list[str]): Liste des tickers
        choix_reference (bool): Choix on non (True/False) du ticker de référence
        start_date_str (str): Date de début en string
        end_date_str (str): Date de fin en string
        simulations (int): Nombre de simulation
        horizon (int): Nombre d'horizon

    Returns:
        None mais enregistre un fichier excel "resultats.xlsx" avec les résultats et les paramètres
    """

    # On vérifie les paramètres all_tickers, choix_reference, simulations et horizons
    max_simulations = 10000
    max_horizon = 252 * 10
    all_tickers=Param_Valides(all_tickers, choix_reference, simulations, horizon, max_simulations, max_horizon) 
        
    # On exécute pour check les dates
    start_date, end_date = Dates_Valides(start_date_str, end_date_str)
    
    # On affiche en format français les dates
    date_format = "%d/%m/%Y"
    print(f"Dates validées : {start_date.strftime(date_format)} - {end_date.strftime(date_format)}")
    
    # On ajoute le ticker de référence + les met en majuscule
    all_tickers = [t.upper() for t in all_tickers]
    all_tickers=Ticker_de_Reference(all_tickers, choix_reference)

    # Permet d'éviter les valeurs absurdes des annualisations dans plus tard dans les class (21 car 21 jours de trading/mois) et prévenir l'utilisateur
    nombre_min_annualisation=21 

    # On crée le dictionnaire 'prix_tickers' et 'dates_tickers' qui contiendra le ticker (clé) et la liste de prix (valeur) et l
    prix_tickers, dates_tickers = Extraction_yfinance(all_tickers, start_date, end_date, nombre_min_annualisation)

    # On affiche la liste des tickers
    print(f"Liste finale de tickers : {all_tickers}")
    
    # Les dictionnaires pour les class
    Ps = {}
    Ass = {}
    Mc = {}
    Trading_days_per_year = 252

    for ticker in all_tickers:
        Ps[ticker] = PriceSeries(prix_tickers[ticker], Trading_days_per_year, nombre_min_annualisation) # On associe à PriceSeries
        Ass[ticker] = Asset(ticker, Ps[ticker]) # On associe à Asset
        Mc[ticker] = MonteCarloSimulator(Ass[ticker], simulations, horizon).simulator() # On initialise la class MonteCarloResults car dépend de MonteCarloSimulator
        Ass[ticker].monte_carlo_result= Mc[ticker] # On associe les méthodes de MonteCarloResults à Asset pour plus de clarté et d'efficacité (on répètera pas la simulation à chaque appel)
    
    
    #MISE EN FORME DU FICHIER EXCEL RESULTATS   
    with pd.ExcelWriter("resultats.xlsx", engine="xlsxwriter") as writer:   #on écrit dans un fichier excel les paramètres et le résumé des métriques
        
        parametres = pd.DataFrame({    # Dataframe pour les paramètres
            "Date début": [start_date_str],
            "Date fin": [end_date_str],
            "Nombre simulations": [simulations],
            "Horizon": [horizon]
        })
        
        parametres.to_excel(  # Paramètres au sommet de l'excel
            writer,
            sheet_name="Résumé",
            index=False,
            startrow=0,
            startcol=0
        )

        data = { #data a mettre dans le dataframe qui sera exporte en excel
            "Tickers": all_tickers,
            f"Prix au {start_date_str}": [Ass[t].initial_price for t in all_tickers],
            f"Prix au {end_date_str}": [Ass[t].current_price for t in all_tickers],
            "Rendement total": [Ass[t].total_return for t in all_tickers],
            "Rendement annuel": [NA(Ass[t].annualized_return) for t in all_tickers],
            "Rendement journalier": [Ass[t].mean_daily_return for t in all_tickers],
            "Volatilité annualisée": [NA(Ass[t].annualized_volatility) for t in all_tickers],
            "Volatilité journalière": [Ass[t].daily_volatility for t in all_tickers],
            "Ratio de Sharpe": [NA(Ass[t].sharpe_ratio) for t in all_tickers],
            "Max Drawdown": [Ass[t].max_drawdown for t in all_tickers],
            "Monte Carlo moyenne base 100": [NA(Ass[t].monte_carlo_result.average(horizon)) for t in all_tickers],
            "Monte Carlo 5% base 100": [NA(Ass[t].monte_carlo_result.percentiles(5, horizon)) for t in all_tickers],
            "Monte Carlo 50% base 100": [NA(Ass[t].monte_carlo_result.percentiles(50, horizon)) for t in all_tickers],
            "Monte Carlo 95% base 100": [NA(Ass[t].monte_carlo_result.percentiles(95, horizon)) for t in all_tickers],
            "Monte Carlo Defaite 100": [NA(Ass[t].monte_carlo_result.defaite(100)) for t in all_tickers],
            }
        df = pd.DataFrame(data)
    
        df = df.set_index('Tickers').T   # Transposition
        df.index.name ='Tickers' # On 'Tickers' en index
    
        # On envoie sur excel ligne 4 colonne 1
        df.to_excel(
            writer,
            sheet_name="Résumé",
            startrow=3,
            startcol=0
        )
        
        
        
        # On calcul la matrice de corrélation
        Matrice_correlation = []
        for t1 in all_tickers: # Double boucle pour parcourir all_ticker fois all_ticker
            ligne = []
            for t2 in all_tickers:
                ligne.append(NA(Ass[t1].correlation_with(Ass[t2]))) # On ajoute chaque corrélation
            Matrice_correlation.append(ligne)

        # On transforme en df avec en index et columns les tickers pour faire une matrice symétrique
        df_correlation = pd.DataFrame(
            Matrice_correlation,
            index=all_tickers,
            columns=all_tickers
        )
        df_correlation.index.name = "Matrice de corrélation"

        # On envoie sur excel ligne 20 colonne 1
        df_correlation.to_excel(
            writer,
            sheet_name="Résumé",
            startrow=19,
            startcol=0
        )

        # On cherche à créer une feuille par ticker pour les données de cotation
        for ticker in all_tickers:
            data_ticker = {
                "Date": dates_tickers[ticker],
                "Prix": prix_tickers[ticker],
                "Prix Base 100" : Ass[ticker].base100
            }
            df_ticker = pd.DataFrame(data_ticker)
            df_ticker.to_excel(writer, sheet_name=ticker, index=False)   # Une feuille par ticker donc


        #Définition du format bold
        bold = writer.book.add_format({'bold': True})
        
        # On spécifie pour la feuille "Résumé" le format de ligne 4 et 20
        ws = writer.sheets["Résumé"]
        ws.set_row(3, None, bold)
        ws.set_row(19, None, bold)

        # Passe en revu chaque sheet pour autofit + bold ligne 1
        for ws in writer.sheets.values(): 
            ws.autofit()
            ws.set_row(0, None, bold)
        
        

    # On print un message si tout s'est bien exécuté
    print("Exécution terminée.")