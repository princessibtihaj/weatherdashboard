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

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather(city: str) -> dict | None:
    """Fetch a short forecast for a single city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")  # read HERE, after load_dotenv() has run

    city_clean = (city or "").strip()
    if not city_clean or not api_key:
        print(f"ERROR: city='{city_clean}', API_KEY loaded? {bool(api_key)}")
        return None

    params = {
        "q": city_clean,
        "appid": api_key,
        "units": "imperial",
        "cnt": 8,
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")

        if resp.status_code != 200:
            return None

        data = resp.json()
        first = data["list"][0]

        return {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "temp_f": first["main"]["temp"],
            "feels_like": first["main"]["feels_like"],
            "description": first["weather"][0]["description"].title(),
            "humidity": first["main"]["humidity"],
            "wind_speed": first["wind"]["speed"],
            "forecast": [
                {
                    "time": item["dt_txt"],
                    "temp_f": item["main"]["temp"],
                    "description": item["weather"][0]["description"].title(),
                }
                for item in data["list"]
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