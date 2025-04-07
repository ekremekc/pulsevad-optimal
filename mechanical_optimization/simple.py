from pulsevad.mechanical_utils import flexuralRigidityJacketed, momentOfInertiaJacket, momentOfInertia

# Lead jacket dimensions

r_lead = 6.0/2 * 1E-3 #m
d_lead = 2*r_lead
t_jacket = 0.7 * 1E-3 #m

# Cable properties
E_silicone = 100 *1E9 # Pa
E_copper = 117 *1E9 # Pa

# 30 AWG
r_signal = 0.80/2 * 1E-3 #m
t_signal = 0.24 * 1E-3 #m
r_copper_signal = r_signal-t_signal/2

N_signal = 7

# 22 AWG
r_power = 1.70/2 * 1E-3 #m
t_power = 0.49 * 1E-3 #m
r_copper_power = r_power-t_power/2

N_power = 3

# Material for axial load

d_axial = 0.5 * 1E-3 # m 
E_axial = 200 * 1E9 # Pa

flexuralRigidity = N_signal * flexuralRigidityJacketed(E_silicone, E_copper, 2*r_signal, 2*r_copper_signal) + \
                   N_power  * flexuralRigidityJacketed(E_silicone, E_copper, 2*r_power, 2*r_copper_power)   + \
                   E_silicone*momentOfInertiaJacket(2*r_lead, d_lead-2*t_jacket) + \
                   E_axial * momentOfInertia(d_axial)

print("Flexural rigidity (N.m^2): ", flexuralRigidity)