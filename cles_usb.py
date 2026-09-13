import numpy as np
import gurobipy as gp
import scipy.sparse as sp
import util_tp1 as ut
import time as tm

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
    #p = np.hstack((p, np.arange(1, m+1, dtype='int32'))) # para ex 6

    #print_arr_data(p, "p")

    return A, B, p

def sol_heuristique(S,t):
    print(f"values: {S}, {t}")
    #tm.sleep(3)
    m = 0 # USB sticks used
    n = len(t)
    usb_sticks_storage = []
    # tri des fichiers (calcul des indices inds de sorte que t[inds[0]] <= t[inds[1]] <= ... t[inds[n-1]]
    inds = np.argsort(t)
    print(f"inds: {inds}")
    for file in reversed(inds):
        #print(file)
        file_allocated = False
        for k in range (m):
            if usb_sticks_storage[k] >= t[file]:
                usb_sticks_storage[k] -= t[file]
                file_allocated = True
        if not file_allocated:
            #print("creating new USB stick")
            m += 1 # add new USB stick
            usb_sticks_storage.append(S)
            usb_sticks_storage[m - 1] -= t[file]
            #print(usb_sticks_storage)
    return m

    # petit test
    if t[inds[n-1]] > S :
        raise RuntimeError("La taille des cl´es est inf´erieure au plus gros fichier !")