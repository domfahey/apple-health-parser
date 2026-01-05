"""Logging configuration for the Apple Health Parser.

Provides a pre-configured logger instance with INFO level and standard formatting.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
