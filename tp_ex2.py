import numpy as np
import gurobipy as gp
import scipy as sp

#ex a
#c = np.array([6, 9, 8, 4])
#A = np.array([
#[4, 6, 5, 4],
#[3, 6, 4, 3],
#])
#b = np.array([8, 7])

#ex b
c = np.array([6, -9, 8, 4])
A = np.array([
[4, -6, 5, -4],
[3, -6, -4, 3],
])
b = np.array([2, 1])

# On d´efinit maintenant le mod`ele pour gurobi.
# 1/ Il faut d’abord instancier un objet de type ‘‘Mod`ele Gurobi’’
m = gp.Model()
# 2/ On d´efinit les variables du mod`ele (le type est ‘‘MVar Gurobi’’)
# il y a pas mal de r´eglages possibles (type des variables, bornes inf et/ou sup, donner un nom, etc.)
# par d´efaut on a des variables continues et born´ees inf´erieurement par 0
x = m.addMVar(len(c), vtype='B')
# 3/ On d´efinit la fonction objectif, exactement comme on ferait pour d´efinir le produit scalaire
# entre deux vecteurs numpy, c’est `a dire avec l’op´erateur @ (attention cependant si c est bien un
# tableau numpy, x joue le r^ole d’une sorte de variable formelle).
# Dans notre cas il faut pr´eciser qu’on veut maximiser (le d´efaut est de minimiser)
# GRB est un sous-module de gurobipy d´efinissant toutes les constantes.
m.setObjective(c @ x, gp.GRB.MAXIMIZE)
# 4/ Les contraintes se d´efinissent aussi naturellement que la fonction objectif, c’est `a dire
# avec l’op´erateur @ (bien s^ur pour des contraintes d’´egalit´e il faudrait utiliser A @ x == b
# et on pourrait aussi utiliser A @ x >= b), on peut aussi ajouter antant de contraintes que l’on
# veut.
m.addConstr( A @ x <= b)
# 5/ reste plus qu’`a r´esoudre, ce qui s’obtient avec :
m.optimize()

print("optimized")
# 6/ apr`es optimisation, on peut :
# 6-a/ obtenir le statut avec :
print(m.Status)
# qui retourne 2 pour OPTIMAL, 3 pour INFEASIBLE, 4 pour INF_OR_UNBD et 5 pour UNBOUNDED = 5
# mais d’autres possibilit´es existe comme 1 pour LOADED (le mod`ele n’a pas encore ´et´e optimis´e)
# ou encore comme 9 pour TIME_LIMIT (il est possible de d´efinir un temps max `a ne pas
# d´epasser).
# 6-b/ obtenir la solution (si le statut est OPTIMAL) sous forme de liste avec :
x_opt = m.X # ou encore np.array(m.X) pour l’avoir sous forme de tableau numpy
print(x_opt)
# 6-c/ la valeur de la fonction objectif avec
f_opt = m.ObjVal
print(f_opt)