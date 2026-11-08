import util_tp3 as u
import numpy as np
import scipy.sparse as sp
import gurobipy as gp
import pdb
import coloration as c
from pathlib import Path

def test_PL(G):
    m = c.heuristique_coloration(G)
    print(f"Heuristic colors used: {m}")
    try:
        nb_col = c.PL_coloration(G, m)
    except gp.GurobiError as error:
        print(f"Gurobi error: {error}")
        return
    print(f"PL colors used: {nb_col}")
    if nb_col is not None:
        print(f"Valid PL coloring: {u.couleurs_distinctes(G)}")

Petersen = u.Petersen()
print("Petersen:")
print(f"Deg max: {c.degmax(Petersen)}")
print(f"colors used: {c.heuristique_coloration(Petersen)}")
print(f"Distinct Colors: {u.couleurs_distinctes(Petersen)}")
petersen_A = c.mat_A(Petersen, 3)
print(np.all(petersen_A.toarray() == u.mat_A_Petersen()))
test_PL(Petersen)

Golomb = u.Golomb()
print("Golomb:")
print(f"Deg max: {c.degmax(Golomb)}")
print(f"colors used: {c.heuristique_coloration(Golomb)}")
print(f"Distinct Colors: {u.couleurs_distinctes(Golomb)}")
test_PL(Golomb)

Reine = u.Reine55()
print("Reine:")
print(f"Deg max: {c.degmax(Reine)}")
print(f"colors used: {c.heuristique_coloration(Reine)}")
print(f"Distinct Colors: {u.couleurs_distinctes(Reine)}")
test_PL(Reine)

Grille = u.graphe_grille()
print("Grille:")
print(f"Deg max: {c.degmax(Grille)}")
print(f"colors used: {c.heuristique_coloration(Grille)}")
print(f"Distinct Colors: {u.couleurs_distinctes(Grille)}")
test_PL(Grille)

for file_path in sorted(Path(__file__).resolve().parent.glob("*.col")):
    print(f"\n{file_path.name}:")
    G, commentaires = u.read_dimacs(file_path)
    test_PL(G)



