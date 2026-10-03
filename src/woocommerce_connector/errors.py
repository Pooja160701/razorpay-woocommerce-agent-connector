class ConnectorError(Exception):
    """Stable connector-facing error."""


class AuthenticationError(ConnectorError):
    """Provider authentication failed."""


class RateLimitError(ConnectorError):
    """Provider rate limit persisted after retries."""


class ProviderError(ConnectorError):
    """Provider returned an error."""
