import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from util_sujet import matrice_B  # utilisée dans la fct solve_via_gurobi

############################################################################
# IMPORTANT : Complétez les chaînes vides suivantes 
nom_eleve = ""
prenom_eleve = ""
############################################################################

def arrange_solution(x):
    """x : tableau (n,m) (x[i,j] = 1 si la tâche i est exécutée par le proc j, 0 sinon)
      
       retourne une liste de taille m, l'élément j étant une liste contenant les numéros 
       des tâches à effectuer par le processeur j
    """
    sol = [0] * len(x[0])
    for i in range(len(sol)):
        sol[i] = []
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] == 1:
                sol[j].append(i)
    return sol

def matrice_A(C):
    """ construit la matrice A des contraintes A X <= 0
    C : tableau numpy de profil (n,m) C[i,j] : temps pour exécuter la tâche i sur le proc j 
    """
    ii = []
    jj = []
    val = []
    z = 0
    for i in range(len(C[0])):
        for j in range(len(C)):
            ii.append(z)
            jj.append(i)
            val.append(C[j][i])
            z+=1
    for i in range(len(C[0])):
        ii.append(z)
        jj.append(i)
        val.append(-1)
    A = sp.coo_matrix((val, (jj, ii)), shape = (len(C[0]), len(C) * len(C[0]) + 1 ))
    return A

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
    b = np.zeros(m) 
    d = np.ones(n)
    A = fct_mat_A(C)
    ii = []
    jj = []
    val = []
    z = 0
    for k in range(m):
        for l in range(n):
            ii.append(l)
            jj.append(z)
            val.append(1)
            z+=1
    B = sp.coo_matrix((val, (ii, jj)), shape = (n, n * m + 1))
    modele = gp.Model()
    X = modele.addMVar(n*m+1, vtype=vt)


    
    # la fonction à optimiser (juste T soit la dernière variable d'où X[-1])
    # ATTENTION, cela suppose que vous déclarez les variables à optimiser avec ce même nom X.
    modele.setObjective(X[-1], gp.GRB.MINIMIZE)
    modele.addConstr(A @ X <= b)
    modele.addConstr(B @ X == d)
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
    if perm is None:  # permutation identité dans ce cas
        perm = np.arange(n)
    sol = [0] * m
    T = np.zeros(m)
    for i in range(len(sol)):
        sol[i] = []
    for i in range(len(perm)):
        mini = C[perm[i]][0] + T[0]
        ind = 0
        for j in range(len(T)):
            if C[perm[i]][j] + T[j]< mini:
                mini = C[perm[i]][j] + T[j]
                ind = j
        sol[ind].append(perm[i])
        T[ind] = mini
    
    return sol, max(T)


    

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
    # à compléter
    
