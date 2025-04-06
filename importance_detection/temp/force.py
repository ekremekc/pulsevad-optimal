import numpy as np
import matplotlib.pyplot as plt

# --- Reuse these helper functions ---
def axial_area(D_mm, d_mm):
    D = D_mm / 1000
    d = d_mm / 1000
    return (np.pi / 4) * (D**2 - d**2)

def layerwise_tensile_stress(F_N, layers):
    layer_EA = []
    areas = []

    for layer in layers:
        A = axial_area(layer['D_mm'], layer['d_mm'])
        E = layer['E_GPa'] * 1e9
        layer_EA.append(E * A)
        areas.append(A)
    
    total_EA = sum(layer_EA)
    strain = F_N / total_EA  # same strain for all layers

    stresses = []
    for i, layer in enumerate(layers):
        E = layer['E_GPa'] * 1e9
        sigma = E * strain  # stress = E * strain
        stresses.append(sigma)

    return stresses  # in Pascals

# --- Example wire design ---
layers = [
    {'D_mm': 0.8, 'd_mm': 0.6, 'E_GPa': 0.5},    # outer soft polymer
    {'D_mm': 0.6, 'd_mm': 0.3, 'E_GPa': 5.0},    # middle harder polymer
    {'D_mm': 0.3, 'd_mm': 0.0, 'E_GPa': 117}   # metal core
]

F_applied = 300  # axial force in Newtons

# --- Compute stresses ---
stresses = layerwise_tensile_stress(F_applied, layers)
stresses_mpa = [s / 1e6 for s in stresses]  # Convert to MPa

# --- Plotting ---
layer_labels = [f"Layer {i+1} ({l['E_GPa']} GPa)" for i, l in enumerate(layers)]

plt.figure(figsize=(8, 5))
bars = plt.bar(layer_labels, stresses_mpa, color='steelblue')
plt.ylabel('Tensile Stress (MPa)')
plt.title('Tensile Stress Distribution Across Layers')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.ylim(0, max(stresses_mpa)*1.2)

# Annotate bars
for bar, val in zip(bars, stresses_mpa):
    plt.text(bar.get_x() + bar.get_width()/2, val + 0.05, f"{val:.2f}", ha='center', va='bottom')

plt.tight_layout()
plt.show()