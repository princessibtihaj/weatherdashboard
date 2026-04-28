# Princess Ibtihaj
# CS492
# Prof. Madi
# database.py
# This file defines the database models for the weather app.
from __future__ import annotations

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SearchHistory(db.Model):
    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=True)
    temp_f = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
