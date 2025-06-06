import time
import json
import hashlib
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Cache:
    """
    A simple in-memory cache with time-based expiration.
    """
    
    def __init__(self, expiry_time: int = 3600):
        """
        Initialize the cache.
        
        Args:
            expiry_time: Default cache entry lifetime in seconds
        """
        self.cache_data: Dict[str, Dict[str, Any]] = {}
        self.default_expiry_time = expiry_time
        logger.info(f"Cache initialized with {expiry_time}s expiry time")
    
    def _generate_key(self, url: str, params: Dict[str, Any]) -> str:
        """
        Generate a unique cache key based on URL and parameters.
        
        Args:
            url: The API endpoint URL
            params: Query parameters
            
        Returns:
            A unique hash key
        """
        # Create a copy of params without the API key to avoid caching based on API key
        cache_params = params.copy()
        if 'apiKey' in cache_params:
            del cache_params['apiKey']
            
        # Create a string representation of the URL and parameters
        cache_data = f"{url}_{json.dumps(cache_params, sort_keys=True)}"
        
        # Generate a hash
        return hashlib.md5(cache_data.encode()).hexdigest()
    
    def get(self, url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from cache if it exists and is still valid.
        
        Args:
            url: The API endpoint URL
            params: Query parameters
            
        Returns:
            Cached data or None if not found or expired
        """
        key = self._generate_key(url, params)
        cache_entry = self.cache_data.get(key)
        
        if not cache_entry:
            logger.debug(f"Cache miss for key {key}")
            return None
            
        # Check if the entry has expired
        timestamp = cache_entry.get('timestamp', 0)
        expiry_time = cache_entry.get('expiry_time', self.default_expiry_time)
        
        if time.time() - timestamp > expiry_time:
            logger.debug(f"Cache entry expired for key {key}")
            del self.cache_data[key]
            return None
            
        logger.debug(f"Cache hit for key {key}")
        return cache_entry.get('data')
    
    def set(self, url: str, params: Dict[str, Any], data: Dict[str, Any], expiry_time: Optional[int] = None) -> None:
        """
        Store data in the cache.
        
        Args:
            url: The API endpoint URL
            params: Query parameters
            data: The data to cache
            expiry_time: Optional custom expiration time
        """
        key = self._generate_key(url, params)
        
        if expiry_time is None:
            expiry_time = self.default_expiry_time
            
        self.cache_data[key] = {
            'data': data,
            'timestamp': time.time(),
            'expiry_time': expiry_time
        }
        
        logger.debug(f"Added entry to cache with key {key}")
        
        # Periodically clean up expired entries
        if len(self.cache_data) % 10 == 0:  # Clean every 10 insertions
            self.clear_expired()
    
    def clear_expired(self) -> None:
        """
        Remove all expired entries from the cache.
        """
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache_data.items():
            timestamp = entry.get('timestamp', 0)
            expiry_time = entry.get('expiry_time', self.default_expiry_time)
            
            if current_time - timestamp > expiry_time:
                expired_keys.append(key)
                
        for key in expired_keys:
            del self.cache_data[key]
            
        if expired_keys:
            logger.debug(f"Cleared {len(expired_keys)} expired cache entries")