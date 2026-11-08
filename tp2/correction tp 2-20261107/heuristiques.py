import numpy as np

""" Quelques heuristiques pour le PL suivant :

       max_{ x \in {0,1}^n avec Ax \le b } f(x) = c @ x
     
    où A une matrice à coefficients positifs ou nuls de profil (m,n)
       b un vecteur à coefficients (strictement) positifs de profil (m,)
       c un vecteur à coefficients (strictement) positifs de profil (n,)
"""

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
    ind = c.argsort()
    return applique_heuristique(ind, c, A, b)

def heuristique2X(c, A, b, X=1):
    """ meilleurs rapports utilité sur consommation de contrainte
        X = choix à faire passer à la fct numpy.linalg.norm
            (1, np.inf, 2, etc...) """
    m = len(b)
    r = c / np.linalg.norm((A/b.reshape((m,1))), axis=0, ord=X)
    ind = r.argsort()    
    return applique_heuristique(ind, c, A, b)

def heuristique(c, A, b, verb=False):
    """ exécute les heuristiques précédentes et choisit
        (retourne xb, Fb) la meilleure qu'on a obtenue.
        
        Note : mettre verb à True permet d'afficher les valeurs obtenues
               pour Fb de chaque heuristique (utile uniquement pour
               retrouver le tableau de l'énoncé via le script
               tests_heuristiques)
    """
    liste_norm = [1, np.inf, 2]
    xb, Fb = heuristique1(c, A, b)
    if verb:
        print(f"{Fb:7d} |", end="")
    for norm in liste_norm:
        xb2X, Fb2X = heuristique2X(c, A, b, X=norm)
        if verb:
            print(f"{Fb2X:7d} |", end="")
        if Fb2X > Fb:
            xb, Fb = xb2X, Fb2X
    return xb, Fb
    

  
