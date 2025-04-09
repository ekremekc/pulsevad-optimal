import gmsh
import os
import sys
import numpy as np
import pandas as pd
from pulsevad.gmsh_utils import wireGenerator, copyAndRotate
from pulsevad.io_utils import write_xdmf_mesh
mesh_dir = "/geomDir"
mesh_name = "/first_cable"

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

gmsh.model.add("Geom")

path = os.path.dirname(os.path.abspath(__file__))

l_lead = 1E-4 #m
N_power = 3
N_signal = 10

df = pd.read_csv("cable_data.csv")
df = df.set_index("Standard", drop = False)

# Power Cables
powerCable = "30AWG"
d_power = df.loc[powerCable]["Do"] * 1E-3 #m
t_power = df.loc[powerCable]["t"] * 1E-3 #m
r_power = d_power/2 #m
d_copper_power = d_power-t_power
r_copper_power = d_copper_power/2

# Signal Cables
signalCable = "30AWG"
d_signal = df.loc[signalCable]["Do"] * 1E-3 #m
t_signal = df.loc[signalCable]["t"] * 1E-3 #m
r_signal = d_signal/2 #m
d_copper_signal = d_signal-t_signal
r_copper_signal = d_copper_signal/2


# Geometry generation

# # Power domain generation
start_angle = 0
r_power_ring = 2*r_power/np.sqrt(3)
powerCopper, powerJacket = wireGenerator(r_power_ring, 0, 0, 0, 0, l_lead, r_copper_power, r_power)
powerCopperTags = copyAndRotate(powerCopper, start_angle, N_power)
powerJacketTags = copyAndRotate(powerJacket, start_angle, N_power)
gmsh.model.occ.synchronize()

# Signal domain generation
start_angle = 0
r_lead_nojacket = r_power_ring+r_power+2*r_signal
d_lead_nojacket = r_lead_nojacket*2
r_signal_ring = r_lead_nojacket-r_signal
signalCopper, signalJacket = wireGenerator(r_signal_ring, 0, 0, 0, 0, l_lead, r_copper_signal, r_signal)
signalCopperTags = copyAndRotate(signalCopper, start_angle, N_signal)
signalJacketTags = copyAndRotate(signalJacket, start_angle, N_signal)
gmsh.model.occ.synchronize()

# Lead jacket generation
t_lead_jacket =  0.50 * 1E-3 #m
r_lead = r_lead_nojacket+t_lead_jacket/2
d_lead = 2*r_lead
wireJacket = wireGenerator(0,0,0,0,0,l_lead, r_lead_nojacket, r_lead, removeTool=True)
print("Total diameter with jacketing (mm): ", 2*r_lead*1E3)

lc = 1E-4
gmsh.option.setNumber("Mesh.MeshSizeMax", lc)
# gmsh.option.setNumber("Mesh.Algorithm", 6)
# gmsh.option.setNumber("Mesh.Algorithm3D", 10) 
gmsh.option.setNumber("Mesh.Optimize", 1)
gmsh.option.setNumber("Mesh.OptimizeNetgen", 0)
gmsh.model.mesh.generate(3)

gmsh.model.addPhysicalGroup(2, [1], 1) # TODO: build 2D surface tags when necessary
gmsh.model.addPhysicalGroup(3, powerCopperTags, 1)
gmsh.model.addPhysicalGroup(3, powerJacketTags, 2)
gmsh.model.addPhysicalGroup(3, signalCopperTags, 3)
gmsh.model.addPhysicalGroup(3, signalJacketTags, 4)
gmsh.model.addPhysicalGroup(3, [wireJacket[0][1]], 5)

# gmsh.option.setNumber('Mesh.StlOneSolidPerSurface', 1)
gmsh.write("{}.msh".format(path+mesh_dir+mesh_name))
# gmsh.write("{}.stl".format(path+mesh_dir+mesh_name))

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

write_xdmf_mesh(path+mesh_dir+mesh_name, 3)


# calculating bending stiffness
from pulsevad.mechanical_utils import momentOfInertia, momentOfInertiaJacket, area, areaConcentric

E_silicone = 11.285 * 1E6 #Pa
E_copper = 149.254 * 1E6 #Pa
E_latex = 1.129 * 1E6 #Pa

I_copper_signal = momentOfInertia(d_copper_signal)
I_silicone_signal = momentOfInertiaJacket(d_signal, d_copper_signal)
I_copper_power = momentOfInertia(d_copper_power) 
I_silicone_power = momentOfInertiaJacket(d_power, d_copper_power)

EI_total = N_power * E_copper * (I_copper_power + area(d_copper_power)*r_power_ring**2) + \
           N_power * E_silicone * (I_silicone_power + areaConcentric(d_power, d_copper_power)*r_power_ring**2) + \
           N_signal * E_copper * (I_copper_signal + area(d_copper_signal)*r_signal_ring**2) + \
           N_signal * E_silicone * (I_silicone_signal + areaConcentric(d_signal, d_copper_signal)*r_signal_ring**2) + \
           E_silicone * momentOfInertiaJacket(d_lead, d_lead_nojacket)

print("Total bending stiffness (N.m2): ", EI_total)
print("Total bending stiffness (N.mm2): ", EI_total*1E6)

L_span = 30 *1E-3 # support span (m)
delta_sigma = 12 *1E-3 # applied deflection (m)
print("Total bending force (N): ", delta_sigma*48*EI_total/L_span**3)
