import gmsh
import numpy as np
import os
import sys
import pandas as pd
from pulsevad.gmsh_utils import copyAndRotate, helixWireGenerator, wireGenerator, helixWireGenerator2
from pulsevad.io_utils import write_xdmf_mesh
from importlib import resources
import params

path = os.path.dirname(os.path.abspath(__file__))
geom_dir = "/geomDir"
mesh_dir = "/MeshDir"
file_name = "/spiral_cable"

gmsh.initialize()
gmsh.model.add("spiral_occ")
gmsh.option.setNumber("General.Terminal", 0)

with resources.files('pulsevad.data').joinpath('cable_data.csv').open('r') as f:
    df = pd.read_csv(f)
df = df.set_index("Standard", drop = False)

# Power Cables
powerCable = "30AWG"
d_power = df.loc[powerCable]["Do"] * 1E-3 #m
t_power = df.loc[powerCable]["t"] * 1E-3 #m
r_power = d_power/2 #m
r_copper_power = r_power-t_power/2
tol = + 3E-5 # required for successful 3D meshing

# helix parameters
r_power_ring = 2*r_power/np.sqrt(3) +tol
l_lead = params.length
helix_angle = params.helix_angle
N_power = params.N_power
start_angle = 0

powerCopperHelix, powerJacketHelix = helixWireGenerator(r_power_ring, helix_angle, l_lead, r_copper_power, r_power)
powerCopperTags = copyAndRotate(powerCopperHelix, start_angle, N_power)
powerJacketTags = copyAndRotate(powerJacketHelix, start_angle, N_power)
gmsh.model.occ.synchronize()
# print(signalTags, powerTags)

t_lead_jacket =  0.5 * 1E-3 #m
r_lead_nojacket = r_power_ring + r_power + tol
r_lead = r_power_ring + r_power + t_lead_jacket

leadCore, leadJacket = wireGenerator(0,0,0,0,0,l_lead, r_lead_nojacket, r_lead, removeTool=False)
gmsh.model.occ.synchronize()

powerCopperCutter = [(3, x) for x in powerCopperTags]
powerJacketCutter = [(3, x) for x in powerJacketTags]
leadGap = gmsh.model.occ.cut(leadCore, powerCopperCutter+powerJacketCutter, removeObject=True, removeTool=False)
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()
gmsh.write(path+geom_dir+file_name+".stl")

lc = 2E-4
gmsh.option.setNumber("Mesh.MeshSizeMax", lc)
gmsh.option.setNumber("Mesh.Algorithm", 6)
gmsh.option.setNumber("Mesh.Algorithm3D", 10) 
gmsh.option.setNumber("Mesh.Optimize", 1)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 10)

print(gmsh.model.getEntities(3))

for surface in gmsh.model.getEntities(dim=2):
    gmsh.model.addPhysicalGroup(2, [surface[1]], tag=surface[1])

gmsh.model.addPhysicalGroup(3, powerCopperTags, 1)
gmsh.model.addPhysicalGroup(3, powerJacketTags, 2)
gmsh.model.addPhysicalGroup(3, [leadJacket[0][1]], 3)
gmsh.model.addPhysicalGroup(3, [leadGap[0][0][1]], 4) # air gap

# for volume in gmsh.model.getEntities(dim=3):
#     gmsh.model.addPhysicalGroup(3, [volume[1]], tag=volume[1])

gmsh.model.mesh.generate(3)
gmsh.write(path+mesh_dir+file_name+".msh")
gmsh.finalize()

write_xdmf_mesh(path+mesh_dir+file_name, 3)
