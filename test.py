import os
import yfinance as yf

def test_yfinance():
    ticker = "AAPL"
    try:
        print(f"Récupération des données pour {ticker}...")
        t = yf.Ticker(ticker)
        df = t.history(period="5d")
        if df.empty:
            print(f"Erreur : aucune donnée récupérée pour {ticker}.")
        else:
            print("Voici un aperçu des données :")
            print(df)
    except Exception as e:
        print("Une erreur est survenue avec yfinance :", e)

if __name__ == "__main__":
    test_yfinance()
