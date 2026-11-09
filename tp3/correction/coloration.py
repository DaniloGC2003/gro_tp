import util_tp3 as u
import numpy as np
import scipy.sparse as sp
import gurobipy as gp
import pdb

def degmax(G):
    """calcule le degré maximal du graphe G
       G : GrapheElem
       retourne un entier (le degré max de G)
    """
    deltaG = 0
    for i in G:
        deltaG = max(deltaG, len(G[i]))
    return deltaG

def heuristique_coloration(G):
    """ heuristique de coloration du graphe
    G : GrapheElem
    retourne un entier (le nb de couleurs différentes utilisées)
    et modifie G en installant (ou modifiant) une couleur en chaque noeud du graphe"""
    # on enlève la coloration éventuelle
    for i in G:
        if "col" in G[i].attr:
            del(G[i].attr["col"])        

    ncmax = degmax(G)+1
    T = np.ones(ncmax,dtype=bool)
    nc = -1
    for i in G:
        for j in G[i]:
            if "col" in G[j].attr:
                T[G[j].attr["col"]] = False
        for k in range(ncmax):
            if T[k]:
                G[i].attr["col"] = k
                nc = max(k, nc)
                break
        # remise du tableau T à vrai
        T[:] = True
    return nc+1

def mat_A(G, m):
    """ calcul de la matrice creuse A
    G : GraphElem
    m : entier (majorant du nb chromatique (i.e. le nb de couleurs optimal)) 
    retourne une matrice creuse en format coo (ij,val)"""
    n = len(G)
    nm = n*m
    na = G.nb_aretes()
    nb_elts = na*3*m
    nb_lignes = na*m
    nb_cols  = m*(n+1)
    ii = np.empty(nb_elts, dtype=np.int32)
    jj = np.empty(nb_elts, dtype=np.int32)
    val = np.empty(nb_elts, dtype=np.int32)

    num = 0
    num_ligne = 0
    for i in G:
        for k in G[i]:
            if i < k:
                for j in range(m):
                    ii[num] = num_ligne; jj[num] = i+j*n; val[num] = 1
                    num += 1
                    ii[num] = num_ligne; jj[num] = k+j*n; val[num] = 1
                    num += 1
                    ii[num] = num_ligne; jj[num] = nm + j; val[num] = -1
                    num += 1
                    num_ligne += 1
    A = sp.coo_array((val, (ii, jj)), shape=(nb_lignes, nb_cols)) 
    return A

def mat_B(m,n):
    """ matrice B des contraintes B x = 1 (ne s'applique qu'aux variables x 
    et pas aux variables y)"""
    vect = np.ones(m, dtype=np.int32)
    B_val = np.ones(m*n, dtype=np.int32)
    B_jj  = np.arange(m*n)
    B_ii = np.kron(vect,np.arange(n))
    return sp.coo_array((B_val, (B_ii, B_jj)), shape=(n, n*m))

def PL_coloration(G, m, with_gurobi_output=False):
    """ résolution du PL de coloration de graphe par gurobi
        G : GrapheElem
        m : entier (majorant du nb chromatique (obtenu par heuristique))
        retourne le nb chromatique du graphe
        et modifie G en installant (ou modifiant) une couleur en chaque noeud du graphe
    """
    n = len(G)
    N = m*(n+1)
    p = np.ones(m, dtype=np.int32)
    A = mat_A(G, m)
    B = mat_B(m, n)
    env = gp.Env(empty=True)
    env.setParam('OutputFlag',with_gurobi_output)
    env.start()
    PL_col = gp.Model(env=env)
    X = PL_col.addMVar(N, vtype=gp.GRB.BINARY)
    PL_col.setObjective(p @ X[-m:], gp.GRB.MINIMIZE)
    PL_col.addConstr( A @ X <= 0)
    PL_col.addConstr( B @ X[:-m] == 1)
    PL_col.optimize()

    # la solution
    if PL_col.Status == gp.GRB.OPTIMAL :
        F_opt = PL_col.ObjVal
        nb_col = int(sum(PL_col.X[-m:]))
        x_opt = np.array(PL_col.X[:-m], dtype=np.int32).reshape((n,m),order='F')
        # coloration du graphe
        couleurs = [j for i in range(n)  for j in range(m) if x_opt[i,j]]
        for i in G:
            G[i].attr["col"] = couleurs[i]
        return nb_col
    else:
        print("Echec de l'optimisation : {PL_col.Status}")
        return None

