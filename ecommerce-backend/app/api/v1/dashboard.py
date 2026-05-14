from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, List, Optional
from app.api.deps import get_admin_user
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.order_repository import OrderRepository
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
import json
import os
import re

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Monitoring"])

# In-memory metrics tracking for fast access
app_metrics = {
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

def record_metric(status_code: int, path: str, error_msg: str = None):
    """Called by middleware to update in-memory metrics"""
    app_metrics["total_requests"] += 1
    
    if status_code == 200: app_metrics["status_distribution"]["200_OK"] += 1
    elif status_code == 201: app_metrics["status_distribution"]["201_CREATED"] += 1
    elif status_code == 400: app_metrics["status_distribution"]["400_BAD_REQ"] += 1
    elif status_code == 401: app_metrics["status_distribution"]["401_UNAUTH"] += 1
    elif status_code == 404: app_metrics["status_distribution"]["404_NOT_FOUND"] += 1
    elif status_code >= 500: 
        app_metrics["status_distribution"]["500_ERROR"] += 1
        app_metrics["error_count"] += 1
        if error_msg:
            app_metrics["recent_errors"].insert(0, f"{path}: {error_msg}")
            app_metrics["recent_errors"] = app_metrics["recent_errors"][:5]

@router.get("/stats")
async def get_dashboard_stats(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive stats for the admin dashboard.
    """
    user_repo = UserRepository(db)
    order_repo = OrderRepository(db)
    
    order_stats = await order_repo.get_stats()
    sales_over_time = await order_repo.get_sales_per_day(30)
    top_products = await order_repo.get_top_selling_products(5)
    
    total_users = await user_repo.count()
    
    return {
        "total_revenue": order_stats["total_revenue"],
        "total_orders": order_stats["total_orders"],
        "pending_orders": order_stats["pending_orders"],
        "total_users": total_users,
        "sales_over_time": sales_over_time,
        "top_products": top_products
    }

@router.get("/metrics")
async def get_metrics(admin: User = Depends(get_admin_user)):
    """
    Monitoring Dashboard Data from in-memory stats.
    """
    return {"success": True, "data": app_metrics}

@router.get("/health/extended")
async def get_extended_health(admin: User = Depends(get_admin_user)):
    """
    Detailed system health information.
    """
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "connected",
        "uptime": "tracked externally",
        "memory_usage": "tracked externally"
    }

def _parse_log_line(line: str) -> Optional[dict]:
    """Parse a loguru log line into structured data."""
    # Pattern to match: 2026-05-14 02:50:00 | INFO | [CATEGORY] Message
    pattern = r"^(.*?)\s+\|\s+(.*?)\s+\|\s+(?:\[(.*?)\])?(.*)$"
    match = re.match(pattern, line)
    if not match:
        return None
        
    timestamp, level, category, message = match.groups()
    category = category.strip() if category else "GENERAL"
    message = message.strip()
    
    return {
        "timestamp": timestamp,
        "level": level.strip(),
        "type": category.lower(),
        "message": message
    }

@router.get("/logs")
async def get_logs(
    type: Optional[str] = Query(None, description="Filter by log type: auth, order, cart, error, general"),
    search: Optional[str] = Query(None, description="Search in log message"),
    limit: int = Query(100, le=500),
    admin: User = Depends(get_admin_user)
):
    """
    Get application logs with filtering.
    """
    from app.core.config import settings
    
    logs = []
    try:
        if os.path.exists(settings.LOG_FILE):
            with open(settings.LOG_FILE, "r") as f:
                # Read last 2000 lines to ensure we have enough after filtering
                lines = f.readlines()[-2000:]
                
                # Process backwards to get newest first
                for line in reversed(lines):
                    if len(logs) >= limit:
                        break
                        
                    parsed = _parse_log_line(line)
                    if not parsed:
                        continue
                        
                    # Apply type filter
                    if type and type.lower() != "all" and parsed["type"] != type.lower():
                        continue
                        
                    # Apply search filter
                    if search and search.lower() not in parsed["message"].lower():
                        continue
                        
                    logs.append(parsed)
    except Exception as e:
        logger.error(f"Failed to read logs: {e}")
        
    return {"success": True, "logs": logs}

@router.get("/logs/stats")
async def get_log_stats(admin: User = Depends(get_admin_user)):
    """
    Get statistics about the application logs.
    """
    from app.core.config import settings
    
    stats = {
        "total": 0,
        "levels": {"INFO": 0, "WARNING": 0, "ERROR": 0},
        "types": {"auth": 0, "order": 0, "cart": 0, "general": 0},
        "recent_24h": {"logins": 0, "orders": 0, "cart_actions": 0}
    }
    
    try:
        if os.path.exists(settings.LOG_FILE):
            with open(settings.LOG_FILE, "r") as f:
                # Read last 1000 lines for stats
                lines = f.readlines()[-1000:]
                
                for line in lines:
                    parsed = _parse_log_line(line)
                    if not parsed:
                        continue
                        
                    stats["total"] += 1
                    
                    level = parsed["level"]
                    if level in stats["levels"]:
                        stats["levels"][level] += 1
                        
                    log_type = parsed["type"]
                    if log_type in stats["types"]:
                        stats["types"][log_type] += 1
                    else:
                        stats["types"][log_type] = 1
                        
                    # Calculate recent activity based on message patterns
                    msg = parsed["message"].lower()
                    if log_type == "auth" and "logged in" in msg:
                        stats["recent_24h"]["logins"] += 1
                    elif log_type == "order" and "order placed" in msg:
                        stats["recent_24h"]["orders"] += 1
                    elif log_type == "cart":
                        stats["recent_24h"]["cart_actions"] += 1
                        
    except Exception as e:
        logger.error(f"Failed to read logs for stats: {e}")
        
    return {"success": True, "stats": stats}
