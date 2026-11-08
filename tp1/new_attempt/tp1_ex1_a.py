import numpy as np
import gurobipy as gp
from util_tp1 import status_to_str

def affichage_resultats(titre, modele):
    print("\n-----------------------------------")
    print(titre)
    print("   Statut : ", status_to_str(modele.Status))
    if modele.Status == 2 :
        print("   Solution : x_opt = ", modele.X)
        print("   F(x_opt) = ", modele.ObjVal)

c = np.array([50, 40, 70, 80])

A = np.array([[2, 4, 8, 6],
              [10, 8, 6, 10],
              [1, 1, 2, 2]])

b = np.array([100, 160, 20])

m = gp.Model()

x = m.addMVar(len(c))

m.setObjective(c @ x, gp.GRB.MAXIMIZE)
m.addConstr( A @ x <= b)
# 5/ reste plus qu’`a r´esoudre, ce qui s’obtient avec :
m.optimize()
# 6/ apr`es optimisation, on peut :
# 6-a/ obtenir le statut avec :
print(m.Status)
# qui retourne 2 pour OPTIMAL, 3 pour INFEASIBLE, 4 pour INF_OR_UNBD et 5 pour UNBOUNDED = 5
# mais d’autres possibilit´es existe comme 1 pour LOADED (le mod`ele n’a pas encore ´et´e optimis´e)
# ou encore comme 9 pour TIME_LIMIT (il est possible de d´efinir un temps max `a ne pas
# d´epasser).
# 6-b/ obtenir la solution (si le statut est OPTIMAL) sous forme de liste avec :
x_opt = m.X # ou encore np.array(m.X) pour l’avoir sous forme de tableau numpy
# 6-c/ la valeur de la fonction objectif avec
f_opt = m.ObjVal
affichage_resultats("Résultat optimisation ex 1-a", m)
