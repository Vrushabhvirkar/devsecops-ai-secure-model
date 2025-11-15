#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

if [ -z "${MODEL_API_KEY:-}" ]; then
  export MODEL_API_KEY=$(python scripts/generate_api_key.py)
  echo "MODEL_API_KEY (save this): $MODEL_API_KEY"
fi

# Expect model/model.joblib to exist, or set MODEL_PATH
uvicorn app.main:app --host 0.0.0.0 --port 8080

