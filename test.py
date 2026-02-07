# test_yfinance.py
import ssl
import certifi
import yfinance as yf

# Forcer yfinance à utiliser le certificat certifi
#ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

tickers = ["AAPL", "MSFT"]

for t in tickers:
    ticker = yf.Ticker(t)
    try:
        df = ticker.history(period="365d", interval="1d")  # dernière semaine
        if df is None or df.empty:
            print(f"Aucune donnée récupérée pour {t}")
        else:
            print(f"Données récupérées pour {t} :")
            print(df)
    except Exception as e:
        print(f"Erreur yfinance pour {t} :", e)
