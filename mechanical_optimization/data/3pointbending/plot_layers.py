import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 18})

column_names = ['Load (N)', 'Machine Extension (mm)']

def readData(path, max_disp=15.00):
    df = pd.read_csv(path, sep='\t', encoding='utf-16-le')
    print(df.columns)  # Check if correct

    # Drop rows where 'Machine Extension (mm)' is NaN or empty
    df = df[df['Machine Extension (mm)'].notna()]
    df = df[df['Machine Extension (mm)'].astype(str).str.strip() != '']

    disp = df['Machine Extension (mm)'].astype(float)
    load = df['Load (N)'].astype(float)

    mask = disp <= max_disp
    return disp[mask], load[mask]
    # return disp, load 

# 1b
onePath1 = 'hm3/1b/test1.txt'
onePath2 = 'hm3/1b/test2.txt'
onePath3 = 'hm3/1b/test3.txt'
onePath4 = 'hm3/1b/test4.txt'
onePath5 = 'hm3/1b/test5.txt'
onePath6 = 'hm3/1b/test6.txt'

disp_1, load_1 = readData(onePath1) 
disp_2, load_2 = readData(onePath2) 
disp_3, load_3 = readData(onePath3) 
disp_4, load_4 = readData(onePath4) 
disp_5, load_5 = readData(onePath5) 
disp_6, load_6 = readData(onePath6) 

plt.figure(figsize=(6, 6))
plt.plot(disp_1, load_1, label='test 1')
plt.plot(disp_2, load_2, label='test 2')
plt.plot(disp_3, load_3, label='test 3')
plt.plot(disp_4, load_4, label='test 4')
plt.plot(disp_5, load_5, label='test 5')
plt.plot(disp_6, load_6, label='test 6')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.ylim(0, 1)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/layers/1b.png", dpi=300)
plt.show()
plt.close()

# 2
twoPath1 = 'hm3/2b/test1.txt'
twoPath2 = 'hm3/2b/test2.txt'
twoPath3 = 'hm3/2b/test3.txt'
twoPath4 = 'hm3/2b/test4.txt'
twoPath5 = 'hm3/2b/test5.txt'
twoPath6 = 'hm3/2b/test6.txt'

disp_1, load_1 = readData(twoPath1) 
disp_2, load_2 = readData(twoPath2) 
disp_3, load_3 = readData(twoPath3) 
disp_4, load_4 = readData(twoPath4) 
disp_5, load_5 = readData(twoPath5) 
disp_6, load_6 = readData(twoPath6) 

plt.figure(figsize=(6, 6))
plt.plot(disp_1, load_1, label='test 1')
plt.plot(disp_2, load_2, label='test 2')
plt.plot(disp_3, load_3, label='test 3')
plt.plot(disp_4, load_4, label='test 4')
plt.plot(disp_5, load_5, label='test 5')
plt.plot(disp_6, load_6, label='test 6')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.ylim(0, 0.2)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/layers/2b.png", dpi=300)
plt.show()
plt.close()

# 4
twoPath1 = 'hm3/4/test1.txt'
twoPath2 = 'hm3/4/test2.txt'
twoPath3 = 'hm3/4/test3.txt'

disp_1, load_1 = readData(twoPath1, max_disp=4) 
disp_2, load_2 = readData(twoPath2, max_disp=4) 
disp_3, load_3 = readData(twoPath3, max_disp=4) 

plt.figure(figsize=(6, 6))
plt.plot(disp_1, load_1, label='test 1')
plt.plot(disp_2, load_2, label='test 2')
plt.plot(disp_3, load_3, label='test 3')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.ylim(0, 1)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/layers/4.png", dpi=300)
plt.show()
plt.close()

# 5
twoPath1 = 'hm3/5/test1.txt'
twoPath2 = 'hm3/5/test2.txt'
twoPath3 = 'hm3/5/test3.txt'

disp_1, load_1 = readData(twoPath1, max_disp=4) 
disp_2, load_2 = readData(twoPath2, max_disp=4) 
disp_3, load_3 = readData(twoPath3, max_disp=4) 

plt.figure(figsize=(6, 6))
plt.plot(disp_1, load_1, label='test 1')
plt.plot(disp_2, load_2, label='test 2')
plt.plot(disp_3, load_3, label='test 3')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.ylim(0, 1)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/layers/5.png", dpi=300)
plt.show()
plt.close()

# 6
twoPath1 = 'hm3/6/test1.txt'
twoPath2 = 'hm3/6/test2.txt'
twoPath3 = 'hm3/6/test3.txt'

disp_1, load_1 = readData(twoPath1, max_disp=4) 
disp_2, load_2 = readData(twoPath2, max_disp=4) 
disp_3, load_3 = readData(twoPath3, max_disp=4) 

plt.figure(figsize=(6, 6))
plt.plot(disp_1, load_1, label='test 1')
plt.plot(disp_2, load_2, label='test 2')
plt.plot(disp_3, load_3, label='test 3')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.ylim(0, 1)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/layers/6.png", dpi=300)
plt.show()
plt.close()

# 7
twoPath1 = 'hm3/7/test1.txt'
twoPath2 = 'hm3/7/test2.txt'
twoPath3 = 'hm3/7/test3.txt'

disp_1, load_1 = readData(twoPath1, max_disp=4) 
disp_2, load_2 = readData(twoPath2, max_disp=4) 
disp_3, load_3 = readData(twoPath3, max_disp=4) 

plt.figure(figsize=(6, 6))
plt.plot(disp_1, load_1, label='test 1')
plt.plot(disp_2, load_2, label='test 2')
plt.plot(disp_3, load_3, label='test 3')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.ylim(0, 1)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/layers/7.png", dpi=300)
plt.show()
plt.close()