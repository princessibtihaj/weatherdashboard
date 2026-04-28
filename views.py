from __future__ import annotations

# Princess Ibtihaj
# CS492
# Prof. Madi
# views.py
# This file defines the routes and weather-fetching logic for the dashboard.

import os
import requests
from flask import Blueprint, jsonify, render_template, request

from database import SearchHistory, db

# Main blueprint for the weather views
main_blueprint = Blueprint("main", __name__)

# WeatherAPI.com forecast endpoint
BASE_URL = "https://api.weatherapi.com/v1/forecast.json"


def get_weather(city: str) -> dict | None:
    """Fetch a short forecast for a single city using WeatherAPI.com."""
    api_key = os.getenv("WEATHERAPI_KEY")  # loaded from .env by load_dotenv()

    city_clean = (city or "").strip()
    if not city_clean or not api_key:
        print(f"ERROR: city='{city_clean}', WEATHERAPI_KEY loaded? {bool(api_key)}")
        return None

    params = {
        "key": api_key,
        "q": city_clean,
        "days": 1,  # today only; includes hourly forecast
        "aqi": "no",
        "alerts": "no",
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")

        if resp.status_code != 200:
            return None

        data = resp.json()

        # WeatherAPI shape:
        # {
        #   "location": {...},
        #   "current": {...},
        #   "forecast": {
        #       "forecastday": [
        #           { "hour": [ {...}, {...}, ... ] }
        #       ]
        #   }
        # }
        location = data["location"]
        current = data["current"]
        hours = data["forecast"]["forecastday"][0]["hour"]

        return {
            "city": location["name"],
            "country": location["country"],
            "temp_f": current["temp_f"],
            "feels_like": current.get("feelslike_f", current["temp_f"]),
            "description": current["condition"]["text"],
            "humidity": current["humidity"],
            "wind_speed": current["wind_mph"],
            "forecast": [
                {
                    "time": hour["time"],
                    "temp_f": hour["temp_f"],
                    "description": hour["condition"]["text"],
                }
                for hour in hours
            ],
        }
    except Exception as e:
        print(f"Exception: {e}")
        return None


def save_search(weather: dict) -> None:
    """Save a weather lookup for simple history tracking."""
    try:
        entry = SearchHistory(
            city=weather.get("city", ""),
            country=weather.get("country"),
            temp_f=weather.get("temp_f"),
            description=weather.get("description"),
        )
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Failed to save search history: {e}")


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    """Home page: simple form + weather card."""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "")
        weather = get_weather(city)
        if weather is None:
            error = f"No weather data for '{city}'. Check spelling or API key."
        else:
            save_search(weather)

    recent_searches = (
        SearchHistory.query.order_by(SearchHistory.created_at.desc()).limit(5).all()
    )
    return render_template(
        "index.html", weather=weather, error=error, recent_searches=recent_searches
    )


@main_blueprint.get("/api/health")
def api_health():
    return jsonify({"status": "ok"})


@main_blueprint.get("/api/weather")
def api_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Missing required query parameter: city"}), 400

    weather = get_weather(city)
    if weather is None:
        return jsonify({"error": "Unable to fetch weather for the requested city"}), 404

    save_search(weather)
    return jsonify(weather), 200


@main_blueprint.get("/api/search-history")
def api_search_history():
    limit_raw = request.args.get("limit", "10").strip()
    try:
        limit = max(1, min(int(limit_raw), 50))
    except ValueError:
        return jsonify({"error": "limit must be an integer"}), 400

    rows = SearchHistory.query.order_by(SearchHistory.created_at.desc()).limit(limit).all()
    data = [
        {
            "id": row.id,
            "city": row.city,
            "country": row.country,
            "temp_f": row.temp_f,
            "description": row.description,
            "created_at": row.created_at.isoformat() + "Z",
        }
        for row in rows
    ]
    return jsonify(data), 200