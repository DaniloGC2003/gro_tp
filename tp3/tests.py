import util_tp3 as u
import numpy as np
import scipy.sparse as sp
import gurobipy as gp
import pdb
import coloration as c
from pathlib import Path

Petersen = u.Petersen()
print("Petersen:")
print(f"Deg max: {c.degmax(Petersen)}")
print(f"colors used: {c.heuristique_coloration(Petersen)}")
print(f"Distinct Colors: {u.couleurs_distinctes(Petersen)}")

Golomb = u.Golomb()
print("Golomb:")
print(f"Deg max: {c.degmax(Golomb)}")
print(f"colors used: {c.heuristique_coloration(Golomb)}")
print(f"Distinct Colors: {u.couleurs_distinctes(Golomb)}")

Reine = u.Reine55()
print("Reine:")
print(f"Deg max: {c.degmax(Reine)}")
print(f"colors used: {c.heuristique_coloration(Reine)}")
print(f"Distinct Colors: {u.couleurs_distinctes(Reine)}")

Grille = u.graphe_grille()
print("Grille:")
print(f"Deg max: {c.degmax(Grille)}")
print(f"colors used: {c.heuristique_coloration(Grille)}")
print(f"Distinct Colors: {u.couleurs_distinctes(Grille)}")

for file_path in sorted(Path(__file__).resolve().parent.glob("*.col")):
    G, commentaires = u.read_dimacs(file_path)
    print(f"{file_path.name}: {c.heuristique_coloration(G)} colors used")

