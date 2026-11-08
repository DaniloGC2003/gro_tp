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

c = np.array([6, -9, 8, 4])

A = np.array([[4, -6, 5, -4],
              [3, -6, -4, 3]])

b = np.array([2, 1])

m = gp.Model()

x = m.addMVar(len(c), vtype=gp.GRB.BINARY)

m.setObjective(c @ x, gp.GRB.MAXIMIZE)
m.addConstr( A @ x <= b)
# 5/ reste plus qu’`a r´esoudre, ce qui s’obtient avec :
m.optimize()
affichage_resultats("Résultat optimisation", m)
