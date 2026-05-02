import time
from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging every request and response.
    Captures: Method, Path, Status Code, and Processing Time.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Extract request info
        method = request.method
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"
        
        # Log request
        logger.info(f"Incoming Request: {method} {path} | Client: {client_host}")
        
        try:
            response = await call_next(request)
            
            process_time = (time.time() - start_time) * 1000
            status_code = response.status_code
            
            # Log response details
            log_msg = f"Response: {method} {path} | Status: {status_code} | Time: {process_time:.2f}ms"
            
            if status_code >= 500:
                logger.error(log_msg)
            elif status_code >= 400:
                logger.warning(log_msg)
            else:
                logger.info(log_msg)
                
            response.headers["X-Process-Time"] = str(process_time)
            return response
            
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.exception(f"Request Failed: {method} {path} | Error: {str(e)} | Time: {process_time:.2f}ms")
            raise e
