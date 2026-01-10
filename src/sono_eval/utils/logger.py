"""Logging configuration for Sono-Eval."""

import logging
import sys
from typing import Optional

from sono_eval.utils.config import get_config


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)
        level: Optional log level override

    Returns:
        Configured logger instance
    """
    config = get_config()
    log_level = level or config.log_level

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Only add handler if it doesn't already exist
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, log_level.upper()))

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
