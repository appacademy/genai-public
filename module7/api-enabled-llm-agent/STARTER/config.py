"""
Configuration settings for the NewsAgent.
"""

# News API settings
NEWS_API_BASE_URL = "https://newsapi.org/v2"
DEFAULT_COUNTRY = "us"
VALID_CATEGORIES = [
    "business", "entertainment", "general",
    "health", "science", "sports", "technology"
]

# Cache settings
DEFAULT_CACHE_EXPIRY = 3600  # 1 hour in seconds

# Rate limiting settings
REQUESTS_PER_MINUTE = 60  # Default API limit
MAX_RETRIES = 3
BACKOFF_FACTOR = 2.0
MAX_BACKOFF_DELAY = 60.0  # Maximum backoff of 1 minute

# Circuit breaker settings
FAILURE_THRESHOLD = 5
RECOVERY_TIMEOUT = 60  # 1 minute
