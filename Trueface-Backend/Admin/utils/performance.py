import time
import logging
from functools import wraps
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)

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
