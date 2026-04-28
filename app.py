from __future__ import annotations

# Princess Ibtihaj
# CS492
# Prof. Madi
# app.py
# This file configures the Flask app and starts the weather server for development.

import os

from dotenv import load_dotenv
from flask import Flask

from database import db
from views import main_blueprint

# Pull in environment variables from .env so local runs behave like prod-ish
load_dotenv()

app = Flask(__name__)
database_url = (
    os.getenv("JAWSDB_URL")
    or os.getenv("DATABASE_URL")
    or "sqlite:///weatherdashboard.db"
)
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
if database_url.startswith("mysql://"):
    database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# All the weather routes live on this blueprint
app.register_blueprint(main_blueprint)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Debug on for local development
    app.run(debug=True)