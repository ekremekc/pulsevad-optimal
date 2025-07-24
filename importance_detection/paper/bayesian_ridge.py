import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
import numpy as np

# Load your dataset
df = pd.read_csv("data.csv")

# Features and target
X = df[["Diameter", "Bending Stiffness", "Coating Material"]]
y = df["Infection Rate"]
sample_weights = df["Sample size"]

# Preprocess: scale numeric + one-hot encode categorical
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["Diameter", "Bending Stiffness"]),
    ("cat", OneHotEncoder(drop="first"), ["Coating Material"])
])

from sklearn.linear_model import RidgeCV

ridge_cv_model = make_pipeline(
    preprocessor,
    RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0, 100.0], scoring='neg_mean_squared_error', cv=5)
)
ridge_cv_model.fit(X, y, ridgecv__sample_weight=sample_weights)
print("Best alpha:", ridge_cv_model.named_steps["ridgecv"].alpha_)


# Ridge regression pipeline
model = make_pipeline(preprocessor, Ridge(alpha=ridge_cv_model.named_steps["ridgecv"].alpha_))

# Fit the model with sample weights
model.fit(X, y, ridge__sample_weight=sample_weights)

# Predict
y_pred = model.predict(X)

# Evaluation
rmse = mean_squared_error(y, y_pred, sample_weight=sample_weights)
print(f"Weighted RMSE: {rmse:.3f}")

# Coefficients
ridge_model = model.named_steps["ridge"]
feature_names = model.named_steps["columntransformer"].get_feature_names_out()
coefs = pd.Series(ridge_model.coef_, index=feature_names)

print("\nRidge Regression Coefficients:")
print(coefs)

import matplotlib.pyplot as plt

plt.scatter(y, y_pred, s=sample_weights/10, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], '--r')
plt.xlabel("Actual Infection Rate")
plt.ylabel("Predicted Infection Rate")
plt.title("Predicted vs. Actual")
plt.show()