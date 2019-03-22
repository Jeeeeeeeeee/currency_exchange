"""
doc string goes here
"""

__all__ = ['BaseBackend']

# Standard library imports.

# Related third party imports.

# Local application/library specific imports.


class BaseBackend:
    provider_name = None

    def download_data(self, on_date):
        raise NotImplementedError()
