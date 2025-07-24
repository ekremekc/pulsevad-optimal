solver = 'ipopt'
 
import pyomo.environ as pyo
SOLVER = pyo.SolverFactory(solver)

assert SOLVER.available(), f"Solver {solver} is not available."

import json

coeffs = json.load(open("model_coeffs.txt"))

model = pyo.ConcreteModel("Wire optimization")


# model.display()

# create decision variables
model.x_1 = pyo.Var(bounds=(5, 10))
model.x_2 = pyo.Var(bounds=(5, 20))
model.x_3 = pyo.Var(bounds=(0, 1), domain=pyo.Binary)
model.x_4 = pyo.Var(bounds=(0, 1), domain=pyo.Binary)
model.x_5 = pyo.Var(bounds=(0, 1), domain=pyo.Binary)
model.x_6 = pyo.Var(bounds=(0, 1), domain=pyo.Binary)

# model.display()

model.cost = coeffs['Diameter'] * model.x_1 + \
             coeffs['Bending Stiffness'] * model.x_2 + \
             coeffs['Coating Material_Carbothane'] * model.x_3 + \
             coeffs['Coating Material_Pellethane'] * model.x_4 + \
             coeffs['Coating Material_silicone'] * model.x_5 + \
             coeffs['Coating Material_soft silicone'] * model.x_6

# model.display()

# objective function
model.infection_rate = pyo.Objective(expr=model.cost, sense=pyo.minimize)

# constraints

model.const = pyo.Constraint(expr = model.x_3 + model.x_4 + model.x_5 + model.x_6 == 1)


results = SOLVER.solve(model, tee=True)

# display the whole model
model.pprint()

pyo.value(model.infection_rate)


print("\n=== Optimal Wire Design to Minimize Infection Rate ===")
print(f"Diameter (mm) = {pyo.value(model.x_1): 9.2f}")
print(f"Bending Stiffness (N/mm2) = {pyo.value(model.x_2): 9.2f}")
print(f"Coating Material_Carbothane = {pyo.value(model.x_3): 9.2f}")
print(f"Coating Material_Pellethane = {pyo.value(model.x_4): 9.2f}")
print(f"Coating Material_silicone = {pyo.value(model.x_5): 9.2f}")
print(f"Coating Material_soft silicone = {pyo.value(model.x_6): 9.2f}")

print(f"Estimated infection rate = {pyo.value(model.cost): 9.2f}")
