import math

class PriceSeries:
    Trading_days_per_year = 252
    
    def __init__(self,values: list[float]) -> None: #sans name sur le word, je ne sais pas si c'est pas nécessaire de l'avoir
            self.values = list(values)
    
    def __repr__(self): #pas sur que ce soit nécessaire de faire du repr et du str
        return f"TimeSeries({self.values!r})"
    
    def __str__(self): #pas sur que ce soit nécessaire de faire du repr et du str
        if not self.values:
            return "Empty PriceSeries"
        else:
            return f" {self.values[-1]: .2f} (latest)"
        
    def __len__(self):
        return len(self.values)
    
    def log_return(self,t):  #preference donnée au rendement avec log
        return math.log(self.values[t]/self.values[t-1])
    
    @property
    def total_return(self)->float: #je garde cette version pour avoir les deux
         return (self.values[-1]-self.values[0])/self.values[0]

    def all_log_return(self)-> list[float]:
        return [self.log_return(t) for t in range(1,len(self.values))]

    @property
    def total_log_return(self) -> float:
        total_log_return = sum(self.all_log_return())
        return math.exp(total_log_return) - 1 #exponentielle pour revenir à un rendement total 
    
    def mean_daily_return(self) -> float: #rendement moyen journalier, pas annualisé
        log_returns = self.all_log_return()
        return sum(log_returns) / len(log_returns)
    
    def annualized_volatility(self) ->float:
        if len(self.values)<3:
            raise ValueError("manque données")
      
        log_returns = self.all_log_return()
        n = len(log_returns)
        mean=sum(log_returns)/n 
        var = sum((l_r - mean)**2 for l_r in log_returns)/(n-1)
        daily_vol = math.sqrt(var)
       
        return daily_vol * math.sqrt(self.Trading_days_per_year)
    
    def annualized_return(self) -> float:
        if len(self) < 2:
            raise ValueError("Not enough values to calculate annualized return")
        r = self.all_log_return()
        return (sum(r)/len(r)) * self.Trading_days_per_year
    
   
    def sharpe_ratio(self, risk_free_rate: float = 0.0) -> float:
       
        vol =  self.annualized_volatility()
        if vol == 0:
            raise ValueError("Vol is equal to zero")
        excess_return = self.annualized_return() - risk_free_rate
        return excess_return / vol
   
    def drawdown_at(self, t: int) -> float:
    
        if t < 0 or t >= len(self.values):
            raise IndexError(f"index {t} is out of range for series of length {len(self.values)}")
 
        peak = max(self.values[:t+1])
        if peak == 0:
            return 0.0
        return (self.values[t] - peak) / peak
    
    def max_drawdown(self) -> float:
        if len(self.values) < 2:
            raise ValueError("Not enough values to calculate drawdown")
 
        max_dd = 0.0
        peak = self.values[0]
 
        for value in self.values[1:]:
            peak = max(peak, value)
            if peak > 0:
                dd = (value - peak) / peak
                max_dd = min(max_dd, dd)
 
        return max_dd
    
    #mettre le premier prix comme base 100
    def base100(self) -> list[float]:
        premier_prix = self.values[0]
        return [(val / premier_prix) * 100 for val in self.values]
    

if __name__ == "__main__": #test de la classe PriceSeries
    series = PriceSeries([150, 110, 105, 120])
    print(series)
    print("Total return:", series.total_return)
    print("Total log return:", series.total_log_return)
    print("Mean daily return:", series.mean_daily_return())
    print("Annualized volatility:", series.annualized_volatility())
    print("Annualized return:", series.annualized_return())
    print("Sharpe ratio:", series.sharpe_ratio())
    print("Drawdown at t=2:", series.drawdown_at(2))
    print("Max drawdown:", series.max_drawdown())
    print("Base 100:", series.base100())