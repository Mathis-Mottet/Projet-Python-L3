from Projet.pipeline import run 
"""
Script principal du projet.

Permet de définir les paramètres de simulation
et de lancer le pipeline principal avec run.
"""

if __name__ == "__main__":
    
    # Tickers choisit (ils seront vérifiés)
    tickers = ["AAPL", "AMZN", "AAPL", "AAPL"]
    
    # Décide (True/False) s'il l'on souhaite choisir nous même le ticker de référence (si False alors par défaut S&P500)
    choix_ticker_reference = False

    # Dates choisis (aussi vérifiées dans le pipeline)
    start_date = "09/10/2002"
    end_date = "30/12/2004"
    
    # Paramètres pour la simulation de Monte Carlo (ils seront vérifiés)
    nombre_simulations = 1
    nombre_horizon = 365

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
