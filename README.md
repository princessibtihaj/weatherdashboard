<!--
Princess Ibtihaj
CS492
Prof. Madi
README.md
This README explains how to set up and run the Princess's Perfect Predictor weather app.
-->
# Princess's Perfect Predictor

A one-page weather dashboard built with Flask, 
Bootstrap 5, & the WeatherAPI.com service.

## Requirements

- Python 3.10+
- A free WeatherAPI.com account and API key

## Getting Your WeatherAPI.com API Key

1. Go to `https://www.weatherapi.com/` and sign up for a free account.
2. After verifying your email, go to your account dashboard and locate your API key.
3. Copy the key; you will paste it into the `.env` file created by the run script.

## Setup & Running (recommended)

1. Clone or download this project folder.

2. From a terminal, change into the project directory:

   ```bash
   cd /path/to/weatherdashboard
   ```

3. Run the startup script:

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   What this script does:
   - Creates a `.venv` virtual environment if it does not exist.
   - Activates the virtual environment and installs `requirements.txt`.
   - Creates a `.env` file with a `WEATHERAPI_KEY` placeholder **if it does not exist**, or appends a `WEATHERAPI_KEY` line if it is missing.
   - Starts the Flask app on `http://127.0.0.1:5001` in debug mode.

4. Edit the `.env` file in the project root and replace the placeholder value:

   ```env
   WEATHERAPI_KEY=your_real_weatherapi_key_here
   ```

5. Restart `./run.sh` after updating the key, then open your browser to:

   `http://127.0.0.1:5001`

## Usage

- Type a city name into the search box and click "Get Weather".
- For best results, include the country code:
  - Houston,US
  - London,GB
  - Toronto,CA

## Project Structure

weather-app/
├── app.py
├── views.py
├── requirements.txt
├── run.sh             ← startup script (venv, .env, run server)
├── .env               ← not committed to Git (created/updated by run.sh)
├── static/
│   └── style.css      ← theme
└── templates/
    └── index.html     ← single Jinja2 template (no base layout)