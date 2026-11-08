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

with gp.Env(empty=True) as env:
    env.setParam('OutputFlag', 0)  # 0 pour retirer les infos du solveur, 1 pour les avoir
    env.start()
        
    print("\n\n===================================================================")
    print("Exercice 1-a :\n")
    ca = np.array([50, 40, 70, 80])
    Aa = np.array([[ 2, 4, 8,  6],
                   [10, 8, 6, 10],
                   [ 1, 1, 2,  2]])
    ba = np.array([100, 160, 20])
    ma = gp.Model(env=env)
    xa = ma.addMVar(len(ca))
    ma.setObjective(ca @ xa, gp.GRB.MAXIMIZE)
    ma.addConstr( Aa@xa <= ba)
    ma.optimize()
    affichage_resultats("Résultat optimisation ex 1-a", ma)

    
    print("\n\n===================================================================")
    print("Exercice 1-b :\n")
    cb = np.array([1, 1])
    Ab = np.array([[ 3, 2],
                   [ 3, 4],
                   [ 0, 1]])
    bb = np.array([15, 21, 3])
    mb = gp.Model(env=env)
    xb = mb.addMVar(len(cb))
    mb.setObjective(cb @ xb, gp.GRB.MAXIMIZE)
    mb.addConstr( Ab@xb <= bb)
    mb.optimize()
    affichage_resultats("Résultat optimisation ex 1-b", mb)

    
    print("\n\n===================================================================")
    print("Exercice 1-c :\n")
    cc = np.array([1, 3])
    Ac = np.array([[-1,-1],
                   [-1, 2],
                   [-2, 1]])
    bc = np.array([-3, -5, 5])
    mc = gp.Model(env=env)
    xc = mc.addMVar(len(cc))
    mc.setObjective(cc @ xc, gp.GRB.MAXIMIZE)
    mc.addConstr( Ac@xc <= bc)
    mc.optimize()
    # on doit obtenir 4 (INF_OR_UNBD)
    affichage_resultats("Résultat optimisation ex 1-c", mc)
    # pour savoir ce qu'il en est on refait une optimisation avec :
    mc.Params.DualReductions = 0
    mc.optimize()
    # on doit obtenir 5  (UNBOUNDED)
    affichage_resultats("Résultat optimisation ex 1-c (après ajustement)", mc)

    
    print("\n\n===================================================================")
    print("Exercice 1_d :\n")
    cd = np.array([1, -1])
    Ad = np.array([[ 1, 2],
                   [ 2, 1],
                   [-1,-1]])
    bd = np.array([5, 6, -4])
    md = gp.Model(env=env)
    xd = md.addMVar(len(cd))
    md.setObjective(cd @ xd, gp.GRB.MAXIMIZE)
    md.addConstr( Ad@xd <= bd)
    md.optimize()
    # on doit obtenir le statut 3 (INFEASIBLE)
    affichage_resultats("Résultat optimisation ex 1-d", md)

    
    print("\n\n===================================================================")
    print("Exercice 2_a :\n")
    c2a = np.array([6, 9, 8, 4])
    A2a = np.array([[ 4, 6, 5, 4],
                    [ 3, 6, 4, 3]])
    b2a = np.array([8, 7])
    m2a = gp.Model(env=env)
    x2a = m2a.addMVar(len(c2a), vtype=gp.GRB.BINARY)
    m2a.setObjective(c2a @ x2a, gp.GRB.MAXIMIZE)
    m2a.addConstr( A2a@x2a <= b2a)
    m2a.optimize()
    affichage_resultats("Résultat optimisation ex 2-a", m2a)

    
    print("\n\n===================================================================")
    print("Exercice 2_b :\n")
    c2b = np.array([6,-9, 8, 4])
    A2b = np.array([[ 4,-6, 5,-4],
                    [ 3,-6,-4, 3]])
    b2b = np.array([2, 1])
    m2b = gp.Model(env=env)
    x2b = m2b.addMVar(len(c2b), vtype=gp.GRB.BINARY)
    m2b.setObjective(c2b @ x2b, gp.GRB.MAXIMIZE)
    m2b.addConstr( A2b@x2b <= b2b)
    m2b.optimize()
    affichage_resultats("Résultat optimisation ex 2-b", m2b)

