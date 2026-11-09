import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from util_sujet import matrice_B  # utilisée dans la fct solve_via_gurobi
import util_sujet as util

############################################################################
# IMPORTANT : Complétez les chaînes vides suivantes 
nom_eleve = "Wolsky Poli"
prenom_eleve = "Rodrigo"
############################################################################

def arrange_solution(x):
    """x : tableau (n,m) (x[i,j] = 1 si la tâche i est exécutée par le proc j, 0 sinon)
      
       retourne une liste de taille m, l'élément j étant une liste contenant les numéros 
       des tâches à effectuer par le processeur j
    """
    n, m = x.shape
    proc = [[] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            if x[i, j] == 1:
                proc[j].append(i)
                break
    return proc
    

def matrice_A(C):
    """ construit la matrice A des contraintes A X <= 0
    C : tableau numpy de profil (n,m) C[i,j] : temps pour exécuter la tâche i sur le proc j 
    retourne : la matrice A au format creux ¨coo¨
    """
    n, m = C.shape
    A_val = C.flatten(order='F')
    A_ii = np.kron(np.arange(m),np.ones(n, dtype='int32'))
    A_jj = np.arange(m*n)

    return sp.hstack((sp.coo_array((A_val, (A_ii, A_jj)), shape=(m, n*m)), -1*np.ones((m,1), dtype='int32')))

def solve_via_gurobi(C, fct_mat_A=matrice_A):
    """ résolution du pb en utilisant gurobi 
        utilise les fonctions matrice_A et matrice_B
        C : tableau numpy de profil (n,m) C[i,j] : temps pour exécuter la tâche i sur le proc j
        fct_mat_A : fct qui calcule la matrice A (UTISEZ ce nom et pas directement
                    matrice_A ce qui nous permettra de tester cette fonction si votre
                    fct matrice_A n'est pas juste).
        retourne : le tableau x de taille (n,m) et le temps max minimal 
    """
    n, m = C.shape
    

    # nb_vars et vt vous seront utiles pour déclarer le vecteur à optimiser
    nb_vars = m*n+1
    # pour préciser le type des variables (m*n 'B'inaires et la dernière 'C'ontinue)
    vt =  ['B' for i in range(m*n)]; vt.append('C')
    # Instantiation d'un modèle gurobi (ne pas changer le nom modele ou alors le changer
    # dans les instructions suivantes déjà écrites)  
    modele = gp.Model()
    # à compléter
    X = modele.addMVar(nb_vars, vtype=vt)
    
    
    # la fonction à optimiser (juste T soit la dernière variable d'où X[-1])
    # ATTENTION, cela suppose que vous déclarez les variables à optimiser avec ce même nom X.
    modele.setObjective(X[nb_vars-1], gp.GRB.MINIMIZE)
    A = fct_mat_A(C)
    modele.addConstr(A @ X <= 0)
    B = matrice_B(n,m)
    modele.addConstr(B @ X == 1)
    modele.optimize()

    
    # fin de l'optimisation (Ne Pas Modifier À Partir De Cette Ligne)
    # récupérer la solution
    if modele.Status == gp.GRB.OPTIMAL :
        X_opt = np.array(modele.X)
        # l'instruction suivante permet de retrouver le tableau x (n,m)
        xij_opt = X_opt[:-1].reshape((n,m),order='F')
        # comme g(x,T) = T, on peut récupérer la valeur de la fonction comme celle de la dernière variable
        T_opt = X_opt[-1]
    else:
        xij_opt = None
        T_opt = None
        print("Echec de l'optimisation : {modele.Status}")

    return xij_opt, T_opt

def solve_via_heuristique(C, perm=None):
    n, m = C.shape
    if perm is None:  # permutation identité dans ce cas.
        perm = np.arange(n)
    T = np.zeros(m)
    xij = np.zeros((n,m), dtype='int32')
    for i in range(n):
        idx = perm[i]
        j_opt = np.argmin(T + C[idx,:])
        xij[idx,j_opt] = 1
        T[j_opt] += C[idx,j_opt]
    Tmax = np.max(T)
    return xij, Tmax

def solve_via_heuristique_bis(C, nb_perm, num_seed=0, fct_heuristique=solve_via_heuristique):
    """ 
    C : tableau définissant le problème d'affectation tâches/processeurs
    nb_perm : nb de permutations autorisées
    num_seed : parmet de ficxer le hasard
    fct_heuristique : la fct qui applique l'heuristique de base (UTISEZ ce nom et pas
                      directement solve_via_heuristique ce qui nous permettra de tester
                      cette fonction si votre solve_via_heuristique n'est pas juste)
    """
    n = C.shape[0]
    np.random.seed(num_seed)
    Tmax = np.inf
    x_opt = None
    for _ in range(nb_perm):
        perm = np.random.permutation(n)
        x_cand, T_cand = fct_heuristique(C, perm)
        if T_cand < Tmax:
            Tmax = T_cand
            x_opt = x_cand
    return x_opt, Tmax
    

