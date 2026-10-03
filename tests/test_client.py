import httpx
import pytest
import respx

from woocommerce_connector.client import WooCommerceClient
from woocommerce_connector.config import Settings
from woocommerce_connector.errors import AuthenticationError, RateLimitError


@pytest.mark.asyncio
async def test_mock_order_search():
    async with WooCommerceClient(Settings(mode="mock")) as client:
        items, meta = await client.search_orders("maya@example.test")
    assert len(items) == 2
    assert meta["total"] == 2


@pytest.mark.asyncio
async def test_live_auth_error():
    settings = Settings(
        mode="live",
        base_url="https://shop.example.test",
        consumer_key="",
        consumer_secret="",
    )
    async with WooCommerceClient(settings) as client:
        with pytest.raises(AuthenticationError):
            await client.list_orders()


@pytest.mark.asyncio
@respx.mock
async def test_retry_after_rate_limit():
    settings = Settings(
        mode="live",
        base_url="https://shop.example.test",
        consumer_key="ck_test",
        consumer_secret="cs_test",
        max_retries=1,
        backoff_factor=0,
    )
    route = respx.get(
        "https://shop.example.test/wp-json/wc/v3/orders"
    ).mock(
        side_effect=[
            httpx.Response(
                429,
                headers={"Retry-After": "0"},
                json={"message": "slow down"},
            ),
            httpx.Response(
                200,
                headers={"X-WP-Total": "4", "X-WP-TotalPages": "2"},
                json=[{"id": 1, "status": "processing"}],
            ),
        ]
    )

    async with WooCommerceClient(settings) as client:
        items, meta = await client.list_orders()

    assert route.call_count == 2
    assert items[0]["id"] == 1
    assert meta["total"] == 4
    assert meta["total_pages"] == 2


@pytest.mark.asyncio
@respx.mock
async def test_rate_limit_exhaustion():
    settings = Settings(
        mode="live",
        base_url="https://shop.example.test",
        consumer_key="ck_test",
        consumer_secret="cs_test",
        max_retries=1,
        backoff_factor=0,
    )
    respx.get(
        "https://shop.example.test/wp-json/wc/v3/orders"
    ).mock(
        side_effect=[
            httpx.Response(
                429,
                headers={"Retry-After": "0"},
                json={"message": "slow down"},
            ),
            httpx.Response(
                429,
                headers={"Retry-After": "0"},
                json={"message": "still slow"},
            ),
        ]
    )

    async with WooCommerceClient(settings) as client:
        with pytest.raises(RateLimitError):
            await client.list_orders()


@pytest.mark.asyncio
async def test_settings_read_environment_at_instantiation(monkeypatch):
    monkeypatch.setenv("WOOCOMMERCE_MODE", "live")
    monkeypatch.setenv("WOOCOMMERCE_BASE_URL", "https://store.example.test")
    monkeypatch.setenv("WOOCOMMERCE_CONSUMER_KEY", "ck_env")
    monkeypatch.setenv("WOOCOMMERCE_CONSUMER_SECRET", "cs_env")

    settings = Settings()

    assert settings.mode == "live"
    assert settings.base_url == "https://store.example.test"
    assert settings.consumer_key == "ck_env"
    assert settings.consumer_secret == "cs_env"
    assert settings.api_root == "https://store.example.test/wp-json/wc/v3"


@pytest.mark.asyncio
async def test_mock_status_filter():
    async with WooCommerceClient(Settings(mode="mock")) as client:
        items, meta = await client.list_orders(status="completed")

    assert [item["id"] for item in items] == [1002]
    assert meta["total"] == 1
