import util_tp3 as u
import coloration as col
from time import time

for fich in u.fichiers_dimacs:
    G, commentaires = u.read_dimacs(fich)
    t0 = time()
    m = col.heuristique_coloration(G)
    t1 = time() - t0
    if not u.couleurs_distinctes(G):
        print(" WARNING : l'heuristique semble bugguée")

    print("\n -----------------------------------------")
    print(f" Pour le graphe {fich} ({len(G)} sommets et {G.nb_aretes()} arêtes)") 
    print(f"   l'heuristique trouve {m} couleurs en {t1} secondes")
    print(f"   le nombre chromatique est {u.fichiers_dimacs[fich]}")

print("\n")

