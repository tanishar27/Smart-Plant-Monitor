
import joblib
import pandas as pd

# Load trained ML model
model = joblib.load("model/plant_model.pkl")

# Test sensor readings
test_data = pd.DataFrame({
    "soil_moisture": [20, 45, 80],
    "temperature": [30, 35, 25],
    "humidity": [60, 40, 70]
})

# Predict
predictions = model.predict(test_data)

print("\n🌱 SMART PLANT ML PREDICTIONS")
print("--------------------------------")

for i, prediction in enumerate(predictions):

    if prediction == 1:
        result = "WATERING REQUIRED 💧"
    else:
        result = "NO WATERING REQUIRED 🌿"

    print(
        f"Soil: {test_data.iloc[i]['soil_moisture']}% | "
        f"Temperature: {test_data.iloc[i]['temperature']}°C | "
        f"Humidity: {test_data.iloc[i]['humidity']}% "
        f"=> {result}"
    )
