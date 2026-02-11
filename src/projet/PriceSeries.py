import math

class PriceSeries:
    Trading_days_per_year = 252
    def __init__(self,values: list[float], name: str) -> None:
        self.name = name
        self.values = list(values)
        
    def __repr__(self):
        return f"TimeSeries({self.name!r},{self.values!r})"
    
    def __str__(self):
        if self.values:
            return f"{self.name}: {self.values[-1]: .2f} (latest)"
        
    def __len__(self):
        return len(self.values)
    
    def linear_return(self,t):
        return (self.values[t] - self.values[t-1])/self.values[t-1]
    
    def log_return(self,t):
        return math.log(self.values[t]/self.values[t-1])
    
    @property
    def total_return(self)->float:
        return (self.values[-1]-self.values(0))/self.values[0]
    
    def all_linear_return(self)-> list[float]:
        #i = 1
        #l =[]
        #while i < len(self.values):
        #   l[i-1]=self.linear_return(i)
        #   i += 1
        #return l
        return [self.linear_return(t) for t in range(1,len(self.values))]

    def all_log_return(self)-> list[float]:
        return [self.log_return(t) for t in range(1,len(self.values))]
    
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
        """
        Ratio de sharpe annualisé :
            - ratio entre les rendements esperés d'une stratégie et sa vol
            - rendement par unité de risque
       
        Formule: SR = (μ - r_f) / σ
       
        Args:
            risk_free_rate: taux sans risque annuel
       
        """
        vol =  self.annualized_volatility()
        if vol == 0:
            raise ValueError("Vol is equal to zero")
        excess_return = self.annualized_return() - risk_free_rate
        return excess_return / vol
   
    def drawdown_at(self, t: int) -> float:
        """
        Retourne le drawdown à l'instant t depuis le début de la série.
        Mesure le déclin par rapport à un pique historique.
 
        Args:
            t (int): index de position de la valeur supérieure de l'intervalle considéré.
 
        Returns:
            float: drawdown (valeur négative ou nulle)
        """
        if t < 0 or t >= len(self.values):
            raise IndexError(f"index {t} is out of range for series of length {len(self.values)}")
 
        peak = max(self.values[:t+1])
        if peak == 0:
            return 0.0
        return (self.values[t] - peak) / peak
    
    def max_drawdown(self) -> float:
        """
        Retourne le drawdown maximum sur toute la série.
 
        Returns:
            float: drawdown maximum (valeur négative ou nulle)
        """
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