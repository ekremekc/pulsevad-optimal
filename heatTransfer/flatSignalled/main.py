from dolfinx import default_scalar_type
from dolfinx.fem import functionspace, Function
from helezon.parameter_utils import Q_volumetric
from helezon.problem import SteadyState
from helezon.boundary_conditions import BoundaryCondition
from helezon.io_utils import xdmf_writer, XDMFReader
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

# Define the boundary conditions
boundary_conditions = [
    BoundaryCondition("Robin", 221, (h1, T_out), V, facet_tags, u),
    # BoundaryCondition("DirichletValue", 221, T_out, V, facet_tags, u),
    # BoundaryCondition("DirichletValue", 15, params.u_edge, V, facet_tags, u),
    # BoundaryCondition("DirichletValue", 17, params.u_edge, V, facet_tags, u),
]

I_power = 0.25
R = 0.33*params.l_lead
N_power = 3
Q_power = Q_volumetric(mesh, subdomains, Q_total=I_power**2*R * N_power, tag=1, degree=0)

I_signal = 500*1E-6
N_signal = 13
Q_signal = Q_volumetric(mesh, subdomains, Q_total=I_signal**2*R * N_signal, tag=3, degree=0)


# from https://onlinelibrary.wiley.com/doi/pdf/10.1155/2018/5475136 
kappa_copper = 400 #W/mK
kappa_insulation = 0.286 #W/mK
kappa_air = 0.0266 #W/mK

Q = functionspace(mesh, ("DG", 0))
kappa = Function(Q)
powerCopperCells = subdomains.find(1)
powerJacketCells = subdomains.find(2)
signalCopperCells = subdomains.find(3)
signalJacketCells = subdomains.find(4)
leadJacketCells = subdomains.find(5)
airCells = subdomains.find(6)

kappa.x.array[powerCopperCells] = np.full_like(powerCopperCells, kappa_copper, dtype=default_scalar_type)
kappa.x.array[powerJacketCells] = np.full_like(powerJacketCells, kappa_insulation, dtype=default_scalar_type)
kappa.x.array[signalCopperCells] = np.full_like(signalCopperCells, kappa_copper, dtype=default_scalar_type)
kappa.x.array[signalJacketCells] = np.full_like(signalJacketCells, kappa_insulation, dtype=default_scalar_type)
kappa.x.array[leadJacketCells] = np.full_like(leadJacketCells, kappa_insulation, dtype=default_scalar_type)
kappa.x.array[airCells] = np.full_like(airCells, kappa_air, dtype=default_scalar_type)
kappa.x.scatter_forward()

xdmf_writer("ResultsDir/kappa", mesh, kappa)

problem = SteadyState(V, subdomains, boundary_conditions, kappa, u, Q_list=[Q_power, Q_signal])
T = problem.solution

xdmf_writer("ResultsDir/T_steady", mesh, T)
