from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter

app = Flask(__name__)
CORS(app)

# Simple in-memory log store
requests_log = []

def predict_category(condition, temperature):
    condition = condition.lower()
    if "sun" in condition or temperature > 30:
        return "travel"
    elif "rain" in condition:
        return "music"
    elif "cloud" in condition:
        return "food"
    elif "snow" in condition:
        return "news"
    else:
        return "default"

@app.route('/')
def home():
    return jsonify({"message": "GeoFlix Backend is running."})

@app.route('/ml-recommend', methods=['POST'])
def ml_recommend():
    data = request.get_json()
    condition = data.get("description", "clear")
    temperature = data.get("temperature", 25)
    city = data.get("city", "Unknown")

    category = predict_category(condition, temperature)

    # Store log
    requests_log.append({
        "condition": condition,
        "temperature": temperature,
        "category": category,
        "city": city
    })

    return jsonify({"category": category})

@app.route('/dashboard')
def dashboard():
    if not requests_log:
        return jsonify({
            "total_requests": 0,
            "common_weather": "N/A",
            "ml_category": "N/A",
            "top_city": "N/A"
        })

    total = len(requests_log)
    common_weather = Counter([r["condition"] for r in requests_log]).most_common(1)[0][0]
    common_category = Counter([r["category"] for r in requests_log]).most_common(1)[0][0]
    top_city = Counter([r["city"] for r in requests_log]).most_common(1)[0][0]

    return jsonify({
        "total_requests": total,
        "common_weather": common_weather,
        "ml_category": common_category,
        "top_city": top_city
    })

if __name__ == '__main__':
    app.run(port=8080, debug=True)
