from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True, as_frame=True)
print(X)
# X = X[:, [2,3]]  # Use only one feature
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=20, shuffle=False)

from sklearn.linear_model import LinearRegression

regressor = LinearRegression().fit(X_train, y_train)

from sklearn.metrics import mean_squared_error, r2_score

y_pred = regressor.predict(X_test)

print(f"Mean squared error: {mean_squared_error(y_test, y_pred):.2f}")
print(f"Coefficient of determination: {r2_score(y_test, y_pred):.2f}")

# import matplotlib.pyplot as plt

# fig, ax = plt.subplots(ncols=2, figsize=(10, 5), sharex=True, sharey=True)

# ax[0].scatter(X_train, y_train, label="Train data points")
# ax[0].plot(
#     X_train,
#     regressor.predict(X_train),
#     linewidth=3,
#     color="tab:orange",
#     label="Model predictions",
# )
# ax[0].set(xlabel="Feature", ylabel="Target", title="Train set")
# ax[0].legend()

# ax[1].scatter(X_test, y_test, label="Test data points")
# ax[1].plot(X_test, y_pred, linewidth=3, color="tab:orange", label="Model predictions")
# ax[1].set(xlabel="Feature", ylabel="Target", title="Test set")
# ax[1].legend()

# fig.suptitle("Linear Regression")

# plt.show()


import matplotlib.pyplot as plt
import seaborn as sns

# Visualization of Feature Importance
plt.figure(figsize=(8, 5))
sns.barplot(x=X.columns, y=regressor.coef_)
plt.title("Feature Importance in Infection Rate Prediction")
plt.xlabel("Wire Properties")
plt.ylabel("Coefficient Value")
plt.xticks(rotation=45)
plt.show()