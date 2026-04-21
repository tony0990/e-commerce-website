"""
Dashboard Data Module (Mahmoud + Tony)
========================================
Provides aggregated data for the admin monitoring dashboard.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User
from app.core.constants import UserRole
from datetime import datetime, timezone, timedelta


class DashboardService:
    """Service for aggregating dashboard statistics."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_overview(self) -> dict:
        """Get general dashboard overview stats."""
        # Total users
        total_users_result = await self.db.execute(
            select(func.count(User.id))
        )
        total_users = total_users_result.scalar() or 0

        # Active users
        active_users_result = await self.db.execute(
            select(func.count(User.id)).where(User.is_active == True)
        )
        active_users = active_users_result.scalar() or 0

        # Admin count
        admin_count_result = await self.db.execute(
            select(func.count(User.id)).where(User.role == UserRole.ADMIN)
        )
        admin_count = admin_count_result.scalar() or 0

        # New users (last 7 days)
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        new_users_result = await self.db.execute(
            select(func.count(User.id)).where(User.created_at >= seven_days_ago)
        )
        new_users = new_users_result.scalar() or 0

        # New users (last 30 days)
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        monthly_users_result = await self.db.execute(
            select(func.count(User.id)).where(User.created_at >= thirty_days_ago)
        )
        monthly_users = monthly_users_result.scalar() or 0

        return {
            "users": {
                "total": total_users,
                "active": active_users,
                "inactive": total_users - active_users,
                "admins": admin_count,
                "new_last_7_days": new_users,
                "new_last_30_days": monthly_users,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    async def get_user_growth(self, days: int = 30) -> list:
        """
        Get daily user registration counts for the given number of days.

        Returns a list of {date, count} objects.
        """
        growth_data = []
        for i in range(days - 1, -1, -1):
            day_start = datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - timedelta(days=i)
            day_end = day_start + timedelta(days=1)

            count_result = await self.db.execute(
                select(func.count(User.id)).where(
                    User.created_at >= day_start,
                    User.created_at < day_end,
                )
            )
            count = count_result.scalar() or 0
            growth_data.append({
                "date": day_start.strftime("%Y-%m-%d"),
                "count": count,
            })

        return growth_data
