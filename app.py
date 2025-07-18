from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

MODEL_PATH = "ml_model.pkl"
LOG_FILE = "prediction_logs.csv"

# Load ML model
try:
    model = joblib.load(MODEL_PATH)
    print("[INFO] ML model loaded successfully.")
except Exception as e:
    print("[ERROR] Failed to load ML model:", e)
    model = None

# Log predictions
def log_prediction(condition, temperature, category):
    log_exists = os.path.exists(LOG_FILE)
    df = pd.DataFrame([{
        "condition": condition,
        "temperature": temperature,
        "predicted_category": category
    }])
    if log_exists:
        df.to_csv(LOG_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)

# ML prediction route
@app.route("/ml-recommend", methods=["POST"])
def ml_recommend():
    data = request.json
    condition = data.get("condition")
    temperature = data.get("temperature")

    if not model:
        return jsonify({"error": "ML model not loaded"}), 500

    try:
        prediction = model.predict([[condition, temperature]])
        category = prediction[0]
        log_prediction(condition, temperature, category)
        return jsonify({"category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Dashboard data route
@app.route("/dashboard")
def dashboard():
    if not os.path.exists(LOG_FILE):
        return jsonify({
            "total_requests": 0,
            "top_city": "N/A",
            "common_weather": "N/A",
            "ml_category": "N/A"
        })

    try:
        df = pd.read_csv(LOG_FILE)

        total_requests = len(df)
        common_weather = df["condition"].mode()[0] if not df.empty else "N/A"
        ml_category = df["predicted_category"].mode()[0] if not df.empty else "N/A"
        top_city = "Not tracked"  # placeholder

        return jsonify({
            "total_requests": total_requests,
            "top_city": top_city,
            "common_weather": common_weather,
            "ml_category": ml_category
        })
    except Exception as e:
        return jsonify({"error": f"Failed to read logs: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
