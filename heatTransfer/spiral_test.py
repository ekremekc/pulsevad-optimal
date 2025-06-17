import gmsh
import math
import sys

gmsh.initialize()
gmsh.model.add("spiral_occ")

# Parameters
radius = 0.25       # Constant radius of helix
pitch = 0.2         # Rise per 2*pi (one full turn)
n_turns = 5         # Total number of turns
n_points = 200      # Number of interpolation points

theta_max = 2 * math.pi * n_turns
dtheta = theta_max / (n_points - 1)

points = []

# Generate 3D helix points with constant radius
for i in range(n_points):
    theta = i * dtheta
    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    z = (pitch / (2 * math.pi)) * theta
    z = pitch * theta  # Spiral rises with angle
    points.append(gmsh.model.occ.addPoint(x, y, z))

# Create the spiral as an OCC spline
helix = gmsh.model.occ.addSpline(points)

helix_wire = gmsh.model.occ.addWire([helix])

# Optional: add a point at the spiral center (not needed for the line)
# gmsh.model.occ.addPoint(0, 0, 0)

gmsh.model.occ.synchronize()

r_signal = 0.1
disk = gmsh.model.occ.addDisk(radius, 0, 0, r_signal, r_signal)
# circle = gmsh.model.occ.addCircle(radius, 0, 0, r_signal)


gmsh.model.occ.synchronize()

print(disk, helix_wire)
print(gmsh.model.getEntities(2))
spiral = gmsh.model.occ.addPipe([(2, disk)], helix_wire, 'DiscreteTrihedron')
gmsh.model.occ.synchronize()

# Optional: generate mesh and export
# gmsh.model.mesh.generate(3)
# gmsh.write("spiral_occ.brep")
gmsh.write("spiral_occ.stl")

# Visualize
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
