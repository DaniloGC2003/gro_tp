# -*- coding: utf-8 -*-

"""module d'utilitaires pour le TP 1 de GRO comprenant :

   la fonction status_to_str pour rendre la valeur du statut de l'optimisation
   par gurobi plus parlante (sous forme de string)

   la fonction choix_test qui permet d'avoir les données pour les différents tests

   la fonction post-traitement pour afficher la répartition des fichiers sur les clés

   la fonction print_key pour afficher graphiquement la répartition des fichiers sur les clés

   Ecrit par Bruno Pinçon pour le TP 1 de GRO  
"""
import numpy as np
import matplotlib.pyplot as plt


reponses_usuelles = {1: "Modèle chargé (mais pas encore optimisé)",
                     2: "Optimum atteint",
                     3: "Problème non réalisable (domaine admissible vide)",
                     4: "Problème non réalisable ou Fct objectif non bornée",
                     5: "Fct objectif non bornée"}
def status_to_str(cle):
    if cle in reponses_usuelles:
        return reponses_usuelles[cle]
    else:
        return f"status (={cle}) voir : " \
               +"https://docs.gurobi.com/projects/optimizer/en/current/reference/numericcodes/statuscodes.html#secstatuscodes"

def choix_test(num_test):
    """Permet d'avoir les données des différents tests proposés dans l'énoncé
       S : taille des clés
       t : taille des fichiers
       n : nb fichiers
       m : nb clés
    """
    if num_test == 1 :
        S = 4
        t = np.array([1,2,3])
        n = len(t)  # nombre de fichiers    
        m = 4       # borne sup sur le nombre de clés
    elif num_test == 2:
        S = 8
        t = np.array([1, 3, 2, 1, 2, 4, 2, 3, 5, 2, 2])
        n = len(t)
        m = 7
    elif num_test == 3:
        S = 500
        n = 50
        np.random.seed(3)  # permet de fixer les nbs aléatoires suivants et donc le même test
        t = np.random.randint(60, high=81, size=n)
        m = 8
    elif num_test == 4:
        S = 500
        n = 100
        np.random.seed(11)  # permet de fixer les nbs aléatoires suivants et donc le même test
        t = np.random.randint(60, size=n, high=81)    
        m = 16
    elif num_test == 5:
        S = 500
        n = 200
        np.random.seed(11)  # permet de fixer les nbs aléatoires suivants et donc le même test
        t = np.random.randint(65, size=n, high=76)    
        m = 31
    elif num_test == 6:  # petit test (merci à Mathurin M. et Félix G.) pour lequel la méthode heuristique ne donne pas
                         # la solution optimale
        S = 13
        t = np.array([9, 5, 5, 3, 2, 2])
        n = len(t)
        m = 3
    else:
        raise RuntimeError("test non prévu...")
    return S, t, n, m

def post_traitement(X, n, m):
    """Affichage de la solution : pour chaque clé, on affiche la liste des fichiers
    stockés sur celle-ci.

    X : solution sortie par gurobi
    n : nombre de fichiers
    m : nombre de clés
    """
    # conversion éventuelle de x comme un tableau numpy.ndarray
    X = np.array(X)

    x = X[:n*m]  # on récupère les variables x
    x = np.reshape(x,(n,m),order='F')  # on les reformate pour retrouver le tableau n x m
    y = X[-m:]   # on récupère les variables y (les m dernières de X)
    print("\n Solution optimale :")
    # rmq : y est un vecteur de flottants même si constitué de 0 et de 1 ; dans la
    #       f-string ci-dessous on rajoute un format pour ne pas afficher de . 
    print(f"   nb de clefs = {np.sum(y):.0f}")  
    for j in range(m) :
        if y[j] :
            stri = "   La clé "+format(j)+" stocke les fichiers : "
            for i in range(n) :
                if x[i,j] : stri = stri + format(i) + ", "
            print(stri)

def print_key(S, t, x, m):
    """Permet d'afficher la répartition des fichiers sur les clés usb dans
       l'exercice 3 du TP 1

    S : taille des clefs usb
    t : liste ou tableau (ndarray) contenant la taille de chaque fichier (n fichiers)
    x : solution obtenue par le solveur (liste ou np.ndarray) de taille m(n+1))
    m : nb initial de clefs """

    # qq vérifications...
    n = len(t) # nb de fichiers
    if len(x) != m*(n+1):
        raise RuntimeError("Arguments incompatibles...")
     
    # conversion éventuelle de x comme un tableau numpy.ndarray
    x = np.array(x)

    # listes de couleurs claires
    couleurs = ["lightgreen", "tan",  "lightgrey", "orange", "skyblue", "hotpink",
                "salmon", "aqua", "powderblue", "turquoise", "gold", "lightpink"]
    nc = len(couleurs)

    # on extrait les variables binaires x_{i,j} (=1 si le fichier i est stocké sur la clé j)
    X = x[0:n*m]
    X = np.reshape(X,(n,m),order='F')

    # on extrait les variables binaires y_i (=1 si la clé i est utilisée)
    y = x[n*m:]

    # pour chaque clé utilisée, on va créer une liste contenant, le numéro de la clé
    # suivie des numéros des fichiers. Toutes ces listes sont mise dans la liste cles_fichiers
    cles_fichiers = []
    for j in range(m):
        if y[j] :     # la clé j est utilisée
            L = [j]   # 1 er élément de la liste (num de la clé)
            for i in range(n): # les autres éléments sont les numéros des fichiers stockés
                if X[i,j] :    # le fichier i est stocké sur la clé j
                    L.append(i)
            cles_fichiers.append(L)

    # nb de clés à dessiner
    nb_key = len(cles_fichiers)

    # affichage
    plt.clf()
    ax = plt.axes()
    # marges (gauche et droite)
    delta = S*0.05
    yticks_lab = []
    ax.set(xlim=(-delta, S+delta), ylim=(0.5, nb_key+0.5))
    for k in range(nb_key) :
        ybas = 1+k-0.25; yhaut = ybas + 0.5; x0 = 0
        num_cle = cles_fichiers[k][0]
        yticks_lab.append(f"clé {num_cle}")
        nb_fich = len(cles_fichiers[k]) - 1
        for j in range(nb_fich) :
            num_fich = cles_fichiers[k][j+1]
            x1 = x0 + t[num_fich]
            ax.fill([x0,x1,x1,x0,x0],[ybas,ybas,yhaut,yhaut,ybas],couleurs[num_fich % nc], edgecolor="k")
            plt.text(0.5*(x0+x1),0.5*(ybas+yhaut),format(num_fich),
                    horizontalalignment='center',verticalalignment='center')
            x0 = x1
    plt.plot([0,S,S,0,0],[ybas,ybas,yhaut,yhaut,ybas],"k")
    ax.set_yticks(np.arange(1,nb_key+1))
    ax.set_yticklabels( yticks_lab)
    ax.set_xticks([0,S])
    plt.title(f"Répartition des fichiers sur les clés ({nb_key} clés utilisées)",fontsize=16)
    plt.show()
