import gmsh
import numpy as np

def copyAndRotate(wire, startAngle, numberOfWires):
    """
    wire: it needs to be vector pair
    """
    jumpAngle = 2*np.pi/numberOfWires
    angle = startAngle
    physical_tags = [wire[0][1]] 
    for i in range(1, numberOfWires):
        copiedwire = gmsh.model.occ.copy(wire)
        angle += jumpAngle
        physical_tags.append(copiedwire[0][1])

        gmsh.model.occ.rotate(copiedwire, 0, 0, 0, 0, 0, 1, angle)
    return physical_tags

def wireGenerator(cx, cy, cz, dx, dy, dz, r_inner, r_outer, removeTool=False):
    Copper = gmsh.model.occ.add_cylinder(cx, cy, cz, dx, dy, dz, r_inner)
    Wire = gmsh.model.occ.add_cylinder(cx, cy, cz, dx, dy, dz, r_outer)
    Jacket = gmsh.model.occ.cut([(3, Wire)], [(3, Copper)], removeTool=removeTool)
    gmsh.model.occ.synchronize()

    tags = [(3, Copper)], Jacket[0]

    if removeTool:
        tags = Jacket[0]
    return tags

def helixWireGenerator(helix_radius, pitch, n_turns, r_inner, r_outer, removeTool=False, n_points=200):
    
    theta_max = 2 * np.pi * n_turns
    dtheta = theta_max / (n_points - 1)

    points = []

    # Generate 3D helix points with constant radius
    for i in range(n_points):
        theta = i * dtheta
        x = helix_radius * np.cos(theta)
        y = helix_radius * np.sin(theta)
        z = (pitch / (2 * np.pi)) * theta
        z = pitch * theta  # Spiral rises with angle
        points.append(gmsh.model.occ.addPoint(x, y, z))

    # Create the spiral as an OCC spline
    helix = gmsh.model.occ.addSpline(points)
    helix_wire = gmsh.model.occ.addWire([helix])
    diskSignal = gmsh.model.occ.addDisk(helix_radius, 0, 0, r_inner, r_inner)
    diskOuter = gmsh.model.occ.addDisk(helix_radius, 0, 0, r_outer, r_outer)
    diskJacket = gmsh.model.occ.cut([(2, diskOuter)], [(2, diskSignal)], removeTool=removeTool)
    print(diskJacket[0][0][1])
    gmsh.model.occ.synchronize()
    helixSignal = gmsh.model.occ.addPipe([(2, diskSignal)], helix_wire, 'DiscreteTrihedron')
    helixJacket = gmsh.model.occ.addPipe([(2, diskJacket[0][0][1])], helix_wire, 'DiscreteTrihedron')
    print(helixSignal)
    print(helixJacket)
    gmsh.model.occ.synchronize()
    tags = helixSignal, helixJacket

    # if removeTool:
    #     tags = Jacket[0]
    return tags