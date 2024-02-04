import pandas as pd
from ortools.linear_solver import pywraplp
df=pd.read_csv('./nutrition plan/nutrition_data.csv',index_col=0)
df=df[df["name"]=="Energy"]
df_groups=df.groupby("description").agg({"name":list,"amount":list,"unit_name":list,"food_category":list})
df_list=df_groups[100:500]
optimal_energy=[2000]
solver = pywraplp.Solver.CreateSolver("SCIP")
if solver is None:
    print("SCIP solver unavailable.")
    exit()
x={}
for i in df_groups:
    for j in optimal_energy:
        x[i["description"],"Energy"]=solver.BoolVar(f"x_{i['description']}_Energy")


# The amount packed in each bin cannot exceed its capacity.
for b in optimal_energy:
    solver.Add(
        sum(x[i["description"],"Energy"] * int(i["amount"][0]) for i in df_groups)
        <= b
    )
# Maximize total value of packed items.
objective = solver.Objective()
for i in df_groups:
    for b in optimal_energy:
        objective.SetCoefficient(x[i["description"],"Energy"],1)
objective.SetMaximization()

print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f"Total packed value: {objective.Value()}")
    total_weight = 0
    for b in optimal_energy:
        print(f"Bin {b}")
        bin_weight = 0
        bin_value = 0
        for i in df_groups:
            if x[i["description"],"Energy"].solution_value() > 0:
                print(
                    f"Item {i['description']}"
                )
else:
    print("The problem does not have an optimal solution.")