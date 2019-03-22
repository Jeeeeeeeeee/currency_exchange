"""
doc string goes here
"""

__all__ = ['registry', 'BackendRegistry']

# Standard library imports.
import copy

# Related third party imports.

# Local application/library specific imports.


class BackendRegistry:
    def __init__(self):
        self._backends = {}

    def register(self, name, cls):
        self._backends[name] = cls

    def get_backend(self, name):
        return self._backends.get(name, None)

    @property
    def backends(self):
        result = copy.deepcopy(self._backends)
        return result


registry = BackendRegistry()
