from __future__ import annotations
import numpy as np
from .priceseries import PriceSeries



import sys
print(sys.version)

class Asset:
    """
    Représente un actif financier avec son historique de prix.
    Pattern de conception : COMPOSITION
    Asset POSSÈDE une PriceSeries (relation HAS-A, pas IS-A).
    ───────────────────────────────────
    Attributes:
        ticker: Symbole (ex: 'AAPL')
        prices: Instance PriceSeries contenant l'historique
        sector: Classification sectorielle optionnelle
        currency: Devise des prix (défaut: USD)
    """
    
    def __init__(
        self, 
        ticker: str, 
        prices: PriceSeries,
    ) -> None:
        # Validation des entrées dans le constructeur
        if not ticker or not ticker.strip():
            raise ValueError("Le ticker ne peut pas être vide")
        if len(prices) == 0:
            raise ValueError("La série de prix ne peut pas être vide")
        
        self.monte_carlo_result = None #attribut pour stocker le résultat du Monte Carlo, initialisé à None
        self.ticker = ticker.upper()  # Normalisation en majuscules
        self.prices = prices  # Composition : Asset POSSÈDE une PriceSeries
        
    
    def __repr__(self) -> str:
        """Représentation pour le développement."""
        return f"Asset({self.ticker!r}, {len(self.prices)} prices)"
    
    def __str__(self) -> str:
        """Représentation pour l'utilisateur."""
        return f"{self.ticker}: ${self.current_price:.2f}"
    
    @property
    def current_price(self) -> float:
        """Dernier prix connu."""
        return self.prices.values[-1]
    
    @property
    def volatility(self) -> float:
        """Volatilité annualisée (délègue à PriceSeries)."""
        return self.prices.annualized_volatility()
    
    @property
    def total_return(self) -> float:
        """Rendement total (délègue à PriceSeries)."""
        return self.prices.total_return
    
    @property
    def sharpe_ratio(self) -> float:
        """Ratio de Sharpe (délègue à PriceSeries)."""
        return self.prices.sharpe_ratio()
    
    @property
    def max_drawdown(self) -> float:
        """Drawdown maximum (délègue à PriceSeries)."""
        return self.prices.max_drawdown()
    
    def correlation_with(self, other: "Asset") -> float:
        """
        Calcule la corrélation de Pearson des log-rendements avec un autre actif.
        
        Args:
            other: Un autre Asset
        
        Returns:
            Coefficient de corrélation entre -1 et 1
        """
        # Récupération des log-rendements
        x = self.prices.all_log_return()
        y = other.prices.all_log_return()

        # Alignement des longueurs (gestion des séries de tailles différentes)
        n = min(len(x), len(y))
        if n < 2:
            raise ValueError(
                f"Pas assez d'observations communes: {n}. "
                "Minimum requis: 2."
            )
        
        x = x[:n]
        y = y[:n]
        
        # Centrage des valeurs (soustraction de la moyenne)
        #x_centered = x - np.mean(x)
        #y_centered = y - np.mean(y)
        
        mean_x = sum(x)/n
        mean_y = sum(y)/n

        cx = [x_i - mean_x for x_i in x]
        cy = [y_i - mean_y for y_i in y]

        # Covariance (numérateur)
        covariance = sum(c_x * c_y for c_x, c_y in zip(cx, cy)) / (n - 1)
        
        # Variances pour le dénominateur
        var_x = sum(c_x * c_x for c_x in cx) / (n - 1)
        var_y = sum(c_y * c_y for c_y in cy) / (n - 1)
        
        # Vérification de la variance nulle
        if var_x == 0 or var_y == 0:
            raise ValueError(
                "Variance nulle détectée. "
                "La corrélation n'est pas définie pour une série constante."
            )
        
        return covariance / np.sqrt(var_x * var_y)
    
if __name__ == "__main__":
    # Exemple d'utilisation
    prices_aapl = PriceSeries([150, 152, 153, 155, 154])
    aapl = Asset("AAPL", prices_aapl)
    prices_amzn = PriceSeries([100, 150, 200, 180, 220])
    amzn = Asset("AMZN", prices_amzn)

    print(aapl)  # AAPL: $154.00
    print(f"current_price: {aapl.current_price:.2f}")
    print(f"Volatilité: {aapl.volatility:.4f}")
    print(f"Rendement total: {aapl.total_return:.4%}")
    print(f"Ratio de Sharpe: {aapl.sharpe_ratio:.4f}")
    print(f"Drawdown max: {aapl.max_drawdown:.4%}")
    print(f"Corrélation AAPL-AMZN: {aapl.correlation_with(amzn):.4f}") 