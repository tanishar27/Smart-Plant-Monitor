
import os
import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Generate demonstration dataset
np.random.seed(42)

number_of_samples = 1000

soil = np.random.randint(5, 101, number_of_samples)
temperature = np.random.randint(15, 41, number_of_samples)
humidity = np.random.randint(20, 91, number_of_samples)

# Demonstration labels based on an illustrative rule
watering_needed = (
    (soil < 40) |
    ((soil < 50) & (temperature > 32))
).astype(int)

# Create dataset
data = pd.DataFrame({
    "soil_moisture": soil,
    "temperature": temperature,
    "humidity": humidity,
    "watering_needed": watering_needed
})

# Save dataset
data.to_csv("plant_data.csv", index=False)

print("Dataset created successfully!")
print(data.head())

# 2. Separate input and output
X = data[[
    "soil_moisture",
    "temperature",
    "humidity"
]]

y = data["watering_needed"]

# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# 5. Evaluate model
predictions = model.predict(X_test)

print("\nModel Evaluation")
print("----------------")
print("Accuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# 6. Save trained model
os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/plant_model.pkl")

print("\nModel saved successfully!")
print("Location: model/plant_model.pkl")
