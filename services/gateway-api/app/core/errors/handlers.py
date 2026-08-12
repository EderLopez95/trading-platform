from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    ValidationException,
    NotFoundException,
    InvalidTokenException,
    ServiceUnavailableException,
    RateLimitExceededException
)

def register_exception_handlers(app):
    @app.exception_handler(AuthenticationException)
    async def auth_exception_handler(request: Request, exc: AuthenticationException):

        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)}
        )

    @app.exception_handler(AuthorizationException)
    async def authorization_exception_handler(request: Request, exc: AuthorizationException):

        return JSONResponse(
            status_code=403,
            content={"detail": str(exc)}
        )

    @app.exception_handler(InvalidTokenException)
    async def token_exception_handler(request: Request, exc: InvalidTokenException):

        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)}
        )
    
    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):

        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )

    @app.exception_handler(ValidationException)
    async def validation_handler(request: Request, exc: ValidationException):

        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
    
    @app.exception_handler(ConflictException)
    async def conflict_handler(request: Request, exc: ConflictException):

        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)}
        )

    @app.exception_handler(RateLimitExceededException)
    async def rate_limit_handler(request: Request, exc: RateLimitExceededException):

        return JSONResponse(
            status_code=429,
            content={"detail": str(exc)}
        )

    @app.exception_handler(ServiceUnavailableException)
    async def service_unavailable_handler(request: Request, exc: ServiceUnavailableException):

        return JSONResponse(
            status_code=503,
            content={"detail": str(exc)}
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error: " + str(exc)}
        )
