import numpy as np
import gurobipy as gp
import scipy.sparse as sp
import util_tp1 as ut

TEST_ID = 6

def print_arr_data(arr, arr_name):
    print(f"Arr {arr_name} data:")
    print(arr)

def create_a_b_p(S, t, n, m):
    # Matrix A
    val = []
    i_idx = []
    j_idx = []
    for j in range(m):
        for i in range(n):
            val.append(t[i])
            i_idx.append(j)
            j_idx.append(j * n + i)
    A_blocks = sp.coo_array((val, (i_idx, j_idx)), shape=(m, n * m))
    block_S = -S * sp.eye(m)
    A = sp.hstack((A_blocks, block_S))
    #print_arr_data(A.toarray(), "A")

    # Matrix B
    m_ones = np.ones(m)
    n_identity = sp.eye(n)
    B = sp.kron(m_ones, n_identity, format='coo')
    zeros_matrix = np.zeros((n, m))
    B = sp.hstack((B, zeros_matrix))
    #print_arr_data(B.toarray(), "B")

    # Array p
    p = np.zeros(n * m)
    p = np.hstack((p, np.ones(m)))
    #p = np.hstack([np.zeros(n * m), np.ones(m)])
    #print_arr_data(p, "p")

    return A, B, p


S, t, n, m = ut.choix_test(TEST_ID)
print(f"Parameters: S = {S}, t = {t}, n = {n}, m = {m}")
matrix_A, matrix_B, array_p = create_a_b_p(S, t, n, m)
# arrays b and d
array_b = np.zeros(m)
array_d = np.ones(n)


model = gp.Model()
x = model.addMVar(len(array_p), vtype='B')
model.setObjective(array_p @ x, gp.GRB.MINIMIZE)
model.addConstr(matrix_A @ x <= array_b)
model.addConstr(matrix_B @ x == array_d)
model.optimize()
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