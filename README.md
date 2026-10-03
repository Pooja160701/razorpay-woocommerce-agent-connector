# Razorpay WooCommerce Agent Connector

A private, read-only WooCommerce connector exposed through MCP tools for an agent integration take-home project.

## What it does

- Lists and searches orders
- Gets an order by ID
- Lists and searches products
- Gets a product by ID
- Uses WooCommerce REST API keys in live mode
- Includes mock mode for local testing without real credentials
- Handles 429/5xx responses with bounded exponential backoff
- Returns stable, agent-friendly errors
- Includes tests, Docker support, and GitHub Actions CI

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
# macOS/Linux
# source .venv/bin/activate
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and keep the default `WOOCOMMERCE_MODE=mock` for a credential-free demo.

Start the MCP server:

```bash
python -m woocommerce_connector.server
```

Run tests:

```bash
pytest -q
```

## Live WooCommerce mode

Set these environment variables:

```env
WOOCOMMERCE_MODE=live
WOOCOMMERCE_BASE_URL=https://your-store.example.com
WOOCOMMERCE_CONSUMER_KEY=ck_your_key
WOOCOMMERCE_CONSUMER_SECRET=cs_your_secret
```

The client talks to `/wp-json/wc/v3` and never stores credentials in source control.

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

## Security and scope

The repository contains only fictional demo data using `example.test` addresses. The connector is intentionally read-only: no order writes, refunds, product mutations, webhook administration, or configuration changes are exposed.

See `docs/SECURITY.md` and `docs/AGENT_CAPABILITIES.md` for assumptions and limitations.

## Assignment fit

This implements the private connector option with working authentication, list/get/search primitives, pagination, rate-limit handling, MCP tool definitions, setup instructions, and documented agent capabilities/limitations.
