import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Sample Data (Replace with your actual dataset)
data = pd.DataFrame({
    'Diameter': [0.5, 0.6, 0.7, 0.8, 0.9, 0.55, 0.75, 0.85, 0.65, 0.95],
    'Coating': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A'],
    'Flexibility': [3.2, 2.8, 2.5, 3.0, 2.6, 3.4, 2.7, 3.1, 2.9, 2.4],
    'InfectionRate': [5.4, 4.9, 6.1, 5.8, 4.5, 5.2, 6.0, 5.7, 4.8, 4.3]
})

# One-Hot Encoding for Coating Material
encoder = OneHotEncoder(sparse=False, drop='first')  # Avoids multicollinearity
coating_encoded = encoder.fit_transform(data[['Coating']])
coating_columns = encoder.get_feature_names_out(['Coating'])

# Merge Encoded Data with Original DataFrame
coating_df = pd.DataFrame(coating_encoded, columns=coating_columns)
data = pd.concat([data.drop(columns=['Coating']), coating_df], axis=1)

# Define Features (X) and Target (y)
X = data.drop(columns=['InfectionRate'])  # Independent Variables
y = data['InfectionRate']  # Dependent Variable

# Scale the Features for Neural Network
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split Data into Training and Test Sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build Neural Network Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)  # Output layer (regression problem)
])

# Compile Model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Train Model
history = model.fit(X_train, y_train, epochs=200, batch_size=4, validation_data=(X_test, y_test), verbose=0)

# Evaluate Model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print Results
print("Mean Squared Error:", mse)
print("R-Squared Value:", r2)

# Plot Training Loss
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('Neural Network Training Loss')
plt.show()

# Function to Find Best Wire Design
def optimize_wire():
    diameters = np.linspace(0.5, 1.0, 10)  # Diameter range (0.5mm to 1.0mm)
    flexibilities = np.linspace(2.0, 5.0, 10)  # Flexibility range (2.0 to 5.0)
    coatings = ["A", "B", "C"]

    best_wire = None
    lowest_infection_rate = float('inf')

    for d in diameters:
        for f in flexibilities:
            for c in coatings:
                # Convert Coating to One-Hot Encoding
                coating_encoded = [1 if c == "B" else 0, 1 if c == "C" else 0]  # Encoding for 'B' and 'C'

                # Create feature array and scale it
                features = np.array([[d, f] + coating_encoded])
                features_scaled = scaler.transform(features)

                # Predict infection rate
                predicted_infection = model.predict(features_scaled)[0][0]

                # Check if it's the best wire design
                if predicted_infection < lowest_infection_rate:
                    lowest_infection_rate = predicted_infection
                    best_wire = (d, f, c)

    return best_wire, lowest_infection_rate

# Find the Best Wire Design
optimal_wire, predicted_rate = optimize_wire()

print("\nOptimized Wire Design:")
print(f"Optimal Diameter: {optimal_wire[0]:.2f} mm")
print(f"Optimal Flexibility: {optimal_wire[1]:.2f} N/mm")
print(f"Optimal Coating Material: {optimal_wire[2]}")
print(f"Predicted Minimum Infection Rate: {predicted_rate:.2f} %")
