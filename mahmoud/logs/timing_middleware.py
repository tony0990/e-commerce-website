import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("ecommerce")


class TimingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)

        logger.info(
            f"Request took {process_time:.4f}s - {request.method} {request.url.path}"
        )

        return response