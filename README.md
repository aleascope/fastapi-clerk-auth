# FastAPI App using Clerk

This repo shows how to integrate Clerk authentication into a FastAPI app.
Routes that need the user to be authenticated are defined in a dedicated **protected.py** router while other routes are defined in the main app.
This demo app also customize the Swagger UI that comes with FastAPP by:
- adding a login/logout button
- activating/deactivating the routes test buttons based on login status

Note that Clerk API keys needs to be provided either as a config file (local dev testing) or as environment variables.
These required variables are listed in config.py.
