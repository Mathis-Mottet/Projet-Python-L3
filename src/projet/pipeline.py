
from .verif_param import Verif_Param
from .dates_valide import Dates_Valide
from .ticker_de_reference import Ticker_de_Reference
from .extraction_yfinance import Extraction_yfinance
from .asset import Asset
from .priceseries import PriceSeries 
from .monte_carlo import MonteCarloSimulator
import pandas as pd

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
    


    #print(prix_tickers[all_tickers[1]])
    #print(prix_tickers[all_tickers[2]])
    #print(dates_tickers[all_tickers[0]][0])
    #print([d.strftime("%d/%m/%Y") for d in dates_tickers[all_tickers[0]]][0])

     #les dictionnaires pour monte carlo
    Ps = {}
    Ass = {}
    Mc = {}
    Matrice_Mc ={}
    Trading_days_per_year = 252
    test=True
    if test:
        for ticker in all_tickers:
            Ps[ticker] = PriceSeries(prix_tickers[ticker], Trading_days_per_year, nombre_min_annualisation) # On associe à PriceSeries
            Ass[ticker] = Asset(ticker, Ps[ticker]) # On associe à Asset
            Mc[ticker] = MonteCarloSimulator(Ass[ticker], simulations, horizon) # On associe à MonteCarloSimulator 
            Matrice_Mc[ticker] = Mc[ticker].simulator() # On initialise la class MonteCarloResults car dépend de MonteCarloSimulator
            Ass[ticker].monte_carlo_result= Matrice_Mc[ticker] # On associe les méthodes de MonteCarloResults à Asset pour plus de clarté et d'efficacité
            print(f"Defaite pour {ticker} : {Ass[ticker].monte_carlo_result.defaite(100)}")
            print(f"Percentiles pour {ticker} : {Ass[ticker].monte_carlo_result.percentiles([5, 50, 95], horizon)}")

        rendement_moyen_journalier = []
        volatilite_annualisee = []
        sharpe_ratio = []
        max_drawdown = []
        for ticker in all_tickers:
            asset = Ass[ticker]
            rendement_moyen_journalier.append(asset.mean_daily_return)
            volatilite_annualisee.append(asset.annualized_volatility)
            sharpe_ratio.append(asset.sharpe_ratio)
            max_drawdown.append(asset.max_drawdown)
       
        df = pd.DataFrame({
            'start_date': start_date_str,
            'end_date': end_date_str,
            'ticker': all_tickers,
            'Rendement Moyen Journalier': rendement_moyen_journalier,
            'Volatilité Annualisée': volatilite_annualisee,
            'Sharpe Ratio': sharpe_ratio,
            'Max Drawdown': max_drawdown
        })

        df.to_excel("resultats.xlsx", index=False)