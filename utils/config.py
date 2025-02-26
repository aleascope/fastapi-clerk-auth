from os import environ as ENV
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TAG: str = ENV.get('APP_TAG')
    CLERK_PK: str = ENV.get('CLERK_PK') # Your Clerk Publishable Key
    CLERK_DOMAIN: str = ENV.get('CLERK_DOMAIN') # Your Clerk Domain e.g. xxx.clerk.accounts.dev
        
    
class FileSettings(Settings):
    class Config:
        env_file = "utils/.env"

if False:
    settings = FileSettings()  # Load variables from .env file
else:
    settings = Settings()  # Use os env variables only
