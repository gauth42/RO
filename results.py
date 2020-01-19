import pandas as pd
import numpy as np
import os
import time
import sys

import flowshop
from grasp import *

start = time.time()

# Range du paramètre alpha
alphas = np.linspace(0, 1, 11)
# Nombre d'itération pour chaque fichier
nb_ite = int(sys.argv[1])

# Tous les jeux de données
files = ["data_1/"+data for data in os.listdir("data_1")]+["data_2/"+data for data in os.listdir("data_2")]

res = list()
for file in files:
    print("------------------------------------------\n"
          "Fichier : {}\n".format(file))
    for alpha in alphas:
        print("Alpha = {}\n".format(alpha))
        biais_type = "lineaire"

        for i in range(nb_ite):
            prob = flowshop.Flowshop()
            prob.definir_par(file)
            grasp = Grasp(prob, alpha, biais_type)
            grasp.main()
            grasp.save_best(file)

            res.append([file, alpha, grasp.ordo.duree()])

# Sauvegarde
df = pd.DataFrame(res, columns=["file_name", "alpha", "Cmax"])
df.to_csv("results_stat/nb_ite_{}".format(nb_ite), index=False)


print("Temps d'exécution : {:.2f}".format(time.time()-start))
