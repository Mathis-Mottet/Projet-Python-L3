import random
import numpy as np

def MonteCarloSimulator(self, asset, nb_simulation, nb_horizon):
        avg, vol = asset.get_metrics()
        prix_finaux = np.array([])


        for i in range(nb_simulation):
                p=100
                for j in range(nb_horizon):
                        p=p*(1+np.random.normal(avg, vol))
                prix_finaux = np.append(prix_finaux, p)
        return(prix_finaux)
                                  

        
def MonteCarloResult(self, prix_finaux, nb_simulation):
        np.percentile(prix_finaux, [5, 50, 95])
        print("Nous avons les percentiles suivantes:")
        print("5% :", p[0])
        print("50% :", p[1])
        print("95% :", p[2])


        #Donne le pourcentage de cas oú nous perdons
        count_below = np.sum(prix_finaux < 100)         
        n_perte = (count_below / nb_simulation) * 100
        print("Nous perdons de l'argent dans :", n_perte, "% des cas")

#Idée: tracer les trajectoires de prix



# suggéré par chat: mais je pense pas besoin Version vectorisée ultra rapide Version log-normale réaliste (GBM)
















