from fastapi import APIRouter
from datetime import datetime

from app.monitoring.metrics import get_metrics
from app.core.database import engine
from app.core.cache import redis_client

router = APIRouter()


def get_health_status():
    db_status = "ok"
    redis_status = "ok"

    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception:
        db_status = "down"

    try:
        redis_client.ping()
    except Exception:
        redis_status = "down"

    overall_status = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status
    }


@router.get("/dashboard")
def dashboard_data():
    metrics = get_metrics()
    health = get_health_status()

    return {
        "health": health,
        "metrics": metrics,
        "timestamp": datetime.utcnow().isoformat() 
    }