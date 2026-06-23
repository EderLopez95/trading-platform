import time
import uuid
import logging
from fastapi import Request

logger = logging.getLogger("gateway")

async def logging_middleware(request: Request, call_next):
    # avoid swagger docs logging
    if request.url.path == "/docs":
        return await call_next(request)
    
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()

    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        user_id = getattr(request.state, "user_id", None)
        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "user_id": user_id,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.query_params),
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "client_ip": request.client.host,
            },
        )
        response.headers["X-Request-ID"] = request_id

        return response
    
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        user_id = getattr(request.state, "user_id", None)
        logger.error(
            "request_failed",
            extra={
                "request_id": request_id,
                "user_id": user_id,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.query_params),
                "status_code": 500,
                "duration_ms": round(duration_ms, 2),
                "client_ip": request.client.host,
                "error": str(e),
            },
        )
        raise
