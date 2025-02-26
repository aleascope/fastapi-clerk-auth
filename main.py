# Imports from public packages
import logging
import uvicorn
import jwt
from fastapi import FastAPI, Request, HTTPException, Response
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# see these links on how to improve performance :
#    https://medium.com/@jesum/optimizing-rest-api-performance-2f554d5bfef
#    https://fastapi.tiangolo.com/advanced/middleware/#gzipmiddleware
from fastapi.middleware.gzip import GZipMiddleware

# Imports from this repo
from utils.config import settings
from protected import protected


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


PORT = 8080
    

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Allow all domains (for development purposes or testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains to access the API
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# Custom middleware for handling exceptions globally
@app.middleware("http")
async def add_exception_handling(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except ValueError as exc:
        logging.error(f"ValueError occurred: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"message": f"ValueError: {str(exc)}"}
        )
    except TypeError as exc:
        logging.error(f"TypeError occurred: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"message": f"TypeError: {str(exc)}"}
        )
    except jwt.ExpiredSignatureError as exc:
        logging.error(f"ExpiredSignatureError occurred: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"message": f"ExpiredSignatureError: {str(exc)}"}
        )
    except jwt.InvalidTokenError as exc:
        logging.error(f"InvalidTokenError occurred: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"message": f"InvalidTokenError: {str(exc)}"}
        )
    except Exception as exc:
        logging.error(f"Unexpected error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"}
        )


app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/", include_in_schema=False)
def root():
    try:
        app_tag = settings.APP_TAG
        return {'message': f'Hello from [{app_tag}]'}
    except:
        return {'message': 'Hello'}
    
    
@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi(request: Request):
    openapi_schema = app.openapi()

    headers = {
        "Cache-Control": "public, max-age=3600"  # Cache for 1 hour (3600 seconds)
    }

    return JSONResponse(content=openapi_schema, headers=headers)


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    # Generate the default Swagger UI HTML (you can still use FastAPI's default UI)
    swagger_ui_html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="FastAPI - Swagger UI",
        #swagger_favicon_url="/static/favicon.ico",
    )
    
    swagger_html_body = swagger_ui_html.body.decode("utf-8")  # decode bytes to string
    
    custom_html = """
    <!-- Rest of your HTML file -->
    <link rel="stylesheet" href="static/custom.css">
    <script
      async
      crossorigin="anonymous"
      data-clerk-publishable-key="{{CLERK_PK}}"
      src="https://{{CLERK_DOMAIN}}/npm/@clerk/clerk-js@5/dist/clerk.browser.js"
      type="text/javascript"
    ></script>
    <script src="static/custom.js"></script>
    """
    custom_html = custom_html.replace('{{CLERK_PK}}', settings.CLERK_PK)
    custom_html = custom_html.replace('{{CLERK_DOMAIN}}', settings.CLERK_DOMAIN)
    
    # Combine the default Swagger UI HTML with the custom JavaScript
    content=swagger_html_body + custom_html

    headers = {
        "Cache-Control": "public, max-age=3600"  # Cache for 1 hour
    }

    return HTMLResponse(content=content, headers=headers)

    
app.include_router(protected)
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, timeout_keep_alive=60)
    
