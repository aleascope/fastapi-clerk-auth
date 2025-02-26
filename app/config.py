from os import environ as ENV
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TAG: str = ENV.get('APP_TAG')
    CLERK_PK: str = ENV.get('CLERK_PK') # Your Clerk Private Key
    CLERK_DOMAIN: str = ENV.get('CLERK_DOMAIN') # Your Clerk Domain e.g. xxx.clerk.accounts.dev
        
    
class FileSettings(Settings):
    class Config:
        env_file = "app/.env"

if False:
    config = FileSettings()  # Load variables from .env file
else:
    config = Settings()  # Use os env variables only
