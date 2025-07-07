from dolfinx.fem import functionspace
from helezon.parameter_utils import Q_volumetric
from helezon.problem import SteadyState
from helezon.boundary_conditions import BoundaryCondition
from helezon.io_utils import xdmf_writer, XDMFReader
from ufl import TrialFunction

geometry = XDMFReader("MeshDir/flat_cable")
geometry.getInfo()

mesh, subdomains, facet_tags = geometry.getAll()

degree = 1

V = functionspace(mesh, ("Lagrange", degree))
u = TrialFunction(V)

h1 = 1
T_out = 36.5

# Define the boundary conditions
boundary_conditions = [
    # BoundaryCondition("Robin", 114, (h1, T_out), V, facet_tags, u),
    BoundaryCondition("DirichletValue", 114, T_out, V, facet_tags, u),
    # BoundaryCondition("DirichletValue", 15, params.u_edge, V, facet_tags, u),
    # BoundaryCondition("DirichletValue", 17, params.u_edge, V, facet_tags, u),
]

Q_power = 1
Q = Q_volumetric(mesh, subdomains, Q_total=Q_power, tag=1, degree=0)

kappa = 5
problem = SteadyState(V, subdomains, boundary_conditions, kappa, u, Q)
T = problem.solution

xdmf_writer("ResultsDir/T_steady", mesh, T)
