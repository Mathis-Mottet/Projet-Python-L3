from src.projet.pipeline import run 

if __name__ == "__main__":
    """
    Script principal du projet.

    Permet de définir les paramètres de simulation
    et de lancer le pipeline principal avec run.
    """
    
    # Tickers choisit (ils seront vérifiés)
    tickers = ["AAPL", "DSY", "MSFT", "AMZN", "GOOGL"]
    
    # Décide (True/False) s'il l'on souhaite choisir nous même le ticker de référence (si False alors par défaut S&P500)
    choix_ticker_reference = False

    # Dates choisis (aussi vérifiées dans le pipeline)
    start_date = "23/01/2023" 
    end_date = "30/01/2024"
   
    # Paramètres pour la simulation de Monte Carlo (ils seront vérifiés)
    nombre_simulations = 100
    nombre_horizon = 252*5 # 5 ans de trading (252 jours de trading par an)

    # Exécution du pipeline
    try:
        run(
            all_tickers=tickers,
            start_date_str=start_date,
            choix_reference=choix_ticker_reference,
            end_date_str=end_date,
            simulations=nombre_simulations,
            horizon=nombre_horizon
            )
    except Exception as e:
        print(f"{type(e).__name__}:", e)
