from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

X = np.array([[0, 0], [1, 1], [0.2, 0.3], [0.9, 0.8]])
y = np.array([0, 1, 0, 1])

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "model/model.joblib")
print("Dummy model saved to model/model.joblib")

