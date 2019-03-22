"""
doc string goes here
"""

__all__ = ['BaseEntity', 'CurrencyEntity', 'CurrencyExchangeRate']

# Standard library imports.
import decimal
import datetime

# Related third party imports.

# Local application/library specific imports.


class BaseEntity:
    pass


class CurrencyEntity(BaseEntity):
    def __init__(self, name, code):
        self._name = name
        self._code = code

    def get_name(self):
        return self._name

    def get_code(self):
        return self._code

    def __str__(self):
        return self._code or self._name


class CurrencyExchangeRate(BaseEntity):
    def __init__(self, provider, from_currency, to_currency, exchange_rate, on_date):
        assert isinstance(from_currency, CurrencyEntity)
        assert isinstance(to_currency, CurrencyEntity)
        assert isinstance(exchange_rate, decimal.Decimal)
        assert isinstance(on_date, datetime.date)

        self._provider = provider
        self._from_currency = from_currency
        self._to_currency = to_currency
        self._exchange_rate = exchange_rate
        self._on_date = on_date

    def swap(self):
        exchange_rate = decimal.Decimal(1.0) / self._exchange_rate
        new_rate = CurrencyExchangeRate(self._provider, self._to_currency, self._from_currency, exchange_rate, self._on_date)
        return new_rate

    def convert(self, amount):
        if not isinstance(amount, decimal.Decimal):
            amount = decimal.Decimal(amount)

        result = amount * self._exchange_rate
        return result

    def get_provider(self):
        return self._provider

    def get_rate(self):
        return self._exchange_rate

    def get_from_currency(self):
        return self._from_currency

    def get_to_currency(self):
        return self._to_currency

    def get_on_date(self):
        return self._on_date
