
import secrets

from fastapi import Header, HTTPException
from backend.config import settings


def require_api_key(
    x_api_key: str | None = Header(default=None)
):
    expected_key = settings.API_KEY

    if not expected_key:
        raise HTTPException(
            status_code=503,
            detail="API authentication is not configured"
        )

    if (
        not x_api_key
        or not secrets.compare_digest(x_api_key, expected_key)
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    return True
