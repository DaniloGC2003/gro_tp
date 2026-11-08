from util_tp2 import *
from heuristiques import *
from time import time

""" permet de repoduire le tableau des résultats des heuristiques sur les 9 pbs de sac à dos """

noms_pb = ["pbsac1", "pbsac2", "pbsac3", "pbsac4", "pbsac5", "pbsac6", "pbsac7", "pbsac8", "pbsac9"]  

barre_horizontale = "\n"+"--------+"*5
for pb in noms_pb:
    
    c, A, b = eval(pb+"()")    # eval permet d'exécuter le code python (ici pbsac<x>())
    print(barre_horizontale)
    print(f" {pb} |", end="")
    xb, Fb = heuristique(c, A, b, verb=True)
print(barre_horizontale)


