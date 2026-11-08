# idem à tests.py mais ici on utilse une facilité de gurobi
# qui permet de déclarer plusieurs variables formelles

from util_tp1 import *
from cles_usb import *
import gurobipy as gp


# les différents tests suggérés dans l'énoncé
# (positionner cette variable sur 1, 2, 3, 4, 5 ou 6)
# le test 5 ne passe pas sans une licence gurobi
num_test = 4

# on charge les données pour le test num_test
S, t, n, m = choix_test(num_test)

print(f"S = {S}, t = {t}, n = {n}, m = {m}")


# on construit les matrices et le vecteur p associés à ces données
p, A, B = mise_en_forme_pb_cle_bis(S, m, t)

# pour l'avant dernière question (modification de la fonction objectif
# pour diminuer la redondance des solutions optimales et aussi faire en
# sorte que les premières clés soient utilisées) il suffit de décommenter
# la ligne suivante
#p = np.arange(1,m+1, dtype="int32") # création du vecteur (1,2,...,m)

# on construit le modèle gurobi
# on pourrait aussi définir un environnement gurobi pour enlever la sortie du solveur
# (cf fichier tp1_ex1_et_ex2_cor.py)
m_cle = gp.Model()
# ici on déclare donc 2 variables formelles vectorielles
# REMARQUE : pour lire la solution avec m_cle.X l'ordre est
#            l'ordre naturel dans lequel on a déclaré nos variables
#            ici m_cle.X[:m*n] => x opt
#             et m_cle.X[-m:]  => y opt
x = m_cle.addMVar(m*n, vtype=gp.GRB.BINARY)
y = m_cle.addMVar(m, vtype=gp.GRB.BINARY)
# la fct objectif s'écrit alors :
m_cle.setObjective(p @ y, gp.GRB.MINIMIZE)
# et les contraintes
m_cle.addConstr( A @ x - S*y <= 0)
m_cle.addConstr( B @ x == 1)

# on le résout
m_cle.optimize()

# la solution
if m_cle.Status == gp.GRB.OPTIMAL :
    # ici on ne redécoupe pas en x et y car les fonctions
    # post_traitement et print_keys font se travail elles-mêmes.
    x_opt = np.array(m_cle.X)
    F_opt = m_cle.ObjVal
    print(f"F_opt = {F_opt}")
    print(f"x_opt = {x_opt}")
    post_traitement(x_opt, n, m)
    print_key(S, t, x_opt, m)
else:
    print("Echec de l'optimisation : {m_cle.Status}")

# calcul d'une solution heuristique (il faudrait en fait obtenir
# cette solution avant pour travail avec une valeur de m pas trop grande....)
Sol = sol_heuristique(S,t)
print("\n Solution heuristique :")
nk = len(Sol)
print(f"   nb de clés = {len(Sol)}")
for i in range(nk) :
    print("   La clé "+format(i)+" stocke les fichiers : ",Sol[i])
    
