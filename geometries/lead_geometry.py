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
mesh_name = "/lead"

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

start_angle = 0

r_power = 1.5 * 1E-3 #m
N_power = 3

l_lead = 0.25 #m
r_signal = 1.0 * 1E-3 #m
N_signal = 13


powerWire = gmsh.model.occ.add_cylinder(2*r_power/np.sqrt(3), 0, 0, 0, 0, l_lead, r_power)
gmsh.model.occ.synchronize()
copyAndRotate([(3, powerWire)], start_angle, N_power)
print(gmsh.model.occ.getEntities(3))
gmsh.model.occ.synchronize()


signalWire = gmsh.model.occ.add_cylinder(2*r_power/np.sqrt(3)+r_power+r_signal, 0, 0, 0, 0, l_lead, r_signal)
gmsh.model.occ.synchronize()
copyAndRotate([(3, signalWire)], start_angle, N_signal)
print(gmsh.model.occ.getEntities(3))
gmsh.model.occ.synchronize()

lead_diamater = 2*r_power/np.sqrt(3)+r_power+2*r_signal
print("Total diameter without jacketing (mm): ", lead_diamater*1E3)

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