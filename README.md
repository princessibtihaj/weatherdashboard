<!--
Princess Ibtihaj
CS492
Prof. Madi
README.md
This README explains how to set up and run the Princess's Perfect Predictor weather app.
-->
# Princess's Perfect Predictor

Simple Flask weather dashboard with:

- web UI (`/`)
- REST API backend (`/api/...`)
- database-backed search history
- Heroku-ready deployment config

## Requirements

- Python 3.11
- WeatherAPI key from [weatherapi.com](https://www.weatherapi.com/)

## Local Setup

```bash
cd /path/to/weatherdashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in project root:

```env
WEATHERAPI_KEY=your_real_key
# optional locally (defaults to SQLite):
# DATABASE_URL=sqlite:///weatherdashboard.db
# SECRET_KEY=change_me
```

Run:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## REST API Endpoints

- `GET /api/health` -> simple health check
- `GET /api/weather?city=Boston` -> current weather + hourly forecast JSON
- `GET /api/search-history?limit=10` -> recent DB search history JSON

## Database

- Cloud first: `JAWSDB_URL` (JawsDB MySQL on Heroku)
- Next fallback: `DATABASE_URL`
- Local fallback: SQLite (`sqlite:///weatherdashboard.db`)
- Note: `mysql://...` is converted to `mysql+pymysql://...` for SQLAlchemy compatibility

## Heroku Deployment

This app uses:

- `Procfile`: `web: gunicorn app:app`
- Python runtime from `.python-version` (`3.11`)
- `JAWSDB_URL` for cloud DB when present

Run:

```bash
git remote add heroku https://git.heroku.com/princessweather.git 2>/dev/null || true
git push heroku main
heroku ps:restart --app princessweather
heroku ps:scale web=1 --app princessweather
heroku logs --tail --app princessweather
```

Test after deploy:

```bash
heroku open --app princessweather
curl "https://princessweather.herokuapp.com/api/health"
curl "https://princessweather.herokuapp.com/api/weather?city=Boston"
curl "https://princessweather.herokuapp.com/api/search-history?limit=5"
```