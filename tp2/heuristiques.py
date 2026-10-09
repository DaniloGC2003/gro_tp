import numpy as np

# Quelques heuristiques pour le PL suivant :
#
#       max_{ x \in {0,1}^n avec Ax \le b } f(x) = c @ x
#
#    où A une matrice à coefficients positifs ou nuls de profil (m,n)
#       b un vecteur à coefficients (strictement) positifs de profil (m,)
#       c un vecteur à coefficients (strictement) positifs de profil (n,)

def applique_heuristique(ind, c, A, b):
    """
    ind : numarray (n,) d'entiers tous dictincts compris entre 0 et n-1 
          (donc une permutation) donnant l'ordre (inverse) selon lequel 
          les variables binaires doivent être examinées pour obtenir une
          solution réalisable (la première variable à examiner est x[ind[n-1]], 
          la deuxième est x[ind[n-2]], etc.)
    A : numarray (m,n) (ne doit contenir que des nombres positifs ou nuls)
    b : numarray (m,) 
    c : numarray (n,)

    retourne :
    xbar : numarray (n,)
    Fbar : scalaire
    """
    n = len(c)
    xbar = np.zeros(n)
    Fbar = 0
    cstr = b.copy()  # pour ne pas modifier b
    for k in range(n-1,-1,-1):  # on examine les variables dans l'ordre inverse
        j = ind[k]
        if min(cstr - A[:,j]) >= 0:
            # la variable j est mise à 1            
            cstr -= A[:,j]
            xbar[j] = 1
            Fbar += c[j]
    return xbar, Fbar

def heuristique1(c, A, b):
    """ simple tri des coefficients de la fct objectif """

    c_sorted = np.argsort(c)
    #print(f"sorted c: {c_sorted}")

    h1 = applique_heuristique(c_sorted, c, A, b)
    #print("h1: ")
    #print(h1)
    return h1

def heuristique2X(c, A, b, X=1):
    """ meilleurs rapports utilité sur consommation de contrainte
        X = choix à faire passer à la fct numpy.linalg.norm
            (1, np.inf, 2, etc...) """
    m = len(b)
    #print(f"m size: {m}")
    P = A/b.reshape((m,1))
    norm_P = np.linalg.norm(P, axis=0, ord=X)
    r = c/norm_P
    #print(r)
    c_sorted = np.argsort(r)
    #print("h2: ")
    #print(f"c sorted : {c_sorted}")
    total = applique_heuristique(c_sorted, c, A, b)
    #print(total)
    return total


def heuristique(c, A, b, verb=False):
    """ exécute les heuristiques précédentes et choisit la meilleure"""
    h1 = heuristique1(c, A, b)
    h2 = heuristique2X(c, A, b)
    if h1[1] > h2[1]:
        print(h1[1])
        return h1
    print(h2[1])
    return h2

    

  
