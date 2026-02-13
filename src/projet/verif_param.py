
def Verif_Param(all_tickers: list[str], choix_reference: bool, simulations: int, horizon: int, max_simulations: int, max_horizon: int):
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
        raise TypeError (f"'{choix_reference}' n'est pas de type bool : True ou False")
    
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
    

    # On vérifie que la liste de ticker n'est pas vide (sinon aucun intérêt)
    if not len(all_tickers)>=1:
        raise ValueError (f"Le nombre de tickers '{all_tickers}' est inférieur à 1 : impossible")
    
    # On vérifie les doublons dans la liste de ticker
    unique_tickers=[]
    for ticker in all_tickers:
        if ticker not in unique_tickers:
            unique_tickers.append(ticker)
        else:
            print(f"Doublon ticker détecté : supression du doublon de '{ticker}'.")
    
    
    return unique_tickers