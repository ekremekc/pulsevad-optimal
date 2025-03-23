# pulsevad-optimal
Optimal wire design

# Installation 

## Conda

This library can be installed directly with conda. We can make a conda environment for pulsevad-optimal.

```bash
conda create -n pulsevad python=3.13.0
conda activate pulsevad
conda install pip Jinja2
pip3 install pandas numpy seaborn matplotlib
conda install -c conda-forge scikit-learn
conda install -c conda-forge pyomo
conda install -c conda-forge ipopt glpk


```

Next, we run the following command in order to activate the environment:

```bash
conda activate pulsevad
```