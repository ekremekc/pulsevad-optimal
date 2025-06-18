import gmsh
import numpy as np
import sys
import pandas as pd
from pulsevad.gmsh_utils import copyAndRotate, helixWireGenerator, wireGenerator

gmsh.initialize()
gmsh.model.add("spiral_occ")
gmsh.option.setNumber("General.Antialiasing", 0)

# Power Cables
d_power = 1.7 * 1E-3 #m
t_power = 0.49 * 1E-3 #m
r_power = d_power/2 #m
r_copper_power = r_power-t_power/2

# helix parameters
r_power_ring = 2*r_power/np.sqrt(3)
pitch = 0.005         # Rise per 2*pi (one full turn)
n_turns = 1         # Total number of turns
n_points = 200
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
gmsh.model.occ.synchronize()
gmsh.model.occ.synchronize()
# print(signalTags, powerTags)

t_lead_jacket =  0.50 * 1E-3 #m
r_lead_nojacket = r_power_ring + r_power
r_lead = r_power_ring + r_power + t_lead_jacket

z_offset = 0
l_lead = 2*np.pi*pitch*n_turns-2*z_offset
wireGap, wireJacket = wireGenerator(0,0,z_offset,0,0,l_lead, r_lead_nojacket, r_lead, removeTool=False)
gmsh.model.occ.synchronize()

gap = gmsh.model.occ.cut(wireGap, helixSignal+helixJacket, removeObject=True, removeTool=False)
gmsh.model.occ.synchronize()
print(gap)
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

lc = 2E-4
gmsh.option.setNumber("Mesh.MeshSizeMax", lc)

gmsh.model.mesh.generate(3)
gmsh.write("geomDir/mwe.stl")


gmsh.finalize()
