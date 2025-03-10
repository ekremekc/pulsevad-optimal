import numpy as np
import scipy.optimize as opt

# Example Coefficients (from regression or assumed)
coeff_diameter = 2.5      # Infection rate increase per mm of diameter
coeff_flexibility = -1.8  # Infection rate decrease per unit flexibility
coeff_coating = {         # Infection rate impact by coating type
    "A": 0.5,
    "B": -0.3,
    "C": 0.2
}

# Define the Objective Function to Minimize Infection Rate
def infection_rate(params):
    diameter, flexibility, coating_idx = params

    # Convert categorical coating to numerical effect
    coating_types = ["A", "B", "C"]
    coating = coating_types[int(round(coating_idx))]  # Ensure valid index
    coating_effect = coeff_coating[coating]

    # Infection rate prediction
    infection_rate = (
        coeff_diameter * diameter +
        coeff_flexibility * flexibility +
        coating_effect
    )

    return infection_rate  # Goal is to minimize this

# Define Bounds (Realistic Ranges for Each Parameter)
bounds = [
    (0.5, 1.0),  # Diameter range (mm)
    (2.0, 5.0),  # Flexibility range (N/mm)
    (0, 2)       # Coating (0: A, 1: B, 2: C)
]

# Define Initial Guess
initial_guess = [0.7, 3.0, 1]  # Example starting point

# Solve Optimization Problem
result = opt.minimize(infection_rate, initial_guess, method='SLSQP', bounds=bounds)

# Extract Optimal Values
optimal_diameter, optimal_flexibility, optimal_coating_idx = result.x
optimal_coating = ["A", "B", "C"][int(round(optimal_coating_idx))]  # Convert index to coating type

# Print Results
print("Optimized Wire Design:")
print(f"Optimal Diameter: {optimal_diameter:.2f} mm")
print(f"Optimal Flexibility: {optimal_flexibility:.2f} N/mm")
print(f"Optimal Coating Material: {optimal_coating}")
print(f"Predicted Minimum Infection Rate: {infection_rate(result.x):.2f} %")
