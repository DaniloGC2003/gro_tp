import numpy as np
import scipy.sparse as sp
import util_tp1 as ut

def create_A(m, n, t, S):
    n_ones = np.ones(n)
    m_range = np.arange(m)
    i = np.kron(m_range, n_ones)
    #print(i)
    j = np.arange(m*n)
    #print(j)
    m_ones = np.ones(m)
    val = np.kron(m_ones, t)
    #print(val)

    A_left_part = sp.coo_array((val, (i, j)), shape=(m, n*m))
    A = sp.hstack((A_left_part, -S * sp.eye(m)))
    #print(A)
    return A
def create_B(m, n, t, S):
    B_left_part = sp.eye(n)
    for i in range(m-1):
        B_left_part = sp.hstack((B_left_part, sp.eye(n)))
    #print(B_left_part)
    zeros_matrix = np.zeros((n, m))
    B = sp.hstack((B_left_part, zeros_matrix), format='coo')
    return B
def create_p(m, n, t, S):
    p = np.zeros(n*m)
    p = sp.hstack((p, np.ones(m)))
    return p

def create_b(m, n, t, S):
    return np.zeros(m)

def create_d(m, n, t, S):
    return np.ones(n)

def sol_heuristique(S,t):
    n = len(t)
    # tri des fichiers (calcul des indices inds de sorte que t[inds[0]] <= t[inds[1]] <= ... t[inds[n-1]]
    inds = np.argsort(t)
    # petit test
    if t[inds[n-1]] > S :
        raise RuntimeError("La taille des cl´es est inf´erieure au plus gros fichier !")

    disks = [] # Each disk contains the indices of its assigned files.
    for file in reversed(inds): # iterate though indices from t
        file_stored = False
        for d in disks:
            if S - sum(t[i] for i in d) >= t[file]:
                file_stored = True
                d.append(file)
                break
        if not file_stored:
            disks.append([file])

    return disks
