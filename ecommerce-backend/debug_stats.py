import asyncio
from sqlalchemy import select, func, String
from app.core.database import AsyncSessionLocal
from app.models.order import Order

async def main():
    async with AsyncSessionLocal() as db:
        query = select(func.substr(func.cast(Order.created_at, String), 1, 10).label('date'))
        result = await db.execute(query)
        print(result.all())

asyncio.run(main())
