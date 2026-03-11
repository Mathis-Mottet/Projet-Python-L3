import numpy as np
def NA(x):
    """Renvoie N/A si x est un NaN, sinon renvoie x"""
    if np.isnan(x):
        return "N/A"
    else:
        return x
