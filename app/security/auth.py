import os
from fastapi import Header, HTTPException, status

API_KEY_ENV = "MODEL_API_KEY"


def require_api_key(x_api_key: str | None = Header(default=None)):
    expected = os.getenv(API_KEY_ENV)
    # Zero Trust: deny by default if not configured
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not configured",
        )
    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

