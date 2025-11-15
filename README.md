# DevSecOps Zero-Trust Starter for Securing a Pre-Trained AI Model

This project wraps any pre-trained model behind a **Zero Trust** FastAPI service,
adds **adversarial input screening**, packages with **Docker**, and wires a CI
pipeline with **Bandit + pytest** (you can extend with Trivy).

## Features

- API key auth (deny-by-default if key not configured)
- Basic rate limiting (`10/min` per IP)
- Input validation (Pydantic) + basic adversarial screening hook
- Non-root Docker image
- GitHub Actions CI: Bandit, pytest
- Pluggable model loader (`app/models/loader.py`)

## Quickstart (local)

```bash
# 1. Put your model at model/model.joblib (joblib-serialized) OR set MODEL_PATH
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Generate an API key
export MODEL_API_KEY=$(python scripts/generate_api_key.py)

# 3. Run the API
uvicorn app.main:app --host 0.0.0.0 --port 8080

# 4. Test a request
curl -s -X POST http://localhost:8080/predict \
  -H "x-api-key: $MODEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"inputs": [[0.1,0.2,0.3],[0.9,0.8,0.1]], "low":0.0, "high":1.0}'

