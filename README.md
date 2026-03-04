<!--
Princess Ibtihaj
CS492
Prof. Madi
README.md
This README explains how to set up and run the Princess's Perfect Predictor weather app.
-->
# Princess's Perfect Predictor

A one-page weather dashboard built with Flask, 
Bootstrap 5, and the OpenWeather API.

## Requirements

- Python 3.10+
- A free OpenWeather account and API key

## Getting Your OpenWeather API Key

1. Go to https://openweathermap.org/price

2. Scroll down to the **"Free Weather API access"** section.

3. Under **"Current weather and forecasts"**, click **Subscribe**.

4. You will be taken to the sign-up page:
   https://home.openweathermap.org/users/sign_up
   Create a free account and verify your email.

5. After logging in, go to your API keys dashboard:
   https://home.openweathermap.org/api_keys

6. Copy your API key 
   - Note: New keys can take up to 2 hours to activate.

7. Test your key in a browser before using it:
   https://api.openweathermap.org/data/2.5/forecast?q=Houston,US&appid=YOUR_KEY&units=imperial
   - If you see JSON weather data, your key is working.
   - If you see {"cod":401}, your key is not active yet — wait and retry.

## Setup

1. Clone or download this project folder.

2. Create and activate a virtual environment:

   Mac/Linux:
   python3 -m venv venv
   source venv/bin/activate

   Windows:
   python -m venv venv
   venv\Scripts\activate

   You should see (venv) in your terminal when it is active.

3. Install dependencies:
   pip install -r requirements.txt

4. Create a `.env` file in the root of the project:
   OPENWEATHER_API_KEY=your_api_key_here

5. Run the app:
   python app.py

6. Open your browser and go to:
   http://127.0.0.1:5000

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
├── .env               ← not committed to Git
├── static/
│   └── style.css      ←theme
└── templates/
    ├── base.html
    └── index.html