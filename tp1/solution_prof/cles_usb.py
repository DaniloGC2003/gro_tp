import numpy as np
import scipy.sparse as sp

def mise_en_forme_pb_cle(S, m, t):
    """ construit et retourne les matrices creuses utiles pour le problème
        du stockage des fichiers dans des clés usb.

    S : taille de chaque clé
    m : borne supérieure sur le nombre de clés à utiliser (peut être obtenue via
        une solution heuristique)
    t : tableau numpy 1d avec les tailles des fichiers à stocker

    les variables (inconnues) du problème sont :
       les x_ij (x_ij = 1 si le fichier i est stocké sur le clé j, 0 sinon). Elles
       sont rangées "colonne par colonne" , on les note x.

       les y_j (=1 si la clé j est utilisée, 0 sinon), on les note y.
      
       et X = (x,y)  est donc le vecteur de toutes les variables
    """
    n = len(t)        # nb de fichiers
    nb_var = m*(n+1)  # nb de variables

    # matrice A (creuse) des contraintes A X <= 0
    vect = np.ones(m, dtype='int32')
    A_val = np.kron(vect,t)
    A_ii = np.kron(np.arange(m),np.ones(n, dtype='int32'))
    A_jj = np.arange(m*n)
    A = sp.coo_array((A_val, (A_ii, A_jj)), shape=(m, n*m))
    # ajout de -S I à droite
    A = sp.hstack((A, -S*sp.eye(m)))

    # matrice B des contraintes B x = 1  (ne s'applique qu'aux variables x et pas aux variables y)
    B_val = np.ones(m*n, dtype='int32')
    B_jj = A_jj
    B_ii = np.kron(vect,np.arange(n))
    B = sp.coo_array((B_val, (B_ii, B_jj)), shape=(n, n*m))

    # vecteur p pour la fonction coût (s'applique juste aux variables y)
    p = np.ones(m)
    
    return p, A, B

def mise_en_forme_pb_cle_bis(S, m, t):
    """ idem à mise_en_forme sauf qu'on suppose qu'on distingue
        au niveau gurobi les variables x et les variables y

        les contraintes d'inégalités peuvent alors s'écrire

        A @ x - S*y <= 0

        où ici la matrice A "n'attaque" pas les variables y, on a donc
        pas besoin de rajouter sp.hstack((A, -S*sp.eye(m)))
    """     
    n = len(t)        # nb de fichiers
    nb_var = m*(n+1)  # nb de variables

    # matrice A (creuse) des contraintes A x - S y <= 0
    vect = np.ones(m, dtype='int32')
    A_val = np.kron(vect,t)
    A_ii = np.kron(np.arange(m),np.ones(n, dtype='int32'))
    A_jj = np.arange(m*n)
    A = sp.coo_array((A_val, (A_ii, A_jj)), shape=(m, n*m))

    # matrice B des contraintes B x = 1  (ne s'applique qu'aux variables x et pas aux variables y)
    B_val = np.ones(m*n, dtype='int32')
    B_jj = A_jj
    B_ii = np.kron(vect,np.arange(n))
    B = sp.coo_array((B_val, (B_ii, B_jj)), shape=(n, n*m))

    # vecteur p pour la fonction coût (s'applique juste aux variables y)
    p = np.ones(m)
    
    return p, A, B

def sol_heuristique(S,t):
    n = len(t)
    # tri des fichiers (calcul des indices inds de sorte que t[inds[0]] <= t[inds[1]] <= ... t[inds[n-1]] 
    inds = np.argsort(t)
    # petit test
    if t[inds[n-1]] > S :
        raise RuntimeError("La taille des clés est inférieure au plus gros fichier !")

    # il s'agit d'une heuristique qu'on pourrait qualifiée de "gloutonne", on essaie de
    # remplir intelligemment une clé puis une deuxième, etc. 
    est_case = np.zeros(n,dtype=bool)  # tableau de booléens est_case[j] signifiera que
                                       # le fichier j a été casé 
    k = n-1 # on commence par le plus gros fichier
    nb_fich_case = 0
    rangement = []
    while nb_fich_case < n :
        # on commence à remplir une nouvelle clef
        # le (numéro du) plus gros fichier actuel non casé est f = inds[k]
        L = []; taille = S
        for i in range(k,-1,-1):
            f = inds[i]
            if (not est_case[f]) and t[f] <= taille :
                L.append(f); taille -= t[f]
                nb_fich_case += 1; est_case[f] = True;
        # on insère L dans la liste rangement
        rangement.append(L)
        # on calcule l'indice (dans inds) du plus gros fichier restant
        if nb_fich_case < n :
            k -=1
            while est_case[inds[k]] :
                k -= 1
    return rangement
