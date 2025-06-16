# ------------------------------------------------------------------------------
#
#  Gmsh Python tutorial 3
#
#  Extruded meshes, ONELAB parameters, options
#
# ------------------------------------------------------------------------------

import gmsh
import math
import sys

gmsh.initialize()

def createGeometryAndMesh():
    # Clear all models and create a new one
    gmsh.clear()
    gmsh.model.add("t3")

    # Copied from `t1.py'...
    # lc = 1e-2
    # gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
    # gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
    # gmsh.model.geo.addPoint(.1, .3, 0, lc, 3)
    # gmsh.model.geo.addPoint(0, .3, 0, lc, 4)
    # gmsh.model.geo.addLine(1, 2, 1)
    # gmsh.model.geo.addLine(3, 2, 2)
    # gmsh.model.geo.addLine(3, 4, 3)
    # gmsh.model.geo.addLine(4, 1, 4)
    # gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
    # gmsh.model.geo.addPlaneSurface([1], 1)
    # gmsh.model.geo.synchronize()
    # gmsh.model.addPhysicalGroup(1, [1, 2, 4], 5)
    # gmsh.model.addPhysicalGroup(2, [1], name="My surface")

    # signal = gmsh.model.geo.addDisk(1,0,0,.25,.25)
    # print(signal)
    # Parameters
    r = 0.25
    cx, cy, cz = 0.35, 0.0, 0.0
    lc = 1e-1  # Mesh size

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
    # As in `t2.py', we plan to perform an extrusion along the z axis.  But
    # here, instead of only extruding the geometry, we also want to extrude the
    # 2D mesh. This is done with the same `extrude()' function, but by
    # specifying element 'Layers' (2 layers in this case, the first one with 8
    # subdivisions and the second one with 2 subdivisions, both with a height of
    # h/2). The number of elements for each layer and the (end) height of each
    # layer are specified in two vectors:
    h = 0.1
    # ov = gmsh.model.geo.extrude([(2, 1)], 0, 0, h, [8, 2], [0.5, 1])

    # The extrusion can also be performed with a rotation instead of a
    # translation, and the resulting mesh can be recombined into prisms (we use
    # only one layer here, with 7 subdivisions). All rotations are specified by
    # an an axis point (-0.1, 0, 0.1), an axis direction (0, 1, 0), and a
    # rotation angle (-Pi/2):
    # ov = gmsh.model.geo.revolve([(2, 28)], -0.1, 0, 0.1, 0, 1, 0, -math.pi / 2,
                                # [7])

    # Using the built-in geometry kernel, only rotations with angles < Pi are
    # supported. To do a full turn, you will thus need to apply at least 3
    # rotations. The OpenCASCADE geometry kernel does not have this limitation.

    # A translation (-2 * h, 0, 0) and a rotation ((0, 0.15, 0.25), (1, 0, 0),
    # angle * Pi / 180) can also be combined to form a "twist".  The last
    # (optional) argument for the extrude() and twist() functions specifies
    # whether the extruded mesh should be recombined or not. The `angle'
    # parameter is retrieved from the ONELAB database (it can be set
    # interactively in the GUI -- see below):
    # angle = gmsh.onelab.getNumber('Parameters/Twisting angle')[0]
    ov = gmsh.model.geo.twist([(2, surf)], 0, 0.0, 0.0, 0, 0, -40 * h, 0, 0, 1,
                              360*math.pi / 180., [10], [], False)
    
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

    gmsh.model.mesh.generate(3)
    # gmsh.write("t3.msh")

# Let us now change some options... Since all interactive options are accessible
# through the API, we can for example make point tags visible or redefine some
# colors:
gmsh.option.setNumber("Geometry.PointNumbers", 1)
gmsh.option.setColor("Geometry.Color.Points", 255, 165, 0)
gmsh.option.setColor("General.Color.Text", 255, 255, 255)
gmsh.option.setColor("Mesh.Color.Points", 255, 0, 0)

# Note that for conciseness "Color." can be ommitted in color options:
r, g, b, a = gmsh.option.getColor("Geometry.Points")
gmsh.option.setColor("Geometry.Surfaces", r, g, b, a)

# We create a ONELAB parameter to define the angle of the twist. ONELAB
# parameters can be modified interactively in the GUI, and can be exchanged with
# other codes connected to the same ONELAB database. The database can be
# accessed through the Gmsh Python API using JSON-formatted strings (see
# https://gitlab.onelab.info/doc/tutorials/-/wikis/ONELAB-JSON-interface for
# more information):
gmsh.onelab.set("""[
  {
    "type":"number",
    "name":"Parameters/Twisting angle",
    "values":[90],
    "min":0,
    "max":120,
    "step":1
  }
]""")

# Create the geometry and mesh it:
createGeometryAndMesh()

# Launch the GUI and handle the "check" event (recorded in the "ONELAB/Action"
# parameter) to recreate the geometry with a new twisting angle if necessary:
def checkForEvent():
    action = gmsh.onelab.getString("ONELAB/Action")
    if len(action) and action[0] == "check":
        gmsh.onelab.setString("ONELAB/Action", [""])
        createGeometryAndMesh()
        gmsh.graphics.draw()
    return True

if "-nopopup" not in sys.argv:
    gmsh.fltk.initialize()
    while gmsh.fltk.isAvailable() and checkForEvent():
        gmsh.fltk.wait()

# When the GUI is launched, you can use the `Help->Current Options and
# Workspace' menu to see the current values of all options. To save the options
# in a file, use `File->Export->Gmsh Options', or through the api:

# gmsh.write("t3.opt");

gmsh.finalize()
