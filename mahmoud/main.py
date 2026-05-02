from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.timing_middleware import TimingMiddleware
from app.monitoring.health import router as health_router
from app.monitoring.metrics import router as metrics_router
from app.helpers import success_response, error_response
from app.monitoring.dashboard_data import router as dashboard_router

# setup logging
setup_logging()

# create app
app = FastAPI()

# add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(TimingMiddleware)

# include routers
app.include_router(health_router)

#include metrics router
app.include_router(metrics_router)

#include dashboard router
app.include_router(dashboard_router)

@app.get("/")
def home():
    return {"message": "Hello Mahmoud"}