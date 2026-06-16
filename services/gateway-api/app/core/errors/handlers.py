from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import AuthenticationException, AuthorizationException, InvalidTokenException

def register_exception_handlers(app):
    @app.exception_handler(AuthenticationException)
    async def auth_exception_handler(request: Request, exc: AuthenticationException):
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AuthorizationException)
    async def authorization_exception_handler(request: Request, exc: AuthorizationException):
        return JSONResponse(
            status_code=403,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidTokenException)
    async def token_exception_handler(request: Request, exc: InvalidTokenException):
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error: " + str(exc)},
        )
