# -*- coding: utf-8 -*-

from util_tp2 import TreeNodePSE
from heapq import heappush, heappop
#import pdb # en cas de besoin de "debug"

def solveur_pse_bin(c, A, b, xh, Fh) :
    """  solveur PNLE en variable binaire
         c, A, b : tableaux numarray définissant le pb 
         xh, Fh : xh (tableau numarray) Fh scalaire : solution réalisable obtenue
                  via une heuristique (xh verifie Axh <= b et Fh = c @ xh
    """

    # xb et Fb doivent contenir en sortie la solution optimale et la valeur optimale
    xb = xh.copy()
    Fb = Fh

    # nombre de variables du pb
    n = len(c)

    # calcul de la potentialité maximum
    Fmax = c.sum()

    # création du sommet de l'arbre
    S = TreeNodePSE(None, Fmax, b, -1, None)

    # nb_node est un compteur (pour savoir le nombre de noeuds de
    # l'arbre qui auront été créés)
    nb_node = 1

    # on créé une file de priorité initialisée avec S
    T = []
    heappush(T,S)

#    pdb.set_trace()  # à décommenter pour débug

    while len(T) > 0 :
        N = heappop(T)

        # si la potentialité est inférieure à Fb on arrête l'exploration
        # (à partir de ce noeud)
        if N.Fmax <= Fb :
            continue

        # numéro de la variable sur laquelle on joue (x[j] = 1 ou 0)
        j = N.num_var + 1
        
        # création enfant gauche (x[j] = 1) s'il reste suffisamment
        # de provisions pour les contraintes
        temp = N.Cstr - A[:,j]
        if min(temp) >= 0:
            nb_node += 1
            N_gauche = TreeNodePSE(N, N.Fmax, temp, j, 1)
            # noeud terminal ?
            if j == n - 1:  # feuille de l'arbre, on a trouvé une meilleure solution
                Fb = N_gauche.Fmax
                xb[n - 1] = 1
                P = N_gauche.parent
                for k in range(n - 2, -1, -1):
                    xb[k] = P.val_var; P = P.parent
            else:
                # on met le noeud dans la file de priorité
                heappush(T, N_gauche)

        # création enfant droit (x[j] = 0) si le nouveau Fmax est > à Fb
        Fmax = N.Fmax - c[j]
        if Fmax > Fb:
            nb_node += 1
            N_droit = TreeNodePSE(N, Fmax, N.Cstr, j, 0)
            # noeud terminal ?
            if j == n - 1:  # feuille de l'arbre, on a trouvé une meilleure solution
                Fb = Fmax
                xb[n - 1] = 0
                P = N_droit.parent
                for k in range(n - 2, -1, -1):
                    xb[k] = P.val_var;
                    P = P.parent
            else:
                # on met le noeud dans la file de priorité
                heappush(T, N_droit)


                
        # création enfant droit (x[j] = 0) si le nouveau Fmax est > à Fb



        
    # c'est fini
    return xb, Fb, nb_node

