#!/usr/bin/env bash
# Run the weather dashboard: create venv, install deps, start server on port 5001.

set -e
cd "$(dirname "$0")"

VENV=".venv"
PORT="${PORT:-5001}"
ENV_FILE=".env"

if [[ ! -d "$VENV" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV"
fi

echo "Activating virtual environment..."
source "$VENV/bin/activate"

echo "Installing dependencies..."
pip install -q -r requirements.txt

# Ensure .env has a WEATHERAPI_KEY entry so the app can start.
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Creating .env with placeholder WEATHERAPI_KEY..."
  cat > "$ENV_FILE" <<EOF
# Environment configuration for the weather dashboard
# Replace the placeholder value below with your real WeatherAPI.com key.
WEATHERAPI_KEY=your_weatherapi_key_here
EOF
elif ! grep -q '^WEATHERAPI_KEY=' "$ENV_FILE"; then
  echo "Adding WEATHERAPI_KEY placeholder to existing .env..."
  {
    echo ""
    echo "# WeatherAPI.com key (add your real key below)"
    echo "WEATHERAPI_KEY=your_weatherapi_key_here"
  } >> "$ENV_FILE"
fi

echo "Starting weather dashboard on http://127.0.0.1:$PORT"
python -c "from app import app; app.run(debug=True, port=$PORT)"
