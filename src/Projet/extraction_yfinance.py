import yfinance as yf
from datetime import timedelta

def Extraction_yfinance(all_tickers: list[str], start_date, end_date):
    """
    S'occupe de vérifier si le ticker existe dans yfinance et de renvoyer la liste de prix

    Args:
        tickers (list[str]): La liste de tickers choisit par l'utilisateur

    Raises:
        ValueError: Si les tickers sont incorrectes
    """

    prix_ticker={}
    dates_ticker={}
    debut_cotation={}
    fin_cotation={}
    invalides = []
    
    for ticker in all_tickers:
        
        # On récupère les prix entre les dates
        df = yf.Ticker(ticker).history(start=start_date,end=end_date + timedelta(days=1))

        # Si aucun prix entre les dates, on ajoute le ticker à la liste        
        if df.empty:
            invalides.append(ticker)
        else:
            prix_ticker[ticker] = df['Close'].tolist() # On choisit le cours du Close
            dates_ticker[ticker]= df.index.date.tolist() # Liste des dates de cotation du ticker
            debut_cotation[ticker] = dates_ticker[ticker][0] # Première date de cotation du ticker
            fin_cotation[ticker] = dates_ticker[ticker][-1] # Dernière date de cotation du ticker
            
    
    
    # On vérifie si des tickers ne renvoient rien du tout
    if len(invalides)>0:
        raise ValueError(f"Les tickers {invalides} sont invalides ou sans données entre {start_date.strftime('%d/%m/%Y')} et {end_date.strftime('%d/%m/%Y')}")


    
    # On définit une liste : tickers qui finissent après la date de début
    tickers_trop_recents = [ticker for ticker, date in debut_cotation.items() if date > start_date]
    
    # On retourne l'erreur associée
    if len(tickers_trop_recents)>0:
        raise ValueError(
            f"Les tickers {tickers_trop_recents} n'ont pas de données à partir de la date de début {start_date.strftime('%d/%m/%Y')}. "
            f"Premières dates disponibles : {', '.join([debut.strftime('%d/%m/%Y') for ticker, debut in debut_cotation.items() if ticker in tickers_trop_recents])}"
        )
    
    
    # On définit une liste : tickers qui finissent avant la date de fin (incertain de si yfinance les cote mais au cas où...)
    ticker_trop_anciens = [ticker for ticker, date in fin_cotation.items() if date < end_date]
    
    # On retourne l'erreur associée
    if ticker_trop_anciens:
        raise ValueError(
            f"Les tickers {ticker_trop_anciens} n'ont pas de données jusqu'à la date de fin {end_date.strftime('%d/%m/%Y')}. "
            f"Dernières dates disponibles : {', '.join([fin.strftime('%d/%m/%Y') for ticker, fin in fin_cotation.items() if ticker in ticker_trop_anciens])}"
        )
    


    # On vérifie que les dates renvoyées sont les mêmes (car certains ticker sont décalés, exemple de LEH.F)
    dates_reference = dates_ticker[all_tickers[0]]
    tickers_dates_diff = [ticker for ticker, dates in dates_ticker.items() if dates != dates_reference]

    # On retourne l'erreur associée
    if tickers_dates_diff:
        raise ValueError(
            f"Les tickers {tickers_dates_diff} n'ont pas les mêmes dates de cotation que le ticker de référence {all_tickers[0]}"
        )


    # Si AUCUNE erreur, alors on retourne le dictionnaire {ticker: list[prix]}
    return prix_ticker, dates_ticker
