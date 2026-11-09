import util_tp3 as u
import coloration as col
from time import time

# choisir un fichier dimacs
fich = "myciel5.col"
G, commentaires = u.read_dimacs(fich)

# ou l'un des graphes avec coordonnées 
#G = u.graphe_grille(19,12)
#fich = "grille"

print("\n -----------------------------------------")
print(f" Pour le graphe {fich}")

# heuristique
t0 = time()
m = col.heuristique_coloration(G)
t1 = time() - t0
# on vérifie que les couleurs sont bien distinctes
if not u.couleurs_distinctes(G):
    print(" l'heuristique semble bugguée")
print(f"   l'heuristique trouve {m} couleurs en {t1} secondes")
print(" -----------------------------------------\n")
# on peut dessiner éventuellement le graphe s'il a des coordonnées 2d
#G.dessine()


# résolution du PL
t0 = time()
ka = col.PL_coloration(G, m, with_gurobi_output=True)
t1 = time() - t0
print(f"\n   la résolution du PL donne kappa = {ka} couleurs en {t1} secondes")
# on peut dessiner éventuellement le graphe s'il a des coordonnées 2d
#G.dessine()

