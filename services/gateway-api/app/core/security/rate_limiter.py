import time
from collections import defaultdict, deque
from fastapi import Request
from app.domain.exceptions import RateLimitExceededException

class RateLimiter:
    # In-memory per-client sliding-window limiter
    # Note: state is per-process. For a multi-instance deployment use a shared store (e.g. Redis) instead

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque] = defaultdict(deque)

    def __call__(self, request: Request):
        key = request.client.host if request.client else "unknown"
        now = time.monotonic()
        hits = self._hits[key]

        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()

        if len(hits) >= self.max_requests:
            
            raise RateLimitExceededException("Too many attempts, please try again later")

        hits.append(now)
