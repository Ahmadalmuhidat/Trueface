import requests
import threading

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_session = None
_session_lock = threading.Lock()

def get_session():
  global _session
  if _session is None:
    with _session_lock:
      if _session is None:
        _session = requests.Session()

        # ... (rest of setup)
        retry_strategy = Retry(
          total=3,
          backoff_factor=1,
          status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(
          max_retries=retry_strategy,
          pool_connections=10,
          pool_maxsize=20
        )

        _session.mount("http://", adapter)
        _session.mount("https://", adapter)
        _session.timeout = 10

  from app.config.configurations import Configurations
  token_data = Configurations.get_token()
  if token_data:
    # Handle if token is a dict or string
    token = token_data.get("token") if isinstance(token_data, dict) else token_data
    _session.headers.update({"Authorization": f"Bearer {token}"})

  return _session
