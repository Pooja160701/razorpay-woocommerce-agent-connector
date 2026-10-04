from dataclasses import dataclass, field
import os
from dotenv import load_dotenv

load_dotenv()

def _int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default

def _float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value else default

@dataclass(frozen=True)
class Settings:
    mode: str = field(default_factory=lambda: os.getenv("WOOCOMMERCE_MODE", "mock"))
    base_url: str = field(
        default_factory=lambda: os.getenv(
            "WOOCOMMERCE_BASE_URL", "https://example.invalid"
        )
    )
    consumer_key: str = field(
        default_factory=lambda: os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
    )
    consumer_secret: str = field(
        default_factory=lambda: os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")
    )
    timeout_seconds: int = field(
        default_factory=lambda: _int("WOOCOMMERCE_TIMEOUT_SECONDS", 10)
    )
    max_retries: int = field(
        default_factory=lambda: _int("WOOCOMMERCE_MAX_RETRIES", 3)
    )
    backoff_factor: float = field(
        default_factory=lambda: _float("WOOCOMMERCE_BACKOFF_FACTOR", 0.5)
    )

    @property
    def api_root(self) -> str:
        return self.base_url.rstrip("/") + "/wp-json/wc/v3"