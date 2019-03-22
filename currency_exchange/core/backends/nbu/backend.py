"""
doc string goes here
"""

__all__ = ['NBUBackend']

# Standard library imports.

# Related third party imports.

# Local application/library specific imports.
from currency_exchange.core.backends.base import BaseBackend
from .methods import JsonExchangeMethod
from .connector import Connector


class NBUBackend(BaseBackend):
    provider_name = 'NBU'

    def __init__(self):
        self.connector = Connector()

    def download_data(self, on_date):
        method = JsonExchangeMethod(on_date, self.provider_name)
        result = self.connector.execute(method)
        swapped = [val.swap() for val in result]
        result.extend(swapped)

        return result
