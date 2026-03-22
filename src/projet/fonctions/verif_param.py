import numpy as np
from datetime import datetime

def Param_Valides(all_tickers: list[str], choix_reference: bool, simulations: int, horizon: int, taux_sans_risque: float, max_simulations: int, max_horizon: int):
    """_summary_

    Args:
        choix_reference (bool): choix de l'utilisateur pour définir le ticker de référence
        simulations (int): nombre de simulations
        horizon (int): horizon de simulation en jours
    
    Raises:
        TypeError: si le type d'un paramètre est incorrect
        ValueError: si une valeur est hors limites
    """
    
    # On vérifie que le type de choix_reference (possibilité de choisir son ticker de référence) est un bool
    if not isinstance(choix_reference, bool):
        raise TypeError (f"'{choix_reference}' pour le choix_reference n'est pas de type bool : True ou False")
    
    # On vérifie que le nombre de simulation et d'horizon est "acceptable" + le type
    if type(simulations) is not int:
        raise TypeError (f"Le nombre de simulation '{simulations}' n'est pas de type int : impossible")
    if type(horizon) is not int:
        raise TypeError (f"Le nombre d'horizon '{horizon}' n'est pas de type int : impossible")

    # On vérifie le nombre de simulation
    if simulations<=0:
        raise ValueError (f"Le nombre de simulation '{simulations}' est inférieur à 0 : impossible")
    elif simulations>max_simulations:
        raise ValueError (f"Le nombre de simulation '{simulations}' est supérieur à {max_simulations} : impossible")
    
    # On vérifie le nombre d'horizon
    if horizon<=0:
        raise ValueError (f"Le nombre d'horizon '{horizon}' est inférieur ou égal à 0 : impossible")
    elif horizon>max_horizon:
        raise ValueError (f"Le nombre d'horizon '{horizon}' est supérieur à {max_horizon} : impossible")
    
    # On vérifie que le taux sans risque est bien un nombre
    if not isinstance(taux_sans_risque, (int,float)):
        raise TypeError (f"'{taux_sans_risque}' pour le taux sans risque n'est pas un nombre : impossible")

    # On vérifie les valeurs absurdes de taux sans risque
    if taux_sans_risque < -5 or taux_sans_risque > 10:
        raise ValueError(
            f"'{taux_sans_risque}' est une valeur incohérente pour un taux sans risque : doit etre entre -5 et 10")

    # On vérifie que la liste de ticker n'est pas vide (sinon aucun intérêt)
    if not len(all_tickers)>=1:
        raise ValueError (f"Le nombre de tickers '{all_tickers}' est inférieur à 1 : impossible")
    
    # On vérifie les doublons dans la liste de ticker et les enlève
    unique_tickers=[]
    for ticker in all_tickers:
        if ticker not in unique_tickers:
            unique_tickers.append(ticker)
        else:
            print(f"Doublon ticker détecté : supression du doublon de '{ticker}'.")
    
    
    return unique_tickers


def Dates_Valides(start_date_str: str, end_date_str: str):
    """
    Docstring pour Dates_Valide
    
    :param start_date_str: Date de début en string
    :param end_date_str: Date de fin en string

    Returns:
        start_date: Date de début
        end_date: Date de fin
    """
    
    # On fixe le format de base en France
    date_format="%d/%m/%Y"

    # On fait différent try pour vérifier la synthaxe et la cohérence
    try:
        start_date = datetime.strptime(start_date_str, date_format).date()
    except ValueError:
        raise ValueError("La date de début doit être au format dd/mm/yyyy")

    try:
        end_date = datetime.strptime(end_date_str, date_format).date()
    except ValueError:
        raise ValueError("La date de fin doit être au format dd/mm/yyyy")

    if start_date >= end_date:
        raise ValueError(f"La date de début {start_date_str} doit être antérieure à la date de fin {end_date_str}")

    if end_date >= datetime.today().date():
        raise ValueError(f"La date de fin {end_date_str} ne peut pas être supérieure ou égale à aujourd'hui ({datetime.today().strftime(date_format)})")    
    

    return start_date, end_date


def NA(x):
    """Renvoie N/A si x est un NaN, sinon renvoie x"""
    if np.isnan(x):
        return "N/A"
    else:
        return x