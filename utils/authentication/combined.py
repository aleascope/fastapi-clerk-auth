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
    HTTPAuthorizationCredentials as ClerkAuthCredentials # rename with Clerk prefix to avoid confusion
)

# Imports from this repo
from workers.authentication.gcp import gcp_auth
from workers.authentication.clerk import clerk_auth_guard


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def combined_auth(
    gcp_result: Optional[Dict[str, str]] = Depends(gcp_auth),
    clerk_credentials: Optional[ClerkAuthCredentials] = Depends(clerk_auth_guard)
):
    """
    Combined authentication that accepts either GCP service or Clerk credentials
    """
    logging.info(f'combined_auth: starting')
    if gcp_result:
        logging.info(f'combined_auth: GCP block')
        return gcp_result
    elif clerk_credentials:
        logging.info(f'combined_auth: Clerk block')
        # The ClerkHTTPBearer dependency already verified the token
        return clerk_credentials
        # WARNING:
        #  this is not ideal as we would like to return eg
        #    return {'user_info': decoded, 'auth_type': 'clerk'}
        #  however as of now we are not making use of the user info
    else:
        raise HTTPException(status_code=401, detail='combined_auth: invalid authentication credentials')

      
