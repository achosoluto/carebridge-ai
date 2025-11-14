"""
Cache service implementation for CareBridge AI.
Provides caching functionality for performance optimization.
"""

from typing import Any, Optional
from django.core.cache import cache
from ..core.interfaces import CacheService


class DjangoCacheService(CacheService):
    """
    Django caching service implementation.
    Uses Django's cache framework with Redis or in-memory backend.
    """

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            return cache.get(key)
        except Exception as e:
            # Log error but don't break functionality
            from django.core.exceptions import ImproperlyConfigured
            from django.conf import settings
            import logging
            
            logger = logging.getLogger(__name__)
            logger.warning(f"Cache get error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Store value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None for default)
        """
        try:
            cache.set(key, value, timeout=ttl or 3600)  # Default 1 hour
        except Exception as e:
            from django.conf import settings
            import logging
            
            logger = logging.getLogger(__name__)
            logger.warning(f"Cache set error for key {key}: {e}")

    def delete(self, key: str) -> None:
        """
        Remove value from cache.

        Args:
            key: Cache key to delete
        """
        try:
            cache.delete(key)
        except Exception as e:
            from django.conf import settings
            import logging
            
            logger = logging.getLogger(__name__)
            logger.warning(f"Cache delete error for key {key}: {e}")


class SimpleCache:
    """
    Simple in-memory cache for development and testing.
    Not persistent across application restarts.
    """
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        entry = self._cache.get(key)
        if entry is None:
            return None
            
        value, expiry = entry
        import time
        
        if expiry and time.time() > expiry:
            # Entry expired, remove it
            del self._cache[key]
            return None
            
        return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        import time
        
        expiry = None
        if ttl:
            expiry = time.time() + ttl
            
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """Delete value from cache"""
        self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()


# Factory function to create appropriate cache service
def create_cache_service(use_simple: bool = False) -> CacheService:
    """
    Factory function to create cache service instance.
    
    Args:
        use_simple: If True, returns simple in-memory cache; otherwise Django cache
    
    Returns:
        CacheService instance
    """
    if use_simple:
        return SimpleCache()
    else:
        return DjangoCacheService()