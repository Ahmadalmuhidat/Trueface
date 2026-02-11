import json
import hashlib
from functools import wraps
from django.core.cache import cache
from django.conf import settings

def cache_result(timeout=300, key_prefix="api"):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()}"
      
      result = cache.get(cache_key)
      if result is not None:
        return result
      
      result = func(*args, **kwargs)
      cache.set(cache_key, result, timeout)
      return result
    return wrapper
  return decorator


def cache_invalidate(pattern):
  try:
    if hasattr(cache, 'keys'):
      cache.delete_many(cache.keys(f"*{pattern}*"))
    else:
      cache.clear()
  except Exception:
    pass

def get_or_set_cache(key, callable_func, timeout=300):
  result = cache.get(key)
  if result is None:
    result = callable_func()
    cache.set(key, result, timeout)
  return result
