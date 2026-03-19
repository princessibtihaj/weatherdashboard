from __future__ import annotations

# Princess Ibtihaj
# CS492
# Prof. Madi
# app.py
# This file configures the Flask app and starts the weather server for development.

from dotenv import load_dotenv
from flask import Flask

from views import main_blueprint

# Pull in environment variables from .env so local runs behave like prod-ish
load_dotenv()

app = Flask(__name__)

# All the weather routes live on this blueprint
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    # Debug on for local development
    app.run(debug=True)