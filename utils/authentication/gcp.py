# Imports from public packages
from typing import Optional, List, Tuple, Dict, Union
import logging
# FastAPI imports
from fastapi import (
    Request,
    HTTPException,
    Depends
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# Imports for OAuth with Google Cloud
import google.oauth2.id_token
import google.auth.transport.requests

# Imports from this repo
from utils.config import settings


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# Google Cloud based auth for internal services invokation (eg PubSub)
# ----------------------------------------------------------------------------

http_bearer = HTTPBearer(auto_error=False)


async def gcp_auth(
    request: Request,
    gcp_credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> Optional[Dict[str, str]]:
    """
    Authenticate requests from GCP services in the same project
    """
    if not gcp_credentials:
        return None  # Let Clerk auth handle it
    
    logging.info(f'gcp_auth: starting to parse and validate credentials')
    try:
        # Verify Google-issued ID token
        token = gcp_credentials.credentials
        id_info = google.oauth2.id_token.verify_token(
            token,
            google.auth.transport.requests.Request(),
            audience=settings.GC_OAUTH_AUDIENCE,
        )
        
        # Validate service account details
        if id_info.get('iss') not in ['accounts.google.com', 'https://accounts.google.com']:
            logging.info('gcp_auth: invalid issuer')
            raise ValueError('gcp_auth: invalid issuer')
        
        sa_email = id_info.get('email', '')
        if not sa_email.endswith(f'.iam.gserviceaccount.com'):
            logging.info('gcp_auth: invalid service account format')
            raise ValueError('gcp_auth: invalid service account format')
            
        # Ensure service account belongs to your project
        if not sa_email.endswith(f'@{settings.GC_PROJECT}.iam.gserviceaccount.com'):
            logging.info('gcp_auth: service account not in project')
            raise ValueError('gcp_auth: service account not in project')

        logging.info(f'gcp_auth: success with [{sa_email}]')
        
        return {'service_account': sa_email, 'auth_type': 'gcp'}
    
    except Exception as _err:
        logging.warning(f"gcp_auth: GCP authentication failed: {str(_err)}")
        return None
