import yfinance as yf
from datetime import timedelta


def Extraction_yfinance(all_tickers: list[str], start_date, end_date, nombre_min_annualisation=21)-> tuple[dict, dict]:
    """
    S'occupe de vérifier si le ticker existe dans yfinance et de renvoyer la liste de prix

    Args:
        tickers (list[str]): La liste de tickers choisit par l'utilisateur

    Raises:
        ValueError: Si les tickers sont incorrectes
    """

    prix_tickers={}
    dates_tickers={}

    invalides = []
    demande_faite = False  # Flag pour ne demander qu'une seule fois si on veut arreter

    for ticker in all_tickers:
        # On récupère les prix entre les dates (on ajoute 1 jour à la fin car le end de yfinance est exclusif)
        df = yf.Ticker(ticker).history(start=start_date, end=end_date + timedelta(days=1))

        if df.empty:
            invalides.append(ticker)
            continue  # On passe au ticker suivant si le df est vide (pas de prix)

        prix_tickers[ticker] = df['Close'].tolist() # On choisit le cours du Close
        dates_tickers[ticker]= df.index.date.tolist() # Liste des dates de cotation du ticker

        # Vérification du nombre minimum de prix par rapport au minimum recommandé : 21
        if len(prix_tickers[ticker]) < nombre_min_annualisation and not demande_faite:
            print(
                "Attention, pas assez de données pour calculer certains indicateurs (Si c'est le cas, renvoie de 'nan' dans le rapport). "
                f"Minimum recommandé de prix : {nombre_min_annualisation}."
            )

            boucle=True
            while boucle:
                choix = input("Voulez-vous arrêter la fonction ? (o/n) : ").strip().lower()
                if choix in ('o', 'oui'):
                    raise ValueError("Arrêt demandé par l'utilisateur")
                elif choix in ('n', 'non'):
                    boucle=False
                else:
                    print("Réponse invalide. Tapez 'o' ou 'n'.")
            
            # On marque que la question a été posée une seule fois pour pas boucler sur le input
            demande_faite = True
    
    # On vérifie si des tickers ne renvoient rien du tout
    if len(invalides)>0:
        raise ValueError(f"Les tickers {invalides} sont invalides ou sans données entre {start_date.strftime('%d/%m/%Y')} et {end_date.strftime('%d/%m/%Y')}")

    # On appelle la fonction verif_dates_yfinance
    verif_dates_yfinance(all_tickers, start_date, end_date, prix_tickers, dates_tickers)

    # Si AUCUNE erreur, alors on retourne les dictionnaires {ticker: list[prix]} et {ticker: list[dates]}
    return prix_tickers, dates_tickers


def verif_dates_yfinance(all_tickers: list[str], start_date, end_date, prix_tickers: dict, dates_tickers: dict)-> None:
    
    debut_cotation={}
    fin_cotation={}
    for ticker in all_tickers: 
        debut_cotation[ticker] = dates_tickers[ticker][0] # Première date de cotation du ticker
        fin_cotation[ticker] = dates_tickers[ticker][-1] # Dernière date de cotation du ticker
          
    
    # On définit une liste : tickers qui finissent après la date de début
    tickers_trop_recents = [ticker for ticker, date in debut_cotation.items() if date > start_date]
    
    # On définit une liste : tickers qui finissent avant la date de fin 
    ticker_trop_anciens = [ticker for ticker, date in fin_cotation.items() if date < end_date]


    # Dans le cas où les deux listes sont non vides :
    if len(tickers_trop_recents)>0 and len(ticker_trop_anciens)>0:
        raise ValueError(
            f"Les tickers {tickers_trop_recents} n'ont pas de données à partir de la date de début {start_date.strftime('%d/%m/%Y')}. \n"
            f"Premières dates disponibles : {', '.join([debut.strftime('%d/%m/%Y') for ticker, debut in debut_cotation.items() if ticker in tickers_trop_recents])}. \n"
            f"Les tickers {ticker_trop_anciens} n'ont pas de données jusqu'à la date de fin {end_date.strftime('%d/%m/%Y')}. \n"
            f"Dernières dates disponibles : {', '.join([fin.strftime('%d/%m/%Y') for ticker, fin in fin_cotation.items() if ticker in ticker_trop_anciens])}."
        )
    
    # Dans le cas où seulement la liste tickers_trop_recents est non vide
    if len(tickers_trop_recents)>0:
        raise ValueError(
            f"Les tickers {tickers_trop_recents} n'ont pas de données à partir de la date de début {start_date.strftime('%d/%m/%Y')}. \n"
            f"Premières dates disponibles : {', '.join([debut.strftime('%d/%m/%Y') for ticker, debut in debut_cotation.items() if ticker in tickers_trop_recents])}."
        )
    
    # Dans le cas où seulement la liste ticker_trop_anciens est non vide
    if len(ticker_trop_anciens)>0:
        raise ValueError(
            f"Les tickers {ticker_trop_anciens} n'ont pas de données jusqu'à la date de fin {end_date.strftime('%d/%m/%Y')}. \n"
            f"Dernières dates disponibles : {', '.join([fin.strftime('%d/%m/%Y') for ticker, fin in fin_cotation.items() if ticker in ticker_trop_anciens])}."
        )
    


    # On vérifie que les dates renvoyées sont les mêmes (car certains ticker sont décalés pour une raison inconnue, exemple de LEH.F)
    # Une autre raison est que notre projet porte sur Equities et non Forex ou Commodities par exemple
    dates_reference = dates_tickers[all_tickers[0]]
    tickers_dates_diff = [ticker for ticker, dates in dates_tickers.items() if dates != dates_reference]

    # On retourne l'erreur associée
    if tickers_dates_diff:
        raise ValueError(
            f"Les tickers {tickers_dates_diff} n'ont pas les mêmes dates de cotation que le ticker de référence {all_tickers[0]}"
        )


    
    
    