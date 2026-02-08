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
    
    ticker_reference_default = "^GSPC"

    if choix_reference:
        
        ticker_reference = input(f"Ticker de référence (appuyez sur Entrée pour {ticker_reference_default}) : ")
        ticker_reference=ticker_reference.strip()
        ticker_reference=ticker_reference.upper()

        if ticker_reference == "":
            ticker_reference=ticker_reference_default
    
        if ticker_reference in all_tickers:
            confirmation = input(f"Vous avez déjà {ticker_reference} dans votre liste de titre. Voulez vous continuer en le mettant comme référence ? (o/n) ").lower()
        
            if confirmation !='o':
                raise NameError(f"Arrêt par l'utilisateur en raison du choix du ticker de réference {ticker_reference}")
            else:
                all_tickers.remove(ticker_reference)
                all_tickers.insert(0,ticker_reference)
    
        else:
            all_tickers.insert(0,ticker_reference)
    else:
        all_tickers.insert(0,ticker_reference_default)
    
    return all_tickers