"""
This module handles API key authentication for FastAPI.
"""

import os  # standard import

from fastapi import HTTPException, Security, status  # third-party imports
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "x-api-key"

# API Key header definition
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validate the provided API key from the request header.
    
    Args:
        api_key_header (str): The API key passed in the request header.
    
    Returns:
        str: The validated API key.
    
    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "status": False,
            "status_code": status.HTTP_403_FORBIDDEN,
            "message": "Unauthorized",
        },
    )
