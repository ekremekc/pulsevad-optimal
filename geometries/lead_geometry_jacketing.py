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
mesh_name = "/leadJacketed"

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
        print(angle)
        gmsh.model.occ.rotate(copiedwire, 0, 0, 0, 0, 0, 1, angle)
        # gmsh.model.occ.synchronize()


l_lead = 0.025 #m
N_power = 3
N_signal = 13

# Power cables
# 22 AWG
r_power = 1.70/2 * 1E-3 #m
t_power = 0.49 * 1E-3 #m
r_copper_power = r_power-t_power/2

# Signal Cables
# 28 AWG
# r_signal = 1.20 * 1E-3 #m
# t_signal = 0.41 * 1E-3 #m
# r_copper_signal = r_signal-t_signal

# 30 AWG
r_signal = 0.80/2 * 1E-3 #m
t_signal = 0.24 * 1E-3 #m
r_copper_signal = r_signal-t_signal/2



# Geometry generation
start_angle = 0

# Power domain generation
powerCopper = gmsh.model.occ.add_cylinder(2*r_power/np.sqrt(3), 0, 0, 0, 0, l_lead, r_copper_power)
gmsh.model.occ.synchronize()
copyAndRotate([(3, powerCopper)], start_angle, N_power)
print(gmsh.model.occ.getEntities(3))
gmsh.model.occ.synchronize()

powerWire = gmsh.model.occ.add_cylinder(2*r_power/np.sqrt(3), 0, 0, 0, 0, l_lead, r_power)
gmsh.model.occ.synchronize()

powerJacket = gmsh.model.occ.cut([(3, powerWire)], [(3, powerCopper)], removeTool=False)
print(powerJacket[0][0])

copyAndRotate(powerJacket[0], start_angle, N_power)
print(gmsh.model.occ.getEntities(3))
gmsh.model.occ.synchronize()


# Signal domain generation
signalCopper = gmsh.model.occ.add_cylinder(2*r_power/np.sqrt(3)+r_power+r_signal, 0, 0, 0, 0, l_lead, r_copper_signal)
gmsh.model.occ.synchronize()
copyAndRotate([(3, signalCopper)], start_angle, N_signal)
print(gmsh.model.occ.getEntities(3))
gmsh.model.occ.synchronize()

signalWire = gmsh.model.occ.add_cylinder(2*r_power/np.sqrt(3)+r_power+r_signal, 0, 0, 0, 0, l_lead, r_signal)
gmsh.model.occ.synchronize()

signalJacket = gmsh.model.occ.cut([(3, signalWire)], [(3, signalCopper)], removeTool=False)
print(signalJacket[0][0])

copyAndRotate(signalJacket[0], start_angle, N_signal)
print(gmsh.model.occ.getEntities(3))
gmsh.model.occ.synchronize()


# Lead jacket generation
lead_radius_nojacket = 2*r_power/np.sqrt(3)+r_power+2*r_signal
t_lead_jacket =  0.70 * 1E-3 #m
lead_radius = lead_radius_nojacket+t_lead_jacket/2
print("Total diameter with jacketing (mm): ", 2*lead_radius*1E3)

leadCopper = gmsh.model.occ.add_cylinder(0, 0, 0, 0, 0, l_lead, lead_radius_nojacket)
gmsh.model.occ.synchronize()

leadWire = gmsh.model.occ.add_cylinder(0, 0, 0, 0, 0, l_lead, lead_radius)
gmsh.model.occ.synchronize()

leadJacket = gmsh.model.occ.cut([(3, leadWire)], [(3, leadCopper)], removeTool=True)
print(leadJacket[0][0])
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