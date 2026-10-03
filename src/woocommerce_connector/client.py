from __future__ import annotations

import asyncio
from typing import Any

import httpx

from .config import Settings
from .errors import AuthenticationError, ConnectorError, ProviderError, RateLimitError
from .mock_data import ORDERS, PRODUCTS

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class WooCommerceClient:
    def __init__(self, settings: Settings | None = None, transport: httpx.AsyncBaseTransport | None = None):
        self.settings = settings or Settings()
        self._transport = transport
        self._http: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self._http = httpx.AsyncClient(
            timeout=self.settings.timeout_seconds,
            transport=self._transport,
        )
        return self

    async def __aexit__(self, *_exc):
        if self._http:
            await self._http.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> tuple[Any, httpx.Headers]:
        if self.settings.mode == "mock":
            raise ConnectorError("Mock requests should use the mock data path")
        if self._http is None:
            raise ConnectorError("Client must be used as an async context manager")
        if not self.settings.consumer_key or not self.settings.consumer_secret:
            raise AuthenticationError("WooCommerce API credentials are not configured")

        url = f"{self.settings.api_root}/{path.lstrip('/')}"
        auth = (self.settings.consumer_key, self.settings.consumer_secret)
        last_error: Exception | None = None

        for attempt in range(self.settings.max_retries + 1):
            try:
                response = await self._http.request(
                    method,
                    url,
                    params=params,
                    auth=auth,
                )

                if response.status_code in {401, 403}:
                    raise AuthenticationError("WooCommerce rejected the API credentials")

                if response.status_code in RETRYABLE_STATUS_CODES:
                    if attempt >= self.settings.max_retries:
                        if response.status_code == 429:
                            raise RateLimitError("WooCommerce rate limit persisted after retries")
                        raise ProviderError(
                            f"WooCommerce returned HTTP {response.status_code}"
                        )

                    retry_after = response.headers.get("Retry-After")
                    delay = _retry_delay(retry_after, self.settings.backoff_factor, attempt)
                    await asyncio.sleep(min(max(delay, 0), 30))
                    continue

                if response.is_error:
                    raise ProviderError(
                        f"WooCommerce returned HTTP {response.status_code}: "
                        f"{_error_detail(response)}"
                    )

                try:
                    return response.json(), response.headers
                except ValueError as exc:
                    raise ProviderError("WooCommerce returned a non-JSON response") from exc

            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt >= self.settings.max_retries:
                    raise ProviderError("WooCommerce request failed after retries") from exc
                await asyncio.sleep(
                    min(self.settings.backoff_factor * (2**attempt), 30)
                )

        raise ProviderError("WooCommerce request failed") from last_error

    async def list_orders(
        self,
        page: int = 1,
        per_page: int = 20,
        status: str | None = None,
    ):
        page, per_page = _page_args(page, per_page)
        if self.settings.mode == "mock":
            items = [x for x in ORDERS if not status or x["status"] == status]
            return _paginate(items, page, per_page)

        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        data, headers = await self._request("GET", "orders", params)
        return _with_headers(data, headers)

    async def search_orders(
        self,
        query: str,
        page: int = 1,
        per_page: int = 20,
    ):
        if not query.strip():
            raise ConnectorError("Search query must not be empty")

        page, per_page = _page_args(page, per_page)

        if self.settings.mode == "mock":
            needle = query.lower()
            items = [
                x
                for x in ORDERS
                if needle in str(x["id"]).lower()
                or needle in x["billing"]["email"].lower()
            ]
            return _paginate(items, page, per_page)

        params = {"search": query, "page": page, "per_page": per_page}
        data, headers = await self._request("GET", "orders", params)
        return _with_headers(data, headers)

    async def get_order(self, order_id: int):
        if self.settings.mode == "mock":
            return _get_mock(ORDERS, order_id, "order")
        data, _ = await self._request("GET", f"orders/{order_id}")
        return data

    async def list_products(self, page: int = 1, per_page: int = 20):
        page, per_page = _page_args(page, per_page)

        if self.settings.mode == "mock":
            return _paginate(PRODUCTS, page, per_page)

        data, headers = await self._request(
            "GET",
            "products",
            {"page": page, "per_page": per_page},
        )
        return _with_headers(data, headers)

    async def search_products(
        self,
        query: str,
        page: int = 1,
        per_page: int = 20,
    ):
        if not query.strip():
            raise ConnectorError("Search query must not be empty")

        page, per_page = _page_args(page, per_page)

        if self.settings.mode == "mock":
            needle = query.lower()
            items = [
                x
                for x in PRODUCTS
                if needle in x["name"].lower()
                or needle in x.get("sku", "").lower()
            ]
            return _paginate(items, page, per_page)

        params = {"search": query, "page": page, "per_page": per_page}
        data, headers = await self._request("GET", "products", params)
        return _with_headers(data, headers)

    async def get_product(self, product_id: int):
        if self.settings.mode == "mock":
            return _get_mock(PRODUCTS, product_id, "product")
        data, _ = await self._request("GET", f"products/{product_id}")
        return data


def _retry_delay(retry_after: str | None, backoff_factor: float, attempt: int) -> float:
    if retry_after:
        try:
            return float(retry_after)
        except ValueError:
            pass
    return backoff_factor * (2**attempt)


def _page_args(page: int, per_page: int) -> tuple[int, int]:
    if page < 1:
        raise ConnectorError("page must be at least 1")
    if per_page < 1 or per_page > 100:
        raise ConnectorError("per_page must be between 1 and 100")
    return page, per_page


def _paginate(
    items: list[dict[str, Any]],
    page: int,
    per_page: int,
):
    total = len(items)
    start = (page - 1) * per_page
    return items[start : start + per_page], {
        "total": total,
        "total_pages": (total + per_page - 1) // per_page if total else 0,
    }


def _with_headers(
    data: list[dict[str, Any]],
    headers: httpx.Headers,
):
    return data, {
        "total": _header_int(headers, "X-WP-Total"),
        "total_pages": _header_int(headers, "X-WP-TotalPages"),
    }


def _header_int(headers: httpx.Headers, name: str) -> int | None:
    value = headers.get(name)
    return int(value) if value and value.isdigit() else None


def _get_mock(items: list[dict[str, Any]], item_id: int, label: str):
    for item in items:
        if item["id"] == item_id:
            return item
    raise ConnectorError(f"{label.capitalize()} {item_id} was not found")


def _error_detail(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text[:200]

    if isinstance(payload, dict):
        return str(payload.get("message") or payload.get("code") or payload)[:200]

    return str(payload)[:200]
