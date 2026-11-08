from util_tp1 import *
from cles_usb import *
import gurobipy as gp


# les différents tests suggérés dans l'énoncé
# (positionner cette variable sur 1, 2, 3, 4, 5 ou 6)
# le test 5 ne passe pas sans une licence gurobi
num_test = 2

# on charge les données pour le test num_test
S, t, n, m = choix_test(num_test)

print(f"S = {S}, t = {t}, n = {n}, m = {m}")


# on construit les matrices et le vecteur p associés à ces données
p, A, B = mise_en_forme_pb_cle(S, m, t)

# pour l'avant dernière question (modification de la fonction objectif
# pour diminuer la redondance des solutions optimales et aussi faire en
# sorte que les premières clés soient utilisées) il suffit de décommenter
# la ligne suivante
#p = np.arange(1,m+1, dtype="int32") # création du vecteur (1,2,...,m)

# on construit le modèle gurobi
nb_var = m*(n+1)
# on pourrait aussi définir un environnement gurobi pour enlever la sortie du solveur
# (cf fichier tp1_ex1_et_ex2_cor.py)
m_cle = gp.Model()
X = m_cle.addMVar(nb_var, vtype=gp.GRB.BINARY)
m_cle.setObjective(p @ X[-m:], gp.GRB.MINIMIZE)
m_cle.addConstr( A @ X <= 0)
m_cle.addConstr( B @ X[:-m] == 1)

# on le résout
m_cle.optimize()

# la solution
if m_cle.Status == gp.GRB.OPTIMAL :
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
print(Sol)
for i in range(nk) :
    print("   La clé "+format(i)+" stocke les fichiers : ",Sol[i])
    
