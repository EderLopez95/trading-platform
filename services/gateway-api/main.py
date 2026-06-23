from fastapi import FastAPI
import uvicorn
from app.api.routes.auth import router
from app.core.errors.handlers import register_exception_handlers
from app.config.settings import validate_settings, PORT, ENV
from app.core.logging.middleware import logging_middleware
from app.core.logging.config import setup_logging
from fastapi.middleware.cors import CORSMiddleware

validate_settings()
setup_logging()
app = FastAPI()
app.middleware("http")(logging_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3002"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/auth")
register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=(ENV == "local"),
    )
