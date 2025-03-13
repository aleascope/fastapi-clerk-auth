from os import environ as ENV
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TAG: str = ENV.get('APP_TAG')
    # Settings if you intend to use Clerk OAuth
    CLERK_PK: str = ENV.get('CLERK_PK') # Your Clerk Publishable Key
    CLERK_DOMAIN: str = ENV.get('CLERK_DOMAIN') # Your Clerk Domain e.g. xxx.clerk.accounts.dev
    # Settings if you intend to use GCP OAuth
    GC_PROJECT: str = ENV.get('GC_PROJECT')
    GC_OAUTH_AUDIENCE: str = ENV.get('GC_OAUTH_AUDIENCE')
        
    
class FileSettings(Settings):
    class Config:
        env_file = "utils/.env"

if False:
    settings = FileSettings()  # Load variables from .env file
else:
    settings = Settings()  # Use os env variables only
