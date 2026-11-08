import numpy as np
import gurobipy as gp
import scipy.sparse as sp
import util_tp1 as ut
import cles_usb as cl
import time

TEST_ID = 4

S, t, n, m = ut.choix_test(TEST_ID)
print(f"Parameters: S = {S}, t = {t}, n = {n}, m = {m}")
matrix_A, matrix_B, array_p = cl.create_a_b_p(S, t, n, m)
# arrays b and d
array_b = np.zeros(m)
array_d = np.ones(n)


model = gp.Model()
x = model.addMVar(len(array_p), vtype='B')
model.setObjective(array_p @ x, gp.GRB.MINIMIZE)
model.addConstr(matrix_A @ x <= array_b)
model.addConstr(matrix_B @ x == array_d)
start = time.time()
model.optimize()
end = time.time()
print(f"elapsed time: {end - start}")
#print(f"solution status: {model.Status}")
x_opt = model.X # ou encore np.array(m.X) pour l’avoir sous forme de tableau numpy
f_opt = model.ObjVal
print(f_opt)

ut.post_traitement(x_opt, n, m)
ut.print_key(S, t, x_opt, m)

# output:
#reconstructed x (one line per file, one column per USB stick):
#0	0	1	0
#0	0	1	0
#0	1	0	0
# USB sticks used:
# 0.0, 1.0, 1.0, 0.0