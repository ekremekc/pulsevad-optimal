import gmsh
import os
import sys
import numpy as np
import pandas as pd
from pulsevad.gmsh_utils import wireGenerator, copyAndRotate
from pulsevad.io_utils import write_xdmf_mesh
import params

path = os.path.dirname(os.path.abspath(__file__))
geom_dir = "/geomDir"
mesh_dir = "/MeshDir"
mesh_name = "/flat_cable"

gmsh.initialize()
gmsh.model.add("Geom")
gmsh.option.setNumber("General.Terminal", 0)

df = pd.read_csv(path+"/../data/cable_data.csv")
df = df.set_index("Standard", drop = False)



# Power Cables
powerCable = "22AWG"
d_power = df.loc[powerCable]["Do"] * 1E-3 #m
t_power = df.loc[powerCable]["t"] * 1E-3 #m
r_power = d_power/2 #m
r_copper_power = r_power-t_power/2
tol = + 1E-5 # required for successful 3D meshing

# Power domain generation
r_power_ring = 2*r_power/np.sqrt(3) +tol
pitch = params.pitch         # Rise per 2*pi (one full turn)
n_turns = params.n_turns         # Total number of turns
l_lead = params.l_lead

N_power = params.N_power
start_angle = 0
powerCopper, powerJacket = wireGenerator(r_power_ring, 0, 0, 0, 0, l_lead, r_copper_power, r_power)
powerCopperTags = copyAndRotate(powerCopper, start_angle, N_power)
powerJacketTags = copyAndRotate(powerJacket, start_angle, N_power)
gmsh.model.occ.synchronize()


# Lead jacket generation
t_lead_jacket =  0.50 * 1E-3 #m
r_lead_nojacket = r_power_ring + r_power + tol
r_lead = r_power_ring + r_power + t_lead_jacket
leadCore, leadJacket = wireGenerator(0,0,0,0,0,l_lead, r_lead_nojacket, r_lead, removeTool=False)
print("Total diameter with jacketing (mm): ", 2*r_lead*1E3)
gmsh.model.occ.synchronize()


powerCopperCutter = [(3, x) for x in powerCopperTags]
powerJacketCutter = [(3, x) for x in powerJacketTags]

leadGap = gmsh.model.occ.cut(leadCore, powerCopperCutter+powerJacketCutter, removeObject=True, removeTool=False)
gmsh.model.occ.synchronize()
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

lc = 2E-4
gmsh.option.setNumber("Mesh.MeshSizeMax", lc)
# gmsh.option.setNumber("Mesh.Algorithm", 6)
# gmsh.option.setNumber("Mesh.Algorithm3D", 10) 
gmsh.option.setNumber("Mesh.Optimize", 1)
gmsh.option.setNumber("Mesh.OptimizeNetgen", 0)
gmsh.model.mesh.generate(3)

for surface in gmsh.model.getEntities(dim=2):
    gmsh.model.addPhysicalGroup(2, [surface[1]], tag=surface[1])

gmsh.model.addPhysicalGroup(3, powerCopperTags, 1)
gmsh.model.addPhysicalGroup(3, powerJacketTags, 2)
gmsh.model.addPhysicalGroup(3, [leadJacket[0][1]], 3)
gmsh.model.addPhysicalGroup(3, [leadGap[0][0][1]], 4) # air gap

gmsh.write("{}.stl".format(path+geom_dir+mesh_name))
gmsh.write("{}.msh".format(path+mesh_dir+mesh_name))

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

write_xdmf_mesh(path+mesh_dir+mesh_name, 3)