"""
doc string goes here
"""

__all__ = ['BaseStorage']

# Standard library imports.

# Related third party imports.

# Local application/library specific imports.


class BaseStorage:
    DB_TABLES = ('currency_exchange_rate', 'currency', 'provider')

    def __init__(self, *args, **kwargs):
        pass

    @property
    def connection(self):
        raise NotImplementedError

    def store_currencies(self, currencies):
        raise NotImplementedError

    def store_rates(self, exchange_rates):
        raise NotImplementedError

    def get_currencies(self, provider_names, currency_codes):
        raise NotImplementedError

    def get_rates(self, provider_names, currency_code, to_currencies=None, on_date=None):
        raise NotImplementedError

    def migrate(self):
        raise NotImplementedError

    def drop_tables(self):
        raise NotImplementedError
