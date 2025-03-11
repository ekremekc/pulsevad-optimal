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
df = pd.DataFrame({
    'Diameter': [4.8, 4.8, 6.0, 6.6, 6.0],
    'Coating': ['Pellethane', 'Carbothane', 'soft_silicone', 'polyurethane', 'polyurethane'],
    'InfectionRate': [10.1, 9.1, 7.2, 11.9, 10.5]
})

# jacketing and dressing to be added 

# One-Hot Encoding for Categorical Variable
encoder = OneHotEncoder(sparse_output=False)
coating_encoded = encoder.fit_transform(df[['Coating']])
coating_columns = encoder.get_feature_names_out(['Coating'])

print(coating_encoded)


# Merge Encoded Data
df_encoded = pd.concat([df.drop(columns=['Coating']), pd.DataFrame(coating_encoded, columns=coating_columns)], axis=1)

# Define Features and Target Variable
X = df_encoded.drop(columns=['InfectionRate'])
y = df_encoded['InfectionRate']

# Set data
regressor = LinearRegression().fit(X, y)

# Train the Regression Model
model = LinearRegression()
model.fit(X, y)

# Predictions
y_pred = model.predict(X)

# Model Evaluation
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)


# save model coefficients
coeffs = dict(zip(X.columns, model.coef_))
with open('model_coeffs.txt', 'w') as convert_file: 
     convert_file.write(json.dumps(coeffs))

# Print Results
print("Model Coefficients:", coeffs)
print("Intercept:", model.intercept_)
print("Mean Squared Error:", mse)
print("R-Squared Value:", r2)

# Visualization of Feature Importance
plt.figure(figsize=(8, 5))
sns.barplot(x=X.columns, y=model.coef_)
plt.title("Feature Importance in Infection Rate Prediction")
plt.xlabel("Wire Properties")
plt.ylabel("Coefficient Value")
plt.xticks(rotation=45)
plt.savefig("importance.png", dpi=300)

df_predict = pd.DataFrame({
    'Diameter': [4.8],
    'Coating_Pellethane': [0],
    'Coating_polyurethane': [1],
    'Coating_soft silicone': [0],
})

# print(model.predict(df_predict))

corr = df_encoded.corr()
corr.style.background_gradient(cmap='coolwarm')