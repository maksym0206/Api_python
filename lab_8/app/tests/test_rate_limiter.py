import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport
from app import app
from app.auth.auth import User, get_optional_user
from app.database import book_collection

@pytest.mark.asyncio
@patch("app.rate_limiter.r", new_callable=AsyncMock)
async def test_anonymous_user_within_limit(mock_redis):
    mock_redis.zremrangebyscore.return_value = None
    mock_redis.zadd.return_value = None
    mock_redis.expire.return_value = None
    mock_redis.zcard.return_value = 1

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books/")
        assert response.status_code == 200

@pytest.mark.asyncio
@patch("app.rate_limiter.r", new_callable=AsyncMock)
async def test_anonymous_user_exceeds_limit(mock_redis):
    mock_redis.zremrangebyscore.return_value = None
    mock_redis.zadd.return_value = None
    mock_redis.expire.return_value = None
    mock_redis.zcard.return_value = 3

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books/")
        assert response.status_code == 429

@pytest.mark.asyncio
@patch("app.rate_limiter.r", new_callable=AsyncMock)
async def test_authenticated_user_within_limit(mock_redis):
    mock_redis.zremrangebyscore.return_value = None
    mock_redis.zadd.return_value = None
    mock_redis.expire.return_value = None
    mock_redis.zcard.return_value = 5

    async def override_get_optional_user():
        return User(username="testuser", email="test@example.com", password="123")
    app.dependency_overrides[get_optional_user] = override_get_optional_user

    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = []
    book_collection.find = MagicMock(return_value=mock_cursor)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books/", headers={"Authorization": "Bearer test_token"})
        assert response.status_code == 200

@pytest.mark.asyncio
@patch("app.rate_limiter.r", new_callable=AsyncMock)
async def test_authenticated_user_exceeds_limit(mock_redis):
    mock_redis.zremrangebyscore.return_value = None
    mock_redis.zadd.return_value = None
    mock_redis.expire.return_value = None
    mock_redis.zcard.return_value = 11

    async def override_get_optional_user():
        return User(username="testuser", email="test@example.com", password="123")
    app.dependency_overrides[get_optional_user] = override_get_optional_user

    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = []
    book_collection.find = MagicMock(return_value=mock_cursor)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books/", headers={"Authorization": "Bearer test_token"})
        assert response.status_code == 429




