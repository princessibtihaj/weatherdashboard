# Princess Ibtihaj
# CS492 
# Prof. Madi
#run.sh
# Run the weather dashboard: create venv, install deps, start server on port 5001.

set -e
cd "$(dirname "$0")"

VENV=".venv"
PORT="${PORT:-5001}"

if [[ ! -d "$VENV" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV"
fi

echo "Activating virtual environment..."
source "$VENV/bin/activate"

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Starting weather dashboard on http://127.0.0.1:$PORT"
python -c "from app import app; app.run(debug=True, port=$PORT)"
