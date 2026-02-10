def Ticker_de_Reference(all_tickers: list[str], choix_reference: bool) -> list[str]:
    """
    Fonction permettant l'implémentation d'un ticker de référence

    Args:
        all_tickers (list[str]): La liste de tickers de l'utilisateur définie dans main.py
        choix_reference (bool): Le choix de l'utilisateur de définir la référence par input

    Raises:
        ValueError: _description_

    Returns:
        list[str]: Liste des tickers avec en première position le ticker de référence
    """
    
    # Le ticker de référence
    ticker_reference_default = "^GSPC"

    # Si l'utilisateur a True en choix_ticker_reference dans son main.py
    if choix_reference:
        
        ticker_reference = input(f"Ticker de référence (appuyez sur Entrée pour {ticker_reference_default}) : ")
        ticker_reference=ticker_reference.strip()
        ticker_reference=ticker_reference.upper()

        # On définit automatiquement si vide
        if ticker_reference == "":
            ticker_reference=ticker_reference_default
    
    # Si l'utilisateur a False en choix_ticker_reference dans son main.py
    else:
        ticker_reference=ticker_reference_default
    
    # On vérifie qu'il n'y a pas de doublons, et soit on arrete soit on révise la liste de ticker
    if ticker_reference in all_tickers:
        confirmation = input(f"Vous avez déjà {ticker_reference} dans votre liste de titre. Voulez vous continuer en le mettant comme référence ? (o/n) ").lower()
        
        if confirmation !='o':
            raise NameError(f"Arrêt par l'utilisateur en raison du choix du ticker de réference {ticker_reference}")
        else:
            all_tickers.remove(ticker_reference)
            all_tickers.insert(0,ticker_reference)
    
    else:
        all_tickers.insert(0,ticker_reference)


    # On vérifie que la liste finale contient bien 2 tickers (sinon on ne pourra pas comparer avec le ticker de référence dans la suite)
    if not len(all_tickers)>=2:
        raise ValueError (
            f"Attention, la taille de la liste de tickers '{all_tickers}' après ajout du ticker de référence est inférieure à 2 : impossible. \n"
            f"Vous avez surement une liste contenant un seul ticker {all_tickers} et chercher à mettre ce ticker en référence"
            )

    return all_tickers