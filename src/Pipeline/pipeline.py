from Utilities.dates_valide import Dates_Valide



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
    else:
        print(start_date)