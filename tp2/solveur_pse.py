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
        j = ...
        
        # création enfant gauche (x[j] = 1) s'il reste suffisamment
        # de provisions pour les contraintes
 
                
        # création enfant droit (x[j] = 0) si le nouveau Fmax est > à Fb



        
    # c'est fini
    return xb, Fb, nb_node

