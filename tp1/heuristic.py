import numpy as np
import gurobipy as gp
import scipy.sparse as sp
import util_tp1 as ut
import cles_usb as cl

TEST_ID = 6

S, t, n, m = ut.choix_test(TEST_ID)
print(f"number of USB sticks estimated: {cl.sol_heuristique(S, t)}")

print(f"number of USB sticks estimated new: {cl.sol_heuristique_new(S, t)}")
