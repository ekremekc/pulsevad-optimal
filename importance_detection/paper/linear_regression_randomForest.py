import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score

# Load data
df = pd.read_csv("data.csv")

# One-Hot Encoding for 'Coating Material'
encoder = OneHotEncoder(sparse_output=False)
coating_encoded = encoder.fit_transform(df[['Coating Material']])
coating_columns = encoder.get_feature_names_out(['Coating Material'])

# Merge encoded data into dataframe
df_encoded = pd.concat([
    df.drop(columns=['Coating Material']),
    pd.DataFrame(coating_encoded, columns=coating_columns, index=df.index)
], axis=1)

# Define features (X), target (y), and sample weights
X = df_encoded.drop(columns=['Device', 'Infection Rate', 'Sample size'])
y = df_encoded['Infection Rate']
sample_weights = df_encoded['Sample size']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
    X, y, sample_weights, test_size=0.3, random_state=42
)

rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train, sample_weight=w_train)

y_pred_test = rf.predict(X_test)

print("Test R²:", r2_score(y_test, y_pred_test))
print("Test MSE:", mean_squared_error(y_test, y_pred_test))

import matplotlib.pyplot as plt

importances = rf.feature_importances_
feature_names = X.columns

plt.figure(figsize=(6, 4))
sns.barplot(x=importances, y=feature_names)
plt.title("Feature Importance (Random Forest)")
plt.tight_layout()
plt.show()