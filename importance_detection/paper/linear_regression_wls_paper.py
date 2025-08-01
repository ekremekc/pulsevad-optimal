import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
import json 

df = pd.read_csv("data.csv")

# Define Features and Target Variable
sample_weights=df["Sample size"]
X = df.drop(columns=['Device','Infection Rate', 'Sample size', 'Coating Material'])
y = df['Infection Rate']

# X_encoded = pd.get_dummies(X, drop_first=True)
# X = sm.add_constant(X)

# model = sm.OLS(y, X_encoded, weights=sample_weights).fit()
model = sm.WLS(y, X, weights=sample_weights).fit()
print(model.summary())

# Prepare coefficient dataframe for plotting
feature_names = X.columns
coef_df = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': model.params
}).reset_index(drop=True)

# Assign colors: highlight primary features, gray out others
color_map = {
    'Diameter': 'tab:red',
    'Bending Stiffness': 'tab:blue'
}

# Plot with manual colors
plt.figure(figsize=(8, 5))
sns.barplot(
    x='Coefficient',
    y='Feature',
    data=coef_df,
    edgecolor='black'
)
plt.axvline(0, linestyle='--', color='gray', linewidth=1)
plt.xlabel('Coefficient', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig("Figure2.pdf", bbox_inches='tight')
# plt.show()
plt.close()