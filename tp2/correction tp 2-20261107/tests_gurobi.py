from util_tp2 import *
from time import time
import gurobipy as gp

def binfloat_to_str(xx):
    """Gurobi sort la solution en flottant, cette fct est utilisée
       pour un affichage plus compact"""
    return '('+','.join(['0' if x==0 else '1' for x in xx])+')'

liste_pb = [pbsac3, pbsac4, pbsac5, pbsac6, pbsac7, pbsac8, pbsac9]  

env = gp.Env(empty=True)
env.setParam('OutputFlag', 0)  # 0 pour retirer les infos du solveur, 1 pour les avoir
env.start()

for num, pb in enumerate(liste_pb, 3):
    c, A, b = pb()
    t0 = time()
    m = gp.Model(env=env)
    x = m.addMVar(len(c), vtype=gp.GRB.BINARY)
    m.setObjective(c @ x, gp.GRB.MAXIMIZE)
    m.addConstr( A@x <= b)
    m.optimize()
    tg = time() - t0
    print("\n\n-----------------------------------")
    print(f"Résolution de pbsac{num} par gurobi")    
    print(f"nb variables = {len(c)}")
    print(f"nb contraintes = {len(b)}")
    print("Résultat :")
    print(f"  x_opt = {binfloat_to_str(m.X)}")
    print(f"  F(x_opt) = {m.ObjVal}")
    print(f"  temps calcul = {tg:6.4f} s")
