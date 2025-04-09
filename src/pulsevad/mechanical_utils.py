import numpy as np

def momentOfInertia(diameter):
    return np.pi * diameter**4 / 64

def momentOfInertiaJacket(d_out, d_in):
    return momentOfInertia(d_out) - momentOfInertia(d_in)

def flexuralRigidity(E, I):
    return E * I

def flexuralRigidityJacketed(E_o, E_i, d_out, d_in):
    return E_i * momentOfInertia(d_in) + E_o*momentOfInertiaJacket(d_out, d_in)

def area(diameter):
    return np.pi * diameter**2 / 4

def areaConcentric(d_out, d_in):
    return np.pi * (d_out**2 - d_in**2) / 4