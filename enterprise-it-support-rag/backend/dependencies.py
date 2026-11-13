
import secrets

from fastapi import Header, HTTPException
from backend.config import settings


def require_api_key(
    x_api_key: str | None = Header(default=None)
):
    expected_key = settings.API_KEY

    print("DEBUG: Expected key length:", len(expected_key))
    print("DEBUG: Received key length:", len(x_api_key or ""))
    print("DEBUG: Header received:", bool(x_api_key))

    if not expected_key:
        raise HTTPException(
            status_code=503,
            detail="API authentication is not configured"
        )

    if (
        not x_api_key
        or not secrets.compare_digest(x_api_key, expected_key)
    ):
        print("DEBUG: API KEY DOES NOT MATCH")

        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    print("DEBUG: API KEY MATCHED")

    return True