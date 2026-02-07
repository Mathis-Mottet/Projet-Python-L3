from Projet.dates_valide import Dates_Valide
from Projet.verif_tickers import Verif_Tickers

def run(
        all_tickers: list[str], 
        start_date_str: str, 
        end_date_str: str, 
        simulations: int, 
        horizon: int
        ) -> None:
    
    try:
        start_date, end_date = Dates_Valide(start_date_str, end_date_str)
    except ValueError as e:
        print("Erreur :", e)
        return
    
    print(f"Dates validées : {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
    


    ticker_reference_default = "^GSPC"
    ticker_reference = input(f"Ticker de référence (appuyez sur Entrée pour {ticker_reference_default}) : ").strip()

    if ticker_reference == "":
        ticker_reference=ticker_reference_default
    
    if ticker_reference in all_tickers:
        confirmation = input(f"Vous avez déjà {ticker_reference} dans votre liste de titre. Voulez vous continuer en le mettant comme référence ? (o/n) ").lower()
        
        if confirmation !='o':
            print("Arret")
            return
        else:
            all_tickers.remove(ticker_reference)
            all_tickers.insert(0,ticker_reference)
    
    else:
        all_tickers.insert(0,ticker_reference)
    
    all_tickers = [t.upper() for t in all_tickers]
    
    try:
        Verif_Tickers(all_tickers)
    except ValueError as e:
        print("Erreur :", e)
        return
    
    print(f"Liste finale de tickers : {all_tickers}")





