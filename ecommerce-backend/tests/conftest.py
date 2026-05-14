import os
import sys
from typing import AsyncGenerator, Optional

import pytest
from fastapi import Header
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.api.deps import get_admin_user, get_current_user
from app.core.constants import UserRole
from app.core.database import Base, get_db
from app.models.product import Category, Product
from app.models.user import User
from app.utils.exceptions import ForbiddenException, UnauthorizedException


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    """
    Create all database tables before tests,
    then drop them after all tests finish.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide one async database session per test.
    """
    async with TestAsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """
    Create a normal test user.
    """
    user = User(
        email="user@test.com",
        hashed_password="hashed-password",
        first_name="Test",
        last_name="User",
        role=UserRole.USER,
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    return user


@pytest.fixture
async def admin_user(db_session: AsyncSession) -> User:
    """
    Create an admin test user.
    """
    admin = User(
        email="admin@test.com",
        hashed_password="hashed-password",
        first_name="Admin",
        last_name="User",
        role=UserRole.ADMIN,
        is_active=True,
    )

    db_session.add(admin)
    await db_session.flush()
    await db_session.refresh(admin)

    return admin


@pytest.fixture
def user_token() -> str:
    """
    Fake user token used only for tests.
    """
    return "test-user-token"


@pytest.fixture
def admin_token() -> str:
    """
    Fake admin token used only for tests.
    """
    return "test-admin-token"


@pytest.fixture
async def test_product(db_session: AsyncSession) -> Product:
    """
    Create a test category and a test product.
    """
    category = Category(
        name="Test Category",
        description="Category for order tests",
    )

    db_session.add(category)
    await db_session.flush()
    await db_session.refresh(category)

    product = Product(
        category_id=category.id,
        name="Test Product",
        description="Product for order tests",
        price=100.0,
        stock=50,
        is_active=True,
    )

    db_session.add(product)
    await db_session.flush()
    await db_session.refresh(product)

    return product


@pytest.fixture
async def client(
    db_session: AsyncSession,
    test_user: User,
    admin_user: User,
    user_token: str,
    admin_token: str,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Provide test client with database and authentication overrides.

    Auth behavior:
    - Bearer test-user-token  -> normal user
    - Bearer test-admin-token -> admin user
    - Missing/invalid token   -> 401
    """

    async def override_get_db():
        yield db_session

    async def override_get_current_user(
        authorization: Optional[str] = Header(None),
    ) -> User:
        if not authorization:
            raise UnauthorizedException("Invalid or expired token")

        parts = authorization.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise UnauthorizedException("Invalid or expired token")

        token = parts[1]

        if token == user_token:
            return test_user

        if token == admin_token:
            return admin_user

        raise UnauthorizedException("Invalid or expired token")

    async def override_get_admin_user(
        authorization: Optional[str] = Header(None),
    ) -> User:
        user = await override_get_current_user(authorization)

        if user.role != UserRole.ADMIN:
            raise ForbiddenException(
                "You don't have permission to perform this action"
            )

        return user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_admin_user] = override_get_admin_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()