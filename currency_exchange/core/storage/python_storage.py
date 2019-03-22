"""
doc string goes here
"""

__all__ = ['PurePythonStorage']

# Standard library imports.

# Related third party imports.

# Local application/library specific imports.
from currency_exchange.core.entities import CurrencyExchangeRate, CurrencyEntity
from .base import BaseStorage


class DictStorage:
    def __init__(self):
        self.providers = {}
        self.currencies = {}
        self.rates = {}


class PurePythonStorage(BaseStorage):
    _connection = None

    @property
    def connection(self):
        if self._connection is None:
            self._connection = DictStorage()
        return self._connection

    def migrate(self):
        pass

    def drop_tables(self):
        pass

    def store_rates(self, exchange_rates):
        assert all([isinstance(obj, CurrencyExchangeRate) for obj in exchange_rates])

        for rate in exchange_rates:
            provider_name = rate.get_provider()
            provider_data = self.connection.rates.setdefault(provider_name, {})

            on_date = rate.get_on_date()
            per_date_data = provider_data.setdefault(on_date, {})

            from_code = rate.get_from_currency().get_code()
            to_code = rate.get_to_currency().get_code()

            per_date_data[(from_code, to_code)] = rate.get_rate()

    def get_currencies(self, provider_names, currency_codes):
        result = {}

        for code in currency_codes:
            data = self.connection.currencies.get(code)

            if data:
                currency = CurrencyEntity(data[0], data[1])
            else:
                currency = CurrencyEntity(code, code)

            result[code] = currency

        return result

    def get_rates(self, provider_names, currency_code, to_currencies=None, on_date=None):
        result = []
        currency_pairs = [(currency_code, to_currency) for to_currency in to_currencies]
        currencies = self.get_currencies(None, to_currencies + [currency_code])

        for prov_name in provider_names:
            provider_data = self.connection.rates.get(prov_name)

            if provider_data:
                on_date_data = provider_data.get(on_date)

                if on_date_data:
                    for pair in currency_pairs:
                        rate = on_date_data.get(pair)

                        if rate:
                            from_currency = currencies.get(pair[0])
                            to_currency = currencies.get(pair[1])
                            exchange_rate = CurrencyExchangeRate(prov_name, from_currency, to_currency, rate, on_date)
                            result.append(exchange_rate)

        return result

    def store_currencies(self, currencies):
        assert all([isinstance(obj, CurrencyEntity) for obj in currencies])

        for currency in currencies:
            self.connection.currencies[currency.get_code()] = (currency.get_name(), currency.get_code())
