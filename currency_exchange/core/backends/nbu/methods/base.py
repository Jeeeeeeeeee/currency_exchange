"""
doc string goes here
"""

__all__ = ['BaseMethod']

# Standard library imports.

# Related third party imports.

# Local application/library specific imports.


class BaseMethod:
    api_method_name = None

    def build_request(self, *args, **kwargs):
        raise NotImplementedError

    def parse_response(self, response):
        raise NotImplementedError
