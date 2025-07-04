import gmsh
import numpy as np
import os
import sys
from pulsevad.gmsh_utils import copyAndRotate, helixWireGenerator, wireGenerator
from pulsevad.io_utils import write_xdmf_mesh

path = os.path.dirname(os.path.abspath(__file__))
mesh_dir = "/geomDir"
mesh_name = "/spiral_cable"

gmsh.initialize()
gmsh.model.add("spiral_occ")

# Power Cables
d_power = 1.7 * 1E-3 #m
t_power = 0.49 * 1E-3 #m
r_power = d_power/2 #m
r_copper_power = r_power-t_power/2

# helix parameters
r_power_ring = 2*r_power/np.sqrt(3) + 1E-5
pitch = 0.005         # Rise per 2*pi (one full turn)
n_turns = 1         # Total number of turns
n_points = 400
theta_max = 2 * np.pi * n_turns
dtheta = theta_max / (n_points - 1)

points = []

# Generate 3D helix points with constant radius
for i in range(n_points):
    theta = i * dtheta
    x = r_power_ring * np.cos(theta)
    y = r_power_ring * np.sin(theta)
    z = (pitch / (2 * np.pi)) * theta
    z = pitch * theta  # Spiral rises with angle
    points.append(gmsh.model.occ.addPoint(x, y, z))

# Create the spiral as an OCC spline
helix = gmsh.model.occ.addSpline(points)
helix_wire = gmsh.model.occ.addWire([helix])
diskSignal = gmsh.model.occ.addDisk(r_power_ring, 0, 0, r_copper_power, r_copper_power)
diskOuter = gmsh.model.occ.addDisk(r_power_ring, 0, 0, r_power, r_power)
diskJacket = gmsh.model.occ.cut([(2, diskOuter)], [(2, diskSignal)], removeTool=False)
gmsh.model.occ.synchronize()

helixSignal = gmsh.model.occ.addPipe([(2, diskSignal)], helix_wire, 'Frenet')
helixJacket = gmsh.model.occ.addPipe([(2, diskJacket[0][0][1])], helix_wire, 'Frenet')
print(helixSignal)
gmsh.model.occ.remove([(2, diskJacket[0][0][1])]+[(2, diskSignal)]+[(1,helix_wire)])
gmsh.model.occ.synchronize()

N = 3
# copyAndRotate([(2,diskSignal)], 0, N)
# copyAndRotate([(2,diskJacket[0][0][1])], 0, N)
# copyAndRotate([(1,helix_wire)], 0, N)

signalTags = copyAndRotate(helixSignal, 0, N)
jacketTags = copyAndRotate(helixJacket, 0, N)
gmsh.model.occ.synchronize()


t_lead_jacket =  0.50 * 1E-3 #m
r_lead_nojacket = r_power_ring + r_power + 1E-5
r_lead = r_power_ring + r_power + t_lead_jacket

l_lead = 2*np.pi*pitch*n_turns
cx, cy, cz, dx, dy, dz = 0,0,0,0,0,l_lead
wireGap = gmsh.model.occ.add_cylinder(cx, cy, cz, dx, dy, dz, r_lead_nojacket)
temp = gmsh.model.occ.add_cylinder(cx, cy, cz, dx, dy, dz, r_lead)
leadJacket = gmsh.model.occ.cut([(3, temp)], [(3, wireGap)], removeTool=False)
gmsh.model.occ.synchronize()
print(leadJacket)
# gap = gmsh.model.occ.cut([(3, wireGap)], helixSignal+helixJacket, removeObject=True, removeTool=False)

signalCutter = [(3, x) for x in signalTags]
powerCutter = [(3, x) for x in jacketTags]
gap = gmsh.model.occ.cut([(3, wireGap)], signalCutter+powerCutter, removeObject=True, removeTool=False)
gmsh.model.occ.synchronize()
print(gap)
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

lc = 2E-4
gmsh.option.setNumber("Mesh.MeshSizeMax", lc)

gmsh.write("geomDir/mwe2_nomesh.stl")

gmsh.model.mesh.generate(3)

print(gmsh.model.getEntities(3))
gmsh.model.addPhysicalGroup(2, [30], 1) # TODO: build 2D surface tags when necessary
gmsh.model.addPhysicalGroup(3, signalTags, 1)
gmsh.model.addPhysicalGroup(3, jacketTags, 2)
# gmsh.model.addPhysicalGroup(3, signalCopperTags, 3)
# gmsh.model.addPhysicalGroup(3, signalJacketTags, 4)
gmsh.model.addPhysicalGroup(3, [leadJacket[0][0][1]], 5)
gmsh.model.addPhysicalGroup(3, [gap[0][0][1]], 6) # air gap


# gmsh.write("geomDir/mwe.brep")
gmsh.write("geomDir/mwe2.stl")
gmsh.write(path+mesh_dir+mesh_name+".msh")


gmsh.finalize()

write_xdmf_mesh(path+mesh_dir+mesh_name, 3)
