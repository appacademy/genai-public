"""
Utility functions for the LangChain-based NewsAgent application.
Provides enhanced terminal output and other helper functions.
"""

import logging
import time
from typing import Any, Optional, Callable
import functools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Flag to enable/disable colored output
USE_COLORS = True


def print_tool_action(message: str) -> None:
    """Print a message about a LangChain tool action."""
    prefix = f"{BLUE}[LangChain Tool]{RESET}" if USE_COLORS else "[LangChain Tool]"
    print(f"{prefix} {message}")


def print_chain_action(message: str) -> None:
    """Print a message about a LangChain chain action."""
    prefix = f"{GREEN}[LangChain Chain]{RESET}" if USE_COLORS else "[LangChain Chain]"
    print(f"{prefix} {message}")


def print_middleware_action(message: str) -> None:
    """Print a message about a LangChain middleware action."""
    prefix = (
        f"{YELLOW}[LangChain Middleware]{RESET}"
        if USE_COLORS
        else "[LangChain Middleware]"
    )
    print(f"{prefix} {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    prefix = f"{RED}[Error]{RESET}" if USE_COLORS else "[Error]"
    print(f"{prefix} {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    prefix = f"{GREEN}[Success]{RESET}" if USE_COLORS else "[Success]"
    print(f"{prefix} {message}")


def print_info(message: str) -> None:
    """Print an informational message."""
    print(message)


def print_header(message: str) -> None:
    """Print a header message."""
    if USE_COLORS:
        print(f"\n{BOLD}{message}{RESET}")
    else:
        print(f"\n{message}")
    print("=" * len(message))


def time_it(func: Callable) -> Callable:
    """Decorator to measure and print the execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print_info(f"Operation completed in {elapsed:.2f} seconds")
        return result

    return wrapper
