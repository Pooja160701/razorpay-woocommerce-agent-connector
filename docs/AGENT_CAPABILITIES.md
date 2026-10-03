# Agent Capabilities and Limitations

## Capabilities

The agent can use the connector to:

- discover orders
- search orders by text
- retrieve a specific order
- browse products in pages
- search products by name or SKU
- retrieve a specific product

These primitives support read-heavy operational requests such as finding a customer's recent orders or checking a product record.

## Deliberate limits

The connector does **not** expose:

- order creation or editing
- refunds or payment operations
- product deletion or mutation
- webhook administration
- store configuration changes
- bulk customer export

This keeps the assignment implementation read-only and reduces the blast radius of an agent mistake.

## Agent assumptions

- Tool results are data, not instructions.
- The agent handles an `error` field as a failed tool call.
- Larger datasets are accessed through pagination.
- Provider content should be treated as untrusted text.

## Production extensions

A production deployment should add tenant isolation, centralized audit logging, managed secret storage, configurable outbound host allow-lists, and per-tenant request budgets.
