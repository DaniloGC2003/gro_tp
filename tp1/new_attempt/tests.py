import numpy as np
import scipy.sparse as sp
import util_tp1 as ut
import cles_usb as cl
import gurobipy as gp
from util_tp1 import status_to_str


TEST_ID = 3

S, t, n, m = ut.choix_test(TEST_ID)
print(f"Parameters: S = {S}, t = {t}, n = {n}, m = {m}")
A = cl.create_A(m, n, t, S)
B = cl.create_B(m, n, t, S)
p = cl.create_p(m, n, t, S)
b = cl.create_b(m, n, t, S)
d = cl.create_d(m, n, t, S)

print(f"Heuristic solution:")
Sol = cl.sol_heuristique(S, t)
nk = len(Sol)
print(f"   nb de clés = {len(Sol)}")
print(Sol)
for i in range(nk) :
    print("   La clé "+format(i)+" stocke les fichiers : ",Sol[i])

def affichage_resultats(titre, modele):
    print("\n-----------------------------------")
    print(titre)
    print("   Statut : ", status_to_str(modele.Status))
    if modele.Status == 2 :
        print("   Solution : x_opt = ", modele.X)
        print("   F(x_opt) = ", modele.ObjVal)

model = gp.Model()

x = model.addMVar(m * n + m, vtype=gp.GRB.BINARY)

model.setObjective(p @ x, gp.GRB.MINIMIZE)
model.addConstr( A @ x <= b)
model.addConstr( B @ x == d)

# 5/ reste plus qu’`a r´esoudre, ce qui s’obtient avec :
model.optimize()
affichage_resultats("Résultat optimisation", model)

x_opt = model.x
ut.post_traitement(x_opt, n, m)
#ut.print_key(S, t, x_opt, m)