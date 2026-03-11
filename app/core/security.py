"""
API Key authentication for Habit API.

This module provides a simple API key-based authentication mechanism.
Clients must include the X-API-Key header with requests.
"""

from fastapi import Header, HTTPException, status

from app.core.config import API_KEY


async def verify_api_key(api_key_header: str | None = Header(None, alias="X-API-Key")) -> str:
    """
    Dependency to verify the X-API-Key header.
    
    Args:
        api_key_header: The API key from the X-API-Key header.
        
    Returns:
        The verified API key.
        
    Raises:
        HTTPException 401: If no API key is provided.
        HTTPException 403: If the API key is invalid.
    """
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include X-API-Key header."
        )
    
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key."
        )
    
    return api_key_header
