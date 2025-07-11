from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

TREND_DB = {
    "New York": ["Broadway shows", "Street food", "Skyline views"],
    "London": ["Royal sights", "Underground art", "West End"],
    "Tokyo": ["Cherry blossoms", "Anime cafes", "Robot shows"],
    "Bangalore": ["Startup culture", "Tech events", "Cafe hopping"]
}

@app.route("/trends")
def get_trend():
    city = request.args.get("city", "Unknown")
    trends = TREND_DB.get(city, ["Local culture", "City highlights", "Top restaurants"])
    return jsonify({
        "city": city,
        "trend": random.choice(trends)
    })

if __name__ == "__main__":
    app.run()
