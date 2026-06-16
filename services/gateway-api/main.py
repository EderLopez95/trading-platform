from fastapi import FastAPI
import uvicorn
from app.api.routes.auth import router
from app.core.errors.handlers import register_exception_handlers
from app.config.settings import validate_settings, PORT, ENV, AUTH_SERVICE_HOST

validate_settings()
app = FastAPI()
app.include_router(router, prefix="/auth")
register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=AUTH_SERVICE_HOST,
        port=PORT,
        reload=(ENV == "local"),
    )
