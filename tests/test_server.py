import pytest

from woocommerce_connector import server


@pytest.mark.asyncio
async def test_list_orders_tool():
    result = await server.list_orders(page=1, per_page=2)
    assert result["page_info"]["total"] == 3
    assert len(result["items"]) == 2


@pytest.mark.asyncio
async def test_search_products_tool():
    result = await server.search_products("BAG")
    assert result["items"][0]["sku"] == "BAG-001"


@pytest.mark.asyncio
async def test_missing_order_returns_stable_error():
    result = await server.get_order(9999)
    assert result["error"] == "Order 9999 was not found"
