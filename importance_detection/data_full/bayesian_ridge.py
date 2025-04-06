import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import json 

df = pd.read_csv("data.csv")

# One-Hot Encoding for Categorical Variable
encoder = OneHotEncoder(sparse_output=False)
coating_encoded = encoder.fit_transform(df[['Coating Material']])
coating_columns = encoder.get_feature_names_out(['Coating Material'])

print(coating_encoded)


# Merge Encoded Data
df_encoded = pd.concat([df.drop(columns=['Coating Material']), pd.DataFrame(coating_encoded, columns=coating_columns)], axis=1)

# Define Features and Target Variable
sample_weights=df["Sample size"]
X = df_encoded.drop(columns=['Device','Infection Rate', 'Sample size'])
y = df_encoded['Infection Rate']

# Train the Regression Model
model = BayesianRidge(fit_intercept=False)
model.fit(X, y, sample_weight=sample_weights)

# Predictions
y_pred = model.predict(X)

# Model Evaluation
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print("Mean Squared Error:", mse)
print("R-Squared Value:", r2)
print("Intercept:", model.intercept_)

feature_names = X.columns
coefficients = model.coef_
coef_df = pd.DataFrame({'Feature': feature_names, 'Coefficient': coefficients})

# Step 6: Add baseline coating info
baseline_coating = sorted(df['Coating Material'].unique())[0]
coef_df = pd.concat([
    pd.DataFrame({'Feature': [f'Coating Material_{baseline_coating}'], 'Coefficient': [0.0]}),
    coef_df
], ignore_index=True)

# Step 7: Display results
print("\n=== Linear Regression Coefficients ===")
print(coef_df)

# Step 8: Plot all feature effects
plt.figure(figsize=(8, 5))
sns.barplot(x='Coefficient', y='Feature', data=coef_df, palette='coolwarm')
plt.axvline(0, linestyle='--', color='gray')
plt.title('Effect of Features on Infection Rate')
plt.tight_layout()
# plt.savefig("data_driven_importance.png", dpi=300)
plt.show()

# # save model coefficients
# coeffs = dict(zip(X.columns, model.coef_))
# with open('model_coeffs.txt', 'w') as convert_file: 
#      convert_file.write(json.dumps(coeffs))
# np.savetxt("model_intercept.txt", np.array([model.intercept_]))

# df_predict = pd.DataFrame({
#     'Diameter': [4.8],
#     'Coating_Pellethane': [0],
#     'Coating_polyurethane': [1],
#     'Coating_soft silicone': [0],
# })

# print(model.predict(df_predict))

# corr = df_encoded.corr()
# corr.style.background_gradient(cmap='coolwarm')
