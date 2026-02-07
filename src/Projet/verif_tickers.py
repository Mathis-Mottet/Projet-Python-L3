import yfinance as yf

def Verif_Tickers(tickers: list[str]):
    
    invalides = []
    for ticker in tickers:
        
        df = yf.Ticker(ticker).history(period="1d")
        if df.empty:
            invalides.append(ticker)
    
    if len(invalides)>0:
        raise ValueError(f"Les tickers suivants sont invalides sur yfinance : {invalides}")
