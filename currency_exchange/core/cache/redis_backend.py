"""
doc string goes here
"""

__all__ = ['RedisBackend']

# Standard library imports.
import pickle

# Related third party imports.
from redis import Redis

# Local application/library specific imports.
from .base import BaseCacheBackend


def _serialize_data(data):
    if isinstance(data, str):
        result = data
    else:
        result = pickle.dumps(data)
    return result


def _deserialize_data(data):
    try:
        result = pickle.loads(data)
    except:
        result = data
    return result


class RedisBackend(BaseCacheBackend):
    _connection = None

    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port

    @property
    def connection(self):
        if self._connection is None:
            self._connection = Redis(host=self.host, port=self.port)
        return self._connection

    def set(self, key, value, timeout=None):
        conn = self.connection
        value = _serialize_data(value)
        conn.set(key, value, timeout)

    def get(self, key, default=None):
        conn = self.connection
        result = conn.get(key) or default
        result = _deserialize_data(result)
        return result
