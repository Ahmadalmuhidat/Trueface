# Import cache utilities from Admin app
from Admin.utils.cache import cache_result, cache_invalidate, get_or_set_cache

__all__ = ['cache_result', 'cache_invalidate', 'get_or_set_cache']
