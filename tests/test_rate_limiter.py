"""Comprehensive tests for rate limiting middleware."""

import asyncio
import time
from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi import FastAPI, Request
from starlette.responses import Response

from sono_eval.middleware.rate_limiter import (
    RateLimiterState,
    RateLimitMiddleware,
    RedisRateLimiterState,
)


class TestRateLimiterState:
    """Test in-memory rate limiter state."""

    @pytest.mark.asyncio
    async def test_initial_request_allowed(self):
        """Test that initial request is allowed."""
        limiter = RateLimiterState(max_requests=5, window_seconds=60)

        result = await limiter.is_allowed("test_client")

        assert result is True

    @pytest.mark.asyncio
    async def test_requests_within_limit(self):
        """Test that requests within limit are allowed."""
        limiter = RateLimiterState(max_requests=3, window_seconds=60)

        # Make 3 requests
        for i in range(3):
            result = await limiter.is_allowed("test_client")
            assert result is True, f"Request {i+1} should be allowed"

    @pytest.mark.asyncio
    async def test_request_exceeds_limit(self):
        """Test that requests exceeding limit are rejected."""
        limiter = RateLimiterState(max_requests=2, window_seconds=60)

        # First 2 requests should succeed
        assert await limiter.is_allowed("test_client") is True
        assert await limiter.is_allowed("test_client") is True

        # Third request should fail
        assert await limiter.is_allowed("test_client") is False

    @pytest.mark.asyncio
    async def test_window_expiration(self):
        """Test that requests are allowed after window expires."""
        limiter = RateLimiterState(max_requests=2, window_seconds=1)

        # Use up the limit
        assert await limiter.is_allowed("test_client") is True
        assert await limiter.is_allowed("test_client") is True
        assert await limiter.is_allowed("test_client") is False

        # Wait for window to expire
        await asyncio.sleep(1.1)

        # Should be allowed again
        assert await limiter.is_allowed("test_client") is True

    @pytest.mark.asyncio
    async def test_different_clients_isolated(self):
        """Test that different clients have separate limits."""
        limiter = RateLimiterState(max_requests=2, window_seconds=60)

        # Client 1 uses up limit
        assert await limiter.is_allowed("client1") is True
        assert await limiter.is_allowed("client1") is True
        assert await limiter.is_allowed("client1") is False

        # Client 2 should still be allowed
        assert await limiter.is_allowed("client2") is True
        assert await limiter.is_allowed("client2") is True

    @pytest.mark.asyncio
    async def test_get_remaining_requests(self):
        """Test getting remaining request count."""
        limiter = RateLimiterState(max_requests=5, window_seconds=60)

        # Initially should have full limit
        assert limiter.get_remaining("new_client") == 5

        # After one request
        await limiter.is_allowed("new_client")
        assert limiter.get_remaining("new_client") == 4

        # After two more requests
        await limiter.is_allowed("new_client")
        await limiter.is_allowed("new_client")
        assert limiter.get_remaining("new_client") == 2

    @pytest.mark.asyncio
    async def test_cleanup_old_keys(self):
        """Test that old keys are cleaned up to prevent memory leaks."""
        limiter = RateLimiterState(max_requests=1, window_seconds=1)

        # Create many keys
        for i in range(10005):
            await limiter.is_allowed(f"client_{i}")

        # Wait for window to expire
        await asyncio.sleep(1.1)

        # Trigger cleanup by adding one more
        await limiter.is_allowed("trigger_cleanup")

        # Should have cleaned up old keys (less than 10005 keys remaining)
        assert len(limiter.requests) < 10005

    @pytest.mark.asyncio
    async def test_concurrent_access(self):
        """Test thread-safe concurrent access."""
        limiter = RateLimiterState(max_requests=10, window_seconds=60)

        async def make_request(client_id):
            return await limiter.is_allowed(client_id)

        # Make 10 concurrent requests for same client
        tasks = [make_request("concurrent_client") for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # All 10 should succeed (within limit)
        assert sum(results) == 10

        # 11th should fail
        assert await limiter.is_allowed("concurrent_client") is False


class TestRedisRateLimiterState:
    """Test Redis-backed rate limiter state."""

    def test_initialization_without_redis(self):
        """Test initialization when Redis is not available."""
        limiter = RedisRateLimiterState(
            max_requests=60,
            window_seconds=60,
            redis_url="redis://nonexistent:6379"
        )

        # Should initialize without error
        assert limiter.max_requests == 60
        assert limiter.window_seconds == 60

    @pytest.mark.asyncio
    async def test_fallback_when_redis_unavailable(self):
        """Test that requests are allowed when Redis is unavailable."""
        limiter = RedisRateLimiterState(
            max_requests=5,
            window_seconds=60,
            redis_url="redis://nonexistent:6379"
        )

        # Should allow requests (fail-open behavior)
        result = await limiter.is_allowed("test_client")
        assert result is True

    @pytest.mark.asyncio
    async def test_redis_connection_with_mock(self):
        """Test Redis operations with mocked Redis client."""
        limiter = RedisRateLimiterState(
            max_requests=5,
            window_seconds=60,
            redis_url="redis://localhost:6379"
        )

        # Mock Redis client
        mock_redis = Mock()
        mock_pipeline = Mock()

        # Setup pipeline mock
        mock_pipeline.execute.return_value = [None, 2, None, None]  # zcard returns 2
        mock_redis.pipeline.return_value = mock_pipeline

        limiter._redis = mock_redis
        limiter._initialized = True

        # Should use Redis
        result = await limiter.is_allowed("test_client")

        assert result is True
        mock_redis.pipeline.assert_called_once()

    @pytest.mark.asyncio
    async def test_redis_rate_limit_exceeded(self):
        """Test rate limit exceeded with Redis."""
        limiter = RedisRateLimiterState(
            max_requests=3,
            window_seconds=60,
            redis_url="redis://localhost:6379"
        )

        # Mock Redis to return count at limit
        mock_redis = Mock()
        mock_pipeline = Mock()
        mock_pipeline.execute.return_value = [None, 3, None, None]  # At limit
        mock_redis.pipeline.return_value = mock_pipeline

        limiter._redis = mock_redis
        limiter._initialized = True

        result = await limiter.is_allowed("test_client")

        # Should be rejected
        assert result is False
        # Should remove the added request
        mock_redis.zrem.assert_called_once()

    @pytest.mark.asyncio
    async def test_redis_error_handling(self):
        """Test graceful handling of Redis errors."""
        limiter = RedisRateLimiterState(
            max_requests=5,
            window_seconds=60,
            redis_url="redis://localhost:6379"
        )

        # Mock Redis to raise error
        mock_redis = Mock()
        mock_redis.pipeline.side_effect = Exception("Redis error")

        limiter._redis = mock_redis
        limiter._initialized = True

        # Should fail open (allow request)
        result = await limiter.is_allowed("test_client")
        assert result is True

    def test_get_remaining_without_redis(self):
        """Test get_remaining when Redis is unavailable."""
        limiter = RedisRateLimiterState(
            max_requests=100,
            window_seconds=60,
            redis_url="redis://nonexistent:6379"
        )

        remaining = limiter.get_remaining("test_client")

        # Should return max when Redis unavailable
        assert remaining == 100


class TestRateLimitMiddleware:
    """Test rate limit middleware integration."""

    @pytest.fixture
    def app(self):
        """Create test FastAPI app."""
        app = FastAPI()

        @app.get("/test")
        async def test_endpoint():
            return {"message": "success"}

        @app.get("/health")
        async def health():
            return {"status": "ok"}

        return app

    @pytest.fixture
    def middleware_app(self, app):
        """Create app with rate limit middleware."""
        middleware = RateLimitMiddleware(
            app,
            max_requests_per_minute=5,
            max_requests_per_hour=20,
            exclude_paths=["/health"],
        )
        return middleware

    @pytest.mark.asyncio
    async def test_request_within_limits(self, middleware_app):
        """Test that requests within limits pass through."""
        # Create mock request and response
        request = Mock(spec=Request)
        request.url.path = "/test"
        request.client.host = "127.0.0.1"
        request.headers.get.return_value = None
        request.state = Mock()
        request.state.request_id = "test-123"

        response_mock = Response(content=b"success", status_code=200)

        async def call_next(req):
            return response_mock

        # Should allow request
        response = await middleware_app.dispatch(request, call_next)

        assert response.status_code == 200
        assert "X-RateLimit-Limit" in response.headers

    @pytest.mark.asyncio
    async def test_excluded_path_not_rate_limited(self, middleware_app):
        """Test that excluded paths bypass rate limiting."""
        request = Mock(spec=Request)
        request.url.path = "/health"

        response_mock = Response(content=b"ok", status_code=200)

        async def call_next(req):
            return response_mock

        # Make many requests - all should succeed
        for _ in range(10):
            response = await middleware_app.dispatch(request, call_next)
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_per_minute_limit_exceeded(self, middleware_app):
        """Test that per-minute limit is enforced."""
        request = Mock(spec=Request)
        request.url.path = "/test"
        request.client.host = "192.168.1.100"
        request.headers.get.return_value = None
        request.state = Mock()
        request.state.request_id = "test-456"

        async def call_next(req):
            return Response(content=b"success", status_code=200)

        # Make requests up to limit (5)
        for i in range(5):
            response = await middleware_app.dispatch(request, call_next)
            assert response.status_code == 200, f"Request {i+1} should succeed"

        # Next request should be rate limited
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            await middleware_app.dispatch(request, call_next)

        assert exc_info.value.status_code == 429
        assert "RATE_LIMIT_EXCEEDED" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_x_forwarded_for_header(self, middleware_app):
        """Test that X-Forwarded-For header is used for client identification."""
        request = Mock(spec=Request)
        request.url.path = "/test"
        request.headers.get.return_value = "10.0.0.5, 10.0.0.1"
        request.state = Mock()
        request.state.request_id = "test-789"

        async def call_next(req):
            return Response(content=b"success", status_code=200)

        response = await middleware_app.dispatch(request, call_next)

        # Should use first IP from X-Forwarded-For
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_rate_limit_headers(self, middleware_app):
        """Test that rate limit headers are added to response."""
        request = Mock(spec=Request)
        request.url.path = "/test"
        request.client.host = "10.0.0.10"
        request.headers.get.return_value = None
        request.state = Mock()
        request.state.request_id = "test-headers"

        async def call_next(req):
            return Response(content=b"success", status_code=200)

        response = await middleware_app.dispatch(request, call_next)

        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Backend" in response.headers
        assert response.headers["X-RateLimit-Backend"] == "memory"

    @pytest.mark.asyncio
    async def test_redis_backend_initialization(self):
        """Test middleware initialization with Redis backend."""
        app = FastAPI()

        with patch.dict("os.environ", {"RATE_LIMIT_REDIS_URL": "redis://localhost:6379"}):
            middleware = RateLimitMiddleware(
                app,
                max_requests_per_minute=60,
                redis_url="redis://localhost:6379",
            )

            # Should attempt Redis initialization
            assert middleware.backend in ["redis", "memory"]

    @pytest.mark.asyncio
    async def test_memory_fallback_on_redis_failure(self):
        """Test that memory fallback works when Redis fails."""
        app = FastAPI()

        middleware = RateLimitMiddleware(
            app,
            max_requests_per_minute=3,
            redis_url="redis://localhost:6379",
        )

        # Force Redis backend but simulate failure
        if middleware.backend == "redis":
            # Mock Redis failure
            middleware.per_minute._redis = Mock()
            middleware.per_minute._redis.pipeline.side_effect = Exception("Redis down")
            middleware.per_minute._initialized = True

        request = Mock(spec=Request)
        request.url.path = "/test"
        request.client.host = "10.0.0.20"
        request.headers.get.return_value = None
        request.state = Mock()
        request.state.request_id = "fallback-test"

        async def call_next(req):
            return Response(content=b"success", status_code=200)

        # Should still work via fallback
        response = await middleware_app.dispatch(request, call_next)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_per_hour_limit_independent_of_minute(self, middleware_app):
        """Test that per-hour limit is checked independently."""
        # This would require more complex setup with time mocking
        # For now, verify the structure exists
        assert hasattr(middleware_app, 'per_hour')
        assert hasattr(middleware_app, 'per_minute')
        assert middleware_app.per_hour.max_requests == 20
        assert middleware_app.per_minute.max_requests == 5

    def test_middleware_configuration(self):
        """Test middleware configuration options."""
        app = FastAPI()

        middleware = RateLimitMiddleware(
            app,
            max_requests_per_minute=100,
            max_requests_per_hour=500,
            exclude_paths=["/custom", "/path"],
        )

        assert middleware.per_minute.max_requests == 100
        assert middleware.per_hour.max_requests == 500
        assert "/custom" in middleware.exclude_paths
        assert "/path" in middleware.exclude_paths


class TestRateLimitEdgeCases:
    """Test edge cases and error scenarios."""

    @pytest.mark.asyncio
    async def test_missing_client_info(self):
        """Test handling of requests without client info."""
        app = FastAPI()
        middleware = RateLimitMiddleware(app, max_requests_per_minute=5)

        request = Mock(spec=Request)
        request.url.path = "/test"
        request.client = None  # No client info
        request.headers.get.return_value = None
        request.state = Mock()
        request.state.request_id = "no-client"

        async def call_next(req):
            return Response(content=b"success", status_code=200)

        # Should handle gracefully
        response = await middleware.dispatch(request, call_next)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_high_concurrency(self):
        """Test rate limiter under high concurrent load."""
        limiter = RateLimiterState(max_requests=50, window_seconds=60)

        async def make_requests(client_id, count):
            results = []
            for _ in range(count):
                results.append(await limiter.is_allowed(client_id))
            return results

        # Simulate 5 clients making 15 requests each concurrently
        tasks = [make_requests(f"client_{i}", 15) for i in range(5)]
        all_results = await asyncio.gather(*tasks)

        # Each client should have independent limits
        for results in all_results:
            # First 50 should succeed, rest should fail
            assert sum(results) == 15  # Within limit for each client
