from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from collections import Counter
import os
import csv

app = Flask(__name__)
CORS(app)

# ML Model: Simple category prediction based on weather
def predict_category(condition, temperature):
    condition = condition.lower()
    if "rain" in condition:
        return "Drama"
    elif "cloud" in condition:
        return "Documentary"
    elif "clear" in condition and temperature > 30:
        return "Action"
    elif "snow" in condition:
        return "Family"
    else:
        return "Comedy"

# Trending topics (dummy data)
dummy_trends = {
    "Bangalore": "Kantara 2 Release",
    "Delhi": "India vs Australia",
    "Mumbai": "Bollywood Awards",
    "Chennai": "Tech Conference",
    "Hyderabad": "Tollywood Updates",
}

@app.route("/")
def home():
    return jsonify({"message": "GeoFlix backend is running!"})

@app.route("/ml-recommend", methods=["POST"])
def recommend():
    data = request.json
    condition = data.get("condition", "")
    temperature = float(data.get("temperature", 0))

    category = predict_category(condition, temperature)

    # Log to CSV
    file_exists = os.path.isfile("ml_logs.csv")
    with open("ml_logs.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["condition", "temperature", "category"])
        writer.writerow([condition, temperature, category])

    return jsonify({"category": category})

@app.route("/trends")
def trends():
    city = request.args.get("city", "")
    trend = dummy_trends.get(city, "Global News")
    return jsonify({"trend": trend})

@app.route("/dashboard")
def dashboard():
    if not os.path.exists("ml_logs.csv"):
        return jsonify({"message": "No data available yet."})

    df = pd.read_csv("ml_logs.csv")
    total_predictions = len(df)
    most_common_category = Counter(df["category"]).most_common(1)[0][0]
    average_temperature = round(df["temperature"].mean(), 2)
    condition_distribution = dict(Counter(df["condition"]))

    return jsonify({
        "total_predictions": total_predictions,
        "most_common_category": most_common_category,
        "average_temperature": average_temperature,
        "condition_distribution": condition_distribution
    })

if __name__ == "__main__":
    app.run(debug=True)
