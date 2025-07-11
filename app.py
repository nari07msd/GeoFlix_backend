from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import joblib
import os

app = Flask(__name__)
CORS(app)

# ==== Mock trend data ====
TREND_DB = {
    "New York": ["Broadway shows", "Street food", "Skyline views"],
    "London": ["Royal sights", "Underground art", "West End"],
    "Tokyo": ["Cherry blossoms", "Anime cafes", "Robot shows"],
    "Bangalore": ["Startup culture", "Tech events", "Cafe hopping"]
}

# ==== Load ML model ====
MODEL_PATH = "ml_model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# ==== Routes ====

@app.route("/trends")
def get_trend():
    city = request.args.get("city", "Unknown")
    trends = TREND_DB.get(city, ["Local culture", "City highlights", "Top restaurants"])
    return jsonify({
        "city": city,
        "trend": random.choice(trends)
    })

@app.route("/ml-recommend", methods=["POST"])
def ml_recommend():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    condition = data.get("condition", "Clear")
    temperature = data.get("temp", 25)

    # Encode weather condition
    condition_map = {"Clear": 0, "Rain": 1, "Clouds": 2, "Snow": 3}
    condition_code = condition_map.get(condition, 0)

    # Predict category
    prediction = model.predict([[condition_code, temperature]])
    return jsonify({"category": prediction[0]})

if __name__ == "__main__":
    app.run()
