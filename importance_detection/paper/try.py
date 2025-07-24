import pandas as pd
import statsmodels.api as sm
from patsy import dmatrices

# Load into DataFrame
df = pd.read_csv("data.csv")

# Construct regression formula (categorical variable for coating material)
formula = 'Q("Infection Rate") ~ Diameter + Q("Bending Stiffness") + C(Q("Coating Material"))'

# Design matrices
y, X = dmatrices(formula, data=df, return_type='dataframe')

# Fit weighted least squares model
weights = df["Sample size"]
model = sm.WLS(y, X, weights=weights).fit()

# Show results
print(model.summary())
