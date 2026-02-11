from .verif_param import Verif_Param
from .dates_valide import Dates_Valide
from .ticker_de_reference import Ticker_de_Reference
from .extraction_yfinance import Extraction_yfinance
from .asset import Asset
from .priceseries import PriceSeries



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

    # On crée le dictionnaire 'prix_tickers' et 'dates_tickers' qui contiendra le ticker (clé) et la liste de prix (valeur) et l
    prix_tickers, dates_tickers = Extraction_yfinance(all_tickers, start_date, end_date)

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
    for ticker in all_tickers:
        Ps[ticker] = PriceSeries(prix_tickers[ticker])
        Ass[ticker] = Asset(ticker, Ps[ticker])
        #Mc[ticker] = MonteCarloSimulator(Ass[ticker], simulations, horizon) #MonteCarloSimulator est le nom propose a renommer ou pas
        #Resultat = Mc[ticker].execution() #execution est la fonction d'execution a renommer ou pas
        #Ass[ticker].monte_carlo_result = Resultat
    print(Ass[all_tickers[1]].correlation_with(Ass[all_tickers[0]]))
