
import numpy as np
from .asset import Asset

class MonteCarloSimulator:
    """
    La simulation de Monte Carlo pour calculé les trajectoires possibles d'un actif financier sur un horizon donné.
    
    Args:
        asset: instance de la classe Asset contenant les caractéristiques de l'actif à simuler
        simulation: nombre de trajectoires à simuler
        horizon: nombre de jours à simuler
        seed: optionnel, pour fixer la graine du générateur de nombres aléatoires pour la reproductibilité des résultats
    """
    def __init__(self, asset: Asset, simulation: int, horizon: int, seed: int = None):
        self.asset = asset
        self.simulation = simulation
        self.horizon = horizon
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)  # Pour reproductibilité


    def simulator(self):

        if len(self.asset.ps) < self.asset.ps.nombre_min_annualisation:
            return MonteCarloResults(np.nan) # Pour gérer les petites valeurs 
        
        start=100 # On commence au prix de 100 pour standardiser
        mean=self.asset.mean_daily_return
        vol=self.asset.daily_volatility

        # Matrice avec en ligne les simulations, en colonne les horizons
        matrice=np.zeros((self.simulation,self.horizon+1)) # +1 car la première colonne est 100
        matrice[:,0]=start

        rendement=np.random.normal(mean,vol, size=(self.simulation, self.horizon)) # Calcul la matrice des rendements aléatoire
        cumul_rendement=np.cumsum(rendement, axis=1) # Additionne les lignes de gauche à droite CAR LES RENDEMENTS SONT DES LOG

        matrice[:,1:]=start*np.exp(cumul_rendement) # On transforme en rendement linéaire

        return MonteCarloResults(matrice) # On retourne la matrice des résultats encapsulée dans une classe pour plus de clarté et d'efficacité (MonetCarl faite 1 fois et on peut faire plein de calculs dessus sans refaire la simulation)



class MonteCarloResults:
    def __init__(self, matrice: np.ndarray):
        self.matrice = matrice
    
    def percentiles(self, percentile: float, horizon: int)-> np.ndarray:
        """
        Calcule les percentiles pour chaque horizon ou pour un horizon spécifique.

        Args:
            percentiles: liste des percentiles à calculer (ex: [5, 50, 95])
            horizon: index de l'horizon à sélectionner (0 pour le prix initial, 1 pour le premier jour, etc.). Si None, calcule les percentiles pour tous les horizons.
            
        Returns:
            Les percentiles calculés pour l'horizon spécifié ou le dernier si horizon == None.
        """
        if self.matrice is np.nan:
            return np.nan
        
        if horizon < 0 or horizon > self.matrice.shape[1]-1:
            raise ValueError(
                f"L'horizon de la méthode percentile de monte carlo '{horizon}' est invalide. "
                f"Il doit être compris entre 0 et {self.matrice.shape[1]-1}"
                )
        
        if horizon is None:
            horizon = self.matrice.shape[1]-1  # Par défaut, on prend le dernier horizon
        
        colonne = self.matrice[:, horizon] # On sélectionne la colonne correspondant à l'horizon spécifié
        result = np.percentile(colonne, percentile) # On calcule le percentile de cette colonne
        
        return result
    
    def average(self, horizon: int) -> float:
        """
        Calcul la moyenne des valeurs simulées pour un horizon donné.

        Args:
            horizon: index de l'horizon à sélectionner (0 pour le prix initial, 1
        """
        if self.matrice is np.nan:
            return np.nan
        if horizon < 0 or horizon > self.matrice.shape[1]-1:
            raise ValueError(
                f"L'horizon de la méthode average de monte carlo '{horizon}' est invalide. "
                f"Il doit être compris entre 0 et {self.matrice.shape[1]-1}"
                )
        colonne = self.matrice[:, horizon] # On sélectionne la colonne correspondant à l'horizon spécifié
        result = np.mean(colonne) # On calcule la moyenne de cette colonne
        return result
    
    def defaite(self, seuil: float=100) -> float:
        if self.matrice is np.nan:
            return np.nan
        final_values = self.matrice[:, -1] # On prend les valeurs finales de chaque simulation (dernière colonne)
        return np.mean(final_values < seuil) # Proportion de simulations où la valeur finale est inférieure au seuil de défaite
    









