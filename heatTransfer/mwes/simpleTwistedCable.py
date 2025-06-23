import gmsh
import math
import sys

gmsh.initialize()


# Clear all models and create a new one
gmsh.clear()
gmsh.model.add("twist")

# Parameters
r = 0.25
cx, cy, cz = 0.35, 0.0, 0.0
lc = 5e-2  # Mesh size

# Define points
p1 = gmsh.model.geo.addPoint(cx + r, cy, cz, lc)
p2 = gmsh.model.geo.addPoint(cx, cy + r, cz, lc)
p3 = gmsh.model.geo.addPoint(cx - r, cy, cz, lc)
p4 = gmsh.model.geo.addPoint(cx, cy - r, cz, lc)
pc = gmsh.model.geo.addPoint(cx, cy, cz, lc)  # center

# Define arcs
a1 = gmsh.model.geo.addCircleArc(p1, pc, p2)
a2 = gmsh.model.geo.addCircleArc(p2, pc, p3)
a3 = gmsh.model.geo.addCircleArc(p3, pc, p4)
a4 = gmsh.model.geo.addCircleArc(p4, pc, p1)

# Line loop and surface
loop = gmsh.model.geo.addCurveLoop([a1, a2, a3, a4])
surf = gmsh.model.geo.addPlaneSurface([loop])

   
h = 0.1
twisted_angle = 360*math.pi / 180.
ov = gmsh.model.geo.twist([(2, surf)], 0, 0.0, 0.0, 0, 0, -40 * h, 0, 0, 1,
                              twisted_angle, [20], [], False)
    
print(ov)
gmsh.model.geo.synchronize()
from pulsevad.gmsh_utils import copyAndRotate
import numpy as np

wire = [ov[1]]
numberOfWires = 3
startAngle = 0 * np.pi / 180
jumpAngle = 2*np.pi/numberOfWires
angle = startAngle
physical_tags = [wire[0][1]] 
for i in range(1, numberOfWires):
    copiedwire = gmsh.model.geo.copy(wire)
    angle += jumpAngle
    physical_tags.append(copiedwire[0][1])

    gmsh.model.geo.rotate(copiedwire, 0, 0, 0, 0, 0, 1, angle)


gmsh.model.geo.synchronize()


# All the extrusion functions return a vector of extruded entities: the
# "top" of the extruded surface (in `ov[0]'), the newly created volume (in
# `ov[1]') and the tags of the lateral surfaces (in `ov[2]', `ov[3]', ...).

# We can then define a new physical volume (with tag 101) to group all the
# elementary volumes:
# gmsh.model.addPhysicalGroup(3, [ov[1]], 101)

# gmsh.model.mesh.generate(3)
gmsh.write("twisted.stl")

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

# When the GUI is launched, you can use the `Help->Current Options and
# Workspace' menu to see the current values of all options. To save the options
# in a file, use `File->Export->Gmsh Options', or through the api:

# gmsh.write("t3.opt");

gmsh.finalize()
