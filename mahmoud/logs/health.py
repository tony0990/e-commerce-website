from fastapi import APIRouter
from app.core.database import engine
from app.core.cache import redis_client

router = APIRouter()


@router.get("/health")
def health_check():
    db_status = "ok"
    redis_status = "ok"

    # check database
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception:
        db_status = "down"

    # check redis
    try:
        redis_client.ping()
    except Exception:
        redis_status = "down"

    return {
        "status": "ok",
        "database": db_status,
        "redis": redis_status
    }