
from .verif_param import Verif_Param
from .dates_valide import Dates_Valide
from .ticker_de_reference import Ticker_de_Reference
from .extraction_yfinance import Extraction_yfinance
from .asset import Asset
from .priceseries import PriceSeries 
from .monte_carlo import MonteCarloSimulator
import pandas as pd
import numpy as np
import xlsxwriter

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
        None
    """

    # On vérifie les paramètres all_tickers, choix_reference, simulations et horizons
    max_simulations = 10000
    max_horizon = 252 * 10
    all_tickers=Verif_Param(all_tickers, choix_reference, simulations, horizon, max_simulations, max_horizon) 
        
    # On exécute pour check les dates
    start_date, end_date = Dates_Valide(start_date_str, end_date_str)
    
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
        print(f"Defaite pour {ticker} : {Ass[ticker].monte_carlo_result.defaite(100)}")
        print(f"5% pour {ticker} : {Ass[ticker].monte_carlo_result.percentiles(5, horizon)}")
        print(f"Corrélation avec {all_tickers[0]} : {Ass[ticker].correlation_with(Ass[all_tickers[0]])}")

    
    
    #MISE EN FORME DU FICHIER EXCEL RESULTATS   
    with pd.ExcelWriter("resultats.xlsx", engine="xlsxwriter") as writer:   #on écrit dans un fichier excel les paramètres et le résumé des métriques
        
        data = {                    #data a mettre dans le dataframe qui sera exporte en excel
            "Tickers": all_tickers,
            f"Prix au {start_date_str}": [Ass[t].initial_price for t in all_tickers],
            f"Prix au {end_date_str}": [Ass[t].current_price for t in all_tickers],
            "Rendement total": [Ass[t].total_return for t in all_tickers],
            "Rendement annuel": [Ass[t].annualized_return if Ass[t].annualized_return is not np.nan else "N/A" for t in all_tickers],
            "Rendement journalier": [Ass[t].mean_daily_return for t in all_tickers],
            "Volatilité annualisée": [Ass[t].annualized_volatility if Ass[t].annualized_volatility is not np.nan else "N/A" for t in all_tickers],
            "Volatilité journalière": [Ass[t].daily_volatility for t in all_tickers],
            "Ratio de Sharpe": [Ass[t].sharpe_ratio if Ass[t].sharpe_ratio is not np.nan else "N/A" for t in all_tickers],
            "Max Drawdown": [Ass[t].max_drawdown for t in all_tickers],
            "Monte Carlo moyenne base 100": [Ass[t].monte_carlo_result.average(horizon) if Ass[t].monte_carlo_result.average(horizon) is not np.nan else "N/A" for t in all_tickers],
            "Monte Carlo 5% base 100": [Ass[t].monte_carlo_result.percentiles(5, horizon) if Ass[t].monte_carlo_result.percentiles(5, horizon) is not np.nan else "N/A" for t in all_tickers],
            "Monte Carlo 50% base 100": [Ass[t].monte_carlo_result.percentiles(50, horizon) if Ass[t].monte_carlo_result.percentiles(50, horizon) is not np.nan else "N/A" for t in all_tickers],
            "Monte Carlo 95% base 100": [Ass[t].monte_carlo_result.percentiles(95, horizon) if Ass[t].monte_carlo_result.percentiles(95, horizon) is not np.nan else "N/A" for t in all_tickers],
            "Monte Carlo Defaite 100": [Ass[t].monte_carlo_result.defaite(100) if Ass[t].monte_carlo_result.defaite(100) is not np.nan else "N/A" for t in all_tickers],
            }
        df = pd.DataFrame(data)
    
        df = df.set_index('Tickers').T   #trasnposition
        df.index.name ='Tickers'
    
        df.to_excel(      #tableau avec les métriques à partir de la ligne 5 et colonne 1
            writer,
            sheet_name="Résumé",
            startrow=3,
            startcol=1
        )

        parametres = pd.DataFrame({    #dataframe pour les paramètres
            "Date début": [start_date_str],
            "Date fin": [end_date_str],
            "Nombre simulations": [simulations],
            "Horizon": [horizon]
        })
        
        parametres.to_excel(  #parametres au sommet
            writer,
            sheet_name="Résumé",
            index=False,
            startrow=0,
            startcol=0
        )

        for ticker in all_tickers:
            data_ticker = {
                "Date": dates_tickers[ticker],
                "Prix": prix_tickers[ticker],
                "Prix Base 100" : Ass[ticker].base100
            }
            df_ticker = pd.DataFrame(data_ticker)
            df_ticker.to_excel(writer, sheet_name=ticker, index=False)   #une feuille par ticker avec les prix et les prix base 


        #definition de bold
        workbook = writer.book
        bold = workbook.add_format({'bold': True})
        
        #autofit et bold par loop sur les sheets
        for sheet in writer.sheets:
            writer.sheets[sheet].autofit()
            writer.sheets[sheet].set_row(0, None, bold)

        #création du format % et choix des rows
        pourcent = workbook.add_format({'num_format': '0.00%'})
        pourcent_rows = [5,6,7,8,9,11,17]  # Adjust to match sheet

        #format %
        for r in pourcent_rows:
            writer.sheets["Résumé"].set_row(r, None, pourcent)

        #loop sur les index/rows pour bold les titres 
        for i, label in enumerate(df.index):
            writer.sheets["Résumé"].write(3, 1, df.index.name, bold)
            writer.sheets["Résumé"].write(4+ i, 1, label, bold)
        
        
            