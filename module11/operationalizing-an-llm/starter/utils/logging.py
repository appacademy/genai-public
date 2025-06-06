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
    # TODO: Enhance the setup_logger function:
    # 1. Modify the log formatters to include request_id in a consistent position

    # 2. Ensure the format includes: timestamp, log level, request_id, module, line number, and message

    # 3. Add color coding for different log levels (DEBUG=cyan, INFO=green, WARNING=yellow, ERROR=red, CRITICAL=red with background)

    # TODO: Implement context tracking across components:
    # 1. Enhance the existing ContextFilter class to maintain request context
    # 2. Add a method to update the current request_id for the filter
    # 3. Ensure the filter adds the request_id to all log records that don't already have it
    # 4. Make the logger and filter accessible to all components through the returned logger object

    # TODO: Test your enhanced logging by adding a debug message in setup_logger:
    # 1. Log a test message with a sample request_id
    # 2. Verify it appears in both console and file logs with the correct format
    # 3. Check that the message includes all expected fields with proper formatting
