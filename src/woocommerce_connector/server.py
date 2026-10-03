from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import WooCommerceClient
from .config import Settings
from .errors import ConnectorError

mcp = FastMCP("woocommerce-private-connector")


def _settings() -> Settings:
    return Settings()


async def _paged(items, page, per_page, meta):
    return {"items": items, "page_info": {"page": page, "per_page": per_page, "total": meta.get("total"), "total_pages": meta.get("total_pages")}}


def _error(exc: ConnectorError) -> dict[str, Any]:
    return {"error": str(exc)}


@mcp.tool()
async def list_orders(page: int = 1, per_page: int = 20, status: str | None = None) -> dict[str, Any]:
    """List WooCommerce orders, optionally filtered by status."""
    try:
        async with WooCommerceClient(_settings()) as client:
            items, meta = await client.list_orders(page, per_page, status)
            return await _paged(items, page, per_page, meta)
    except ConnectorError as exc:
        return _error(exc)


@mcp.tool()
async def search_orders(query: str, page: int = 1, per_page: int = 20) -> dict[str, Any]:
    """Search WooCommerce orders by text such as order ID or customer email."""
    try:
        async with WooCommerceClient(_settings()) as client:
            items, meta = await client.search_orders(query, page, per_page)
            return await _paged(items, page, per_page, meta)
    except ConnectorError as exc:
        return _error(exc)


@mcp.tool()
async def get_order(order_id: int) -> dict[str, Any]:
    """Get one WooCommerce order by ID."""
    try:
        async with WooCommerceClient(_settings()) as client:
            return await client.get_order(order_id)
    except ConnectorError as exc:
        return _error(exc)


@mcp.tool()
async def list_products(page: int = 1, per_page: int = 20) -> dict[str, Any]:
    """List WooCommerce products."""
    try:
        async with WooCommerceClient(_settings()) as client:
            items, meta = await client.list_products(page, per_page)
            return await _paged(items, page, per_page, meta)
    except ConnectorError as exc:
        return _error(exc)


@mcp.tool()
async def search_products(query: str, page: int = 1, per_page: int = 20) -> dict[str, Any]:
    """Search products by name or SKU."""
    try:
        async with WooCommerceClient(_settings()) as client:
            items, meta = await client.search_products(query, page, per_page)
            return await _paged(items, page, per_page, meta)
    except ConnectorError as exc:
        return _error(exc)


@mcp.tool()
async def get_product(product_id: int) -> dict[str, Any]:
    """Get one WooCommerce product by ID."""
    try:
        async with WooCommerceClient(_settings()) as client:
            return await client.get_product(product_id)
    except ConnectorError as exc:
        return _error(exc)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
