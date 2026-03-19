from __future__ import annotations

# Princess Ibtihaj
# CS492
# Prof. Madi
# views.py
# This file defines the routes and weather-fetching logic for the dashboard.

import os
import requests
from flask import Blueprint, render_template, request

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

    return render_template("index.html", weather=weather, error=error)