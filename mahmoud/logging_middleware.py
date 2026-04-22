import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.monitoring.metrics import increment_requests, increment_errors

logger = logging.getLogger("ecommerce")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # count request
        increment_requests()

        method = request.method
        path = request.url.path

        logger.info(f"Incoming request: {method} {path}")

        try:
            response = await call_next(request)
        except Exception as e:
            increment_errors()
            logger.error(f"Error occurred: {str(e)}")
            raise e

        process_time = time.time() - start_time
        status_code = response.status_code

        # لو فيه error status code
        if status_code >= 400:
            increment_errors()

        logger.info(
            f"Completed: {method} {path} - Status: {status_code} - Time: {process_time:.4f}s"
        )

        return response