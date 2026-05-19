import hashlib
import logging
import os
import random
import string
import sys
import time
from functools import wraps

import jwt
from django.conf import settings
from django.core.cache import cache
from django.db import connection

from authentication.services.mailer import SendEmailTemplate

logger = logging.getLogger(__name__)


# --- Password Utilities ---
def generate_password(length=12, use_special_chars=False):
  characters = string.ascii_letters + string.digits
  if use_special_chars:
    characters += string.punctuation

  password_chars = [
    random.choice(string.ascii_lowercase),
    random.choice(string.ascii_uppercase),
    random.choice(string.digits),
  ]
  if use_special_chars:
    password_chars.append(random.choice(string.punctuation))

  while len(password_chars) < length:
    password_chars.append(random.choice(characters))

  random.shuffle(password_chars)
  return "".join(password_chars)


# --- JWT Utilities ---
def GenerateToken(payload):
  try:
    return jwt.encode(payload=payload, key=os.getenv("JWT_TOKEN_SECRET"), algorithm="HS256")
  except Exception:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(exc_obj)


def validate_token(token):
  try:
    return jwt.decode(token, key=os.getenv("JWT_TOKEN_SECRET"), algorithms=["HS256"])
  except jwt.ExpiredSignatureError:
    print("Token has expired. Please log in again.")
  except jwt.InvalidTokenError:
    print("Invalid token. Access denied.")
  except Exception:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(exc_obj)


# --- Mail Utilities ---
def SendGeneratedPasswordMail(password: str, recipient_list: list[str]):
  template_path = os.path.join(os.path.dirname(__file__), "services", "mail_templates", "generated_pass.html")
  with open(template_path) as f:
    html_template = f.read()

  html_content = html_template.replace("{{password}}", password)
  subject = "Welcome to TrueFace"

  SendEmailTemplate(subject, html_content, recipient_list)


# --- Cache Utilities ---
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
    if hasattr(cache, "keys"):
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


# --- Performance Monitoring Utilities ---
def monitor_performance(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.time()
    initial_queries = len(connection.queries)

    try:
      result = func(*args, **kwargs)
      end_time = time.time()
      execution_time = end_time - start_time
      queries_count = len(connection.queries) - initial_queries

      logger.info(f"Function {func.__name__} executed in {execution_time:.3f}s with {queries_count} queries")

      if execution_time > 1.0:
        logger.warning(f"Slow function: {func.__name__} took {execution_time:.3f}s")

      if queries_count > 10:
        logger.warning(f"High query count: {func.__name__} executed {queries_count} queries")

      return result

    except Exception as e:
      end_time = time.time()
      execution_time = end_time - start_time
      logger.error(f"Function {func.__name__} failed after {execution_time:.3f}s: {str(e)}")
      raise

  return wrapper


def log_sql_queries(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if settings.DEBUG:
      initial_queries = len(connection.queries)
      result = func(*args, **kwargs)
      queries = connection.queries[initial_queries:]

      logger.info(f"SQL queries for {func.__name__}:")
      for query in queries:
        logger.info(f"  {query['sql']} ({query['time']}s)")

      return result
    else:
      return func(*args, **kwargs)

  return wrapper
