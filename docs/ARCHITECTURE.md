# Architecture

```text
Agent / MCP client
        |
        v
+------------------------+
| MCP tool layer         |
| orders / products      |
+-----------+------------+
            |
            v
+------------------------+
| WooCommerce client     |
| auth / timeout /       |
| retries / errors       |
+-----------+------------+
            |
      +-----+-----+
      |           |
      v           v
  Mock data   WooCommerce
              REST API
```

## Tool layer

`server.py` is the stable agent-facing contract. It exposes only the operations useful for the assignment and converts connector exceptions into predictable tool results.

## Client layer

`client.py` owns HTTP concerns: authentication, timeout, retry behavior, rate limits, pagination arguments, and provider error normalization.

## Mock layer

`mock_data.py` provides deterministic fictional records so the project can be evaluated without a real store or customer information.

## Configuration

`config.py` reads environment variables and supplies safe defaults for mock mode.

## Production direction

For a multi-tenant deployment, credentials should be provided by a secret manager or credential broker. The connector should receive tenant-scoped credentials rather than exposing a shared master credential to the agent runtime. Metrics and audit events should be emitted outside the connector so provider-specific code stays focused.