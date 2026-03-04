#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
echo "Installing ALPHA_BOT into: $ROOT"

python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install --upgrade pip
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements.txt"

if [ ! -f "$ROOT/.env" ]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  echo ".env created from .env.example — edit it and add your TELEGRAM_TOKEN"
fi

echo "Installation complete. To run the bot:"
echo "source $ROOT/.venv/bin/activate"
echo "python $ROOT/main.py"
