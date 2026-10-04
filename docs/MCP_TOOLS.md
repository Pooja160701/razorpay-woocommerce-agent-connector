# MCP Tool Specification

The connector exposes six read-only tools through the MCP server.

## `list_orders`

Lists orders with bounded pagination and optional status filtering.

Arguments:
- `page`: integer, default `1`
- `per_page`: integer, default `20`, maximum `100`
- `status`: optional WooCommerce status

## `search_orders`

Searches orders using provider search text. Mock mode also matches fictional order IDs and emails.

Arguments:
- `query`: required non-empty string
- `page`: integer
- `per_page`: integer

## `get_order`

Arguments:
- `order_id`: integer

## `list_products`

Arguments:
- `page`: integer
- `per_page`: integer

## `search_products`

Searches product name or SKU.

Arguments:
- `query`: required non-empty string
- `page`: integer
- `per_page`: integer

## `get_product`

Arguments:
- `product_id`: integer

## Common response shape

Paged tools return:

```json
{
  "items": [],
  "page_info": {
    "page": 1,
    "per_page": 20,
    "total": 3,
    "total_pages": 1
  }
}
```

## Error shape

The MCP tool layer normalizes connector failures to:

```json
{"error": "human-readable message"}
```

Credentials, authorization headers, and raw secrets are never returned to the agent.

## Example agent calls

```text
search_orders(query="maya@example.test")
get_order(order_id=1001)
search_products(query="BAG-001")
get_product(product_id=501)
```