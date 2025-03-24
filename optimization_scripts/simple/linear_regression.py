import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.metrics import mean_squared_error, r2_score
import json 

# Sample Data
# Pellethane HVAD - Carbothane HVAD - HeartMate II - HeartMate 3 - HeartWare
# df = pd.DataFrame({
#     'Diameter': [4.8, 4.8, 6.0, 6.6, 6.0],
#     'Coating': ['Pellethane', 'Carbothane', 'soft_silicone', 'polyurethane', 'polyurethane'],
#     'InfectionRate': [10.1, 9.1, 7.2, 11.9, 10.5]
# })

df = pd.read_csv("data.csv")


# One-Hot Encoding for Categorical Variable
encoder = OneHotEncoder(sparse_output=False)
coating_encoded = encoder.fit_transform(df[['Coating Material']])
coating_columns = encoder.get_feature_names_out(['Coating Material'])

print(coating_encoded)


# Merge Encoded Data
df_encoded = pd.concat([df.drop(columns=['Coating Material']), pd.DataFrame(coating_encoded, columns=coating_columns)], axis=1)

# Define Features and Target Variable
X = df_encoded.drop(columns=['Device','Infection Rate'])
y = df_encoded['Infection Rate']

# Train the Regression Model
model = LinearRegression(fit_intercept=False)
model.fit(X, y)

# Predictions
y_pred = model.predict(X)

# Model Evaluation
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print("Mean Squared Error:", mse)
print("R-Squared Value:", r2)
print("Intercept:", model.intercept_)



# # Visualization of Feature Importance
# plt.figure(figsize=(8, 5))
# sns.barplot(x=X.columns, y=model.coef_)
# plt.title("Feature Importance in Infection Rate Prediction")
# plt.xlabel("Wire Properties")
# plt.ylabel("Coefficient Value")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig("importance.png", dpi=300)


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
plt.savefig("importance2.png", dpi=300)
# plt.show()

# save model coefficients
coeffs = dict(zip(X.columns, model.coef_))
with open('model_coeffs.txt', 'w') as convert_file: 
     convert_file.write(json.dumps(coeffs))
np.savetxt("model_intercept.txt", np.array([model.intercept_]))

# df_predict = pd.DataFrame({
#     'Diameter': [4.8],
#     'Coating_Pellethane': [0],
#     'Coating_polyurethane': [1],
#     'Coating_soft silicone': [0],
# })

# print(model.predict(df_predict))

# corr = df_encoded.corr()
# corr.style.background_gradient(cmap='coolwarm')

# === Step 2: Define the grid (e.g., diameter and stiffness) ===
diameter_range = np.linspace(4.0, 7.0, 50)
stiffness_range = np.linspace(4.0, 16.0, 50)
D, S = np.meshgrid(diameter_range, stiffness_range)

# === Step 3: Predict infection rate over the grid ===
# Fix coating (e.g., choose 'soft silicone')
fixed_coating = np.array([0, 0, 0, 1])  # assuming one-hot encoding: [Pellethane, silicone, soft silicone]

Z = np.zeros_like(D)

for i in range(D.shape[0]):
    for j in range(D.shape[1]):
        diameter = D[i, j]
        stiffness = S[i, j]
        
        # Create the full feature vector for prediction
        features = np.array([diameter, stiffness, *fixed_coating])
        Z[i, j] = model.predict([features])[0]

# === Step 4: Plot the heatmap ===
plt.figure(figsize=(10, 6))
contour = plt.contourf(D, S, Z, levels=30, cmap='viridis')
plt.colorbar(contour, label='Predicted Infection Rate (%)')
plt.xlabel('Diameter (mm)')
plt.ylabel('Bending Stiffness (N/mm)')
plt.title('Predicted Infection Rate Heatmap (Coating: soft silicone)')
plt.tight_layout()
plt.show()