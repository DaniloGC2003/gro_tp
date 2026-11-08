from util_tp2 import *
from time import time
import gurobipy as gp

# choix du pb
c, A, b = pbsac6()

model = gp.Model()
x = model.addMVar(len(c), vtype='B')
model.setObjective(c@x, gp.GRB.MAXIMIZE)
model.addConstr(A@x <= b)

model.optimize()

print(f"status: {model.Status}")
print(f"solution: {[int(v) for v in model.X]}")
print(f"Optimal value: {model.ObjVal}")