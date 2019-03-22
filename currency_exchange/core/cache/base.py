"""
doc string goes here
"""

__all__ = ['BaseCacheBackend']

# Standard library imports.

# Related third party imports.

# Local application/library specific imports.


class BaseCacheBackend:
    def set(self, key, value, timeout=None):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError
