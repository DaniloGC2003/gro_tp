import numpy as np
import scipy.sparse as sp
import util_tp1 as ut

def create_A(m, n, t, S):
    #n 0's, n 1's...
    i = np.kron(np.arange(m), np.ones(n))
    j = np.arange(n*m)
    val = np.kron(np.ones(m), t)

    A = sp.coo_array((val, (i, j)), shape=(m, n*m))

    A = sp.hstack((A, -S * sp.eye(m)))
    return A

def create_B(m, n, t, S):
    B = sp.eye(n)
    for i in range(m-1):
        B = sp.hstack((B, sp.eye(n)))
    B = sp.hstack((B, np.zeros((n, m))))
    return B