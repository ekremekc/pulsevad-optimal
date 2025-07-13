import numpy as np
from importlib import resources
import pandas as pd

# helix parameters
with resources.files('pulsevad.data').joinpath('cable_data.csv').open('r') as f:
    df = pd.read_csv(f)
df = df.set_index("Standard", drop = False)

tol = + 3E-5 # required for successful 3D meshing

# Power Cables
powerCable = "30AWG"
d_power = df.loc[powerCable]["Do"] * 1E-3 #m
t_power = df.loc[powerCable]["t"] * 1E-3 #m
r_power = d_power/2 #m

helix_radius = 2*r_power/np.sqrt(3) +tol
pitch = 0.027         # HM3 has 27mm rise per 2*pi
helix_angle = np.rad2deg(np.arctan(pitch/(2 * np.pi * helix_radius))) # gives 83.47 degrees
helix_angle = 89 # mesh without fail
print(helix_angle)

n_turns = 1         # Total number of turns
# l_lead = pitch*n_turns#*2*np.pi
length = pitch #m


N_power = 3
N_signal = 13


