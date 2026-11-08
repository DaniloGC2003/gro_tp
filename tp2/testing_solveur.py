from util_tp2 import *
from heuristiques_squelette import *
from solveur_pse_squelette import *
from time import time

# choix du pb
c, A, b = pbsac4()

print(f"nb variables = {len(c)}")
print(f"nb contraintes = {len(b)}")

t0 = time()
xb, Fb = heuristique(c, A, b)
th = time() - t0
print(f" temps heuristiques = {th}\n F heuristique = {Fb}")

t0 = time()
xopt, Fopt, nb_node = solveur_pse_bin(c, A, b, xb, Fb)
ts = time() - t0
print(f" temps solveur pse = {ts}")
print(f" F opt = {Fopt}")
print(f" nb de noeuds créés : {nb_node}")
print(f" x_opt = : {xopt}")




