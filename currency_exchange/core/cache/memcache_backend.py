"""
doc string goes here
"""

__all__ = ['MemcachedBackend']

# Standard library imports.

# Related third party imports.
from pymemcache.client import base
from pymemcache import serde

# Local application/library specific imports.
from .base import BaseCacheBackend


class MemcachedBackend(BaseCacheBackend):
    _connection = None

    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port

    @property
    def connection(self):
        if self._connection is None:
            connection_string = '{}:{}'.format(self.host, self.port)
            # self._connection = base.Client(connection_string)
            self._connection = base.Client(
                server=(self.host, self.port),
                serializer=serde.python_memcache_serializer,
                deserializer=serde.python_memcache_deserializer
            )

        return self._connection

    def set(self, key, value, timeout=None):
        conn = self.connection
        conn.set(key, value, timeout)

    def get(self, key, default=None):
        conn = self.connection
        result = conn.get(key, default)
        return result
