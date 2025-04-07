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