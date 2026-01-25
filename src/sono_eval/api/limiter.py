"""Rate limiter configuration."""

from slowapi import Limiter
from slowapi.util import get_remote_address
from sono_eval.utils.config import get_config

config = get_config()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[config.rate_limit_default],
    enabled=config.rate_limit_enabled,
)
