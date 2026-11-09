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
    max = 0
    for i in G:
        count = len(G[i])
        if count > max:
            max = count
    return max

def heuristique_coloration(G):
    """ heuristique de coloration du graphe
    G : GrapheElem
    retourne un entier (le nb de couleurs différentes utilisées)
    et modifie G en installant (ou modifiant) une couleur en chaque noeud du graphe"""
    # on enlève la coloration éventuelle
    for i in G:
        if "col" in G[i].attr:
            del(G[i].attr["col"])

    # à compléter à partir après cette ligne
    max_colors = degmax(G) + 1
    global_colors_used = []
    T = []

    for i in G:
        T = []
        for it in range(max_colors):
            T.append(True)
        for j in G[i]:
            if "col" in G[j].attr:
                T[G[j].attr["col"]] = False
        smallest_color = 0
        #print(f"T array: {T}")
        while not T[smallest_color]:
            smallest_color += 1
        G[i].attr["col"] = smallest_color
        if not smallest_color in global_colors_used:
            global_colors_used.append(smallest_color)
    return len(global_colors_used)

def mat_A(G, m):
    """ calcul de la matrice creuse A
    G : GraphElem
    m : entier (majorant du nb chromatique (i.e. le nb de couleurs optimal)) 
    retourne une matrice creuse en format coo (ij,val)"""
    n = len(G)
    na = G.nb_aretes()
    nb_elts = 3 * na * m
    nb_lignes = na * m
    nb_cols = (n+1) * m
    ii = np.empty(nb_elts, dtype=np.int32)
    jj = np.empty(nb_elts, dtype=np.int32)
    val = np.empty(nb_elts, dtype=np.int32)

    ligne = 0
    pos = 0
    for i in G:
        for k in G[i]:
            if i < k:  # chaque arête est traitée une seule fois
                for j in range(m): # for each color
                    # x_{i,j} + x_{k,j} - y_j <= 0
                    # coefficient de x_{i,j}
                    ii[pos] = ligne
                    jj[pos] = i + n*j
                    val[pos] = 1
                    pos += 1

                    # coefficient de x_{k,j}
                    ii[pos] = ligne
                    jj[pos] = k + n*j
                    val[pos] = 1
                    pos += 1

                    # coefficient de y_j
                    ii[pos] = ligne
                    jj[pos] = n*m + j
                    val[pos] = -1
                    pos += 1

                    ligne += 1

    A = sp.coo_matrix((val, (ii, jj)), shape=(nb_lignes, nb_cols))
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
        with_gurobi_output : argument optionnel nommé (à positionner à True pour avoir la sortie du solveur)
    
        Retourne le nb chromatique du graphe
        et modifie G en installant (ou modifiant) une couleur en chaque noeud du graphe
    """
    n = len(G)
    N = m*(n+1)

    # calcul des matrices et du vecteur p

    # création environnement gurobi (pour avoir ou non la sortie du solveur selon
    # l'argument optionnel nommé   with_gurobi_output, vous pouvez décommenter
    # les 3 lignes suivantes
    env = gp.Env(empty=True)
    env.setParam('OutputFlag',with_gurobi_output)
    env.start()

    # déclaration du modèle gurobi (ne pas changer l'identificateur PL_col si vous voulez
    # utiliser la fin du code). Décommenter la ligne suivante
    PL_col = gp.Model(env=env)
    x = PL_col.addMVar(N, vtype='B')
    c = np.zeros(n*m)
    c = np.concatenate((c, np.ones(m)))
    A = mat_A(G, m)
    zero_arr = np.zeros(G.nb_aretes() * m)
    PL_col.setObjective(c @ x, gp.GRB.MINIMIZE)
    PL_col.addConstr(A @ x <= zero_arr)
    B = mat_B(m, n)
    b = np.ones(n)
    PL_col.addConstr(B @ x[:n*m] == b) # this constraint does not concern the last y_j variables
    PL_col.optimize()


    # fin de l'optimisation, vous pouvez décommenter ce qui suit
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
        print(f"Echec de l'optimisation : {PL_col.Status}")
        return None

