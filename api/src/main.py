import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src import main_router
from src.config.settings import settings

app = FastAPI()

# This code block is checking if the `BACKEND_CORS_ORIGIN` setting is defined in the `settings`
# module. If it is defined, it adds a CORS (Cross-Origin Resource Sharing) middleware to the FastAPI
# application.
if settings.BACKEND_CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=json.loads(settings.BACKEND_CORS_ORIGIN),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )

# This is just to initialize the translation system
if settings.APP_NAME:
    app.title = settings.APP_NAME

# `app.include_router(main_router)` is including the routes defined in the `main_router` in the
# FastAPI application.
app.include_router(main_router)

add_pagination(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
