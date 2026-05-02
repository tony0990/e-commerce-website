request_count = 0
error_count = 0


def increment_requests():
    global request_count
    request_count += 1


def increment_errors():
    global error_count
    error_count += 1


def get_metrics():
    return {
        "requests": request_count,
        "errors": error_count
    }


# -------- API Endpoint --------
from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
def metrics_endpoint():
    return get_metrics()