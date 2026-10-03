# Security Notes

## Credentials

Live credentials are read from environment variables only:

- `WOOCOMMERCE_CONSUMER_KEY`
- `WOOCOMMERCE_CONSUMER_SECRET`

Do not commit keys, screenshots containing keys, or copied store data.

## Data handling

The repository contains fictional records only. Demo email addresses use `example.test`.

## Access scope

The connector exposes read-only primitives. Use credentials scoped to the intended WooCommerce store and environment.

## Reliability controls

Requests have bounded timeouts and bounded retries. HTTP 429 and common transient 5xx responses use exponential backoff; `Retry-After` is honored when supplied.

## Threats and mitigations

| Risk | Mitigation |
|---|---|
| Credential leakage | Environment-only secrets and `.gitignore` |
| Accidental write | No write tools are implemented |
| Request storms | Bounded retries and pagination |
| Provider outage | Normalized provider errors |
| Prompt injection in store content | Treat provider content as untrusted data; defense belongs in the agent layer |
| Cross-tenant access | Requires tenant-scoped credentials in the deployment layer |
