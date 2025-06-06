"""
Logging setup and utilities
"""

import logging
import colorlog
from logging import Logger, Filter


class ContextFilter(Filter):
    """Filter to add request_id to log records"""

    def __init__(self):
        super().__init__()
        self.request_id = "no_request"

    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = self.request_id
        return True


def setup_logger() -> Logger:
    """
    Create a comprehensive logging system with structured fields and context tracking
    """
    # Create a custom logger
    logger = logging.getLogger("llm_app")

    # Clear any existing handlers
    if logger.handlers:
        logger.handlers = []

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Create console handler with colored output
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] [%(request_id)s] %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )

    # Add formatter to console handler
    console_handler.setFormatter(formatter)

    # Create file handler for persistent logging
    file_handler = logging.FileHandler("llm_app.log")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(request_id)s] %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Create a filter to add request_id to log records
    context_filter = ContextFilter()
    logger.addFilter(context_filter)

    # Add the filter to the logger to provide a default request_id
    logger.context_filter = context_filter

    return logger
