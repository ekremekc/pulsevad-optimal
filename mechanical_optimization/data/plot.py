import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# data = np.loadtxt('test_data/22awg_silicone_1_50mm.txt')
column_names = ['Load (N)', 'Machine Extension (mm)']
path = 'test_data/22awg_silicone_1_50mm.txt'
df = pd.read_csv(path, encoding='utf-16', usecols=column_names, sep='\t')

load_1 = df['Load (N)'] 
disp_1 = df['Machine Extension (mm)'] 

plt.plot(disp_1, load_1)
plt.savefig("force_disp.pdf")
plt.close()


r_out = 1.7/2 #mm
r_in = (1.7-0.49)/2 #mm
A_i = np.pi*(r_out**2-r_in**2)
L0 = 50 # mm
L_instant = L0 + disp_1
A_instant = A_i*L0/L_instant

strain = disp_1/L0
stress_eng = load_1/A_i
stress_true = load_1/A_instant

plt.plot(strain, stress_eng)
plt.plot(strain, stress_true)
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.grid(True)
plt.savefig("stress_strain.pdf")

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(strain.values.reshape(-1, 1), stress_true.values)
E_modulus_MPa = model.coef_[0]
print(f"Estimated Elastic Modulus: {E_modulus_MPa:.3f} MPa")
