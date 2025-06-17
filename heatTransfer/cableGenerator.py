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
N_signal = 13

df = pd.read_csv("cable_data.csv")
df = df.set_index("Standard", drop = False)

# Power Cables
powerCable = "22AWG"
d_power = df.loc[powerCable]["Do"] * 1E-3 #m
t_power = df.loc[powerCable]["t"] * 1E-3 #m
r_power = d_power/2 #m
r_copper_power = r_power-t_power/2

# Signal Cables
signalCable = "30AWG"
d_signal = df.loc[signalCable]["Do"] * 1E-3 #m
t_signal = df.loc[signalCable]["t"] * 1E-3 #m
r_signal = d_signal/2 #m
r_copper_signal = r_signal-t_signal/2


# Geometry generation
start_angle = 0

# # Power domain generation
r_power_ring = 2*r_power/np.sqrt(3)
powerCopper, powerJacket = wireGenerator(r_power_ring, 0, 0, 0, 0, l_lead, r_copper_power, r_power)
powerCopperTags = copyAndRotate(powerCopper, start_angle, N_power)
powerJacketTags = copyAndRotate(powerJacket, start_angle, N_power)
gmsh.model.occ.synchronize()

# Signal domain generation
r_lead_nojacket = r_power_ring+r_power+2*r_signal
r_signal_ring = r_lead_nojacket-r_signal
signalCopper, signalJacket = wireGenerator(r_signal_ring, 0, 0, 0, 0, l_lead, r_copper_signal, r_signal)
signalCopperTags = copyAndRotate(signalCopper, start_angle, N_signal)
signalJacketTags = copyAndRotate(signalJacket, start_angle, N_signal)
gmsh.model.occ.synchronize()

# Lead jacket generation
t_lead_jacket =  0.50 * 1E-3 #m
r_lead = r_lead_nojacket+t_lead_jacket/2
wireGap, wireJacket = wireGenerator(0,0,0,0,0,l_lead, r_lead_nojacket, r_lead, removeTool=False)
print("Total diameter with jacketing (mm): ", 2*r_lead*1E3)
gmsh.model.occ.synchronize()

coppers = powerCopperTags + signalCopperTags 
jackets = powerJacketTags + signalJacketTags 
signalCutter = [(3, x) for x in coppers]
powerCutter = [(3, x) for x in jackets]

gap = gmsh.model.occ.cut(wireGap, signalCutter+powerCutter, removeObject=True, removeTool=False)
gmsh.model.occ.synchronize()


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
gmsh.model.addPhysicalGroup(3, [x[1] for x in gap[0]], 6) # air gap

gmsh.write("{}.msh".format(path+mesh_dir+mesh_name))
# gmsh.write("{}.stl".format(path+mesh_dir+mesh_name))

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

write_xdmf_mesh(path+mesh_dir+mesh_name, 3)