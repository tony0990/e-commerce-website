from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.deps import get_admin_user
from app.models.user import User
from loguru import logger
import json

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Monitoring"])

@router.get("/metrics")
async def get_metrics(admin: User = Depends(get_admin_user)):
    """
    Monitoring Dashboard Data.
    Requires ADMIN privileges. 
    
    Reads recent logs to calculate basic metrics like error rates and incoming traffic.
    """
    metrics: Dict[str, Any] = {
        "total_requests": 0,
        "error_count": 0,
        "status_distribution": {
            "200_OK": 0,
            "201_CREATED": 0,
            "400_BAD_REQ": 0,
            "401_UNAUTH": 0,
            "404_NOT_FOUND": 0,
            "500_ERROR": 0
        },
        "recent_errors": []
    }
    
    try:
        from app.core.config import settings
        with open(settings.LOG_FILE, "r") as f:
            lines = f.readlines()[-1000:] # read last 1000 logs
            
            for line in lines:
                if "Incoming Request" in line:
                    metrics["total_requests"] += 1
                
                if "Response:" in line and "Status:" in line:
                    status_part = line.split("Status: ")[1].split(" ")[0]
                    if status_part == "200": metrics["status_distribution"]["200_OK"] += 1
                    elif status_part == "201": metrics["status_distribution"]["201_CREATED"] += 1
                    elif status_part == "400": metrics["status_distribution"]["400_BAD_REQ"] += 1
                    elif status_part == "401": metrics["status_distribution"]["401_UNAUTH"] += 1
                    elif status_part == "404": metrics["status_distribution"]["404_NOT_FOUND"] += 1
                    elif status_part.startswith("5"): 
                        metrics["status_distribution"]["500_ERROR"] += 1
                        metrics["error_count"] += 1
                
                if "Request Failed" in line or "| ERROR |" in line:
                    metrics["error_count"] += 1
                    metrics["recent_errors"].append(line.strip())
                    
        # keep only last 5 errors
        metrics["recent_errors"] = metrics["recent_errors"][-5:]
        
    except Exception as e:
        logger.error(f"Failed to read logs for metrics: {e}")
        metrics["log_read_error"] = str(e)
        
    return {"success": True, "data": metrics}
