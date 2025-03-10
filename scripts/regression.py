import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score

# Sample Data (Replace with your actual dataset)
data = pd.DataFrame({
    'Diameter': [0.5, 0.6, 0.7, 0.8, 0.9],
    'Coating': ['A', 'B', 'C', 'A', 'B'],
    'Flexibility': [3.2, 2.8, 2.5, 3.0, 2.6],
    'InfectionRate': [5.4, 4.9, 6.1, 5.8, 4.5]
})

# One-Hot Encoding for Categorical Variable (Coating Material)
encoder = OneHotEncoder(sparse=False, drop='first')  # Avoids dummy variable trap
coating_encoded = encoder.fit_transform(data[['Coating']])
coating_columns = encoder.get_feature_names_out(['Coating'])

# Create a DataFrame with Encoded Variables
coating_df = pd.DataFrame(coating_encoded, columns=coating_columns)

# Merge Encoded Data with Original DataFrame
data = pd.concat([data.drop(columns=['Coating']), coating_df], axis=1)

# Define Features (X) and Target (y)
X = data.drop(columns=['InfectionRate'])  # Independent Variables
y = data['InfectionRate']  # Dependent Variable

# Split Data into Training and Test Sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Model Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print Results
print("Model Coefficients:", dict(zip(X.columns, model.coef_)))
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
plt.show()
