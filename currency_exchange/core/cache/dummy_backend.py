"""
doc string goes here
"""

__all__ = ['DummyCacheBackend']

# Standard library imports.

# Related third party imports.

# Local application/library specific imports.
from .base import BaseCacheBackend


class DummyCacheBackend(BaseCacheBackend):
    def set(self, key, value, timeout=None):
        pass

    def get(self, key, default=None):
        pass
