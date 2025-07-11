# train_model.py

from sklearn.tree import DecisionTreeClassifier
import joblib

# Sample training data: [condition_code, temperature]
X = [
    [0, 30],  # Clear, hot → outdoors
    [1, 20],  # Rainy, mild → indoors
    [2, 25],  # Cloudy, warm → relax
    [3, 0]    # Snow, cold → indoors
]
y = ["outdoors", "indoors", "relax", "indoors"]

model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "ml_model.pkl")
