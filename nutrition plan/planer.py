import pandas as pd
from ortools.linear_solver import pywraplp
#df=pd.read_csv('./nutrition plan/nutrition_data.csv',index_col=0)
df=pd.read_csv('nutrition_data.csv',index_col=0)
df=df[df["name"]=="Energy"]
df_groups=df.groupby("description").agg({"name":list,"amount":list,"unit_name":list,"food_category":list})
df_list=df_groups[100:500]
optimal_energy=[2100]
solver = pywraplp.Solver.CreateSolver("SCIP")
if solver is None:
    print("SCIP solver unavailable.")
    exit()

x={}
for idx, row in df_groups.iterrows():
    for j in optimal_energy:
        x[idx,"Energy"]=solver.BoolVar(f"x_{idx}_Energy")

# The amount packed in each bin cannot exceed its capacity.
for b in optimal_energy:
    solver.Add(
        sum(x[idx, "Energy"] * int(row["amount"][0]) for idx, row in df_groups.iterrows())
        <= b
    )
# Maximize total value of packed items.
objective = solver.Objective()
for idx, row in df_groups.iterrows():
    for b in optimal_energy:
        objective.SetCoefficient(x[idx,"Energy"],1)
objective.SetMaximization()

print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f"Total packed value: {objective.Value()}")
    total_weight = 0
    for b in optimal_energy:
        print(f"Bin {b}")
        sum_weight = 0
        for idx, row in df_groups.iterrows():
            if x[idx,"Energy"].solution_value() > 0:
                print( f"Item {idx} - energy: {row['amount'][0]}, value: {x[idx,'Energy'].solution_value()}, unit {row['unit_name'][0]} ")
                sum_weight += row["amount"][0] * x[idx,"Energy"].solution_value()
        print(f"Total weight: {sum_weight}")
        print("Groups", df_groups.shape)
else:
    print("The problem does not have an optimal solution.")
