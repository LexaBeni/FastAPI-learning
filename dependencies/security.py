from fastapi import Header, HTTPException
from core.settings import settings

def verify_api_key(api_key = Header(None)):
    if not api_key or api_key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )