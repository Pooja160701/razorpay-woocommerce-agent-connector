# Razorpay WooCommerce Agent Connector

A private, read-only WooCommerce connector exposed through MCP tools for an agent integration take-home project.

## What it does

- Lists and searches orders
- Gets an order by ID
- Lists and searches products
- Gets a product by ID
- Uses WooCommerce REST API key-pair authentication in live mode
- Includes mock mode for local testing without real credentials
- Handles 429/5xx responses with bounded exponential backoff
- Honors numeric `Retry-After` values when supplied
- Returns stable, agent-friendly errors
- Includes automated tests, Docker support, and GitHub Actions CI

## Structure

```text
.
├── src/woocommerce_connector/
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   ├── errors.py
│   ├── mock_data.py
│   ├── models.py
│   └── server.py
├── tests/
├── docs/
├── .github/workflows/ci.yml
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Run locally

Python 3.11+ is required.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Git Bash on Windows
# source .venv/Scripts/activate
# macOS/Linux
# source .venv/bin/activate
pip install -e ".[dev]"
```

Copy `.env.example` to `.env`. The application loads `.env` automatically. Keep the default `WOOCOMMERCE_MODE=mock` for a credential-free demo.

Start the MCP server:

```bash
python -m woocommerce_connector.server
```

The server uses MCP stdio, so a normal terminal can appear to wait without printing a web server URL. That is expected.

Run tests:

```bash
pytest -q
```

## MCP Inspector

The MCP Inspector can launch the connector process itself. Do not start a second standalone connector process first.

From the repository root:

```bash
npx @modelcontextprotocol/inspector python -m woocommerce_connector.server
```

Open the local Inspector URL printed by the command and verify the six tools:

- `list_orders`
- `search_orders`
- `get_order`
- `list_products`
- `search_products`
- `get_product`

Useful demo calls include:

```text
list_orders(page=1, per_page=2)
search_orders(query="maya@example.test")
get_order(order_id=1001)
search_products(query="BAG")
get_product(product_id=501)
```

## Live WooCommerce mode

The connector supports both a real HTTPS WooCommerce store and a local HTTP WooCommerce installation. WooCommerce requires one-legged OAuth 1.0a for non-SSL REST API requests; HTTPS can use Basic Auth. The local `http://pooja` setup therefore uses OAuth automatically.

Set these environment variables:

```env
WOOCOMMERCE_MODE=live
WOOCOMMERCE_BASE_URL=https://your-store.example.com
WOOCOMMERCE_CONSUMER_KEY=ck_your_key
WOOCOMMERCE_CONSUMER_SECRET=cs_your_secret
```

The client talks to `/wp-json/wc/v3` and never stores credentials in source control.

The implementation uses HTTP Basic authentication with the WooCommerce consumer key and consumer secret. Use store credentials with only the permissions required for the connector.

## Agent tools

| Tool | Purpose |
|---|---|
| `list_orders` | Paginated order listing with optional status |
| `search_orders` | Search orders by text such as ID/email |
| `get_order` | Get one order |
| `list_products` | Paginated product listing |
| `search_products` | Search products by name/SKU |
| `get_product` | Get one product |

See `docs/MCP_TOOLS.md` for the contract.

## Error handling

Tool failures are returned as a stable JSON object:

```json
{"error": "human-readable message"}
```

Examples include missing credentials, invalid pagination, empty search queries, missing records, authentication failures, provider failures, and exhausted rate-limit retries.

## Security and scope

The repository contains only fictional demo data using `example.test` addresses. The connector is intentionally read-only: no order writes, refunds, product mutations, webhook administration, or configuration changes are exposed.

See `docs/SECURITY.md` and `docs/AGENT_CAPABILITIES.md` for assumptions and limitations.

## Docker

Build the image:

```bash
docker build -t razorpay-woocommerce-agent-connector .
```

Validate and build the Compose service:

```bash
docker compose config
docker compose build
```

The default Compose configuration runs in mock mode, so no store credentials are required. If a local `.env` sets live-mode variables, Compose passes them into the container without baking them into the image.

## Assignment fit

This implements the private connector option with:

- working WooCommerce API-key authentication
- list/get/search primitives for orders and products
- pagination
- rate-limit and transient-error handling
- MCP tool definitions
- mock mode for safe evaluation
- setup and run instructions
- documented agent capabilities and limitations
- automated tests and CI
- container support

## Evaluation notes

No real customer data, passwords, API keys, or production store information are included. All sample records are fictional and use `example.test` addresses.

The implementation deliberately keeps the agent surface read-only. Write operations can be added later behind explicit authorization, audit logging, and narrower credential scopes.
