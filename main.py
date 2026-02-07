from Projet.pipeline import run



if __name__ == "__main__":
    tickers = ["AAPL", "MSFT"]
    start_date = "01/01/2000"
    end_date = "05/06/2022"
    nombre_simulations = 10
    horizon_simulation = 365

    run(
    all_tickers=tickers,
    start_date_str=start_date,
    end_date_str=end_date,
    simulations=nombre_simulations,
    horizon=horizon_simulation
    )