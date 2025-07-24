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

# One-Hot Encoding for Categorical Variable
encoder = OneHotEncoder(sparse_output=False)
coating_encoded = encoder.fit_transform(df[['Coating Material']])
coating_columns = encoder.get_feature_names_out(['Coating Material'])

# Merge Encoded Data
df_encoded = pd.concat([df.drop(columns=['Coating Material']), pd.DataFrame(coating_encoded, columns=coating_columns)], axis=1)

# Define Features and Target Variable
sample_weights=df["Sample size"]
X = df_encoded.drop(columns=['Device','Infection Rate', 'Sample size'])
y = df_encoded['Infection Rate']

X_encoded = pd.get_dummies(X, drop_first=True)
# X_encoded = sm.add_constant(X_encoded)

# model = sm.OLS(y, X_encoded, weights=sample_weights).fit()
model = sm.WLS(y, X_encoded, weights=sample_weights).fit()
print(model.summary())

# Prepare coefficient dataframe for plotting
feature_names = X_encoded.columns
coef_df = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': model.params
}).reset_index(drop=True)

# Drop intercept
coef_df = coef_df[coef_df['Feature'] != 'const']

# Define primary and secondary features
primary_features = ['Diameter', 'Bending Stiffness']
other_features = [f for f in coef_df['Feature'] if f not in primary_features]
ordered_features = primary_features + sorted(other_features)

# Assign colors: highlight primary features, gray out others
color_map = {
    'Diameter': 'tab:red',
    'Bending Stiffness': 'tab:blue'
}
# Default all to gray, then update with highlights
coef_df['Color'] = coef_df['Feature'].map(lambda f: color_map.get(f, 'lightgray'))

# Plot with manual colors
plt.figure(figsize=(8, 5))
sns.barplot(
    x='Coefficient',
    y='Feature',
    data=coef_df,
    order=ordered_features,
    palette=coef_df.set_index('Feature').loc[ordered_features]['Color'].to_list(),
    edgecolor='black'
)
plt.axvline(0, linestyle='--', color='gray', linewidth=1)
plt.xlabel('Coefficient', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig("impact_mechanical.png", dpi=300, bbox_inches='tight')
# plt.show()
