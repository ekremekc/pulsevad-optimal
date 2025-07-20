import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 18})

column_names = ['Load (N)', 'Machine Extension (mm)']

def readData(path):
    df = pd.read_csv(path, sep='\t', encoding='utf-16-le', skiprows=[1])
    print(df.columns)  # Check if correct

    # Drop rows where 'Machine Extension (mm)' is NaN or empty
    df = df[df['Machine Extension (mm)'].notna()]
    df = df[df['Machine Extension (mm)'].astype(str).str.strip() != '']

    disp = df['Machine Extension (mm)'].astype(float)
    load = df['Load (N)'].astype(float)

    mask = disp <= 15.0
    return disp[mask], load[mask]

# hm3
hm3Path1 = 'hm3/7/test1.txt'
hm3Path2 = 'hm3/7/test2.txt'
hm3Path3 = 'hm3/7/test3.txt'

disp_1, load_1 = readData(hm3Path1) 
disp_2, load_2 = readData(hm3Path2) 
disp_3, load_3 = readData(hm3Path3) 

plt.figure(figsize=(6, 6))
plt.plot(disp_1, load_1, label='test 1')
plt.plot(disp_2, load_2, label='test 2')
plt.plot(disp_3, load_3, label='test 3')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.ylim(0, 2)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/hm3.png", dpi=300)
plt.show()
plt.close()

# HVAD
HVADPath1 = 'HVAD/test1.txt'
HVADPath2 = 'HVAD/test2.txt'
HVADPath3 = 'HVAD/test3.txt'

disp_1, load_1 = readData(HVADPath1) 
disp_2, load_2 = readData(HVADPath2) 
disp_3, load_3 = readData(HVADPath3) 

plt.figure(figsize=(6, 6))
plt.plot(disp_1, load_1, label='test 1')
plt.plot(disp_2, load_2, label='test 2')
plt.plot(disp_3, load_3, label='test 3')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.ylim(0, 2)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/HVAD.png", dpi=300)
plt.show()
plt.close()

# # Ventrassist
# VentrassistPath1 = 'Ventrassist/test1.txt'
# VentrassistPath2 = 'Ventrassist/test2.txt'
# VentrassistPath3 = 'Ventrassist/test3.txt'

# disp_1, load_1 = readData(VentrassistPath1) 
# disp_2, load_2 = readData(VentrassistPath2) 
# disp_3, load_3 = readData(VentrassistPath3) 

# plt.plot(disp_1, load_1, label='test 1')
# plt.plot(disp_2, load_2, label='test 2')
# plt.plot(disp_3, load_3, label='test 3')
# plt.xlabel('Displacement (mm)')
# plt.ylabel('Load (N)')
# plt.ylim(0, 4)
# plt.legend()
# plt.tight_layout()
# plt.savefig("plots/Ventrassist.png", dpi=300)
# plt.show()
# plt.close()