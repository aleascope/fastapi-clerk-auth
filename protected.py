# Imports from public packages
import logging
from fastapi import APIRouter, Depends

# Imports from this repo
from utils.auth import clerk_auth

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a router and apply authentication globally
protected = APIRouter(
    tags=["Protected API"],
    dependencies=[Depends(clerk_auth)]
)


@protected.post("/private/func")
def func(msg: str):
    """
    Example:
        msg = 'a dummy payload'
    """
    return {"message": msg}
