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

c = np.array([1, 3])

A = np.array([[1, 1],
              [1, -2],
              [2, -1]])

b = np.array([3, 5, -5])

m = gp.Model()

x = m.addMVar(len(c))

m.setObjective(c @ x, gp.GRB.MAXIMIZE)
m.addConstr( A @ x <= b)
# 5/ reste plus qu’`a r´esoudre, ce qui s’obtient avec :
m.optimize()
affichage_resultats("Résultat optimisation ex 1-a", m)
