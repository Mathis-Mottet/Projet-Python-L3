from Projet.verif_param import Verif_Param
from Projet.dates_valide import Dates_Valide
from Projet.ticker_de_reference import Ticker_de_Reference
from Projet.extraction_yfinance import Extraction_yfinance



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
        start_date_str (str): Date de début
        end_date_str (str): Date de fin
        simulations (int): Nombre de simulation
        horizon (int): Nombre d'horizon

    Returns:
        None
    """

    # On vérifie les paramètres choix_reference, simulations et horizons
    max_simulations = 10000
    max_horizon = 252 * 10
    Verif_Param(choix_reference, simulations, horizon, max_simulations, max_horizon) 
        
    # On exécute pour check les dates
    start_date, end_date = Dates_Valide(start_date_str, end_date_str)
    
    # On affiche en format français
    date_format = "%d/%m/%Y"
    print(f"Dates validées : {start_date.strftime(date_format)} - {end_date.strftime(date_format)}")
    
    # On ajoute le ticker de référence + les met en majuscule
    all_tickers = [t.upper() for t in all_tickers]
    all_tickers=Ticker_de_Reference(all_tickers, choix_reference)

    # On crée le dictionnaire 'prix_tickers' qui contiendra le ticker (clé) et la liste de prix (valeur)
    prix_tickers = Extraction_yfinance(all_tickers, start_date, end_date)

    # On affiche la liste des tickers
    print(f"Liste finale de tickers : {all_tickers}")
    
    print(prix_tickers[all_tickers[4]])
    # On check l'écriture des tickers et si yfinance les accepte
    
    