from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from .config import get_settings

api_key_header = APIKeyHeader(name="X-API-Token", auto_error=False)
settings = get_settings()


async def verify_token(token: str = Security(api_key_header)):
    if token != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API token",
        )
