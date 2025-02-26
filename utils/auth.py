# Imports from public packages
import logging
from fastapi import Request, Query, Depends, Response, status
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials

# Imports from this repo
from config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a router and apply authentication globally

clerk_config = ClerkConfig(jwks_url=f"https://{config.CLERK_DOMAIN}/.well-known/jwks.json")
clerk_auth_guard = ClerkHTTPBearer(config=clerk_config)

async def clerk_auth(credentials: HTTPAuthorizationCredentials | None = Depends(clerk_auth_guard)):
    """Dependency to enforce authentication on protected routes."""
    token = credentials.credentials
    logging.info(f"Received Bearer token: {token}")
    return credentials
