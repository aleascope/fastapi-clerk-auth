# Imports from public packages
from typing import Optional, List, Tuple, Dict, Union
import logging
# FastAPI imports
from fastapi import (
    HTTPException,
    Depends
)
# Imports for OAuth with Clerk
from fastapi_clerk_auth import (
    ClerkConfig,
    ClerkHTTPBearer,
    HTTPAuthorizationCredentials as ClerkAuthCredentials # rename with Clerk prefix to avoid confusion
)

# Imports from this repo
from utils.config import settings


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


clerk_config = ClerkConfig(jwks_url=f"https://{settings.CLERK_DOMAIN}/.well-known/jwks.json")


clerk_auth_guard = ClerkHTTPBearer(
    config=clerk_config,
    auto_error=False # NOTE : important as otherwise raise 403 error instead of returning None
)


async def clerk_auth(credentials: ClerkAuthCredentials | None = Depends(clerk_auth_guard)):
    """Dependency to enforce authentication on protected routes."""
    token = credentials.credentials
    logging.info(f"Received Bearer token: {token}")
    return credentials
