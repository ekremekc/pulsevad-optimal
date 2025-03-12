import gmsh
import os
import sys
import numpy as np


def copyAndRotate(geometry, startAngle, N):
    tags = [geometry[0]]
    jumpAngle = 2*np.pi/N
    angle = startAngle
    for i in range(1, N):
        copiedGeometry = gmsh.model.occ.copy(geometry)
        tags.append(copiedGeometry[0])
        angle += jumpAngle
        gmsh.model.occ.rotate(copiedGeometry, 0, 0, 0, 0, 0, 1, angle)
    gmsh.model.occ.synchronize()
    return tags

mesh_dir = "/geomDir"
mesh_name = "/leadJacketedRearranged5mm"

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

gmsh.model.add("Geom")

path = os.path.dirname(os.path.abspath(__file__))

def copyAndRotate(wire, startAngle, numberOfWires):
    """
    wire: it needs to be vector pair
    """
    jumpAngle = 2*np.pi/numberOfWires
    angle = startAngle
    for i in range(1, numberOfWires):
        copiedwire = gmsh.model.occ.copy(wire)
        angle += jumpAngle
        # print(angle)
        gmsh.model.occ.rotate(copiedwire, 0, 0, 0, 0, 0, 1, angle)
        # gmsh.model.occ.synchronize()

def wireGenerator(cx, cy, cz, dx, dy, dz, r_inner, r_outer, removeTool=False):
    Copper = gmsh.model.occ.add_cylinder(cx, cy, cz, dx, dy, dz, r_inner)
    Wire = gmsh.model.occ.add_cylinder(cx, cy, cz, dx, dy, dz, r_outer)
    Jacket = gmsh.model.occ.cut([(3, Wire)], [(3, Copper)], removeTool=removeTool)
    gmsh.model.occ.synchronize()
    return [(3, Copper)], Jacket[0]

l_lead = 0.025 #m
N_power = 3
N_signal = 3

# Power cables
# 22 AWG
# r_power = 1.70/2 * 1E-3 #m
# t_power = 0.49 * 1E-3 #m
# r_copper_power = r_power-t_power/2

# 24 AWG
r_power = 1.60/2 * 1E-3 #m
t_power = 0.51 * 1E-3 #m
r_copper_power = r_power-t_power/2

# Signal Cables
# 28 AWG
# r_signal = 1.20/2 * 1E-3 #m
# t_signal = 0.41 * 1E-3 #m
# r_copper_signal = r_signal-t_signal/2

# 30 AWG
r_signal = 0.80/2 * 1E-3 #m
t_signal = 0.24 * 1E-3 #m
r_copper_signal = r_signal-t_signal/2


# Geometry generation
start_angle = 0

r_lead = 2.5 * 1E-3 #m
t_lead_jacket =  0.70/2 * 1E-3 #m
r_lead_nojacket = r_lead-t_lead_jacket
print("Total diameter with jacketing (mm): ", 2*r_lead*1E3)

# Lead jacket generation
wireJacket = wireGenerator(0,0,0,0,0,l_lead, r_lead_nojacket, r_lead, removeTool=True)

# # Power domain generation
powerCopper, powerJacket = wireGenerator(r_lead_nojacket-r_power, 0, 0, 0, 0, l_lead, r_copper_power, r_power)
copyAndRotate(powerCopper, start_angle, N_power)
copyAndRotate(powerJacket, start_angle, N_power)
gmsh.model.occ.synchronize()

# # Signal domain generation

# outermost layer
signalCopper, signalJacket = wireGenerator(r_lead_nojacket-r_signal, 0, 0, 0, 0, l_lead, r_copper_signal, r_signal)
signalCopper2, signalJacket2 = wireGenerator(r_lead_nojacket-r_signal, 0, 0, 0, 0, l_lead, r_copper_signal, r_signal)

start_angle_signal = np.pi/180*46
gmsh.model.occ.rotate(signalCopper, 0, 0, 0, 0, 0, 1, start_angle_signal)
gmsh.model.occ.rotate(signalJacket, 0, 0, 0, 0, 0, 1, start_angle_signal)
copyAndRotate(signalCopper, start_angle, N_signal)
copyAndRotate(signalJacket, start_angle, N_signal)
gmsh.model.occ.synchronize()

start_angle_signal2 = np.pi/180*74
gmsh.model.occ.rotate(signalCopper2, 0, 0, 0, 0, 0, 1, start_angle_signal2)
gmsh.model.occ.rotate(signalJacket2, 0, 0, 0, 0, 0, 1, start_angle_signal2)
copyAndRotate(signalCopper2, start_angle, N_signal)
copyAndRotate(signalJacket2, start_angle, N_signal)
gmsh.model.occ.synchronize()

# # middle layer
start_angle_signal3 = np.pi/180*60
signalCopper3, signalJacket3 = wireGenerator(r_lead_nojacket-2.9*r_signal, 0, 0, 0, 0, l_lead, r_copper_signal, r_signal)

gmsh.model.occ.rotate(signalCopper3, 0, 0, 0, 0, 0, 1, start_angle_signal3)
gmsh.model.occ.rotate(signalJacket3, 0, 0, 0, 0, 0, 1, start_angle_signal3)
copyAndRotate(signalCopper3, start_angle, N_signal)
copyAndRotate(signalJacket3, start_angle, N_signal)
gmsh.model.occ.synchronize()

# central layer
signalCopper5, signalJacket5 = wireGenerator(0, 0, 0, 0, 0, l_lead, r_copper_signal, r_signal)
gmsh.model.occ.synchronize()



lc = 8E-3
gmsh.option.setNumber("Mesh.MeshSizeMax", lc)
# gmsh.option.setNumber("Mesh.Algorithm", 6)
# gmsh.option.setNumber("Mesh.Algorithm3D", 10) 
gmsh.option.setNumber("Mesh.Optimize", 1)
gmsh.option.setNumber("Mesh.OptimizeNetgen", 0)
# gmsh.model.mesh.generate(3)

# gmsh.model.addPhysicalGroup(2, burner_lateral, burner_lateral_mark)


# gmsh.write("{}.msh".format(path+mesh_dir+mesh_name))
gmsh.write("{}.stl".format(path+mesh_dir+mesh_name))

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()