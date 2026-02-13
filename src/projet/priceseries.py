import math
import numpy as np
# numpy sert ici à np.nan qui permet de gérer facilement les erreurs de chaque fonction qui interviennent dans la suite du code

class PriceSeries:
    """
    Classe réalisant différente fonction sur la série de prix choisie
    """
    Trading_days_per_year = 252
    def __init__(self,prix: list[float], nombre_min_annualisation: int = 21) -> None:
            self.prix = list(prix)
            self.nombre_min_annualisation=nombre_min_annualisation # Permet d'éviter les valeurs absurdes des annualisation (21 car 21 jours de trading/mois) et prévenir l'utilisateur
    
    def __repr__(self): # On copie celle du cours par principe
        return f"TimeSeries({self.prix!r})"
    
    def __str__(self): # Pas sur que ce soit nécessaire de faire du repr et du str
        if not self.prix:
            raise ValueError (f"Attention, la série de prix {self.prix} est vide") # Cette erreur n'arrivera jamais vu qu'elle est gérer en amont du pipeline mais par principe
        else:
            return f" {self.prix[-1]: .2f} (dernière cotation)"
        
    def __len__(self):
        return len(self.prix)
    

    # Calcul du rendement journalier
    def linear_return(self, t: int) -> float:
        if t < 1:
            raise ValueError(f"L'index {t} dans la fonction linear_return doit au moins être égal à 1")
        if t >= len(self.prix):
            raise IndexError(f"L'index {t} dans la fonction linear_return dépasse la longueur de la liste de prix : max={len(self.prix)-1}")
        
        return (self.prix[t] - self.prix[t-1]) / self.prix[t-1]

    # Calcul du rendement total
    def total_return(self)->float: # Pour l'affichage finale du Excel seulement
         return (self.prix[-1]-self.prix[0])/self.prix[0]

    # Calcul du rendement log journalier ; préférence donnée au log pour Monte Carlo
    def log_return(self,t)-> float: 
        if t < 1:
            raise ValueError(f"L'index {t} dans la fonction log_return doit au moins être égal à 1")
        if t >= len(self.prix):
            raise IndexError(f"L'index {t} dans la fonction log_return dépasse la longueur de la liste de prix : max={len(self.prix)-1}")
        return math.log(self.prix[t]/self.prix[t-1])
    
    # Dénombrement de tous les rendements log journalier
    def all_log_return(self)-> list[float]:
        return [self.log_return(t) for t in range(1,len(self.prix))]

    # Calcul du rendement moyen journalier logarithmique pour la Monte Carlo 
    def mean_daily_return(self) -> float: 
        log_returns = self.all_log_return()
        return sum(log_returns) / len(log_returns)
    
    # Calcul du rendement annuel linéaire mais passant par les log puis correction
    def annualized_return(self) -> float:
        if len(self.prix) < self.nombre_min_annualisation:
            return np.nan
        else:
            return math.exp(self.mean_daily_return() * self.Trading_days_per_year)-1
        


    # Calcul de la vol journalière en log toujours pour la Monte Carlo
    def daily_volatility(self) -> float:
        if len(self.prix)<3:
            raise ValueError(
                f"Pas assez de dates de cotation pour calculer la volatilité quotidienne (current = {len(self.prix)} ; min = 3)." 
                f"Veuillez étendre la plage."
                )
        
        log_returns = self.all_log_return()
        n = len(log_returns)
        mean=self.mean_daily_return()
        var = sum((l_r - mean)**2 for l_r in log_returns)/(n-1)
        daily_vol = math.sqrt(var)
        return daily_vol

    # Calcul de la vol annualisé
    def annualized_volatility(self) ->float:
        if len(self.prix) < self.nombre_min_annualisation:
            return np.nan
        else:
            return self.daily_volatility() * math.sqrt(self.Trading_days_per_year)
    
    
    
   
    # La ratio de Sharpe du cours mais revisité
    def sharpe_ratio(self, taux_sans_risque: float = 0.0) -> float:
       
        vol =  self.annualized_volatility()
        if vol == 0 or np.isnan(vol):
             return np.nan
        
        else:
            excess_return = self.annualized_return() - taux_sans_risque
            return excess_return / vol
   

    # Le drawdown du cours mais revisité avec t=0 possible
    def drawdown_at(self, t: int) -> float:
    
        if t < 0:
            raise ValueError(f"L'index {t} dans la fonction drawdown doit au moins être égal à 0")
        if t >= len(self.prix):
            raise IndexError(f"L'index {t} dans la fonction drawdown dépasse la longueur de la liste de prix : max={len(self.prix)-1}")
        
        peak = max(self.prix[:t+1])
        if peak == 0:
            return 0.0
        return (self.prix[t] - peak) / peak
    
    # Le max drawdown mais revisité par rapport au cours pour simplifier
    def max_drawdown(self) -> float:
        if len(self.prix) < 2:
            raise ValueError(
                f"Pas assez de dates de cotation pour calculer le maxdrawndown (current = {len(self.prix)} ; min = 2)." 
                f"Veuillez étendre la plage"
                )
 
        max_dd=min(self.drawdown_at(t) for t in range(len(self.prix)))
        return max_dd
    
    
    # On transforme en base 100 les prix
    def base100(self) -> list[float]: # Mettre le premier prix comme base 100
        premier_prix = self.prix[0]
        return [(val / premier_prix) * 100 for val in self.prix]



if __name__ == "__main__": #test de la classe PriceSeries
    liste=[100,100,100,100]
    series = PriceSeries(liste)
    print(series)
    print("Total return:", series.total_return())
    print("Mean daily return:", series.mean_daily_return())
    print("Annualized return:", series.annualized_return())
    print("Annualized volatility:", series.annualized_volatility())
    print("Sharpe ratio:", series.sharpe_ratio())
    print("Drawdown at t:", series.drawdown_at(2))
    print("Max drawdown:", series.max_drawdown())
    #print("Base 100:", series.base100())