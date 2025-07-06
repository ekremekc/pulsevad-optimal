import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

r_out = 1.7/2 #mm
r_in = (1.7-0.49)/2 #mm
A_silicone = np.pi*(r_out**2-r_in**2)
L_copper = L_silicone = 50 # mm

A_copper = np.pi*r_in**2 #mm
A_latex = 0.8*6.4 #mm
L_latex = 30.5

path1 = 'test_data/22awg_silicone_1_50mm.txt'
path2 = 'test_data/22awg_silicone_2_50mm.txt'
path3 = 'test_data/22awg_silicone_3_50mm.txt'

path_copper_1a = 'test_data/22awg_copper_1a_50mm.txt'
path_copper_2a = 'test_data/22awg_copper_2a_50mm.txt'
path_copper_3a = 'test_data/22awg_copper_3a_50mm.txt'
path_copper_1 = 'test_data/22awg_copper_1_50mm.txt'
path_copper_2 = 'test_data/22awg_copper_2_50mm.txt'
path_copper_3 = 'test_data/22awg_copper_3_50mm.txt'

path_latex = 'test_data/latex_1_30.5mm.txt'

def calculateElasticModulus(path, L0, Ai, elastic=None):
    column_names = ['Load (N)', 'Machine Extension (mm)']
    df = pd.read_csv(path, encoding='utf-16', usecols=column_names, sep='\t')

    load_1 = df['Load (N)'] 
    disp_1 = df['Machine Extension (mm)'] 

    strain = disp_1/L0
    if elastic:
        L_instant = L0 + disp_1
        A_instant = Ai*L0/L_instant
        stress = load_1/A_instant # true stress
    else:
        stress = load_1/Ai # engineering stress

    model = LinearRegression()
    model.fit(strain.values.reshape(-1, 1), stress.values)
    E_modulus_MPa = model.coef_[0]
    print(f"Estimated Elastic Modulus: {E_modulus_MPa:.3f} MPa")
    return E_modulus_MPa

print("Silicone jacket: ")
E_silicone_1 = calculateElasticModulus(path1, L_silicone, A_silicone, elastic=True)
E_silicone_2 = calculateElasticModulus(path2, L_silicone, A_silicone, elastic=True)
E_silicone_3 = calculateElasticModulus(path3, L_silicone, A_silicone, elastic=True)
print(f"Averaged Elastic Modulus: {np.average([E_silicone_1, E_silicone_2, E_silicone_3]):.3f} MPa")

print("\nCopper conductor: ")
E_copper_1 = calculateElasticModulus(path_copper_1, L_copper, A_copper)
E_copper_2 = calculateElasticModulus(path_copper_2, L_copper, A_copper)
E_copper_3 = calculateElasticModulus(path_copper_3, L_copper, A_copper)
E_copper_1a = calculateElasticModulus(path_copper_1a, L_copper, A_copper)
# E_copper_2a = calculateElasticModulus(path_copper_2a, L_copper, A_copper)
E_copper_3a = calculateElasticModulus(path_copper_3a, L_copper, A_copper)
print(f"Averaged Elastic Modulus: {np.average([E_copper_1, E_copper_2, E_copper_3, E_copper_1a,  E_copper_3a]):.3f} MPa")


print("\nLatex: ")
E_copper_3a = calculateElasticModulus(path_latex, L_latex, A_latex, elastic=True)

