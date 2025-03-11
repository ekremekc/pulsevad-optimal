import numpy as np
import scipy.optimize as opt
import json

coeffs = json.load(open("model_coeffs.txt"))

# Example Coefficients (from regression or assumed)
coeff_diameter = coeffs['Diameter']      # Infection rate increase per mm of diameter
coeff_coating = {         # Infection rate impact by coating type
    'Coating_Carbothane':coeffs['Coating_Carbothane'], 
    'Coating_Pellethane': coeffs['Coating_Pellethane'], 
    'Coating_polyurethane': coeffs['Coating_polyurethane'], 
    'Coating_soft_silicone': coeffs['Coating_soft_silicone']
}

print(coeff_coating)
# # Example Coefficients (from regression or assumed)
# coeff_diameter = 2.333      # Infection rate increase per mm of diameter
# coeff_coating = {         # Infection rate impact by coating type
#     "Pellethane": 0.5,
#     "Carbothane": -1.4,
#     "soft_silicone": -4.7,
#     "polyurethane": -1.4,
# }

# Define the Objective Function to Minimize Infection Rate
def infection_rate(params):
    diameter, coating_idx = params

    # Convert categorical coating to numerical effect
    coating_types = ["Coating_Carbothane", "Coating_Pellethane", "Coating_polyurethane", "Coating_soft_silicone"]
    coating = coating_types[int(round(coating_idx))]  # Ensure valid index
    coating_effect = coeff_coating[coating]

    # Infection rate prediction
    infection_rate = (
        coeff_diameter * diameter +
        coating_effect
    )

    return infection_rate  # Goal is to minimize this

# Define Bounds (Realistic Ranges for Each Parameter)
bounds = [
    (4.0, 7.0),  # Diameter range (mm)
    (0, 3)       # Coating (0: A, 1: B, 2: C)
]

# Define Initial Guess
initial_guess = [5.7, 3]  # Example starting point

# Solve Optimization Problem
result = opt.minimize(infection_rate, initial_guess, method='SLSQP', bounds=bounds)

# Extract Optimal Values
optimal_diameter, optimal_coating_idx = result.x
optimal_coating = ["Coating_Carbothane", "Coating_Pellethane", "Coating_polyurethane", "Coating_soft_silicone"][int(round(optimal_coating_idx))]  # Convert index to coating type

# Print Results
print("Optimized Wire Design:")
print(f"Optimal Diameter: {optimal_diameter:.2f} mm")
print(f"Optimal Coating Material: {optimal_coating}")
print(f"Predicted Minimum Infection Rate: {infection_rate(result.x):.2f} %")
