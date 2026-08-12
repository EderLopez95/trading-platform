from fastapi import FastAPI
import uvicorn
from app.api.routes.auth import router as auth
from app.api.routes.configurations import router as configurations
from app.api.routes.analysis import router as analysis
from app.api.routes.signals import router as signals
from app.core.errors.handlers import register_exception_handlers
from app.config.settings import validate_settings, PORT, ENV, CORS_ORIGINS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
from app.core.logging.middleware import logging_middleware
from app.core.logging.config import setup_logging
from fastapi.middleware.cors import CORSMiddleware

validate_settings()

setup_logging()

app = FastAPI()

app.middleware("http")(logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

app.include_router(auth, prefix="/auth", tags=["Authentication"])

app.include_router(configurations, prefix="/configurations", tags=["Configurations"])

app.include_router(analysis, prefix="/analysis", tags=["Analysis"])

app.include_router(signals, prefix="/signals", tags=["Signals"])

register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=(ENV == "local"),
    )
