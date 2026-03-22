from projet import run

if __name__ == "__main__":
    """
    Script principal du projet.

    Permet de définir les paramètres de simulation
    et de lancer le pipeline principal avec run.
    """
    
    # Tickers choisit (ils seront vérifiés)
    tickers = ["AAPL", "DIS", "MSFT", "AMZN", "GOOGL"]
    
    # Décide (True/False) s'il l'on souhaite choisir nous même le ticker de référence (si False alors par défaut S&P500)
    choix_ticker_reference = False

    # Dates choisis format dd/mm/yyyy (aussi vérifiées dans le pipeline)
    start_date = "04/01/2010" 
    end_date = "31/12/2024"
   
    # Paramètres pour la simulation de Monte Carlo (ils seront vérifiés)
    nombre_simulations = 1000
    nombre_horizon = 252*1 # 5 ans de trading (252 jours de trading par an)

    # Le taux sans risque pour le ratio de Sharpe (convertit en pourcent par le code)
    taux_sans_risque=2

    # Exécution du pipeline
    try:
        run(
            all_tickers=tickers,
            start_date_str=start_date,
            choix_reference=choix_ticker_reference,
            end_date_str=end_date,
            simulations=nombre_simulations,
            horizon=nombre_horizon,
            TSR=taux_sans_risque
            )
    except Exception as e:
        print(f"{type(e).__name__}:", e)
