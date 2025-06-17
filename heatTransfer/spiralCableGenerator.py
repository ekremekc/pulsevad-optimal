import gmsh
import numpy as np
import sys
import pandas as pd
from pulsevad.gmsh_utils import copyAndRotate, helixWireGenerator, wireGenerator

gmsh.initialize()
gmsh.model.add("spiral_occ")

df = pd.read_csv("cable_data.csv")
df = df.set_index("Standard", drop = False)

# Power Cables
powerCable = "22AWG"
d_power = df.loc[powerCable]["Do"] * 1E-3 #m
t_power = df.loc[powerCable]["t"] * 1E-3 #m
r_power = d_power/2 #m
r_copper_power = r_power-t_power/2

# helix parameters
r_power_ring = 2*r_power/np.sqrt(3)
pitch = 0.01         # Rise per 2*pi (one full turn)
n_turns = 1         # Total number of turns

signalHelix, powerHelix = helixWireGenerator(r_power_ring, pitch, n_turns, r_copper_power, r_power)
# signalTags = copyAndRotate(signalHelix, 0, 3)
# powerTags = copyAndRotate(powerHelix, 0, 3)
gmsh.model.occ.synchronize()
# print(signalTags, powerTags)

t_lead_jacket =  0.50 * 1E-3 #m
r_lead_nojacket = r_power_ring + r_power
r_lead = r_power_ring + r_power + t_lead_jacket

wireGap, wireJacket = wireGenerator(0,0,0,0,0,2*np.pi*pitch, r_lead_nojacket, r_lead)
gmsh.model.occ.synchronize()

# signalCutter = [(3, x) for x in signalTags]
# powerCutter = [(3, x) for x in powerTags]

# gmsh.model.occ.cut(wireGap, signalCutter+powerCutter, removeObject=True, removeTool=False)
gmsh.model.occ.cut(wireGap, signalHelix+powerHelix, removeObject=True, removeTool=False)
gmsh.model.occ.synchronize()
# gmsh.model.occ.removeAllDuplicates()
# gmsh.model.occ.synchronize()

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

lc = 2E-4
gmsh.option.setNumber("Mesh.MeshSizeMax", lc)
# gmsh.option.setNumber("Mesh.Algorithm", 6)
# gmsh.option.setNumber("Mesh.Algorithm3D", 10) 
gmsh.option.setNumber("Mesh.Optimize", 1)

# Optional: generate mesh and export
gmsh.model.mesh.generate(3)
# gmsh.write("spiral_occ.brep")
gmsh.write("geomDir/spiral_occ.stl")



gmsh.finalize()
