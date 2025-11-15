import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("ok") is True


def test_predict_no_key():
    payload = {"inputs": [[0.1, 0.2, 0.3]]}
    r = client.post("/predict", json=payload)
    # Either 401 (no key) or 503 (not configured)
    assert r.status_code in (401, 503)


def test_predict_with_key_but_no_model(monkeypatch):
    os.environ["MODEL_API_KEY"] = "testkey"
    os.environ["MODEL_PATH"] = "nonexistent.joblib"
    payload = {"inputs": [[0.1, 0.2, 0.3]]}
    r = client.post(
        "/predict",
        headers={"x-api-key": "testkey"},
        json=payload,
    )
    assert r.status_code == 503

