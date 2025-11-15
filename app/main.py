from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, conlist
from typing import List, Any
import numpy as np
from fastapi import Request

from app.security.auth import require_api_key
from app.security.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.models.loader import load_model, predict, ModelNotAvailable
from app.security.adversarial import basic_input_screen

app = FastAPI(title="Secure AI Model API", version="0.1.0")

# Rate limiting setup
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
def rl_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too Many Requests"},
    )


from typing import List
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    inputs: List[List[float]] = Field(
        ..., description="2D array-like inputs"
    )
    low: float = 0.0
    high: float = 1.0


class PredictResponse(BaseModel):
    predictions: List[Any]
    suspicious: bool
    reason: str


@app.get("/healthz")
def health():
    return {"ok": True}


@app.post("/predict", response_model=PredictResponse)
@limiter.limit("10/minute")
def predict_api(request: Request, body: PredictRequest, _=Depends(require_api_key)):
    try:
        model = load_model()
    except ModelNotAvailable as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )

    x = np.array(body.inputs, float)
    suspicious, reason = basic_input_screen(x, (body.low, body.high))
    y = predict(model, x)
    return PredictResponse(
        predictions=y,
        suspicious=suspicious,
        reason=reason,
    )

