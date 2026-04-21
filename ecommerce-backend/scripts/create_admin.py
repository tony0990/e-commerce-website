import asyncio
import os
import sys

# Add the project root to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.core.constants import UserRole

async def create_admin():
    """Create a default admin user based on environment variables."""
    print(f"[*] Starting admin creation process...")
    
    async with AsyncSessionLocal() as session:
        # Check if admin already exists
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
        admin = result.scalar_one_or_none()
        
        if admin:
            print(f"[!] Admin user with email {settings.ADMIN_EMAIL} already exists.")
            return

        # Create new admin user
        new_admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=hash_password(settings.ADMIN_PASSWORD),
            first_name=settings.ADMIN_FIRST_NAME,
            last_name=settings.ADMIN_LAST_NAME,
            role=UserRole.ADMIN,
            is_active=True
        )
        
        session.add(new_admin)
        await session.commit()
        print(f"[+] Admin user {settings.ADMIN_EMAIL} created successfully!")

if __name__ == "__main__":
    asyncio.run(create_admin())
