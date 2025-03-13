# FastAPI app using Clerk authentication

This repo shows how to integrate **Clerk** authentication into a **FastAPI** app using the **fastapi_clerk_auth** package.

**Remark**: This repo also covers **GCP OAuth** to authenticate traffic from **Google Cloud** services (eg a PubSub subscriptions invoking the app deployed on **Cloud Run**). It also covers the case where both authentication methods (Clerk, GCP) are combined.

Routes that need the user to be authenticated are defined in a dedicated **protected.py** router while other routes are defined in the main app.

This demo app also customizes the **Swagger UI** that comes with FastAPI by:
- adding the Clerk official login/logout button
- activating/deactivating the routes *Try it on* buttons based on login status

The Swagger page will look like this:
| <img width="1320" alt="swagger_ui" src="https://github.com/user-attachments/assets/6605df1b-49c6-4351-902e-53c46693a12b"> |
|---|



Note that Clerk API keys needs to be provided either as a config file (local dev testing) or as environment variables (prod setup).
These required variables are listed in **config.py**.
