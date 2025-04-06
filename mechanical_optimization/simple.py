import numpy as np

def momentOfInertia(diameter):
    return np.pi * diameter**4 / 64

def momentOfInertiaConcentric(d_out, d_in):
    return momentOfInertia(d_out) - momentOfInertia(d_in)


d_jacketed = 6 #mm
t_jacket = 0.7 #mm
full = momentOfInertia(d_jacketed)
concentric = momentOfInertiaConcentric(d_jacketed, d_jacketed-2*t_jacket)

print(full)
print(concentric)
