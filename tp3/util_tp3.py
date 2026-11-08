"""Module d'utilitaires pour le TP3 de GRO 1
   auteur Bruno Pinçon
"""
import numpy as np
import scipy.sparse as sp
import matplotlib.colors as colors
import pdb
inf = np.inf

# un choix de (13) couleurs pour colorier un graphe 
noms_old = ("blue", "red", "yellow", "springgreen", "orange",
        "darkviolet", "sienna", "paleturquoise", "hotpink",
        "silver", "powderblue", "darkseagreen", "gold")
noms = ("silver", "paleturquoise", "yellow", "springgreen", "orange",
        "darkviolet", "sienna", "paleturquoise", "hotpink",
        "silver", "powderblue", "darkseagreen", "gold")
nb_col = len(noms)
graph_col = [colors.CSS4_COLORS[nom] for nom in noms]

# quelques fichiers dimacs (avec leur nombre chromatique) obtenus
# à cette url : https://mat.tepper.cmu.edu/COLOR/instances.html
fichiers_dimacs = {"myciel5.col":6 , "myciel6.col":7, "david.col":11, "le450_5a.col":5,
                   "le450_15d.col":15, "anna.col":11, "miles250.col":8, "inithx.i.2.col":31}

class Node:
    """Cette classe permet de stoker toutes les informations liées à un sommet/noeud :
        - attr est un dictionnaire d'attributs du noeud (par exemple ses coordonnées s'il en a, sa couleur, etc.)
        - voisins est l'ensemble dont les éléments sont les clés (les identificateurs) des 
          noeuds voisins (ceux partageant une arête avec le noeud)
    """
    def __init__ (self, data=None):
        self.attr = {}
        self.voisins = set()
        if data :
            if not (type(data) == dict) :
                raise TypeError("data= doit être un dictionnaire")
            self.attr = data
        
    def __getitem__ (self, cle) :
        """pour alléger l'accès aux arêtes"""
        return self.voisins[cle]
    
    def __setitem__ (self, cle, item) :
        """pour alléger l'accès aux arêtes"""
        self.voisins[cle] = item

    def __iter__ (self) :
        """permet d'alléger la syntaxe pour itérer sur les voisins"""
        return iter(self.voisins)

    def __len__(self) :
        """nb de voisin du noeud"""
        return len(self.voisins)

    def __contains__(self, cle) :
        """pour alléger l'accès aux voisins"""
        return cle in self.voisins
    
    def __repr__(self) :
        """permet d'afficher les attributs d'un noeud, et les identificateurs de ses voisins"""
        big_string  = "< type Node, attr : "+format(self.attr)+", voisins : "
        for cle in self.voisins :
            big_string += format(cle)+" "
        big_string += ">"
        return big_string
   
class GrapheElem:
    """Permet de représenter et de manipuler des graphes non orientés (et non valués) : 
         
         G.nom string (permet de donner un nom au graphe)

         G.donnees est un dictionnaire dont les clés sont les noms (identificateurs)
         des noeuds/sommets du graphe. On peut utiliser tout objet python
         valable en tant que clé de dictionnaire (string, entiers, ....).

         Pour éviter trop de lourdeurs, on définit les méthodes __getitem__ et __setitem__ 
         ce qui permet d'écrire G[k] plutôt que G.donnees[k]  (on utilise la première notation
         dans la suite).
          
         Si k est l'identificateur d'un sommet alors G[k] est un objet de classe Node et :
            G[k].attr est un dictionnaire permettant d'ajouter des attributs associés au noeud k 
                      (par exemple des coordonnées x,y, une couleur, etc)
            G[k].voisins est un ensemble dont les clés sont les identificateurs des sommets voisins du noeud k
     """
    def __init__ (self,nom=""):
        """création d'une instance (vide) d'un graphe :
           G = GrapheElem(nom=string) initialise un tel objet
               auquel on peut donner un éventuel nom via l'argument optionnel donné nom=."""
        self.nom = nom
        self.donnees = {}

    def __contains__(self, toto):
        """permet de raccourcir la syntaxe d'appartenance d'un noeud toto au graphe"""
        return toto in self.donnees

    def __getitem__(self, n):
        """permet d'alléger la notation d'extration des données d'un noeud n du graphe"""
        return self.donnees[n]

    def __iter__(self):
        """permet d'alléger la notation pour itérer sur les noeuds d'un graphe"""
        return iter(self.donnees)

    def __delitem__(self, n):
        """permet d'alléger la notation pour enlever le noeud n du graphe"""
        del self.donnees[n]

    def __setitem__(self, n, item):
        """permet d'alléger la notation d'insertion des données d'un noeud n du graphe
           item doit être un objet de classe Node"""
        self.donnees[n] = item

    def __len__(self) :
        """nb de sommets/noeuds du graphe"""
        return len(self.donnees)

    def __repr__(self) :
        """affichage sommaire"""
        big_string = "< type GrapheElem : nom = "+format(self.nom)
        for cle in self :
            big_string += "\n noeud "+format(cle)+", voisins : "+format(self[cle].voisins)
        big_string += ">"
        return big_string

    def __str__(self) :
        """permet d'afficher le graphe via print"""
        big_string  = " nom du graphe : "+self.nom+"\n"
        big_string += " les "+format(len(self))+" noeuds :"
        for cle in self :
            big_string += "\n     id : "+format(cle)+", attributs : "+format(self[cle].attr)
        na = self.nb_aretes()
        big_string += "\n les "+format(na)+" arêtes : "
        aretes = set()
        for cle in self :
            for clef in self[cle] :
                a = (cle,clef); b = (clef,cle)
                if a not in aretes and b not in aretes:
                    aretes.add(a)
        paquet = 8  # on affiche 8 arêtes max par ligne
        for k,(a0,a1) in enumerate(aretes):
            if k % paquet == 0:
                big_string += "\n     "
            big_string += "{"+format(a0)+","+format(a1)+"}"
            if k < na-1:
                big_string += ", "
        return big_string

    def ajoute_noeud(self, k, data=None):
        """G.ajoute_noeud(k) ajoute le sommet/noeud k au graphe G
           (méthode utile pour ajouter un noeud s'il possède des attributs)
           data doit être un dictionnaire typiquement {"coord" , [x,y]}.
           Si le noeud k existe déjà cette méthode ne fait rien (pas d'erreur levée)"""
        if k not in self :
            self[k] = Node(data= data)

    def ajoute_attribut(self, k, data):
        """G.ajoute_attribut(k) ajoute des attributs au sommet/noeud k du graphe G
           data doit être un dictionnaire. Si une des clés du dictionnaire existait déjà
           le contenu correspondant est effacé"""
        if k not in self :
            raise RuntimeError("Le noeud k n'est pas dans le graphe")
        if not (type(data) == dict) :
            raise TypeError("data doit être un dictionnaire")
        for cle in data :
            self[k].attr[cle] = data[cle]

    def ajoute_arete(self, node1, node2):
        """G.ajoute_arete(node1, node2) ajoute l'arête non orienté non valuée "{node1,node2}" au graphe G
           si node1 (ou node2) ne fait pas parti du graphe il y est automatiquement ajouté (inutile
           d'utiliser G.ajoute_noeud(node1))"""
        if node1 not in self :
            self[node1] = Node()
        if node2 not in self :
            self[node2] = Node()
        self[node1].voisins.add(node2)
        self[node2].voisins.add(node1)        
            
    def nb_aretes(self) :
        """G.nb_aretes() retourne le nombre d'arêtes du graphe G"""
        na = 0
        for clef in self :
            na += len(self[clef])
        return na//2  # on va compter 2 fois la même arête

    def enleve_noeud(self, node):
        """G.enleve_noeud(node) enlève le noeud node du graphe G (et toutes les arêtes
           dont node est l'un des 2 sommets)"""
        if node in self :
            for cle in self[node] :
                # on enleve node de la liste des voisins du noeud cle
                self[cle].voisins.remove(node)
            del self[node]

    def enleve_arete(self, node1, node2) :
        """G.enleve_arete(node1,node2) enlève l'arête {node1, node2} du graphe G
           (ne supprime pas node1 et node2 même s'ils sont isolés)"""
        if node1 in self and node2 in self :
            # les deux noeuds font bien partie du graphe
            # vérifions que cette arête existe bien
            if node2 in self[node1]:  
                self[node1].voisins.remove(node2)
                self[node2].voisins.remove(node1)

    def dessine(self, with_node_id=True, fontsize='medium', num_fig=None):
        """tentative de dessin d'un graphe si les sommets sont munis d'un attribut coord (en 2d seulement)
           et d'un attribut color (un entier compris entre 0 et nbcol-1, s'il n'y a pas d'attribut col le noeud
           est peint en blanc) 
        """
        import matplotlib.pyplot as plt
        import matplotlib.colors as colors
        import matplotlib.cm as cmx
        import matplotlib as mpl

        # 2 fonctions à usage interne 
        def recupere_coord(noeud, ident):
            if "coord" not in noeud.attr :
                raise RuntimeError("pas d'attribut coord pour le noeud "+format(ident))
            coord = noeud.attr["coord"]
            # coord doit être une liste (ou un tuple) à 2 éléments (on teste juste
            # la longueur, ni le type, ni le type des éléments de coord...)
            d = len(coord)
            if d != 2 :
                raise RuntimeError("dessine ne fct qu'en 2d, le noeud "+format(ident)+" est en dim "+format(d))
            return coord[0], coord[1]
        def recupere_col(noeud):
            if "col" not in noeud.attr :
                return -1
            else:
                return noeud.attr["col"]            
        if num_fig is None:
            fig = plt.figure()
        else:
            fig = plt.figure(num=num_fig);
        fig.clf()
        ax  = fig.add_axes([0.05, 0.05, 0.9, 0.9])
        xmin = inf; xmax = -inf; ymin = inf; ymax = -inf
        arete_dessinees = set()
        for i in self :
            x, y = recupere_coord(self[i], i)
            xmin = min(xmin,x); xmax = max(x, xmax)
            ymin = min(ymin,y); ymax = max(y, ymax)

            # on dessine d'abord les arêtes (en espérant que le dessin des noeuds puisse cacher...)
            for j in self[i] :
                # dessin de l'arrete {i,j} si elle n'est pas déjà dessinée
                if (j,i) not in arete_dessinees:
                    arete_dessinees.add((i,j))
                    xx, yy = recupere_coord(self[j], j)
                    ax.plot([x,xx],[y,yy], color="black")
            
            # dessin du nom du noeud avec une boîte colorée avec la couleur du noeud 
            if with_node_id:
                txt = format(i)
            else:
                txt = " "
            num_col = recupere_col(self[i])    
            if num_col == -1:   # ce noeud n'avait pas de couleur definie
                col = "white"
            elif 0 <= num_col < nb_col:
                col = graph_col[num_col]
            else:   # pas assez de couleurs ou numéro de couleur mal défini
                col = "black"
                
            ax.text(x,y, txt, va="center", ha="center", fontsize = fontsize,
                    bbox = dict(facecolor=col, edgecolor = "black"))

        # maj de l'échelle
        sx = 0.03*(xmax - xmin); sy = 0.03*(ymax - ymin)
        ax.set_xlim((xmin-sx,xmax+sx))
        ax.set_ylim((ymin-sy,ymax+sy))
        ax.set_aspect('equal')
        # on retire le cadre (et les graduations, labels éventuels)
        ax.axis("off")
        fig.suptitle(self.nom, fontsize=16)
        plt.show()


def Petersen():
    """Le graphe de Petersen"""
    theta = np.linspace(np.pi/10, 17*np.pi/10, 5)
    x = np.cos(theta)
    y = np.sin(theta)
    xx = 2*x 
    yy = 2*y
    x = np.concatenate((xx,x))
    y = np.concatenate((yy,y))
    G = GrapheElem(nom="Petersen")
    for k in range(10):
        G.ajoute_noeud(k, data={"coord":[x[k],y[k]]})
    for k in range(4):
        G.ajoute_arete(k,k+1)
    for k in range(5):
        G.ajoute_arete(k,k+5)
    G.ajoute_arete(0,4); G.ajoute_arete(5,7)
    G.ajoute_arete(5,8); G.ajoute_arete(6,8)
    G.ajoute_arete(6,9); G.ajoute_arete(7,9)
    return G

def Golomb():
    """Le graphe de Golomb"""
    theta = np.linspace(np.pi/6, 13*np.pi/6, 7)
    x = 2*np.cos(theta)
    y = 2*np.sin(theta)
    x[-1] = 0; y[-1] = 0
    xx = np.array([(x[0] + x[1] + x[6])/3, (x[2] + x[3] + x[6])/3, (x[4] + x[5] + x[6])/3])
    yy = np.array([(y[0] + y[1] + y[6])/3, (y[2] + y[3] + y[6])/3, (y[4] + y[5] + y[6])/3])    
    x = np.concatenate((x,xx))
    y = np.concatenate((y,yy))
    G = GrapheElem(nom="Golomb")
    for k in range(10):
        G.ajoute_noeud(k, data={"coord":[x[k],y[k]]})
    for k in range(5):
        G.ajoute_arete(k,k+1)
    G.ajoute_arete(5,0)    
    for k in range(6):
        G.ajoute_arete(k,6)
    G.ajoute_arete(7,8); G.ajoute_arete(8,9)
    G.ajoute_arete(9,7); G.ajoute_arete(5,7)
    G.ajoute_arete(1,8); G.ajoute_arete(3,9)
    return G

def Reine55():
    """Le graphe engendré par le contrôle des cases d'un échiquier (ici 5 x 5) 
       par une reine : étant donnée une case/noeud k:=(i,j) 0 <= i <= 4 et 
       0 <= j <= 4, le noeud k partage une arête avec toutes les autres 
       cases/noeuds qui peuvent être atteintes par une reine placée en k=(i,j)"""
    G = GrapheElem(nom = "Reine 5x5 ")
    dec = 2.9*np.pi/32
    ij = [(i,j) for j in range(5) for i in range(5)]
    # création des noeuds avec tentative de coordonnées...
    for k, (i, j) in enumerate(ij):
        # niveau du cercle
        x = i - 2; y = j - 2
        r = max(abs(x), abs(y))
        if r == 0:  # case centrale (2,2)
            G.ajoute_noeud(k, data={"coord":[0,0]})
        elif r == 1: # cercle interieur, il faut légèrement décaler l'angle
            R = np.sqrt(x**2 + y**2)
            x = x/R; y = y/R
            theta = np.arccos(x)
            if y < 0:
                theta = - theta
            x = 1.2*np.cos(theta+dec); y = 1.2*np.sin(theta+dec)
            G.ajoute_noeud(k, data={"coord":[x,y]})            
        else: # cercle extérieur
            R = np.sqrt(x**2 + y**2)
            x = r*(x/R); y = r*(y/R)
            G.ajoute_noeud(k, data={"coord":[x,y]})
    # création des arêtes (étant donnée une case (i,j), on récupère son numéro avec k = i + 5*j)
    for k, (i, j) in enumerate(ij):
        # addition des cases de la même ligne (j)
        for ii in range(5):
            if ii != i:
                kp = ii + 5*j
                if k < kp :
                    G.ajoute_arete(k, kp)
        # addition des cases de la même colonne (i)
        for jj in range(5):
            if jj != j:
                kp = i + 5*jj
                if k < kp :
                    G.ajoute_arete(k, kp)
        # addition des cases de la diagonale d'équation i+j=Cte
        num_diag = i+j
        for ii in range(5):
            jj = num_diag - ii
            if 0 <= jj <= 4 and ii!=i :
                kp = ii + 5*jj
                if k < kp :
                    G.ajoute_arete(k, kp)
        # addition des cases de la diagonale d'équation j-i=Cte
        num_diag = j-i
        for ii in range(5):
            jj = num_diag + ii
            if 0 <= jj <= 4 and ii!=i :
                kp = ii + 5*jj
                if k < kp :
                    G.ajoute_arete(k, kp)
    return G

def graphe_grille() :
    """graphe formée d'une grille
       les noeuds sont les points de coordonnées (i,j) 0 <= i < m
       et 0 <= j < n, les points sont rangés ligne par ligne.
       Dans cette version on a fixé m = 13 et n = 8.
    """
    m = 13; n = 8
    G = GrapheElem("grille")
    k = -1    
    for j in range(n):
        for i in range(m):
            k += 1
            G.ajoute_noeud(k,data={"coord":[i,j]})

    im = (m-1)/2; jm = (n-1)/2
    # création des arêtes horizontales
    for j in range(n) :
        nv = j*m
        for i in range(m-1) :
            nv += 1
            G.ajoute_arete(nv-1, nv)

    # création des arêtes verticales
    for j in range(n-1) :
        for i in range(m) :
            k1 = i+j*m; k2 = i + (j+1)*m
            G.ajoute_arete(k1, k2)

    # création d'arêtes obliques
    for j in range(n-1) :
        for i in range(m-1) :
            # on considère la cellule rectangulaire [i,i+1]x[j,j+1]
            if i < j :
                k1 = i+j*m; k2 = i+1 + (j+1)*m
                G.ajoute_arete(k1, k2)
            else:
                k1 = i+1+j*m; k2 = i + (j+1)*m
                G.ajoute_arete(k1, k2)
    return G

def mat_A_Petersen():
    """ retourne la matrice A du graphe de Petersen en format plein 
    """
    val = np.array([ 1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1,
                     -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,
                     1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,
                     1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1,
                     -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,
                     1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,
                     1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1,
                     -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1],
                   dtype=np.int32)
    i = np.array([ 0,  0,  0,  1,  1,  1,  2,  2,  2,  3,  3,  3,  4,  4,  4,  5,  5,
                   5,  6,  6,  6,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10, 10, 10, 11,
                   11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16,
                   17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22,
                   22, 23, 23, 23, 24, 24, 24, 25, 25, 25, 26, 26, 26, 27, 27, 27, 28,
                   28, 28, 29, 29, 29, 30, 30, 30, 31, 31, 31, 32, 32, 32, 33, 33, 33,
                   34, 34, 34, 35, 35, 35, 36, 36, 36, 37, 37, 37, 38, 38, 38, 39, 39,
                   39, 40, 40, 40, 41, 41, 41, 42, 42, 42, 43, 43, 43, 44, 44, 44],
                 dtype=np.int32)
    j = np.array([ 0,  1, 30, 10, 11, 31, 20, 21, 32,  0,  4, 30, 10, 14, 31, 20, 24,
                   32,  0,  5, 30, 10, 15, 31, 20, 25, 32,  1,  2, 30, 11, 12, 31, 21,
                   22, 32,  1,  6, 30, 11, 16, 31, 21, 26, 32,  2,  3, 30, 12, 13, 31,
                   22, 23, 32,  2,  7, 30, 12, 17, 31, 22, 27, 32,  3,  8, 30, 13, 18,
                   31, 23, 28, 32,  3,  4, 30, 13, 14, 31, 23, 24, 32,  4,  9, 30, 14,
                   19, 31, 24, 29, 32,  5,  8, 30, 15, 18, 31, 25, 28, 32,  5,  7, 30,
                   15, 17, 31, 25, 27, 32,  6,  8, 30, 16, 18, 31, 26, 28, 32,  6,  9,
                   30, 16, 19, 31, 26, 29, 32,  7,  9, 30, 17, 19, 31, 27, 29, 32],
                 dtype=np.int32)
    return sp.coo_array((val, (i, j)), shape=(45, 33)).toarray()


def read_dimacs(file_name, verb=False, output_fmt="GrapheElem"):
    """ tentative de lecture du format de graphe dimacs
        on ne lit que les arêtes
    """
    with open(file_name, "r") as fd:
        lines = [(line.rstrip('\n')).strip() for line in fd]

    commentaires = []
    pb_descriptor = False
    for line in lines:
        if line[0] == 'c':
            # ligne avec commentaires
            commentaires.append(line)
        elif line[0] == 'p':
            # ligne qui décrit le nombre de noeuds et d'arêtes du graphe
            # on ne doit la rencontrer qu'une seule fois avant la description
            # des arêtes (ou d'autres choses)
            words = line.split()
            if len(words) != 4:
                raise RuntimeError("la ligne commençant par p n'est pas conforme !")
            if words[1] != "edge":
                raise RuntimeError("la ligne commençant par p n'est pas conforme !")
            # n est le nombre de noeuds de ce graphe et m le nombre d'arêtes
            n = int(words[2]); m = int(words[3])
            A = np.empty((m,2), dtype=np.int32)
            i = -1
        elif line[0] == 'e':
            # ligne qui décrit une arête
            words = line.split()
            if len(words) != 3:
                raise RuntimeError("ligne de description d'une arête non conforme : "+line)
            i += 1
            if i >= m:
                raise RuntimeError("il y a plus d'arêtes qu'attendu !")
            A[i,:] = int(words[1]), int(words[2])
        else :
            if verb :
                print("Warning : ligne non prise en compte !")

    # on vérifie qu'on a bien trouvé m arêtes
    if i+1 != m:
        raise RuntimeError("On a pas trouvé {m} arêtes mais {i+1} !")

    # les noeuds sont numérotés de 1 à n, il faut numéroter de 0 à n-1
    A -= 1
    if output_fmt == "GrapheElem":
        G = GrapheElem(nom=file_name)
        for i in range(n):     # certains graphes dimacs ont des noeuds isolés et qui ne seraient pas
            G.ajoute_noeud(i)  # créés dans le graphe via la boucle suivante sur les arêtes
            
        for n1,n2 in A:  # itérations sur les lignes de A, chaque ligne comporte 2 éléments
                         # que l'on peut "extraire" dans le for (comme si c'était un tuple)
            G.ajoute_arete(n1,n2)
    else:  # on utilise une liste de 0 à n-1 (G[i] est la liste des voisins de i
        G = [None]*n
        for i in range(n):
            G[i] = []
        for n1,n2 in A:
            G[n1].append(n2)
            G[n2].append(n1)            
    return G, commentaires
 
def couleurs_distinctes(G, verb=False):
    """ vérifie que le graphe G (de type GrapheElem) est bien colorié """
    if type(G) is not GrapheElem:
        raise RuntimeError(f"On attend un objet GrapheElem et pas un {type(G)}")
    for i in G:
        # on vérifie que tous les sommets ont été coloriés
        if "col" not in G[i].attr:
            raise RuntimeError(f"le sommet {i} n'est pas colorié")
    for i in G:
        col_i = G[i].attr["col"]
        for j in G[i]: # on parcourt les voisins
            if G[j].attr["col"] == col_i:
                if verb:
                    print(f"Les sommets {i} et {j} ont une couleur identique !") 
                return False
    return True

