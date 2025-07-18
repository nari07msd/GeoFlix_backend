from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import random
from collections import Counter

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# In-memory storage for analytics (temporary)
requests_log = []

# === ML MODEL: simple weather → category rule-based logic ===
def predict_category(weather_desc, temperature):
    desc = weather_desc.lower()
    if "sun" in desc or temperature > 30:
        return "travel"
    elif "rain" in desc:
        return "music"
    elif "cloud" in desc:
        return "food"
    elif "snow" in desc:
        return "news"
    else:
        return "default"

# === ML Endpoint ===
@app.route('/ml-recommend', methods=['POST'])
def ml_recommend():
    data = request.get_json()

    weather_desc = data.get("description", "")
    temperature = data.get("temperature", 0.0)

    category = predict_category(weather_desc, temperature)

    # Store request info for dashboard (optional)
    entry = {
        "weather": weather_desc,
        "temperature": temperature,
        "category": category,
        "city": data.get("city", "Unknown")
    }
    requests_log.append(entry)

    return jsonify({"category": category})

# === Dashboard Endpoint ===
@app.route('/dashboard', methods=['GET'])
def dashboard_data():
    if not requests_log:
        return jsonify({
            "total_requests": 0,
            "common_weather": "N/A",
            "ml_category": "N/A",
            "top_city": "N/A"
        })

    total_requests = len(requests_log)
    weather_list = [r["weather"] for r in requests_log]
    category_list = [r["category"] for r in requests_log]
    city_list = [r.get("city", "Unknown") for r in requests_log]

    most_common_weather = Counter(weather_list).most_common(1)[0][0]
    most_common_category = Counter(category_list).most_common(1)[0][0]
    top_city = Counter(city_list).most_common(1)[0][0]

    return jsonify({
        "total_requests": total_requests,
        "common_weather": most_common_weather,
        "ml_category": most_common_category,
        "top_city": top_city
    })

# === Root route to test server is alive ===
@app.route('/')
def index():
    return "GeoFlix ML Backend is running!"

if __name__ == '__main__':
    app.run(port=8080, debug=True)
