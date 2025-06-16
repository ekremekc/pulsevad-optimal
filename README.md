# pulsevad-optimal
Optimal wire design

# Installation 

## Conda

This library can be installed directly with conda. We can make a conda environment for pulsevad-optimal.

```bash
conda create -n pulsevad python=3.13.0 -y
conda activate pulsevad
conda install pip Jinja2 -y
pip3 install pandas numpy seaborn matplotlib meshio h5py gmsh
conda install -c conda-forge scikit-learn pyomo ipopt glpk -y
# pull the pulsevad code
pip3 install -e .
```

Next, we run the following command in order to activate the environment:

```bash
conda activate pulsevad
```