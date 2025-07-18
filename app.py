from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from collections import Counter
import os
import csv

app = Flask(__name__)
CORS(app)

# Dummy ML model
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

# Dummy local trends
dummy_trends = {
    "Bangalore": "Kantara 2 Release",
    "Delhi": "India vs Australia",
    "Mumbai": "Bollywood Awards",
    "Chennai": "Tech Conference",
    "Hyderabad": "Tollywood Updates",
}

LOG_FILE = "ml_logs.csv"

@app.route("/")
def home():
    return jsonify({"message": "GeoFlix backend is running!"})

@app.route("/ml-recommend", methods=["POST"])
def recommend():
    try:
        data = request.json
        condition = data.get("condition", "")
        temperature = float(data.get("temperature", 0))

        category = predict_category(condition, temperature)

        log_data = [condition, temperature, category]
        file_exists = os.path.isfile(LOG_FILE)
        with open(LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["condition", "temperature", "category"])
            writer.writerow(log_data)

        return jsonify({"category": category})

    except Exception as e:
        return jsonify({"error": f"ML Recommendation failed: {str(e)}"}), 500

@app.route("/trends")
def trends():
    try:
        city = request.args.get("city", "")
        trend = dummy_trends.get(city, "Global News")
        return jsonify({"trend": trend})
    except Exception as e:
        return jsonify({"error": f"Trends fetch failed: {str(e)}"}), 500

@app.route("/dashboard")
def dashboard():
    try:
        if not os.path.exists(LOG_FILE):
            return jsonify({"message": "No data available yet."})

        df = pd.read_csv(LOG_FILE)

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

    except Exception as e:
        return jsonify({"error": f"Dashboard failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
