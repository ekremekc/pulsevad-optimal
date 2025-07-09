from dolfinx import default_scalar_type
from dolfinx.fem import functionspace, Function
from helezon.parameter_utils import Q_volumetric
from helezon.problem import SteadyState
from helezon.boundary_conditions import BoundaryCondition
from helezon.io_utils import xdmf_writer, XDMFReader
from helezon.dolfinx_utils import getFunctionAverage, getFunctionMaximum
from ufl import TrialFunction
import numpy as np
import params
import os

path = os.path.dirname(os.path.abspath(__file__))

geometry = XDMFReader(path+"/MeshDir/flat_cable")
geometry.getInfo()

mesh, subdomains, facet_tags = geometry.getAll()

degree = 1

V = functionspace(mesh, ("Lagrange", degree))
u = TrialFunction(V)

h1 = 500
T_out = 36.5
outerSurfaceTag = 24
# Define the boundary conditions
boundary_conditions = [
    BoundaryCondition("Robin", outerSurfaceTag, (h1, T_out), V, facet_tags, u),
    # BoundaryCondition("DirichletValue", outerSurfaceTag, T_out, V, facet_tags, u),
    # BoundaryCondition("DirichletValue", 15, params.u_edge, V, facet_tags, u),
    # BoundaryCondition("DirichletValue", 17, params.u_edge, V, facet_tags, u),
]

I_power = 1#0.25
R = 0.33*params.l_lead
N_power = 3
Q_power = Q_volumetric(mesh, subdomains, Q_total=I_power**2*R * N_power, tag=1, degree=0)

# from https://onlinelibrary.wiley.com/doi/pdf/10.1155/2018/5475136 
kappa_copper = 400 #W/mK
kappa_insulation = 0.286 #W/mK
kappa_air = 0.0266 #W/mK

Q = functionspace(mesh, ("DG", 0))
kappa = Function(Q)
powerCopperCells = subdomains.find(1)
powerJacketCells = subdomains.find(2)
leadJacketCells = subdomains.find(3)
airCells = subdomains.find(4)

kappa.x.array[powerCopperCells] = np.full_like(powerCopperCells, kappa_copper, dtype=default_scalar_type)
kappa.x.array[powerJacketCells] = np.full_like(powerJacketCells, kappa_insulation, dtype=default_scalar_type)
kappa.x.array[leadJacketCells] = np.full_like(leadJacketCells, kappa_insulation, dtype=default_scalar_type)
kappa.x.array[airCells] = np.full_like(airCells, kappa_air, dtype=default_scalar_type)
kappa.x.scatter_forward()

xdmf_writer("ResultsDir/kappa", mesh, kappa)

problem = SteadyState(V, subdomains, boundary_conditions, kappa, u, Q_list=[Q_power])
T = problem.solution

T_avg_surface = getFunctionAverage(mesh, facet_tags, outerSurfaceTag, T, 'facet')
print("Average temperature on the surface: ", T_avg_surface)
T_max_surface = getFunctionMaximum(V, T, entity="facet", facet_tags=facet_tags, entityTag=outerSurfaceTag)
print("Maximum temperature on the surface: ", T_max_surface)
T_max_body = getFunctionMaximum(V, T)
print("Maximum temperature on the whole body: ", T_max_body)

xdmf_writer("ResultsDir/T_steady", mesh, T)
